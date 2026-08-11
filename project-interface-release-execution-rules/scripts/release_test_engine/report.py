"""上线测试报告、脱敏证据和基线投影。"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from .events import BaselineEvent, utc_now
from .report_support import (
    ensure_report_output_path as _ensure_report_output_path,
    interface_fields as _interface_fields,
    parameter_summary as _parameter_summary,
    parse_jsonish as _parse_jsonish,
    redact_evidence as _redact,
    risk_statistics as _risk_statistics,
    safe_name as _safe_name,
    sensitive_evidence_values as _sensitive_evidence_values,
    status_counts as _status_counts,
    write_text as _write_text,
    yaml_dump as _yaml_dump,
)
from .scenario_report import (
    cleanup_summary as _cleanup_summary,
    evidence_gate as _evidence_gate,
    external_asset as _external_asset,
    normalize_scenario_result as _scenario_report_item,
    scenario_status_summary as _scenario_status_summary,
    write_evidence_manifest,
)
from .storage import BaselineStore


def _relative_hint(target: Path, base: Path) -> str:
    """计算中文主报告指向机器产物根的可点击前缀。

    [参数] target: 机器产物根目录；base: 中文主报告所在目录。
    [返回] str：以 `/` 分隔并以 `/` 结尾的相对前缀，同目录返回空串；跨盘无法相对化时回落绝对 POSIX 路径。
    最近修改时间：2026-08-11；改动原因：主报告与机器产物分根后需要稳定的跨目录指引。
    """
    # 1. 同目录时不加前缀，保持旧报告里 `runtime-matrix.yaml` 这类裸文件名的写法。
    if target.resolve() == base.resolve():
        return ""
    # 2. Windows 跨盘符无法相对化，此时直接给绝对路径而不是抛错中断报告生成。
    try:
        relative = Path(os.path.relpath(target.resolve(), base.resolve()))
    except ValueError:
        return target.resolve().as_posix().rstrip("/") + "/"
    return relative.as_posix().rstrip("/") + "/"


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


def write_report(
    output_dir: str | Path,
    results: Iterable[Mapping[str, Any]],
    gate: Mapping[str, Any],
    *,
    run_id: str = "",
    interfaces: Iterable[Mapping[str, Any]] = (),
    dependency_graph: Mapping[str, Any] | None = None,
    environment: str = "local",
    doc_report_path: str | Path | None = None,
    parameter_summary: Mapping[str, Any] | None = None,
    sync_metadata: Mapping[str, Any] | None = None,
    baseline_summary: Mapping[str, Any] | None = None,
    runtime_matrix: Mapping[str, Any] | None = None,
    scenario_results: Iterable[Mapping[str, Any]] = (),
    consumer_coverage: Mapping[str, Any] | None = None,
    protocol_capabilities: Mapping[str, Any] | None = None,
    cleanup_report: Mapping[str, Any] | None = None,
    dual_gate_diff: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """生成兼容接口报告、独立场景报告和脱敏证据清单。

    [参数] output_dir: 机器产物归档根目录；doc_report_path: 中文主报告 md 落点，缺省时回落到产物根内的 README.md；results: 接口判定结果；gate: 接口门禁；scenario_results: 真实场景结果；其余为接口、依赖和外部场景资产。
    [返回] 关键归档文件路径映射。
    最近修改时间：2026-08-11，机器产物移出 doc/ 并与中文主报告 md 分离归档。
    """

    # 1. 所有调用方输入先生成脱敏副本，后续统计、渲染和归档禁止再读取原始对象。
    root = Path(output_dir)
    _ensure_report_output_path(root)
    root.mkdir(parents=True, exist_ok=True)
    raw_items = [dict(item) for item in results]
    raw_interfaces = [dict(item) for item in interfaces]
    raw_scenario_items = [dict(item) for item in scenario_results]
    sensitive_values = _sensitive_evidence_values({
        # 1.1 三类核心运行输入共同参与敏感原值提取，防止接口与场景边界漏扫。
        "results": raw_items,
        "interfaces": raw_interfaces,
        "scenario_results": raw_scenario_items,
        "gate": gate,
        "dependency_graph": dependency_graph,
        # 1.2 附属报告输入按字段组加入扫描，原值仅在当前调用内存中存在。
        "parameter_summary": parameter_summary,
        "sync_metadata": sync_metadata,
        "baseline_summary": baseline_summary,
        "runtime_matrix": runtime_matrix,
        "consumer_coverage": consumer_coverage,
        "protocol_capabilities": protocol_capabilities,
        "cleanup_report": cleanup_report,
        "dual_gate_diff": dual_gate_diff,
    })
    items = [dict(_redact(item)) for item in raw_items]
    interface_map = {str(item.get("operation_id", "")): dict(_redact(item)) for item in raw_interfaces}
    gate = dict(_redact(dict(gate)))
    dependency_graph = _redact(dependency_graph) if dependency_graph else None
    baseline_summary = _redact(baseline_summary) if baseline_summary else None
    # 1.4 机器产物直接落在传入的产物根，不再嵌一层 ascii-artifacts。
    artifact_root = root
    # 1.5 中文主报告默认留在产物根，调用方给出 doc 落点时改写到 doc/5-tests/ 的扁平 md。
    report_path = Path(doc_report_path) if doc_report_path else artifact_root / "README.md"
    _ensure_report_output_path(report_path.parent)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_items = [_report_item(item) for item in items]
    # 1.3 接口与场景分别归档；旧调用方不传场景时只得到明确的未配置集合。
    scenario_items = [_scenario_report_item(_redact(item)) for item in raw_scenario_items]
    interface_data = dict(interface_map)
    risks = _risk_statistics(items, interface_data)
    parameters = dict(_redact(parameter_summary or _parameter_summary(items)))
    sync = _sync_summary(interface_data, _redact(sync_metadata) if sync_metadata else None)
    runtime = _runtime_matrix(items, interface_data, run_id, _redact(runtime_matrix) if runtime_matrix else None)
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
    interface_payload = {
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
    coverage = _scenario_status_summary(scenario_items, run_id, _redact(consumer_coverage) if consumer_coverage else None)
    cleanup = _cleanup_summary(scenario_items, run_id, _redact(cleanup_report) if cleanup_report else None)
    capabilities = _external_asset(_redact(protocol_capabilities) if protocol_capabilities else None, name="protocol-capabilities", run_id=run_id)
    gate_diff = _external_asset(_redact(dual_gate_diff) if dual_gate_diff else None, name="dual-gate-diff", run_id=run_id)
    scenario_status = coverage["status"] if scenario_items else "not_configured"
    # 2. 兼容报告继续使用接口结果，新文件不再让接口结果冒充场景结果。
    json_path = Path(_write_text(artifact_root / "release-test-report.json", json.dumps(payload, ensure_ascii=False, indent=2)))
    interface_results_path = Path(_write_text(artifact_root / "interface-results.json", json.dumps(interface_payload, ensure_ascii=False, indent=2)))
    # 3. 人工可读明细只渲染脱敏字段，失败原因已收敛为安全机器码或通用摘要。
    markdown: list[str] = ["# 接口测试明细", ""]
    for index, item in enumerate(items, 1):
        # 3.1 每个接口沿用固定块状字段顺序，便于人工与机器消费者稳定读取。
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
    # 4. 项目级依赖、场景、能力和双轨资产使用同一运行身份集中归档。
    graph = dict(dependency_graph or {})
    _write_text(artifact_root / "dependency-graph.json", json.dumps(graph, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "scenario-results.json", json.dumps({"schema_version": "external-scenario/1.0", "run_id": run_id, "status": scenario_status, "results": scenario_items}, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "consumer-coverage.json", json.dumps(coverage, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "protocol-capabilities.json", json.dumps(capabilities, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "cleanup-report.json", json.dumps(cleanup, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "dual-gate-diff.json", json.dumps(gate_diff, ensure_ascii=False, indent=2))
    _write_text(artifact_root / "interface-sync-report.yaml", _yaml_dump(sync))
    _write_text(artifact_root / "runtime-matrix.yaml", _yaml_dump(runtime))
    _write_text(artifact_root / "inventory-reconcile.yaml", _yaml_dump({"run_id": run_id, "added": [], "deleted": [], "changed": [], "pending": sync.get("drift", []), "status": sync.get("status", "not_configured")}))
    _write_text(artifact_root / "release-test-plan.yaml", _yaml_dump({"schema_version": "2.0", "environment": environment, "run_id": run_id, "generated_at": generated_at, "interface_count": len(items), "risk_statistics": risks, "parameter_summary": parameters}))
    _write_text(artifact_root / "artifacts" / "dependency-trace.json", json.dumps([item.get("evidence", {}).get("dependency_trace", []) for item in items], ensure_ascii=False, indent=2))
    # 5. 逐接口证据继续保留兼容目录结构，但原始命名只表示目录角色，内容已经脱敏。
    for item in items:
        # 5.1 请求、响应、参数和依赖追踪分别写入兼容位置，内容只来自安全副本。
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
    # 6. 最后生成基线摘要和发布结论 README，阻断列表只引用已脱敏接口结果。
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
    # 6.1 中文主报告与机器产物可能不同根，指引统一按主报告所在目录换算相对路径。
    artifact_hint = _relative_hint(artifact_root, report_path.parent)
    readme = [
        "# 上线前项目接口测试报告", "", "## 基本信息",
        f"- 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"- 测试环境：{environment} 本地环境",
        "- 测试范围：当前项目扫描到的全部接口", f"- 接口总数：{len(items)}", f"- 必测接口数：{len(items)}", "- 可选测接口数：0", "- 跳过接口数：0", f"- 通过接口数：{passed}", f"- 不通过接口数：{failed}", f"- 待确认接口数：{pending}",
        "", "## 风险等级统计",
        *[f"- {risk} 级接口：总数 {values['total']}，通过 {values['passed']}，不通过 {values['failed']}，待确认 {values['pending']}，跳过 {values['skipped']}" for risk, values in risks.items()],
        "", "## 接口基线扫描摘要", "- 扫描模式：全量建基线 / 增量扫描", f"- 扫描时间：{generated_at}", f"- 扫描接口数：{len(interface_map)}", "- 新增/删除/变更接口数：0 / 0 / 0",
        "", "## 对账结果", f"- 当前代码接口数：{sync['code_count']}", f"- swag manifest 接口数：{sync['manifest_count']}", f"- interface inventory 接口数：{sync['inventory_count']}", f"- 缺失 manifest：{'是' if sync['missing_manifest'] else '否'}", f"- 缺失 inventory：{'是' if sync['missing_inventory'] else '否'}", f"- schema 漂移接口数：{sync['schema_drift_count']}", f"- 详见：{artifact_hint}interface-sync-report.yaml",
        "", "## Runtime 能力矩阵", f"- 详见：{artifact_hint}runtime-matrix.yaml",
        "", "## 最终门禁结论", f"### 结论等级：{gate.get('gate', 'PENDING')}", f"- 是否允许上线：{'是' if gate.get('allow_release') else '否'}",
        "", "## 阻断项列表", *blocked_lines,
        "", "## 参数复用与失效摘要", f"- 本轮参数总数：{parameters.get('total', 0)}", f"- 已解析参数数：{parameters.get('resolved', 0)}", f"- 未解析参数数：{parameters.get('unresolved', 0)}", f"- 本轮复用参数数：{parameters.get('reused', 0)}", f"- 复验成功参数数：{parameters.get('revalidated', 0)}", f"- 新增 candidate 参数数：{parameters.get('candidate', 0)}", f"- 标记 stale 参数数：{parameters.get('stale', 0)}", f"- 标记 invalid 参数数：{parameters.get('invalid', 0)}", f"- 标记 quarantined 参数数：{parameters.get('quarantined', 0)}", f"- 状态计数：{json.dumps(status_counts, ensure_ascii=False, sort_keys=True)}",
    ]
    readme_path = Path(_write_text(report_path, "\n".join(readme) + "\n"))
    # 7. 清单只记录相对路径、摘要哈希和脱敏状态，不把原始请求响应复制进索引。
    additional_files = [("doc-report.md", readme_path)] if doc_report_path else []
    evidence_path = Path(write_evidence_manifest(artifact_root, run_id, sensitive_values=sensitive_values, additional_files=additional_files))
    evidence_status = str(json.loads(evidence_path.read_text(encoding="utf-8"))["status"])
    final_gate = _evidence_gate(gate, evidence_status)
    if final_gate != gate:
        # 7.1 清单非 PASS 时重写所有门禁摘要，再重算哈希，禁止 JSON/README 继续声称可放行。
        gate = final_gate
        payload["gate"] = dict(gate)
        interface_payload["gate"] = dict(gate)
        _write_text(json_path, json.dumps(payload, ensure_ascii=False, indent=2))
        _write_text(interface_results_path, json.dumps(interface_payload, ensure_ascii=False, indent=2))
        readme = [f"### 结论等级：{gate.get('gate', 'PENDING')}" if line.startswith("### 结论等级：") else f"- 是否允许上线：{'是' if gate.get('allow_release') else '否'}" if line.startswith("- 是否允许上线：") else line for line in readme]
        _write_text(readme_path, "\n".join(readme) + "\n")
        evidence_path = Path(write_evidence_manifest(artifact_root, run_id, sensitive_values=sensitive_values, additional_files=additional_files))
    return {"report": str(md_path), "json": str(json_path), "interface_results": str(interface_results_path), "scenario_results": str(artifact_root / "scenario-results.json"), "consumer_coverage": str(artifact_root / "consumer-coverage.json"), "protocol_capabilities": str(artifact_root / "protocol-capabilities.json"), "cleanup_report": str(artifact_root / "cleanup-report.json"), "dual_gate_diff": str(artifact_root / "dual-gate-diff.json"), "evidence_manifest": str(evidence_path), "evidence_manifest_status": evidence_status, "gate": gate, "responses": str(artifact_root / "responses.json"), "readme": str(readme_path), "runtime_matrix": str(artifact_root / "runtime-matrix.yaml"), "artifact_root": str(artifact_root)}


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
