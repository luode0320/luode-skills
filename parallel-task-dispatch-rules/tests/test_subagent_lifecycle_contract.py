"""子 Agent 生命周期规则的纯标准库契约测试。"""

from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
LIFECYCLE = (SKILL_ROOT / "references" / "subagent-lifecycle-and-reconciliation.md").read_text(
    encoding="utf-8"
)
BLOCKERS = (SKILL_ROOT / "references" / "blockers-and-fallbacks.md").read_text(encoding="utf-8")
SCHEMA = (SKILL_ROOT / "references" / "launch-plan-schema.md").read_text(encoding="utf-8")
TEMPLATES = (SKILL_ROOT / "references" / "subagent-task-templates.md").read_text(encoding="utf-8")
PROMPT = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
TERMINAL_STATES = {"completed", "failed", "canceled", "interrupted", "abandoned"}
REAL_CLOSE_ACTIONS = {"close_agent", "equivalent_release"}


def reconcile(instances: list[dict[str, object]], needed_ids: set[str] | None = None) -> dict[str, object]:
    """归纳当前会话实例的回收动作和数量。

    [参数] instances：扫描实例；needed_ids：当前任务仍需保留的实例 ID。
    [返回] 包含逐实例动作、数量、批次门禁和告警的字典。
    最近修改时间：2026-07-25 15:05:19，建立生命周期规则的可执行状态模型。
    """
    # 1. 只处理当前会话非根实例，并按 agent_id 幂等保留最新事实。
    latest: dict[str, dict[str, object]] = {}
    for instance in instances:
        if instance.get("is_root") or not instance.get("current_session", True):
            continue
        latest[str(instance["agent_id"])] = instance

    # 2. 按是否仍被需要、执行状态和真实关闭双重判定归纳逐实例结果。
    needed_ids = needed_ids or set()
    rows: list[dict[str, object]] = []
    for agent_id, instance in latest.items():
        state = str(instance["execution_state"])
        needed = agent_id in needed_ids
        close_action = str(instance.get("close_action", "none"))
        close_tool_success = bool(instance.get("close_tool_success", False))
        active_after_verification = bool(instance.get("active_after_verification", state == "running"))
        closed = close_action in REAL_CLOSE_ACTIONS and close_tool_success and not active_after_verification
        if needed:
            required_action = "preserve"
        elif state == "running":
            required_action = "stop_then_close"
        elif state in TERMINAL_STATES:
            required_action = "close"
        else:
            required_action = "warn_unknown"
        rows.append(
            {
                "agent_id": agent_id,
                "state": state,
                "needed": needed,
                "required_action": required_action,
                "closed": closed,
                "active_after_verification": active_after_verification,
            }
        )

    # 3. 所有数量都从去重台账重算，未关闭实例直接形成下一批门禁。
    unclosed = [row for row in rows if not row["needed"] and not row["closed"]]
    warnings = [str(row["agent_id"]) for row in unclosed]
    return {
        "rows": rows,
        "terminal_count": sum(row["state"] in TERMINAL_STATES for row in rows),
        "completed_count": sum(row["state"] == "completed" for row in rows),
        "closed_count": sum(bool(row["closed"]) for row in rows),
        "final_sweep_count": len(rows),
        "still_active_count": sum(bool(row["active_after_verification"]) for row in rows),
        "unclosed_count": len(unclosed),
        "warning_agent_ids": warnings,
        "can_start_next_batch": not unclosed,
    }


