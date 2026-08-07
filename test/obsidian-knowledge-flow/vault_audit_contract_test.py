"""验证知识库只读巡检脚本的零写入约束与候选判定纯函数。"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AUDIT_PATH = ROOT / "obsidian-knowledge-flow" / "scripts" / "audit_vault_knowledge.py"
# 任何写操作命令名出现在巡检源码里都视为越界；巡检必须保持只读。
FORBIDDEN_COMMANDS = ("property-set", "property_set", '"move"', '"delete"', '"create"', '"append"')


def load_audit() -> Any:
    """按文件路径加载巡检模块，避免依赖带连字符的目录可导入。

    [参数] 无。
    [返回] Any：已加载的巡检模块对象。
    最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
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

    [参数] path：笔记路径；overrides：需要覆盖的字段。
    [返回] Any：巡检事实对象。
    最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
    """
    return AUDIT.NoteFacts(path=path, **overrides)


class ReadOnlyGuardTest(unittest.TestCase):
    """只读约束组：校验巡检源码不含任何写操作入口。"""

    def test_source_contains_no_write_command(self) -> None:
        """巡检源码不得出现写操作命令名。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        source = AUDIT_PATH.read_text(encoding="utf-8")
        for command in FORBIDDEN_COMMANDS:
            self.assertNotIn(command, source, f"巡检脚本出现写操作命令：{command}")

    def test_only_readonly_bridge_commands_are_invoked(self) -> None:
        """巡检只允许调用四个只读桥接命令。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        source = AUDIT_PATH.read_text(encoding="utf-8")
        invoked = {line.split('run_bridge("', 1)[1].split('"', 1)[0] for line in source.splitlines() if 'run_bridge("' in line}
        self.assertEqual(invoked, {"doctor", "files", "properties", "orphans"})

    def test_execution_cases_are_skipped(self) -> None:
        """执行案例目录不参与分级处置，巡检必须跳过。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        self.assertEqual(AUDIT.EXECUTION_CASE_PREFIX, "知识库/20-Knowledge/execution-failure-cases/")
        report = AUDIT.build_report([], ["知识库/20-Knowledge/execution-failure-cases/owner/case.md"])
        self.assertEqual(report["candidates"]["orphans"], [])


class CandidateGroupingTest(unittest.TestCase):
    """候选判定组：校验四类候选的纯函数判定。"""

    def test_shared_topic_groups_active_notes(self) -> None:
        """主题标签有交集且均为当前有效的笔记要归入同一候选组。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        notes = [
            make_note("知识库/20-Knowledge/a.md", title="配置命名口径", status="active", topics=("配置",)),
            make_note("知识库/20-Knowledge/b.md", title="内嵌配置文件名", status="active", topics=("配置",)),
        ]
        groups = AUDIT.group_conflict_candidates(notes)
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]["members"]), 2)

    def test_similar_titles_group_without_shared_topic(self) -> None:
        """标题高度相似即使没有共同标签也应归入候选组。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        notes = [
            make_note("知识库/20-Knowledge/a.md", title="Obsidian CLI 回显编码限制", status="active"),
            make_note("知识库/20-Knowledge/b.md", title="Obsidian CLI 回显编码约束", status="active"),
        ]
        self.assertEqual(len(AUDIT.group_conflict_candidates(notes)), 1)

    def test_non_active_notes_are_not_grouped(self) -> None:
        """已取代或已归档的笔记不再造成检索歧义，不进候选组。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        notes = [
            make_note("知识库/20-Knowledge/a.md", title="同一个主题", status="superseded", topics=("配置",)),
            make_note("知识库/20-Knowledge/b.md", title="同一个主题", status="active", topics=("配置",)),
        ]
        self.assertEqual(AUDIT.group_conflict_candidates(notes), [])

    def test_report_flags_non_active_and_dangling_pointer(self) -> None:
        """报告要分别列出状态非当前有效与标了已取代却缺接替者的笔记。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        notes = [
            make_note("知识库/20-Knowledge/a.md", title="缺接替者", status="superseded"),
            make_note("知识库/20-Knowledge/b.md", title="有接替者", status="superseded", superseded_by=("[[新笔记]]",)),
            make_note("知识库/20-Knowledge/c.md", title="正常", status="active"),
        ]
        candidates = AUDIT.build_report(notes, [])["candidates"]
        self.assertEqual(len(candidates["non_active_status"]), 2)
        self.assertEqual([item["path"] for item in candidates["superseded_without_pointer"]], ["知识库/20-Knowledge/a.md"])

    def test_report_records_unreadable_notes(self) -> None:
        """头部读不出来的笔记必须单独列出，不能被静默忽略。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        notes = [make_note("知识库/20-Knowledge/x.md", read_error="frontmatter 不是合法 JSON")]
        report = AUDIT.build_report(notes, [])
        self.assertEqual(len(report["unreadable_notes"]), 1)
        self.assertIn("disposition_hint", report)

    def test_property_list_and_scalar_are_normalized(self) -> None:
        """头部字段无论标量还是列表都要归一成字符串元组。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        self.assertEqual(AUDIT.as_tuple(None), ())
        self.assertEqual(AUDIT.as_tuple("配置"), ("配置",))
        self.assertEqual(AUDIT.as_tuple(["a", "", "b"]), ("a", "b"))

    def test_cli_error_payload_is_detected(self) -> None:
        """退出码为零的错误载荷必须被识别为读取失败。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 17:50:00 新增巡检脚本契约测试。
        """
        self.assertTrue(AUDIT.is_cli_error('Error: File "x.md" not found.'))
        self.assertFalse(AUDIT.is_cli_error('{"status": "active"}'))

    def test_missing_frontmatter_is_distinguished(self) -> None:
        """没有 frontmatter 与解析失败必须区分，报告才可据以行动。

        [参数] 无。
        [返回] None：断言失败时抛出 AssertionError。
        最近修改时间: 2026-08-05 18:00:00 区分缺少 frontmatter 与解析失败。
        """
        self.assertEqual(AUDIT.NO_FRONTMATTER_MARKER, "No frontmatter found.")
        source = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("笔记没有 frontmatter，无法参与状态治理", source)
        self.assertFalse(AUDIT.is_cli_error(AUDIT.NO_FRONTMATTER_MARKER))


if __name__ == "__main__":
    unittest.main()
