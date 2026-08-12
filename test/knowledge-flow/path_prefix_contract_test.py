"""回归本轮根因：知识库笔记路径必须是裸相对路径，不得再带 知识库/ 前缀。

前缀叠加会生成嵌套目录 `D:\\谷歌云盘\\知识库\\知识库\\`，该错误约定在 Obsidian 时代即已存在。
本测试把「禁止前缀」固化成常驻断言，防止未来任何 skill 资产重新引入。
"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_ROOT = Path("D:/谷歌云盘/知识库")
# 带前缀的路径写法一旦出现在规则或脚本里，就会被执行方原样拼到知识库根之后。
FORBIDDEN_PREFIXES = (
    "知识库/00-Inbox",
    "知识库/10-Sessions",
    "知识库/20-Knowledge",
    "知识库/30-MOCs",
    "知识库/40-Entities",
    "知识库/50-Sources",
    "知识库/90-Archive",
    "知识库/INDEX",
)
# 参与扫描的 skill 资产目录：这些文件会被 agent 当作执行口径读取。
SCAN_TARGETS = (
    "knowledge-flow",
    "execution-failure-learning-rules",
    "reasoning-summary-structure-rules",
    "skill-hit-check-rules",
    "project-memory-rules",
    "project-style-rules",
    "git-collaboration-rules",
    "session-handoff-rules",
    "task-plan-rehydration-rules",
    "continuous-code-quality-supervisor-rules",
    # 自举脚本是 AGENTS.md / CLAUDE.md 的模板源，漏检会导致下次自举写回旧路径写法
    "project-rule-file-bootstrap-rules",
)
SCAN_SUFFIXES = (".md", ".py", ".yaml", ".sh")
# 负向示例文件：这些文件必须保留前缀写法作为反例说明，不参与禁止扫描。
NEGATIVE_EXAMPLE_FILES = (
    "knowledge-flow/references/file-operations.md",
    "knowledge-flow/references/knowledge-layout.md",
    "knowledge-flow/references/validation-checklist.md",
)


def iter_asset_files() -> list[Path]:
    """收集需要检查前缀的 skill 资产文件。

    [参数] 无。
    [返回] list[Path]：待扫描文件路径列表。
    最近修改时间: 2026-08-12 新增路径前缀回归测试。
    """
    files = []
    for target in SCAN_TARGETS:
        base = ROOT / target
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                continue
            if "__pycache__" in path.parts:
                continue
            files.append(path)
    return files


class PathPrefixContractTest(unittest.TestCase):
    """前缀禁止组：确保活动 skill 资产不再产出带前缀的笔记路径。"""

    def test_no_prefixed_path_in_skill_assets(self) -> None:
        """除负向示例外，skill 资产不得出现带 知识库/ 前缀的路径。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增路径前缀回归测试。
        """
        offenders = []
        for path in iter_asset_files():
            rel = path.relative_to(ROOT).as_posix()
            if rel in NEGATIVE_EXAMPLE_FILES:
                continue
            text = path.read_text(encoding="utf-8")
            for prefix in FORBIDDEN_PREFIXES:
                if prefix in text:
                    offenders.append(f"{rel} -> {prefix}")
        self.assertEqual(offenders, [], f"出现带 知识库/ 前缀的笔记路径：{offenders}")

    def test_negative_examples_still_document_the_trap(self) -> None:
        """负向示例文件必须仍然保留前缀反例，避免规则失去解释力。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增路径前缀回归测试。
        """
        text = (ROOT / "knowledge-flow" / "references" / "file-operations.md").read_text(encoding="utf-8")
        self.assertIn("知识库/20-Knowledge", text, "错误写法对照表缺少带前缀反例")
        self.assertIn("嵌套", text, "反例未说明嵌套后果")

    def test_layout_forbids_nested_knowledge_dir(self) -> None:
        """布局规则必须显式禁止嵌套知识库目录。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增路径前缀回归测试。
        """
        text = (ROOT / "knowledge-flow" / "references" / "knowledge-layout.md").read_text(encoding="utf-8")
        self.assertIn("禁止嵌套知识库目录", text)
        self.assertIn("裸相对路径", text)


class ThemeListContractTest(unittest.TestCase):
    """主题清单组：实际目录必须在落点规则声明的清单内，阻断新造主题目录。"""

    def test_declared_themes_match_layout_rule(self) -> None:
        """索引脚本的主题常量必须与落点规则声明的 7 主题一致。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增主题清单一致性断言。
        """
        layout = (ROOT / "knowledge-flow" / "references" / "knowledge-layout.md").read_text(encoding="utf-8")
        # 主题常量定义在巡检脚本，索引脚本单向复用它；因此断言定义方而非消费方。
        script = (ROOT / "knowledge-flow" / "scripts" / "audit_vault_knowledge.py").read_text(encoding="utf-8")
        for theme in ("项目", "代码规则", "工程实践", "研发流程", "AI协作", "数据清洗", "开发环境"):
            self.assertIn(f"`{theme}/`", layout, f"落点规则缺少主题 {theme}")
            self.assertIn(f'"{theme}"', script, f"主题常量定义方缺少主题 {theme}")
        self.assertIn("固定主题清单", layout)
        self.assertIn("契约固定落点", layout)
        # 索引脚本必须复用而非自持一套主题常量
        index_script = (ROOT / "knowledge-flow" / "scripts" / "knowledge_index.py").read_text(encoding="utf-8")
        self.assertIn("DECLARED_THEMES = AUDIT.DECLARED_THEMES", index_script)
        self.assertIn("note_theme = AUDIT.note_theme", index_script)

    def test_actual_dirs_are_within_declared_list(self) -> None:
        """知识库实际目录必须全部在 7 主题 + 3 契约落点清单内。

        这条直接阻断「为单篇笔记又新造一个主题目录」，是本轮防复发的核心断言。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增主题合规实测断言。
        """
        knowledge_dir = KNOWLEDGE_ROOT / "20-Knowledge"
        if not knowledge_dir.exists():
            self.skipTest("知识库不可达，跳过实测")
        allowed = {
            "项目", "代码规则", "工程实践", "研发流程", "AI协作", "数据清洗", "开发环境",
            "execution-failure-cases", "project-rules", "code-style",
        }
        actual = {p.name for p in knowledge_dir.iterdir() if p.is_dir()}
        self.assertEqual(actual - allowed, set(), f"出现未登记的主题目录：{actual - allowed}")

    def test_no_stray_notes_in_knowledge_root(self) -> None:
        """20-Knowledge 根下不得散落笔记，必须归入主题。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增散落笔记断言。
        """
        knowledge_dir = KNOWLEDGE_ROOT / "20-Knowledge"
        if not knowledge_dir.exists():
            self.skipTest("知识库不可达，跳过实测")
        stray = [p.name for p in knowledge_dir.glob("*.md")]
        self.assertEqual(stray, [], f"20-Knowledge 根下出现散落笔记：{stray}")


class LiveKnowledgeBaseTest(unittest.TestCase):
    """真实知识库组：目录存在时校验没有重新长出嵌套层。"""

    def test_no_nested_knowledge_directory(self) -> None:
        """知识库根下不得存在嵌套的 知识库 子目录。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增嵌套目录实测断言。
        """
        if not KNOWLEDGE_ROOT.exists():
            self.skipTest("知识库根目录不可达，跳过实测")
        nested = KNOWLEDGE_ROOT / "知识库"
        self.assertFalse(nested.exists(), f"嵌套目录重新出现：{nested}")

    def test_notes_live_under_standard_layout(self) -> None:
        """根目录下除 INDEX.md 外不应散落笔记文件。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增标准布局断言。
        """
        if not KNOWLEDGE_ROOT.exists():
            self.skipTest("知识库根目录不可达，跳过实测")
        stray = [p.name for p in KNOWLEDGE_ROOT.glob("*.md") if p.name != "INDEX.md"]
        self.assertEqual(stray, [], f"根目录出现散落笔记：{stray}")


if __name__ == "__main__":
    unittest.main()