class SubagentLifecycleContractTests(unittest.TestCase):
    """验证双扫描、真实关闭和数量对账契约。"""

    def test_rule_assets_expose_all_mandatory_contracts(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，锁定规则资产关键语句。"""
        # 1. 主规则必须同时暴露三段扫描、双重关闭判定和完整数量字段。
        for phrase in ("进入前预检", "批次回收", "终局扫描", "interrupt_agent", "重新枚举复查"):
            self.assertIn(phrase, SKILL)
        for field in ("终态数", "终局扫描数", "仍活跃数", "未关闭数", "告警原因"):
            self.assertIn(field, SKILL)
        # 2. 唯一细则和默认提示词必须同步真实关闭与无能力告警边界。
        self.assertIn("只有同时满足以下两个条件", LIFECYCLE)
        self.assertIn("平台未提供真实关闭能力", LIFECYCLE)
        self.assertIn("平台无关闭能力时仅告警", PROMPT)
        self.assertIn("已启动实例回收", BLOCKERS)
        self.assertIn("关闭数不要求等于完成数", SCHEMA)
        self.assertIn("关闭工具结果", TEMPLATES)
        self.assertNotIn("并发上限与空闲回收（强制）", SKILL + SCHEMA)
        self.assertNotIn("已关闭线程数”与“已完成线程数”一致", SCHEMA)

    def test_needed_running_agent_is_preserved(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，覆盖仍需执行实例的保留路径。"""
        result = reconcile([{"agent_id": "agent-a", "execution_state": "running"}], {"agent-a"})

        self.assertEqual(result["rows"][0]["required_action"], "preserve")
        self.assertTrue(result["can_start_next_batch"])

    def test_terminal_agent_closes_only_after_successful_verification(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，覆盖终态实例真实关闭。"""
        result = reconcile(
            [{"agent_id": "agent-a", "execution_state": "completed", "close_action": "close_agent", "close_tool_success": True, "active_after_verification": False}]
        )

        self.assertEqual(result["closed_count"], 1)
        self.assertEqual(result["unclosed_count"], 0)

    def test_running_agent_requires_stop_then_close(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，覆盖运行实例的回收顺序。"""
        result = reconcile([{"agent_id": "agent-a", "execution_state": "running"}])

        self.assertEqual(result["rows"][0]["required_action"], "stop_then_close")
        self.assertFalse(result["can_start_next_batch"])

    def test_interrupt_does_not_count_as_close(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，拒绝把中断计作关闭。"""
        result = reconcile(
            [{"agent_id": "agent-a", "execution_state": "interrupted", "close_action": "interrupt_agent", "close_tool_success": True, "active_after_verification": False}]
        )

        self.assertEqual(result["closed_count"], 0)
        self.assertEqual(result["unclosed_count"], 1)

    def test_close_success_without_verification_stays_unclosed(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，锁定关闭后复查门禁。"""
        result = reconcile(
            [{"agent_id": "agent-a", "execution_state": "completed", "close_action": "close_agent", "close_tool_success": True, "active_after_verification": True}]
        )

        self.assertEqual(result["closed_count"], 0)
        self.assertFalse(result["can_start_next_batch"])

    def test_close_failure_stays_unclosed(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，覆盖关闭工具失败。"""
        result = reconcile(
            [{"agent_id": "agent-a", "execution_state": "failed", "close_action": "close_agent", "close_tool_success": False, "active_after_verification": False}]
        )

        self.assertEqual(result["closed_count"], 0)
        self.assertEqual(result["unclosed_count"], 1)

    def test_unavailable_close_only_warns_and_blocks_next_batch(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，覆盖无关闭工具的告警策略。"""
        result = reconcile([{"agent_id": "agent-a", "execution_state": "completed"}])

        self.assertEqual(result["unclosed_count"], 1)
        self.assertEqual(result["warning_agent_ids"], ["agent-a"])
        self.assertFalse(result["can_start_next_batch"])

    def test_repeated_scan_is_idempotent(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，验证重复扫描不重复累计。"""
        instances = [
            {"agent_id": "agent-a", "execution_state": "running"},
            {"agent_id": "agent-a", "execution_state": "completed", "close_action": "close_agent", "close_tool_success": True, "active_after_verification": False},
        ]

        result = reconcile(instances)
        self.assertEqual(result["final_sweep_count"], 1)
        self.assertEqual(result["closed_count"], 1)

    def test_root_and_other_session_agents_are_protected(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，会话范围与根实例保护。"""
        instances = [
            {"agent_id": "root", "execution_state": "running", "is_root": True},
            {"agent_id": "other", "execution_state": "completed", "current_session": False},
            {"agent_id": "local", "execution_state": "completed"},
        ]

        result = reconcile(instances)
        self.assertEqual(result["final_sweep_count"], 1)
        self.assertEqual(result["warning_agent_ids"], ["local"])

    def test_mixed_terminal_states_reconcile_independently(self) -> None:
        """[参数] 无；[返回] None；最近修改时间：2026-07-25 15:05:19，覆盖失败取消中断与放弃终态。"""
        instances = [
            {"agent_id": state, "execution_state": state, "close_action": "equivalent_release", "close_tool_success": True, "active_after_verification": False}
            for state in ("failed", "canceled", "interrupted", "abandoned")
        ]

        result = reconcile(instances)
        self.assertEqual(result["terminal_count"], 4)
        self.assertEqual(result["completed_count"], 0)
        self.assertEqual(result["closed_count"], 4)


if __name__ == "__main__":
    unittest.main()
