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
TOP_LEVEL_FIELDS = {
    "version",
    "state",
    "plan_key",
    "source_document",
    "plan_fingerprint",
    "updated_at",
    "steps",
}
STEP_FIELDS = {"id", "step", "status"}
STEP_STATUSES = {"pending", "in_progress", "completed"}
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


class ProjectionContractError(ValueError):
    """任务投影违反 schema、标记或安全契约。"""


class ProjectionIOError(OSError):
    """任务投影文件读取或原子写入失败。"""


# compute_plan_fingerprint 根据任务 ID、顺序和文案计算稳定指纹。
# [参数] steps: 含 id 和 step 的有序步骤序列。
# [返回] str：64 位小写 SHA-256。
# 最近修改时间：2026-07-23；改动原因：为跨进程计划来源校验提供稳定标识。
def compute_plan_fingerprint(steps: Sequence[Mapping[str, Any]]) -> str:
    """根据任务 ID、顺序和文案计算稳定指纹。"""
    # 1. 只投影影响计划身份的两个字段，状态变化不参与指纹。
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

    # 2. 使用固定 JSON 序列化口径，确保不同进程得到相同结果。
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# _reject_sensitive_keys 递归拒绝敏感键，避免未知嵌套结构绕过顶层白名单。
# [参数] value: 任意 JSON 值；path: 当前字段路径。
# [返回] None：发现敏感键时抛出 ProjectionContractError。
# 最近修改时间：2026-07-23；改动原因：禁止任务投影保存凭据、原始输入和业务数据。
def _reject_sensitive_keys(value: Any, path: str = "projection") -> None:
    """递归拒绝敏感键。"""
    # 1. 映射逐键检查，并递归进入子值。
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in SENSITIVE_KEYS:
                raise ProjectionContractError(f"sensitive field is forbidden: {path}.{key}")
            _reject_sensitive_keys(child, f"{path}.{key}")
        return

    # 2. 数组逐项检查；标量不包含可递归字段。
    if isinstance(value, list):
        for index, child in enumerate(value):
            _reject_sensitive_keys(child, f"{path}[{index}]")


# _validate_utc_timestamp 校验更新时间为带 UTC 时区的 ISO-8601。
# [参数] value: updated_at 字段值。
# [返回] None：格式或时区错误时抛出 ProjectionContractError。
# 最近修改时间：2026-07-23；改动原因：统一跨进程时间口径。
def _validate_utc_timestamp(value: Any) -> None:
    """校验更新时间为带 UTC 时区的 ISO-8601。"""
    # 1. 先拒绝空值和非字符串，避免解析器接受隐式转换。
    if not isinstance(value, str) or not value.strip():
        raise ProjectionContractError("updated_at must be a non-empty UTC ISO-8601 string")
    # 2. 解析 ISO-8601，统一把 Z 转为标准 UTC 偏移。
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ProjectionContractError("updated_at must be valid ISO-8601") from error
    # 3. 最后锁定 UTC 时区，拒绝本地时间和其它偏移。
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ProjectionContractError("updated_at must use UTC timezone")


