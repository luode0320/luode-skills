"""确定性响应判定和项目门禁聚合。"""

from __future__ import annotations

import json
from typing import Any, Iterable, Mapping


STATUSES = {"PASS", "EXPECTED_FAIL", "FAIL", "PENDING", "BLOCKED"}


def _mask(value: Any) -> Any:
    sensitive = {"token", "password", "secret", "authorization", "cookie", "phone", "idcard", "bankcard", "api-key", "x-api-key"}
    if isinstance(value, Mapping):
        return {key: ("***" if str(key).lower() in sensitive else _mask(child)) for key, child in value.items()}
    if isinstance(value, list):
        return [_mask(item) for item in value]
    return value


def _evidence_json(value: Any) -> str:
    return json.dumps(_mask(value or {}), ensure_ascii=False, sort_keys=True)


def judge(result: Mapping[str, Any], interface: Any | None = None) -> dict[str, Any]:
    status = str(result.get("status", "PENDING"))
    if status not in STATUSES:
        status = "PENDING"
    response = result.get("response", {})
    expected = interface.response_schema if interface is not None else {}
    reason = "transport reported pass" if status == "PASS" else str(result.get("failure_type") or result.get("evidence", {}).get("reason", "no deterministic success evidence"))
    body = response.get("body") if isinstance(response, Mapping) else response
    if status == "PASS" and isinstance(body, Mapping):
        if interface is not None and interface.protocol == "graphql" and body.get("errors"):
            status, reason = "FAIL", "graphql response contains errors"
        elif interface is not None and interface.protocol == "jsonrpc" and body.get("error"):
            status, reason = "FAIL", "json-rpc response contains error"
    if status == "PASS" and interface is not None and interface.protocol == "soap" and "fault" in str(body).lower():
        status, reason = "FAIL", "soap response contains Fault"
    if status == "PASS" and isinstance(expected, Mapping):
        code_path = expected.get("code_path")
        success_values = expected.get("success_values")
        if code_path and success_values:
            value: Any = response
            for part in str(code_path).lstrip("$.").split("."):
                if isinstance(value, Mapping):
                    value = value.get(part)
                else:
                    value = None
            if value not in success_values:
                status = "FAIL"
                reason = f"business code {value!r} is not successful"
        required_fields = expected.get("required_fields", [])
        if status == "PASS" and required_fields:
            missing = [field for field in required_fields if not _has_path(body, str(field))]
            if missing:
                status = "FAIL"
                reason = "response schema missing fields: " + ", ".join(str(field) for field in missing)
    # 判定不得丢失请求和响应证据；报告层随后统一脱敏后落盘。
    return {
        "operation_id": result.get("operation_id", ""),
        "status": status,
        "reason": reason,
        "failure_type": result.get("failure_type", ""),
        "request": _evidence_json(result.get("request", {})),
        "response": _evidence_json(result.get("response", {})),
        "evidence": result.get("evidence", {}),
    }


def _has_path(value: Any, path: str) -> bool:
    """[参数] value/path: 响应对象与点路径；[返回] 字段是否存在；最近修改时间: 2026-07-12 支持响应 schema 必填字段。"""

    current = value
    for part in path.lstrip("$.").split("."):
        if not part:
            continue
        if not isinstance(current, Mapping) or part not in current:
            return False
        current = current[part]
    return True


def aggregate(results: Iterable[Mapping[str, Any]], interfaces: Iterable[Any] = ()) -> dict[str, Any]:
    items = [dict(item) for item in results]
    by_id = {item.operation_id: item for item in interfaces}
    p0 = [item for item in items if by_id.get(item.get("operation_id"), None) is not None and getattr(by_id[item["operation_id"]], "risk", "P2") == "P0"]
    failures = [item for item in items if item.get("status") in {"FAIL", "BLOCKED"}]
    pending = [item for item in items if item.get("status") == "PENDING"]
    p0_bad = [item for item in p0 if item.get("status") != "PASS"]
    if p0_bad or failures:
        gate = "FAIL"
    elif pending:
        gate = "PARTIAL"
    else:
        gate = "PASS"
    return {"gate": gate, "allow_release": gate == "PASS", "total": len(items), "passed": sum(item.get("status") == "PASS" for item in items), "failed": len(failures), "pending": len(pending), "p0_non_pass": [item.get("operation_id") for item in p0_bad], "results": items}
