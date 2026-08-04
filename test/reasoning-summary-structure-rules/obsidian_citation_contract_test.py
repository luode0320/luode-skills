"""验证最终总结的知识引用小节与 Obsidian 引用台账的规则文本契约。"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OBSIDIAN_SKILL = ROOT / "obsidian-knowledge-flow" / "SKILL.md"
OBSIDIAN_FLOW = ROOT / "obsidian-knowledge-flow" / "references" / "capture-retrieve-distill.md"
SUMMARY_SKILL = ROOT / "reasoning-summary-structure-rules" / "SKILL.md"
SUMMARY_AGENT = ROOT / "reasoning-summary-structure-rules" / "agents" / "openai.yaml"
SUMMARY_TEMPLATE = ROOT / "reasoning-summary-structure-rules" / "references" / "summary-structure-template.md"
SUMMARY_CONDITIONS = ROOT / "reasoning-summary-structure-rules" / "references" / "conditional-sections-rules.md"
SUMMARY_EXAMPLES = ROOT / "reasoning-summary-structure-rules" / "references" / "output-examples.md"
ALL_RULE_FILES = (
    OBSIDIAN_SKILL,
    OBSIDIAN_FLOW,
    SUMMARY_SKILL,
    SUMMARY_AGENT,
    SUMMARY_TEMPLATE,
    SUMMARY_CONDITIONS,
    SUMMARY_EXAMPLES,
)

LEDGER_FIELDS = ("笔记名", "所在目录", "本轮用途", "status", "操作", "readback")
CITATION_SECTION = "## 📚 知识引用"
CITE_TABLE_HEADER = "| # | 笔记 | 本轮用途 |"
DISTILL_TABLE_HEADER = "| # | 笔记 | 操作 | readback |"
# 被本轮取代的旧口径：单行摘要与单开小节禁令，不允许在任何规则文件里残留
RETIRED_PHRASES = (
    "不得新增独立 Obsidian 小节",
    "在本节用一行简短说明检索情况",
    "在本节用一行简短说明沉淀结果",
    "真实 Obsidian 沉淀行计入 5 句上限",
    "真实 Obsidian 沉淀行计入最多 5 句上限",
    "只在「方案与根因」补一行检索摘要",
    "Obsidian 检索（仅真实触发时）",
    "Obsidian 沉淀（仅真实触发时",
)


def read_text(path: Path) -> str:
    """按 UTF-8 读取规则文件全文，编码异常直接暴露为测试失败。

    [参数] path：目标规则文件路径。
    [返回] str：规则文件的 UTF-8 文本。
    最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
    """
    return path.read_text(encoding="utf-8")


class ObsidianLedgerContractTest(unittest.TestCase):
    """台账组：校验引用台账的字段、登记时机与三条硬约束。"""

    def test_ledger_section_defines_six_fields(self) -> None:
        """台账小节必须定义六个固定字段。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(OBSIDIAN_FLOW)
        self.assertIn("## 引用台账", content)
        for field in LEDGER_FIELDS:
            self.assertIn(field, content, f"引用台账缺少字段 {field}")

    def test_ledger_registers_immediately(self) -> None:
        """台账必须要求成功返回后立即登记，禁止收口时补记。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(OBSIDIAN_FLOW)
        self.assertIn("立即登记", content)
        self.assertIn("不得延后到收口阶段", content)

    def test_ledger_rejects_unread_notes(self) -> None:
        """search 命中但未 read 的笔记不得进入引用表。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(OBSIDIAN_FLOW)
        self.assertIn("一律不得入表", content)
        self.assertIn("候选线索", content)

    def test_ledger_forbids_cli_echo_as_note_name(self) -> None:
        """笔记名必须取自本地 path 字符串，不使用 CLI 回显文本。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(OBSIDIAN_FLOW)
        self.assertIn("不使用 CLI 回显文本", content)
        self.assertIn("回显中文会乱码", content)

    def test_ledger_is_session_scoped(self) -> None:
        """台账是本轮会话内事实，不写入 vault、不落盘项目文件。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(OBSIDIAN_FLOW)
        self.assertIn("不写入 vault", content)
        self.assertIn("不落盘到项目文件", content)

    def test_skill_entry_points_reference_ledger(self) -> None:
        """检索规则与捕获规则都必须给出台账登记入口。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(OBSIDIAN_SKILL)
        self.assertEqual(content.count("引用台账"), 3, "检索规则、捕获规则与 reference 指引各需一处台账入口")
        self.assertIn("不使用 CLI 回显文本", content)
        self.assertIn("`search` 命中但未读取的笔记不得入表", content)


class CitationOrderContractTest(unittest.TestCase):
    """顺序组：校验知识引用在固定顺序中的位置与末尾分流。"""

    def test_fixed_order_places_citation_after_changes(self) -> None:
        """固定顺序中知识引用必须在改动点之后、阻断收口之前。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_SKILL)
        changes = content.index("9. 本次改动点")
        citation = content.index("10. 知识引用")
        blocker = content.index("11. 任务阻断收口")
        self.assertLess(changes, citation, "知识引用必须排在本次改动点之后")
        self.assertLess(citation, blocker, "任务阻断收口必须仍是最后一项")

    def test_tail_order_branches_on_ledger(self) -> None:
        """末尾顺序必须按台账是否非空分流，而不是固定由改动点收尾。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_SKILL)
        self.assertIn("台账非空时「知识引用」放在所有内容节点的最后", content)
        self.assertIn("台账为空时「本次改动点」放在最后", content)
        self.assertIn("改动点与知识引用（如有）必须置于其前", content)

    def test_self_check_requires_traceable_citation_rows(self) -> None:
        """发送前自检必须要求每行引用可回指真实 bridge 调用。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_SKILL)
        self.assertIn("回指本轮一次返回 `verified=true` 的 bridge 调用", content)
        self.assertIn("台账为空时是否已整节省略", content)

    def test_condition_gate_and_verdict_cover_citation(self) -> None:
        """条件字段判定、通过标准与驳回标准都必须覆盖知识引用。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_SKILL)
        self.assertIn("引用台账是否非空", content)
        self.assertIn("台账非空时知识引用位于总结最后", content)
        self.assertIn("引用台账非空却缺少「知识引用」小节", content)
        self.assertIn("台账为空却输出该小节或空表", content)

    def test_description_and_agent_prompt_declare_citation(self) -> None:
        """技能 description 与代理提示词都必须声明引用清单口径。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        skill = read_text(SUMMARY_SKILL)
        agent = read_text(SUMMARY_AGENT)
        self.assertIn("必须在总结末尾输出「知识引用」小节", skill)
        self.assertIn("知识引用", agent)
        self.assertIn("readback", agent)
        self.assertIn("改动点与知识引用置于阻断区块之前", agent)

    def test_emoji_catalog_contains_citation_section(self) -> None:
        """小节图标清单必须登记知识引用。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        self.assertIn("📚 知识引用", read_text(SUMMARY_SKILL))


class RetiredPhraseContractTest(unittest.TestCase):
    """禁令组：校验被取代的旧口径已从全部规则文件中移除。"""

    def test_retired_phrases_are_absent(self) -> None:
        """旧禁令与两处单行摘要口径不得在任何规则文件中残留。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        for path in ALL_RULE_FILES:
            content = read_text(path)
            for phrase in RETIRED_PHRASES:
                self.assertNotIn(phrase, content, f"{path.name} 仍残留旧口径：{phrase}")

    def test_result_section_no_longer_hosts_obsidian_line(self) -> None:
        """结果与结论不再承载 Obsidian 摘要行，也不占用句数上限。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_SKILL)
        self.assertIn("统一由「知识引用」小节承载，不在本节写摘要行", content)
        self.assertIn("不得输出笔记正文、不得摘录笔记片段", content)


class CitationTemplateContractTest(unittest.TestCase):
    """模板组：校验模板与条件字段规则给出可直接照抄的引用小节。"""

    def test_template_defines_both_tables(self) -> None:
        """模板必须给出引用小节与两张表的固定表头。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_TEMPLATE)
        self.assertIn(CITATION_SECTION, content)
        self.assertIn(CITE_TABLE_HEADER, content)
        self.assertIn(DISTILL_TABLE_HEADER, content)
        self.assertIn("**本轮引用**", content)
        self.assertIn("**本轮沉淀**", content)

    def test_template_structure_requirements_cover_tail_order(self) -> None:
        """模板结构要求必须写明含知识引用的固定顺序与台账分流。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_TEMPLATE)
        self.assertIn("改动点 → 知识引用 → 任务阻断收口", content)
        self.assertIn("台账非空由知识引用收尾", content)
        self.assertIn("引用台账为空时整节省略", content)

    def test_condition_rules_section_five_is_citation(self) -> None:
        """条件字段规则第 5 节必须是知识引用，且覆盖入表门槛与边界。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_CONDITIONS)
        self.assertIn("## 5. 知识引用", content)
        self.assertIn(CITE_TABLE_HEADER, content)
        self.assertIn(DISTILL_TABLE_HEADER, content)
        self.assertIn("一律不得入表", content)
        self.assertIn("台账为空时整节省略", content)
        self.assertIn("不得输出笔记正文", content)
        self.assertIn("不豁免本节", content)