# validate_projection 校验投影字段、状态、指纹和可选来源预期。
# [参数] value: 投影对象；expected_fingerprint/source_document: 可选恢复期预期值。
# [返回] dict：规范化后的投影副本。
# 最近修改时间：2026-07-23；改动原因：建立任务投影唯一机器契约。
def validate_projection(
    value: Any,
    *,
    expected_fingerprint: str | None = None,
    expected_source_document: str | None = None,
) -> dict[str, Any]:
    """校验投影字段、状态、指纹和可选来源预期。"""
    # 1. 校验顶层字段和敏感内容，拒绝任何平行扩展字段。
    if not isinstance(value, Mapping):
        raise ProjectionContractError("projection root must be an object")
    _reject_sensitive_keys(value)
    actual_fields = set(value)
    if actual_fields != TOP_LEVEL_FIELDS:
        missing = sorted(TOP_LEVEL_FIELDS - actual_fields)
        unknown = sorted(actual_fields - TOP_LEVEL_FIELDS)
        raise ProjectionContractError(f"projection fields mismatch: missing={missing}, unknown={unknown}")
    if value.get("version") != 1:
        raise ProjectionContractError("version must be 1")
    state = value.get("state")
    if state not in {"active", "inactive"}:
        raise ProjectionContractError("state must be active or inactive")

    # 2. 校验计划标识、来源、时间和步骤数组基础结构。
    plan_key = value.get("plan_key")
    source_document = value.get("source_document")
    fingerprint = value.get("plan_fingerprint")
    for field_name, field_value in (
        ("plan_key", plan_key),
        ("source_document", source_document),
        ("plan_fingerprint", fingerprint),
    ):
        if not isinstance(field_value, str):
            raise ProjectionContractError(f"{field_name} must be a string")
    _validate_utc_timestamp(value.get("updated_at"))
    steps = value.get("steps")
    if not isinstance(steps, list):
        raise ProjectionContractError("steps must be an array")
    if len(steps) > MAX_STEPS:
        raise ProjectionContractError(f"steps must not exceed {MAX_STEPS}")

    # 3. 逐步骤校验白名单、唯一 ID、文案长度和状态数量。
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

    # 4. 校验活动/失活状态和指纹，空失活槽位允许空标识。
    if not normalized_steps:
        if state != "inactive" or any((plan_key, source_document, fingerprint)):
            raise ProjectionContractError("empty steps are only allowed for an empty inactive slot")
    else:
        if not plan_key.strip() or not source_document.strip():
            raise ProjectionContractError("non-empty projection requires plan_key and source_document")
        computed = compute_plan_fingerprint(normalized_steps)
        if not re.fullmatch(r"[0-9a-f]{64}", fingerprint) or fingerprint != computed:
            raise ProjectionContractError("plan_fingerprint does not match ordered step ids and text")
        if state == "active" and all(step["status"] == "completed" for step in normalized_steps):
            raise ProjectionContractError("an all-completed projection must be inactive")
        if state == "inactive" and any(step["status"] != "completed" for step in normalized_steps):
            raise ProjectionContractError("inactive projection may only retain completed steps")

    # 5. 恢复期可追加来源和指纹预期，防止错误计划被重建。
    if expected_fingerprint is not None and fingerprint != expected_fingerprint:
        raise ProjectionContractError("projection fingerprint does not match expected fingerprint")
    if expected_source_document is not None and source_document != expected_source_document:
        raise ProjectionContractError("projection source_document does not match expected source")
    return {
        "version": 1,
        "state": state,
        "plan_key": plan_key,
        "source_document": source_document,
        "plan_fingerprint": fingerprint,
        "updated_at": value["updated_at"],
        "steps": normalized_steps,
    }


# _validate_markers 校验托管标记数量和顺序。
# [参数] document: PROJECT_CURRENT.md 文本。
# [返回] tuple[int, int] | None：完整区块起止位置；无区块返回 None。
# 最近修改时间：2026-07-23；改动原因：保护非托管正文并拒绝重复或损坏区块。
def _validate_markers(document: str) -> tuple[int, int] | None:
    """校验托管标记数量和顺序。"""
    # 1. 分别收集起止标记，避免半标记和重复标记绕过整块正则。
    begins = [match.start() for match in re.finditer(re.escape(BEGIN_MARKER), document)]
    ends = [match.start() for match in re.finditer(re.escape(END_MARKER), document)]
    # 2. 没有标记表示尚未初始化，由写入入口负责追加唯一托管区。
    if not begins and not ends:
        return None
    # 3. 已有标记必须严格形成一对且起点在终点之前。
    if len(begins) != 1 or len(ends) != 1 or begins[0] >= ends[0]:
        raise ProjectionContractError("task projection markers must form exactly one ordered pair")
    # 4. 标记内部必须是唯一、完整的 JSON fenced block。
    match = BLOCK_PATTERN.search(document)
    if match is None or match.start() != begins[0] or match.end() != ends[0] + len(END_MARKER):
        raise ProjectionContractError("task projection block must contain one exact json fence")
    return match.start(), match.end()


