"""C10-02 doctor、pipeline、runtime matrix 与门禁合同回归。"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.cli import run_doctor, run_pipeline
from release_test_engine.discovery import DiscoveryResult
from release_test_engine.gate import aggregate_gate
from release_test_engine.model import InterfaceIR


def _fixture_interface(*, risk: str = "P2", cleanup: bool = False) -> InterfaceIR:
    fixture: dict[str, object] = {
        "status": "PASS",
        "body": {"ok": True},
        "local_provenance": True,
        "run_id": "fixture-run",
        "startup_handle": "fixture-handle",
        "handler_ref": "local.fixture.handler",
    }
    if cleanup:
        fixture["cleanup_ref"] = "local.fixture.cleanup"
    return InterfaceIR(
        "fixture-fingerprint",
        "fixture-service",
        "event_operation",
        "event",
        {"target_ref": "local_config", "fixture_response": fixture},
        risk=risk,
    )


class RuntimeReportContractTests(unittest.TestCase):
    """所有样本仅使用 local 临时目录，禁止外部服务连接。"""

    def test_mapping_strict_fixture_is_transmitted_and_runtime_failure_is_reported(self) -> None:
        interface = _fixture_interface()
        discovery = DiscoveryResult("fixture-fingerprint", (interface,), ())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "artifacts"
            with patch("release_test_engine.cli.discover_project", return_value=discovery):
                result = run_pipeline(
                    {"project_root": root, "output_dir": output, "strict_fixture": True, "strict_contracts": False},
                    environment="local",
                )
            self.assertEqual("PARTIAL", result["status"])
            self.assertTrue(result["strict_fixture"])
            self.assertFalse(result["strict_contracts"])
            self.assertEqual("FIXTURE_CLEANUP_UNEXECUTABLE", result["gate"]["results"][0]["failure_type"])
            matrix = yaml.safe_load((output / "runtime-matrix.yaml").read_text(encoding="utf-8"))
            self.assertEqual(result["run_id"], matrix["run_id"])
            entry = matrix["entries"][0]
            self.assertEqual("event_operation", entry["operation_id"])
            self.assertEqual("pending", entry["execution_status"])
            self.assertEqual("FIXTURE_CLEANUP_UNEXECUTABLE", entry["failure_type"])
            self.assertEqual("pending", entry["capability_status"])
            self.assertEqual("local", entry["local_provenance"])

    def test_mapping_strict_contracts_blocks_missing_contract_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "openapi.yaml").write_text(
                yaml.safe_dump({"openapi": "3.0.3", "info": {"title": "local", "version": "1"}, "paths": {}}, sort_keys=False),
                encoding="utf-8",
            )
            with tempfile.TemporaryDirectory() as output_directory:
                result = run_pipeline(
                    {"project_root": root, "output_dir": Path(output_directory), "strict_contracts": True},
                    environment="local",
                    dry_run=True,
                )
            self.assertEqual("BLOCKED", result["status"])
            self.assertTrue(result["strict_contracts"])

    def test_pipeline_uses_one_run_id_for_fixture_request_cleanup_and_report(self) -> None:
        observed: list[str] = []

        def startup(run_id: str) -> str:
            observed.append("startup:" + run_id)
            return "started"

        def handler(run_id: str) -> dict[str, object]:
            observed.append("handler:" + run_id)
            return {"status": "PASS", "body": {"ok": True}}

        def cleanup(run_id: str) -> None:
            observed.append("cleanup:" + run_id)

        fixture = {
            "status": "PASS",
            "body": {"ok": True},
            "local_provenance": True,
            "run_id": "fixture-static-id",
            "startup_handle": lambda: "fixture-handle",
            "startup_callback": startup,
            "handler": handler,
            "cleanup_callback": cleanup,
        }
        interface = InterfaceIR("fixture-fingerprint", "fixture-service", "event_operation", "event", {"target_ref": "local_config", "fixture_response": fixture})
        discovery = DiscoveryResult("fixture-fingerprint", (interface,), ())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "artifacts"
            with patch("release_test_engine.cli.discover_project", return_value=discovery):
                result = run_pipeline({"project_root": root, "output_dir": output, "strict_fixture": True}, environment="local")
            report = json.loads((output / "release-test-report.json").read_text(encoding="utf-8"))
        run_id = result["run_id"]
        self.assertEqual("PASS", result["status"])
        self.assertEqual([f"startup:{run_id}", f"handler:{run_id}", f"cleanup:{run_id}"], observed)
        item = report["results"][0]
        request = json.loads(item["request"])
        self.assertEqual(run_id, request["run_id"])
        self.assertEqual(run_id, item["evidence"]["run_id"])
        self.assertEqual(run_id, report["run_id"])

    def test_doctor_mapping_strict_fixture_prechecks_cleanup_callback(self) -> None:
        interface = _fixture_interface()
        discovery = DiscoveryResult("fixture-fingerprint", (interface,), ())
        with tempfile.TemporaryDirectory() as directory, patch("release_test_engine.cli.discover_project", return_value=discovery):
            result = run_doctor({"project_root": Path(directory), "strict_fixture": True}, environment="local")
        self.assertEqual("PENDING", result["status"])
        self.assertTrue(result["strict_fixture"])
        matrix = result["adapter_matrix"]["event"]
        self.assertEqual("pending", matrix["execution_status"])
        self.assertEqual("FIXTURE_CLEANUP_UNEXECUTABLE", matrix["failure_type"])

    def test_gate_blocks_p0_p1_runtime_and_cleanup_failures_but_keeps_generic_p1_partial(self) -> None:
        p1 = _fixture_interface(risk="P1")
        p2 = _fixture_interface(risk="P2")
        cleanup = {"operation_id": "event_operation", "status": "BLOCKED", "failure_type": "FIXTURE_CLEANUP_FAILED", "reason": "cleanup failed"}
        self.assertEqual("FAIL", aggregate_gate([cleanup], [p1])["gate"])
        runtime = {"operation_id": "event_operation", "status": "PENDING", "failure_type": "UNSUPPORTED_ADAPTER", "reason": "missing runtime"}
        self.assertEqual("FAIL", aggregate_gate([runtime], [p1])["gate"])
        self.assertEqual("PARTIAL", aggregate_gate([runtime], [p2])["gate"])
        generic = {"operation_id": "event_operation", "status": "FAIL", "failure_type": "BUSINESS_ERROR", "reason": "expected contract failure"}
        self.assertEqual("PARTIAL", aggregate_gate([generic], [p1])["gate"])


if __name__ == "__main__":
    unittest.main()
