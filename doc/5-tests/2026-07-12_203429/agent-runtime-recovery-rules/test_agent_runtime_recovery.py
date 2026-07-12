"""验证统一智能体运行期恢复规则的协议与职责边界。"""

from __future__ import annotations

import json
import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOT = ROOT / "agent-runtime-recovery-rules"


def load_state_module():
    """Load the standard-library checkpoint implementation from the skill asset."""

    module_path = SKILL_ROOT / "scripts/recovery_state.py"
    spec = importlib.util.spec_from_file_location("recovery_state", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class AgentRuntimeRecoveryContractTests(unittest.TestCase):
    """检查恢复协议的核心资产和安全约束。"""

    def test_required_assets_exist(self) -> None:
        required = (
            "SKILL.md",
            "references/recovery-state-machine.md",
            "references/adapter-contract.schema.json",
            "references/platform-capability-matrix.md",
            "references/execution-failure-casebook.md",
        )
        missing = [item for item in required if not (SKILL_ROOT / item).is_file()]
        self.assertEqual([], missing)

    def test_adapter_schema_is_platform_neutral_and_safe(self) -> None:
        schema_path = SKILL_ROOT / "references/adapter-contract.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        properties = schema["properties"]
        self.assertIn("platform_id", properties)
        self.assertIn("adapter_id", properties)
        self.assertIn("components", properties)
        self.assertIn("operations", properties)
        self.assertIn("limits", properties)
        self.assertIn("checkpoint_policy", properties)
        component_properties = properties["components"]["items"]["properties"]
        self.assertIn("component_kind", component_properties)
        self.assertIn("capability_level", component_properties)
        self.assertIn("idempotency_classes", component_properties)
        self.assertEqual({0, 1, 2, 3, 4, 5}, set(range(component_properties["capability_level"]["minimum"], component_properties["capability_level"]["maximum"] + 1)))

    def test_protocol_contains_safety_invariants(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        state_text = (SKILL_ROOT / "references/recovery-state-machine.md").read_text(encoding="utf-8")
        combined = f"{skill_text}\n{state_text}"
        for phrases in (
            ("non-idempotent",),
            ("single-flight",),
            ("cooldown", "冷却"),
            ("manual_handoff",),
            ("checkpoint",),
            ("capability",),
        ):
            self.assertTrue(any(phrase in combined for phrase in phrases), phrases)

    def test_runtime_owner_is_referenced_by_existing_routes(self) -> None:
        routing = (ROOT / "execution-failure-learning-rules/references/classification-and-routing.md").read_text(encoding="utf-8")
        mcp = (ROOT / "mcp-installation-rules/SKILL.md").read_text(encoding="utf-8")
        plugin = (ROOT / "plugin-installation-rules/SKILL.md").read_text(encoding="utf-8")
        for phrase in ("agent-runtime-recovery-rules", "mcp_runtime_transport", "plugin_runtime_unhealthy", "agent_host_unhealthy"):
            self.assertIn(phrase, routing)
        self.assertIn("agent-runtime-recovery-rules", mcp)
        self.assertIn("agent-runtime-recovery-rules", plugin)

    def test_checkpoint_state_machine_and_single_flight(self) -> None:
        state = load_state_module()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            state.create_checkpoint(path, {
                "recovery_id": "r-1",
                "task_id_hash": "task-hash",
                "component_id": "local-mcp",
                "scope": "task",
                "idempotency_class": "read_only",
            })
            state.claim(path, "r-1")
            with self.assertRaises(RuntimeError):
                state.claim(path, "r-2")
            state.transition(path, "diagnosed")
            state.transition(path, "recovering")
            state.transition(path, "reconnected")
            state.transition(path, "verified")
            state.transition(path, "manual_handoff")
            with self.assertRaises(ValueError):
                state.transition(path, "healthy")

    def test_checkpoint_rejects_sensitive_fields(self) -> None:
        state = load_state_module()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            with self.assertRaises(ValueError):
                state.create_checkpoint(path, {
                    "recovery_id": "r-1",
                    "task_id_hash": "task-hash",
                    "component_id": "local-mcp",
                    "scope": "task",
                    "idempotency_class": "read_only",
                    "token": "must-not-persist",
                })

    def test_checkpoint_hashes_scope_and_rejects_extra_fields(self) -> None:
        """验证作用域脱敏和检查点白名单。

        [参数] 无
        [返回] 无；断言失败时测试失败
        最近修改时间：2026-07-12 22:40:00；补齐 scope_hash 与业务字段拒绝证据。
        """

        state = load_state_module()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            record = state.create_checkpoint(path, {
                "recovery_id": "r-scope",
                "task_id_hash": "task-hash",
                "component_id": "local-mcp",
                "scope": "local_fixture/transport",
                "idempotency_class": "read_only",
            })
            self.assertIn("scope_hash", record)
            self.assertNotIn("scope", record)
            self.assertEqual(record["scope_hash"], state.read_checkpoint(path)["scope_hash"])
            with self.assertRaises(ValueError):
                state.create_checkpoint(path, {
                    "recovery_id": "r-extra",
                    "task_id_hash": "task-hash",
                    "component_id": "local-mcp",
                    "scope": "local_fixture/transport",
                    "idempotency_class": "read_only",
                    "business_data": "must-not-persist",
                })

    def test_checkpoint_rejects_expired_and_damaged_records(self) -> None:
        """验证检查点 TTL 到期和损坏 JSON 均拒绝读取。

        [参数] 无
        [返回] 无；断言失败时测试失败
        最近修改时间：2026-07-12 22:40:00；补齐 TTL 与损坏记录负向证据。
        """

        state = load_state_module()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            record = state.create_checkpoint(path, {
                "recovery_id": "r-expired",
                "task_id_hash": "task-hash",
                "component_id": "local-mcp",
                "scope": "local_fixture/transport",
                "idempotency_class": "read_only",
            }, ttl_seconds=1)
            expired_now = datetime.fromisoformat(record["expires_at"]) + timedelta(seconds=1)
            with self.assertRaises(ValueError):
                state.read_checkpoint(path, now=expired_now)
            path.write_text("{broken-json", encoding="utf-8")
            with self.assertRaises(ValueError):
                state.read_checkpoint(path, now=datetime.now(timezone.utc))

    def test_resumed_checkpoint_can_close_to_healthy(self) -> None:
        """验证 L5 续接成功后检查点可进入 healthy 终态。

        [参数] 无
        [返回] 无；断言失败时测试失败
        最近修改时间：2026-07-12 22:40:00；同步状态机文档与实现终态。
        """

        state = load_state_module()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            state.create_checkpoint(path, {
                "recovery_id": "r-resume",
                "task_id_hash": "task-hash",
                "component_id": "local-host",
                "scope": "local_fixture/host",
                "idempotency_class": "read_only",
            })
            for target in ("diagnosed", "recovering", "restarted", "verified", "resumed", "healthy"):
                state.transition(path, target)
            self.assertEqual("healthy", state.read_checkpoint(path)["state"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
