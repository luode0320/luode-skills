"""上线测试报告、脱敏证据和基线投影。"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from .storage import BaselineStore
from .events import BaselineEvent, utc_now


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


def _redact(value: Any) -> Any:
    """递归脱敏报告对象，避免请求、响应和基线携带凭据原值。

    [参数] value: 待脱敏的映射、序列或标量。
    [返回] 与输入结构兼容、敏感字段替换为 ``***`` 的值。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 统一报告和基线的凭据脱敏边界。
    """

    if isinstance(value, Mapping):
        return {key: ("***" if str(key).lower() in SENSITIVE_FIELDS else _redact(child)) for key, child in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def _json_contract(value: Any) -> str:
    """把请求或简要响应转换成可归档、可复核的 JSON 字符串。"""

    if isinstance(value, str):
        try:
            return json.dumps(_redact(json.loads(value)), ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError):
            pass
    return json.dumps(_redact(value), ensure_ascii=False, sort_keys=True)


def _preview_data(value: Any, *, limit: int = 8) -> Any:
    """从完整业务数据生成有界的 ``dataPreview``，避免报告吞入大响应。

    [参数] value: 完整响应中的 data 或业务对象；limit: 对象字段上限。
    [返回] 脱敏且可 JSON 序列化的业务摘要。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 为人工复核保留业务证据并限制响应体积。
    """

    if isinstance(value, Mapping):
        preferred = ("id", "*Id", "status", "state", "code", "count", "total", "amount", "currency", "createdAt", "updatedAt")
        keys = list(value)
        selected: list[Any] = []
        for candidate in preferred:
            if candidate == "*Id":
                selected.extend(key for key in keys if str(key).lower().endswith("id") and key not in selected)
            elif candidate in value and candidate not in selected:
                selected.append(candidate)
        selected.extend(key for key in keys if key not in selected)
        return _redact({key: value[key] for key in selected[:limit]})
    if isinstance(value, list):
        return {"count": len(value), "items": _redact(value[:3])}
    return _redact(value)


def _response_summary(value: Any) -> dict[str, Any]:
    """从完整响应抽取合法 JSON 的人工可读摘要。

    [参数] value: runner/judge 输出的响应对象或 JSON 字符串。
    [返回] 包含 HTTP/业务状态、消息和 ``dataPreview`` 的脱敏对象。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 满足报告简要响应契约并保留业务内容。
    """

    parsed = _parse_jsonish(value)
    if not isinstance(parsed, Mapping):
        return {"dataPreview": _preview_data(parsed)}
    body = parsed.get("body", parsed)
    body = body if isinstance(body, Mapping) else {"data": body}
    summary: dict[str, Any] = {}
    for key in ("httpCode", "httpStatus", "status", "code", "message", "msg", "errorType", "error"):
        if key in parsed:
            summary[key] = parsed[key]
        elif key in body:
            summary[key] = body[key]
    data = body.get("data", body)
    summary["dataPreview"] = _preview_data(data)
    return _redact(summary)


def _response_contract(value: Any) -> str:
    """把完整响应压缩成带业务预览的 JSON 字符串。

    [参数] value: 完整响应对象或字符串。
    [返回] 稳定排序、脱敏的简要响应 JSON 字符串。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 统一 Markdown 和 JSON 报告的响应契约。
    """

    return json.dumps(_response_summary(value), ensure_ascii=False, sort_keys=True)


def _status_counts(items: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    """统计接口状态并保留旧 gate 计数键。

    [参数] items: 接口判定结果集合。
    [返回] 各合法状态及 skipped 的数量。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 让风险统计和门禁摘要使用同一状态口径。
    """

    statuses = ("PASS", "EXPECTED_FAIL", "FAIL", "PENDING", "BLOCKED", "SKIPPED")
    counts = {status: 0 for status in statuses}
    for item in items:
        status = str(item.get("status", "PENDING")).upper()
        counts[status if status in counts else "PENDING"] += 1
    return counts


def _risk_statistics(items: Iterable[Mapping[str, Any]], interfaces: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, int]]:
    """按 P0/P1/P2 汇总接口状态，未执行接口计入 skipped。

    [参数] items: 测试结果；interfaces: operation_id 到接口 IR 的映射。
    [返回] 风险等级到总数、通过、不通过、待确认和跳过数量的映射。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 补齐 README 与 JSON 的风险等级统计。
    """

    result_by_id = {str(item.get("operation_id", "")): item for item in items}
    buckets: dict[str, dict[str, int]] = {}
    source = interfaces or result_by_id
    for operation_id, interface in source.items():
        item = result_by_id.get(str(operation_id), {})
        risk = str(interface.get("risk", item.get("risk", "P2"))).upper()
        risk = risk if risk in {"P0", "P1", "P2"} else "P2"
        counts = buckets.setdefault(risk, {"total": 0, "passed": 0, "failed": 0, "pending": 0, "skipped": 0})
        counts["total"] += 1
        status = str(item.get("status", "SKIPPED")).upper()
        if status == "PASS":
            counts["passed"] += 1
        elif status in {"PENDING", "BLOCKED"}:
            counts["pending"] += 1
        elif status == "SKIPPED":
            counts["skipped"] += 1
        else:
            counts["failed"] += 1
    for risk in ("P0", "P1", "P2"):
        buckets.setdefault(risk, {"total": 0, "passed": 0, "failed": 0, "pending": 0, "skipped": 0})
    return {risk: buckets[risk] for risk in ("P0", "P1", "P2")}


def _parameter_summary(items: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """汇总参数解析、复用和失效状态，供报告与 baseline 共用。

    [参数] items: 带 dependency_trace 的接口结果集合。
    [返回] 参数总数、来源计数、成功/失败计数和生命周期计数。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 取代固定 0 参数摘要并支持基线复用。
    """

    traces: list[Mapping[str, Any]] = []
    events: list[Mapping[str, Any]] = []
    for item in items:
        evidence = item.get("evidence", {})
        if not isinstance(evidence, Mapping):
            continue
        trace = evidence.get("dependency_trace", [])
        if isinstance(trace, list):
            traces.extend(entry for entry in trace if isinstance(entry, Mapping))
        reusable_events = evidence.get("reusable_param_events", [])
        if isinstance(reusable_events, list):
            events.extend(entry for entry in reusable_events if isinstance(entry, Mapping))
    source_counts: dict[str, int] = {}
    resolved = unresolved = 0
    lifecycle = {name: 0 for name in ("reused", "revalidated", "candidate", "stale", "invalid", "quarantined")}
    for trace in traces:
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


def _sync_summary(interface_map: Mapping[str, Mapping[str, Any]], metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    """生成三方接口索引同步元数据，未知来源时明确标为未配置。

    [参数] interface_map: 当前代码发现的接口；metadata: 可选 manifest/inventory 对账输入。
    [返回] 可写入 YAML/JSON 的同步摘要。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 防止用单一发现结果冒充三方已同步。
    """

    supplied = dict(metadata or {})
    current = sorted(interface_map)
    summary = {
        "code_interfaces": supplied.get("code_interfaces", current),
        "manifest_interfaces": supplied.get("manifest_interfaces", supplied.get("swag_interfaces", [])),
        "inventory_interfaces": supplied.get("inventory_interfaces", []),
        "drift": list(supplied.get("drift", [])),
        "missing_manifest": bool(supplied.get("missing_manifest", not bool(supplied.get("manifest_interfaces", supplied.get("swag_interfaces", []))))),
        "missing_inventory": bool(supplied.get("missing_inventory", not bool(supplied.get("inventory_interfaces", [])))),
        "status": str(supplied.get("status", "not_configured" if not metadata else "PENDING")),
        "contract_status": str(supplied.get("contract_status", supplied.get("status", "not_configured" if not metadata else "PENDING"))),
        "failure_types": list(supplied.get("failure_types", [])),
        "manifest_provenance": dict(supplied.get("manifest_provenance", {})),
        "inventory_provenance": dict(supplied.get("inventory_provenance", {})),
        "reusable_params_provenance": dict(supplied.get("reusable_params_provenance", {})),
        "missing_reusable_params": bool(supplied.get("missing_reusable_params", False)),
    }
    summary["code_count"] = len(summary["code_interfaces"])
    summary["manifest_count"] = len(summary["manifest_interfaces"])
    summary["inventory_count"] = len(summary["inventory_interfaces"])
    summary["schema_drift_count"] = len(summary["drift"])
    summary["requires_refresh"] = bool(summary["missing_manifest"] or summary["missing_inventory"] or summary["missing_reusable_params"] or summary["drift"] or summary["failure_types"] or summary["contract_status"] == "BLOCKED")
    return summary


def _runtime_matrix(items: Iterable[Mapping[str, Any]], interfaces: Mapping[str, Mapping[str, Any]], run_id: str, metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    """从真实判定结果生成逐入口 runtime 能力矩阵并保留失败分类。

    [参数] items: 判定结果；interfaces: 接口 IR 映射；run_id: 本轮执行标识；metadata: 严格开关元数据。
    [返回] 含统一 run_id 和逐入口生命周期状态的矩阵对象。
    最近修改时间: 2026-07-13 01:05:00 改动原因: 为缺 runtime 与 cleanup failure 提供可复核产物。
    """

    entries: list[dict[str, Any]] = []
    for item in items:
        operation_id = str(item.get("operation_id", ""))
        interface = interfaces.get(operation_id, {})
        protocol = str(interface.get("protocol", ""))
        evidence = item.get("evidence", {}) if isinstance(item.get("evidence", {}), Mapping) else {}
        capability = evidence.get("capability", {}) if isinstance(evidence.get("capability", {}), Mapping) else {}
        lifecycle = capability.get("lifecycle", {}) if isinstance(capability.get("lifecycle", {}), Mapping) else {}
        status = str(item.get("status", "PENDING"))
        default_execution = "ready" if status in {"PASS", "FAIL", "EXPECTED_FAIL"} else "pending"
        failure_type = str(item.get("failure_type", "") or "")
        entries.append({
            "operation_id": operation_id,
            "protocol": protocol,
            "run_id": run_id,
            "discovery_status": str(capability.get("discovery_status", "ready")),
            "fixture_status": str(capability.get("fixture_status", "not_required" if protocol in {"http", "cli"} else "unavailable")),
            "execution_status": str(capability.get("execution_status", default_execution)),
            "reason": str(item.get("reason", "") or evidence.get("reason", "") or capability.get("reason", "")),
            "failure_type": failure_type,
            "cleanup_status": str(evidence.get("cleanup_status", "not_required")),
            "capability_status": "ready" if default_execution == "ready" and failure_type == "" else "pending",
            "local_provenance": "local" if lifecycle.get("local_provenance") is True or protocol in {"http", "cli"} else "unknown",
        })
    supplied = dict(metadata or {})
    return {
        "schema_version": "2.0",
        "run_id": run_id,
        "strict_fixture": bool(supplied.get("strict_fixture", False)),
        "strict_contracts": bool(supplied.get("strict_contracts", False)),
        "entries": entries,
    }


def _sanitize_result(item: Mapping[str, Any]) -> dict[str, Any]:
    """为 baseline 事件固定请求/响应字符串并再次脱敏。

    [参数] item: 单接口判定结果。
    [返回] 可安全写入事件 payload 的结果对象。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 防止直接调用投影函数时泄漏 JSON 字符串凭据。
    """

    result = _redact(dict(item))
    result["request"] = _json_contract(item.get("request", {}))
    result["response"] = _response_contract(item.get("response", {}))
    result["dataPreview"] = _response_summary(item.get("response", {})).get("dataPreview")
    return result


def _validate_execution_event(event: Mapping[str, Any]) -> None:
    """校验 execution.completed 事件的最小可重放契约。

    [参数] event: 待追加的事件字典。
    [返回] 无；契约不满足时抛出 ValueError。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 阻止不完整事件污染长期基线。
    """

    baseline_event = BaselineEvent.from_dict(event)
    if baseline_event.event_type != "execution.completed":
        raise ValueError("event_type must be execution.completed")
    try:
        datetime.fromisoformat(baseline_event.occurred_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("occurred_at must be ISO-8601") from exc
    payload = baseline_event.payload
    for field in ("gate", "interfaces", "dependency_graph", "results"):
        if field not in payload:
            raise ValueError(f"event payload missing {field}")
    if not isinstance(payload["gate"], Mapping) or not isinstance(payload["interfaces"], list) or not isinstance(payload["results"], list):
        raise ValueError("event payload has invalid execution field types")


def _validate_projection(document: Mapping[str, Any]) -> None:
    """校验 baseline 投影具备最新门禁、清单、图、场景和事件历史。

    [参数] document: 原子写入前的基线文档。
    [返回] 无；字段缺失或类型错误时抛出 ValueError。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 保证事件回放结果可被下次执行复用。
    """

    required = ("schema_version", "latest_gate", "interface_inventory", "dependency_graph", "scenarios", "events")
    missing = [field for field in required if field not in document]
    if missing:
        raise ValueError("baseline projection missing " + ", ".join(missing))
    if str(document["schema_version"]) != "2.0" or not isinstance(document["latest_gate"], Mapping) or not isinstance(document["interface_inventory"], list) or not isinstance(document["dependency_graph"], Mapping) or not isinstance(document["scenarios"], list) or not isinstance(document["events"], list):
        raise ValueError("baseline projection has invalid field types")


def _report_item(item: Mapping[str, Any]) -> dict[str, Any]:
    """生成报告明细，保留判定字段并固定请求/响应字段类型。

    [参数] item: 单接口判定结果。
    [返回] 脱敏后的报告明细，响应包含 ``dataPreview``。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 将业务响应预览纳入稳定 JSON 契约。
    """

    result = _redact(dict(item))
    result["request"] = _json_contract(item.get("request", {}))
    result["response"] = _response_contract(item.get("response", {}))
    result["dataPreview"] = _response_summary(item.get("response", {})).get("dataPreview")
    return result


def _safe_name(value: Any) -> str:
    """将接口标识转换为稳定的归档文件名。

    [参数] value: 接口标识。
    [返回] 仅包含 ASCII 安全字符的文件名片段。
    最近修改时间: 2026-07-12 18:30 改动原因: 支持每接口证据归档。
    """

    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value or "unknown"))
    return name.strip("._") or "unknown"


def _parse_jsonish(value: Any) -> Any:
    """解析报告中的 JSON 字符串，失败时保留原始值。

    [参数] value: 任意请求或响应证据。
    [返回] 可序列化的结构化值。
    最近修改时间: 2026-07-12 18:30 改动原因: 统一证据文件格式。
    """

    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return {"raw": value}
    return value


def _yaml_dump(value: Any) -> str:
    """以 UTF-8 输出 YAML，缺少 PyYAML 时退化为合法 JSON。

    [参数] value: 待归档对象。
    [返回] YAML 或 JSON 文本。
    最近修改时间: 2026-07-12 18:30 改动原因: 生成规范归档骨架。
    """

    try:
        import yaml
        return yaml.safe_dump(value, allow_unicode=True, sort_keys=False)
    except ImportError:
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def _interface_fields(interface: Mapping[str, Any] | None, item: Mapping[str, Any], index: int) -> dict[str, str]:
    """从接口 IR 和判定结果提取块状报告字段。

    [参数] interface: 接口 IR 字典；item: 判定结果；index: 接口序号。
    [返回] 标准报告字段映射。
    最近修改时间: 2026-07-12 18:30 改动原因: 对齐 report-format 块状字段。
    """

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
        "reason": str(item.get("reason", "")),
        "risk": str(interface.get("risk", "P2")),
        "source": ", ".join(str(e.get("source", e.get("type", ""))) for e in interface.get("evidence", []) if isinstance(e, Mapping)) or str(interface.get("adapter", "unknown")),
        "parameter_source": source,
        "allow_release": "否" if status != "PASS" else "是",
    }


def _write_text(path: Path, value: str) -> str:
    """创建父目录并以 UTF-8 写入文本。

    [参数] path: 输出路径；value: 文本内容。
    [返回] 输出文件绝对路径字符串。
    最近修改时间: 2026-07-12 18:30 改动原因: 统一归档写入行为。
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")
    return str(path)


