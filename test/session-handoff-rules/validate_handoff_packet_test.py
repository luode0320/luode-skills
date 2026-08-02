"""会话交接包校验脚本的本地契约测试。"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "session-handoff-rules" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_handoff_packet import validate_file, validate_packet  # noqa: E402


def valid_packet() -> dict:
    """返回不含敏感信息的最小有效交接包。

    [参数] 无。
    [返回] dict：最小有效交接包。
    最近修改时间：2026-08-02 03:29:00；为契约测试提供稳定样本。
    """

    # 1. 构造覆盖全部必填字段的本地样本。
    return {
        "schema_version": "1.0",
        "packet_type": "codex-session-handoff",
        "created_at": "2026-08-02T08:00:00Z",
        "task_summary": "继续维护会话交接 skill",
        "goal": "让新任务能够安全接续并完成验证",
        "scope": {"in_scope": ["交接包校验"], "out_of_scope": ["自动归档"]},
        "completed": ["确定触发词"],
        "in_progress": ["等待脚本测试"],
        "next_steps": ["运行契约测试"],
        "blocked": [],
        "validation": ["尚未运行真实测试"],
        "decisions": ["归档策略为 manual_only"],
        "continuation": {
            "project_alias": "skills",
            "environment": "local",
            "archive_policy": "manual_only",
            "new_session_prompt": "先命中检查并读取四件套。",
        },
    }


class ValidateHandoffPacketTests(unittest.TestCase):
    """验证交接包的正向和安全边界。"""

    def test_valid_packet_passes(self) -> None:
        """验证有效交接包通过校验。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-08-02 03:29:00；覆盖正向契约。
        """

        # 1. 有效样本必须返回空错误列表。
        self.assertEqual(validate_packet(valid_packet()), [])

    def test_next_steps_is_required_and_non_empty(self) -> None:
        """验证缺少下一步时被拒绝。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-08-02 03:29:00；覆盖任务接续必填边界。
        """

        # 1. 清空下一步数组，验证接续不可执行时阻断。
        packet = valid_packet()
        packet["next_steps"] = []
        errors = validate_packet(packet)
        self.assertTrue(any("next_steps" in error for error in errors))

    def test_sensitive_field_is_rejected(self) -> None:
        """验证敏感字段被拒绝。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-08-02 03:29:00；覆盖脱敏边界。
        """

        # 1. 注入敏感字段，验证字段白名单和扫描均能阻断。
        packet = valid_packet()
        packet["secret"] = "redacted-value"
        errors = validate_packet(packet)
        self.assertTrue(any("敏感字段" in error or "未知字段" in error for error in errors))

    def test_file_size_limit_is_enforced(self) -> None:
        """验证文件大小上限被执行。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-08-02 03:29:00；覆盖文件大小闸门。
        """

        # 1. 写入临时样本并以更小上限验证失败。
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "packet.json"
            path.write_text(json.dumps(valid_packet(), ensure_ascii=False), encoding="utf-8")
            errors = validate_file(path, max_bytes=64)
        self.assertTrue(any("字节" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