class CitationExampleContractTest(unittest.TestCase):
    """样例组：校验正反例都覆盖引用小节。"""

    def test_positive_example_contains_citation_section(self) -> None:
        """正例必须含引用小节，且位于改动点之后。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_EXAMPLES)
        changes = content.index("## 📦 改动点")
        citation = content.index(CITATION_SECTION)
        self.assertLess(changes, citation, "正例中引用小节必须排在改动点之后")
        self.assertIn(CITE_TABLE_HEADER, content)
        self.assertIn(DISTILL_TABLE_HEADER, content)

    def test_negative_example_covers_unread_note(self) -> None:
        """必须存在“未 read 却列入引用”的反例并写明不通过原因。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        content = read_text(SUMMARY_EXAMPLES)
        self.assertIn("## 反例（search 命中未 read 却列入知识引用）", content)
        self.assertIn("候选线索，不得入表", content)
        self.assertIn("笔记名取自 CLI 回显", content)


class RuleFileEncodingTest(unittest.TestCase):
    """编码组：校验全部目标规则文件为可解码 UTF-8 且无 NUL。"""

    def test_all_rule_files_are_utf8(self) -> None:
        """七份规则文件必须是合法 UTF-8 且不含 NUL 字节。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-04 20:10:45 新增知识引用契约测试。
        """
        for path in ALL_RULE_FILES:
            raw = path.read_bytes()
            raw.decode("utf-8")
            self.assertNotIn(b"\x00", raw, f"{path.name} 含 NUL 字节")


if __name__ == "__main__":
    unittest.main()
