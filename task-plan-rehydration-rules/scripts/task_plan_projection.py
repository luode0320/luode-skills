"""维护 PROJECT_CURRENT.md 中的任务投影托管区。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


BEGIN_MARKER = "<!-- BEGIN TASK PLAN PROJECTION -->"
END_MARKER = "<!-- END TASK PLAN PROJECTION -->"
MAX_FILE_BYTES = 51_200
MAX_STEPS = 20
MAX_STEP_CHARS = 256
EXPLANATION = "悬浮任务列表已从 PROJECT_CURRENT 重建；进行中步骤必须先核验中断点"
EXPLANATION_SYNTH_EXACT = "悬浮任务列表已根据当前会话与项目文档正式补建；进行中步骤必须先核验中断点"
EXPLANATION_SYNTH_FALLBACK = "悬浮任务列表已根据当前会话与项目文档生成安全恢复列表；进行中步骤必须先核验中断点"
FALLBACK_PREFIX = "SYNTH-FALLBACK/"
EXACT_PREFIX = "SYNTH-EXACT/"
TOP_LEVEL_FIELDS_V1 = {
    "version",
    "state",
    "plan_key",
    "source_document",
    "plan_fingerprint",
    "updated_at",
    "steps",
}
TOP_LEVEL_FIELDS_V2 = TOP_LEVEL_FIELDS_V1 | {"projection_origin", "synthesis_mode"}
STEP_FIELDS = {"id", "step", "status"}
STEP_STATUSES = {"pending", "in_progress", "completed"}
PROJECTION_ORIGINS = {"persisted", "synthesized"}
SYNTHESIS_MODES = {"none", "exact", "fallback"}
SAFE_FALLBACK_STEPS = (
    ("RECOVERY-01", "[RECOVERY-01] 核对当前任务目标与范围", "in_progress"),
    ("RECOVERY-02", "[RECOVERY-02] 确认中断点与未完成工作", "pending"),
    ("RECOVERY-03", "[RECOVERY-03] 继续当前任务执行", "pending"),
)
SENSITIVE_KEYS = {
    "prompt",
    "response",
    "token",
    "api_key",
    "password",
    "secret",
    "private_key",
    "thread_id",
    "user_input",
    "business_data",
}
BLOCK_PATTERN = re.compile(
    rf"{re.escape(BEGIN_MARKER)}\r?\n```json\r?\n(?P<json>.*?)\r?\n```\r?\n{re.escape(END_MARKER)}",
    re.DOTALL,
)
TASK_LABEL_PATTERN = re.compile(r"(?P<label>\[(?P<id>TASK-[A-Z0-9-]+)\]\s*[^\r\n]+)")
FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(?P<body>.*?)\r?\n---\r?\n?", re.DOTALL)


class ProjectionContractError(ValueError):
    """任务投影违反 schema、标记或安全契约。"""


class ProjectionIOError(OSError):
    """任务投影文件读取或原子写入失败。"""


def compute_plan_fingerprint(steps: Sequence[Mapping[str, Any]]) -> str:
    """根据任务 ID、顺序和文案计算稳定指纹。"""
    if not isinstance(steps, Sequence) or isinstance(steps, (str, bytes, bytearray)):
        raise ProjectionContractError("steps must be an array")
    canonical = []
    for step in steps:
        if not isinstance(step, Mapping):
            raise ProjectionContractError("step must be an object")
        task_id = step.get("id")
        text = step.get("step")
        if not isinstance(task_id, str) or not task_id.strip():
            raise ProjectionContractError("step id must be a non-empty string")
        if not isinstance(text, str) or not text.strip():
            raise ProjectionContractError("step text must be a non-empty string")
        canonical.append({"id": task_id, "step": text})
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _reject_sensitive_keys(value: Any, path: str = "projection") -> None:
    """递归拒绝敏感键。"""
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in SENSITIVE_KEYS:
                raise ProjectionContractError(f"sensitive field is forbidden: {path}.{key}")
            _reject_sensitive_keys(child, f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _reject_sensitive_keys(child, f"{path}[{index}]")


def _validate_utc_timestamp(value: Any) -> None:
    """校验更新时间为带 UTC 时区的 ISO-8601。"""
    if not isinstance(value, str) or not value.strip():
        raise ProjectionContractError("updated_at must be a non-empty UTC ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ProjectionContractError("updated_at must be valid ISO-8601") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ProjectionContractError("updated_at must use UTC timezone")


def _validate_string_field(field_name: str, field_value: Any) -> str:
    """校验投影字符串字段。"""
    if not isinstance(field_value, str):
        raise ProjectionContractError(f"{field_name} must be a string")
    return field_value


def _normalize_steps(steps: Any) -> list[dict[str, str]]:
    """校验步骤数组并返回规范化副本。"""
    if not isinstance(steps, list):
        raise ProjectionContractError("steps must be an array")
    if len(steps) > MAX_STEPS:
        raise ProjectionContractError(f"steps must not exceed {MAX_STEPS}")
    normalized_steps: list[dict[str, str]] = []
    task_ids: set[str] = set()
    in_progress_count = 0
    for index, step in enumerate(steps):
        if not isinstance(step, Mapping) or set(step) != STEP_FIELDS:
            raise ProjectionContractError(f"step[{index}] fields must be exactly {sorted(STEP_FIELDS)}")
        task_id = step.get("id")
        text = step.get("step")
        status = step.get("status")
        if not isinstance(task_id, str) or not task_id.strip():
            raise ProjectionContractError(f"step[{index}].id must be non-empty")
        if task_id in task_ids:
            raise ProjectionContractError(f"duplicate step id: {task_id}")
        if not isinstance(text, str) or not text.strip():
            raise ProjectionContractError(f"step[{index}].step must be non-empty")
        if len(text) > MAX_STEP_CHARS:
            raise ProjectionContractError(f"step[{index}].step exceeds {MAX_STEP_CHARS} characters")
        if status not in STEP_STATUSES:
            raise ProjectionContractError(f"step[{index}].status is invalid")
        task_ids.add(task_id)
        in_progress_count += int(status == "in_progress")
        normalized_steps.append({"id": task_id, "step": text, "status": status})
    if in_progress_count > 1:
        raise ProjectionContractError("at most one step may be in_progress")
    return normalized_steps


def validate_projection(
    value: Any,
    *,
    expected_fingerprint: str | None = None,
    expected_source_document: str | None = None,
) -> dict[str, Any]:
    """校验投影字段、状态、指纹和可选来源预期。"""
    if not isinstance(value, Mapping):
        raise ProjectionContractError("projection root must be an object")
    _reject_sensitive_keys(value)
    version = value.get("version")
    if version == 1:
        expected_fields = TOP_LEVEL_FIELDS_V1
    elif version == 2:
        expected_fields = TOP_LEVEL_FIELDS_V2
    else:
        raise ProjectionContractError("version must be 1 or 2")
    actual_fields = set(value)
    if actual_fields != expected_fields:
        missing = sorted(expected_fields - actual_fields)
        unknown = sorted(actual_fields - expected_fields)
        raise ProjectionContractError(f"projection fields mismatch: missing={missing}, unknown={unknown}")

    state = value.get("state")
    if state not in {"active", "inactive"}:
        raise ProjectionContractError("state must be active or inactive")
    plan_key = _validate_string_field("plan_key", value.get("plan_key"))
    source_document = _validate_string_field("source_document", value.get("source_document"))
    fingerprint = _validate_string_field("plan_fingerprint", value.get("plan_fingerprint"))
    _validate_utc_timestamp(value.get("updated_at"))
    normalized_steps = _normalize_steps(value.get("steps"))

    if version == 1:
        projection_origin = "persisted"
        synthesis_mode = "none"
    else:
        projection_origin = _validate_string_field("projection_origin", value.get("projection_origin"))
        synthesis_mode = _validate_string_field("synthesis_mode", value.get("synthesis_mode"))
        if projection_origin not in PROJECTION_ORIGINS:
            raise ProjectionContractError("projection_origin is invalid")
        if synthesis_mode not in SYNTHESIS_MODES:
            raise ProjectionContractError("synthesis_mode is invalid")
        if projection_origin == "persisted" and synthesis_mode != "none":
            raise ProjectionContractError("persisted projection must use synthesis_mode none")
        if projection_origin == "synthesized" and synthesis_mode == "none":
            raise ProjectionContractError("synthesized projection must use exact or fallback mode")

    if not normalized_steps:
        if state != "inactive" or any((plan_key, source_document, fingerprint)):
            raise ProjectionContractError("empty steps are only allowed for an empty inactive slot")
    else:
        computed = compute_plan_fingerprint(normalized_steps)
        if not re.fullmatch(r"[0-9a-f]{64}", fingerprint) or fingerprint != computed:
            raise ProjectionContractError("plan_fingerprint does not match ordered step ids and text")
        if state == "active" and all(step["status"] == "completed" for step in normalized_steps):
            raise ProjectionContractError("an all-completed projection must be inactive")
        if state == "inactive" and any(step["status"] != "completed" for step in normalized_steps):
            raise ProjectionContractError("inactive projection may only retain completed steps")
        if projection_origin == "persisted":
            if not plan_key.strip() or not source_document.strip():
                raise ProjectionContractError("persisted projection requires plan_key and source_document")
        elif synthesis_mode == "exact":
            if not plan_key.strip():
                raise ProjectionContractError("exact synthesized projection requires plan_key")
            if not source_document.strip():
                raise ProjectionContractError("exact synthesized projection requires source_document")
        else:
            if not plan_key.startswith(FALLBACK_PREFIX):
                raise ProjectionContractError("fallback synthesized projection must use SYNTH-FALLBACK plan_key")
            if source_document:
                raise ProjectionContractError("fallback synthesized projection must not set source_document")

    if expected_fingerprint is not None and fingerprint != expected_fingerprint:
        raise ProjectionContractError("projection fingerprint does not match expected fingerprint")
    if expected_source_document is not None and source_document != expected_source_document:
        raise ProjectionContractError("projection source_document does not match expected source")

    normalized = {
        "version": version,
        "state": state,
        "plan_key": plan_key,
        "source_document": source_document,
        "plan_fingerprint": fingerprint,
        "updated_at": value["updated_at"],
        "steps": normalized_steps,
    }
    if version == 2:
        normalized["projection_origin"] = projection_origin
        normalized["synthesis_mode"] = synthesis_mode
    return normalized


def _validate_markers(document: str) -> tuple[int, int] | None:
    """校验托管标记数量和顺序。"""
    begins = [match.start() for match in re.finditer(re.escape(BEGIN_MARKER), document)]
    ends = [match.start() for match in re.finditer(re.escape(END_MARKER), document)]
    if not begins and not ends:
        return None
    if len(begins) != 1 or len(ends) != 1 or begins[0] >= ends[0]:
        raise ProjectionContractError("task projection markers must form exactly one ordered pair")
    match = BLOCK_PATTERN.search(document)
    if match is None or match.start() != begins[0] or match.end() != ends[0] + len(END_MARKER):
        raise ProjectionContractError("task projection block must contain one exact json fence")
    return match.start(), match.end()


def extract_projection(document: str) -> dict[str, Any] | None:
    """从文档中解析并校验任务投影。"""
    bounds = _validate_markers(document)
    if bounds is None:
        return None
    match = BLOCK_PATTERN.search(document, bounds[0], bounds[1])
    if match is None:
        raise ProjectionContractError("task projection block is malformed")
    try:
        value = json.loads(match.group("json"))
    except json.JSONDecodeError as error:
        raise ProjectionContractError(f"task projection JSON is invalid: {error.msg}") from error
    return validate_projection(value)


def load_projection(
    path: str | os.PathLike[str],
    *,
    expected_fingerprint: str | None = None,
    expected_source_document: str | None = None,
) -> dict[str, Any]:
    """从严格 UTF-8 文件读取并校验任务投影。"""
    target = Path(path)
    try:
        document = target.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
    projection = extract_projection(document)
    if projection is None:
        raise ProjectionContractError("task projection block is missing")
    return validate_projection(
        projection,
        expected_fingerprint=expected_fingerprint,
        expected_source_document=expected_source_document,
    )


def _to_version_two_projection(projection: Mapping[str, Any]) -> dict[str, Any]:
    """把 version:1 兼容投影升级为 version:2。"""
    normalized = validate_projection(projection)
    if normalized["version"] == 2:
        return dict(normalized)
    upgraded = dict(normalized)
    upgraded["version"] = 2
    upgraded["projection_origin"] = "persisted"
    upgraded["synthesis_mode"] = "none"
    return validate_projection(upgraded)


def render_projection_block(projection: Mapping[str, Any], newline: str = "\n") -> str:
    """把合法投影渲染为唯一托管区块。"""
    normalized = _to_version_two_projection(projection)
    encoded = json.dumps(normalized, ensure_ascii=False, indent=2)
    encoded = encoded.replace("\n", newline)
    return newline.join((BEGIN_MARKER, "```json", encoded, "```", END_MARKER))


def _write_text_atomic(path: Path, document: str) -> None:
    """在同目录完整写入并原子替换目标文件。"""
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temp_name = stream.name
            stream.write(document)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
        temp_name = None
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except OSError:
            pass
    except OSError as error:
        raise ProjectionIOError(f"unable to atomically write PROJECT_CURRENT: {path}") from error
    finally:
        if temp_name:
            try:
                os.unlink(temp_name)
            except OSError:
                pass


def upsert_projection(path: str | os.PathLike[str], projection: Mapping[str, Any]) -> dict[str, Any]:
    """新增或替换唯一任务投影区块，并保护非托管正文。"""
    target = Path(path)
    try:
        original_bytes = target.read_bytes()
        document = original_bytes.decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error

    normalized = _to_version_two_projection(projection)
    bounds = _validate_markers(document)
    newline = "\r\n" if "\r\n" in document else "\n"
    block = render_projection_block(normalized, newline)
    if bounds is None:
        separator = "" if not document or document.endswith(("\n", "\r")) else newline
        candidate = document + separator + block + newline
    else:
        candidate = document[: bounds[0]] + block + document[bounds[1] :]
    if len(candidate.encode("utf-8")) > MAX_FILE_BYTES:
        raise ProjectionContractError(f"PROJECT_CURRENT exceeds {MAX_FILE_BYTES} UTF-8 bytes")
    _write_text_atomic(target, candidate)
    return normalized


def deactivate_projection(
    path: str | os.PathLike[str],
    *,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """将现有活动投影失活，保留完成步骤作为恢复证据。"""
    projection = load_projection(path)
    projection["steps"] = [
        {"id": step["id"], "step": step["step"], "status": "completed"}
        for step in projection["steps"]
    ]
    projection["state"] = "inactive"
    projection["updated_at"] = updated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return upsert_projection(path, projection)


def _payload_explanation(projection: Mapping[str, Any]) -> str:
    """根据投影来源生成 explanation。"""
    normalized = _to_version_two_projection(projection)
    origin = normalized["projection_origin"]
    mode = normalized["synthesis_mode"]
    if origin == "synthesized" and mode == "exact":
        return EXPLANATION_SYNTH_EXACT
    if origin == "synthesized" and mode == "fallback":
        return EXPLANATION_SYNTH_FALLBACK
    return EXPLANATION


def build_update_plan_payload(projection: Mapping[str, Any]) -> dict[str, Any]:
    """生成可直接传给 update_plan 的参数对象。"""
    normalized = validate_projection(projection)
    if normalized["state"] != "active":
        raise ProjectionContractError("inactive projection cannot build update_plan payload")
    return {
        "explanation": _payload_explanation(normalized),
        "plan": [{"step": step["step"], "status": step["status"]} for step in normalized["steps"]],
    }


def _read_json_input(source: str) -> Any:
    """从文件或标准输入读取 JSON。"""
    try:
        text = sys.stdin.read() if source == "-" else Path(source).read_text(encoding="utf-8")
        return json.loads(text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProjectionIOError(f"unable to read JSON input: {source}") from error


def _print_json(value: Any, stream: Any = sys.stdout) -> None:
    """以统一 UTF-8 JSON 格式输出命令结果。"""
    stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


def _compact_utc_now() -> str:
    """生成 UTC 紧凑时间串。"""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _read_utf8_text(path: Path, *, label: str) -> str:
    """读取严格 UTF-8 文本。"""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ProjectionIOError(f"unable to read {label}: {path}") from error


def _extract_frontmatter_fields(document: str) -> dict[str, str]:
    """提取 Markdown frontmatter 字段。"""
    match = FRONTMATTER_PATTERN.match(document.lstrip("\ufeff"))
    if match is None:
        return {}
    fields: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def _extract_markdown_section(document: str, heading_text: str) -> str:
    """按二级标题提取 Markdown 小节正文。"""
    pattern = re.compile(rf"^##\\s+.*{re.escape(heading_text)}.*\\n(?P<body>.*?)(?=^##\\s+|\\Z)", re.M | re.S)
    match = pattern.search(document)
    return match.group("body") if match else ""


def _parse_markdown_table(section_text: str) -> list[list[str]]:
    """解析 Markdown 表格的有效数据行。"""
    rows: list[list[str]] = []
    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) < 2:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        rows.append(cells)
    return rows
def _extract_task_steps_from_document(path: Path) -> list[dict[str, str]]:
    """从正式实施文档中提取唯一 TASK 步骤。"""
    document = _read_utf8_text(path, label="source document")
    task_section = _extract_markdown_section(document, "最小任务清单")
    steps: list[dict[str, str]] = []
    seen: set[str] = set()
    if task_section:
        for cells in _parse_markdown_table(task_section):
            header = cells[0]
            goal = cells[1] if len(cells) > 1 else ""
            match = re.fullmatch(r"`(?P<id>TASK-[A-Z0-9-]+)`", header)
            if match is None:
                continue
            task_id = match.group("id")
            if task_id in seen:
                continue
            if not goal.strip():
                raise ProjectionContractError(f"source document task goal is empty: {task_id}")
            seen.add(task_id)
            steps.append({"id": task_id, "step": f"[{task_id}] {goal.strip()}", "status": "pending"})
    else:
        for match in TASK_LABEL_PATTERN.finditer(document):
            task_id = match.group("id")
            label = match.group("label").strip()
            if task_id in seen:
                continue
            seen.add(task_id)
            steps.append({"id": task_id, "step": label, "status": "pending"})
    if not steps:
        raise ProjectionContractError("source document does not contain any task definitions")
    return steps


def _normalize_context(context: Any) -> dict[str, Any]:
    """校验 synthesize 输入上下文的必要结构。"""
    if not isinstance(context, Mapping):
        raise ProjectionContractError("synthesis context must be an object")
    trigger = context.get("trigger")
    current_message = context.get("current_message")
    project_current_summary = context.get("project_current_summary")
    thread_evidence = context.get("thread_evidence")
    candidate_source_documents = context.get("candidate_source_documents")
    if trigger != "continue":
        raise ProjectionContractError("synthesis trigger must be continue")
    if not isinstance(current_message, str) or not current_message.strip():
        raise ProjectionContractError("current_message must be a non-empty string")
    if not isinstance(project_current_summary, Mapping):
        raise ProjectionContractError("project_current_summary must be an object")
    if not isinstance(thread_evidence, Mapping):
        raise ProjectionContractError("thread_evidence must be an object")
    if not isinstance(candidate_source_documents, list):
        raise ProjectionContractError("candidate_source_documents must be an array")
    for key in ("goal", "current_scope", "next_execution_point", "source_document_hint"):
        if key not in project_current_summary:
            raise ProjectionContractError(f"project_current_summary missing field: {key}")
        if not isinstance(project_current_summary.get(key), str):
            raise ProjectionContractError(f"project_current_summary.{key} must be a string")
    recent_task_labels = thread_evidence.get("recent_task_labels", [])
    completed_step_hints = thread_evidence.get("completed_step_hints", [])
    current_step_hint = thread_evidence.get("current_step_hint")
    for field_name, field_value in (
        ("recent_task_labels", recent_task_labels),
        ("completed_step_hints", completed_step_hints),
    ):
        if not isinstance(field_value, list) or any(not isinstance(item, str) for item in field_value):
            raise ProjectionContractError(f"thread_evidence.{field_name} must be a string array")
    if current_step_hint is not None and not isinstance(current_step_hint, str):
        raise ProjectionContractError("thread_evidence.current_step_hint must be a string or null")
    normalized_candidates = []
    for candidate in candidate_source_documents:
        if not isinstance(candidate, str) or not candidate.strip():
            raise ProjectionContractError("candidate_source_documents must contain non-empty strings")
        if candidate not in normalized_candidates:
            normalized_candidates.append(candidate)
    return {
        "trigger": trigger,
        "current_message": current_message,
        "project_current_summary": dict(project_current_summary),
        "thread_evidence": {
            "recent_task_labels": recent_task_labels,
            "completed_step_hints": completed_step_hints,
            "current_step_hint": current_step_hint,
        },
        "candidate_source_documents": normalized_candidates,
    }


def _build_exact_projection(
    project_current_path: Path,
    source_document: str,
    context: Mapping[str, Any],
) -> dict[str, Any]:
    """根据唯一正式计划源生成 exact 补建投影。"""
    source_path = project_current_path.parent / source_document
    steps = _extract_task_steps_from_document(source_path)
    source_document_text = _read_utf8_text(source_path, label="source document")
    frontmatter = _extract_frontmatter_fields(source_document_text)
    completed_ids = set(context["thread_evidence"]["completed_step_hints"])
    current_step_hint = context["thread_evidence"]["current_step_hint"]
    if not (completed_ids or current_step_hint):
        raise ProjectionContractError("exact synthesis requires explicit step hints")
    step_ids = {step["id"] for step in steps}
    recent_task_ids = {
        label.strip()
        for label in context["thread_evidence"]["recent_task_labels"]
        if label.strip().startswith("TASK-")
    }
    if not completed_ids <= step_ids:
        raise ProjectionContractError("completed step hints conflict with source document tasks")
    if current_step_hint and current_step_hint not in step_ids:
        raise ProjectionContractError("current_step_hint conflicts with source document tasks")
    if current_step_hint and current_step_hint in completed_ids:
        raise ProjectionContractError("current_step_hint must not also be completed")
    if not recent_task_ids <= step_ids:
        raise ProjectionContractError("recent task labels conflict with source document tasks")
    unfinished_index: int | None = None
    for index, step in enumerate(steps):
        if step["id"] in completed_ids:
            step["status"] = "completed"
        elif current_step_hint and step["id"] == current_step_hint:
            step["status"] = "in_progress"
        else:
            step["status"] = "pending"
            if unfinished_index is None:
                unfinished_index = index
    if current_step_hint is None and unfinished_index is not None:
        steps[unfinished_index]["status"] = "in_progress"
    if all(step["status"] == "completed" for step in steps):
        raise ProjectionContractError("exact synthesis requires at least one unfinished step")
    updated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return validate_projection(
        {
            "version": 2,
            "projection_origin": "synthesized",
            "synthesis_mode": "exact",
            "state": "active",
            "plan_key": frontmatter.get("doc_id") or f"{EXACT_PREFIX}{Path(source_document).stem}",
            "source_document": source_document,
            "plan_fingerprint": compute_plan_fingerprint(steps),
            "updated_at": updated_at,
            "steps": steps,
        }
    )


def _build_fallback_projection() -> dict[str, Any]:
    """生成固定三步安全恢复列表。"""
    steps = [{"id": item[0], "step": item[1], "status": item[2]} for item in SAFE_FALLBACK_STEPS]
    updated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return validate_projection(
        {
            "version": 2,
            "projection_origin": "synthesized",
            "synthesis_mode": "fallback",
            "state": "active",
            "plan_key": f"{FALLBACK_PREFIX}{_compact_utc_now()}",
            "source_document": "",
            "plan_fingerprint": compute_plan_fingerprint(steps),
            "updated_at": updated_at,
            "steps": steps,
        }
    )


def synthesize_projection(path: str | os.PathLike[str], context: Any) -> dict[str, Any]:
    """根据当前会话与项目文档生成 exact 或 fallback 补建结果。"""
    project_current_path = Path(path)
    _read_utf8_text(project_current_path, label="UTF-8 PROJECT_CURRENT")
    normalized_context = _normalize_context(context)
    summary = normalized_context["project_current_summary"]
    thread_evidence = normalized_context["thread_evidence"]
    candidates = normalized_context["candidate_source_documents"]
    source_document_hint = summary["source_document_hint"].strip()
    unique_source = len(candidates) == 1
    explicit_hints = bool(thread_evidence["completed_step_hints"] or thread_evidence["current_step_hint"])
    exact_candidate = unique_source and bool(source_document_hint) and explicit_hints
    if exact_candidate:
        candidate = candidates[0].replace("\\", "/")
        hint = source_document_hint.replace("\\", "/")
        exact_candidate = candidate == hint

    try:
        if not exact_candidate:
            raise ProjectionContractError("fallback requested")
        projection = _build_exact_projection(project_current_path, candidates[0], normalized_context)
        mode = "exact"
        identity_confidence = "high"
        status_confidence = "explicit" if thread_evidence["current_step_hint"] else "conservative"
        used_sources = ["project_current", "thread_history", "source_document"]
    except ProjectionContractError:
        projection = _build_fallback_projection()
        mode = "fallback"
        identity_confidence = "low"
        status_confidence = "conservative"
        used_sources = ["project_current", "thread_history"] + (["source_document"] if exact_candidate else [])
    return {
        "mode": mode,
        "projection": projection,
        "payload": build_update_plan_payload(projection),
        "evidence": {
            "identity_confidence": identity_confidence,
            "status_confidence": status_confidence,
            "used_sources": used_sources,
        },
    }


def main() -> None:
    """解析 CLI 子命令并返回稳定退出码。"""
    parser = argparse.ArgumentParser(description="Maintain PROJECT_CURRENT task plan projection")
    subparsers = parser.add_subparsers(dest="command", required=True)
    fingerprint_parser = subparsers.add_parser("fingerprint")
    fingerprint_parser.add_argument("--input", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--project-current", required=True)
    write_parser = subparsers.add_parser("write")
    write_parser.add_argument("--project-current", required=True)
    write_parser.add_argument("--input", required=True)
    payload_parser = subparsers.add_parser("payload")
    payload_parser.add_argument("--project-current", required=True)
    synthesize_parser = subparsers.add_parser("synthesize")
    synthesize_parser.add_argument("--project-current", required=True)
    synthesize_parser.add_argument("--input", required=True)
    deactivate_parser = subparsers.add_parser("deactivate")
    deactivate_parser.add_argument("--project-current", required=True)
    deactivate_parser.add_argument("--updated-at")
    for current in (validate_parser, payload_parser):
        current.add_argument("--expected-fingerprint")
        current.add_argument("--expected-source-document")
    args = parser.parse_args()

    try:
        if args.command == "fingerprint":
            value = _read_json_input(args.input)
            steps = value.get("steps") if isinstance(value, Mapping) else value
            _print_json({"plan_fingerprint": compute_plan_fingerprint(steps)})
        elif args.command == "validate":
            projection = load_projection(
                args.project_current,
                expected_fingerprint=args.expected_fingerprint,
                expected_source_document=args.expected_source_document,
            )
            _print_json({"ok": True, "projection": projection})
        elif args.command == "write":
            projection = upsert_projection(args.project_current, _read_json_input(args.input))
            _print_json({"ok": True, "projection": projection})
        elif args.command == "payload":
            projection = load_projection(
                args.project_current,
                expected_fingerprint=args.expected_fingerprint,
                expected_source_document=args.expected_source_document,
            )
            _print_json(build_update_plan_payload(projection))
        elif args.command == "synthesize":
            _print_json(synthesize_projection(args.project_current, _read_json_input(args.input)))
        else:
            projection = deactivate_projection(args.project_current, updated_at=args.updated_at)
            _print_json({"ok": True, "projection": projection})
    except ProjectionContractError as error:
        _print_json({"error": "contract", "message": str(error)}, sys.stderr)
        raise SystemExit(2) from error
    except ProjectionIOError as error:
        _print_json({"error": "io", "message": str(error)}, sys.stderr)
        raise SystemExit(3) from error


if __name__ == "__main__":
    main()
