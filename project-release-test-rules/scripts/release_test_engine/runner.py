"""多协议本地执行器；未知适配器显式返回 PENDING。"""

from __future__ import annotations

import json
import inspect
import os
import shlex
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping

from .safety import check_operation
from .auth import AuthResolutionError, merge_auth_headers, resolve_auth
from .adapters import fixture_capability


def capability_status(interface: Any, *, strict_fixture: bool = False) -> dict[str, Any]:
    """[参数] interface/strict_fixture: 统一入口和 fixture 生命周期严格开关；[返回] discovery/execution 能力状态；最近修改时间: 2026-07-13 00:35:00 暴露缺 runtime 的确定性 PENDING。"""

    if getattr(interface, "protocol", "") in {"grpc", "websocket", "message", "scheduler", "event"}:
        capability = fixture_capability(interface, strict_fixture=strict_fixture)
        if capability.get("fixture_status") == "ready":
            return {"discovery_status": "ready", "fixture_status": "ready", "execution_status": "ready", "reason": "local fixture is executable", "capability": capability}
        return {"discovery_status": "ready", "fixture_status": capability.get("fixture_status", "unavailable"), "execution_status": "pending", "reason": capability.get("reason", "local fixture is unavailable"), "failure_type": capability.get("failure_type", "UNSUPPORTED_ADAPTER"), "capability": capability}
    if getattr(interface, "protocol", "") in {"http", "cli", "graphql", "soap", "jsonrpc"}:
        return {"discovery_status": "ready", "fixture_status": "not_required", "execution_status": "ready" if getattr(interface, "protocol", "") in {"http", "cli"} else "pending", "reason": "built-in runner capability"}
    return {"discovery_status": "ready", "fixture_status": "unavailable", "execution_status": "pending", "reason": "unsupported protocol", "failure_type": "UNSUPPORTED_ADAPTER"}


@dataclass(frozen=True)
class ExecutionResult:
    operation_id: str
    status: str
    request: Mapping[str, Any]
    response: Mapping[str, Any]
    evidence: Mapping[str, Any]
    failure_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"operation_id": self.operation_id, "status": self.status, "request": dict(self.request), "response": dict(self.response), "evidence": dict(self.evidence), "failure_type": self.failure_type}


