# -*- coding: utf-8 -*-
"""sync_recent_project_sessions 专项测试。"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# 将脚本目录加入 sys.path
SCRIPT_DIR = Path(__file__).parent.parent.parent / "project-memory-rules" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from sync_recent_project_sessions import (
    BEGIN_MARKER,
    END_MARKER,
    build_session_line,
    format_cst_time,
    map_status,
    normalize_project_root,
    redact_sensitive,
    render_section,
    sanitize_text,
    sync_recent_sessions,
    truncate_unicode,
    SyncError,
)


def make_session(
    session_id="019f-ac2c-7383-903c-70d2d8bd85f6",
    project_root="F:/luode-skills",
    title="测试任务",
    summary="测试摘要",
    status="active",
    updated_at="2026-08-10T06:00:00Z",
    kind="codex",
):
    return {
        "id": session_id,
        "projectRoot": project_root,
        "title": title,
        "summary": summary,
        "status": status,
        "updatedAt": updated_at,
        "kind": kind,
    }


class TestSanitize(unittest.TestCase):
    def test_sanitize_markdown(self):
        result = sanitize_text("**标题** [链接](http://x) `code`")
        self.assertNotIn("*", result)
        self.assertNotIn("[", result)
        self.assertNotIn("]", result)
        self.assertNotIn("`", result)

    def test_sanitize_html(self):
        result = sanitize_text("<script>alert(1)</script> 正常文本")
        self.assertNotIn("<", result)
        # HTML_RE 只移除标签，标签间内容保留
        self.assertIn("正常文本", result)
        # 控制字符被移除
        self.assertNotIn("<", result)

    def test_sanitize_control_chars(self):
        result = sanitize_text("正常\x00\x1f文本")
        self.assertEqual(result, "正常文本")

    def test_redact_sensitive(self):
        result = redact_sensitive("api_key=abcdef1234567890")
        self.assertIn("[REDACTED]", result)
        self.assertNotIn("abcdef1234567890", result)

    def test_redact_token_prefix(self):
        result = redact_sensitive("sk-abcdef1234567890abcdef1234567890")
        self.assertIn("[REDACTED]", result)

    def test_redact_windows_path(self):
        result = redact_sensitive("截图在 C:\\Users\\luode\\Pictures\\test.png 中")
        self.assertIn("[PATH-REDACTED]", result)
        self.assertNotIn("C:\\Users\\luode\\Pictures", result)


class TestTruncate(unittest.TestCase):
    def test_truncate_ascii(self):
        self.assertEqual(truncate_unicode("a" * 60, 48), "a" * 48)

    def test_truncate_unicode(self):
        text = "中" * 60
        result = truncate_unicode(text, 48)
        self.assertEqual(result, "中" * 48)


class TestTimeAndStatus(unittest.TestCase):
    def test_format_cst_time(self):
        result = format_cst_time("2026-08-10T06:00:00Z")
        self.assertEqual(result, "2026-08-10 14:00:00 +08:00")

    def test_format_with_offset(self):
        result = format_cst_time("2026-08-10T06:00:00+00:00")
        self.assertEqual(result, "2026-08-10 14:00:00 +08:00")

    def test_map_status(self):
        self.assertEqual(map_status("active"), "活动中")
        self.assertEqual(map_status("idle"), "空闲")
        self.assertEqual(map_status("notLoaded"), "未加载")
        self.assertEqual(map_status("unknown"), "未知")


class TestSessionLine(unittest.TestCase):
    def test_build_session_line(self):
        session = make_session()
        line = build_session_line(session)
        self.assertIn("2026-08-10 14:00:00 +08:00", line)
        self.assertIn("[活动中]", line)
        self.assertIn("测试任务", line)
        self.assertIn("测试摘要", line)

    def test_empty_summary_fallback(self):
        session = make_session(summary="")
        line = build_session_line(session)
        self.assertIn("无摘要", line)


class TestNormalizeProjectRoot(unittest.TestCase):
    def test_normalize_windows(self):
        self.assertEqual(normalize_project_root("F:\\luode-skills"), "f:/luode-skills")
        self.assertEqual(normalize_project_root("F:/luode-skills/"), "f:/luode-skills")
        self.assertEqual(normalize_project_root("F:/luode-skills"), "f:/luode-skills")


class TestRenderSection(unittest.TestCase):
    def test_render_section(self):
        sessions = [make_session()]
        section = render_section(sessions)
        self.assertIn(BEGIN_MARKER, section)
        self.assertIn(END_MARKER, section)
        self.assertIn("## 最近 5 个同项目会话", section)
        self.assertIn("只读回忆索引", section)


class TestSync(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_current = Path(self.temp_dir.name) / "PROJECT_CURRENT.md"
        self.project_current.write_text(
            "# 项目当前状态\n\n## 已完成\n\n- 测试\n\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_section_when_missing(self):
        sessions = [make_session()]
        result = sync_recent_sessions(
            str(self.project_current),
            "F:/luode-skills",
            sessions,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["action"], "created")
        self.assertEqual(result["entry_count"], 1)
        content = self.project_current.read_text(encoding="utf-8")
        self.assertIn(BEGIN_MARKER, content)

    def test_replace_when_exists(self):
        sessions = [make_session()]
        sync_recent_sessions(str(self.project_current), "F:/luode-skills", sessions)
        content1 = self.project_current.read_text(encoding="utf-8")
        # 改变摘要后再次同步
        sessions2 = [make_session(title="新标题", summary="新摘要")]
        result = sync_recent_sessions(str(self.project_current), "F:/luode-skills", sessions2)
        self.assertEqual(result["action"], "replaced")
        content2 = self.project_current.read_text(encoding="utf-8")
        self.assertIn("新标题", content2)
        self.assertNotIn("测试任务", content2)

    def test_preserves_task_projection(self):
        # 先加入任务投影
        projection_block = (
            "<!-- BEGIN TASK PLAN PROJECTION -->\n"
            "```json\n{\"version\": 4, \"projections\": [{\"session_id\": \"abc\"}]}\n"
            "```\n"
            "<!-- END TASK PLAN PROJECTION -->\n"
        )
        self.project_current.write_text(
            "# 项目当前状态\n\n" + projection_block,
            encoding="utf-8",
        )
        sessions = [make_session()]
        sync_recent_sessions(str(self.project_current), "F:/luode-skills", sessions)
        content = self.project_current.read_text(encoding="utf-8")
        self.assertIn(projection_block, content)

    def test_filters_other_project(self):
        sessions = [
            make_session(project_root="F:/other-project"),
            make_session(project_root="F:/luode-skills"),
        ]
        result = sync_recent_sessions(
            str(self.project_current),
            "F:/luode-skills",
            sessions,
        )
        self.assertEqual(result["entry_count"], 1)
        content = self.project_current.read_text(encoding="utf-8")
        self.assertIn("测试任务", content)
        self.assertNotIn("F:/other-project", content)

    def test_only_keeps_five(self):
        sessions = [
            make_session(session_id=f"id-{i}", title=f"会话{i}", updated_at=f"2026-08-10T0{i}:00:00Z")
            for i in range(1, 8)
        ]
        result = sync_recent_sessions(str(self.project_current), "F:/luode-skills", sessions)
        self.assertEqual(result["entry_count"], 5)
        content = self.project_current.read_text(encoding="utf-8")
        self.assertNotIn("会话1", content)
        self.assertIn("会话7", content)

    def test_new_replaces_old_fifth(self):
        sessions_a = [
            make_session(session_id=f"id-{i}", title=f"会话{i}", updated_at=f"2026-08-10T0{i}:00:00Z")
            for i in range(1, 7)
        ]
        sync_recent_sessions(str(self.project_current), "F:/luode-skills", sessions_a)
        content1 = self.project_current.read_text(encoding="utf-8")
        self.assertNotIn("会话1", content1)

        # 新会话进入后，会话2 被替换
        sessions_b = [
            make_session(session_id=f"id-{i}", title=f"会话{i}", updated_at=f"2026-08-10T0{i}:00:00Z")
            for i in range(2, 8)
        ]
        sync_recent_sessions(str(self.project_current), "F:/luode-skills", sessions_b)
        content2 = self.project_current.read_text(encoding="utf-8")
        self.assertNotIn("会话2", content2)
        self.assertIn("会话7", content2)

    def test_half_marker_rejected(self):
        self.project_current.write_text(
            "# 项目当前状态\n\n<!-- BEGIN RECENT PROJECT SESSIONS -->\n\n",
            encoding="utf-8",
        )
        with self.assertRaises(SyncError):
            sync_recent_sessions(str(self.project_current), "F:/luode-skills", [make_session()])

    def test_duplicate_marker_rejected(self):
        self.project_current.write_text(
            "# 项目当前状态\n\n"
            + BEGIN_MARKER + "\n\n" + END_MARKER + "\n\n"
            + BEGIN_MARKER + "\n\n" + END_MARKER + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(SyncError):
            sync_recent_sessions(str(self.project_current), "F:/luode-skills", [make_session()])

    def test_size_limit_51200(self):
        # 构造接近 51200 字节的文件
        # 需确保加上快照后超过51200。快照约800字节，所以base填50800
        base = "# 项目当前状态\n\n" + "x" * 51000 + "\n"
        self.project_current.write_text(base, encoding="utf-8")
        # 添加少量快照应该超过 51200
        sessions = [make_session()]
        with self.assertRaises(SyncError):
            sync_recent_sessions(str(self.project_current), "F:/luode-skills", sessions)

    def test_section_size_limit(self):
        # 用 patching 模拟超限
        import sync_recent_project_sessions as mod
        orig = mod.MAX_SECTION_BYTES
        mod.MAX_SECTION_BYTES = 100
        sessions = [make_session()]
        raised = False
        try:
            sync_recent_sessions(str(self.project_current), "F:/luode-skills", sessions)
        except SyncError:
            raised = True
        except Exception:
            pass
        mod.MAX_SECTION_BYTES = orig
        self.assertTrue(raised, "Should have raised SyncError")


class TestIdempotency(unittest.TestCase):
    def test_second_run_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            pc = Path(tmp) / "PROJECT_CURRENT.md"
            pc.write_text("# 项目当前状态\n\n", encoding="utf-8")
            sessions = [make_session()]
            sync_recent_sessions(str(pc), "F:/luode-skills", sessions)
            sync_recent_sessions(str(pc), "F:/luode-skills", sessions)
            content = pc.read_text(encoding="utf-8")
            self.assertEqual(content.count(BEGIN_MARKER), 1)
            self.assertEqual(content.count(END_MARKER), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
