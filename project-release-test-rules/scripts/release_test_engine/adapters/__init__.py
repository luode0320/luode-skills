"""协议适配器支持矩阵；未知协议必须显式降级为 PENDING。"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .cli_entry import ADAPTER as CLI_ADAPTER
from .event_handler import ADAPTER as EVENT_ADAPTER
from .graphql import ADAPTER as GRAPHQL_ADAPTER
from .grpc import ADAPTER as GRPC_ADAPTER
from .http_openapi import ADAPTER as OPENAPI_ADAPTER
from .messaging import ADAPTER as MESSAGE_ADAPTER
from .scheduler import ADAPTER as SCHEDULER_ADAPTER
from .soap_jsonrpc import ADAPTER as SOAP_JSONRPC_ADAPTER
from .websocket import ADAPTER as WEBSOCKET_ADAPTER


ADAPTERS = (OPENAPI_ADAPTER, GRAPHQL_ADAPTER, GRPC_ADAPTER, WEBSOCKET_ADAPTER, SOAP_JSONRPC_ADAPTER, MESSAGE_ADAPTER, CLI_ADAPTER, SCHEDULER_ADAPTER, EVENT_ADAPTER)

ADAPTER_MATRIX: dict[str, dict[str, Any]] = {
    "http": {"status": "ready", "discovery_status": "ready", "execution_status": "ready", "runner": "builtin.http", "discovery": "openapi-or-route"},
    "cli": {"status": "ready", "discovery_status": "ready", "execution_status": "ready", "runner": "builtin.cli", "discovery": "command-declaration"},
    "graphql": {"status": "pending", "discovery_status": "ready", "execution_status": "pending", "runner": None, "discovery": "schema-or-resolver"},
    "grpc": {"status": "pending", "discovery_status": "ready", "execution_status": "pending", "runner": None, "discovery": "proto-rpc"},
    "websocket": {"status": "pending", "discovery_status": "ready", "execution_status": "pending", "runner": None, "discovery": "websocket-declaration"},
    "soap": {"status": "pending", "discovery_status": "ready", "execution_status": "pending", "runner": None, "discovery": "wsdl-operation"},
    "jsonrpc": {"status": "pending", "discovery_status": "ready", "execution_status": "pending", "runner": None, "discovery": "jsonrpc-method"},
    "message": {"status": "pending", "discovery_status": "ready", "execution_status": "pending", "runner": None, "discovery": "queue-consumer-declaration"},
    "scheduler": {"status": "pending", "discovery_status": "ready", "execution_status": "pending", "runner": None, "discovery": "schedule-declaration"},
    "event": {"status": "pending", "discovery_status": "ready", "execution_status": "pending", "runner": None, "discovery": "event-handler-declaration"},
}

_FIXTURE_STATUSES = {"PASS", "EXPECTED_FAIL", "FAIL", "PENDING", "BLOCKED"}
_FIXTURE_TRANSPORTS = {"fixture", "in-process", "in_process"}
_FIXTURE_REFERENCE_KEYS = {
    "target_ref",
    "endpoint_ref",
    "base_url_ref",
    "broker_ref",
    "trigger_ref",
    "bus_ref",
    "command_ref",
}
_LOCAL_REFERENCE_VALUES = {
    "local",
    "local_config",
    "local_config_ref",
    "local_fixture",
    "in_process",
    "in-process",
    "in_process_fixture",
    "in-process-fixture",
    "development",
    "dev",
    "localhost",
    "127.0.0.1",
}


def _entrypoint_external_references(entrypoint: Mapping[str, Any]) -> list[str]:
    """识别 strict fixture 入口中的非 local 引用。"""

    invalid: list[str] = []
    for key in _FIXTURE_REFERENCE_KEYS:
        value = entrypoint.get(key)
        if value in (None, ""):
            continue
        if isinstance(value, Mapping):
            environment = str(value.get("environment", value.get("provenance", ""))).strip().lower()
            if environment in {"local", "local-dev", "development"}:
                continue
            invalid.append(key)
            continue
        normalized = str(value).strip().lower()
        if normalized in _LOCAL_REFERENCE_VALUES:
            continue
        if any(marker in normalized for marker in ("local", "fixture", "in_process", "in-process", "localhost", "127.0.0.1")):
            continue
        invalid.append(key)
    return invalid


def fixture_capability(interface: Any, *, strict_fixture: bool = False) -> dict[str, Any]:
    """[参数] interface/strict_fixture: 统一入口 IR 和是否要求生命周期契约；[返回] local fixture 能力和原因；最近修改时间: 2026-07-13 00:30:00 增加 strict 生命周期校验。"""

    entrypoint = getattr(interface, "entrypoint", {}) or {}
    if not isinstance(entrypoint, Mapping):
        return {"fixture_status": "unavailable", "execution_status": "pending", "reason": "entrypoint is not an object"}
    fixture = entrypoint.get("fixture_response", entrypoint.get("fixture"))
    if fixture is None:
        return {"fixture_status": "unavailable", "execution_status": "pending", "reason": "explicit fixture_response is missing"}
    if not isinstance(fixture, Mapping):
        return {"fixture_status": "invalid", "execution_status": "pending", "reason": "fixture_response must be an object"}
    status = str(fixture.get("status", "")).upper()
    if status not in _FIXTURE_STATUSES:
        return {"fixture_status": "invalid", "execution_status": "pending", "reason": "fixture_response.status must be explicit and supported", "failure_type": "FIXTURE_STATUS_MISSING"}
    transport = str(fixture.get("transport", "fixture")).strip().lower()
    if transport not in _FIXTURE_TRANSPORTS:
        return {"fixture_status": "invalid", "execution_status": "pending", "reason": "fixture transport must be local in-process", "failure_type": "FIXTURE_TRANSPORT_INVALID"}
    lifecycle = {
        "local_provenance": fixture.get("local_provenance") is True,
        "run_id": bool(fixture.get("run_id")),
        "startup_handle": callable(fixture.get("startup_handle", fixture.get("handle"))),
        "handler": callable(fixture.get("handler")),
        "cleanup_declared": callable(fixture.get("cleanup_callback")) or (isinstance(fixture.get("cleanup"), Mapping) and callable(fixture["cleanup"].get("callback"))),
    }
    if strict_fixture:
        external_entrypoint_fields = _entrypoint_external_references(entrypoint)
        if external_entrypoint_fields:
            return {
                "fixture_status": "invalid",
                "execution_status": "pending",
                "reason": "strict fixture entrypoint references are not local: " + ", ".join(external_entrypoint_fields),
                "failure_type": "LOCAL_CONFIG_PROVENANCE_INVALID",
                "lifecycle": lifecycle,
            }
        external_fields = [field for field in ("endpoint", "url", "base_url", "broker", "target") if fixture.get(field)]
        if external_fields:
            return {"fixture_status": "invalid", "execution_status": "pending", "reason": "strict fixture cannot declare external endpoint fields: " + ", ".join(external_fields), "failure_type": "FIXTURE_EXTERNAL_ENDPOINT", "lifecycle": lifecycle}
        cleanup_metadata = any(key in fixture for key in ("cleanup_callback", "cleanup_ref", "cleanup"))
        cleanup_callable = callable(fixture.get("cleanup_callback")) or (isinstance(fixture.get("cleanup"), Mapping) and callable(fixture["cleanup"].get("callback")))
        if not cleanup_metadata:
            return {"fixture_status": "invalid", "execution_status": "pending", "reason": "strict fixture cleanup callback is not executable", "failure_type": "FIXTURE_CLEANUP_UNEXECUTABLE", "lifecycle": lifecycle}
        missing = [name for name, present in lifecycle.items() if not present]
        if missing:
            return {"fixture_status": "invalid", "execution_status": "pending", "reason": "strict fixture lifecycle fields missing: " + ", ".join(missing), "failure_type": "FIXTURE_LIFECYCLE_INCOMPLETE", "lifecycle": lifecycle}
        if not cleanup_callable:
            return {"fixture_status": "invalid", "execution_status": "pending", "reason": "strict fixture cleanup callback is not executable", "failure_type": "FIXTURE_CLEANUP_UNEXECUTABLE", "lifecycle": lifecycle}
    return {"fixture_status": "ready", "execution_status": "ready", "execution_mode": "in-process-fixture", "fixture_status_value": status, "reason": "explicit local fixture_response", "lifecycle": lifecycle, "lifecycle_status": "complete" if all(lifecycle.values()) else "legacy"}


def adapter_matrix_status(protocol: str, interfaces: Sequence[Any] = (), *, strict_fixture: bool = False) -> dict[str, Any]:
    """[参数] protocol/interfaces/strict_fixture: 协议、入口集合和生命周期严格开关；[返回] 发现/fixture/执行三态矩阵；最近修改时间: 2026-07-13 00:30:00 让 doctor 暴露 fixture 生命周期阻断。"""

    # 1. 先复制静态适配器能力，避免修改全局矩阵或污染其他项目。
    result = adapter_status(protocol)
    items = [item for item in interfaces if getattr(item, "protocol", None) == protocol]
    fixture_items = [fixture_capability(item, strict_fixture=strict_fixture) for item in items]
    result["interface_count"] = len(items)
    result["discovery_status"] = "ready" if items or result.get("discovery_status") == "ready" else "pending"
    if result.get("execution_status") == "ready":
        result["fixture_status"] = "not_required"
        result["execution_mode"] = result.get("runner") or "builtin"
    elif not items:
        result["fixture_status"] = "unavailable"
        result["execution_mode"] = "none"
        result["reason"] = "no discovered interface to execute"
    else:
        ready = [item for item in fixture_items if item.get("fixture_status") == "ready"]
        invalid = [item for item in fixture_items if item.get("fixture_status") == "invalid"]
        result["fixture_status"] = "ready" if len(ready) == len(items) else "partial" if ready else "unavailable"
        result["execution_status"] = "ready" if len(ready) == len(items) else "partial" if ready else "pending"
        result["execution_mode"] = "in-process-fixture" if ready else "none"
        if ready:
            result["runner"] = "builtin.fixture"
        if invalid:
            first_invalid = invalid[0]
            result["reason"] = first_invalid.get("reason", "fixture contract invalid")
            result["failure_type"] = first_invalid.get("failure_type", "FIXTURE_CONTRACT_INVALID")
            lifecycle = first_invalid.get("lifecycle", {})
            result["local_provenance"] = "local" if isinstance(lifecycle, Mapping) and lifecycle.get("local_provenance") is True else "unknown"
        elif not ready:
            result["reason"] = "discovery-ready but no executable local fixture"
            result["failure_type"] = "UNSUPPORTED_ADAPTER"
    result["interfaces"] = [
        {
            "operation_id": getattr(interface, "operation_id", ""),
            "discovery_status": "ready",
            **fixture_capability(interface, strict_fixture=strict_fixture),
        }
        for interface in items
    ]
    result["fixture_count"] = sum(item.get("fixture_status") == "ready" for item in fixture_items)
    result["pending_count"] = sum(item.get("execution_status") != "ready" for item in fixture_items) if result.get("execution_mode") == "in-process-fixture" else (len(items) if result.get("execution_status") != "ready" else 0)
    if result.get("execution_status") == "ready":
        result["status"] = "ready"
    return result


def adapter_status(protocol: str) -> dict[str, Any]:
    return dict(ADAPTER_MATRIX.get(protocol, {"status": "unsupported", "runner": None, "discovery": "unknown"}))


def supported_protocols() -> list[str]:
    """[参数] 无；[返回] 当前存在真实 runner 的协议；最近修改时间: 2026-07-12 19:20:00 区分发现和执行能力。"""

    return sorted(name for name, item in ADAPTER_MATRIX.items() if item.get("execution_status", item["status"]) == "ready")


def discovery_adapters() -> tuple[Any, ...]:
    """[参数] 无；[返回] 内建发现适配器；最近修改时间: 2026-07-12 19:20:00 提供 discovery 注册表。"""

    return ADAPTERS
