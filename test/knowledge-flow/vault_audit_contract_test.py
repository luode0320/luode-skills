"""验证知识库只读巡检脚本的零写入约束与候选判定纯函数。"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AUDIT_PATH = ROOT / "knowledge-flow" / "scripts" / "audit_vault_knowledge.py"
# 任何写操作入口出现在巡检源码里都视为越界；巡检必须保持只读。
FORBIDDEN_WRITES = (
    "write_text",
    "open(",
    "shutil.move",
    "shutil.copy",
    "os.remove",
    "os.rename",
    "unlink",
    "mkdir",
)
# 巡检必须保持纯文件系统读取，不得依赖任何外部进程。
FORBIDDEN_LEGACY = ("run_bridge", "subprocess", "verified=true")


def load_audit() -> Any:
    """按文件路径加载巡检模块，避免依赖带连字符的目录可导入。

    [参数] 无。
    [返回] Any：已加载的巡检模块对象。
    最近修改时间: 2026-08-12 迁移到 knowledge-flow 纯文件系统实现。
    """
    name = "audit_vault_knowledge_under_test"
    spec = importlib.util.spec_from_file_location(name, AUDIT_PATH)
    module = importlib.util.module_from_spec(spec)
    # 先注册再执行：巡检内的 dataclass 装饰器会按模块名回查命名空间。
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_audit()


def make_note(path: str, **overrides: Any) -> Any:
    """构造一条巡检事实，便于纯函数断言。

    [参数] path：笔记的裸相对路径；overrides：需要覆盖的字段。
    [返回] Any：巡检事实对象。
    最近修改时间: 2026-08-12 路径改为裸相对路径。
    """
    return AUDIT.NoteFacts(path=path, **overrides)


class ReadOnlyGuardTest(unittest.TestCase):
    """只读约束组：校验巡检源码不含任何写操作入口。"""

    def test_source_contains_no_write_entry(self) -> None:
        """巡检源码不得出现写文件或移动删除入口。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 由命令名断言改为文件系统写入口断言。
        """
        source = AUDIT_PATH.read_text(encoding="utf-8")
        for entry in FORBIDDEN_WRITES:
            self.assertNotIn(entry, source, f"巡检脚本出现写操作入口：{entry}")

    def test_source_has_no_external_process_dependency(self) -> None:
        """巡检不得依赖任何外部进程或旧桥接标识。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 替代原“只允许四个只读桥接命令”断言。
        """
        source = AUDIT_PATH.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN_LEGACY:
            self.assertNotIn(token, source, f"巡检脚本残留已废除依赖：{token}")

    def test_knowledge_root_is_google_drive(self) -> None:
        """巡检必须锁定 Google Drive 知识库根目录。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增固定根目录断言。
        """
        self.assertEqual(AUDIT.KB_ROOT.as_posix(), "D:/谷歌云盘/知识库")

    def test_execution_cases_are_skipped(self) -> None:
        """执行案例目录不参与分级处置，巡检必须跳过。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 前缀改为裸相对路径。
        """
        self.assertEqual(AUDIT.EXECUTION_CASE_PREFIX, "20-Knowledge/execution-failure-cases/")
        report = AUDIT.build_report([], ["20-Knowledge/execution-failure-cases/owner/case.md"])
        self.assertEqual(report["candidates"]["orphans"], [])


class PathPrefixContractTest(unittest.TestCase):
    """路径前缀组：确保巡检产出裸相对路径，不再生成嵌套知识库层。"""

    def test_prefix_is_not_reintroduced(self) -> None:
        """巡检源码不得出现带 知识库/ 前缀的路径常量。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增前缀回归断言。
        """
        source = AUDIT_PATH.read_text(encoding="utf-8")
        for bad in ("知识库/20-Knowledge", "知识库/30-MOCs", "知识库/INDEX"):
            self.assertNotIn(bad, source, f"巡检脚本出现嵌套前缀路径：{bad}")

    def test_knowledge_folder_is_bare_relative(self) -> None:
        """主题落点根目录必须是裸相对路径。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 常量由默认扫描目录改为主题落点根目录。
        """
        self.assertEqual(AUDIT.KNOWLEDGE_FOLDER, "20-Knowledge")

    def test_default_scan_range_is_whole_vault(self) -> None:
        """默认扫描范围必须是全库，不得只覆盖单个子目录。

        实测默认只扫 20-Knowledge 时覆盖率仅 42/63，30-MOCs 与 50-Sources 从未参与
        冲突与孤儿判定，导致「孤儿 0 篇」这类结论被当成全库结论。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增默认全库断言。
        """
        saved = sys.argv
        try:
            sys.argv = ["audit_vault_knowledge.py"]
            args = AUDIT.parse_args()
        finally:
            sys.argv = saved
        self.assertEqual(args.folder, "", "默认 folder 必须为空，才会退到全库根目录")


class CandidateGroupingTest(unittest.TestCase):
    """候选判定组：校验四类候选的纯函数判定。"""

    def test_same_theme_with_two_shared_tags_groups(self) -> None:
        """同主题且共享标签达到下限的当前有效笔记要归入同一候选组。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 归组条件收紧为同主题 + 双标签。
        """
        notes = [
            make_note(
                "20-Knowledge/工程实践/a.md", title="配置命名口径", status="active", topics=("配置", "命名")
            ),
            make_note(
                "20-Knowledge/工程实践/b.md", title="内嵌配置文件名", status="active", topics=("配置", "命名")
            ),
        ]
        groups = AUDIT.group_conflict_candidates(notes)
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]["members"]), 2)

    def test_single_shared_tag_does_not_group(self) -> None:
        """只共享一个标签不足以归组，这是本轮降噪的核心条件。

        原先共享 1 个标签即归组，实测 30 对候选里几乎全是误报。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增单标签负例，防条件退回。
        """
        # 标题必须差异明显，否则会走标题相似度通道，测不到标签下限条件
        notes = [
            make_note("20-Knowledge/工程实践/a.md", title="副本集连接串改造", status="active", topics=("配置",)),
            make_note("20-Knowledge/工程实践/b.md", title="启动可靠性排查", status="active", topics=("配置",)),
        ]
        self.assertEqual(AUDIT.group_conflict_candidates(notes), [])

    def test_cross_theme_shared_tags_do_not_group(self) -> None:
        """跨主题即使标签重叠也不归组，避免把不同主题的笔记判成重复。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增跨主题负例。
        """
        notes = [
            make_note(
                "20-Knowledge/代码规则/a.md", title="甲写法约定", status="active", topics=("配置", "命名")
            ),
            make_note(
                "20-Knowledge/项目/b.md", title="乙项目事实", status="active", topics=("配置", "命名")
            ),
        ]
        self.assertEqual(AUDIT.group_conflict_candidates(notes), [])

    def test_moc_notes_do_not_group(self) -> None:
        """导航笔记不参与归组：同家族分册天生同主题同标签。

        实测 30-MOCs/blog-data/ 下 10 篇分册 MOC 被归成一组，把 5 组真候选淹没。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增导航笔记豁免断言。
        """
        notes = [
            make_note(
                "30-MOCs/blog-data/前端-逐篇沉淀.md",
                title="前端逐篇沉淀",
                status="active",
                note_type="moc",
                topics=("blog-data", "逐篇沉淀"),
            ),
            make_note(
                "30-MOCs/blog-data/后端-逐篇沉淀.md",
                title="后端逐篇沉淀",
                status="active",
                note_type="moc",
                topics=("blog-data", "逐篇沉淀"),
            ),
        ]
        self.assertEqual(AUDIT.group_conflict_candidates(notes), [])

    def test_mutually_related_notes_do_not_group(self) -> None:
        """已互相写入 related 的两篇不再归组：双向关联是判为补充留下的裁决痕迹。

        没有这条豁免，判过补充的组每轮都会重新报出来，使用者很快会学会忽略这份报告。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增已裁决候选豁免断言。
        """
        notes = [
            make_note(
                "20-Knowledge/工程实践/a.md",
                title="配置命名口径",
                status="active",
                topics=("配置", "命名"),
                related=("[[20-Knowledge/工程实践/b|内嵌配置文件名]]",),
            ),
            make_note(
                "20-Knowledge/工程实践/b.md",
                title="内嵌配置文件名",
                status="active",
                topics=("配置", "命名"),
                related=("[[20-Knowledge/工程实践/a|配置命名口径]]",),
            ),
        ]
        self.assertEqual(AUDIT.group_conflict_candidates(notes), [])

    def test_quoted_wikilink_related_do_not_group(self) -> None:
        """带 YAML 引号的 related 写法同样要能归一，否则已裁决的组会继续误报。

        实测三组已双向关联的笔记因 `- "[[目标]]"` 未剥引号而归一失败。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增带引号 wikilink 归一断言。
        """
        notes = [
            make_note(
                "20-Knowledge/工程实践/a.md",
                title="配置命名口径",
                status="active",
                topics=("配置", "命名"),
                related=('"[[20-Knowledge/工程实践/b|内嵌配置文件名]]"',),
            ),
            make_note(
                "20-Knowledge/工程实践/b.md",
                title="内嵌配置文件名",
                status="active",
                topics=("配置", "命名"),
                related=('"[[20-Knowledge/工程实践/a]]"',),
            ),
        ]
        self.assertEqual(AUDIT.group_conflict_candidates(notes), [])

    def test_one_sided_related_still_groups(self) -> None:
        """只有单侧 related 不算裁决痕迹，仍要作为候选报出。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增单侧关联负例，防豁免过宽。
        """
        notes = [
            make_note(
                "20-Knowledge/工程实践/a.md",
                title="配置命名口径",
                status="active",
                topics=("配置", "命名"),
                related=("[[20-Knowledge/工程实践/b|内嵌配置文件名]]",),
            ),
            make_note(
                "20-Knowledge/工程实践/b.md",
                title="内嵌配置文件名",
                status="active",
                topics=("配置", "命名"),
            ),
        ]
        self.assertEqual(len(AUDIT.group_conflict_candidates(notes)), 1)

    def test_cross_theme_similar_titles_still_group(self) -> None:
        """标题高度相似是跨主题例外通道：分类不同也要报，因为那基本是重复写入。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增跨主题标题相似正例。
        """
        notes = [
            make_note("20-Knowledge/代码规则/a.md", title="配置来源优先级限制", status="active"),
            make_note("20-Knowledge/项目/b.md", title="配置来源优先级约束", status="active"),
        ]
        self.assertEqual(len(AUDIT.group_conflict_candidates(notes)), 1)

    def test_min_shared_tags_constant_is_two(self) -> None:
        """共享标签下限必须是 2；退回 1 会让候选清单重新被误报淹没。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增下限常量断言。
        """
        self.assertEqual(AUDIT.MIN_SHARED_TAGS, 2)

    def test_similar_titles_group_without_shared_topic(self) -> None:
        """标题高度相似即使没有共同标签也应归入候选组。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 fixture 标题换为与已废除工具无关的中性样本。
        """
        notes = [
            make_note("20-Knowledge/a.md", title="配置来源优先级限制", status="active"),
            make_note("20-Knowledge/b.md", title="配置来源优先级约束", status="active"),
        ]
        self.assertEqual(len(AUDIT.group_conflict_candidates(notes)), 1)

    def test_non_active_notes_are_not_grouped(self) -> None:
        """已取代或已归档的笔记不再造成检索歧义，不进候选组。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 路径改为裸相对路径。
        """
        notes = [
            make_note("20-Knowledge/a.md", title="同一个主题", status="superseded", topics=("配置",)),
            make_note("20-Knowledge/b.md", title="同一个主题", status="active", topics=("配置",)),
        ]
        self.assertEqual(AUDIT.group_conflict_candidates(notes), [])

    def test_report_flags_non_active_and_dangling_pointer(self) -> None:
        """报告要分别列出状态非当前有效与标了已取代却缺接替者的笔记。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 路径改为裸相对路径。
        """
        notes = [
            make_note("20-Knowledge/a.md", title="缺接替者", status="superseded"),
            make_note("20-Knowledge/b.md", title="有接替者", status="superseded", superseded_by=("[[新笔记]]",)),
            make_note("20-Knowledge/c.md", title="正常", status="active"),
        ]
        candidates = AUDIT.build_report(notes, [])["candidates"]
        self.assertEqual(len(candidates["non_active_status"]), 2)
        self.assertEqual([item["path"] for item in candidates["superseded_without_pointer"]], ["20-Knowledge/a.md"])

    def test_report_records_unreadable_notes(self) -> None:
        """头部读不出来的笔记必须单独列出，不能被静默忽略。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 路径改为裸相对路径。
        """
        notes = [make_note("20-Knowledge/x.md", read_error="frontmatter 不是合法 JSON")]
        report = AUDIT.build_report(notes, [])
        self.assertEqual(len(report["unreadable_notes"]), 1)
        self.assertIn("disposition_hint", report)


class FrontmatterParsingTest(unittest.TestCase):
    """头部解析组：校验 frontmatter 标量、列表与缺失情形的处理。"""

    def test_list_field_accepts_inline_and_block(self) -> None:
        """列表字段无论行内数组还是块状条目都要归一成字符串元组。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 由 as_tuple 改为 parse_list_field 契约。
        """
        inline = '---\ntopics: ["配置", "命名"]\n---\n正文\n'
        block = "---\ntopics:\n  - 配置\n  - 命名\n---\n正文\n"
        scalar = "---\ntopics: 配置\n---\n正文\n"
        self.assertEqual(AUDIT.parse_list_field(inline, "topics"), ("配置", "命名"))
        self.assertEqual(AUDIT.parse_list_field(block, "topics"), ("配置", "命名"))
        self.assertEqual(AUDIT.parse_list_field(scalar, "topics"), ("配置",))
        self.assertEqual(AUDIT.parse_list_field("没有头部\n", "topics"), ())

    def test_scalar_field_is_unquoted(self) -> None:
        """标量字段解析要去掉引号，供状态治理直接比对。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 新增 parse_frontmatter 契约。
        """
        text = '---\nstatus: "active"\ntitle: 配置口径\n---\n正文\n'
        parsed = AUDIT.parse_frontmatter(text)
        self.assertEqual(parsed["status"], "active")
        self.assertEqual(parsed["title"], "配置口径")

    def test_missing_frontmatter_is_flagged(self) -> None:
        """没有 frontmatter 的笔记必须被标成读取失败，不能静默参与状态治理。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-12 替代原 NO_FRONTMATTER_MARKER 断言。
        """
        self.assertEqual(AUDIT.parse_frontmatter("没有头部的正文\n"), {})
        source = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("no frontmatter", source)


if __name__ == "__main__":
    unittest.main()
