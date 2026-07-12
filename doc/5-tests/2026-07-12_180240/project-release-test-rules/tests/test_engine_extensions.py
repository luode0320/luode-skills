"""通用上线测试引擎扩展能力的契约测试。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.auth import AuthResolutionError, resolve_auth
from release_test_engine.dependency_diagnostics import diagnose
from release_test_engine.gate import aggregate_gate
from release_test_engine.migrate_baseline import migrate_v1_to_v2
from release_test_engine.model import InterfaceIR
from release_test_engine.parameter_store import ParameterCandidate, ParameterStore, namespace_key
from release_test_engine.topology import TopologyError, ordered_nodes


class ParameterStoreTests(unittest.TestCase):
    def test_namespace_isolation_and_priority(self) -> None:
        store = ParameterStore()
        left = namespace_key("svc", "get", "query", "id")
        right = namespace_key("svc", "post", "body", "id")
        store.put(ParameterCandidate(left, "low", "generated", confidence=0.99))
        store.put(ParameterCandidate(left, "high", "reusable", confidence=0.5))
        store.put(ParameterCandidate(right, "other", "reusable", confidence=1.0))
        self.assertEqual("high", store.best(left, source_priority=("reusable", "generated")).value)
        self.assertEqual(1, len(store.candidates(right)))
        self.assertEqual("***", ParameterCandidate(left, "secret", "env", sensitive=True).to_trace()["value_masked"])


class AuthAndTopologyTests(unittest.TestCase):
    def test_auth_requires_local_reference_and_masks_secret(self) -> None:
        handle = resolve_auth({"token_env": "TOKEN", "header": "X-Api-Key", "prefix": ""}, environ={"TOKEN": "secret"})
        self.assertEqual("***", handle.masked()["headers"]["X-Api-Key"])
        with self.assertRaises(AuthResolutionError):
            resolve_auth({"token_env": "TOKEN"}, environment="production", environ={"TOKEN": "secret"})
        with self.assertRaises(AuthResolutionError):
            resolve_auth({"token_env": "MISSING"}, environ={})

    def test_confidence_order_and_cycle_and_dependency_diagnostics(self) -> None:
        edges = [{"provider": "a", "consumer": "b", "confidence": 0.9}, {"provider": "b", "consumer": "c", "confidence": 0.4}]
        self.assertEqual(["a", "c", "b"], ordered_nodes(["c", "b", "a"], edges, min_confidence=0.5))
        with self.assertRaises(TopologyError):
            ordered_nodes(["a", "b"], [{"provider": "a", "consumer": "b"}, {"provider": "b", "consumer": "a"}], min_confidence=0.5)
        blocked = diagnose({"operation_id": "provider", "status": "FAIL"}, "consumer")
        self.assertEqual("BLOCKED_BY_DEPENDENCY", blocked["failure_type"])
        unresolved = diagnose({"operation_id": "provider", "status": "PASS"}, "consumer", missing_fields=["id"])
        self.assertEqual("PARAM_UNRESOLVED", unresolved["failure_type"])


class GateAndMigrationTests(unittest.TestCase):
    def test_p0_p1_p2_truth_table(self) -> None:
        interfaces = [
            InterfaceIR("fp", "svc", "critical", "http", {}, risk="P0"),
            InterfaceIR("fp", "svc", "important", "http", {}, risk="P1"),
            InterfaceIR("fp", "svc", "minor", "http", {}, risk="P2"),
        ]
        self.assertEqual("FAIL", aggregate_gate([{"operation_id": "critical", "status": "FAIL"}], interfaces)["gate"])
        self.assertEqual("PARTIAL", aggregate_gate([{ "operation_id": "important", "status": "FAIL"}], interfaces)["gate"])
        self.assertEqual("PARTIAL", aggregate_gate([], interfaces, unsupported=[{"protocol": "grpc"}])["gate"])

    def test_v1_migration_keeps_evidence_and_source(self) -> None:
        migrated = migrate_v1_to_v2({"schema_version": "1.0", "results": []}, project_fingerprint="fp", source_revision="r1")
        self.assertEqual("2.0", migrated["schema_version"])
        self.assertEqual("r1", migrated["source_revision"])
        self.assertEqual("migration", migrated["evidence"][-1]["type"])


if __name__ == "__main__":
    unittest.main()