def write_report(
    output_dir: str | Path,
    results: Iterable[Mapping[str, Any]],
    gate: Mapping[str, Any],
    *,
    run_id: str = "",
    interfaces: Iterable[Mapping[str, Any]] = (),
    dependency_graph: Mapping[str, Any] | None = None,
    environment: str = "local",
    canonical_layout: bool = False,
    parameter_summary: Mapping[str, Any] | None = None,
    sync_metadata: Mapping[str, Any] | None = None,
    baseline_summary: Mapping[str, Any] | None = None,
    runtime_matrix: Mapping[str, Any] | None = None,
) -> dict[str, str]:
    """生成中文主报告、ASCII 镜像和逐接口证据。

    [参数] output_dir: 归档根目录；results: 判定结果；gate: 门禁结论；其余为接口、依赖和环境元数据。
    [返回] 关键归档文件路径映射。
    最近修改时间: 2026-07-12 21:10:00 改动原因: 补齐风险、参数、同步元数据和响应预览产物。
    """

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    items = [dict(item) for item in results]
    interface_map = {str(item.get("operation_id", "")): dict(item) for item in interfaces}
    artifact_root = root / "ascii-artifacts" if canonical_layout else root
    artifact_root.mkdir(parents=True, exist_ok=True)
    report_items = [_report_item(item) for item in items]
    interface_data = {str(item.get("operation_id", "")): dict(item) for item in interfaces}
    risks = _risk_statistics(items, interface_data)
    parameters = dict(parameter_summary or _parameter_summary(items))
    sync = _sync_summary(interface_data, sync_metadata)
    runtime = _runtime_matrix(items, interface_data, run_id, runtime_matrix)
    generated_at = utc_now()
    payload = {
        "schema_version": "2.0",
        "run_id": run_id,
        "generated_at": generated_at,
        "environment": environment,
        "gate": dict(gate),
        "risk_statistics": risks,
        "parameter_summary": parameters,
        "sync_metadata": sync,
        "runtime_matrix": runtime,
        "results": report_items,
    }
    json_path = Path(_write_text(artifact_root / "release-test-report.json", json.dumps(payload, ensure_ascii=False, indent=2)))
    markdown: list[str] = ["# 接口测试明细", ""]
    for index, item in enumerate(items, 1):
        interface = interface_map.get(str(item.get("operation_id", "")), {})
        fields = _interface_fields(interface, item, index)
        operation = fields["operation_id"]
        trace_path = f"artifacts/dependency-trace/{_safe_name(operation)}.json"
        request = _json_contract(item.get("request", {}))
        response = _response_contract(item.get("response", {}))
        markdown.extend([
            f"【接口 {index}】",
            f"接口            {fields['endpoint']}",
            f"接口名称        {fields['name']}",
            f"接口标识        {operation}",
            f"请求参数        {request}",
            f"参数来源        {fields['parameter_source']}",
            f"依赖追踪        {trace_path if item.get('evidence', {}).get('dependency_trace') else '无'}",
            f"简要响应        {response}",
            f"Agent 判定      {fields['verdict']}",
            f"阻断分类        {fields['block']}",
            f"判定理由        {fields['reason']}",
            f"风险等级        {fields['risk']}",
            f"发现来源        {fields['source']}",
            f"是否阻断上线    {'是' if fields['allow_release'] == '否' else '否'}",
            "",
        ])
    md_path = Path(_write_text(artifact_root / "interface-test-results.md", "\n".join(markdown)))
    evidence_path = artifact_root / "responses.json"
    responses = []
    for item in items:
        responses.append(_redact(_parse_jsonish(item.get("response", {}))))
    _write_text(evidence_path, json.dumps(responses, ensure_ascii=False, indent=2))
    graph = dict(dependency_graph or {})
    _write_text(artifact_root / "dependency-graph.json", json.dumps(graph, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "scenario-results.json", json.dumps(report_items, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "interface-sync-report.yaml", _yaml_dump(sync))
    _write_text(artifact_root / "runtime-matrix.yaml", _yaml_dump(runtime))
    _write_text(artifact_root / "inventory-reconcile.yaml", _yaml_dump({"run_id": run_id, "added": [], "deleted": [], "changed": [], "pending": sync.get("drift", []), "status": sync.get("status", "not_configured")}))
    _write_text(artifact_root / "release-test-plan.yaml", _yaml_dump({"schema_version": "2.0", "environment": environment, "run_id": run_id, "generated_at": generated_at, "interface_count": len(items), "risk_statistics": risks, "parameter_summary": parameters}))
    _write_text(artifact_root / "artifacts" / "dependency-trace.json", json.dumps([item.get("evidence", {}).get("dependency_trace", []) for item in items], ensure_ascii=False, indent=2))
    for item in items:
        operation = _safe_name(item.get("operation_id", "unknown"))
        request = _redact(_parse_jsonish(item.get("request", {})))
        response = _redact(_parse_jsonish(item.get("response", {})))
        trace = item.get("evidence", {}).get("dependency_trace", []) if isinstance(item.get("evidence", {}), Mapping) else []
        _write_text(artifact_root / "artifacts" / "raw-request" / f"{operation}.json", json.dumps(request, ensure_ascii=False, indent=2))
        _write_text(artifact_root / "artifacts" / "raw-response" / f"{operation}.json", json.dumps(response, ensure_ascii=False, indent=2))
        _write_text(artifact_root / "artifacts" / "masked-response" / f"{operation}.json", json.dumps(_redact(response), ensure_ascii=False, indent=2))
        _write_text(artifact_root / "artifacts" / "resolved-params" / f"{operation}.json", json.dumps(request, ensure_ascii=False, indent=2))
        _write_text(artifact_root / "artifacts" / "dependency-trace" / f"{operation}.json", json.dumps(trace, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "artifacts" / "reusable-param-events.yaml", _yaml_dump({"schema_version": "2.0", "run_id": run_id, "events": parameters.get("events", [])}))
    baseline_info = dict(baseline_summary or {})
    baseline_info.update({"schema_version": "2.0", "run_id": run_id, "event_id": f"run-{run_id}", "event_type": "execution.completed", "parameter_summary": parameters, "risk_statistics": risks})
    baseline_info.setdefault("updated", False)
    baseline_info.setdefault("projection_status", "not_requested")
    baseline_info.setdefault("path", "doc/5-tests/基线/")
    _write_text(artifact_root / "artifacts" / "baseline-update-summary.yaml", _yaml_dump(baseline_info))
    _write_text(artifact_root / "artifacts" / "logs" / "execute.log", "run_id: " + run_id + "\n")
    passed = int(gate.get("passed", 0))
    failed = int(gate.get("failed", 0))
    pending = int(gate.get("pending", 0))
    blocked_lines = [f"- {item.get('operation_id', 'unknown')}：{item.get('reason', '')}" for item in items if item.get("status") != "PASS"] or ["- 无"]
    status_counts = _status_counts(items)
    readme = [
        "# 上线前项目接口测试报告", "", "## 基本信息",
        f"- 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"- 测试环境：{environment} 本地环境",
        "- 测试范围：当前项目扫描到的全部接口", f"- 接口总数：{len(items)}", f"- 必测接口数：{len(items)}", "- 可选测接口数：0", "- 跳过接口数：0", f"- 通过接口数：{passed}", f"- 不通过接口数：{failed}", f"- 待确认接口数：{pending}",
        "", "## 风险等级统计",
        *[f"- {risk} 级接口：总数 {values['total']}，通过 {values['passed']}，不通过 {values['failed']}，待确认 {values['pending']}，跳过 {values['skipped']}" for risk, values in risks.items()],
        "", "## 接口基线扫描摘要", "- 扫描模式：全量建基线 / 增量扫描", f"- 扫描时间：{generated_at}", f"- 扫描接口数：{len(interface_map)}", "- 新增/删除/变更接口数：0 / 0 / 0",
        "", "## 对账结果", f"- 当前代码接口数：{sync['code_count']}", f"- swag manifest 接口数：{sync['manifest_count']}", f"- interface inventory 接口数：{sync['inventory_count']}", f"- 缺失 manifest：{'是' if sync['missing_manifest'] else '否'}", f"- 缺失 inventory：{'是' if sync['missing_inventory'] else '否'}", f"- schema 漂移接口数：{sync['schema_drift_count']}", "- 详见：ascii-artifacts/interface-sync-report.yaml",
        "", "## Runtime 能力矩阵", "- 详见：runtime-matrix.yaml",
        "", "## 最终门禁结论", f"### 结论等级：{gate.get('gate', 'PENDING')}", f"- 是否允许上线：{'是' if gate.get('allow_release') else '否'}",
        "", "## 阻断项列表", *blocked_lines,
        "", "## 参数复用与失效摘要", f"- 本轮参数总数：{parameters.get('total', 0)}", f"- 已解析参数数：{parameters.get('resolved', 0)}", f"- 未解析参数数：{parameters.get('unresolved', 0)}", f"- 本轮复用参数数：{parameters.get('reused', 0)}", f"- 复验成功参数数：{parameters.get('revalidated', 0)}", f"- 新增 candidate 参数数：{parameters.get('candidate', 0)}", f"- 标记 stale 参数数：{parameters.get('stale', 0)}", f"- 标记 invalid 参数数：{parameters.get('invalid', 0)}", f"- 标记 quarantined 参数数：{parameters.get('quarantined', 0)}", f"- 状态计数：{json.dumps(status_counts, ensure_ascii=False, sort_keys=True)}",
    ]
    readme_path = Path(_write_text(root / "README.md", "\n".join(readme) + "\n"))
    if not canonical_layout:
        # 兼容已有自定义 output_dir 调用方的平铺文件契约。
        _write_text(root / "release-test-report.json", json.dumps(payload, ensure_ascii=False, indent=2))
        _write_text(root / "interface-test-results.md", "\n".join(markdown))
        _write_text(root / "responses.json", json.dumps(responses, ensure_ascii=False, indent=2))
    return {"report": str(md_path), "json": str(json_path), "responses": str(evidence_path), "readme": str(readme_path), "runtime_matrix": str(artifact_root / "runtime-matrix.yaml"), "artifact_root": str(artifact_root)}


def project_execution_to_baseline(
    baseline_path: str | Path,
    run_id: str,
    gate: Mapping[str, Any],
    *,
    interfaces: Iterable[Mapping[str, Any]] = (),
    dependency_graph: Mapping[str, Any] | None = None,
    results: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """将接口、参数/依赖、场景结果和门禁作为一次原子 execution 事件投影。

    [参数] baseline_path/run_id/gate/interfaces/dependency_graph/results: 基线位置、执行标识、门禁和执行证据。
    [返回] 原子投影后的 v2 基线文档。
    最近修改时间: 2026-07-12 22:05:00 改动原因: 强制事件与投影契约校验并保持响应脱敏字符串。
    """

    # 1. 先把响应固定为脱敏 JSON 字符串，防止原始对象污染长期事件。
    store = BaselineStore(baseline_path)
    sanitized_results = [_sanitize_result(item) for item in results]
    payload = {
        "gate": _redact(dict(gate)),
        "interfaces": [_redact(dict(item)) for item in interfaces],
        "dependency_graph": _redact(dict(dependency_graph or {})),
        "results": sanitized_results,
    }
    # 2. 事件追加前校验最小契约，避免不完整执行结果进入 baseline。
    event = {"schema_version": "2.0", "event_id": f"run-{run_id}", "run_id": run_id, "event_type": "execution.completed", "occurred_at": utc_now(), "payload": payload}
    _validate_execution_event(event)
    store.append_event(event)

    def projector(document: dict[str, Any], current: Any) -> dict[str, Any]:
        projected = dict(document)
        projected["schema_version"] = "2.0"
        projected["latest_gate"] = dict(current.payload.get("gate", {}))
        projected["interface_inventory"] = list(current.payload.get("interfaces", []))
        projected["dependency_graph"] = dict(current.payload.get("dependency_graph", {}))
        projected["scenarios"] = list(current.payload.get("results", []))
        history = projected.setdefault("events", [])
        if not any(item.get("event_id") == current.event_id for item in history if isinstance(item, dict)):
            history.append(current.to_dict())
        return projected

    # 3. 原子投影完成后再次校验字段，确保下次执行能够 replay。
    projected = store.project(projector)
    _validate_projection(projected)
    return projected