# extract_projection 从文档中解析并校验任务投影。
# [参数] document: PROJECT_CURRENT.md 全文。
# [返回] dict | None：合法投影；没有托管区时返回 None。
# 最近修改时间：2026-07-23；改动原因：提供无文件副作用的解析入口。
def extract_projection(document: str) -> dict[str, Any] | None:
    """从文档中解析并校验任务投影。"""
    # 1. 先验证托管区边界；没有区块时保持无副作用返回。
    bounds = _validate_markers(document)
    if bounds is None:
        return None
    # 2. 在已确认边界内提取 JSON fenced block。
    match = BLOCK_PATTERN.search(document, bounds[0], bounds[1])
    if match is None:
        raise ProjectionContractError("task projection block is malformed")
    # 3. JSON 损坏时转换为稳定契约错误，不泄漏解析器细节。
    try:
        value = json.loads(match.group("json"))
    except json.JSONDecodeError as error:
        raise ProjectionContractError(f"task projection JSON is invalid: {error.msg}") from error
    # 4. 解析成功后继续执行完整 schema 和状态校验。
    return validate_projection(value)


# load_projection 从严格 UTF-8 文件读取并校验任务投影。
# [参数] path: PROJECT_CURRENT.md；expected_*: 可选恢复期预期。
# [返回] dict：合法投影。
# 最近修改时间：2026-07-23；改动原因：支持跨进程恢复和来源校验。
def load_projection(
    path: str | os.PathLike[str],
    *,
    expected_fingerprint: str | None = None,
    expected_source_document: str | None = None,
) -> dict[str, Any]:
    """从严格 UTF-8 文件读取并校验任务投影。"""
    target = Path(path)
    # 1. 以严格 UTF-8 读取，拒绝替换字符和系统默认编码漂移。
    try:
        document = target.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error
    # 2. 提取唯一托管区，缺失时明确拒绝恢复。
    projection = extract_projection(document)
    if projection is None:
        raise ProjectionContractError("task projection block is missing")
    # 3. 恢复路径追加来源和指纹预期，防止错计划重建。
    return validate_projection(
        projection,
        expected_fingerprint=expected_fingerprint,
        expected_source_document=expected_source_document,
    )


# render_projection_block 把合法投影渲染为唯一托管区块。
# [参数] projection: 投影对象；newline: 原文换行风格。
# [返回] str：完整 Markdown 托管区块。
# 最近修改时间：2026-07-23；改动原因：统一 PROJECT_CURRENT 托管区格式。
def render_projection_block(projection: Mapping[str, Any], newline: str = "\n") -> str:
    """把合法投影渲染为唯一托管区块。"""
    normalized = validate_projection(projection)
    encoded = json.dumps(normalized, ensure_ascii=False, indent=2)
    encoded = encoded.replace("\n", newline)
    return newline.join((BEGIN_MARKER, "```json", encoded, "```", END_MARKER))


# _write_text_atomic 在同目录完整写入并原子替换目标文件。
# [参数] path: 目标文件；document: 已完成大小校验的候选全文。
# [返回] None：写入失败时抛出 ProjectionIOError。
# 最近修改时间：2026-07-23；改动原因：保证中断和替换失败不会留下半份状态。
def _write_text_atomic(path: Path, document: str) -> None:
    """在同目录完整写入并原子替换目标文件。"""
    temp_name: str | None = None
    try:
        # 1. 临时文件与目标位于同一目录，写入后刷新文件内容。
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

        # 2. 关闭临时文件后原子替换；成功后尝试刷新目录元数据。
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


# upsert_projection 新增或替换唯一任务投影区块，并保护非托管正文。
# [参数] path: PROJECT_CURRENT.md；projection: 合法投影对象。
# [返回] dict：实际写入的规范化投影。
# 最近修改时间：2026-07-23；改动原因：实现活动投影的原子持久化入口。
def upsert_projection(path: str | os.PathLike[str], projection: Mapping[str, Any]) -> dict[str, Any]:
    """新增或替换唯一任务投影区块，并保护非托管正文。"""
    target = Path(path)
    try:
        original_bytes = target.read_bytes()
        document = original_bytes.decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as error:
        raise ProjectionIOError(f"unable to read UTF-8 PROJECT_CURRENT: {target}") from error

    # 1. 先校验投影和既有标记，在任何临时文件写入前构造完整候选。
    normalized = validate_projection(projection)
    bounds = _validate_markers(document)
    newline = "\r\n" if "\r\n" in document else "\n"
    block = render_projection_block(normalized, newline)
    if bounds is None:
        separator = "" if not document or document.endswith(("\n", "\r")) else newline
        candidate = document + separator + block + newline
    else:
        candidate = document[: bounds[0]] + block + document[bounds[1] :]

    # 2. 按最终全文 UTF-8 字节数执行硬闸门，通过后才原子替换。
    if len(candidate.encode("utf-8")) > MAX_FILE_BYTES:
        raise ProjectionContractError(f"PROJECT_CURRENT exceeds {MAX_FILE_BYTES} UTF-8 bytes")
    _write_text_atomic(target, candidate)
    return normalized


