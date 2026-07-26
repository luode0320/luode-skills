"""验证结果与结论的适中详细度契约。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SKILL_FILE = ROOT / "reasoning-summary-structure-rules" / "SKILL.md"
TEMPLATE_FILE = ROOT / "reasoning-summary-structure-rules" / "references" / "summary-structure-template.md"
EXAMPLES_FILE = ROOT / "reasoning-summary-structure-rules" / "references" / "output-examples.md"
CONDITIONAL_FILE = ROOT / "reasoning-summary-structure-rules" / "references" / "conditional-sections-rules.md"
OPENAI_FILE = ROOT / "reasoning-summary-structure-rules" / "agents" / "openai.yaml"


def evaluate_result_block(block: str) -> tuple[bool, str]:
    """按本轮冻结契约判断一段结果区样例。

    [参数] block: 结果与结论引用块文本
    [返回] (是否通过, 失败原因或通过说明)
    最近修改时间: 2026-07-26 15:37:33，新增结果区 3–5 句正负回归契约
    """

    # 1. 只统计结果区引用句，避免把标题或执行证据误算进句数。
    lines = [line.strip() for line in block.splitlines() if line.strip().startswith(">")]
    core_prefixes = ("本次解决的问题：", "采用的方法：", "结果确认：")
    core_count = sum(any(prefix in line for prefix in core_prefixes) for line in lines)

    # 2. 以核心三句和最多五句边界判断粒度，拒绝状态词或流水账。
    if core_count < 3:
        return False, "核心问题、方法、结果/验证状态不足三句"
    if len(lines) > 5:
        return False, "结果区超过五句"
    if any(line in {"> 已完成。", "> 已解决。", "> 请查看文件。"} for line in lines):
        return False, "结果区只有空泛状态词"
    if any(token in block for token in ("完整测试清单", "逐文件改动", "执行流水账")):
        return False, "结果区复制了详细证据"
    return True, "结果区粒度符合契约"


class ResultConclusionDetailTests(unittest.TestCase):
    """覆盖规则文本、模板和结果区正负样例。"""

    @classmethod
    def setUpClass(cls) -> None:
        """加载本地规则资产并输出测试开始日志。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 15:37:33，固定本地测试资产读取入口
        """

        # 1. 只读取 UTF-8 规则资产，不调用外部服务或写回生产目录。
        cls.skill_text = SKILL_FILE.read_text(encoding="utf-8")
        cls.template_text = TEMPLATE_FILE.read_text(encoding="utf-8")
        cls.examples_text = EXAMPLES_FILE.read_text(encoding="utf-8")
        cls.conditional_text = CONDITIONAL_FILE.read_text(encoding="utf-8")
        cls.openai_text = OPENAI_FILE.read_text(encoding="utf-8")
        print("[开始] 结果与结论适中详细度本地契约回归")

    @classmethod
    def tearDownClass(cls) -> None:
        """输出测试结束日志，不保留临时资源。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 15:37:33，补齐测试结束可观测性
        """

        # 1. 当前测试只使用内存字符串，没有外部资源需要回收。
        print("[结束] 结果与结论适中详细度本地契约回归")

    def test_skill_preserves_waiting_decision_gate_and_declares_detail_contract(self) -> None:
        """验证主规则保留未决阻断并声明 3–5 句契约。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 15:37:33，覆盖结果区规则与 PMW 兼容性
        """

        # 1. 断言当前升级没有削弱既有未决总结闸门。
        self.assertIn("SUMMARY-GATE-PMW-001", self.skill_text)
        self.assertIn("WAITING_DECISION", self.skill_text)

        # 2. 断言主规则明确适中句数、具体内容与防流水账约束。
        for marker in ("3 个简短句子", "4–5 句", "复制命令", "完整测试清单", "执行流水账"):
            self.assertIn(marker, self.skill_text)

    def test_template_and_openai_prompt_share_same_contract(self) -> None:
        """验证模板与公开默认提示没有漂移。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 15:37:33，保持模板与 UI 提示口径一致
        """

        # 1. 定位模板结果区并确认三个核心字段只出现于结果区骨架。
        result_section = re.search(r"## 📌 结果与结论(?P<body>.*?)(?=^## )", self.template_text, re.M | re.S)
        self.assertIsNotNone(result_section)
        body = result_section.group("body")
        for marker in ("本次解决的问题：", "采用的方法：", "结果确认：", "范围边界或残留卡点"):
            self.assertIn(marker, body)

        # 2. 确认公开提示同样限制为最多五句且禁止重复证据。
        for marker in ("3 个简短句子", "最多 5 句", "逐文件改动"):
            self.assertIn(marker, self.openai_text)

    def test_simple_three_sentence_fixture_passes(self) -> None:
        """验证简单任务的三句结果区通过。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 15:37:33，覆盖推荐的最小正例
        """

        # 1. 使用具体对象、方法和验证状态构造最小正例。
        block = (
            "> 本次解决的问题：结果区缺少可复核的完成状态。\n"
            "> 采用的方法：补充问题、方法和验证状态三句骨架。\n"
            "> 结果确认：模板与规则已同步，并通过本地结构回归。"
        )
        self.assertEqual((True, "结果区粒度符合契约"), evaluate_result_block(block))

    def test_complex_five_sentence_fixture_passes(self) -> None:
        """验证复杂任务补充必要边界时不超过五句。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 15:37:33，覆盖复杂任务上限正例
        """

        # 1. 只增加必要的范围与验证边界，不伪造 Obsidian 沉淀事实。
        block = (
            "> 本次解决的问题：复杂总结的结果区过于简略。\n"
            "> 采用的方法：统一规则、模板和正反例的 3–5 句契约。\n"
            "> 结果确认：专项回归覆盖过短、适中和冗长场景并通过。\n"
            "> 范围边界或残留卡点：真实模型生成质量仍需后续人工抽样。\n"
            "> 验证边界：本轮仅验证规则资产和静态契约，不代表真实模型输出质量。"
        )
        self.assertEqual((True, "结果区粒度符合契约"), evaluate_result_block(block))

    def test_short_and_verbose_fixtures_are_rejected(self) -> None:
        """验证过短、超长和重复证据结果区被拒绝。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 15:37:33，覆盖用户反馈的两类负例
        """

        # 1. 过短样例不能用单个状态词替代三项核心内容。
        short_block = "> 已完成。"
        self.assertFalse(evaluate_result_block(short_block)[0])

        # 2. 超长样例不能把完整证据清单复制到结果区。
        verbose_block = "\n".join(
            [
                "> 本次解决的问题：结果区过短。",
                "> 采用的方法：补充详细度契约。",
                "> 结果确认：规则已通过验证。",
                "> 范围边界或残留卡点：无。",
                "> 额外说明：完整测试清单、逐文件改动和执行流水账。",
                "> 额外说明：不应出现的第六句。",
            ]
        )
        self.assertFalse(evaluate_result_block(verbose_block)[0])

    def test_examples_record_short_and_repetition_boundaries(self) -> None:
        """验证公开正反例同步记录过短与冗长边界。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 15:37:33，防止样例与规则再次漂移
        """

        # 1. 公开样例必须能让后续 Agent 找到过短和重复证据的拒绝原因。
        self.assertIn("结果区至少要用 3 个简短句子", self.examples_text)
        self.assertIn("最多 5 句", self.examples_text)
        self.assertIn("复制命令", self.examples_text)

    def test_conditional_reference_shares_result_contract(self) -> None:
        """验证条件字段说明与结果区核心契约保持同步。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 16:05:00，补充条件说明防漂移断言
        """

        # 1. 条件说明必须重复句数、核心信息和去重边界，避免最终输出分叉。
        for marker in ("3 个简短句子", "第 4–5 句", "完整测试清单", "最多 5 句上限"):
            self.assertIn(marker, self.conditional_text)

    def test_waiting_decision_gate_remains_blocking(self) -> None:
        """验证未决选择仍然阻断任何结果区收口。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 16:08:00，补充未决选择边界回归
        """

        # 1. 既有总结闸门必须同时保留状态名称和禁止收口语义。
        self.assertIn("SUMMARY-GATE-PMW-001", self.skill_text)
        self.assertIn("WAITING_DECISION", self.skill_text)
        self.assertIn("不得把推荐项或文本总结当作完成信号", self.skill_text)

    def test_obsidian_condition_cannot_claim_success_without_cli(self) -> None:
        """验证没有真实 CLI 时不能伪造 Obsidian 检索或沉淀成果。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 16:08:00，补充条件状态防伪回归
        """

        # 1. 条件规则必须明确 CLI 缺失时不输出成功态，避免结果区误报。
        self.assertIn("没有真实 CLI 证据时，不得写“已检索”或“已沉淀”", self.conditional_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