def _http(interface: Any, params: Mapping[str, Any], env: Mapping[str, str]) -> ExecutionResult:
    entry = interface.entrypoint
    base_ref = str(entry.get("base_url_ref", "base_url"))
    # 只有 local_config 引用或显式 local provenance 才允许使用传入 URL；避免把任意
    # base_url 当作 local 配置而误连 test/prod。
    if env.get("base_url") and not env.get("local_config") and str(env.get("config_environment", "")).lower() not in {"local", "local-dev", "development"}:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"params": dict(params)}, {}, {"reason": "base URL provenance is not local"}, "LOCAL_CONFIG_PROVENANCE_INVALID")
    process_base = os.getenv("RELEASE_TEST_BASE_URL", "") if str(os.getenv("RELEASE_TEST_CONFIG_ENV", "")).lower() in {"local", "local-dev", "development"} else ""
    base = env.get(base_ref) or (env.get("base_url") if base_ref == "base_url" else "") or process_base
    if not base:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"params": dict(params)}, {}, {"reason": "local base URL missing"}, "LOCAL_CONFIG_MISSING")
    path = str(entry.get("path", ""))
    path_names = {item.name for item in interface.parameters if item.location == "path"}
    query_names = {item.name for item in interface.parameters if item.location == "query"}
    header_names = {item.name for item in interface.parameters if item.location == "header"}
    cookie_names = {item.name for item in interface.parameters if item.location == "cookie"}
    body_names = {item.name for item in interface.parameters if item.location in {"body", "form", "multipart"}}
    for key in path_names:
        if key in params:
            path = path.replace("{" + str(key) + "}", str(params[key]))
    url = base.rstrip("/") + "/" + path.lstrip("/")
    method = str(entry.get("method", "GET")).upper()
    query = {key: params[key] for key in query_names if key in params}
    if query and method in {"GET", "HEAD", "DELETE"}:
        from urllib.parse import urlencode
        url += ("&" if "?" in url else "?") + urlencode(query)
    elif query:
        from urllib.parse import urlencode
        url += ("&" if "?" in url else "?") + urlencode(query)
    body_params = {key: params[key] for key in body_names if key in params}
    body = None if method in {"GET", "HEAD"} else json.dumps(body_params, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    for key, value in dict(entry.get("headers", {})).items():
        headers[str(key)] = str(value)
    for key in header_names:
        if key in params:
            headers[str(key)] = str(params[key])
    if cookie_names:
        cookies = [f"{key}={params[key]}" for key in sorted(cookie_names) if key in params]
        if cookies:
            headers["Cookie"] = "; ".join(cookies)
    try:
        auth = resolve_auth(interface.auth, environment="local", environ=env or os.environ)
        headers = merge_auth_headers(headers, auth)
    except AuthResolutionError as exc:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"url": url, "method": method, "params": dict(params)}, {}, {"reason": str(exc)}, "LOCAL_AUTH_UNAVAILABLE")
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw)
            except ValueError:
                payload = {"raw": raw}
            return ExecutionResult(interface.operation_id, "PASS", {"url": url, "method": method, "params": dict(params)}, {"status": response.status, "body": payload}, {"transport": "urllib"})
    except urllib.error.HTTPError as exc:
        return ExecutionResult(interface.operation_id, "FAIL", {"url": url, "method": method, "params": dict(params)}, {"status": exc.code, "body": exc.read().decode("utf-8", errors="replace")}, {"transport": "urllib"}, "HTTP_ERROR")
    except (OSError, urllib.error.URLError) as exc:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"url": url, "method": method, "params": dict(params)}, {}, {"transport": "urllib", "reason": str(exc)}, "LOCAL_SERVICE_UNAVAILABLE")


def _fixture(interface: Any, params: Mapping[str, Any], *, strict_fixture: bool = False, run_id: str | None = None) -> ExecutionResult | None:
    """[参数] interface/params/strict_fixture/run_id: 入口、参数、严格开关和执行批次；[返回] fixture 结果或空。"""

    fixture = interface.entrypoint.get("fixture_response", interface.entrypoint.get("fixture"))
    if fixture is None:
        return None
    capability = fixture_capability(interface, strict_fixture=strict_fixture)
    if capability.get("fixture_status") != "ready":
        return ExecutionResult(
            interface.operation_id,
            "PENDING",
            {"params": dict(params), "fixture": True},
            {},
            {"transport": "fixture", "reason": capability.get("reason", "fixture contract is not executable"), "capability": capability},
            str(capability.get("failure_type", "FIXTURE_CONTRACT_INVALID")),
        )
    if not isinstance(fixture, Mapping):
        fixture = {"body": fixture}
    status = str(fixture.get("status", "PASS")).upper()
    if status not in {"PASS", "EXPECTED_FAIL", "FAIL", "PENDING", "BLOCKED"}:
        status = "PENDING"
    failure_type = "" if status in {"PASS", "EXPECTED_FAIL"} else str(fixture.get("failure_type", "FIXTURE_STATUS"))
    return _execute_fixture_lifecycle(interface, params, fixture, capability, status, failure_type, run_id=run_id)


_LIFECYCLE_KEYS = {
    "status",
    "transport",
    "http_status",
    "failure_type",
    "local_provenance",
    "run_id",
    "startup_handle",
    "handle",
    "startup_callback",
    "handler",
    "handler_ref",
    "cleanup_callback",
    "cleanup_ref",
    "cleanup",
    "endpoint",
    "url",
    "base_url",
    "broker",
    "target",
}


