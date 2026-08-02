"""维护 PROJECT_CURRENT.md 中的任务投影托管区。"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


BEGIN_MARKER = "<!-- BEGIN TASK PLAN PROJECTION -->"
END_MARKER = "<!-- END TASK PLAN PROJECTION -->"
MAX_FILE_BYTES = 51_200
MAX_STEPS = 20
MAX_STEP_CHARS = 256
MAX_PROJECTIONS = 64
REGISTRY_VERSION = 4
REGISTRY_SCHEMA = "task_plan_projection_registry"
LEGACY_SESSION_ID = "legacy/default"
LOCK_RETRIES = 40
LOCK_WAIT_SECONDS = 0.05
TIMEOUT_SECONDS = 600.0
INACTIVE_PROJECTION_RETENTION_SECONDS = 604_800
SESSION_ENV_NAME = "CODEX_THREAD_ID"
EXPLANATION = "悬浮任务列表已从 PROJECT_CURRENT 重建；进行中步骤必须先核验中断点"
EXPLANATION_SYNTH_EXACT = "悬浮任务列表已根据当前会话与项目文档正式补建；进行中步骤必须先核验中断点"
EXPLANATION_SYNTH_FALLBACK = "悬浮任务列表已根据当前会话与项目文档生成安全恢复列表；进行中步骤必须先核验中断点"
EXPLANATION_GOAL_ACTIVE = "Goal 任务进度已恢复；进行中步骤必须先核验中断点"
EXPLANATION_GOAL_BLOCKED = "Goal 当前已阻断；任务列表仅用于观察进度，不恢复执行授权"
EXPLANATION_COMPLETED = "任务已完成；悬浮任务列表已完成收口"
FALLBACK_PREFIX = "SYNTH-FALLBACK/"
EXACT_PREFIX = "SYNTH-EXACT/"
GOAL_PLAN_KEY = "GOAL/ACTIVE"
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
TOP_LEVEL_FIELDS_V3 = TOP_LEVEL_FIELDS_V2
REGISTRY_FIELDS = {"version", "registry_schema", "registry_updated_at", "projections"}
PROJECTION_ENTRY_FIELDS = (TOP_LEVEL_FIELDS_V3 - {"version"}) | {"projection_id", "session_id"}
STEP_FIELDS = {"id", "step", "status"}
STEP_STATUSES = {"pending", "in_progress", "completed"}
PROJECTION_STATES = {"active", "blocked", "inactive"}
PROJECTION_ORIGINS = {"persisted", "synthesized", "goal"}
SYNTHESIS_MODES = {"none", "exact", "fallback", "goal_default", "goal_blocked"}
SAFE_FALLBACK_STEPS = (
    ("RECOVERY-01", "[RECOVERY-01] 核对当前任务目标与范围", "in_progress"),
    ("RECOVERY-02", "[RECOVERY-02] 确认中断点与未完成工作", "pending"),
    ("RECOVERY-03", "[RECOVERY-03] 继续当前任务执行", "pending"),
)
GOAL_DEFAULT_STEPS = (
    ("GOAL-01", "[GOAL-01] 确认当前闭环", "in_progress"),
    ("GOAL-02", "[GOAL-02] 执行并更新进度", "pending"),
    ("GOAL-03", "[GOAL-03] 验证并完成 Goal", "pending"),
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
    "objective",
    "goal_objective",
    "goal_id",
    "goal_prompt",
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


def _validate_session_id(value: Any) -> str:
    """校验受控会话标识，拒绝空值、换行和过长输入。

    [参数] value: 宿主提供的原始会话标识。
    [返回] str：可持久化到受控字段的会话标识。
    最近修改时间：2026-07-25 00:00:00；改动原因：为多会话注册表建立唯一归属边界。
    """
    if not isinstance(value, str) or not value.strip():
        raise ProjectionContractError("session_id must be a non-empty string")
    if len(value) > 256 or any(char in value for char in "\r\n"):
        raise ProjectionContractError("session_id is invalid")
    return value


def _require_session_id(value: Any) -> str:
    """解析状态入口会话归属，显式值优先并支持宿主环境回退。

    [参数] value: 待检查的会话标识。
    [返回] str：通过格式校验的会话标识。
    最近修改时间：2026-07-26 00:00:00；改动原因：支持宿主会话回退并拒绝显式值与环境值冲突。
    """
    # 1. 显式参数与宿主环境同时存在时必须一致，避免错写其它会话。
    return resolve_session_id(value)


def resolve_session_id(
    value: Any = None,
    *,
    environ: Mapping[str, str] | None = None,
    required: bool = True,
) -> str | None:
    """解析当前会话标识，冲突或缺失时失败关闭。

    [参数] value: 可选显式会话标识；environ: 可选环境映射；required: 是否要求最终存在标识。
    [返回] str | None：显式参数或 `CODEX_THREAD_ID` 的受控值。
    最近修改时间：2026-07-26 00:00:00；改动原因：让宿主会话自动绑定任务投影并拒绝身份冲突。
    """
    # 1. 显式值先校验；环境变量存在时也校验，禁止空值或非法内容绕过安全边界。
    explicit = _validate_session_id(value) if value is not None else None
    source = os.environ if environ is None else environ
    env_present = SESSION_ENV_NAME in source
    env_value = _validate_session_id(source.get(SESSION_ENV_NAME)) if env_present else None
    # 2. 两个来源同时存在但不一致时立即停止，不猜测归属。
    if explicit is not None and env_value is not None and explicit != env_value:
        raise ProjectionContractError("session_id conflicts with CODEX_THREAD_ID")
    if explicit is not None:
        return explicit
    if env_value is not None:
        return env_value
    if required:
        raise ProjectionContractError(
            "session_id is required; pass --session-id or set CODEX_THREAD_ID"
        )
    return None


def compute_projection_id(session_id: str, projection: Mapping[str, Any]) -> str:
    """根据会话和计划身份生成稳定投影 ID。

    [参数] session_id: 原始会话标识；projection: 合法任务投影。
    [返回] str：不暴露业务步骤内容的稳定投影 ID。
    最近修改时间：2026-07-25 00:00:00；改动原因：为每个会话当前投影提供可校验身份。
    """
    # 1. 先规范化会话和兼容版本，避免旧格式直接参与身份计算。
    sid = _validate_session_id(session_id)
    normalized = _to_version_three_projection(projection)
    # 2. 只使用会话与计划身份字段计算摘要，状态迁移不改变同一计划的 ID。
    identity = json.dumps(
        {
            "session_id": sid,
            "plan_key": normalized["plan_key"],
            "source_document": normalized["source_document"],
            "projection_origin": normalized["projection_origin"],
            "synthesis_mode": normalized["synthesis_mode"],
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"SESSION/{hashlib.sha256(identity).hexdigest()}"


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


def _parse_utc_timestamp(field_name: str, value: Any) -> datetime:
    """解析带 UTC 时区的 ISO-8601 时间。

    [参数] field_name: 错误信息中的字段名；value: 待解析时间。
    [返回] datetime：规范化前、带 UTC 时区的时间对象。
    最近修改时间：2026-07-25 00:00:00；改动原因：复用超时起止时间与投影更新时间的 UTC 校验。
    """
    # 1. 先拒绝空值和非法 ISO-8601，避免时间差计算接受隐式本地时间。
    if not isinstance(value, str) or not value.strip():
        raise ProjectionContractError(f"{field_name} must be a non-empty UTC ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ProjectionContractError(f"{field_name} must be valid ISO-8601") from error
    # 2. 只接受显式 UTC，禁止把本地时间或其它时区静默换算为执行计时起点。
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ProjectionContractError(f"{field_name} must use UTC timezone")
    return parsed


def _validate_utc_timestamp(value: Any) -> None:
    """校验更新时间为带 UTC 时区的 ISO-8601。

    [参数] value: 待校验更新时间。
    [返回] None。
    最近修改时间：2026-07-25 00:00:00；改动原因：统一复用 UTC 时间解析入口并保持既有错误模型。
    """
    # 1. 更新时间只需要校验，解析结果由调用方按原契约忽略。
    _parse_utc_timestamp("updated_at", value)


def _validate_paused_seconds(value: Any) -> float:
    """校验并规范化暂停秒数。

    [参数] value: CLI 或 Python API 传入的暂停秒数。
    [返回] float：有限且非负的暂停秒数。
    最近修改时间：2026-07-25 00:00:00；改动原因：从墙钟耗时中扣除 Plan Mode、等待用户、blocked 和 manual_handoff 暂停。
    """
    # 1. bool 虽是 int 子类，但不属于合法秒数；其它输入统一尝试转为浮点数。
    if isinstance(value, bool):
        raise ProjectionContractError("paused_seconds must be a non-negative finite number")
    try:
        paused_seconds = float(value)
    except (TypeError, ValueError) as error:
        raise ProjectionContractError("paused_seconds must be a non-negative finite number") from error
    # 2. 拒绝负数、NaN 和无穷值，确保边界比较稳定可复验。
    if not math.isfinite(paused_seconds) or paused_seconds < 0:
        raise ProjectionContractError("paused_seconds must be a non-negative finite number")
    return paused_seconds


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
    """校验投影字段、状态、指纹和可选来源预期。

    [参数] value: 待校验投影；expected_fingerprint: 可选预期指纹；expected_source_document: 可选预期来源。
    [返回] dict：字段已标准化且符合版本契约的投影。
    最近修改时间：2026-07-25 00:00:00；改动原因：新增 Goal v3 身份、阻断与终态契约。
    """
    # 1. 先拒绝非对象和敏感字段，避免任何 Goal 原文进入后续状态计算。
    if not isinstance(value, Mapping):
        raise ProjectionContractError("projection root must be an object")
    _reject_sensitive_keys(value)
    version = value.get("version")
    if version == 1:
        expected_fields = TOP_LEVEL_FIELDS_V1
    elif version == 2:
        expected_fields = TOP_LEVEL_FIELDS_V2
    elif version == 3:
        expected_fields = TOP_LEVEL_FIELDS_V3
    else:
        raise ProjectionContractError("version must be 1, 2 or 3")
    actual_fields = set(value)
    if actual_fields != expected_fields:
        missing = sorted(expected_fields - actual_fields)
        unknown = sorted(actual_fields - expected_fields)
        raise ProjectionContractError(f"projection fields mismatch: missing={missing}, unknown={unknown}")

    # 2. 再按版本确定允许字段与状态边界，保留 v1/v2 读取兼容性。
    state = value.get("state")
    if state not in PROJECTION_STATES or (version < 3 and state == "blocked"):
        raise ProjectionContractError("projection state is invalid")
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
        if version == 2 and (projection_origin == "goal" or synthesis_mode.startswith("goal_")):
            raise ProjectionContractError("version 2 does not support Goal projection semantics")
        # 3. 来源与合成模式必须一一对应，Goal 专属模式不得泄漏到常规投影。
        if projection_origin == "persisted" and synthesis_mode != "none":
            raise ProjectionContractError("persisted projection must use synthesis_mode none")
        if projection_origin == "synthesized" and synthesis_mode == "none":
            raise ProjectionContractError("synthesized projection must use exact or fallback mode")
        if projection_origin != "goal" and synthesis_mode.startswith("goal_"):
            raise ProjectionContractError("only Goal projection may use Goal synthesis modes")

    if not normalized_steps:
        if state != "inactive" or any((plan_key, source_document, fingerprint)):
            raise ProjectionContractError("empty steps are only allowed for an empty inactive slot")
    else:
        computed = compute_plan_fingerprint(normalized_steps)
        if not re.fullmatch(r"[0-9a-f]{64}", fingerprint) or fingerprint != computed:
            raise ProjectionContractError("plan_fingerprint does not match ordered step ids and text")
        # 4. Goal 只能使用固定安全三步和受限状态组合，禁止带入目标原文或自定义步骤。
        if projection_origin == "goal":
            expected_goal_steps = [(item[0], item[1]) for item in GOAL_DEFAULT_STEPS]
            actual_goal_steps = [(step["id"], step["step"]) for step in normalized_steps]
            if version != 3 or plan_key != GOAL_PLAN_KEY or source_document:
                raise ProjectionContractError("Goal projection must use fixed v3 identity fields")
            if actual_goal_steps != expected_goal_steps:
                raise ProjectionContractError("Goal projection steps must use the fixed safe default list")
            if state == "active" and synthesis_mode == "goal_default":
                if all(step["status"] == "completed" for step in normalized_steps):
                    raise ProjectionContractError("an all-completed Goal projection must be inactive")
            elif state == "blocked" and synthesis_mode == "goal_blocked":
                if any(step["status"] == "in_progress" for step in normalized_steps):
                    raise ProjectionContractError("blocked Goal projection must not have an in_progress step")
                if all(step["status"] == "completed" for step in normalized_steps):
                    raise ProjectionContractError("an all-completed Goal projection must be inactive")
            elif state == "inactive" and synthesis_mode == "goal_default":
                if any(step["status"] != "completed" for step in normalized_steps):
                    raise ProjectionContractError("inactive Goal projection may only retain completed steps")
            else:
                raise ProjectionContractError("Goal projection state and synthesis_mode combination is invalid")
        else:
            if state == "active" and all(step["status"] == "completed" for step in normalized_steps):
                raise ProjectionContractError("an all-completed projection must be inactive")
            if state == "inactive" and any(step["status"] != "completed" for step in normalized_steps):
                raise ProjectionContractError("inactive projection may only retain completed steps")
            if state == "blocked":
                raise ProjectionContractError("only Goal projection may use blocked state")
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

    # 5. 最后校验调用方提供的身份预期，避免错源恢复到当前会话。
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
    if version >= 2:
        normalized["projection_origin"] = projection_origin
        normalized["synthesis_mode"] = synthesis_mode
    return normalized


def _projection_entry_from_projection(projection: Mapping[str, Any], session_id: str) -> dict[str, Any]:
    """把 v3 投影包装为带会话归属的 registry entry。

    [参数] projection: v1-v3 投影；session_id: 原始会话标识。
    [返回] dict：符合 v4 registry 的会话投影条目。
    最近修改时间：2026-07-25 00:00:00；改动原因：统一旧投影与多会话条目之间的转换。
    """
    # 1. 先统一旧版本字段，再由会话和计划身份生成稳定 projection_id。
    sid = _validate_session_id(session_id)
    normalized = _to_version_three_projection(projection)
    # 2. 只复制契约允许的投影字段，避免把原始输入扩散到注册表。
    return {
        "projection_id": compute_projection_id(sid, normalized),
        "session_id": sid,
        "projection_origin": normalized["projection_origin"],
        "synthesis_mode": normalized["synthesis_mode"],
        "state": normalized["state"],
        "plan_key": normalized["plan_key"],
        "source_document": normalized["source_document"],
        "plan_fingerprint": normalized["plan_fingerprint"],
        "updated_at": normalized["updated_at"],
        "steps": normalized["steps"],
    }


def _projection_from_entry(entry: Mapping[str, Any]) -> dict[str, Any]:
    """从 registry entry 还原既有 v3 投影接口。

    [参数] entry: 已通过外层结构检查的 registry 条目。
    [返回] dict：兼容既有 payload 和 Goal 逻辑的 v3 投影。
    最近修改时间：2026-07-25 00:00:00；改动原因：减少 v4 改造对既有业务校验的侵入。
    """
    # 1. 将 registry entry 映射回旧版业务投影，再复用既有校验逻辑。
    return validate_projection(
        {
            "version": 3,
            "projection_origin": entry["projection_origin"],
            "synthesis_mode": entry["synthesis_mode"],
            "state": entry["state"],
            "plan_key": entry["plan_key"],
            "source_document": entry["source_document"],
            "plan_fingerprint": entry["plan_fingerprint"],
            "updated_at": entry["updated_at"],
            "steps": entry["steps"],
        }
    )


def validate_projection_entry(value: Any) -> dict[str, Any]:
    """校验 registry 中的单个会话投影条目。

    [参数] value: 待校验的会话投影条目。
    [返回] dict：字段、身份和内部投影均规范化的条目。
    最近修改时间：2026-07-25 00:00:00；改动原因：防止会话归属和计划身份不一致。
    """
    # 1. 先锁定条目字段白名单，再复用 v3 投影契约校验业务状态。
    if not isinstance(value, Mapping) or set(value) != PROJECTION_ENTRY_FIELDS:
        raise ProjectionContractError(
            f"projection entry fields must be exactly {sorted(PROJECTION_ENTRY_FIELDS)}"
        )
    session_id = _validate_session_id(value.get("session_id"))
    projection = _projection_from_entry(value)
    projection_id = _validate_string_field("projection_id", value.get("projection_id"))
    # 2. 最后复算投影身份，拒绝调用方伪造 projection_id。
    expected_projection_id = compute_projection_id(session_id, projection)
    if projection_id != expected_projection_id:
        raise ProjectionContractError("projection_id does not match session and plan identity")
    normalized = _projection_entry_from_projection(projection, session_id)
    normalized["projection_id"] = projection_id
    return normalized


def validate_registry(value: Any) -> dict[str, Any]:
    """校验 v4 多会话任务投影注册表。

    [参数] value: 待校验的注册表对象。
    [返回] dict：字段顺序稳定且全部条目已规范化的 v4 注册表。
    最近修改时间：2026-07-25 00:00:00；改动原因：建立单文件多会话状态总契约。
    """
    # 1. 校验顶层 schema、版本和时间，避免旧单投影被误解释为注册表。
    if not isinstance(value, Mapping) or set(value) != REGISTRY_FIELDS:
        actual = set(value) if isinstance(value, Mapping) else set()
        raise ProjectionContractError(
            f"registry fields mismatch: missing={sorted(REGISTRY_FIELDS - actual)}, "
            f"unknown={sorted(actual - REGISTRY_FIELDS)}"
        )
    if value.get("version") != REGISTRY_VERSION:
        raise ProjectionContractError("registry version must be 4")
    if value.get("registry_schema") != REGISTRY_SCHEMA:
        raise ProjectionContractError("registry_schema is invalid")
    _validate_utc_timestamp(value.get("registry_updated_at"))
    projections = value.get("projections")
    if not isinstance(projections, list) or len(projections) > MAX_PROJECTIONS:
        raise ProjectionContractError(f"projections must be an array of at most {MAX_PROJECTIONS} entries")
    # 2. 逐条校验会话投影，并保证 projection_id 与 session_id 都不重复。
    normalized_entries = []
    projection_ids: set[str] = set()
    session_ids: set[str] = set()
    for index, entry in enumerate(projections):
        try:
            normalized = validate_projection_entry(entry)
        except ProjectionContractError as error:
            raise ProjectionContractError(f"projections[{index}] is invalid: {error}") from error
        if normalized["projection_id"] in projection_ids:
            raise ProjectionContractError(f"duplicate projection_id: {normalized['projection_id']}")
        if normalized["session_id"] in session_ids:
            raise ProjectionContractError(f"duplicate session_id: {normalized['session_id']}")
        projection_ids.add(normalized["projection_id"])
        session_ids.add(normalized["session_id"])
        normalized_entries.append(normalized)
    return {
        "version": REGISTRY_VERSION,
        "registry_schema": REGISTRY_SCHEMA,
        "registry_updated_at": value["registry_updated_at"],
        "projections": normalized_entries,
    }


def _new_registry(projections: Sequence[Mapping[str, Any]] = ()) -> dict[str, Any]:
    """创建合法的空或带条目的 v4 注册表。

    [参数] projections: 可选初始会话投影条目序列。
    [返回] dict：带 UTC 更新时间的合法 v4 注册表。
    最近修改时间：2026-07-25 00:00:00；改动原因：统一 bootstrap、迁移和首次写入的构造路径。
    """
    # 1. 复制条目后统一生成 registry 元数据，并通过顶层契约校验。
    entries = [dict(item) for item in projections]
    return validate_registry(
        {
            "version": REGISTRY_VERSION,
            "registry_schema": REGISTRY_SCHEMA,
            "registry_updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "projections": entries,
        }
    )


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


def _extract_raw_projection_value(document: str) -> Any | None:
    """从唯一托管区读取未经业务解释的 JSON 值。

    [参数] document: PROJECT_CURRENT.md 全文。
    [返回] Any | None：托管区 JSON 值；无托管区时返回 None。
    最近修改时间：2026-07-25 00:00:00；改动原因：在同一读取入口区分旧投影和 v4 registry。
    """
    # 1. 先校验唯一 marker，再严格解析 JSON，避免读取损坏托管区。
    bounds = _validate_markers(document)
    if bounds is None:
        return None
    match = BLOCK_PATTERN.search(document, bounds[0], bounds[1])
    if match is None:
        raise ProjectionContractError("task projection block is malformed")
    try:
        return json.loads(match.group("json"))
    except json.JSONDecodeError as error:
        raise ProjectionContractError(f"task projection JSON is invalid: {error.msg}") from error


def extract_projection(document: str) -> dict[str, Any] | None:
    """从旧版单投影托管区解析并校验 v1-v3 投影。

    [参数] document: PROJECT_CURRENT.md 全文。
    [返回] dict | None：合法旧投影；无托管区时返回 None。
    最近修改时间：2026-07-25 00:00:00；改动原因：保留旧版显式读取但拒绝误读 v4 registry。
    """
    # 1. 读取原始值并拒绝 v4 注册表，保持旧 API 的单投影语义明确。
    value = _extract_raw_projection_value(document)
    if value is None:
        return None
    if isinstance(value, Mapping) and value.get("version") == REGISTRY_VERSION:
        raise ProjectionContractError("v4 registry requires session-aware loading")
    return validate_projection(value)


def extract_registry(document: str, *, session_id: str | None = None) -> dict[str, Any] | None:
    """解析 v4 注册表，并把 v1-v3 单投影包装为内存中的单条注册表。

    [参数] document: PROJECT_CURRENT.md 全文；session_id: 旧活动投影迁移归属。
    [返回] dict | None：合法 v4 注册表；无托管区时返回 None。
    最近修改时间：2026-07-25 00:00:00；改动原因：统一新旧格式读取并阻止旧活动投影无归属恢复。
    """
    # 1. v4 直接按 registry 契约读取，旧版投影进入显式兼容路径。
    value = _extract_raw_projection_value(document)
    if value is None:
        return None
    if isinstance(value, Mapping) and value.get("version") == REGISTRY_VERSION:
        return validate_registry(value)
    legacy = validate_projection(value)
    # 2. 旧活动投影必须由调用方提供真实会话归属；只有明确 inactive 可无会话只读。
    if session_id is None and legacy["state"] != "inactive":
        raise ProjectionContractError("active legacy projection requires session_id before recovery")
    sid = _validate_session_id(session_id or LEGACY_SESSION_ID)
    return _new_registry([_projection_entry_from_projection(legacy, sid)])


def load_projection(
    path: str | os.PathLike[str],
    *,
    session_id: str | None = None,
    expected_fingerprint: str | None = None,
    expected_source_document: str | None = None,
) -> dict[str, Any]:
    """从严格 UTF-8 文件读取并校验任务投影。

    [参数] path: PROJECT_CURRENT 路径；session_id: 可选显式会话标识（缺省回退 CODEX_THREAD_ID）；expected_fingerprint: 可选预期指纹；expected_source_document: 可选来源。
    [返回] dict：已通过读取和身份校验的投影。
    最近修改时间：2026-07-26 00:00:00；改动原因：按当前宿主会话精确读取目标投影并拒绝无归属猜测。
    """
    # 1. 严格按 UTF-8 读取，优先报告文件损坏而不进行任何会话猜测。
    target = Path(path)
    try:
        document = target.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
    # 2. 读取入口随后绑定当前会话，避免无 session 时按条目数量猜测目标投影。
    sid = _require_session_id(session_id)
    registry = extract_registry(document, session_id=sid)
    if registry is None:
        raise ProjectionContractError("task projection block is missing")
    entries = registry["projections"]
    matches = [entry for entry in entries if entry["session_id"] == sid]
    if len(matches) != 1:
        raise ProjectionContractError("session_id is required when multiple projections are active")
    return validate_projection(
        _projection_from_entry(matches[0]),
        expected_fingerprint=expected_fingerprint,
        expected_source_document=expected_source_document,
    )


def load_registry(path: str | os.PathLike[str], *, session_id: str | None = None) -> dict[str, Any]:
    """从严格 UTF-8 文件读取 v4 注册表。

    [参数] path: PROJECT_CURRENT.md 路径；session_id: 旧活动投影兼容归属。
    [返回] dict：合法 v4 注册表或旧投影的内存包装结果。
    最近修改时间：2026-07-26 00:00:00；改动原因：让注册表读取兼容显式和宿主会话解析。
    """
    # 1. 严格读取 UTF-8 文档，再交由统一兼容入口完成版本判断。
    target = Path(path)
    try:
        document = target.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
    # 2. v4 注册表读取可返回全部会话；旧活动投影仍使用显式或宿主会话完成兼容归属。
    sid = resolve_session_id(session_id, required=False)
    registry = extract_registry(document, session_id=sid)
    if registry is None:
        raise ProjectionContractError("task projection block is missing")
    return registry


def _find_registry_entry(registry: Mapping[str, Any], session_id: str) -> dict[str, Any] | None:
    """按会话定位唯一投影，允许目标会话尚未创建投影。

    [参数] registry: 合法 v4 注册表；session_id: 当前会话标识。
    [返回] dict | None：唯一匹配条目；无匹配时返回 None。
    最近修改时间：2026-07-25 00:00:00；改动原因：禁止恢复时跨会话选择投影。
    """
    # 1. 只按当前 session_id 查询，发现重复归属时立即拒绝恢复。
    sid = _validate_session_id(session_id)
    matches = [entry for entry in registry["projections"] if entry["session_id"] == sid]
    if len(matches) > 1:
        raise ProjectionContractError("multiple projections match session_id")
    return matches[0] if matches else None


def _to_version_three_projection(projection: Mapping[str, Any]) -> dict[str, Any]:
    """把兼容投影升级为统一写出的 version:3。

    [参数] projection: 已读取的 v1、v2 或 v3 投影。
    [返回] dict：可安全写回的 v3 投影。
    最近修改时间：2026-07-25 00:00:00；改动原因：将 Goal 专属 v3 与旧版本读取兼容边界集中到写入前。
    """
    # 1. 先按原版本校验，再仅在成功写入路径转换，避免读取旧投影时发生隐式迁移。
    normalized = validate_projection(projection)
    if normalized["version"] == 3:
        return dict(normalized)
    upgraded = dict(normalized)
    upgraded["version"] = 3
    if "projection_origin" not in upgraded:
        upgraded["projection_origin"] = "persisted"
        upgraded["synthesis_mode"] = "none"
    return validate_projection(upgraded)


def render_registry_block(registry: Mapping[str, Any], newline: str = "\n") -> str:
    """把合法 v4 注册表渲染为唯一托管区块。

    [参数] registry: 待渲染注册表；newline: 目标文档换行符。
    [返回] str：带唯一标记和 JSON 围栏的托管区块。
    最近修改时间：2026-07-25 00:00:00；改动原因：统一多会话注册表的落盘格式。
    """
    # 1. 先校验并规范化 registry，再按目标换行符渲染稳定 JSON。
    normalized = validate_registry(registry)
    encoded = json.dumps(normalized, ensure_ascii=False, indent=2)
    encoded = encoded.replace("\n", newline)
    return newline.join((BEGIN_MARKER, "```json", encoded, "```", END_MARKER))


def render_projection_block(
    projection: Mapping[str, Any], newline: str = "\n", *, session_id: str | None = None
) -> str:
    """把单个投影包装为 v4 注册表托管区块。

    [参数] projection: 待写入投影；newline: 目标文档换行符；session_id: 会话标识。
    [返回] str：带 JSON 围栏和唯一标记的 v4 托管区块。
    最近修改时间：2026-07-25 00:00:00；改动原因：将单投影入口兼容到多会话注册表并强制会话归属。
    """
    # 1. 保留旧函数名，统一通过 v4 注册表渲染，避免继续生成单投影文件。
    entry = _projection_entry_from_projection(projection, _require_session_id(session_id))
    return render_registry_block(_new_registry([entry]), newline)


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


@contextmanager
def _projection_file_lock(path: Path):
    """使用同目录排他锁串行化跨进程注册表读改写。

    [参数] path: PROJECT_CURRENT.md 路径。
    [返回] context manager：持锁期间允许一次完整读改写。
    最近修改时间：2026-07-25 00:00:00；改动原因：防止多个会话同时写入时产生丢失更新。
    """
    lock_path = path.with_name(f".{path.name}.lock")
    lock_fd: int | None = None
    try:
        # 1. 以 O_EXCL 创建锁文件，避免两个会话同时读取旧注册表再互相覆盖。
        for _ in range(LOCK_RETRIES):
            try:
                lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                break
            except FileExistsError:
                time.sleep(LOCK_WAIT_SECONDS)
        if lock_fd is None:
            raise ProjectionIOError(f"unable to acquire PROJECT_CURRENT lock: {path}")
        os.write(lock_fd, str(os.getpid()).encode("ascii", errors="ignore"))
        yield
    except OSError as error:
        if isinstance(error, ProjectionIOError):
            raise
        raise ProjectionIOError(f"unable to lock PROJECT_CURRENT: {path}") from error
    finally:
        if lock_fd is not None:
            try:
                os.close(lock_fd)
            except OSError:
                pass
            try:
                os.unlink(lock_path)
            except OSError:
                pass


def _prune_expired_inactive_projections(
    registry: Mapping[str, Any],
    *,
    current_session_id: str,
    observed_at: datetime | None = None,
) -> dict[str, Any]:
    """删除超过保留窗口的非当前会话完成投影。

    [参数] registry: 已校验的 v4 注册表；current_session_id: 当前会话；observed_at: 可注入的 UTC 当前时间。
    [返回] dict：仅移除过期完成投影后的 registry 副本。
    最近修改时间：2026-08-02 12:33:51；改动原因：限制 PROJECT_CURRENT 只保留近期完成投影。
    """
    # 1. 先复制并校验当前会话，避免清理逻辑修改调用方传入对象。
    sid = _require_session_id(current_session_id)
    now = observed_at or datetime.now(timezone.utc)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ProjectionContractError("observed_at must be timezone-aware")
    cutoff = now.astimezone(timezone.utc) - timedelta(seconds=INACTIVE_PROJECTION_RETENTION_SECONDS)
    updated_registry = dict(registry)
    retained = []
    for item in registry["projections"]:
        entry = dict(item)
        if entry["session_id"] == sid or entry["state"] != "inactive":
            retained.append(entry)
            continue
        completed_at = _parse_utc_timestamp("updated_at", entry["updated_at"])
        if completed_at >= cutoff:
            retained.append(entry)
    updated_registry["projections"] = retained
    return updated_registry


def _upsert_projection_while_locked(
    target: Path,
    document: str,
    bounds: tuple[int, int] | None,
    registry: Mapping[str, Any],
    projection: Mapping[str, Any],
    session_id: str,
) -> dict[str, Any]:
    """在调用方已持有文件锁时新增或替换会话投影。

    [参数] target: 目标文件；document: 锁内读取的原文；bounds: 托管区边界；registry: 已校验注册表；projection: 新投影；session_id: 当前会话。
    [返回] dict：成功原子落盘的 v3 投影。
    最近修改时间：2026-07-25 00:00:00；改动原因：让超时条件检查与条件写入共享同一临界区。
    """
    # 1. 基于锁内快照只替换当前会话条目，其它会话投影保持原样。
    normalized = _to_version_three_projection(projection)
    entry = _projection_entry_from_projection(normalized, session_id)
    updated_registry = dict(registry)
    updated_registry["projections"] = [dict(item) for item in registry["projections"]]
    replaced = False
    for index, current in enumerate(updated_registry["projections"]):
        if current["session_id"] == session_id:
            updated_registry["projections"][index] = entry
            replaced = True
            break
    if not replaced:
        updated_registry["projections"].append(entry)

    # 2. 统一清理过期完成投影，再校验完整候选 registry 和文件大小。
    now = datetime.now(timezone.utc)
    updated_registry = _prune_expired_inactive_projections(
        updated_registry,
        current_session_id=session_id,
        observed_at=now,
    )
    updated_registry["registry_updated_at"] = now.isoformat().replace("+00:00", "Z")
    updated_registry = validate_registry(updated_registry)
    newline = "\r\n" if "\r\n" in document else "\n"
    block = render_registry_block(updated_registry, newline)
    if bounds is None:
        separator = "" if not document or document.endswith(("\n", "\r")) else newline
        candidate = document + separator + block + newline
    else:
        candidate = document[: bounds[0]] + block + document[bounds[1] :]
    if len(candidate.encode("utf-8")) > MAX_FILE_BYTES:
        raise ProjectionContractError(f"PROJECT_CURRENT exceeds {MAX_FILE_BYTES} UTF-8 bytes")
    _write_text_atomic(target, candidate)
    return normalized


def upsert_projection(
    path: str | os.PathLike[str], projection: Mapping[str, Any], *, session_id: str | None = None
) -> dict[str, Any]:
    """新增或替换指定会话投影，并保护其它会话与非托管正文。

    [参数] path: PROJECT_CURRENT 路径；projection: 待持久化投影；session_id: 会话标识。
    [返回] dict：原子写入后可重读的 v3 投影。
    最近修改时间：2026-07-25 00:00:00；改动原因：复用持锁 upsert 并保持多会话写入串行化。
    """
    # 1. 在锁内读取并校验最新 registry，避免多个会话基于同一旧快照互相覆盖。
    target = Path(path)
    sid = _require_session_id(session_id)
    with _projection_file_lock(target):
        try:
            original_bytes = target.read_bytes()
            document = original_bytes.decode("utf-8", errors="strict")
        except (OSError, UnicodeDecodeError) as error:
            raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
        bounds = _validate_markers(document)
        registry = extract_registry(document, session_id=sid) or _new_registry()
        # 2. 调用只允许在持锁状态使用的写入函数，完成校验和原子替换。
        return _upsert_projection_while_locked(target, document, bounds, registry, projection, sid)


def _deactivate_projection_with_payload(
    path: str | os.PathLike[str],
    *,
    session_id: str | None = None,
    updated_at: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """在同一文件锁内完成失活写入并生成一次性完成 payload。

    [参数] path: PROJECT_CURRENT 路径；session_id: 当前会话；updated_at: 可选 UTC 更新时间。
    [返回] tuple[dict, dict]：失活后的投影与仅供本次 UI 收口的一次性 payload。
    最近修改时间：2026-07-26 00:00:00；改动原因：保证完成收口 payload 与失活写入使用同一锁和会话。
    """
    # 1. 先解析会话并在同一锁内读取目标投影，避免完成收口错写其它会话。
    sid = _require_session_id(session_id)
    target = Path(path)
    with _projection_file_lock(target):
        # 2. 严格读取托管文件并校验标记，任何损坏都不触碰原文。
        try:
            document = target.read_bytes().decode("utf-8", errors="strict")
        except (OSError, UnicodeDecodeError) as error:
            raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
        bounds = _validate_markers(document)
        registry = extract_registry(document, session_id=sid)
        if registry is None:
            raise ProjectionContractError("task projection block is missing")
        entry = _find_registry_entry(registry, sid)
        if entry is None:
            raise ProjectionContractError("current session projection is missing")
        # 3. 先生成一次性完成 payload，再将同一投影原子迁移为 inactive。
        current = _projection_from_entry(entry)
        completion_payload = build_completion_payload(current)
        current["steps"] = [
            {"id": step["id"], "step": step["step"], "status": "completed"}
            for step in current["steps"]
        ]
        current["state"] = "inactive"
        if current.get("projection_origin") == "goal":
            current["synthesis_mode"] = "goal_default"
        current["updated_at"] = updated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        persisted = _upsert_projection_while_locked(target, document, bounds, registry, current, sid)
    return persisted, completion_payload


def migrate_projection(path: str | os.PathLike[str], session_id: str | None = None) -> dict[str, Any]:
    """把现有 v1-v3 单投影立即迁移为 v4 注册表。

    [参数] path: PROJECT_CURRENT.md 路径；session_id: 旧投影归属的真实会话标识，可回退宿主会话。
    [返回] dict：迁移后或原本已存在的 v4 注册表。
    最近修改时间：2026-07-26 00:00:00；改动原因：迁移入口支持宿主会话回退并返回可同步 payload。
    """
    # 1. 已是 v4 时只校验返回，避免重复迁移改变现有多会话状态。
    sid = _require_session_id(session_id)
    target = Path(path)
    document = _read_utf8_text(target, label="UTF-8 PROJECT_CURRENT")
    raw = _extract_raw_projection_value(document)
    if raw is None:
        raise ProjectionContractError("task projection block is missing")
    if isinstance(raw, Mapping) and raw.get("version") == REGISTRY_VERSION:
        return validate_registry(raw)
    # 2. 旧格式必须绑定调用方提供的会话，再通过统一 upsert 原子写入。
    legacy = validate_projection(raw)
    upsert_projection(target, legacy, session_id=sid)
    return load_registry(target)


def deactivate_projection(
    path: str | os.PathLike[str],
    *,
    session_id: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """将现有活动投影失活，保留完成步骤作为恢复证据。

    [参数] path: PROJECT_CURRENT 路径；session_id: 会话标识；updated_at: 可选 UTC 完成时间。
    [返回] dict：全部步骤完成且已失活的 v3 投影。
    最近修改时间：2026-07-26 00:00:00；改动原因：复用锁内完成收口并返回一次性完成 payload。
    """
    # 1. 将所有步骤一次性设为完成，避免终态文件中残留进行中步骤。
    projection, _ = _deactivate_projection_with_payload(
        path, session_id=session_id, updated_at=updated_at
    )
    return projection


def _payload_explanation(projection: Mapping[str, Any]) -> str:
    """根据投影来源生成 explanation。

    [参数] projection: 已通过契约的投影。
    [返回] str：与来源和阻断状态一致的 UI 说明。
    最近修改时间：2026-07-25 00:00:00；改动原因：为 Goal 活动与阻断观察列表提供专属提示。
    """
    # 1. 先规范化版本，再依据来源而非业务内容选择无敏感数据的提示语。
    normalized = _to_version_three_projection(projection)
    origin = normalized["projection_origin"]
    mode = normalized["synthesis_mode"]
    if origin == "goal":
        return EXPLANATION_GOAL_BLOCKED if normalized["state"] == "blocked" else EXPLANATION_GOAL_ACTIVE
    if origin == "synthesized" and mode == "exact":
        return EXPLANATION_SYNTH_EXACT
    if origin == "synthesized" and mode == "fallback":
        return EXPLANATION_SYNTH_FALLBACK
    return EXPLANATION


def build_update_plan_payload(projection: Mapping[str, Any]) -> dict[str, Any]:
    """生成可直接传给 update_plan 的参数对象。

    [参数] projection: 已持久化或待验证的投影。
    [返回] dict：可由主会话传给 update_plan 的安全 payload。
    最近修改时间：2026-07-25 00:00:00；改动原因：允许 blocked Goal 仅观察刷新，禁止 completed Goal 重放。
    """
    # 1. 只允许活动投影和 Goal 阻断观察投影生成 UI 数据，失活投影不得重放。
    normalized = validate_projection(projection)
    payload_allowed = normalized["state"] == "active" or (
        normalized["state"] == "blocked" and normalized.get("projection_origin") == "goal"
    )
    if not payload_allowed:
        raise ProjectionContractError("only active or blocked Goal projection can build update_plan payload")
    return {
        "explanation": _payload_explanation(normalized),
        "plan": [{"step": step["step"], "status": step["status"]} for step in normalized["steps"]],
    }


def build_completion_payload(projection: Mapping[str, Any]) -> dict[str, Any]:
    """生成一次性完成收口 payload，失活后不可再次重放。

    [参数] projection: 已持久化的活动或 Goal 阻断投影。
    [返回] dict：所有步骤为 completed 的一次性 UI 收口数据。
    最近修改时间：2026-07-26 00:00:00；改动原因：让状态迁移在失活前完成悬浮窗收口。
    """
    # 1. 只接受仍可收口的活动或阻断投影；已失活投影禁止重新生成完成 payload。
    normalized = validate_projection(projection)
    if normalized["state"] not in {"active", "blocked"}:
        raise ProjectionContractError("completion payload requires an active projection")
    completed_projection = dict(normalized)
    completed_projection["state"] = "active"
    completed_projection["steps"] = [
        {"id": step["id"], "step": step["step"], "status": "completed"}
        for step in normalized["steps"]
    ]
    # 2. 使用独立说明明确这是完成收口，不把该临时 payload 写回磁盘或恢复为活动状态。
    return {
        "explanation": EXPLANATION_COMPLETED,
        "plan": [{"step": step["step"], "status": "completed"} for step in completed_projection["steps"]],
    }


def _goal_default_projection() -> dict[str, Any]:
    """构建不含 Goal 原文的固定安全三步。

    [参数] 无。
    [返回] dict：固定标识、固定文案和初始状态的活动 Goal v3 投影。
    最近修改时间：2026-07-25 00:00:00；改动原因：Goal 创建不保存目标原文也能提供可观察进度。
    """
    # 1. 只从常量复制安全步骤，禁止通过调用参数或运行时输入构造悬浮窗文案。
    steps = [{"id": item[0], "step": item[1], "status": item[2]} for item in GOAL_DEFAULT_STEPS]
    return validate_projection(
        {
            "version": 3,
            "state": "active",
            "projection_origin": "goal",
            "synthesis_mode": "goal_default",
            "plan_key": GOAL_PLAN_KEY,
            "source_document": "",
            "plan_fingerprint": compute_plan_fingerprint(steps),
            "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "steps": steps,
        }
    )


def handle_goal_event(
    path: str | os.PathLike[str], event: str, *, session_id: str | None = None
) -> dict[str, Any]:
    """按 Goal 生命周期持久化或恢复安全任务投影。

    [参数] path: PROJECT_CURRENT 路径；event: create、restore、blocked 或 complete；session_id: 会话标识。
    [返回] dict：事件动作、投影和可选 UI payload；complete 返回一次性完成收口 payload。
    最近修改时间：2026-07-26 00:00:00；改动原因：完成事件先返回收口 payload 再原子失活投影。
    """
    # 1. 先限制事件集合并读取既有投影；只有 create 可在无投影时初始化安全三步。
    if event not in {"create", "restore", "blocked", "complete"}:
        raise ProjectionContractError("Goal event is invalid")
    sid = _require_session_id(session_id)
    try:
        registry = load_registry(path, session_id=sid)
        entry = _find_registry_entry(registry, sid)
        projection = _projection_from_entry(entry) if entry is not None else None
    except ProjectionContractError as error:
        if event == "create" and str(error) == "task projection block is missing":
            registry = _new_registry()
            projection = None
        else:
            raise

    if event == "create":
        # 2. 仅保护活动正式计划；fallback 恢复列表不是正式来源，必须让位给 Goal 安全三步。
        formal_projection = projection is not None and projection["state"] == "active" and (
            projection.get("projection_origin", "persisted") == "persisted"
            or (projection.get("projection_origin") == "synthesized" and projection.get("synthesis_mode") == "exact")
        )
        if formal_projection:
            return {
                "ok": True,
                "action": "preserved_formal",
                "projection": projection,
                "payload": build_update_plan_payload(projection),
            }
        if projection is not None and projection["state"] == "active" and projection.get("projection_origin") == "goal":
            return {
                "ok": True,
                "action": "created",
                "projection": projection,
                "payload": build_update_plan_payload(projection),
            }
        projection = upsert_projection(path, _goal_default_projection(), session_id=sid)
        return {
            "ok": True,
            "action": "created",
            "projection": projection,
            "payload": build_update_plan_payload(projection),
        }

    # 3. 正式计划被保留后与 Goal 默认投影不建立关联，后续 Goal 事件不得失活或改写真实实施任务。
    formal_projection = projection is not None and projection["state"] == "active" and (
        projection.get("projection_origin", "persisted") == "persisted"
        or (projection.get("projection_origin") == "synthesized" and projection.get("synthesis_mode") == "exact")
    )
    if formal_projection:
        return {"ok": True, "action": "preserved_formal", "projection": projection, "payload": None}
    # 4. 其余生命周期事件只允许操作已有 Goal 安全投影，防止外部计划被错误迁移。
    if projection is None or projection.get("projection_origin") != "goal":
        raise ProjectionContractError("Goal event requires an existing Goal projection")
    if event == "restore":
        if projection["state"] != "active":
            raise ProjectionContractError("Goal restore requires an active Goal projection")
        return {
            "ok": True,
            "action": "restored",
            "projection": projection,
            "payload": build_update_plan_payload(projection),
        }
    if event == "blocked":
        # 5. blocked 只保留观察价值，所有进行中步骤回退为 pending 且不恢复执行授权。
        if projection["state"] != "active":
            raise ProjectionContractError("Goal blocked event requires an active Goal projection")
        projection["state"] = "blocked"
        projection["synthesis_mode"] = "goal_blocked"
        projection["steps"] = [
            {"id": step["id"], "step": step["step"], "status": "pending" if step["status"] == "in_progress" else step["status"]}
            for step in projection["steps"]
        ]
        projection["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        projection = upsert_projection(path, projection, session_id=sid)
        return {
            "ok": True,
            "action": "blocked",
            "projection": projection,
            "payload": build_update_plan_payload(projection),
        }
    # 6. complete 先生成一次性完成 payload，再以原子写入终止后续悬浮窗重放。
    if projection["state"] not in {"active", "blocked"}:
        raise ProjectionContractError("Goal complete event requires an active or blocked Goal projection")
    completion_payload = build_completion_payload(projection)
    projection["steps"] = [
        {"id": step["id"], "step": step["step"], "status": "completed"}
        for step in projection["steps"]
    ]
    projection["state"] = "inactive"
    projection["synthesis_mode"] = "goal_default"
    projection["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    projection = upsert_projection(path, projection, session_id=sid)
    return {"ok": True, "action": "completed", "projection": projection, "payload": completion_payload}


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
    """按二级标题提取 Markdown 小节正文。

    [参数] document: Markdown 全文；heading_text: 标题必须包含的文本。
    [返回] str：目标二级标题下、下一个二级标题前的正文；未命中时返回空字符串。
    最近修改时间：2026-07-25 18:23:00；改动原因：限制标题匹配不跨行并兼容 LF/CRLF，避免 exact 任务清单被吞为空区段。
    """
    # 1. 标题字符只在当前行匹配，正文再以非贪婪方式读取到下一二级标题或文末。
    pattern = re.compile(rf"^##\s+[^\r\n]*{re.escape(heading_text)}[^\r\n]*\r?\n(?P<body>.*?)(?=^##\s+|\Z)", re.M | re.S)
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
    """从正式实施文档中提取唯一 TASK 步骤。

    [参数] path: 正式实施文档路径。
    [返回] list[dict[str, str]]：按文档顺序生成的任务投影步骤。
    最近修改时间：2026-07-25 18:18:00；改动原因：兼容正式周期标题及任务 ID 不在首列的最小任务清单。
    """
    # 1. 兼容清单标题和工程文档门禁的标准执行顺序标题，再按表头定位任务 ID 与目标列。
    document = _read_utf8_text(path, label="source document")
    task_section = _extract_markdown_section(document, "最小任务清单")
    if not task_section:
        task_section = _extract_markdown_section(document, "周期内最小任务执行顺序")
    steps: list[dict[str, str]] = []
    seen: set[str] = set()
    if task_section:
        rows = _parse_markdown_table(task_section)
        task_id_column = 0
        goal_column = 1
        if rows and "任务 ID" in rows[0]:
            header_row = rows.pop(0)
            task_id_column = header_row.index("任务 ID")
            if "唯一目标" in header_row:
                goal_column = header_row.index("唯一目标")
        for cells in rows:
            if max(task_id_column, goal_column) >= len(cells):
                continue
            header = cells[task_id_column]
            goal = cells[goal_column]
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
        # 2. 没有清单章节时保留既有标签扫描兜底，不扩大可接受的任务语法。
        for match in TASK_LABEL_PATTERN.finditer(document):
            task_id = match.group("id")
            label = match.group("label").strip()
            if task_id in seen:
                continue
            seen.add(task_id)
            steps.append({"id": task_id, "step": label, "status": "pending"})
    # 3. 两条路径都没有任务时返回契约错误，禁止生成空 exact 投影。
    if not steps:
        raise ProjectionContractError("source document does not contain any task definitions")
    return steps


def _normalize_context(context: Any) -> dict[str, Any]:
    """校验 synthesize 输入上下文的必要结构。

    [参数] context: 继续恢复或超时升级的补建证据。
    [返回] dict：字段完整且触发类型受控的上下文副本。
    最近修改时间：2026-07-26 00:00:00；改动原因：新增 start 触发并保持 timeout 仅作异常修复入口。
    """
    # 1. 先校验顶层字段和触发类型，禁止其它场景借合成入口写入投影。
    if not isinstance(context, Mapping):
        raise ProjectionContractError("synthesis context must be an object")
    trigger = context.get("trigger")
    current_message = context.get("current_message")
    project_current_summary = context.get("project_current_summary")
    thread_evidence = context.get("thread_evidence")
    candidate_source_documents = context.get("candidate_source_documents")
    if trigger not in {"start", "continue", "timeout"}:
        raise ProjectionContractError("synthesis trigger must be start, continue or timeout")
    if not isinstance(current_message, str) or not current_message.strip():
        raise ProjectionContractError("current_message must be a non-empty string")
    if not isinstance(project_current_summary, Mapping):
        raise ProjectionContractError("project_current_summary must be an object")
    if not isinstance(thread_evidence, Mapping):
        raise ProjectionContractError("thread_evidence must be an object")
    if not isinstance(candidate_source_documents, list):
        raise ProjectionContractError("candidate_source_documents must be an array")
    # 2. 当前状态和线程证据必须保持既有白名单结构，超时路径不放宽业务证据要求。
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
    # 3. 候选来源按输入顺序去重，避免重复路径被误判为多来源冲突。
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


def synthesize_projection(
    path: str | os.PathLike[str], context: Any, session_id: str | None = None
) -> dict[str, Any]:
    """根据当前会话与项目文档生成 exact 或 fallback 补建结果。

    [参数] path: PROJECT_CURRENT.md 路径；context: 补建证据；session_id: 当前会话标识。
    [返回] dict：补建模式、投影、payload、会话归属和证据摘要。
    最近修改时间：2026-07-26 00:00:00；改动原因：让 start/continue 补建结果强制绑定当前宿主会话。
    """
    # 1. 补建入口也必须绑定当前会话，显式值缺失时仅允许使用宿主 CODEX_THREAD_ID。
    resolved_session_id = _require_session_id(session_id)
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

    # 2. 只有唯一来源与明确步骤证据同时成立时生成 exact，否则固定 fallback。
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
    # 3. payload 始终根据当前补建投影生成；会话标识只进入受控返回字段。
    result = {
        "mode": mode,
        "projection": projection,
        "payload": build_update_plan_payload(projection),
        "evidence": {
            "identity_confidence": identity_confidence,
            "status_confidence": status_confidence,
            "used_sources": used_sources,
        },
    }
    result["session_id"] = resolved_session_id
    return result


def _is_projection_input(value: Any) -> bool:
    """判断 ensure-start 输入是否已经是正式投影对象。

    [参数] value: 首次投影入口收到的 JSON 值。
    [返回] bool：值同时包含版本和步骤字段时返回 True。
    最近修改时间：2026-07-26 00:00:00；改动原因：区分正式投影输入与 start/continue 补建上下文。
    """
    # 1. 仅以正式投影的最小身份字段判定，详细字段由统一契约继续校验。
    return isinstance(value, Mapping) and "version" in value and "steps" in value


def ensure_start_projection(
    path: str | os.PathLike[str],
    input_value: Any,
    *,
    session_id: str | None = None,
) -> dict[str, Any]:
    """原子创建当前会话首个活动投影并立即返回 update_plan payload。

    [参数] path: PROJECT_CURRENT 路径；input_value: 正式投影或 start/continue 补建上下文；session_id: 当前会话。
    [返回] dict：创建、保留或更新动作、投影和可直接调用的 payload。
    最近修改时间：2026-07-26 00:00:00；改动原因：持久化任务后强制进入悬浮任务列表同步检查点。
    """
    # 1. 先解析当前会话；没有显式参数时只允许使用宿主 CODEX_THREAD_ID。
    sid = _require_session_id(session_id)
    _reject_sensitive_keys(input_value)
    target = Path(path)
    with _projection_file_lock(target):
        try:
            document = target.read_bytes().decode("utf-8", errors="strict")
        except (OSError, UnicodeDecodeError) as error:
            raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
        bounds = _validate_markers(document)
        registry = extract_registry(document, session_id=sid) or _new_registry()
        current_entry = _find_registry_entry(registry, sid)
        if current_entry is not None and current_entry["state"] in {"active", "blocked"}:
            current_projection = _projection_from_entry(current_entry)
            action = "already_active" if current_entry["state"] == "active" else "blocked_preserved"
            return {
                "ok": True,
                "action": action,
                "projection": current_projection,
                "payload": build_update_plan_payload(current_projection),
                "session_id": sid,
            }

        # 2. 正式投影直接写入；上下文输入走 exact/fallback 合成，但两条路径共用同一锁和原子替换。
        mode: str | None = None
        evidence: dict[str, Any] | None = None
        if _is_projection_input(input_value):
            candidate = _to_version_three_projection(input_value)
            if candidate["state"] != "active":
                raise ProjectionContractError("ensure-start requires an active projection")
        else:
            context = _normalize_context(input_value)
            if context["trigger"] == "timeout":
                raise ProjectionContractError("ensure-start requires start or continue trigger")
            synthesis_result = synthesize_projection(target, context, session_id=sid)
            candidate = synthesis_result["projection"]
            mode = synthesis_result["mode"]
            evidence = synthesis_result["evidence"]
        persisted = _upsert_projection_while_locked(
            target, document, bounds, registry, candidate, sid
        )
    result = {
        "ok": True,
        "action": "created",
        "projection": persisted,
        "payload": build_update_plan_payload(persisted),
        "session_id": sid,
    }
    if mode is not None:
        result["mode"] = mode
    if evidence is not None:
        result["evidence"] = evidence
    return result


def _calculate_effective_elapsed_seconds(
    *, started_at: str, observed_at: str, paused_seconds: Any = 0
) -> float:
    """计算扣除暂停后的主动执行秒数。

    [参数] started_at: 首次真实执行时间；observed_at: 当前检查时间；paused_seconds: 不计时的暂停秒数。
    [返回] float：非负且不超过墙钟时长的主动执行秒数。
    最近修改时间：2026-07-25 20:30:00；改动原因：让只读探测与持久化升级共享同一时间边界。
    """
    # 1. 统一校验 UTC 时间和暂停区间，避免两个超时入口产生边界漂移。
    started = _parse_utc_timestamp("started_at", started_at)
    observed = _parse_utc_timestamp("observed_at", observed_at)
    normalized_paused_seconds = _validate_paused_seconds(paused_seconds)
    if observed < started:
        raise ProjectionContractError("observed_at must not be earlier than started_at")
    wall_elapsed_seconds = (observed - started).total_seconds()
    if normalized_paused_seconds > wall_elapsed_seconds:
        raise ProjectionContractError("paused_seconds must not exceed wall elapsed seconds")
    return wall_elapsed_seconds - normalized_paused_seconds


def probe_timeout_projection(
    path: str | os.PathLike[str],
    *,
    started_at: str,
    observed_at: str,
    session_id: str | None = None,
    paused_seconds: Any = 0,
) -> dict[str, Any]:
    """只读判断当前会话是否应进入 Goal 检查。

    [参数] path: PROJECT_CURRENT.md 路径；started_at: 首次真实执行时间；observed_at: 当前检查时间；session_id: 当前会话；paused_seconds: 不计时暂停秒数。
    [返回] dict：not_due、already_active、blocked_goal_preserved 或 goal_check_required；payload 固定为空。
    最近修改时间：2026-07-25 20:30:00；改动原因：在创建 Goal 前提供无投影写入的严格十分钟资格探测。
    """
    # 1. 先校验会话和时间；非法输入不得触碰项目状态。
    sid = _require_session_id(session_id)
    effective_elapsed_seconds = _calculate_effective_elapsed_seconds(
        started_at=started_at,
        observed_at=observed_at,
        paused_seconds=paused_seconds,
    )
    # 2. 直接读取原子维护的 registry；探测不能创建锁文件或其它临时文件。
    target = Path(path)
    try:
        document = target.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
    _validate_markers(document)
    registry = extract_registry(document, session_id=sid)
    if effective_elapsed_seconds <= TIMEOUT_SECONDS:
        action = "not_due"
    else:
        current_entry = _find_registry_entry(registry, sid) if registry is not None else None
        if current_entry is None or current_entry["state"] == "inactive":
            action = "goal_check_required"
        elif current_entry["state"] == "blocked":
            action = "blocked_goal_preserved"
        else:
            action = "already_active"
    # 3. 探测只返回控制事实；不生成 projection 或 UI payload，也不写入文件。
    return {
        "ok": True,
        "action": action,
        "effective_elapsed_seconds": effective_elapsed_seconds,
        "payload": None,
        "session_id": sid,
    }


def ensure_timeout_projection(
    path: str | os.PathLike[str],
    *,
    started_at: str,
    observed_at: str,
    context: Any,
    session_id: str | None = None,
    paused_seconds: Any = 0,
) -> dict[str, Any]:
    """在有效执行耗时超过十分钟时为当前会话补建任务投影。

    [参数] path: PROJECT_CURRENT.md 路径；started_at: 首次真实执行时间；observed_at: 本次观测时间；context: 合成证据；session_id: 当前会话；paused_seconds: 不计时的暂停秒数。
    [返回] dict：not_due、already_active、blocked_goal_preserved 或 escalated 动作及可用 payload。
    最近修改时间：2026-07-25 00:00:00；改动原因：让无悬浮窗任务在有效执行超过 600 秒后强制升级。
    """
    # 1. 先校验会话、时间和暂停输入；任一非法输入都不得触碰磁盘状态。
    sid = _require_session_id(session_id)
    effective_elapsed_seconds = _calculate_effective_elapsed_seconds(
        started_at=started_at,
        observed_at=observed_at,
        paused_seconds=paused_seconds,
    )
    _reject_sensitive_keys(context)
    normalized_context = _normalize_context(context)
    if normalized_context["trigger"] != "timeout":
        raise ProjectionContractError("ensure-timeout requires synthesis trigger timeout")

    # 2. 锁内严格读取并校验现有 registry；损坏状态必须报错，不能以无投影处理。
    target = Path(path)
    with _projection_file_lock(target):
        try:
            document = target.read_bytes().decode("utf-8", errors="strict")
        except (OSError, UnicodeDecodeError) as error:
            raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
        bounds = _validate_markers(document)
        registry = extract_registry(document, session_id=sid)
        if effective_elapsed_seconds <= TIMEOUT_SECONDS:
            return {
                "ok": True,
                "action": "not_due",
                "effective_elapsed_seconds": effective_elapsed_seconds,
                "payload": None,
            }

        # 3. 超时后只检查当前会话；活动投影和 blocked Goal 都直接返回且不重复写入。
        current_entry = _find_registry_entry(registry, sid) if registry is not None else None
        if current_entry is not None and current_entry["state"] in {"active", "blocked"}:
            current_projection = _projection_from_entry(current_entry)
            action = "already_active" if current_entry["state"] == "active" else "blocked_goal_preserved"
            return {
                "ok": True,
                "action": action,
                "effective_elapsed_seconds": effective_elapsed_seconds,
                "projection": current_projection,
                "payload": build_update_plan_payload(current_projection),
            }

        # 4. inactive 或无当前会话投影时在同一临界区完成合成与条件写入，消除 TOCTOU 覆盖窗口。
        synthesis_result = synthesize_projection(target, normalized_context, session_id=sid)
        persisted_projection = _upsert_projection_while_locked(
            target,
            document,
            bounds,
            registry or _new_registry(),
            synthesis_result["projection"],
            sid,
        )
    # 5. payload 只根据成功原子落盘的结果生成；写入失败时不会进入返回路径。
    return {
        "ok": True,
        "action": "escalated",
        "effective_elapsed_seconds": effective_elapsed_seconds,
        "mode": synthesis_result["mode"],
        "projection": persisted_projection,
        "payload": build_update_plan_payload(persisted_projection),
        "evidence": synthesis_result["evidence"],
        "session_id": sid,
    }


def main() -> None:
    """解析 CLI 子命令并返回稳定退出码。

    [参数] 无；命令行参数由 argparse 读取。
    [返回] None：成功输出 JSON，契约或 I/O 失败输出稳定错误码。
    最近修改时间：2026-07-26 00:00:00；改动原因：增加 ensure-start、会话回退和完成收口 payload CLI。
    """
    # 1. 注册全部子命令，Goal 事件仅接受四个受控生命周期值。
    parser = argparse.ArgumentParser(description="Maintain PROJECT_CURRENT task plan projection")
    subparsers = parser.add_subparsers(dest="command", required=True)
    fingerprint_parser = subparsers.add_parser("fingerprint")
    fingerprint_parser.add_argument("--input", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--project-current", required=True)
    validate_parser.add_argument("--session-id")
    write_parser = subparsers.add_parser("write")
    write_parser.add_argument("--project-current", required=True)
    write_parser.add_argument("--input", required=True)
    write_parser.add_argument("--session-id")
    ensure_start_parser = subparsers.add_parser("ensure-start")
    ensure_start_parser.add_argument("--project-current", required=True)
    ensure_start_parser.add_argument("--input", required=True)
    ensure_start_parser.add_argument("--session-id")
    payload_parser = subparsers.add_parser("payload")
    payload_parser.add_argument("--project-current", required=True)
    payload_parser.add_argument("--session-id")
    synthesize_parser = subparsers.add_parser("synthesize")
    synthesize_parser.add_argument("--project-current", required=True)
    synthesize_parser.add_argument("--input", required=True)
    synthesize_parser.add_argument("--session-id")
    probe_timeout_parser = subparsers.add_parser("probe-timeout")
    probe_timeout_parser.add_argument("--project-current", required=True)
    probe_timeout_parser.add_argument("--started-at", required=True)
    probe_timeout_parser.add_argument("--observed-at", required=True)
    probe_timeout_parser.add_argument("--session-id")
    probe_timeout_parser.add_argument("--paused-seconds", default="0")
    ensure_timeout_parser = subparsers.add_parser("ensure-timeout")
    ensure_timeout_parser.add_argument("--project-current", required=True)
    ensure_timeout_parser.add_argument("--started-at", required=True)
    ensure_timeout_parser.add_argument("--observed-at", required=True)
    ensure_timeout_parser.add_argument("--input", required=True)
    ensure_timeout_parser.add_argument("--session-id")
    ensure_timeout_parser.add_argument("--paused-seconds", default="0")
    deactivate_parser = subparsers.add_parser("deactivate")
    deactivate_parser.add_argument("--project-current", required=True)
    deactivate_parser.add_argument("--updated-at")
    deactivate_parser.add_argument("--session-id")
    migrate_parser = subparsers.add_parser("migrate")
    migrate_parser.add_argument("--project-current", required=True)
    migrate_parser.add_argument("--session-id")
    goal_parser = subparsers.add_parser("goal")
    goal_parser.add_argument("--project-current", required=True)
    goal_parser.add_argument("--event", choices=("create", "restore", "blocked", "complete"), required=True)
    goal_parser.add_argument("--session-id")
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
                session_id=args.session_id,
                expected_fingerprint=args.expected_fingerprint,
                expected_source_document=args.expected_source_document,
            )
            _print_json({"ok": True, "projection": projection})
        elif args.command == "write":
            projection = upsert_projection(
                args.project_current, _read_json_input(args.input), session_id=args.session_id
            )
            payload = build_update_plan_payload(projection) if projection["state"] in {"active", "blocked"} else None
            _print_json({"ok": True, "projection": projection, "payload": payload})
        elif args.command == "ensure-start":
            _print_json(
                ensure_start_projection(
                    args.project_current, _read_json_input(args.input), session_id=args.session_id
                )
            )
        elif args.command == "payload":
            projection = load_projection(
                args.project_current,
                session_id=args.session_id,
                expected_fingerprint=args.expected_fingerprint,
                expected_source_document=args.expected_source_document,
            )
            _print_json(build_update_plan_payload(projection))
        elif args.command == "synthesize":
            _print_json(
                synthesize_projection(
                    args.project_current, _read_json_input(args.input), session_id=args.session_id
                )
            )
        elif args.command == "probe-timeout":
            _print_json(
                probe_timeout_projection(
                    args.project_current,
                    started_at=args.started_at,
                    observed_at=args.observed_at,
                    session_id=args.session_id,
                    paused_seconds=args.paused_seconds,
                )
            )
        elif args.command == "ensure-timeout":
            _print_json(
                ensure_timeout_projection(
                    args.project_current,
                    started_at=args.started_at,
                    observed_at=args.observed_at,
                    context=_read_json_input(args.input),
                    session_id=args.session_id,
                    paused_seconds=args.paused_seconds,
                )
            )
        elif args.command == "goal":
            # 2. CLI 只持久化和返回 payload，主会话决定是否调用 update_plan。
            _print_json(handle_goal_event(args.project_current, args.event, session_id=args.session_id))
        elif args.command == "migrate":
            sid = _require_session_id(args.session_id)
            registry = migrate_projection(args.project_current, sid)
            projection = load_projection(args.project_current, session_id=sid)
            payload = build_update_plan_payload(projection) if projection["state"] in {"active", "blocked"} else None
            _print_json({"ok": True, "registry": registry, "projection": projection, "payload": payload})
        elif args.command == "deactivate":
            projection, payload = _deactivate_projection_with_payload(
                args.project_current, session_id=args.session_id, updated_at=args.updated_at
            )
            _print_json({"ok": True, "projection": projection, "payload": payload})
    except ProjectionContractError as error:
        _print_json({"error": "contract", "message": str(error)}, sys.stderr)
        raise SystemExit(2) from error
    except ProjectionIOError as error:
        _print_json({"error": "io", "message": str(error)}, sys.stderr)
        raise SystemExit(3) from error


if __name__ == "__main__":
    main()
