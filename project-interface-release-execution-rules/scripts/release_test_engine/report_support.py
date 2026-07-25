"""接口报告的统计、格式化和 UTF-8 写入辅助函数。"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping


SENSITIVE_FIELDS = {
    "token",
    "access_token",
    "refresh_token",
    "password",
    "secret",
    "authorization",
    "cookie",
    "set-cookie",
    "phone",
    "idcard",
    "bankcard",
    "api-key",
    "api_key",
    "apikey",
    "x-api-key",
}
SENSITIVE_TEXT_FIELDS = {"reason", "message", "msg", "error", "detail", "explanation", "raw", "stdout", "stderr"}
SAFE_PROTOCOL_CODE_PATTERN = re.compile(
    r"\b(?:SSE_(?:MEDIA_TYPE_INVALID|EVENT_TIMEOUT|STREAM_INTERRUPTED|SUBSCRIPTION_NOT_READY)"
    r"|WS_(?:MESSAGE_TIMEOUT|DUPLICATE_MESSAGE|CONNECTION_CLOSED_(?:[0-9]+|unknown)|SESSION_(?:ALREADY_CONNECTED|NOT_CONNECTED))"
    r"|SOCKETIO_(?:CONNECT_FAILED|ACK_FAILED|EVENT_TIMEOUT))\b"
)
SAFE_REPORT_MESSAGES = {
    "all deterministic assertions passed",
    "deterministic scenario assertion or transport failed",
    "declared cleanup did not complete",
    "required protocol runtime is unavailable",
}
REDACTED_REPORT_DETAIL = "report detail redacted"


def safe_report_reason(value: Any) -> str:
    """把外部失败文本收敛为安全机器码或通用摘要。

    [参数] value: 可能包含请求值、响应值或敏感文本的失败详情。
    [返回] 白名单协议码、固定安全摘要或空字符串。
    最近修改时间：2026-07-25 21:59:37，禁止任意失败原因进入正式 JSON、Markdown 和 shadow 证据。
    """

    # 1. 空值与引擎固定摘要原样保留，协议异常只提取已注册的稳定机器码。
    text = str(value or "")
    if not text or text in SAFE_REPORT_MESSAGES:
        return text
    matched = SAFE_PROTOCOL_CODE_PATTERN.search(text)
    if matched:
        return matched.group(0)
    return REDACTED_REPORT_DETAIL


def redact_evidence(value: Any) -> Any:
    """递归生成可持久化的脱敏证据副本。

    [参数] value: 门禁、报告或场景运行产生的任意结构化值。
    [返回] 敏感字段和自由文本已收敛、原始字节已摘要化的副本。
    最近修改时间：2026-07-25 21:59:37，失败字段无论标量还是容器都整体收敛后再写盘。
    """

    # 1. 映射先按字段语义处理凭据和自由文本，再递归处理普通结构字段。
    if isinstance(value, Mapping):
        result: dict[Any, Any] = {}
        for key, child in value.items():
            # 1.1 凭据字段直接掩码，自由文本字段收敛摘要，其余字段继续递归。
            normalized_key = str(key).lower()
            if normalized_key in SENSITIVE_FIELDS:
                result[key] = "***"
            elif normalized_key in SENSITIVE_TEXT_FIELDS:
                result[key] = safe_report_reason(child)
            else:
                result[key] = redact_evidence(child)
        return result
    # 2. 序列保持声明顺序，原始字节只保留长度和摘要，避免敏感报文落盘。
    if isinstance(value, (list, tuple)):
        return [redact_evidence(item) for item in value]
    if isinstance(value, bytes):
        return {"length": len(value), "sha256": hashlib.sha256(value).hexdigest()}
    return value


def sensitive_evidence_values(value: Any) -> set[bytes]:
    """提取本轮脱敏流程应删除的原始敏感值，仅供内存内证据复核。

    [参数] value: 写报告前的原始结构化输入。
    [返回] 需要从正式产物中消失的非空 UTF-8 或原始字节集合。
    最近修改时间：2026-07-25 23:08:00，补齐数字和布尔敏感标量的内存扫描标记。
    """

    values: set[bytes] = set()

    def collect_leaves(child: Any) -> None:
        """收集敏感字段容器中的全部标量字节。

        [参数] child: 已由敏感字段名确认的值或嵌套容器。
        [返回] 无，结果写入外层内存集合。
        最近修改时间：2026-07-25 23:08:00，支持文本、字节、数字和布尔失败详情复核。
        """

        # 1. 容器递归展开，字符串和字节只保存在当前调用内存，不进入任何报告。
        if isinstance(child, Mapping):
            for nested in child.values():
                collect_leaves(nested)
            return
        if isinstance(child, (list, tuple)):
            for nested in child:
                collect_leaves(nested)
            return
        if isinstance(child, bytes) and child and child != b"***":
            values.add(child)
        elif isinstance(child, str) and child and child != "***":
            values.add(child.encode("utf-8"))
        elif isinstance(child, (int, float, bool)):
            values.add(str(child).encode("ascii"))

    def visit(child: Any) -> None:
        """按字段语义寻找会被脱敏流程删除的输入值。

        [参数] child: 当前递归节点。
        [返回] 无，结果写入外层内存集合。
        最近修改时间：2026-07-25 21:59:37，区分凭据字段、自由文本字段和普通结构字段。
        """

        # 1. 凭据字段全部收集；自由文本只在安全摘要会改变内容时收集原值。
        if isinstance(child, Mapping):
            for key, nested in child.items():
                normalized_key = str(key).lower()
                if normalized_key in SENSITIVE_FIELDS:
                    collect_leaves(nested)
                elif normalized_key in SENSITIVE_TEXT_FIELDS and safe_report_reason(nested) != str(nested or ""):
                    collect_leaves(nested)
                else:
                    visit(nested)
            return
        # 2. 普通序列继续寻找内部带语义字段的映射，不把普通业务字符串误判为敏感值。
        if isinstance(child, (list, tuple)):
            for nested in child:
                visit(nested)

    # 1. 提取过程只返回待验证字节，不返回字段路径或原始结构。
    visit(value)
    return values


def status_counts(items: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    """统计接口状态并保留旧 gate 计数键。

    [参数] items: 接口判定结果集合。
    [返回] 各合法状态及 skipped 的数量。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从超长报告模块迁出无状态统计逻辑。
    """

    # 1. 未知状态按 PENDING 统计，避免报告把新状态误算为通过。
    statuses = ("PASS", "EXPECTED_FAIL", "FAIL", "PENDING", "BLOCKED", "SKIPPED")
    counts = {status: 0 for status in statuses}
    for item in items:
        status = str(item.get("status", "PENDING")).upper()
        counts[status if status in counts else "PENDING"] += 1
    return counts


def risk_statistics(items: Iterable[Mapping[str, Any]], interfaces: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, int]]:
    """按 P0/P1/P2 汇总接口状态，未执行接口计入 skipped。

    [参数] items: 测试结果；interfaces: operation_id 到接口 IR 的映射。
    [返回] 风险等级到总数、通过、不通过、待确认和跳过数量的映射。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从超长报告模块迁出风险统计逻辑。
    """

    # 1. 以接口事实为全集，避免只统计有结果的接口而掩盖跳过项。
    result_by_id = {str(item.get("operation_id", "")): item for item in items}
    buckets: dict[str, dict[str, int]] = {}
    source = interfaces or result_by_id
    for operation_id, interface in source.items():
        # 1.1 每个接口按真实风险和执行状态落入唯一统计桶。
        item = result_by_id.get(str(operation_id), {})
        risk = str(interface.get("risk", item.get("risk", "P2"))).upper()
        risk = risk if risk in {"P0", "P1", "P2"} else "P2"
        counts = buckets.setdefault(risk, {"total": 0, "passed": 0, "failed": 0, "pending": 0, "skipped": 0})
        counts["total"] += 1
        status = str(item.get("status", "SKIPPED")).upper()
        if status == "PASS":
            # 1.2 PASS、待确认、跳过和失败四类互斥累计。
            counts["passed"] += 1
        elif status in {"PENDING", "BLOCKED"}:
            # 1.3 待确认、跳过和失败分支继续保持互斥。
            counts["pending"] += 1
        elif status == "SKIPPED":
            counts["skipped"] += 1
        else:
            counts["failed"] += 1
    # 2. 固定输出三个风险桶，保证旧报告消费者无需判空。
    for risk in ("P0", "P1", "P2"):
        buckets.setdefault(risk, {"total": 0, "passed": 0, "failed": 0, "pending": 0, "skipped": 0})
    return {risk: buckets[risk] for risk in ("P0", "P1", "P2")}


def parameter_summary(items: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """汇总参数解析、复用和失效状态，供报告与 baseline 共用。

    [参数] items: 带 dependency_trace 的接口结果集合。
    [返回] 参数总数、来源计数、成功/失败计数和生命周期计数。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从超长报告模块迁出参数统计逻辑。
    """

    # 1. 只读取结构化依赖追踪和生命周期事件，缺失证据不做推断。
    traces: list[Mapping[str, Any]] = []
    events: list[Mapping[str, Any]] = []
    for item in items:
        # 1.1 每条结果只接受映射型 evidence，非法证据不参与统计。
        evidence = item.get("evidence", {})
        if not isinstance(evidence, Mapping):
            continue
        trace = evidence.get("dependency_trace", [])
        if isinstance(trace, list):
            traces.extend(entry for entry in trace if isinstance(entry, Mapping))
        reusable_events = evidence.get("reusable_param_events", [])
        if isinstance(reusable_events, list):
            events.extend(entry for entry in reusable_events if isinstance(entry, Mapping))
    # 2. 分别统计解析结果、来源和生命周期，防止同一字段混用语义。
    source_counts: dict[str, int] = {}
    resolved = unresolved = 0
    lifecycle = {name: 0 for name in ("reused", "revalidated", "candidate", "stale", "invalid", "quarantined")}
    for trace in traces:
        # 2.1 每条依赖追踪同时累计来源、解析状态和生命周期。
        source = str(trace.get("source_type", trace.get("type", "unknown")))
        source_counts[source] = source_counts.get(source, 0) + 1
        if trace.get("resolved") is True:
            resolved += 1
        else:
            unresolved += 1
        status = str(trace.get("status", "")).lower()
        if status in {"reusable", "reused"}:
            lifecycle["reused"] += 1
        if status == "revalidated" or trace.get("revalidated") is True:
            lifecycle["revalidated"] += 1
        if status in {"candidate", "stale", "invalid", "quarantined"}:
            lifecycle[status] += 1
    for event in events:
        status = str(event.get("status", event.get("to_status", ""))).lower()
        if status in lifecycle:
            lifecycle[status] += 1
    return {
        "total": len(traces),
        "resolved": resolved,
        "unresolved": unresolved,
        "source_counts": dict(sorted(source_counts.items())),
        "reused": lifecycle["reused"],
        "revalidated": lifecycle["revalidated"],
        "candidate": lifecycle["candidate"],
        "stale": lifecycle["stale"],
        "invalid": lifecycle["invalid"],
        "quarantined": lifecycle["quarantined"],
        "events": [dict(event) for event in events],
    }


def safe_name(value: Any) -> str:
    """将接口标识转换为稳定的归档文件名。

    [参数] value: 接口标识。
    [返回] 仅包含 ASCII 安全字符的文件名片段。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从超长报告模块迁出文件名清理逻辑。
    """

    # 1. 非 ASCII 安全字符统一替换，空结果回退为 unknown。
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value or "unknown"))
    return name.strip("._") or "unknown"


def parse_jsonish(value: Any) -> Any:
    """解析报告中的 JSON 字符串，失败时保留原始值。

    [参数] value: 任意请求或响应证据。
    [返回] 可序列化的结构化值。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从超长报告模块迁出证据解析逻辑。
    """

    # 1. 仅解析字符串，非法 JSON 作为 raw 证据保留而不丢弃。
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return {"raw": value}
    return value


def yaml_dump(value: Any) -> str:
    """以 UTF-8 输出 YAML，缺少 PyYAML 时退化为合法 JSON。

    [参数] value: 待归档对象。
    [返回] YAML 或 JSON 文本。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从超长报告模块迁出序列化逻辑。
    """

    # 1. PyYAML 是可选工具依赖，缺失时仍生成可机读 JSON。
    try:
        import yaml

        return yaml.safe_dump(value, allow_unicode=True, sort_keys=False)
    except ImportError:
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def interface_fields(interface: Mapping[str, Any] | None, item: Mapping[str, Any], index: int) -> dict[str, str]:
    """从接口 IR 和判定结果提取块状报告字段。

    [参数] interface: 接口 IR 字典；item: 判定结果；index: 接口序号。
    [返回] 标准报告字段映射。
    最近修改时间：2026-07-25 21:59:37，接口失败原因只允许安全机器码或通用摘要进入文本报告。
    """

    # 1. 先规范入口、状态、阻断类型和参数来源，再组装稳定字段集合。
    interface = interface or {}
    entrypoint = interface.get("entrypoint", {}) if isinstance(interface.get("entrypoint", {}), Mapping) else {}
    method = str(entrypoint.get("method", "")).upper()
    path = str(entrypoint.get("path", entrypoint.get("url", "")))
    endpoint = f"{method} {path}".strip() or str(item.get("operation_id", "unknown"))
    status = str(item.get("status", "PENDING"))
    verdict = {"PASS": "通过", "EXPECTED_FAIL": "不通过", "FAIL": "不通过", "BLOCKED": "待确认", "PENDING": "待确认"}.get(status, "待确认")
    failure = str(item.get("failure_type", "") or "")
    runtime_failures = {"BLOCKED_BY_DEPENDENCY", "PARAM_UNRESOLVED", "ENV_BLOCKED", "BASELINE_STALE", "UNSUPPORTED_ADAPTER", "LOCAL_CONFIG_PROVENANCE_INVALID"}
    block = failure if failure in runtime_failures or failure.startswith("FIXTURE_") else "无"
    traces = item.get("evidence", {}).get("dependency_trace", []) if isinstance(item.get("evidence", {}), Mapping) else []
    source = ", ".join(str(trace.get("source_type", "")) for trace in traces if isinstance(trace, Mapping) and trace.get("source_type")) or "无"
    return {
        "number": str(index),
        "endpoint": endpoint,
        "name": str(interface.get("summary", interface.get("operation_id", item.get("operation_id", "unknown")))),
        "operation_id": str(item.get("operation_id", interface.get("operation_id", "unknown"))),
        "verdict": verdict,
        "block": block,
        "reason": safe_report_reason(item.get("reason", "")),
        "risk": str(interface.get("risk", "P2")),
        "source": ", ".join(str(e.get("source", e.get("type", ""))) for e in interface.get("evidence", []) if isinstance(e, Mapping)) or str(interface.get("adapter", "unknown")),
        "parameter_source": source,
        "allow_release": "否" if status != "PASS" else "是",
    }


def ensure_report_output_path(path: Path) -> None:
    """确认报告目标及现有父路径不包含符号链接。

    [参数] path: 即将创建或写入的报告路径。
    [返回] 无；检测到符号链接时抛出稳定权限异常。
    最近修改时间：2026-07-25 23:18:15，在任何 mkdir 前阻断父级 symlink 越界。
    """

    # 1. 缺失路径允许后续创建，现有任一层符号链接都可能把输出导向声明根外。
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise PermissionError("REPORT_OUTPUT_SYMLINK_FORBIDDEN")


def write_text(path: Path, value: str) -> str:
    """创建父目录并以 UTF-8 写入文本。

    [参数] path: 输出路径；value: 文本内容。
    [返回] 输出文件绝对路径字符串。
    最近修改时间：2026-07-25 23:18:15，复用 mkdir 前可调用的统一 symlink 路径闸门。
    """

    # 1. 预置 symlink 可能把正式证据导向输出根外，任何路径层级命中都必须先阻断。
    ensure_report_output_path(path)
    # 2. 所有正式文本显式使用 UTF-8，避免宿主默认编码漂移。
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")
    return str(path)
