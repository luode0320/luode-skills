#!/usr/bin/env python3
"""渲染并校验执行失败知识案例，不直接读写 Obsidian vault。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ALLOWED_STATES = {"candidate", "active", "stale", "conflicted", "rejected"}
REQUIRED_FIELDS = (
    "case_id",
    "owner_skill",
    "category",
    "tool_or_model",
    "tool_major",
    "error_signature",
    "minimal_input",
    "input_fingerprint",
    "root_cause",
    "solution",
    "verification_command",
    "success_criteria",
    "scope",
    "avoid",
    "source",
    "updated",
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)\b(token|password|secret|api[_-]?key)\s*[=:]\s*[^\s,;]+"),
    re.compile(r"(?i)\b(authorization)\s*:\s*[^\s,;]+"),
)
PRIVATE_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\Users\\[^\s]+|/home/[^\s]+)")


def sanitize(value: str) -> str:
    """脱敏案例文本。

    [参数] value: 待写入案例的文本。
    [返回] 删除凭据和私有路径后的文本。
    最近修改时间: 2026-07-14 增加 Obsidian 执行案例脱敏渲染。
    """
    result = value
    for pattern in SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return PRIVATE_PATH_PATTERN.sub("<workspace>", result)


def text_value(payload: dict[str, Any], field: str) -> str:
    """读取并脱敏一个必填文本字段。"""
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return sanitize(value.strip())


def case_key(payload: dict[str, Any]) -> str:
    """根据稳定字段生成可读的跨项目去重键。"""
    parts = (
        text_value(payload, "owner_skill"),
        text_value(payload, "category"),
        text_value(payload, "tool_major"),
        text_value(payload, "error_signature"),
        text_value(payload, "input_fingerprint"),
        text_value(payload, "scope"),
    )
    normalized = "|".join(" ".join(part.split()).lower() for part in parts)
    return normalized


def validate(payload: dict[str, Any]) -> None:
    """校验案例字段、状态和环境边界。

    [参数] payload: 尚未渲染的案例对象。
    [返回] 无；不满足契约时抛出 ValueError。
    最近修改时间: 2026-07-14 增加案例状态与 local-only 门禁。
    """
    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    state = payload.get("state", "candidate")
    if state not in ALLOWED_STATES:
        raise ValueError(f"unsupported state: {state}")
    if payload.get("environment", "local") != "local":
        raise ValueError("execution cases must use local environment")
    if payload.get("expected_negative") or payload.get("business_bug"):
        raise ValueError("expected negative tests and business bugs are not reusable cases")
    for field in REQUIRED_FIELDS:
        text_value(payload, field)
    for field in ("negative_example", "positive_example"):
        text_value(payload, field)


def yaml_scalar(value: str) -> str:
    """以 JSON 字符串形式输出兼容 YAML 的安全标量。"""
    return json.dumps(value, ensure_ascii=False)


def render(payload: dict[str, Any]) -> str:
    """生成可通过 bridge create/append 写入的案例 Markdown。

    [参数] payload: 已通过 validate 的案例对象。
    [返回] UTF-8 Markdown 文本。
    最近修改时间: 2026-07-14 增加正反例和追加式状态事件正文。
    """
    validate(payload)
    values = {field: text_value(payload, field) for field in REQUIRED_FIELDS}
    state = payload.get("state", "candidate")
    today = text_value(payload, "updated")
    key = case_key(payload)
    lines = [
        "---",
        f"id: {yaml_scalar(values['case_id'])}",
        "type: knowledge",
        f"title: {yaml_scalar('执行失败案例 - ' + values['case_id'])}",
        "aliases: [\"execution failure\", \"执行失败\"]",
        "tags: [execution-failure, verified-example]",
        f"status: {state}",
        f"created: {yaml_scalar(today)}",
        f"updated: {yaml_scalar(today)}",
        f"knowledge_kind: execution_case",
        f"case_key: {yaml_scalar(key)}",
        f"case_state: {yaml_scalar(state)}",
        f"owner_skill: {yaml_scalar(values['owner_skill'])}",
        f"category: {yaml_scalar(values['category'])}",
        "environment: local",
        f"tool_or_model: {yaml_scalar(values['tool_or_model'])}",
        f"tool_major: {yaml_scalar(values['tool_major'])}",
        f"input_fingerprint: {yaml_scalar(values['input_fingerprint'])}",
        f"source: {yaml_scalar(values['source'])}",
        "---",
        "",
        "## 失败特征",
        f"- 类别：{values['category']}",
        f"- 工具或模型：{values['tool_or_model']}",
        f"- 稳定错误特征：{values['error_signature']}",
        f"- 最小输入摘要：{values['minimal_input']}",
        "",
        "## 反例",
        values["negative_example"],
        "",
        "## 正例",
        values["positive_example"],
        "",
        "## 根因与正确方案",
        f"- 根因：{values['root_cause']}",
        f"- 正确方案：{values['solution']}",
        f"- 适用范围：{values['scope']}",
        f"- 禁止动作：{values['avoid']}",
        "",
        "## 验证证据",
        f"- 入口：{values['verification_command']}",
        f"- 成功标准：{values['success_criteria']}",
        f"- 环境：local",
        "",
        "## 状态事件",
        f"### {today} | {state} | created",
        "- 原因：案例由受控渲染器生成。",
        "- 证据：后续状态只能通过 bridge append 追加。",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="render a sanitized Obsidian execution case")
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 JSON case input")
    parser.add_argument("--output", required=True, type=Path, help="UTF-8 Markdown output")
    return parser.parse_args()


def main() -> int:
    """执行 JSON 读取、契约校验和 UTF-8 Markdown 写入。"""
    args = parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("case input must be a JSON object")
    args.output.write_text(render(payload), encoding="utf-8", newline="\n")
    print(json.dumps({"ok": True, "case_key": case_key(payload)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
