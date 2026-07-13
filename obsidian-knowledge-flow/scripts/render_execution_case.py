#!/usr/bin/env python3
"""渲染并校验执行失败知识案例，不直接读写 Obsidian vault。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ALLOWED_STATES = {
    "candidate",
    "active",
    "stale",
    "conflicted",
    "superseded",
    "rejected",
}
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
    "created",
    "updated",
    "environment",
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(
        r"(?i)\b(?:token|password|secret|api[_-]?key|client[_-]?secret)\s*[=:]\s*"
        r"(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)"
    ),
    re.compile(r"(?i)\b(?:authorization|proxy-authorization)\s*:\s*[^\r\n]+"),
    re.compile(r"(?i)\b(?:cookie|set-cookie)\s*:\s*[^\r\n]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^\s]+"),
    re.compile(r"https?://[^\s?#]+\?[^\s#]+", re.IGNORECASE),
)
PRIVATE_PATH_PATTERN = re.compile(
    r"(?:[A-Za-z]:\\[^\s]+|/home/[^\s]+|/mnt/[A-Za-z]/[^\s]+)"
)
PII_PATTERNS = (
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),
)
CASE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{0,127}$")
DATE_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)?$"
)
INPUT_FINGERPRINT_PATTERN = re.compile(r"^sha256:[a-z0-9][a-z0-9._-]{2,127}$")


def sanitize(value: str) -> str:
    """脱敏案例文本。

    [参数] value: 待写入案例的文本。
    [返回] 删除凭据和私有路径后的文本。
    最近修改时间: 2026-07-14 增加 Obsidian 执行案例脱敏渲染。
    """
    result = value
    for pattern in SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    result = PRIVATE_PATH_PATTERN.sub("<workspace>", result)
    for pattern in PII_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def text_value(payload: dict[str, Any], field: str) -> str:
    """读取并脱敏一个必填文本字段。"""
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return sanitize(value.strip())


def validate_stable_field(value: str, field: str, *, allow_pipe: bool = False) -> None:
    """拒绝会污染去重键或状态事件结构的动态/路径字符。

    [参数] value: 待校验的稳定字段；field: 字段名；allow_pipe: 是否允许 scope 分隔符。
    [返回] 无；不满足稳定字段契约时抛出 ValueError。
    最近修改时间: 2026-07-14 收紧执行案例去重键和状态事件输入边界。
    """
    if any(ord(char) < 32 for char in value):
        raise ValueError(f"{field} contains control characters")
    if not allow_pipe and "|" in value:
        raise ValueError(f"{field} must not contain the case-key delimiter")
    if any(separator in value for separator in ("/", "\\", "..")):
        raise ValueError(f"{field} must not contain a path segment")


def validate_date(value: str, field: str) -> None:
    """确保 frontmatter 日期和状态事件标题保持 ISO 形式。

    [参数] value: 待校验的日期或时间文本；field: 字段名。
    [返回] 无；格式不正确时抛出 ValueError。
    最近修改时间: 2026-07-14 防止状态事件标题注入非结构化时间文本。
    """
    if not DATE_PATTERN.fullmatch(value):
        raise ValueError(f"{field} must be an ISO date or datetime")


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
    if state != "candidate":
        raise ValueError("new execution cases must start as candidate; append later state events")
    if payload.get("environment") != "local":
        raise ValueError("execution cases require explicit local environment")
    if payload.get("expected_negative") or payload.get("business_bug"):
        raise ValueError("expected negative tests and business bugs are not reusable cases")
    for field in REQUIRED_FIELDS:
        text_value(payload, field)
    for field in ("negative_example", "positive_example"):
        text_value(payload, field)
    case_id = text_value(payload, "case_id")
    if not CASE_ID_PATTERN.fullmatch(case_id):
        raise ValueError("case_id must be a safe ASCII slug")
    owner_skill = text_value(payload, "owner_skill")
    if not SLUG_PATTERN.fullmatch(owner_skill):
        raise ValueError("owner_skill must be a normalized skill slug")
    for field in ("category", "tool_major", "error_signature", "input_fingerprint"):
        validate_stable_field(text_value(payload, field), field)
    if not INPUT_FINGERPRINT_PATTERN.fullmatch(text_value(payload, "input_fingerprint")):
        raise ValueError("input_fingerprint must use a stable sha256:... value")
    validate_stable_field(text_value(payload, "scope"), "scope", allow_pipe=True)
    validate_date(text_value(payload, "updated"), "updated")
    validate_date(text_value(payload, "created"), "created")
    confidence = payload.get("confidence", "medium")
    if confidence not in {"low", "medium", "high"}:
        raise ValueError("confidence must be low, medium, or high")
    mode = payload.get("mode", "learn")
    if mode not in {"prevent", "recover", "learn"}:
        raise ValueError("mode must be prevent, recover, or learn")


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
    values = {
        field: text_value(payload, field)
        for field in (*REQUIRED_FIELDS, "negative_example", "positive_example")
    }
    state = payload.get("state", "candidate")
    created = text_value(payload, "created")
    today = text_value(payload, "updated")
    key = case_key(payload)
    owner = values["owner_skill"]
    case_path = f"知识库/20-Knowledge/execution-failure-cases/{owner}/{values['case_id']}.md"
    source_refs = json.dumps([values["source"]], ensure_ascii=False)
    confidence = payload.get("confidence", "medium")
    mode = payload.get("mode", "learn")
    failure_stage = sanitize(str(payload.get("failure_stage", "unknown")).strip() or "unknown")
    lines = [
        "---",
        f"id: {yaml_scalar(values['case_id'])}",
        "type: knowledge",
        f"title: {yaml_scalar('执行失败案例 - ' + values['case_id'])}",
        "aliases: [\"execution failure\", \"执行失败\"]",
        "tags: [execution-failure, verified-example]",
        f"status: {state}",
        f"created: {yaml_scalar(created)}",
        f"updated: {yaml_scalar(today)}",
        "source_sessions: []",
        f"source_refs: {source_refs}",
        "related: []",
        "entities: []",
        "topics: [\"执行失败持续学习\"]",
        f"confidence: {confidence}",
        "project_id: unknown",
        "project_name: unknown",
        "project_root_native: null",
        "project_root_windows: null",
        "project_root_wsl: null",
        "path_aliases: []",
        f"knowledge_kind: execution_case",
        "storage: obsidian",
        f"obsidian_path: {yaml_scalar(case_path)}",
        f"seed_source: {yaml_scalar(values['source'])}",
        f"case_key: {yaml_scalar(key)}",
        f"case_state: {yaml_scalar(state)}",
        f"owner_skill: {yaml_scalar(values['owner_skill'])}",
        f"category: {yaml_scalar(values['category'])}",
        f"error_signature: {yaml_scalar(values['error_signature'])}",
        f"scope: {yaml_scalar(values['scope'])}",
        f"environment: {yaml_scalar(values['environment'])}",
        f"tool_or_model: {yaml_scalar(values['tool_or_model'])}",
        f"tool_major: {yaml_scalar(values['tool_major'])}",
        f"input_fingerprint: {yaml_scalar(values['input_fingerprint'])}",
        f"source: {yaml_scalar(values['source'])}",
        f"mode: {mode}",
        f"failure_stage: {yaml_scalar(failure_stage)}",
        "verification:",
        f"  command_or_entrypoint: {yaml_scalar(values['verification_command'])}",
        f"  success_criteria: {yaml_scalar(values['success_criteria'])}",
        "  result: passed",
        "occurrences: 1",
        f"first_observed: {yaml_scalar(created)}",
        f"last_verified: {yaml_scalar(today)}",
        "replaces: null",
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
        f"- 环境：{values['environment']}",
        "",
        "## 状态事件",
        f"### {today} | {state} | created",
        f"- status: {state}",
        "- event: created",
        "- 原因：案例由受控渲染器生成。",
        "- 证据：后续状态只能通过 bridge append 追加。",
        f"- 验证时间：{today}",
        f"- scope: {values['scope']}",
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
