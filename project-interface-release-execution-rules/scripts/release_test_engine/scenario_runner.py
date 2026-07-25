"""外部场景串行执行器；协议分派与接口级 runner 保持隔离。"""

from __future__ import annotations

import re
import threading
import time
import urllib.error
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Mapping

from .scenario_assertions import ScenarioAssertionError, assert_document, json_pointer
from .local_probe import LocalProbeRegistry
from .report_support import redact_evidence as _redact, safe_report_reason
from .scenario_model import SCENARIO_ACTIONS, ExternalScenario, ScenarioStep, scenario_requires_cleanup
from .transports.http import execute_http_request
from .transports.sse import expect_sse
from .transports.socketio import SocketIORuntime
from .transports.websocket import WebSocketRuntime


class CleanupError(RuntimeError):
    """声明式清理没有完成。"""

    def __init__(self, message: str, reports: list[dict[str, Any]] | None = None) -> None:
        """保存清理失败前已经产生的报告。

        [参数] message: 清理失败摘要；reports: 已完成的清理步骤报告。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，保证清理阻断仍保留可核验证据。
        """

        # 1. 报告与异常一起向 runner 传播，避免阻断结论丢失执行现场。
        super().__init__(message)
        self.reports = reports or []


CAPTURE_PATTERN = re.compile(r"\$\{capture\.([A-Za-z0-9_.-]+)\}")


def _safe_failure_reason(exc: Exception) -> str:
    """提取不携带请求值的协议错误码。

    [参数] exc: 断言或传输阶段捕获的异常。
    [返回] 白名单协议错误码；没有安全错误码时返回通用失败摘要。
    最近修改时间：2026-07-25 21:59:37，复用共享安全摘要并保持协议错误可追踪性。
    """

    # 1. 只有传输层 ValueError 才允许提取注册协议码，断言文本一律使用固定安全摘要。
    if isinstance(exc, ValueError):
        return safe_report_reason(exc)
    return safe_report_reason("deterministic scenario assertion or transport failed")


def _expand(value: Any, captures: Mapping[str, Any]) -> Any:
    """展开声明式配置中的场景捕获值。

    [参数] value: 待展开的配置值；captures: 已完成步骤的结构化捕获值。
    [返回] 保持原类型的完整占位符值，或完成字符串内替换后的配置。
    最近修改时间：2026-07-25 14:23:51，支持 URL 内捕获值并拒绝缺失引用静默变成 None。
    """

    # 1. 完整占位符保留原始类型，供 JSON、form 等结构化负载跨步骤传值。
    if isinstance(value, str):
        matched = CAPTURE_PATTERN.fullmatch(value)
        if matched:
            name = matched.group(1)
            if name not in captures:
                raise ValueError(f"capture is unavailable: {name}")
            return captures[name]

        # 2. 字符串内占位符只做文本替换，适用于 URL 和请求头等文本配置。
        def replace(match: re.Match[str]) -> str:
            """把单个捕获占位符替换为文本值。

            [参数] match: 正则捕获到的占位符。
            [返回] 对应捕获值的字符串形式。
            最近修改时间：2026-07-25 14:23:51，新增 URL 内受限占位符替换。
            """

            # 1. 缺失捕获直接失败，避免携带未展开占位符请求错误资源。
            name = match.group(1)
            if name not in captures:
                raise ValueError(f"capture is unavailable: {name}")
            return str(captures[name])

        return CAPTURE_PATTERN.sub(replace, value)
    if isinstance(value, Mapping):
        return {key: _expand(child, captures) for key, child in value.items()}
    if isinstance(value, list):
        return [_expand(item, captures) for item in value]
    return value


