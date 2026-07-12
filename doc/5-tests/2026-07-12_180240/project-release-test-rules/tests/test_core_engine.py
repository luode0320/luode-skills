"""契约内核、原子投影和安全阻断的真实单元测试。"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.events import BaselineEvent, EventValidationError
from release_test_engine.model import IRValidationError, InterfaceIR, validate_ir
from release_test_engine.safety import SafetyViolation, assert_safe, check_operation
from release_test_engine.storage import BaselineStore, StorageError


class IRContractTests(unittest.TestCase):
    def test_fixture_is_valid_and_round_trips(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "valid_ir.yaml"
        document = yaml.safe_load(fixture.read_text(encoding="utf-8"))
        validate_ir(document)
        interface = InterfaceIR.from_dict(document["interfaces"][0])
        self.assertEqual(interface.to_dict()["operation_id"], "get_account")
        self.assertEqual(interface.to_dict()["parameters"][0]["location"], "path")
        self.assertNotIn("schema_version", interface.to_dict())

    def test_invalid_protocol_and_missing_contract_are_rejected(self) -> None:
        with self.assertRaises(IRValidationError) as context:
            validate_ir({"schema_version": "1.0", "project_fingerprint": "x", "interfaces": [{"protocol": "unknown"}]})
        self.assertIn("schema_version must be 2.0", str(context.exception))
        self.assertIn("interfaces[0].service_id is required", str(context.exception))
        with self.assertRaises(IRValidationError):
            validate_ir(None)


class AtomicStorageTests(unittest.TestCase):
    def test_append_and_project_are_replayable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = BaselineStore(Path(directory) / "baseline.yaml")
            event = store.append_event(BaselineEvent(run_id="run-1", event_type="interface.tested", payload={"status": "PASS"}))
            projected = store.project()
            self.assertEqual(projected["schema_version"], "2.0")
            self.assertEqual(projected["events"][0]["event_id"], event.event_id)
            self.assertEqual(store.read_events()[0].run_id, "run-1")
            store.project()
            self.assertEqual(len(store.read_baseline()["events"]), 1)

    def test_projector_failure_keeps_existing_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.yaml"
            store = BaselineStore(path)
            store.write_atomic({"schema_version": "2.0", "value": "old"})
            store.append_event(BaselineEvent(run_id="run-1", event_type="bad", payload={}))

            def fail(_document, _event):
                raise RuntimeError("simulated projector failure")

            with self.assertRaises(RuntimeError):
                store.project(fail)
            self.assertEqual(store.read_baseline()["value"], "old")

    def test_invalid_event_does_not_append(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = BaselineStore(Path(directory) / "baseline.yaml")
            with self.assertRaises(EventValidationError):
                store.append_event({"run_id": "x", "payload": {}})
            self.assertFalse(store.events_path.exists())


class SafetyTests(unittest.TestCase):
    def test_blocks_extreme_operations(self) -> None:
        for operation in (
            "DROP TABLE accounts",
            "TRUNCATE TABLE accounts",
            "terraform destroy -auto-approve",
            {"command": "shutil.rmtree(project_root)"},
            "rm -rf project",
            "git clean -fdx",
        ):
            decision = check_operation(operation)
            self.assertFalse(decision.allowed, operation)
            with self.assertRaises(SafetyViolation):
                assert_safe(operation)

    def test_allows_normal_business_delete_and_requires_local(self) -> None:
        self.assertTrue(check_operation({"method": "DELETE", "path": "/orders/123"}).allowed)
        self.assertFalse(check_operation("GET /health", environment="production").allowed)
        assert_safe({"method": "POST", "path": "/orders"}, environment="local")


if __name__ == "__main__":
    unittest.main()
