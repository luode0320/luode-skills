"""消费者场景报告、清理摘要和脱敏证据清单。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from .report_support import ensure_report_output_path, write_text


def normalize_scenario_result(item: Mapping[str, Any]) -> dict[str, Any]:
    """规范已脱敏的真实消费者场景结果，并固定单步事件字段。

    [参数] item: 已完成递归脱敏的场景 runner 结果。
    [返回] 可归档的场景结果，包含真实 run_id、scenario_id 和步骤事件。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从接口报告模块拆出场景结果边界。
    """

    # 1. 场景结果保持声明顺序，步骤缺字段时补为可审计的显式空值。
    result = dict(item)
    steps = result.get("steps", [])
    normalized_steps: list[dict[str, Any]] = []
    if isinstance(steps, list):
        # 1.1 不按状态或标识重排，避免报告改变事件因果关系。
        for step in steps:
            # 1.2 每个合法步骤固定七个事件字段，其余已脱敏输出原样保留。
            if not isinstance(step, Mapping):
                continue
            normalized = dict(step)
            normalized_steps.append({
                # 1.3 运行、场景、步骤和动作共同标识一条事件。
                "run_id": str(normalized.get("run_id", result.get("run_id", ""))),
                "scenario_id": str(normalized.get("scenario_id", result.get("scenario_id", ""))),
                "step_id": str(normalized.get("step_id", "")),
                "action": str(normalized.get("action", "")),
                # 1.4 状态、耗时和失败类型构成固定事件结果字段组。
                "status": str(normalized.get("status", "PENDING")),
                "duration_ms": int(normalized.get("duration_ms", 0) or 0),
                "failure_type": str(normalized.get("failure_type", "") or ""),
                **{key: value for key, value in normalized.items() if key not in {"run_id", "scenario_id", "step_id", "action", "status", "duration_ms", "failure_type"}},
            })
    result["steps"] = normalized_steps
    result["cleanup"] = result.get("cleanup", [])
    return result


def scenario_status_summary(items: Iterable[Mapping[str, Any]], run_id: str, supplied: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """汇总场景状态、风险和消费者覆盖。

    [参数] items: 已脱敏真实场景结果；run_id: 本轮执行标识；supplied: 已脱敏覆盖摘要。
    [返回] 消费者覆盖报告。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从接口报告模块拆出场景覆盖统计。
    """

    # 1. 每个场景只贡献一次风险、状态和消费者计数。
    scenarios = [dict(item) for item in items]
    counts = {status: 0 for status in ("PASS", "FAIL", "BLOCKED", "PENDING")}
    risks: dict[str, dict[str, int]] = {}
    consumers: dict[str, dict[str, int]] = {}
    for item in scenarios:
        # 1.1 每个场景同时累计总状态、风险桶和消费者覆盖。
        status = str(item.get("status", "PENDING")).upper()
        counts[status if status in counts else "PENDING"] += 1
        risk = str(item.get("risk", "P2")).upper()
        risk_bucket = risks.setdefault(risk, {"total": 0, "passed": 0, "failed": 0, "pending": 0})
        risk_bucket["total"] += 1
        if status == "PASS":
            # 1.2 风险桶把 PASS、FAIL 和待确认状态互斥累计。
            risk_bucket["passed"] += 1
        elif status == "FAIL":
            risk_bucket["failed"] += 1
        else:
            risk_bucket["pending"] += 1
        for consumer in item.get("consumers", []) if isinstance(item.get("consumers", []), list) else []:
            # 1.3 消费者覆盖只按当前场景贡献一次总数和通过数。
            bucket = consumers.setdefault(str(consumer), {"total": 0, "passed": 0})
            bucket["total"] += 1
            bucket["passed"] += int(status == "PASS")
    # 2. 阻断优先级固定高于失败和待验证，空集合保持未配置。
    statuses = {str(item.get("status", "PENDING")).upper() for item in scenarios}
    if not scenarios:
        # 2.1 空输入保持未配置，其余按 BLOCKED、FAIL、PENDING、PASS 优先级派生。
        derived_status = "not_configured"
    elif "BLOCKED" in statuses:
        # 2.2 任一清理或环境阻断优先于业务失败和待验证。
        derived_status = "BLOCKED"
    elif "FAIL" in statuses:
        # 2.3 无阻断时，断言失败优先于待验证状态。
        derived_status = "FAIL"
    elif "PENDING" in statuses:
        # 2.4 仅剩待验证时保持 PENDING，全部通过才进入 PASS。
        derived_status = "PENDING"
    else:
        derived_status = "PASS"
    # 3. 固定输出版本、运行身份、状态计数、风险和消费者五组字段。
    summary = {
        # 3.1 版本与运行身份字段组。
        "schema_version": "external-scenario/1.0",
        "run_id": run_id,
        "status": derived_status,
        # 3.2 总量和四类状态计数字段组。
        "total": len(scenarios),
        "passed": counts["PASS"],
        "failed": counts["FAIL"],
        "blocked": counts["BLOCKED"],
        "pending": counts["PENDING"],
        # 3.3 风险和消费者覆盖明细字段组。
        "risks": risks,
        "consumers": consumers,
    }
    if supplied:
        summary.update(dict(supplied))
        summary["run_id"] = run_id
        summary["status"] = derived_status
    return summary


def cleanup_summary(items: Iterable[Mapping[str, Any]], run_id: str, supplied: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """从已脱敏场景结果汇总清理证据并显式标记清理缺口。

    [参数] items: 场景结果；run_id: 本轮执行标识；supplied: 已脱敏清理摘要。
    [返回] 清理步骤数量、状态和逐场景证据。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从接口报告模块拆出清理门禁摘要。
    """

    # 1. 清理状态只来自 runner 记录，缺失记录不能被推断为执行成功。
    scenarios = [dict(item) for item in items]
    reports: list[dict[str, Any]] = []
    total = passed = failed = 0
    for item in scenarios:
        # 1.1 每个场景保留自身状态和全部已脱敏清理步骤。
        cleanup = item.get("cleanup", [])
        if not isinstance(cleanup, list):
            cleanup = []
        reports.append({"scenario_id": item.get("scenario_id", ""), "status": item.get("status", "PENDING"), "steps": cleanup})
        for step in cleanup:
            # 1.2 每条清理证据只按显式 PASS 或失败累计，不推断缺失状态。
            if not isinstance(step, Mapping):
                continue
            total += 1
            if str(step.get("status", "")).upper() == "PASS":
                passed += 1
            else:
                failed += 1
    # 2. 清理摘要固定输出身份、派生状态、步骤计数和逐场景报告。
    summary = {
        # 2.1 版本、运行身份和派生状态字段组。
        "schema_version": "external-scenario/1.0",
        "run_id": run_id,
        "status": "not_configured" if not scenarios and not supplied else ("PASS" if failed == 0 else "BLOCKED"),
        # 2.2 清理步骤计数和逐场景明细字段组。
        "total_steps": total,
        "passed_steps": passed,
        "failed_steps": failed,
        "scenarios": reports,
    }
    # 2. 调用方摘要只能补字段，不能覆盖真实清理状态。
    derived_status = summary["status"]
    if supplied:
        summary.update(dict(supplied))
        summary["run_id"] = run_id
        summary["status"] = derived_status if scenarios else "not_configured"
    return summary


def external_asset(value: Mapping[str, Any] | None, *, name: str, run_id: str) -> dict[str, Any]:
    """规范已脱敏外部场景附属资产，缺输入时保持未配置。

    [参数] value: 已脱敏能力或对账摘要；name: 资产名称；run_id: 本轮执行标识。
    [返回] 带 schema、运行标识和状态的资产对象。
    最近修改时间: 2026-07-25 16:55:00 改动原因: 从接口报告模块拆出附属资产契约。
    """

    # 1. 缺少运行时输入时固定 not_configured，不能解释为真实通过。
    asset = dict(value or {})
    asset.setdefault("schema_version", "external-scenario/1.0")
    asset.setdefault("run_id", run_id)
    asset.setdefault("status", "not_configured")
    asset.setdefault("asset", name)
    asset["run_id"] = run_id
    return asset


def evidence_gate(gate: Mapping[str, Any], evidence_status: str) -> dict[str, Any]:
    """把证据脱敏清单状态合并到最终发布门禁。

    [参数] gate: 原接口或场景门禁；evidence_status: 证据清单 PASS/FAIL/PENDING。
    [返回] 不会放宽原门禁且已反映证据状态的门禁副本。
    最近修改时间：2026-07-25 23:18:15，禁止 manifest 非 PASS 时继续自动放行。
    """

    # 1. 清单通过时保持原门禁；原门禁已非 PASS 时只附加证据状态，禁止改写兼容分类。
    result = dict(gate)
    result["evidence_manifest_status"] = evidence_status
    if evidence_status == "PASS":
        return result
    if str(result.get("gate", "PENDING")).upper() != "PASS":
        result["allow_release"] = False
        return result
    # 2. 只有原门禁 PASS 时重新分类；敏感值落盘属于安全阻断，验证受限保持 PENDING。
    if evidence_status == "FAIL":
        result.update({"gate": "BLOCKED", "allow_release": False, "failure_type": "EVIDENCE_REDACTION_BLOCKED"})
        return result
    result.update({"gate": "PENDING", "allow_release": False, "failure_type": "EVIDENCE_REDACTION_PENDING"})
    return result


def write_evidence_manifest(
    artifact_root: Path,
    run_id: str,
    *,
    sensitive_values: Iterable[bytes] = (),
    additional_files: Iterable[tuple[str, Path]] = (),
) -> str:
    """为正式产物生成相对路径、摘要和脱敏复核状态清单。

    [参数] artifact_root: 正式产物根；run_id: 本轮执行标识；sensitive_values: 仅在内存中用于扫描的原始敏感字节；additional_files: 根外正式文件的安全逻辑名与路径。
    [返回] 证据清单文件路径。
    最近修改时间：2026-07-25 23:37:04，禁止清单跟随输出目录内的 symlink 读取根外文件。
    """

    # 1. 仅扫描足够长的原值，短值不能可靠匹配时显式降级为待确认，避免单字符误报。
    markers = tuple(value for value in sensitive_values if value)
    reliable_markers = tuple(value for value in markers if len(value) >= 4)
    verification_limited = len(reliable_markers) != len(markers)
    entries: list[dict[str, Any]] = []
    files = [(path.relative_to(artifact_root).as_posix(), path) for path in sorted(artifact_root.rglob("*"))]
    for logical_name, path in additional_files:
        # 1.1 附加逻辑名必须保持相对 POSIX 路径，不能把绝对路径或父级跳转写入清单。
        logical_path = PurePosixPath(logical_name)
        if not logical_name or "\\" in logical_name or logical_path.is_absolute() or logical_path.as_posix() != logical_name or any(part in {"", ".", ".."} for part in logical_path.parts):
            raise ValueError("EVIDENCE_MANIFEST_PATH_INVALID")
        files.append((logical_name, path))
    for logical_name, path in sorted(files, key=lambda item: item[0]):
        # 1.2 读取前复用输出路径闸门，防止文件 symlink 把根外内容伪装成正式证据。
        ensure_report_output_path(path)
        # 1.3 只索引正式文件并跳过清单自身，防止摘要递归变化。
        if not path.is_file() or path.name == "evidence-manifest.json":
            continue
        payload = path.read_bytes()
        sensitive_value_detected = any(marker in payload for marker in reliable_markers)
        if sensitive_value_detected:
            redacted = False
            redaction_status = "sensitive_value_detected"
        elif verification_limited:
            redacted = False
            redaction_status = "verification_limited"
        else:
            redacted = True
            redaction_status = "verified_absent" if markers else "no_sensitive_input"
        entries.append({
            # 1.4 每条证据固定记录安全逻辑路径、SHA-256 和基于真实输入原值的复核状态。
            "path": logical_name,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "redacted": redacted,
            "redaction_status": redaction_status,
        })
    # 2. 真实泄漏优先失败；只有短值验证受限时保持待确认，其余情况才允许通过。
    statuses = {item["redaction_status"] for item in entries}
    status = "FAIL" if "sensitive_value_detected" in statuses else ("PENDING" if "verification_limited" in statuses else "PASS")
    payload = {"schema_version": "external-scenario/1.0", "run_id": run_id, "status": status, "entries": entries}
    return write_text(artifact_root / "evidence-manifest.json", json.dumps(payload, ensure_ascii=False, indent=2))
