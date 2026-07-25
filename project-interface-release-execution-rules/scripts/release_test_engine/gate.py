"""项目门禁真值表。"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from pathlib import Path
from typing import Any, Iterable, Mapping

from .report_support import redact_evidence, safe_report_reason


CUTOVER_EVIDENCE_SCHEMA = "shadow-cutover-evidence/1.0"
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")


def _canonical_json_bytes(value: Any) -> bytes:
    """把门禁证据编码为稳定 UTF-8 JSON 字节。

    [参数] value: 只包含脱敏机器字段的证据对象。
    [返回] 末尾带换行的规范化 UTF-8 字节。
    最近修改时间：2026-07-25 23:35:00，统一 shadow evidence 写入与摘要复核口径。
    """

    # 1. 排序键和紧凑分隔符确保不同进程对同一证据得到相同字节。
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def persist_cutover_evidence(
    project_root: str | Path,
    *,
    run_id: str,
    environment: str,
    scenario_fingerprint: str,
    expected_scenarios: Mapping[str, Any],
    scenario_results: Iterable[Mapping[str, Any]],
    legacy_gate: Mapping[str, Any],
) -> dict[str, Any]:
    """持久化一次可由切换门禁独立重算的 shadow 证据。

    [参数] project_root/run_id/environment/scenario_fingerprint/expected_scenarios/scenario_results/legacy_gate: 项目根、运行身份和真实双轨输入。
    [返回] 项目根内相对路径、文件 SHA-256、重算场景门禁和双轨差异。
    最近修改时间：2026-07-25 21:59:37，shadow 计算和持久化只使用共享脱敏副本。
    """

    # 1. 文件名只接受受限运行标识，证据固定写在项目根内专用目录。
    if not RUN_ID_PATTERN.fullmatch(str(run_id)):
        raise ValueError("CUTOVER_RUN_ID_INVALID")
    root = Path(project_root).resolve()
    evidence_root = root / ".release-test-engine"
    evidence_dir = evidence_root / "shadow-evidence"
    # 1.1 在 mkdir 前逐级检查既有 symlink，禁止先在项目根外创建任何目录。
    for candidate in (evidence_root, evidence_dir):
        if candidate.exists() or candidate.is_symlink():
            try:
                candidate.resolve().relative_to(root)
            except ValueError as exc:
                raise PermissionError("CUTOVER_EVIDENCE_PATH_OUTSIDE_PROJECT") from exc
    evidence_dir.mkdir(parents=True, exist_ok=True)
    final_path = evidence_dir / f"{run_id}.json"
    if final_path.exists() or final_path.is_symlink():
        raise FileExistsError("CUTOVER_EVIDENCE_ALREADY_EXISTS")

    # 2. 场景门禁和双轨差异只从脱敏场景结果、目录全集和 legacy 状态重新计算。
    results = [dict(redact_evidence(dict(item))) for item in scenario_results]
    expected = {str(key): dict(redact_evidence(dict(value))) for key, value in expected_scenarios.items()}
    legacy_summary = {"gate": str(legacy_gate.get("gate", ""))}
    recomputed_gate = scenario_gate(results, expected_scenarios=expected)
    recomputed_diff = compare_gate_tracks(legacy_summary, results, run_id=run_id, expected_scenarios=expected)
    document = {
        "schema_version": CUTOVER_EVIDENCE_SCHEMA,
        "asset": "shadow-cutover-evidence",
        "run_id": run_id,
        "environment": environment,
        "scenario_fingerprint": scenario_fingerprint,
        "expected_scenarios": expected,
        "scenario_results": results,
        "legacy_gate": legacy_summary,
        "scenario_gate": recomputed_gate,
        "dual_gate_diff": recomputed_diff,
    }
    payload = _canonical_json_bytes(document)

    # 3. 随机临时名以独占创建模式写入，既有普通文件或 symlink 都不能被跟随覆盖。
    temporary_path = evidence_dir / f".{run_id}.{uuid.uuid4().hex}.tmp"
    created = False
    try:
        with temporary_path.open("xb") as stream:
            created = True
            stream.write(payload)
        temporary_path.replace(final_path)
    finally:
        if created and (temporary_path.exists() or temporary_path.is_symlink()):
            temporary_path.unlink()
    relative_path = final_path.relative_to(root).as_posix()
    return {
        "evidence_path": relative_path,
        "artifact_sha256": hashlib.sha256(payload).hexdigest(),
        "scenario_gate": recomputed_gate,
        "dual_gate_diff": recomputed_diff,
    }


def _verify_cutover_evidence(record: Mapping[str, Any], project_root: str | Path | None) -> dict[str, Any]:
    """回读并重算一条 shadow 历史绑定的真实证据文件。

    [参数] record: cutover 历史摘要；project_root: 证据所属项目根。
    [返回] valid、重算摘要和稳定失败原因。
    最近修改时间：2026-07-25 23:35:00，把历史资格绑定到项目根内真实 artifact。
    """

    # 1. 缺项目根、相对路径或文件摘要时直接判为不可复核。
    if project_root is None:
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}
    relative = Path(str(record.get("evidence_path", "")))
    if not str(relative) or relative.is_absolute() or not record.get("artifact_sha256"):
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}
    root = Path(project_root).resolve()
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}

    # 2. 文件必须存在且原始字节摘要匹配记录，禁止只校验自签摘要。
    try:
        payload = path.read_bytes()
    except OSError:
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}
    if hashlib.sha256(payload).hexdigest() != record.get("artifact_sha256"):
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}
    try:
        document = json.loads(payload.decode("utf-8"))
    except (UnicodeError, ValueError):
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}
    if not isinstance(document, Mapping) or document.get("schema_version") != CUTOVER_EVIDENCE_SCHEMA or document.get("asset") != "shadow-cutover-evidence":
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}

    # 3. 运行身份、环境和目录指纹必须同时匹配记录，目录指纹再由全集重算一次。
    expected = document.get("expected_scenarios", {})
    results = document.get("scenario_results", [])
    legacy_gate = document.get("legacy_gate", {})
    if not isinstance(expected, Mapping) or not isinstance(results, list) or not isinstance(legacy_gate, Mapping):
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}
    expected_fingerprint = hashlib.sha256(json.dumps(expected, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    identity_fields = ("run_id", "environment", "scenario_fingerprint")
    if any(document.get(field) != record.get(field) for field in identity_fields) or expected_fingerprint != document.get("scenario_fingerprint"):
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}

    # 4. 从文件中的真实结果重算门禁和差异，并与文件及历史摘要逐字段对账。
    recomputed_gate = scenario_gate(results, expected_scenarios=expected)
    recomputed_diff = compare_gate_tracks(legacy_gate, results, run_id=str(document.get("run_id", "")), expected_scenarios=expected)
    if document.get("scenario_gate") != recomputed_gate or document.get("dual_gate_diff") != recomputed_diff:
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}
    summary = {
        "run_id": str(document.get("run_id", "")),
        "environment": str(document.get("environment", "")),
        "scenario_fingerprint": str(document.get("scenario_fingerprint", "")),
        "scenario_gate": str(recomputed_gate.get("gate", "")),
        "coverage_complete": bool(recomputed_gate.get("coverage", {}).get("coverage_complete", False)),
        "cleanup_failed": len(recomputed_gate.get("cleanup_failures", [])),
        "unexplained_differences": list(recomputed_diff.get("unexplained_differences", [])),
    }
    record_summary = {key: record.get(key) for key in summary}
    if record_summary != summary:
        return {"valid": False, "reason": "HISTORY_EVIDENCE_INVALID", "summary": {}}
    return {"valid": True, "reason": "", "summary": summary}


def seal_cutover_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """为一次真实 shadow 摘要生成可复核指纹。

    [参数] record: 不含 evidence_digest 的运行摘要。
    [返回] 带稳定 SHA-256 摘要的运行记录副本。
    最近修改时间: 2026-07-25 19:20:00 改动原因: 防止重复或被篡改的历史摘要取得硬切资格。
    """

    # 1. 摘要只覆盖机器字段，调用方不能用自报 digest 绕过内容复核。
    result = {key: value for key, value in record.items() if key != "evidence_digest"}
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    result["evidence_digest"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return result


def evaluate_scenario_cutover(
    history: Iterable[Mapping[str, Any]],
    *,
    required_runs: int = 3,
    current_run_id: str = "",
    scenario_fingerprint: str = "",
    project_root: str | Path | None = None,
) -> dict[str, Any]:
    """判断场景门禁是否满足连续 local 达标切换条件。

    [参数] history: shadow 摘要；required_runs: 连续次数；current_run_id: 当前真实运行；scenario_fingerprint: 当前目录指纹；project_root: 证据所属项目根。
    [返回] 切换资格、窗口记录、缺口分类和最近运行状态。
    最近修改时间：2026-07-25 23:35:00，每条历史必须绑定并通过真实 evidence 文件重算。
    """

    # 1. 只看末尾连续窗口，并同时验证自签摘要和项目根内 evidence artifact。
    records = [dict(item) for item in history]
    window = records[-required_runs:] if required_runs > 0 else []
    run_ids = [str(item.get("run_id", "")) for item in window]
    fingerprints = [str(item.get("scenario_fingerprint", "")) for item in window]
    digest_valid = [seal_cutover_record(item).get("evidence_digest") == item.get("evidence_digest") for item in window]
    evidence_checks = [_verify_cutover_evidence(item, project_root) for item in window]
    evidence_valid = [bool(item.get("valid")) for item in evidence_checks]
    summaries = [dict(item.get("summary", {})) for item in evidence_checks]
    identity_valid = (
        bool(current_run_id)
        and bool(scenario_fingerprint)
        and len(run_ids) == len(set(run_ids))
        and all(run_ids)
        and bool(run_ids)
        and run_ids[-1] == current_run_id
        and all(value == scenario_fingerprint for value in fingerprints)
        and all(digest_valid)
        and all(evidence_valid)
    )
    qualified = len(window) == required_runs and identity_valid and all(
        str(item.get("environment", "")) == "local"
        and str(item.get("scenario_gate", "")) == "PASS"
        and bool(item.get("coverage_complete", False))
        and int(item.get("cleanup_failed", 1) or 0) == 0
        and not item.get("unexplained_differences", [])
        for item in summaries
    )
    # 2. 每类不满足条件都生成稳定原因；业务状态只读取已验证 artifact 的重算摘要。
    reasons: list[str] = []
    if len(window) < required_runs:
        reasons.append("INSUFFICIENT_HISTORY")
    if not run_ids or any(not value for value in run_ids) or len(run_ids) != len(set(run_ids)):
        reasons.append("RUN_ID_INVALID")
    if not current_run_id or not run_ids or run_ids[-1] != current_run_id:
        reasons.append("CURRENT_RUN_MISSING")
    if not scenario_fingerprint or any(value != scenario_fingerprint for value in fingerprints):
        reasons.append("SCENARIO_FINGERPRINT_MISMATCH")
    if any(not value for value in digest_valid) or any(not value for value in evidence_valid):
        reasons.append("HISTORY_EVIDENCE_INVALID")
    valid_summaries = [summary for summary, valid in zip(summaries, evidence_valid) if valid]
    if any(str(item.get("environment", "")) != "local" for item in valid_summaries):
        reasons.append("NON_LOCAL_RUN")
    if any(str(item.get("scenario_gate", "")) != "PASS" for item in valid_summaries):
        reasons.append("SCENARIO_NOT_PASS")
    if any(not bool(item.get("coverage_complete", False)) for item in valid_summaries):
        reasons.append("P0_P1_COVERAGE_INCOMPLETE")
    if any(int(item.get("cleanup_failed", 1) or 0) != 0 for item in valid_summaries):
        reasons.append("CLEANUP_INCOMPLETE")
    if any(item.get("unexplained_differences", []) for item in valid_summaries):
        reasons.append("UNEXPLAINED_DIFF")
    return {
        "status": "PASS" if qualified else "BLOCKED",
        "qualified": qualified,
        "required_runs": required_runs,
        "observed_runs": len(window),
        "reasons": sorted(set(reasons)),
        "window": window,
    }

def enforce_gate_mode(requested_mode: str, state: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """执行硬切后的门禁模式约束，禁止运行时回退旧轨道。

    [参数] requested_mode: 请求的门禁模式；state: 已持久化的切换状态。
    [返回] 规范化模式、是否允许和阻断原因。
    最近修改时间: 2026-07-25 19:20:00 改动原因: 硬切后禁止 legacy 和 shadow，切换前禁止直接请求 scenario。
    """

    # 1. scenario 是持久化硬切状态；切换前后都不得通过请求参数静默改变事实状态。
    mode = str(requested_mode or "legacy").lower()
    current = str((state or {}).get("active_mode", "legacy")).lower()
    if mode not in {"legacy", "shadow", "scenario"}:
        return {"status": "BLOCKED", "allowed": False, "mode": mode, "failure_type": "INVALID_GATE_MODE"}
    if current == "scenario" and mode != "scenario":
        return {"status": "BLOCKED", "allowed": False, "mode": mode, "failure_type": "LEGACY_FALLBACK_FORBIDDEN"}
    if current != "scenario" and mode == "scenario":
        return {"status": "BLOCKED", "allowed": False, "mode": mode, "failure_type": "SCENARIO_CUTOVER_NOT_ACTIVATED"}
    return {"status": "PASS", "allowed": True, "mode": mode, "failure_type": ""}


def _expected_scenario_map(expected_scenarios: Mapping[str, Any] | Iterable[Mapping[str, Any]] | None) -> dict[str, dict[str, Any]]:
    """规范化门禁所需的场景全集。

    [参数] expected_scenarios: 场景 ID 映射或场景契约集合。
    [返回] 场景 ID 到风险、来源指纹和清理要求的映射。
    最近修改时间：2026-07-25 21:59:37，目录全集进入门禁前统一脱敏并保持风险事实。
    """

    # 1. 映射和值对象两种形式统一收敛，缺少显式全集时返回空映射并由门禁阻断。
    if expected_scenarios is None:
        return {}
    if isinstance(expected_scenarios, Mapping):
        normalized: dict[str, dict[str, Any]] = {}
        for scenario_id, value in expected_scenarios.items():
            normalized[str(scenario_id)] = dict(redact_evidence(dict(value))) if isinstance(value, Mapping) else {"risk": str(value)}
        return normalized
    return {
        str(item.get("scenario_id", "")): dict(redact_evidence(dict(item)))
        for item in expected_scenarios
        if isinstance(item, Mapping) and str(item.get("scenario_id", ""))
    }


def scenario_gate(
    results: Iterable[Mapping[str, Any]],
    *,
    required_risks: Iterable[str] = ("P0", "P1"),
    expected_scenarios: Mapping[str, Any] | Iterable[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """根据目录全集和真实消费者场景结果计算 P0/P1 门禁。

    [参数] results: runner 结果；required_risks: 必测风险；expected_scenarios: verified 目录中的场景全集。
    [返回] 场景门禁、覆盖计数、非通过场景和清理失败列表。
    最近修改时间：2026-07-25 21:59:37，增加目录风险与结果风险一致性校验并返回脱敏门禁结果。
    """

    # 1. 以已验证目录为全集，对结果身份、风险和来源指纹逐项对账。
    items = [dict(redact_evidence(dict(item))) for item in results]
    required = {str(risk).upper() for risk in required_risks}
    expected = _expected_scenario_map(expected_scenarios)
    expected_required = {scenario_id: item for scenario_id, item in expected.items() if str(item.get("risk", "P2")).upper() in required}
    selected = [item for item in items if str(item.get("risk", "P2")).upper() in required]
    selected_ids = [str(item.get("scenario_id", "")) for item in selected]
    missing = sorted(set(expected_required) - set(selected_ids))
    unexpected = sorted(set(selected_ids) - set(expected_required))
    duplicate = sorted({scenario_id for scenario_id in selected_ids if scenario_id and selected_ids.count(scenario_id) > 1})
    source_mismatch = sorted(
        scenario_id
        for scenario_id, contract in expected_required.items()
        if contract.get("source_fingerprint")
        and any(str(item.get("scenario_id", "")) == scenario_id and item.get("source_fingerprint") != contract.get("source_fingerprint") for item in selected)
    )
    risk_mismatch = sorted(
        scenario_id
        for scenario_id, contract in expected_required.items()
        if any(
            str(item.get("scenario_id", "")) == scenario_id
            and str(item.get("risk", "P2")).upper() != str(contract.get("risk", "P2")).upper()
            for item in items
        )
    )
    non_pass = [str(item.get("scenario_id", "")) for item in selected if str(item.get("status", "PENDING")).upper() != "PASS"]
    # 2. 有写入副作用的场景必须声明且真实执行清理；空数组不能被解释为清理成功。
    cleanup_failures = [
        str(item.get("scenario_id", ""))
        for item in selected
        if any(str(step.get("status", "")).upper() != "PASS" for step in item.get("cleanup", []) if isinstance(step, Mapping))
        or bool(expected_required.get(str(item.get("scenario_id", "")), {}).get("cleanup_required", item.get("cleanup_required", False)))
        and not any(isinstance(step, Mapping) and str(step.get("status", "")).upper() == "PASS" for step in item.get("cleanup", []))
    ]
    # 2.1 覆盖字段固定记录风险、期望、实到、通过和五类身份差异。
    coverage = {
        "required_risks": sorted(required),
        "selected": len(selected),
        "passed": sum(str(item.get("status", "PENDING")).upper() == "PASS" for item in selected),
        "non_pass": len(non_pass),
        "expected": len(expected_required),
        "missing": missing,
        "unexpected": unexpected,
        "duplicate": duplicate,
        "source_mismatch": source_mismatch,
        "risk_mismatch": risk_mismatch,
        "coverage_complete": bool(expected_required) and not (missing or unexpected or duplicate or source_mismatch or risk_mismatch),
    }
    # 3. 覆盖事实不完整优先阻断；全集完整后再根据真实失败和清理失败判定。
    if not coverage["coverage_complete"]:
        # 3.1 目录全集为空或身份对账存在差异时固定阻断。
        gate = "BLOCKED"
        failure_type = "SCENARIO_COVERAGE_MISSING"
    elif non_pass or cleanup_failures:
        # 3.2 全集完整后，任一非 PASS 或清理不完整都固定失败。
        gate = "FAIL"
        failure_type = "SCENARIO_NON_PASS" if non_pass else "CLEANUP_INCOMPLETE"
    else:
        gate = "PASS"
        failure_type = ""
    # 4. 返回门禁结论、计数、覆盖明细、失败列表和原始选中结果。
    return {
        # 4.1 放行结论和总量计数字段组。
        "gate": gate,
        "allow_release": gate == "PASS",
        "total": len(selected),
        "passed": coverage["passed"],
        "failed": len(non_pass),
        "pending": sum(str(item.get("status", "PENDING")).upper() == "PENDING" for item in selected),
        # 4.2 覆盖、失败分类和选中结果字段组。
        "coverage": coverage,
        "non_pass": non_pass,
        "cleanup_failures": cleanup_failures,
        "failure_type": failure_type,
        "results": selected,
    }


def compare_gate_tracks(
    legacy_gate: Mapping[str, Any],
    scenario_results: Iterable[Mapping[str, Any]],
    *,
    run_id: str = "",
    required_risks: Iterable[str] = ("P0", "P1"),
    expected_scenarios: Mapping[str, Any] | Iterable[Mapping[str, Any]] | None = None,
    explanations: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """对账 legacy 与 scenario 两条门禁轨道并分类未解释差异。

    [参数] legacy_gate/scenario_results/run_id/required_risks/expected_scenarios/explanations: 旧门禁、真实结果、运行标识、风险、目录全集和差异解释。
    [返回] 双轨门禁、差异分类、解释状态和场景门禁对象。
    最近修改时间：2026-07-25 21:59:37，双轨输出和差异解释进入证据前统一脱敏。
    """

    # 1. 先独立计算场景真值，再与 legacy 结果比较，禁止由 legacy 反推场景通过。
    scenario = scenario_gate(scenario_results, required_risks=required_risks, expected_scenarios=expected_scenarios)
    known_explanations = {str(key): safe_report_reason(value) for key, value in (explanations or {}).items()}
    differences: list[dict[str, Any]] = []
    if legacy_gate.get("gate") != scenario.get("gate"):
        differences.append({"type": "STATUS_DISAGREEMENT", "legacy": legacy_gate.get("gate"), "scenario": scenario.get("gate")})
    if not scenario["coverage"]["coverage_complete"]:
        differences.append({"type": "P0_P1_COVERAGE_GAP", "reason": scenario["failure_type"]})
    if scenario["non_pass"]:
        differences.append({"type": "SCENARIO_NON_PASS", "scenario_ids": scenario["non_pass"]})
    if scenario["cleanup_failures"]:
        differences.append({"type": "CLEANUP_INCOMPLETE", "scenario_ids": scenario["cleanup_failures"]})
    # 2. 只有项目显式提供解释的差异才能离开 PENDING。
    for difference in differences:
        difference["explanation"] = known_explanations.get(str(difference["type"]), "")
    unexplained = [item for item in differences if not item.get("explanation")]
    return {
        "schema_version": "external-scenario/1.0",
        "asset": "dual-gate-diff",
        "run_id": run_id,
        "status": "PASS" if not unexplained else "PENDING",
        "legacy_gate": redact_evidence(dict(legacy_gate)),
        "scenario_gate": scenario,
        "differences": differences,
        "unexplained_differences": unexplained,
    }


def aggregate_gate(results: Iterable[Mapping[str, Any]], interfaces: Iterable[Any], *, unsupported: Iterable[Mapping[str, Any]] = ()) -> dict[str, Any]:
    items = [dict(item) for item in results]
    by_id = {item.operation_id: item for item in interfaces}
    p0_bad: list[str] = []
    p1_bad: list[str] = []
    p2_bad: list[str] = []
    runtime_blocking_types = {
        "UNSUPPORTED_ADAPTER",
        "FIXTURE_LIFECYCLE_INCOMPLETE",
        "FIXTURE_CLEANUP_UNEXECUTABLE",
        "FIXTURE_EXTERNAL_ENDPOINT",
        "FIXTURE_CLEANUP_FAILED",
        "FIXTURE_STATUS_MISSING",
        "FIXTURE_TRANSPORT_INVALID",
        "LOCAL_CONFIG_PROVENANCE_INVALID",
    }
    runtime_p0_p1: list[str] = []
    cleanup_failures: list[str] = []
    for item in items:
        risk = getattr(by_id.get(item.get("operation_id")), "risk", "P2")
        status = str(item.get("status", "PENDING"))
        failure_type = str(item.get("failure_type", "") or "")
        if failure_type == "FIXTURE_CLEANUP_FAILED":
            cleanup_failures.append(str(item.get("operation_id", "")))
        if failure_type in runtime_blocking_types or failure_type.startswith("FIXTURE_"):
            if risk in {"P0", "P1"} and status != "PASS":
                runtime_p0_p1.append(str(item.get("operation_id", "")))
        if status != "PASS":
            if risk == "P0":
                p0_bad.append(str(item.get("operation_id", "")))
            elif risk == "P1":
                p1_bad.append(str(item.get("operation_id", "")))
            else:
                p2_bad.append(str(item.get("operation_id", "")))
    unknown = list(unsupported)
    if p0_bad or runtime_p0_p1 or cleanup_failures:
        gate = "FAIL"
    elif p1_bad or p2_bad or unknown:
        gate = "PARTIAL"
    else:
        gate = "PASS"
    counts = {status: sum(item.get("status") == status for item in items) for status in ("PASS", "EXPECTED_FAIL", "FAIL", "PENDING", "BLOCKED")}
    return {
        "gate": gate,
        "allow_release": gate == "PASS",
        "total": len(items),
        "passed": counts["PASS"],
        "failed": counts["FAIL"] + counts["BLOCKED"],
        "pending": counts["PENDING"],
        "counts": counts,
        "p0_non_pass": p0_bad,
        "p1_non_pass": p1_bad,
        "p2_non_pass": p2_bad,
        "runtime_p0_p1_blocked": runtime_p0_p1,
        "cleanup_failures": cleanup_failures,
        "unsupported": unknown,
        "results": items,
    }