def _json_safe(value: Any) -> Any:
    """将 fixture body 限制为可序列化值，避免 callback 泄漏到报告。"""

    if isinstance(value, Mapping):
        return {str(key): _json_safe(child) for key, child in value.items() if not callable(child)}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _fixture_default_body(fixture: Mapping[str, Any]) -> dict[str, Any]:
    """从 fixture 元数据提取无生命周期 callback 的默认 body。"""

    return {str(key): _json_safe(value) for key, value in fixture.items() if key not in _LIFECYCLE_KEYS and key != "body" and not callable(value)}


def _invoke_callback(callback: Any, values: Mapping[str, Any]) -> Any:
    """按回调参数名传入已知生命周期值，兼容零参数旧 callback。"""

    if not callable(callback):
        return None
    try:
        signature = inspect.signature(callback)
    except (TypeError, ValueError):
        return callback()
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    for parameter in signature.parameters.values():
        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            continue
        if parameter.name in values:
            if parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
                args.append(values[parameter.name])
            else:
                kwargs[parameter.name] = values[parameter.name]
        elif parameter.default is inspect.Parameter.empty:
            # 不猜测未知参数，交给回调抛出明确的生命周期错误。
            return callback()
    return callback(*args, **kwargs)


def _execute_fixture_lifecycle(
    interface: Any,
    params: Mapping[str, Any],
    fixture: Mapping[str, Any],
    capability: Mapping[str, Any],
    status: str,
    failure_type: str,
    *,
    run_id: str | None,
) -> ExecutionResult:
    """执行 local fixture 的 startup/handler/cleanup，并隔离不可序列化生命周期对象。"""

    effective_run_id = str(run_id or fixture.get("run_id", ""))
    request = {"params": dict(params), "fixture": True, "run_id": effective_run_id}
    cleanup_evidence = fixture.get("cleanup_ref", "callback" if fixture.get("cleanup_callback") or isinstance(fixture.get("cleanup"), Mapping) else "declared")
    evidence: dict[str, Any] = {
        "transport": "fixture",
        "execution_mode": "in-process-fixture",
        "run_id": effective_run_id,
        "cleanup": cleanup_evidence,
        "cleanup_status": "declared",
        "capability": dict(capability),
    }
    response_status = fixture.get("http_status", 200)
    response_body: Any = fixture.get("body") if "body" in fixture else _fixture_default_body(fixture)
    result_status = status
    result_failure = failure_type
    startup = fixture.get("startup_callback")
    if not callable(startup) and callable(fixture.get("startup_handle")):
        # 兼容 in-process fixture 直接把启动器放在 startup_handle 的契约。
        startup = fixture.get("startup_handle")
    handler = fixture.get("handler")
    cleanup = fixture.get("cleanup_callback")
    if not callable(cleanup) and isinstance(fixture.get("cleanup"), Mapping):
        cleanup = fixture["cleanup"].get("callback")
    callback_values = {"params": dict(params), "run_id": effective_run_id, "startup_handle": fixture.get("startup_handle", fixture.get("handle")), "handle": fixture.get("startup_handle", fixture.get("handle"))}
    try:
        if callable(startup):
            startup_result = _invoke_callback(startup, callback_values)
            if startup_result is not None:
                callback_values["startup_handle"] = startup_result
                callback_values["handle"] = startup_result
            evidence["startup_status"] = "PASS"
        if callable(handler):
            handler_result = _invoke_callback(handler, callback_values)
            if isinstance(handler_result, Mapping) and ("body" in handler_result or "status" in handler_result):
                response_body = handler_result.get("body", handler_result)
                response_status = handler_result.get("http_status", response_status)
                result_status = str(handler_result.get("status", result_status)).upper()
                if result_status not in {"PASS", "EXPECTED_FAIL", "FAIL", "PENDING", "BLOCKED"}:
                    result_status = "PENDING"
            elif handler_result is not None:
                response_body = handler_result
            evidence["handler_status"] = "PASS"
        response = {"status": response_status, "body": _json_safe(response_body)}
    except Exception as exc:
        result_status = "BLOCKED"
        result_failure = "FIXTURE_HANDLER_FAILED"
        evidence["handler_status"] = "FAIL"
        evidence["handler_reason"] = str(exc)
        response = {"status": response_status, "body": _json_safe(response_body)}
    try:
        if callable(cleanup):
            _invoke_callback(cleanup, callback_values)
            evidence["cleanup_status"] = "PASS"
        elif capability.get("lifecycle", {}).get("cleanup_declared"):
            evidence["cleanup_status"] = "declared"
    except Exception as exc:  # fixture cleanup is a release gate, not a best-effort log.
        evidence["cleanup_status"] = "FAIL"
        evidence["cleanup_reason"] = str(exc)
        evidence["cleanup_run_id"] = effective_run_id
        return ExecutionResult(interface.operation_id, "BLOCKED", request, response, evidence, "FIXTURE_CLEANUP_FAILED")
    return ExecutionResult(interface.operation_id, result_status, request, response, evidence, result_failure)