def _execute_action(step: ScenarioStep, config: Mapping[str, Any], environment: str, runtime: Mapping[str, Any], ready_event: threading.Event | None = None) -> dict[str, Any]:
    """执行一个已展开配置的白名单场景动作。

    [参数] step: 场景步骤；config: 已展开配置；environment: 执行环境；runtime: 场景连接运行时；ready_event: 流式订阅就绪信号。
    [返回] 协议传输产生的结构化结果。
    最近修改时间：2026-07-25 14:50:26，增加独立 Socket.IO 动作分派。
    """

    # 1. 动作必须由显式白名单分派，未知运行时不能回退到 fixture 或静态结果。
    if step.action == "http.request":
        return execute_http_request(config, environment)
    if step.action == "sse.expect":
        return expect_sse(config, environment, ready_event=ready_event)
    if step.action == "ws.connect":
        return runtime["websocket"].connect(config, environment)
    if step.action == "ws.send":
        return runtime["websocket"].send(config)
    if step.action == "ws.expect":
        return runtime["websocket"].expect(config)
    if step.action == "ws.close":
        return runtime["websocket"].close(config)
    if step.action == "socketio.connect":
        return runtime["socketio"].connect(config, environment)
    if step.action == "socketio.emit":
        return runtime["socketio"].emit(config)
    if step.action == "socketio.expect":
        return runtime["socketio"].expect(config)
    if step.action == "socketio.disconnect":
        return runtime["socketio"].disconnect(config)
    if step.action == "state.probe":
        return runtime["probe"].execute(config, environment)
    raise NotImplementedError(f"runtime action unavailable: {step.action}")


def _timed_action(step: ScenarioStep, config: Mapping[str, Any], environment: str, runtime: Mapping[str, Any], ready_event: threading.Event | None = None) -> tuple[dict[str, Any], int]:
    """执行动作并记录单步耗时。

    [参数] step: 场景步骤；config: 已展开配置；environment: 执行环境；runtime: 场景连接运行时；ready_event: 流式订阅就绪信号。
    [返回] 动作输出和毫秒耗时。
    最近修改时间：2026-07-25 14:50:26，为多种有状态协议传入同一场景运行时集合。
    """

    # 1. 耗时覆盖完整网络动作，不把排队前的场景准备时间算入步骤。
    started = time.monotonic()
    output = _execute_action(step, config, environment, runtime, ready_event)
    return output, round((time.monotonic() - started) * 1000)


def _execute_parallel_group(steps: tuple[ScenarioStep, ...], captures: Mapping[str, Any], environment: str, runtime: Mapping[str, Any]) -> list[tuple[ScenarioStep, dict[str, Any], int]]:
    """执行一个包含 SSE 订阅者的显式并行组。

    [参数] steps: 同一并行组的连续步骤；captures: 前序捕获值；environment: 执行环境；runtime: 场景连接运行时。
    [返回] 按声明顺序排列的步骤、输出和耗时。
    最近修改时间：2026-07-25 14:50:26，为并行步骤传入多协议场景运行时集合。
    """

    # 1. 当前协议闭环只允许一个订阅者，避免多个流共享触发动作产生关联歧义。
    sse_indexes = [index for index, step in enumerate(steps) if step.action == "sse.expect"]
    if len(sse_indexes) != 1:
        raise ValueError("parallel group requires exactly one sse.expect step")
    expanded = [_expand(step.config, captures) for step in steps]
    ready = threading.Event()
    futures: dict[int, Future[tuple[dict[str, Any], int]]] = {}

    # 2. 先启动 SSE；只有服务端响应头确认订阅成功后，才并发执行其余动作。
    with ThreadPoolExecutor(max_workers=len(steps), thread_name_prefix="external-scenario") as executor:
        # 2.1 订阅 future 单独持有就绪信号，其余 future 在信号到达后才创建。
        sse_index = sse_indexes[0]
        futures[sse_index] = executor.submit(_timed_action, steps[sse_index], expanded[sse_index], environment, runtime, ready)
        ready_timeout = float(expanded[sse_index].get("ready_timeout_seconds", 3))
        if not ready.wait(ready_timeout):
            if futures[sse_index].done():
                futures[sse_index].result()
            raise ValueError("SSE_SUBSCRIPTION_NOT_READY")
        for index, step in enumerate(steps):
            if index != sse_index:
                futures[index] = executor.submit(_timed_action, step, expanded[index], environment, runtime)

        # 3. 结果按声明顺序收集，保证断言、捕获和事件日志具有稳定顺序。
        return [(step, *futures[index].result()) for index, step in enumerate(steps)]