# deactivate_projection 将现有活动投影失活，保留完成步骤作为恢复证据。
# [参数] path: PROJECT_CURRENT.md；updated_at: 可选 UTC 时间。
# [返回] dict：失活后的投影。
# 最近修改时间：2026-07-23；改动原因：防止完成计划在后续回合重复出现。
def deactivate_projection(
    path: str | os.PathLike[str],
    *,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """将现有活动投影失活，保留完成步骤作为恢复证据。"""
    # 1. 失活是最后一步完成和 state 切换的单次原子迁移，不留下 active 全完成中间态。
    projection = load_projection(path)
    projection["steps"] = [
        {"id": step["id"], "step": step["step"], "status": "completed"}
        for step in projection["steps"]
    ]
    projection["state"] = "inactive"
    projection["updated_at"] = updated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return upsert_projection(path, projection)


# build_update_plan_payload 生成可直接传给 update_plan 的参数对象。
# [参数] projection: 已校验活动投影。
# [返回] dict：explanation 和 plan 数组。
# 最近修改时间：2026-07-23；改动原因：保证 UI 步骤和磁盘状态使用同一数据源。
def build_update_plan_payload(projection: Mapping[str, Any]) -> dict[str, Any]:
    """生成可直接传给 update_plan 的参数对象。"""
    # 1. 先执行完整契约校验，并拒绝任何失活投影。
    normalized = validate_projection(projection)
    if normalized["state"] != "active":
        raise ProjectionContractError("inactive projection cannot build update_plan payload")
    # 2. payload 只保留 update_plan 接受的 explanation、step 和 status。
    return {
        "explanation": EXPLANATION,
        "plan": [
            {"step": step["step"], "status": step["status"]}
            for step in normalized["steps"]
        ],
    }


# _read_json_input 从文件或标准输入读取 JSON。
# [参数] source: 文件路径或 '-'。
# [返回] Any：解析后的 JSON 值。
# 最近修改时间：2026-07-23；改动原因：避免内联 JSON 的 shell 转义和参数泄露。
def _read_json_input(source: str) -> Any:
    """从文件或标准输入读取 JSON。"""
    # 1. 统一按 UTF-8 读取并解析，避免把 shell 内联转义当作业务数据。
    try:
        text = sys.stdin.read() if source == "-" else Path(source).read_text(encoding="utf-8")
        return json.loads(text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProjectionIOError(f"unable to read JSON input: {source}") from error


# _print_json 以统一 UTF-8 JSON 格式输出命令结果。
# [参数] value: 可 JSON 序列化结果；stream: 输出流。
# [返回] None。
# 最近修改时间：2026-07-23；改动原因：统一 CLI stdout/stderr 契约。
def _print_json(value: Any, stream: Any = sys.stdout) -> None:
    """以统一 UTF-8 JSON 格式输出命令结果。"""
    stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


# main 解析 CLI 子命令并返回稳定退出码。
# [参数] 无：从命令行读取。
# [返回] None：成功退出 0，契约错误退出 2，I/O 错误退出 3。
# 最近修改时间：2026-07-23；改动原因：提供可由 Skill 稳定调用的投影操作入口。
def main() -> None:
    """解析 CLI 子命令并返回稳定退出码。"""
    # 1. 定义五个子命令和共享恢复期预期参数。
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
    deactivate_parser = subparsers.add_parser("deactivate")
    deactivate_parser.add_argument("--project-current", required=True)
    deactivate_parser.add_argument("--updated-at")
    for current in (validate_parser, payload_parser):
        current.add_argument("--expected-fingerprint")
        current.add_argument("--expected-source-document")
    args = parser.parse_args()

    # 2. 执行确定性操作；脚本只生成 payload，不直接调用 update_plan。
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