def _rpc_http(interface: Any, params: Mapping[str, Any], env: Mapping[str, str], protocol: str) -> ExecutionResult:
    """[参数] interface/params/env/protocol: RPC 入口和 local 配置；[返回] HTTP 承载 RPC 结果；最近修改时间: 2026-07-12 19:30:00 复用标准库请求。"""

    endpoint_ref = str(interface.entrypoint.get("endpoint_ref", "endpoint"))
    endpoint = env.get(endpoint_ref)
    uses_local_config = endpoint_ref == "local_config" and bool(env.get("local_config"))
    config_environment = str(env.get("config_environment", "")).strip().lower()
    local_environment = config_environment in {"local", "local-dev", "development"}
    if config_environment and not local_environment:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"params": dict(params)}, {}, {"reason": "RPC endpoint provenance is not local", "protocol": protocol}, "LOCAL_CONFIG_PROVENANCE_INVALID")
    if endpoint is None and not uses_local_config:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"params": dict(params)}, {}, {"reason": "RPC endpoint must come from explicit local config", "protocol": protocol}, "LOCAL_CONFIG_PROVENANCE_INVALID")
    # 自定义 endpoint 引用必须带显式 local provenance；缺省环境名不能默认为 local。
    if not uses_local_config and not local_environment:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"params": dict(params)}, {}, {"reason": "RPC endpoint provenance is not local", "protocol": protocol}, "LOCAL_CONFIG_PROVENANCE_INVALID")
    endpoint = str(endpoint if endpoint is not None else env.get("local_config", ""))
    if not endpoint:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"params": dict(params)}, {}, {"reason": "local RPC endpoint missing", "protocol": protocol}, "LOCAL_CONFIG_MISSING")
    if protocol == "graphql":
        payload = {"query": interface.entrypoint.get("query", ""), "variables": dict(params), "operationName": interface.entrypoint.get("field", "")}
    elif protocol == "jsonrpc":
        payload = {"jsonrpc": "2.0", "id": interface.operation_id, "method": interface.entrypoint.get("method", interface.operation_id), "params": dict(params)}
    else:
        payload = {"request": dict(params)}
    if protocol == "soap":
        method = interface.entrypoint.get("method", interface.operation_id)
        payload = {"xml": f"<soap:Envelope xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><{method}>{json.dumps(dict(params), ensure_ascii=False)}</{method}></soap:Body></soap:Envelope>"}
        data = str(payload["xml"]).encode("utf-8")
        headers = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": str(interface.entrypoint.get("soap_action_ref", method))}
    else:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json"}
    try:
        auth = resolve_auth(interface.auth, environment="local", environ=env or os.environ)
        headers = merge_auth_headers(headers, auth)
    except AuthResolutionError as exc:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"url": endpoint, "protocol": protocol}, {}, {"reason": str(exc), "protocol": protocol}, "LOCAL_AUTH_UNAVAILABLE")
    request = urllib.request.Request(endpoint, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                body = json.loads(raw)
            except ValueError:
                body = {"raw": raw}
            return ExecutionResult(interface.operation_id, "PASS", {"url": endpoint, "protocol": protocol, "payload": payload}, {"status": response.status, "body": body}, {"transport": "urllib", "protocol": protocol})
    except urllib.error.HTTPError as exc:
        return ExecutionResult(interface.operation_id, "FAIL", {"url": endpoint, "protocol": protocol, "payload": payload}, {"status": exc.code, "body": exc.read().decode("utf-8", errors="replace")}, {"transport": "urllib", "protocol": protocol}, "RPC_HTTP_ERROR")
    except (OSError, urllib.error.URLError) as exc:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"url": endpoint, "protocol": protocol, "payload": payload}, {}, {"transport": "urllib", "protocol": protocol, "reason": str(exc)}, "LOCAL_SERVICE_UNAVAILABLE")