def _run_cleanup(scenario: ExternalScenario, captures: dict[str, Any], environment: str, runtime: Mapping[str, Any]) -> list[dict[str, Any]]:
    """按声明顺序执行场景清理，并把失败升级为阻断。

    [参数] scenario: 已验证场景；captures: 主流程捕获值；environment: 执行环境；runtime: 场景运行时集合。
    [返回] 脱敏清理步骤报告。
    最近修改时间：2026-07-25 23:50:00，清理断言失败只持久化安全摘要。
    """

    reports: list[dict[str, Any]] = []
    for index, raw in enumerate(scenario.cleanup):
        # 1. 清理动作仍走同一白名单 runner，禁止清理配置嵌入任意代码或 SQL。
        if not isinstance(raw, Mapping):
            raise CleanupError("CLEANUP_CONTRACT_INVALID")
        action = str(raw.get("action", ""))
        if action not in SCENARIO_ACTIONS or action in {"cleanup", "state.probe"}:
            raise CleanupError("CLEANUP_ACTION_NOT_ALLOWED")
        config = _expand(raw.get("config", {}), captures)
        if not isinstance(config, Mapping):
            raise CleanupError("CLEANUP_CONFIG_INVALID")
        step = ScenarioStep(
            step_id=str(raw.get("step_id", f"cleanup-{index + 1}")),
            action=action,
            config=dict(config),
            captures=dict(raw.get("captures", {})) if isinstance(raw.get("captures", {}), Mapping) else {},
            assertions=tuple(raw.get("assertions", ())) if isinstance(raw.get("assertions", ()), (list, tuple)) else (),
        )
        output, duration_ms = _timed_action(step, config, environment, runtime)
        try:
            assert_document(output, step.assertions)
        except (ScenarioAssertionError, ValueError) as exc:
            reports.append({"step_id": step.step_id, "action": action, "status": "FAIL", "duration_ms": duration_ms, "failure_type": "CLEANUP_ASSERTION_FAILED", "reason": _safe_failure_reason(exc), "output": _redact(output)})
            raise CleanupError("CLEANUP_ASSERTION_FAILED", reports) from exc
        for name, pointer in step.captures.items():
            captures[name] = json_pointer(output, pointer)
        reports.append({"step_id": step.step_id, "action": action, "status": "PASS", "duration_ms": duration_ms, "output": _redact(output)})
    return reports


