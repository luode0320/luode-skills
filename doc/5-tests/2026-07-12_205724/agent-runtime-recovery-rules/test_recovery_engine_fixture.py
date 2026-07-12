"""使用进程内 local adapter fixture 验证运行期恢复协议的真实动作边界。"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOT = ROOT / "agent-runtime-recovery-rules"
SCHEMA_PATH = SKILL_ROOT / "references" / "adapter-contract.schema.json"


def load_state_module():
    """加载运行期 skill 提供的标准库检查点实现。"""

    module_path = SKILL_ROOT / "scripts" / "recovery_state.py"
    spec = importlib.util.spec_from_file_location("recovery_state_fixture", module_path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load state module: {module_path}")
    spec.loader.exec_module(module)
    return module


def load_engine_module():
    """加载统一恢复编排器，确保 fixture 测试覆盖真实 RecoveryEngine。"""

    module_path = SKILL_ROOT / "scripts" / "recovery_engine.py"
    spec = importlib.util.spec_from_file_location("recovery_engine_fixture", module_path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load engine module: {module_path}")
    spec.loader.exec_module(module)
    return module


class LocalAdapterFixture:
    """只在进程内记录动作的 local adapter，不创建端口或访问外部服务。"""

    _FORBIDDEN_SEGMENTS = {"test", "staging", "pre", "release", "prod", "production"}

    def __init__(self) -> None:
        self.provenance = "local"
        self.action_log: list[tuple[str, str]] = []
        self._probe_counts: defaultdict[str, int] = defaultdict(int)
        self._recovered: set[str] = set()
        self.resume_criterion_verified = True
        self.components = {
            "local-observer": {
                "component_id": "local-observer",
                "component_kind": "other",
                "scope": "local_fixture/observer",
                "capability_level": 0,
                "capabilities": ["probe"],
                "idempotency_classes": ["read_only"],
            },
            "local-transport": {
                "component_id": "local-transport",
                "component_kind": "mcp",
                "scope": "local_fixture/transport",
                "capability_level": 2,
                "capabilities": ["probe", "reconnect", "wait_ready"],
                "idempotency_classes": ["read_only", "idempotent"],
            },
            "local-plugin": {
                "component_id": "local-plugin",
                "component_kind": "plugin",
                "scope": "local_fixture/plugin",
                "capability_level": 3,
                "capabilities": ["probe", "reload", "wait_ready"],
                "idempotency_classes": ["read_only", "idempotent"],
            },
            "local-host": {
                "component_id": "local-host",
                "component_kind": "agent_host",
                "scope": "local_fixture/host",
                "capability_level": 4,
                "capabilities": ["probe", "restart", "wait_ready"],
                "idempotency_classes": ["read_only", "idempotent_with_key"],
            },
            "local-l5": {
                "component_id": "local-l5",
                "component_kind": "agent_host",
                "scope": "local_fixture/l5",
                "capability_level": 5,
                "capabilities": ["probe", "restart", "wait_ready", "checkpoint", "resume"],
                "idempotency_classes": ["read_only", "idempotent_with_key"],
            },
        }

    @property
    def contract(self) -> dict[str, object]:
        """返回符合 adapter schema 的平台无关契约。"""

        operation_names = ("probe", "reconnect", "reload", "restart", "wait_ready")
        operations = {
            name: {
                "supported": True,
                "entrypoint": f"local_fixture.{name}",
                "success_criteria": f"local fixture {name} returns ready",
            }
            for name in operation_names
        }
        operations.update(
            {
                "checkpoint": {
                    "supported": True,
                    "entrypoint": "local_fixture.checkpoint",
                    "success_criteria": "checkpoint contains only redacted control fields",
                },
                "resume": {
                    "supported": True,
                    "entrypoint": "local_fixture.resume",
                    "success_criteria": "resume verifies the original success criterion",
                },
            }
        )
        return {
            "adapter_id": "local.runtime.fixture",
            "platform_id": "local.agent",
            "version": "1.0",
            "components": list(self.components.values()),
            "operations": operations,
            "limits": {
                "max_probe_attempts": 1,
                "max_retries_per_level": 1,
                "cooldown_seconds": 600,
                "lock_ttl_seconds": 600,
            },
            "checkpoint_policy": {
                "enabled": True,
                "ttl_seconds": 600,
                "redaction_version": "1",
                "fields": [
                    "recovery_id",
                    "task_id_hash",
                    "component_id",
                    "scope_hash",
                    "idempotency_class",
                    "request_digest",
                    "created_at",
                    "expires_at",
                    "lock_key",
                ],
            },
        }

    def reset(self, component_id: str) -> None:
        """清理一个 fixture 组件的本轮动作和故障注入状态。"""

        self.action_log.clear()
        self._probe_counts[component_id] = 0
        self._recovered.discard(component_id)

    def probe(self, component_id: str) -> bool:
        """前两次探针模拟同一故障，恢复动作后返回健康。"""

        self._require_capability(component_id, "probe")
        self._probe_counts[component_id] += 1
        self.action_log.append(("probe", component_id))
        return component_id in self._recovered

    def invoke(
        self,
        operation_or_component_id: str,
        component_or_operation: dict[str, object] | str,
        request: object | None = None,
    ) -> dict[str, object]:
        """执行组件声明过的单个恢复动作并返回引擎可消费的结果。"""

        if request is None:
            component_id = operation_or_component_id
            operation = component_or_operation
            if not isinstance(operation, str):
                raise TypeError("direct fixture invocation requires an operation string")
        else:
            operation = operation_or_component_id
            if not isinstance(component_or_operation, dict):
                raise TypeError("engine invocation requires a component mapping")
            component_id = str(component_or_operation["component_id"])
        self._require_capability(component_id, operation)
        self.action_log.append((operation, component_id))
        if operation in {"reconnect", "reload", "restart"}:
            self._recovered.add(component_id)
            return {"ok": True, "reason": f"{operation}_ok"}
        if operation == "wait_ready":
            return {"ok": True, "healthy": True, "reason": "ready"}
        if operation == "probe":
            healthy = component_id in self._recovered
            return {"ok": healthy, "healthy": healthy, "reason": "healthy" if healthy else "unavailable"}
        if operation == "checkpoint":
            return {"ok": True, "reason": "checkpoint_saved"}
        if operation == "resume":
            return {
                "ok": True,
                "success_criterion_verified": self.resume_criterion_verified,
                "reason": "criterion_verified" if self.resume_criterion_verified else "criterion_unverified",
            }
        return {"ok": False, "reason": f"unsupported_fixture_operation:{operation}"}

    def _require_capability(self, component_id: str, operation: str) -> None:
        component = self.components[component_id]
        if operation not in component["capabilities"]:
            raise PermissionError(f"undeclared capability: {component_id}/{operation}")

    def assert_local(self) -> None:
        """拒绝非 local scope、入口或 provenance，防止 fixture 漂移到外部环境。"""

        if self.provenance != "local":
            raise AssertionError(f"unexpected provenance: {self.provenance}")
        contract = self.contract
        for component in contract["components"]:
            self._assert_local_reference(component["scope"])
        for operation in contract["operations"].values():
            self._assert_local_reference(operation["entrypoint"])

    def _assert_local_reference(self, value: str) -> None:
        lowered = value.lower()
        if not lowered.startswith("local"):
            raise AssertionError(f"non-local fixture reference: {value}")
        segments = {segment for segment in re.split(r"[^a-z0-9]+", lowered) if segment}
        forbidden = segments.intersection(self._FORBIDDEN_SEGMENTS)
        if forbidden:
            raise AssertionError(f"forbidden environment segment: {sorted(forbidden)}")


class RecoveryFixtureTests(unittest.TestCase):
    """通过本地 fixture 驱动检查点状态机并核对动作边界。"""

    @classmethod
    def setUpClass(cls) -> None:
        print("[START] local adapter recovery fixture tests")
        cls.state = load_state_module()
        cls.engine_module = load_engine_module()
        cls.fixture = LocalAdapterFixture()

    @classmethod
    def tearDownClass(cls) -> None:
        print("[END] local adapter recovery fixture tests; no external service started")

    def setUp(self) -> None:
        print(f"[CASE] {self._testMethodName}")

    def _engine_recover(
        self,
        component_id: str,
        *,
        idempotency_class: str = "read_only",
        idempotency_key: str | None = None,
    ) -> tuple[dict[str, object], list[tuple[str, str]]]:
        """通过真实 RecoveryEngine 执行一次 local fixture 恢复。"""

        component = self.fixture.components[component_id]
        self.fixture.reset(component_id)
        with tempfile.TemporaryDirectory(prefix="arr-engine-local-") as directory:
            request = self.engine_module.RecoveryRequest(
                recovery_id=f"engine-recovery-{component_id}",
                task_id_hash="local-engine-task-hash",
                component_id=component_id,
                scope=component["scope"],
                idempotency_class=idempotency_class,
                success_criterion="local fixture operation is ready",
                idempotency_key=idempotency_key,
            )
            engine = self.engine_module.RecoveryEngine(
                self.fixture,
                Path(directory) / "checkpoint.json",
            )
            result = engine.recover(request)
            return result, list(self.fixture.action_log)

    def _recover(
        self,
        component_id: str,
        *,
        idempotency_class: str = "read_only",
        require_resume: bool = False,
    ) -> tuple[dict[str, object], list[tuple[str, str]]]:
        """执行一次受控恢复流程，返回终态与动作日志。"""

        component = self.fixture.components[component_id]
        self.fixture.reset(component_id)
        with tempfile.TemporaryDirectory(prefix="arr-local-") as directory:
            checkpoint_path = Path(directory) / "checkpoint.json"
            recovery_id = f"recovery-{component_id}"
            self.state.create_checkpoint(
                checkpoint_path,
                {
                    "recovery_id": recovery_id,
                    "task_id_hash": "local-task-hash",
                    "component_id": component_id,
                    "scope": component["scope"],
                    "idempotency_class": idempotency_class,
                },
            )
            self.state.claim(checkpoint_path, recovery_id)
            self.assertFalse(self.fixture.probe(component_id))
            self.assertFalse(self.fixture.probe(component_id))
            record = self.state.transition(checkpoint_path, "diagnosed")

            if idempotency_class == "non_idempotent":
                record = self.state.transition(checkpoint_path, "manual_handoff")
                return record, list(self.fixture.action_log)

            operation = {
                2: "reconnect",
                3: "reload",
                4: "restart",
            }.get(component["capability_level"])
            if operation is None:
                record = self.state.transition(checkpoint_path, "manual_handoff")
                return record, list(self.fixture.action_log)

            self.state.transition(checkpoint_path, "recovering")
            self.fixture.invoke(component_id, operation)
            self.fixture.invoke(component_id, "wait_ready")
            self.assertTrue(self.fixture.probe(component_id))
            record = self.state.transition(
                checkpoint_path,
                {"reconnect": "reconnected", "reload": "reloaded", "restart": "restarted"}[operation],
            )
            record = self.state.transition(checkpoint_path, "verified")
            if require_resume and "resume" not in component["capabilities"]:
                record = self.state.transition(checkpoint_path, "blocked")
            else:
                record = self.state.transition(checkpoint_path, "manual_handoff")
            return record, list(self.fixture.action_log)

    def test_adapter_contract_is_platform_neutral_and_local(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        contract = self.fixture.contract
        self.fixture.assert_local()
        self.assertEqual({0, 2, 3, 4, 5}, {item["capability_level"] for item in contract["components"]})
        self.assertEqual(0, schema["properties"]["components"]["items"]["properties"]["capability_level"]["minimum"])
        self.assertEqual(5, schema["properties"]["components"]["items"]["properties"]["capability_level"]["maximum"])
        self.assertTrue(contract["operations"]["resume"]["supported"])

    def test_engine_l2_reconnect_is_real_and_hands_off_without_l5(self) -> None:
        result, actions = self._engine_recover("local-transport")
        self.assertEqual("manual_handoff", result["status"])
        self.assertEqual("tool_recovered_resume_not_supported", result["reason"])
        self.assertEqual(["reconnect"], result["attempted_actions"])
        self.assertEqual(["probe", "probe", "reconnect", "wait_ready", "probe"], [operation for operation, _ in actions])

    def test_engine_l3_reload_skips_undeclared_lower_action(self) -> None:
        result, actions = self._engine_recover("local-plugin")
        self.assertEqual("manual_handoff", result["status"])
        self.assertEqual(["reload"], result["attempted_actions"])
        self.assertEqual(["reconnect"], result["skipped_actions"])
        self.assertEqual(["probe", "probe", "reload", "wait_ready", "probe"], [operation for operation, _ in actions])

    def test_engine_l4_restart_skips_reload_and_has_no_resume(self) -> None:
        result, actions = self._engine_recover("local-host")
        self.assertEqual("manual_handoff", result["status"])
        self.assertEqual(["restart"], result["attempted_actions"])
        self.assertEqual(["reconnect", "reload"], result["skipped_actions"])
        self.assertNotIn(("resume", "local-host"), actions)

    def test_engine_non_idempotent_is_manual_handoff_without_replay(self) -> None:
        result, actions = self._engine_recover("local-transport", idempotency_class="non_idempotent")
        self.assertEqual("manual_handoff", result["status"])
        self.assertEqual("non_idempotent_or_unknown_operation", result["reason"])
        self.assertEqual([], result.get("attempted_actions", []))
        self.assertEqual(["probe", "probe"], [operation for operation, _ in actions])

    def test_engine_l5_resume_succeeds_when_criterion_is_verified(self) -> None:
        self.fixture.resume_criterion_verified = True
        result, actions = self._engine_recover("local-l5", idempotency_class="idempotent_with_key", idempotency_key="local-key")
        self.assertEqual("resumed", result["status"])
        self.assertEqual("checkpoint_resume_success_criterion_verified", result["reason"])
        self.assertEqual(["restart"], result["attempted_actions"])
        self.assertEqual(
            ["probe", "probe", "restart", "wait_ready", "probe", "checkpoint", "resume"],
            [operation for operation, _ in actions],
        )

    def test_engine_l5_unverified_criterion_stays_manual_handoff(self) -> None:
        self.fixture.resume_criterion_verified = False
        try:
            result, actions = self._engine_recover("local-l5", idempotency_class="idempotent_with_key", idempotency_key="local-key")
        finally:
            self.fixture.resume_criterion_verified = True
        self.assertEqual("manual_handoff", result["status"])
        self.assertEqual("resume_success_criterion_unverified", result["reason"])
        self.assertIn(("checkpoint", "local-l5"), actions)
        self.assertIn(("resume", "local-l5"), actions)

    def test_expired_checkpoint_is_rejected_by_read_and_claim(self) -> None:
        with tempfile.TemporaryDirectory(prefix="arr-expired-") as directory:
            checkpoint_path = Path(directory) / "checkpoint.json"
            self.state.create_checkpoint(
                checkpoint_path,
                {
                    "recovery_id": "expired-recovery",
                    "task_id_hash": "local-task-hash",
                    "component_id": "local-transport",
                    "scope": "local_fixture/transport",
                    "idempotency_class": "read_only",
                },
                ttl_seconds=1,
            )
            time.sleep(1.1)
            with self.assertRaisesRegex(ValueError, "checkpoint_expired"):
                self.state.read_checkpoint(checkpoint_path)
            with self.assertRaisesRegex(ValueError, "checkpoint_expired"):
                self.state.claim(checkpoint_path, "expired-recovery")

    def test_damaged_checkpoint_json_is_rejected_by_read_and_claim(self) -> None:
        with tempfile.TemporaryDirectory(prefix="arr-damaged-") as directory:
            checkpoint_path = Path(directory) / "checkpoint.json"
            checkpoint_path.write_text("{not-json", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "checkpoint_invalid"):
                self.state.read_checkpoint(checkpoint_path)
            with self.assertRaisesRegex(ValueError, "checkpoint_invalid"):
                self.state.claim(checkpoint_path, "damaged-recovery")

    def test_engine_missing_l5_resume_hook_is_manual_handoff(self) -> None:
        result, actions = self._engine_recover("local-host", idempotency_class="idempotent_with_key", idempotency_key="local-key")
        self.assertEqual("manual_handoff", result["status"])
        self.assertEqual("tool_recovered_resume_not_supported", result["reason"])
        self.assertNotIn(("resume", "local-host"), actions)
        self.assertNotIn("resume", self.fixture.components["local-host"]["capabilities"])

    def test_engine_l0_unsupported_component_is_blocked(self) -> None:
        result, actions = self._engine_recover("local-observer")
        self.assertEqual("blocked", result["status"])
        self.assertEqual("probe_capability_missing", result["reason"])
        self.assertEqual([], result.get("attempted_actions", []))
        self.assertEqual([], actions)

    def test_engine_scope_mismatch_is_blocked_without_adapter_action(self) -> None:
        """验证任务作用域不匹配时不调用任何 adapter 动作。

        [参数] 无
        [返回] 无；断言失败时测试失败
        最近修改时间：2026-07-12 22:55:00；补齐 scope 越权的真实负向证据。
        """

        self.fixture.reset("local-transport")
        with tempfile.TemporaryDirectory(prefix="arr-engine-scope-") as directory:
            request = self.engine_module.RecoveryRequest(
                recovery_id="engine-recovery-scope-mismatch",
                task_id_hash="local-engine-task-hash",
                component_id="local-transport",
                scope="local_fixture/other-component",
                idempotency_class="read_only",
                success_criterion="local fixture operation is ready",
            )
            result = self.engine_module.RecoveryEngine(self.fixture, Path(directory) / "checkpoint.json").recover(request)
        self.assertEqual("blocked", result["status"])
        self.assertEqual("component_scope_mismatch", result["reason"])
        self.assertEqual([], self.fixture.action_log)

    def test_l0_observer_only_hands_off(self) -> None:
        record, actions = self._recover("local-observer")
        self.assertEqual("manual_handoff", record["state"])
        self.assertEqual(["probe", "probe"], [operation for operation, _ in actions])

    def test_l2_reconnect_does_not_reload_or_restart(self) -> None:
        record, actions = self._recover("local-transport")
        self.assertEqual("manual_handoff", record["state"])
        operations = [operation for operation, _ in actions]
        self.assertEqual(["probe", "probe", "reconnect", "wait_ready", "probe"], operations)
        self.assertNotIn("reload", operations)
        self.assertNotIn("restart", operations)

    def test_l3_reload_does_not_restart(self) -> None:
        record, actions = self._recover("local-plugin")
        self.assertEqual("manual_handoff", record["state"])
        operations = [operation for operation, _ in actions]
        self.assertEqual(["probe", "probe", "reload", "wait_ready", "probe"], operations)
        self.assertNotIn("restart", operations)

    def test_l4_restart_waits_ready_without_claiming_resume(self) -> None:
        record, actions = self._recover("local-host")
        self.assertEqual("manual_handoff", record["state"])
        operations = [operation for operation, _ in actions]
        self.assertEqual(["probe", "probe", "restart", "wait_ready", "probe"], operations)
        self.assertNotIn("resume", operations)

    def test_single_flight_rejects_second_recovery_until_release(self) -> None:
        with tempfile.TemporaryDirectory(prefix="arr-local-lock-") as directory:
            checkpoint_path = Path(directory) / "checkpoint.json"
            self.state.create_checkpoint(
                checkpoint_path,
                {
                    "recovery_id": "recovery-one",
                    "task_id_hash": "local-task-hash",
                    "component_id": "local-transport",
                    "scope": "local_fixture/transport",
                    "idempotency_class": "read_only",
                },
            )
            self.state.claim(checkpoint_path, "recovery-one")
            with self.assertRaises(RuntimeError):
                self.state.claim(checkpoint_path, "recovery-two")
            self.state.release(checkpoint_path, "recovery-one")
            self.state.claim(checkpoint_path, "recovery-two")
            self.state.release(checkpoint_path, "recovery-two")

    def test_non_idempotent_call_always_manual_handoff_without_replay(self) -> None:
        record, actions = self._recover("local-transport", idempotency_class="non_idempotent")
        self.assertEqual("manual_handoff", record["state"])
        self.assertEqual(["probe", "probe"], [operation for operation, _ in actions])

    def test_missing_l5_resume_hook_is_blocked_after_l4_verification(self) -> None:
        """验证无 L5 组件能力时 L4 后仍不得伪造续接成功。

        [参数] 无
        [返回] 无；断言失败时测试失败
        最近修改时间：2026-07-12 22:45:00；说明全局 resume 声明与组件能力的边界。
        """

        record, actions = self._recover("local-host", require_resume=True)
        self.assertEqual("blocked", record["state"])
        self.assertIn(("restart", "local-host"), actions)
        self.assertNotIn(("resume", "local-host"), actions)
        self.assertNotIn("resume", self.fixture.components["local-host"]["capabilities"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
