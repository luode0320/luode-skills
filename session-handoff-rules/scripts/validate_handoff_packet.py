#!/usr/bin/env python3
"""校验会话交接包的结构、大小和脱敏边界。"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import sys
from typing import Any


MAX_PACKET_BYTES = 24_576
MAX_LIST_ITEMS = 40
MAX_ITEM_CHARS = 2_000

TOP_LEVEL_FIELDS = {
    "schema_version",
    "packet_type",
    "created_at",
    "task_summary",
    "goal",
    "scope",
    "completed",
    "in_progress",
    "next_steps",
    "blocked",
    "validation",
    "decisions",
    "continuation",
}
CONTINUATION_FIELDS = {"project_alias", "environment", "archive_policy", "new_session_prompt"}
SCOPE_FIELDS = {"in_scope", "out_of_scope"}

SENSITIVE_KEY_PATTERN = re.compile(
    r"(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|password|secret|private[_ -]?key|"
    r"authorization|cookie|connection[_ -]?string|credential|session[_ -]?id|thread[_ -]?id)",
    re.IGNORECASE,
)
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|password|secret|token)\s*[:=]\s*\S+"),
    re.compile(r"(?i)\bbearer\s+[a-z0-9._-]{12,}"),
    re.compile(r"\b(?:sk|rk)-[a-zA-Z0-9_-]{16,}\b"),
    re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:mysql|postgres(?:ql)?|mongodb(?:\+srv)?|redis)://[^\s]*@"),
    re.compile(r"(?:[A-Za-z]:\\|\\\\|/(?:home|Users|mnt)/)"),
)


def _add_error(errors: list[str], message: str) -> None:
    """追加去重后的字段错误，保持命令行输出稳定。

    [参数] errors: 错误列表；message: 待追加的错误文本。
    [返回] 无。
    最近修改时间：2026-08-02 03:29:00；统一交接包错误输出并去重。
    """

    # 1. 仅追加尚未出现的错误，避免重复噪声。
    if message not in errors:
        errors.append(message)


def _validate_string(value: Any, path: str, errors: list[str], *, required: bool = False) -> None:
    """校验字符串类型、长度、控制字符和敏感模式。

    [参数] value: 待校验值；path: 字段路径；errors: 错误列表；required: 是否非空。
    [返回] 无。
    最近修改时间：2026-08-02 03:29:00；收敛交接包字符串安全边界。
    """

    # 1. 先确认类型，避免后续字符串操作触发异常。
    if not isinstance(value, str):
        _add_error(errors, f"{path} 必须是字符串")
        return
    # 2. 检查非空约束、控制字符和长度上限。
    if required and not value.strip():
        _add_error(errors, f"{path} 不能为空")
    if "\x00" in value or any(ord(char) < 32 and char not in "\n\r\t" for char in value):
        _add_error(errors, f"{path} 含有控制字符")
    if len(value) > MAX_ITEM_CHARS:
        _add_error(errors, f"{path} 超过 {MAX_ITEM_CHARS} 个字符")
    # 3. 拒绝秘密、鉴权值和绝对路径，避免把本机信息带入新任务。
    for pattern in SENSITIVE_VALUE_PATTERNS:
        if pattern.search(value):
            _add_error(errors, f"{path} 命中敏感信息或绝对路径模式")
            break


def _walk_for_sensitive_keys(value: Any, path: str, errors: list[str]) -> None:
    """递归检查所有对象字段名和字符串值。

    [参数] value: 当前节点；path: 当前节点路径；errors: 错误列表。
    [返回] 无。
    最近修改时间：2026-08-02 03:29:00；覆盖嵌套字段的敏感信息扫描。
    """

    # 1. 递归遍历对象、数组和字符串节点。
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                _add_error(errors, f"{path} 含有非字符串字段名")
                continue
            if SENSITIVE_KEY_PATTERN.search(key):
                _add_error(errors, f"{path}.{key} 是禁止的敏感字段")
            _walk_for_sensitive_keys(child, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_for_sensitive_keys(child, f"{path}[{index}]", errors)
    elif isinstance(value, str):
        _validate_string(value, path, errors)


def _validate_string_list(value: Any, path: str, errors: list[str], *, required: bool = False) -> None:
    """校验交接包中的字符串数组及其数量上限。

    [参数] value: 待校验数组；path: 字段路径；errors: 错误列表；required: 是否至少一项。
    [返回] 无。
    最近修改时间：2026-08-02 03:29:00；固定任务列表的数量和类型契约。
    """

    # 1. 确认数组类型和数量边界。
    if not isinstance(value, list):
        _add_error(errors, f"{path} 必须是数组")
        return
    if required and not value:
        _add_error(errors, f"{path} 至少需要一项")
    if len(value) > MAX_LIST_ITEMS:
        _add_error(errors, f"{path} 超过 {MAX_LIST_ITEMS} 项")
    # 2. 逐项复用字符串安全校验。
    for index, item in enumerate(value):
        _validate_string(item, f"{path}[{index}]", errors, required=True)


def _validate_utc_timestamp(value: Any, errors: list[str]) -> None:
    """校验交接包创建时间为带 UTC 时区的 ISO-8601 字符串。

    [参数] value: 创建时间值；errors: 错误列表。
    [返回] 无。
    最近修改时间：2026-08-02 03:29:00；防止跨时区交接时间歧义。
    """

    # 1. 先确认字符串类型，再解析 ISO-8601 时间。
    if not isinstance(value, str):
        _add_error(errors, "$.created_at 必须是字符串")
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        _add_error(errors, "$.created_at 必须是 ISO-8601 时间")
        return
    # 2. 只接受带 UTC 偏移的时间，避免本地时区误读。
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        _add_error(errors, "$.created_at 必须带 UTC 时区")


def validate_packet(packet: Any, *, encoded_size: int | None = None, max_bytes: int = MAX_PACKET_BYTES) -> list[str]:
    """校验交接包结构并返回字段级错误。

    [参数] packet: JSON 解码后的对象；encoded_size: UTF-8 字节数；max_bytes: 大小上限。
    [返回] list[str]：校验错误列表，空列表表示有效。
    最近修改时间：2026-08-02 03:29:00；实现交接包结构和安全闸门。
    """

    # 1. 先校验大小和顶层类型，避免对非法对象做深层访问。
    errors: list[str] = []
    if encoded_size is not None and encoded_size > max_bytes:
        _add_error(errors, f"交接包超过 {max_bytes} 字节")
    if not isinstance(packet, dict):
        return ["交接包顶层必须是 JSON 对象"]

    # 2. 拒绝未知或缺失的顶层字段，保持契约可预测。
    unknown = set(packet) - TOP_LEVEL_FIELDS
    for key in sorted(unknown):
        _add_error(errors, f"$ 中存在未知字段 {key}")
    missing = TOP_LEVEL_FIELDS - set(packet)
    for key in sorted(missing):
        _add_error(errors, f"$ 缺少必填字段 {key}")

    # 3. 校验版本、时间和任务摘要的基础类型。
    _validate_utc_timestamp(packet.get("created_at"), errors)
    _validate_string(packet.get("schema_version"), "$.schema_version", errors, required=True)
    _validate_string(packet.get("packet_type"), "$.packet_type", errors, required=True)
    if packet.get("schema_version") != "1.0":
        _add_error(errors, "$.schema_version 必须为 1.0")
    if packet.get("packet_type") != "codex-session-handoff":
        _add_error(errors, "$.packet_type 必须为 codex-session-handoff")
    _validate_string(packet.get("task_summary"), "$.task_summary", errors, required=True)
    _validate_string(packet.get("goal"), "$.goal", errors, required=True)

    # 4. 校验范围对象的固定字段。
    scope = packet.get("scope")
    if not isinstance(scope, dict):
        _add_error(errors, "$.scope 必须是对象")
    else:
        for key in sorted(set(scope) - SCOPE_FIELDS):
            _add_error(errors, f"$.scope 中存在未知字段 {key}")
        for key in sorted(SCOPE_FIELDS - set(scope)):
            _add_error(errors, f"$.scope 缺少字段 {key}")
        # 4.1 范围数组必须保持字符串列表。
        for key in sorted(SCOPE_FIELDS & set(scope)):
            _validate_string_list(scope[key], f"$.scope.{key}", errors)

    # 5. 校验六类任务状态数组，下一步数组必须非空。
    for key in ("completed", "in_progress", "next_steps", "blocked", "validation", "decisions"):
        if key in packet:
            _validate_string_list(packet[key], f"$.{key}", errors, required=key == "next_steps")

    # 6. 校验新任务的项目、环境和归档策略。
    continuation = packet.get("continuation")
    if not isinstance(continuation, dict):
        _add_error(errors, "$.continuation 必须是对象")
    else:
        for key in sorted(set(continuation) - CONTINUATION_FIELDS):
            _add_error(errors, f"$.continuation 中存在未知字段 {key}")
        for key in sorted(CONTINUATION_FIELDS - set(continuation)):
            _add_error(errors, f"$.continuation 缺少字段 {key}")
        for key in sorted(CONTINUATION_FIELDS & set(continuation)):
            _validate_string(continuation[key], f"$.continuation.{key}", errors, required=True)
        if continuation.get("environment") != "local":
            _add_error(errors, "$.continuation.environment 必须为 local")
        if continuation.get("archive_policy") != "manual_only":
            _add_error(errors, "$.continuation.archive_policy 必须为 manual_only")

    # 7. 对所有嵌套节点执行最终敏感信息扫描。
    _walk_for_sensitive_keys(packet, "$", errors)
    return errors


def validate_file(path: Path, *, max_bytes: int = MAX_PACKET_BYTES) -> list[str]:
    """读取并校验一个 UTF-8 JSON 交接包。

    [参数] path: 交接包路径；max_bytes: 文件大小上限。
    [返回] list[str]：校验错误列表，空列表表示有效。
    最近修改时间：2026-08-02 03:29:00；提供只读文件校验入口。
    """

    # 1. 读取原始字节并先执行大小闸门。
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return [f"无法读取交接包：{exc}"]
    if len(raw) > max_bytes:
        return [f"交接包超过 {max_bytes} 字节"]
    # 2. 严格按 UTF-8 解码并解析 JSON。
    try:
        packet = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError:
        return ["交接包必须是严格 UTF-8"]
    except json.JSONDecodeError as exc:
        return [f"交接包不是有效 JSON：{exc.msg}"]
    return validate_packet(packet, encoded_size=len(raw), max_bytes=max_bytes)


def main(argv: list[str] | None = None) -> int:
    """执行命令行校验并返回进程退出码。

    [参数] argv: 可选命令行参数列表。
    [返回] int：有效返回 0，无效返回 1。
    最近修改时间：2026-08-02 03:29:00；提供稳定的本地 CLI 验证入口。
    """

    # 1. 解析输入路径和可选大小上限。
    parser = argparse.ArgumentParser(description="校验脱敏会话交接包")
    parser.add_argument("packet", type=Path, help="交接包 JSON 文件")
    parser.add_argument("--max-bytes", type=int, default=MAX_PACKET_BYTES)
    args = parser.parse_args(argv)
    # 2. 执行只读校验并输出机器可读的结论前缀。
    errors = validate_file(args.packet, max_bytes=args.max_bytes)
    if errors:
        for error in errors:
            print(f"INVALID: {error}")
        return 1
    print("VALID: session handoff packet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
