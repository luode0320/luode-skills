import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_PATH = Path(__file__).with_name("fixtures") / "plan_output_cases.json"
WAIT_LOOP_TEST = REPO_ROOT / "doc" / "5-tests" / "2026-07-26_040607" / "plan_mode_wait_loop" / "test_plan_mode_wait_loop.py"


class PlanOutputContractTests(unittest.TestCase):
    # [参数] cls：测试类；[返回] 无；最近修改时间：2026-07-26 18:00:00，补齐计划出口回归测试注释。
    @classmethod
    def setUpClass(cls) -> None:
        # 1. 统一加载脱敏 fixture，保证每个断言使用同一份协议样本。
        cls.cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-07-26 18:00:00，锁定唯一 proposed_plan 出口。
    def test_plan_ready_has_only_one_complete_proposed_plan(self) -> None:
        case = self.cases["plan_ready"]
        visible = "\n".join(case["visible_messages"])
        # 1. 校验 Plan Mode 只保留完整计划标签，且未混入总结出口。
        self.assertEqual(case["mode"], "plan")
        self.assertEqual(case["hit_skills"].count("reasoning-summary-structure-rules"), 0)
        self.assertEqual(len(re.findall(r"<proposed_plan>", visible)), 1)
        self.assertEqual(len(re.findall(r"</proposed_plan>", visible)), 1)
        plan_body = visible.split("<proposed_plan>", 1)[1].split("</proposed_plan>", 1)[0].strip()
        self.assertTrue(plan_body, "proposed_plan 不能是空标签")
        for section in case["required_plan_sections"]:
            self.assertIn(section, plan_body)
        self.assertNotIn("# 📋 本轮总结", visible)
        self.assertNotIn("final_answer", visible)

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-07-26 18:00:00，锁定等待态冻结输出。
    def test_waiting_decision_freezes_visible_output(self) -> None:
        case = self.cases["plan_waiting"]
        # 1. 确认未决状态只能重发选择框，不得产生可见计划或总结。
        self.assertEqual(case["status"], "WAITING_DECISION")
        self.assertEqual(case["tool_calls"], ["request_user_input"])
        visible = "\n".join(case["visible_messages"])
        for token in case["forbidden_tokens"]:
            self.assertNotIn(token, visible)

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-07-26 18:10:00，接入永久等待状态模型回归。
    def test_wait_loop_behavior_model_passes(self) -> None:
        # 1. 运行现有状态机回归，验证空答案、部分答案和冻结输出的真实迁移。
        result = subprocess.run(
            [sys.executable, "-B", str(WAIT_LOOP_TEST)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("plan-mode-wait-loop: PASS (10 cases)", result.stdout)

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-07-26 18:00:00，锁定压缩恢复不生成总结。
    def test_compaction_recovery_has_no_summary_final_answer(self) -> None:
        case = self.cases["plan_compacted"]
        # 1. 确认压缩恢复仍回到计划 Owner，冻结总结型 final_answer。
        self.assertEqual(case["recovery_owner"], "implementation-planning-rules")
        visible = "\n".join(case["visible_messages"])
        for token in case["forbidden_tokens"]:
            self.assertNotIn(token, visible)

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-07-26 18:00:00，保留默认模式总结兼容性。
    def test_default_mode_keeps_summary_skill(self) -> None:
        case = self.cases["default_summary"]
        # 1. 校验总结 Skill 仍仅在 Default Mode 生效。
        self.assertEqual(case["mode"], "default")
        self.assertIn("reasoning-summary-structure-rules", case["hit_skills"])
        self.assertIn("# 📋 本轮总结", "\n".join(case["visible_messages"]))

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-07-26 18:00:00，锁定四份规则源的边界声明。
    def test_static_owner_boundaries_are_present(self) -> None:
        summary = (REPO_ROOT / "reasoning-summary-structure-rules" / "SKILL.md").read_text(encoding="utf-8")
        planning = (REPO_ROOT / "implementation-planning-rules" / "SKILL.md").read_text(encoding="utf-8")
        hit_check = (REPO_ROOT / "skill-hit-check-rules" / "SKILL.md").read_text(encoding="utf-8")
        compression = (REPO_ROOT / "context-compression-rules" / "SKILL.md").read_text(encoding="utf-8")
        # 1. 校验计划 Owner、总结排除、命中总控和压缩恢复边界均已落盘。
        self.assertIn("Plan Mode 负向退出", summary)
        self.assertIn("唯一计划 Owner", planning)
        self.assertIn("命中列表不得包含 `reasoning-summary-structure-rules`", hit_check)
        self.assertIn("`Plan Mode` 不持久化活动 projection", compression)

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-08-09 02:00:00，验证正例包含完整零决策字段。
    def test_plan_ready_detailed_fields(self) -> None:
        case = self.cases["plan_ready_detailed"]
        # 1. 校验正例包含所有零决策字段，内容密度足以指导后续编码。
        zero_fields = case["zero_decision_fields"]
        required_fields = [
            "文件/符号", "操作", "禁止触碰", "精确测试命令",
            "断言", "清理", "回滚", "完成条件", "停止条件",
        ]
        for field in required_fields:
            self.assertIn(field, zero_fields, f"正例缺少零决策字段: {field}")
            self.assertTrue(zero_fields[field].strip(), f"正例零决策字段为空: {field}")

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-08-09 02:00:00，验证骨架例被拒绝。
    def test_plan_ready_skeleton_fails(self) -> None:
        case = self.cases["plan_ready_skeleton_only"]
        # 1. 骨架例只有章节标题，缺少零决策字段，必须被闸门拒绝。
        zero_fields = case["zero_decision_fields"]
        required_fields = [
            "文件/符号", "操作", "禁止触碰", "精确测试命令",
            "断言", "清理", "回滚", "完成条件", "停止条件",
        ]
        missing = [field for field in required_fields if field not in zero_fields]
        self.assertTrue(missing, "骨架例应缺少零决策字段")

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-08-09 02:00:00，验证 concise 例被拒绝。
    def test_plan_ready_concise_fails(self) -> None:
        case = self.cases["plan_ready_concise_plan"]
        # 1. concise 例使用 Summary/Key Changes/Test Plan 通用壳，缺少仓库模板字段，必须被拒绝。
        visible = "\n".join(case["visible_messages"])
        self.assertIn("Summary", visible)
        self.assertIn("Key Changes", visible)
        self.assertIn("Test Plan", visible)
        self.assertNotIn("最小任务清单", visible)

    # [参数] self：测试实例；[返回] 无；最近修改时间：2026-08-09 02:00:00，验证占位词例被拒绝。
    def test_plan_ready_placeholder_fails(self) -> None:
        case = self.cases["plan_ready_placeholder"]
        # 1. 占位例含"见上文""后续再定""若干文件"等占位词，必须被闸门拒绝。
        zero_fields = case["zero_decision_fields"]
        placeholder_terms = ["见上文", "后续再定", "若干文件", "TBD", "TODO", "实现时再看"]
        found_placeholder = []
        for field, value in zero_fields.items():
            for term in placeholder_terms:
                if term in value:
                    found_placeholder.append((field, term))
        self.assertTrue(found_placeholder, "占位例应包含占位词")
        self.assertIn("见上文", zero_fields["文件/符号"])
        self.assertIn("若干文件", zero_fields["禁止触碰"])


if __name__ == "__main__":
    unittest.main()
