"""非 HTTP 协议 local in-process fixture 与 execution matrix 回归。"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.adapters import adapter_matrix_status
from release_test_engine.cli import run_doctor
from release_test_engine.discovery import DiscoveryResult
from release_test_engine.model import InterfaceIR
from release_test_engine.runner import execute


class RuntimeMatrixTests(unittest.TestCase):
    """验证发现能力、显式 fixture 能力与真正执行状态不会混淆。"""

    @staticmethod
    def _interface(protocol: str, fixture: dict[str, object] | None = None) -> InterfaceIR:
        """[参数] protocol: 协议名；fixture: 显式 local fixture；[返回] 测试入口 IR；最近修改时间: 2026-07-12 20:15:00 复用统一 fixture 样本。"""

        entrypoint: dict[str, object] = {"target_ref": "local_config"}
        if fixture is not None:
            entrypoint["fixture_response"] = fixture
        return InterfaceIR("local-fixture-fp", "fixture-service", f"{protocol}_operation", protocol, entrypoint)

    def test_non_http_protocols_execute_with_explicit_local_fixture(self) -> None:
        """[参数] 无；[返回] 五类协议均有真实 fixture 结果；最近修改时间: 2026-07-12 20:15:00 覆盖 C06-02 local matrix。"""

        for protocol in ("grpc", "websocket", "message", "scheduler", "event"):
            result = execute(self._interface(protocol, {"status": "PASS", "body": {"ok": True}}), environment="local")
            self.assertEqual("PASS", result.status, protocol)
            self.assertEqual("fixture", result.evidence["transport"], protocol)
            self.assertEqual("in-process-fixture", result.evidence["execution_mode"], protocol)

        failed = execute(self._interface("websocket", {"status": "FAIL", "body": {"ok": False}}), environment="local")
        self.assertEqual("FAIL", failed.status)
        self.assertEqual("FIXTURE_STATUS", failed.failure_type)

    def test_missing_or_invalid_fixture_is_pending_and_never_passes(self) -> None:
        """[参数] 无；[返回] 缺失或非法 fixture 均结构化 PENDING；最近修改时间: 2026-07-12 20:15:00 防止伪造 PASS。"""

        missing = execute(self._interface("grpc"), environment="local")
        self.assertEqual("PENDING", missing.status)
        self.assertEqual("UNSUPPORTED_ADAPTER", missing.failure_type)

        no_status = execute(self._interface("grpc", {"body": {"ok": True}}), environment="local")
        self.assertEqual("PENDING", no_status.status)
        self.assertEqual("FIXTURE_STATUS_MISSING", no_status.failure_type)

        remote = execute(self._interface("grpc", {"status": "PASS", "transport": "http"}), environment="local")
        self.assertEqual("PENDING", remote.status)
        self.assertEqual("FIXTURE_TRANSPORT_INVALID", remote.failure_type)

    def test_matrix_reports_partial_fixture_and_pending_entry(self) -> None:
        """[参数] 无；[返回] matrix 同时暴露 fixture-ready 与 pending；最近修改时间: 2026-07-12 20:15:00 验证支持矩阵聚合。"""

        ready = self._interface("message", {"status": "PASS", "body": {"ack": True}})
        pending = self._interface("message")
        matrix = adapter_matrix_status("message", [ready, pending])
        self.assertEqual("ready", matrix["discovery_status"])
        self.assertEqual("partial", matrix["fixture_status"])
        self.assertEqual("partial", matrix["execution_status"])
        self.assertEqual(1, matrix["fixture_count"])
        self.assertEqual(1, matrix["pending_count"])
        self.assertEqual("ready", matrix["interfaces"][0]["fixture_status"])
        self.assertEqual("pending", matrix["interfaces"][1]["execution_status"])

    def test_doctor_uses_fixture_matrix_for_non_http_entry(self) -> None:
        """[参数] 无；[返回] doctor 对显式 fixture 给出 PASS；最近修改时间: 2026-07-12 20:15:00 验证 doctor 与 runner 状态一致。"""

        interface = self._interface("event", {"status": "PASS", "body": {"handled": True}})
        discovery = DiscoveryResult("local-fixture-fp", (interface,), ())
        with tempfile.TemporaryDirectory() as directory, patch("release_test_engine.cli.discover_project", return_value=discovery):
            result = run_doctor(Path(directory), environment="local")
        self.assertEqual("PASS", result["status"])
        matrix = result["adapter_matrix"]["event"]
        self.assertEqual("ready", matrix["discovery_status"])
        self.assertEqual("ready", matrix["fixture_status"])
        self.assertEqual("ready", matrix["execution_status"])
        self.assertEqual("builtin.fixture", matrix["runner"])

    def test_strict_fixture_requires_local_lifecycle_and_runs_cleanup(self) -> None:
        cleaned: list[str] = []

        def cleanup() -> None:
            cleaned.append("done")

        fixture = {"status": "PASS", "body": {"ok": True}, "local_provenance": True, "run_id": "run-local-1", "startup_handle": lambda: "fixture-handle", "handler": lambda params: {"ok": True}, "cleanup_callback": cleanup}
        result = execute(self._interface("grpc", fixture), environment="local", strict_fixture=True)
        self.assertEqual("PASS", result.status)
        self.assertEqual("PASS", result.evidence["cleanup_status"])
        self.assertEqual(["done"], cleaned)

        incomplete = {"status": "PASS", "body": {"ok": True}, "local_provenance": True, "run_id": "run-local-2", "startup_handle": lambda: "fixture-handle", "handler": lambda params: {"ok": True}}
        pending = execute(self._interface("grpc", incomplete), environment="local", strict_fixture=True)
        self.assertEqual("PENDING", pending.status)
        self.assertEqual("FIXTURE_CLEANUP_UNEXECUTABLE", pending.failure_type)

    def test_strict_lifecycle_callbacks_execute_for_each_protocol(self) -> None:
        """[参数] 无；[返回] 五协议均执行 startup/handler/cleanup；最近修改时间: 2026-07-13 01:10:00 固定 C10 callback 契约。"""

        for protocol in ("grpc", "websocket", "message", "scheduler", "event"):
            calls: list[str] = []

            def startup() -> str:
                calls.append("startup")
                return f"handle-{protocol}"

            def handler(params: dict[str, object]) -> dict[str, object]:
                calls.append("handler")
                return {"protocol": protocol, "params": dict(params), "ok": True}

            def cleanup() -> None:
                calls.append("cleanup")

            fixture = {
                "status": "PASS",
                "local_provenance": True,
                "run_id": "fixture-run-id",
                "startup_handle": startup,
                "handler": handler,
                "cleanup_callback": cleanup,
            }
            result = execute(self._interface(protocol, fixture), {"id": protocol}, environment="local", strict_fixture=True, run_id="pipeline-run-id")
            self.assertEqual("PASS", result.status, protocol)
            self.assertEqual({"protocol": protocol, "params": {"id": protocol}, "ok": True}, result.response["body"], protocol)
            self.assertEqual(["startup", "handler", "cleanup"], calls, protocol)
            self.assertEqual("pipeline-run-id", result.request["run_id"], protocol)
            self.assertEqual("pipeline-run-id", result.evidence["run_id"], protocol)
            self.assertEqual("PASS", result.evidence["cleanup_status"], protocol)

    def test_strict_fixture_rejects_external_entrypoint_reference(self) -> None:
        """[参数] 无；[返回] fixture 存在时入口级外部引用仍被阻断；最近修改时间: 2026-07-13 01:10:00 防止入口引用绕过 local gate。"""

        fixture = {
            "status": "PASS",
            "local_provenance": True,
            "run_id": "run-local-entrypoint",
            "startup_handle": lambda: "handle",
            "handler": lambda params: {"ok": True},
            "cleanup_callback": lambda: None,
        }
        interface = self._interface("grpc", fixture)
        interface.entrypoint["target_ref"] = "https://prod.invalid"
        result = execute(interface, environment="local", strict_fixture=True, run_id="pipeline-run-id")
        self.assertEqual("PENDING", result.status)
        self.assertEqual("LOCAL_CONFIG_PROVENANCE_INVALID", result.failure_type)

    def test_mapping_entries_preserve_strict_fixture_flag(self) -> None:
        """[参数] 无；[返回] mapping 入口不丢失 strict_fixture；最近修改时间: 2026-07-13 01:10:00 防止 CLI 映射降级为宽松模式。"""

        interface = self._interface("grpc", {"status": "PASS", "body": {"ok": True}})
        discovery = DiscoveryResult("local-fixture-fp", (interface,), ())
        with tempfile.TemporaryDirectory() as directory, patch("release_test_engine.cli.discover_project", return_value=discovery):
            result = run_doctor({"project_root": directory, "strict_fixture": True}, environment="local")
        self.assertTrue(result["strict_fixture"])
        self.assertEqual("PENDING", result["status"])

    def test_strict_fixture_cleanup_failure_blocks_release(self) -> None:
        def cleanup() -> None:
            raise RuntimeError("local fixture cleanup failed")

        fixture = {"status": "PASS", "body": {"ok": True}, "local_provenance": True, "run_id": "run-local-3", "startup_handle": lambda: "fixture-handle", "handler": lambda params: {"ok": True}, "cleanup_callback": cleanup}
        result = execute(self._interface("event", fixture), environment="local", strict_fixture=True)
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("FIXTURE_CLEANUP_FAILED", result.failure_type)
        self.assertEqual("FAIL", result.evidence["cleanup_status"])

    def test_strict_fixture_rejects_external_endpoint(self) -> None:
        fixture = {"status": "PASS", "body": {"ok": True}, "local_provenance": True, "run_id": "run-local-4", "startup_handle": lambda: "fixture-handle", "handler": lambda params: {"ok": True}, "cleanup_ref": "local.fixture.cleanup", "endpoint": "https://prod.invalid"}
        result = execute(self._interface("grpc", fixture), environment="local", strict_fixture=True)
        self.assertEqual("PENDING", result.status)
        self.assertEqual("FIXTURE_EXTERNAL_ENDPOINT", result.failure_type)


if __name__ == "__main__":
    unittest.main()