def execute(interface: Any, params: Mapping[str, Any] | None = None, *, environment: str = "local", env: Mapping[str, str] | None = None, dry_run: bool = False, strict_fixture: bool = False, run_id: str | None = None) -> ExecutionResult:
    """[参数] interface/params/environment/env/dry_run/strict_fixture/run_id: 入口、参数、环境、配置、试运行、严格开关和批次 ID；[返回] 结构化结果。"""

    params = params or {}
    env = env or {}
    decision = check_operation({"interface": interface.to_dict(), "params": dict(params)}, environment=environment)
    if not decision.allowed:
        return ExecutionResult(interface.operation_id, "BLOCKED", {"params": dict(params)}, {}, {"rule": decision.rule, "reason": decision.reason}, decision.rule)
    if dry_run:
        return ExecutionResult(interface.operation_id, "PENDING", {"params": dict(params), "entrypoint": dict(interface.entrypoint)}, {}, {"reason": "dry-run; request not sent", "protocol": interface.protocol}, "DRY_RUN")
    fixture = _fixture(interface, params, strict_fixture=strict_fixture, run_id=run_id)
    if fixture is not None:
        return fixture
    if interface.protocol == "http":
        return _http(interface, params, env)
    if interface.protocol in {"graphql", "soap", "jsonrpc"}:
        return _rpc_http(interface, params, env, interface.protocol)
    if interface.protocol in {"websocket", "grpc", "message", "scheduler", "event"}:
        return ExecutionResult(interface.operation_id, "PENDING", {"params": dict(params)}, {}, {"reason": f"runner dependency for {interface.protocol} is not installed", "protocol": interface.protocol}, "UNSUPPORTED_ADAPTER")
    if interface.protocol == "cli":
        command = interface.entrypoint.get("command") or env.get(f"cli_command:{interface.entrypoint.get('command_name', '')}")
        if not command:
            return ExecutionResult(interface.operation_id, "PENDING", {"params": dict(params)}, {}, {"reason": "CLI command missing from local config"}, "LOCAL_CONFIG_MISSING")
        try:
            argv = command if isinstance(command, (list, tuple)) else shlex.split(str(command))
            command_decision = check_operation({"argv": argv, "params": dict(params)}, environment=environment)
            if not command_decision.allowed:
                return ExecutionResult(interface.operation_id, "BLOCKED", {"params": dict(params)}, {}, {"rule": command_decision.rule, "reason": command_decision.reason}, command_decision.rule)
            completed = subprocess.run(argv, shell=False, capture_output=True, text=True, timeout=30, env=dict(env) or None, check=False)
            return ExecutionResult(interface.operation_id, "PASS" if completed.returncode == 0 else "FAIL", {"command": command, "params": dict(params)}, {"returncode": completed.returncode, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]}, {"transport": "subprocess"}, "" if completed.returncode == 0 else "CLI_EXIT_NONZERO")
        except (OSError, subprocess.SubprocessError) as exc:
            return ExecutionResult(interface.operation_id, "BLOCKED", {"command": command}, {}, {"reason": str(exc)}, "CLI_UNAVAILABLE")
    return ExecutionResult(interface.operation_id, "PENDING", {"params": dict(params)}, {}, {"reason": f"no adapter for protocol {interface.protocol}"}, "UNSUPPORTED_ADAPTER")
