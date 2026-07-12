"""项目门禁真值表。"""

from __future__ import annotations

from typing import Any, Iterable, Mapping


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