def run_scenario(scenario: ExternalScenario, *, environment: str = "local", probe_registry: LocalProbeRegistry | None = None) -> dict[str, Any]:
    """按声明顺序执行场景，返回场景级而非接口级结果。

    [参数] scenario: 已加载的外部消费者场景；environment: 执行环境名称；probe_registry: 项目显式注册的只读探针。
    [返回] 场景状态、步骤证据和脱敏捕获值。
    最近修改时间：2026-07-25 21:59:37，把超时和拒绝连接归一化为结构化场景失败。
    """

    # 1. 初始化一次场景运行的身份、协议运行时和脱敏结果容器。
    run_id = uuid.uuid4().hex
    runtime = {"websocket": WebSocketRuntime(), "socketio": SocketIORuntime(), "probe": probe_registry or LocalProbeRegistry()}
    captures: dict[str, Any] = {}
    step_results: list[dict[str, Any]] = []
    started = time.monotonic()
    status = "PASS"
    failure_type = ""
    reason = "all deterministic assertions passed"
    cleanup_results: list[dict[str, Any]] = []
    try:
        # 2. 前置条件必须与当前 local 运行一致，未知或不满足的条件不能被静默跳过。
        if any(condition.get("environment") != environment for condition in scenario.preconditions):
            raise PermissionError("SCENARIO_PRECONDITION_BLOCKED")
        # 3. 候选或漂移场景只能验证，不能伪装为正式门禁运行。
        if scenario.lifecycle != "verified":
            status, failure_type, reason = "PENDING", "SCENARIO_NOT_VERIFIED", f"scenario lifecycle is {scenario.lifecycle}"
            return {"run_id": run_id, "scenario_id": scenario.scenario_id, "risk": scenario.risk, "consumers": list(scenario.consumers), "source_fingerprint": scenario.source_fingerprint, "cleanup_required": scenario_requires_cleanup(scenario), "status": status, "failure_type": failure_type, "reason": reason, "steps": [], "captures": {}, "cleanup": []}
        # 4. 默认保持串行；只有连续步骤显式声明同一并行组时才并发。
        index = 0
        while index < len(scenario.steps):
            step = scenario.steps[index]
            if step.parallel_group:
                # 4.1 连续同名并行组作为一个批次执行，其余步骤保持逐条串行。
                end = index + 1
                while end < len(scenario.steps) and scenario.steps[end].parallel_group == step.parallel_group:
                    end += 1
                executions = _execute_parallel_group(scenario.steps[index:end], captures, environment, runtime)
                index = end
            else:
                config = _expand(step.config, captures)
                output, duration_ms = _timed_action(step, config, environment, runtime)
                executions = [(step, output, duration_ms)]
                index += 1

            # 5. 即使并行执行，断言、捕获和日志也按场景声明顺序确定性落位。
            for executed_step, output, duration_ms in executions:
                # 5.1 当前步骤先完成断言与捕获，再生成脱敏日志，避免失败证据被记为 PASS。
                assert_document(output, executed_step.assertions)
                for name, pointer in executed_step.captures.items():
                    captures[name] = json_pointer(output, pointer)
                step_results.append({"run_id": run_id, "scenario_id": scenario.scenario_id, "step_id": executed_step.step_id, "action": executed_step.action, "status": "PASS", "duration_ms": duration_ms, "failure_type": "", "output": _redact(output)})
        # 6. 场景级断言使用结构化上下文，防止依赖非确定性自然语言判断。
        assert_document({"captures": captures, "steps": step_results}, scenario.assertions)
    except PermissionError as exc:
        status, failure_type, reason = "BLOCKED", str(exc), str(exc)
    except (ScenarioAssertionError, ValueError) as exc:
        # 7. 失败原因只保留白名单协议错误码，禁止把断言实际值、URL 或鉴权内容写入正式结果。
        status, failure_type, reason = "FAIL", "SCENARIO_ASSERTION_FAILED", _safe_failure_reason(exc)
    except (urllib.error.URLError, OSError) as exc:
        # 7.1 HTTP 超时和实时端口拒绝连接必须返回结构化 FAIL，禁止原始网络异常逃逸 CLI。
        status, failure_type, reason = "FAIL", "SCENARIO_TRANSPORT_FAILED", _safe_failure_reason(exc)
    except (ImportError, NotImplementedError):
        status, failure_type, reason = "PENDING", "PROTOCOL_RUNTIME_UNAVAILABLE", "required protocol runtime is unavailable"
    finally:
        # 8. 主流程失败也必须执行声明清理，清理失败优先升级为 BLOCKED。
        if scenario.lifecycle == "verified":
            # 8.1 只有 verified 场景执行声明清理，任何清理异常都覆盖主流程结论为阻断。
            try:
                cleanup_results = _run_cleanup(scenario, captures, environment, runtime)
            except (CleanupError, PermissionError, ScenarioAssertionError, urllib.error.URLError, OSError, ValueError, ImportError, NotImplementedError) as exc:
                cleanup_results = getattr(exc, "reports", cleanup_results)
                status, failure_type, reason = "BLOCKED", "CLEANUP_FAILED", "declared cleanup did not complete"

        # 9. 无论成功、断言失败或协议异常，都回收当前场景创建的实时连接。
        runtime["websocket"].close_all()
        runtime["socketio"].close_all()
    # 10. 把声明中的消费者身份带入结果，覆盖报告才能按真实消费者统计而不是按接口猜测。
    return {"run_id": run_id, "scenario_id": scenario.scenario_id, "risk": scenario.risk, "consumers": list(scenario.consumers), "source_fingerprint": scenario.source_fingerprint, "cleanup_required": scenario_requires_cleanup(scenario), "status": status, "failure_type": failure_type, "reason": reason, "duration_ms": round((time.monotonic() - started) * 1000), "steps": step_results, "captures": _redact(captures), "cleanup": cleanup_results}
