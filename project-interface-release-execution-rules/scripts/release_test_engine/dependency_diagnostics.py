"""依赖失败分类，避免把 provider 问题误报成 consumer 失败。"""

from __future__ import annotations

from typing import Any, Mapping


def diagnose(provider: Mapping[str, Any], consumer_id: str, *, missing_fields: list[str] | None = None) -> dict[str, Any]:
    status = str(provider.get("status", "PENDING"))
    if status != "PASS":
        return {"consumer": consumer_id, "provider": provider.get("operation_id", ""), "status": "BLOCKED", "failure_type": "BLOCKED_BY_DEPENDENCY", "reason": f"provider returned {status}"}
    if missing_fields:
        return {"consumer": consumer_id, "provider": provider.get("operation_id", ""), "status": "PENDING", "failure_type": "PARAM_UNRESOLVED", "missing_fields": list(missing_fields)}
    return {"consumer": consumer_id, "provider": provider.get("operation_id", ""), "status": "READY"}
