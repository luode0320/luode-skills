"""验证知识库机器索引的构建、查询、主题归一化与新鲜度自动重建。

索引是检索第一跳，手写导航只覆盖约三分之一笔记时它是唯一可信入口，
因此对字段完整性、召回超集性与过期自动重建三点做常驻断言。
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
INDEX_SCRIPT = ROOT / "knowledge-flow" / "scripts" / "knowledge_index.py"


def load_index_module() -> Any:
    """按文件路径加载索引模块，避免依赖带连字符的目录可导入。

    [参数] 无。
    [返回] Any: 已加载的索引模块对象。
    最近修改时间: 2026-08-12 新增机器索引契约测试。
    """
    name = "knowledge_index_under_test"
    spec = importlib.util.spec_from_file_location(name, INDEX_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


INDEX = load_index_module()


def make_fake_kb(base: Path) -> None:
    """构造一个最小知识库样本，覆盖完整笔记、缺字段笔记与契约落点。

    [参数] base: 样本知识库根目录。
    [返回] None。
    最近修改时间: 2026-08-12 新增机器索引契约测试。
    """
    full = base / "20-Knowledge" / "代码规则" / "样例风格约定.md"
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(
        "---\n"
        "title: 样例风格约定\n"
        "aliases: [样例别名词]\n"
        "tags: [样例标签]\n"
        "topics: [样例主题]\n"
        "status: active\n"
        "---\n\n正文里有独特词 bodyonlyword。\n",
        encoding="utf-8",
    )
    # 无 frontmatter 的笔记必须降级入索引，不能因缺字段被漏掉
    bare = base / "20-Knowledge" / "项目" / "裸笔记.md"
    bare.parent.mkdir(parents=True, exist_ok=True)
    bare.write_text("没有头部的正文，含 barekeyword。\n", encoding="utf-8")
    # 契约固定落点不得被判为 unknown 主题
    case = base / "20-Knowledge" / "execution-failure-cases" / "owner" / "案例.md"
    case.parent.mkdir(parents=True, exist_ok=True)
    case.write_text("---\ntitle: 案例\nstatus: candidate\n---\n\n案例正文。\n", encoding="utf-8")
    # 未登记目录必须被标成 unknown，便于巡检发现新造目录
    stray = base / "20-Knowledge" / "未登记目录" / "野笔记.md"
    stray.parent.mkdir(parents=True, exist_ok=True)
    stray.write_text("---\ntitle: 野笔记\nstatus: active\n---\n\n野正文。\n", encoding="utf-8")
    # 知识库根下的入口文件主题应为 root
    (base / "INDEX.md").write_text("---\ntitle: INDEX\nstatus: active\n---\n\n入口。\n", encoding="utf-8")


class ThemeNormalizationTest(unittest.TestCase):
    """主题归一化组：校验路径到主题的推导规则。"""

    def test_declared_themes_are_recognized(self) -> None:
        """7 个声明主题必须被正确识别。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        for theme in INDEX.DECLARED_THEMES:
            self.assertEqual(INDEX.note_theme(f"20-Knowledge/{theme}/x.md"), theme)

    def test_contract_dirs_are_not_unknown(self) -> None:
        """契约固定落点不得被判为未登记主题。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        for name in INDEX.CONTRACT_DIRS:
            self.assertEqual(INDEX.note_theme(f"20-Knowledge/{name}/owner/x.md"), name)

    def test_unregistered_dir_is_unknown(self) -> None:
        """未登记目录必须标成 unknown，作为新造目录的发现信号。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        self.assertEqual(INDEX.note_theme("20-Knowledge/临时目录/x.md"), "unknown")
        self.assertEqual(INDEX.note_theme("20-Knowledge/直接散落.md"), "unknown")

    def test_root_and_other_top_dirs(self) -> None:
        """根入口文件为 root，其它顶层目录以自身为主题。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        self.assertEqual(INDEX.note_theme("INDEX.md"), "root")
        self.assertEqual(INDEX.note_theme("30-MOCs/a.md"), "30-MOCs")
        self.assertEqual(INDEX.note_theme("90-Archive/b.md"), "90-Archive")


class IndexBuildAndQueryTest(unittest.TestCase):
    """构建与查询组：在临时样本库上校验字段完整性与召回。"""

    def setUp(self) -> None:
        """在临时目录构造样本库并把索引根指向它。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        make_fake_kb(self.base)
        self._saved_root = INDEX.KB_ROOT
        INDEX.KB_ROOT = self.base
        INDEX.AUDIT.KB_ROOT = self.base

    def tearDown(self) -> None:
        """还原索引根并清理临时目录。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        INDEX.KB_ROOT = self._saved_root
        INDEX.AUDIT.KB_ROOT = self._saved_root
        self._tmp.cleanup()

    def test_index_covers_every_note(self) -> None:
        """索引必须覆盖全部笔记，包括无 frontmatter 的。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        index = INDEX.build_index()
        actual = len(list(self.base.rglob("*.md")))
        self.assertEqual(index["notes_count"], actual)
        paths = {n["path"] for n in index["notes"]}
        self.assertIn("20-Knowledge/项目/裸笔记.md", paths)

    def test_bare_note_degrades_with_stem_title(self) -> None:
        """缺 frontmatter 的笔记用文件名兜底标题并标记 partial。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        index = INDEX.build_index()
        bare = next(n for n in index["notes"] if n["path"].endswith("裸笔记.md"))
        self.assertEqual(bare["title"], "裸笔记")
        self.assertTrue(bare["partial"])

    def test_query_matches_each_structured_field(self) -> None:
        """标题、别名、标签、topics、主题、路径六类字段都要能命中。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        index = INDEX.build_index()
        cases = {
            "样例风格约定": "title",
            "样例别名词": "aliases",
            "样例标签": "tags",
            "样例主题": "topics",
            "代码规则": "theme",
        }
        for keyword, field in cases.items():
            hits = INDEX.query_index(index, keyword)
            self.assertTrue(hits, f"关键词 {keyword} 应有命中")
            self.assertIn(field, hits[0]["matched"], f"{keyword} 应按 {field} 命中")

    def test_query_falls_back_to_body(self) -> None:
        """结构化字段没有的词也要能通过正文命中，避免召回损失。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增正文兜底断言。
        """
        index = INDEX.build_index()
        hits = INDEX.query_index(index, "bodyonlyword")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["matched"], ["body"])
        bare_hits = INDEX.query_index(index, "barekeyword")
        self.assertEqual(len(bare_hits), 1, "无 frontmatter 笔记也要能按正文命中")

    def test_structured_hits_rank_above_body_only(self) -> None:
        """结构化命中必须排在纯正文命中之前。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增相关性排序断言。
        """
        index = INDEX.build_index()
        hits = INDEX.query_index(index, "样例")
        self.assertGreaterEqual(len(hits), 1)
        first_structured = [r for r in hits[0]["matched"] if r != "body"]
        self.assertTrue(first_structured, "排首位的命中应含结构化字段")

    def test_empty_keyword_returns_nothing(self) -> None:
        """空关键词不得返回全库，避免误当成通配查询。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        index = INDEX.build_index()
        self.assertEqual(INDEX.query_index(index, "   "), [])


class FrontmatterCheckTest(unittest.TestCase):
    """契约校验组：note-schema 的必填字段与状态枚举必须可机器校验。"""

    def setUp(self) -> None:
        """构造含合规与不合规笔记的样本库。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增 frontmatter 合规校验测试。
        """
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self._saved_root = INDEX.KB_ROOT
        INDEX.KB_ROOT = self.base
        INDEX.AUDIT.KB_ROOT = self.base

    def tearDown(self) -> None:
        """还原根目录并清理临时目录。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增 frontmatter 合规校验测试。
        """
        INDEX.KB_ROOT = self._saved_root
        INDEX.AUDIT.KB_ROOT = self._saved_root
        self._tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        """写入样本笔记。

        [参数] rel: 裸相对路径；text: 笔记全文。
        [返回] None。
        最近修改时间: 2026-08-12 新增 frontmatter 合规校验测试。
        """
        path = self.base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def full_note(self, title: str, status: str = "active") -> str:
        """生成一篇必填字段齐全的笔记。

        [参数] title: 标题；status: 状态值。
        [返回] str: 笔记全文。
        最近修改时间: 2026-08-12 新增 frontmatter 合规校验测试。
        """
        return (
            f"---\nid: 20260812-000000-{title}\ntype: knowledge\ntitle: {title}\n"
            f"status: {status}\ncreated: 2026-08-12\nupdated: 2026-08-12\n---\n\n正文。\n"
        )

    def test_compliant_note_passes(self) -> None:
        """字段齐全且状态合规的笔记不应被报出。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增 frontmatter 合规校验测试。
        """
        self.write("20-Knowledge/项目/好笔记.md", self.full_note("好笔记"))
        report = INDEX.check_frontmatter()
        self.assertTrue(report["ok"])
        self.assertEqual(report["violation_count"], 0)

    def test_missing_required_field_is_reported(self) -> None:
        """缺必填字段必须被报出，字段名要能定位。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增 frontmatter 合规校验测试。
        """
        self.write(
            "20-Knowledge/项目/缺字段.md",
            "---\ntype: knowledge\ntitle: 缺字段\nstatus: active\n---\n\n正文。\n",
        )
        report = INDEX.check_frontmatter()
        self.assertFalse(report["ok"])
        entry = report["missing_required_fields"][0]
        self.assertIn("id", entry["missing"])
        self.assertIn("created", entry["missing"])

    def test_missing_frontmatter_is_reported(self) -> None:
        """完全没有头部的笔记必须被报出。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增 frontmatter 合规校验测试。
        """
        self.write("20-Knowledge/项目/裸的.md", "没有头部\n")
        report = INDEX.check_frontmatter()
        self.assertEqual(report["missing_frontmatter"], ["20-Knowledge/项目/裸的.md"])

    def test_status_out_of_enum_is_reported(self) -> None:
        """状态枚举外的取值必须被报出，防止枚举静默漂移。

        实测曾漂移出 confirmed、test-fixture 两个未声明值。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增状态枚举断言。
        """
        self.write("20-Knowledge/项目/怪状态.md", self.full_note("怪状态", status="confirmed"))
        report = INDEX.check_frontmatter()
        self.assertEqual(report["status_out_of_enum"][0]["status"], "confirmed")

    def test_case_status_is_allowed(self) -> None:
        """执行案例的 candidate 属于合法状态，不得误报。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增执行案例状态断言。
        """
        self.write(
            "20-Knowledge/execution-failure-cases/owner/案例.md",
            self.full_note("案例", status="candidate"),
        )
        report = INDEX.check_frontmatter()
        self.assertEqual(report["status_out_of_enum"], [])

    def test_archive_zone_is_exempt(self) -> None:
        """只读历史归档区豁免头部与必填字段校验，不为历史残留补字段。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增归档豁免断言。
        """
        self.write("90-Archive/_system-tests/残留.md", "没有头部\n")
        report = INDEX.check_frontmatter()
        self.assertTrue(report["ok"], "归档区不应计入违规")
        self.assertEqual(report["exempt_notes"], 1)

    def test_archive_zone_missing_fields_still_exempt(self) -> None:
        """归档区缺必填字段仍然豁免，豁免收窄不得连带收紧字段要求。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增归档豁免边界断言。
        """
        self.write("90-Archive/旧笔记.md", "---\nstatus: archived\n---\n\n正文。\n")
        report = INDEX.check_frontmatter()
        self.assertTrue(report["ok"], "归档区缺字段不应计入违规")
        self.assertEqual(report["missing_required_fields"], [])

    def test_archive_zone_bad_status_is_reported(self) -> None:
        """归档区的非法状态值必须报出：整体豁免会让归档区变成枚举盲区。

        实测归档区曾长期存在未声明的 test-fixture 状态而零告警。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增归档区状态枚举断言。
        """
        self.write("90-Archive/夹具.md", self.full_note("夹具", status="test-fixture"))
        report = INDEX.check_frontmatter()
        self.assertFalse(report["ok"], "归档区非法状态值必须报出")
        self.assertEqual(report["status_out_of_enum"][0]["status"], "test-fixture")

    def test_bom_does_not_break_frontmatter_detection(self) -> None:
        """带 BOM 的笔记不得被误判为无头部。

        实测曾有一篇带 BOM 的笔记被判成无 frontmatter，其全部字段在索引里静默丢失。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增 BOM 容忍断言。
        """
        path = self.base / "20-Knowledge" / "项目" / "带BOM.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"\xef\xbb\xbf" + self.full_note("带BOM").encode("utf-8"))
        report = INDEX.check_frontmatter()
        self.assertEqual(report["missing_frontmatter"], [])
        self.assertTrue(report["ok"])


class DeadLinkContractTest(unittest.TestCase):
    """死链组：双链目标必须解析到真实笔记，文档示例不得被误报。"""

    def setUp(self) -> None:
        """构造临时知识库根目录。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增死链校验测试。
        """
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self._saved_root = INDEX.KB_ROOT
        INDEX.KB_ROOT = self.base
        INDEX.AUDIT.KB_ROOT = self.base

    def tearDown(self) -> None:
        """还原根目录并清理临时目录。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增死链校验测试。
        """
        INDEX.KB_ROOT = self._saved_root
        INDEX.AUDIT.KB_ROOT = self._saved_root
        self._tmp.cleanup()

    def write(self, rel: str, title: str, body: str) -> None:
        """写入一篇带正文的样本笔记。

        [参数] rel: 裸相对路径；title: 标题；body: 正文内容。
        [返回] None。
        最近修改时间: 2026-08-12 新增死链校验测试。
        """
        path = self.base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        text = (
            f"---\nid: 20260812-000000-{title}\ntype: knowledge\ntitle: {title}\n"
            f"status: active\ncreated: 2026-08-12\nupdated: 2026-08-12\n---\n\n{body}\n"
        )
        path.write_text(text, encoding="utf-8")

    def test_live_link_passes(self) -> None:
        """指向真实笔记的双链不应被报出。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增死链校验测试。
        """
        self.write("20-Knowledge/项目/甲篇.md", "甲篇", "见 [[乙篇]]。")
        self.write("20-Knowledge/项目/乙篇.md", "乙篇", "正文。")
        report = INDEX.check_dead_links()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["dead_link_count"], 0)

    def test_dead_link_is_reported(self) -> None:
        """解析不到目标的双链必须被报出，并能定位来源笔记。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增死链校验测试。
        """
        self.write("20-Knowledge/项目/甲篇.md", "甲篇", "见 [[查无此篇]]。")
        report = INDEX.check_dead_links()
        self.assertFalse(report["ok"])
        entry = report["dead_links"][0]
        self.assertEqual(entry["target"], "查无此篇")
        self.assertEqual(entry["referenced_by"], ["20-Knowledge/项目/甲篇.md"])

    def test_link_inside_fenced_block_is_ignored(self) -> None:
        """围栏代码块内的双链是示例文本，不得报成死链。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增围栏排除断言。
        """
        self.write(
            "20-Knowledge/项目/甲篇.md",
            "甲篇",
            "示例：\n\n```yaml\nrelated:\n  - \"[[示例目标]]\"\n```\n\n以上是写法说明。",
        )
        report = INDEX.check_dead_links()
        self.assertTrue(report["ok"], report)

    def test_link_inside_inline_code_is_ignored(self) -> None:
        """行内代码内的双链是示例文本，不得报成死链。

        实测上一轮解释 YAML 引号问题时写的 `- "[[目标]]"` 曾被误报。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增行内代码排除断言。
        """
        self.write("20-Knowledge/项目/甲篇.md", "甲篇", '块状条目写成 `- "[[目标]]"` 时要先剥引号。')
        report = INDEX.check_dead_links()
        self.assertTrue(report["ok"], report)

    def test_path_and_alias_forms_resolve(self) -> None:
        """完整路径、无后缀路径与显示名写法都要能解析到同一篇笔记。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增多形态解析断言。
        """
        self.write("20-Knowledge/项目/乙篇.md", "乙篇", "正文。")
        self.write(
            "20-Knowledge/项目/甲篇.md",
            "甲篇",
            "三种写法：[[20-Knowledge/项目/乙篇.md]]、"
            "[[20-Knowledge/项目/乙篇|显示名]]、[[乙篇#某小节]]。",
        )
        report = INDEX.check_dead_links()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["checked_links"], 3)


class SupersessionContractTest(unittest.TestCase):
    """接替关系组：note-schema 声明的双向接替与状态互斥必须可机器校验。"""

    def setUp(self) -> None:
        """构造临时知识库根目录。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self._saved_root = INDEX.KB_ROOT
        INDEX.KB_ROOT = self.base
        INDEX.AUDIT.KB_ROOT = self.base

    def tearDown(self) -> None:
        """还原根目录并清理临时目录。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        INDEX.KB_ROOT = self._saved_root
        INDEX.AUDIT.KB_ROOT = self._saved_root
        self._tmp.cleanup()

    def write(self, rel: str, title: str, status: str, extra: str = "") -> None:
        """写入一篇带接替字段的样本笔记。

        [参数] rel: 裸相对路径；title: 标题；status: 状态值；extra: 追加的接替字段行。
        [返回] None。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        path = self.base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        text = (
            f"---\nid: 20260812-000000-{title}\ntype: knowledge\ntitle: {title}\n"
            f"status: {status}\ncreated: 2026-08-12\nupdated: 2026-08-12\n{extra}---\n\n正文。\n"
        )
        path.write_text(text, encoding="utf-8")

    def test_bidirectional_pair_passes(self) -> None:
        """双向写全的接替关系不应被报出。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        self.write("20-Knowledge/项目/新篇.md", "新篇", "active", "supersedes: [[旧篇]]\n")
        self.write("20-Knowledge/项目/旧篇.md", "旧篇", "superseded", "superseded_by: [[新篇]]\n")
        report = INDEX.check_supersession()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["supersession_violation_count"], 0)

    def test_one_sided_supersession_is_reported(self) -> None:
        """只写一侧的接替关系必须被报出，否则检索顺不到接替笔记。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        self.write("20-Knowledge/项目/新篇.md", "新篇", "active")
        self.write("20-Knowledge/项目/旧篇.md", "旧篇", "superseded", "superseded_by: [[新篇]]\n")
        report = INDEX.check_supersession()
        self.assertFalse(report["ok"])
        entry = report["dangling_supersession"][0]
        self.assertEqual(entry["path"], "20-Knowledge/项目/旧篇.md")
        self.assertEqual(entry["reason"], "对侧未写 supersedes")

    def test_active_with_superseded_by_is_reported(self) -> None:
        """已被接替的笔记状态不得仍是 active。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        self.write("20-Knowledge/项目/新篇.md", "新篇", "active", "supersedes: [[旧篇]]\n")
        self.write("20-Knowledge/项目/旧篇.md", "旧篇", "active", "superseded_by: [[新篇]]\n")
        report = INDEX.check_supersession()
        self.assertFalse(report["ok"])
        self.assertEqual(
            report["active_with_superseded_by"][0]["path"], "20-Knowledge/项目/旧篇.md"
        )

    def test_pointing_to_missing_note_is_reported(self) -> None:
        """接替目标笔记不存在时必须被报出，避免悬空指针。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        self.write("20-Knowledge/项目/旧篇.md", "旧篇", "superseded", "superseded_by: [[查无此篇]]\n")
        report = INDEX.check_supersession()
        self.assertFalse(report["ok"])
        self.assertEqual(report["dangling_supersession"][0]["reason"], "目标笔记不存在")

    def test_archive_zone_participates(self) -> None:
        """归档区不豁免接替校验：归档退场本身就要写 superseded_by。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        self.write("20-Knowledge/项目/新篇.md", "新篇", "active")
        self.write("90-Archive/旧篇.md", "旧篇", "archived", "superseded_by: [[新篇]]\n")
        report = INDEX.check_supersession()
        self.assertFalse(report["ok"], "归档区的单侧接替也必须报出")

    def test_no_supersession_fields_passes(self) -> None:
        """全库没有接替字段时不得误报。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增接替关系校验测试。
        """
        self.write("20-Knowledge/项目/独立篇.md", "独立篇", "active")
        report = INDEX.check_supersession()
        self.assertTrue(report["ok"])


class SharedThemeContractTest(unittest.TestCase):
    """口径共用组：主题推导必须与巡检同一实现，避免两处分叉。"""

    def test_theme_impl_is_shared_with_audit(self) -> None:
        """索引的 note_theme 必须直接复用巡检的实现。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增口径共用断言。
        """
        self.assertIs(INDEX.note_theme, INDEX.AUDIT.note_theme)
        self.assertIs(INDEX.DECLARED_THEMES, INDEX.AUDIT.DECLARED_THEMES)
        self.assertIs(INDEX.CONTRACT_DIRS, INDEX.AUDIT.CONTRACT_DIRS)


class IndexFreshnessTest(unittest.TestCase):
    """新鲜度组：索引过期必须自动重建，不依赖人工记得重建。"""

    def setUp(self) -> None:
        """构造样本库并写入初始索引。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        make_fake_kb(self.base)
        self._saved_root = INDEX.KB_ROOT
        INDEX.KB_ROOT = self.base
        INDEX.AUDIT.KB_ROOT = self.base
        INDEX.write_index(INDEX.build_index())

    def tearDown(self) -> None:
        """还原索引根并清理临时目录。

        [参数] 无。
        [返回] None。
        最近修改时间: 2026-08-12 新增机器索引契约测试。
        """
        INDEX.KB_ROOT = self._saved_root
        INDEX.AUDIT.KB_ROOT = self._saved_root
        self._tmp.cleanup()

    def test_new_note_triggers_rebuild(self) -> None:
        """新增笔记后直接查询也要能命中，索引应自动重建。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增新鲜度断言。
        """
        before = json.loads((self.base / INDEX.INDEX_NAME).read_text(encoding="utf-8"))["notes_count"]
        new_note = self.base / "20-Knowledge" / "工程实践" / "后加笔记.md"
        new_note.parent.mkdir(parents=True, exist_ok=True)
        new_note.write_text("---\ntitle: 后加笔记\nstatus: active\n---\n\n含 lateaddedword。\n", encoding="utf-8")

        index = INDEX.load_index()
        self.assertEqual(index["notes_count"], before + 1, "索引应自动重建到最新笔记数")
        self.assertTrue(INDEX.query_index(index, "lateaddedword"))

    def test_corrupted_index_is_rebuilt(self) -> None:
        """索引文件损坏时必须重建而非直接失败。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增损坏恢复断言。
        """
        (self.base / INDEX.INDEX_NAME).write_text("{ 不是合法 JSON", encoding="utf-8")
        index = INDEX.load_index()
        self.assertGreater(index["notes_count"], 0)

    def test_write_index_readback_verified(self) -> None:
        """索引写入后必须回读校验笔记数一致。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增回读校验断言。
        """
        index = INDEX.build_index()
        target = INDEX.write_index(index)
        back = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(back["notes_count"], index["notes_count"])
        self.assertEqual(back["schema_version"], INDEX.SCHEMA_VERSION)


if __name__ == "__main__":
    unittest.main()
