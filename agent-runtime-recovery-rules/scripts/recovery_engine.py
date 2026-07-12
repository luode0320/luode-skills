"""平台无关的智能体运行期恢复编排器。

本模块只消费 adapter 的声明和回调，不猜测宿主命令、进程名或 UI 操作。
它把探针、能力准入、单飞锁、L2-L4 单次动作和安全终态收敛成一个最小入口。
"""

from __future__ import annotations

import importlib.util
import hashlib
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol


_STATE_MODULE_PATH = Path(__file__).with_name("recovery_state.py")
_STATE_SPEC = importlib.util.spec_from_file_location("agent_runtime_recovery_state", _STATE_MODULE_PATH)
if _STATE_SPEC is None or _STATE_SPEC.loader is None:
    raise ImportError(f"unable to load recovery state module: {_STATE_MODULE_PATH}")
_STATE_MODULE = importlib.util.module_from_spec(_STATE_SPEC)
_STATE_SPEC.loader.exec_module(_STATE_MODULE)


IDEMPOTENT_CLASSES = {"read_only", "idempotent", "idempotent_with_key"}
ACTION_LEVELS = (
    (2, "reconnect", "reconnected"),
    (3, "reload", "reloaded"),
    (4, "restart", "restarted"),
)
TERMINAL_RESULTS = {"healthy", "resumed", "manual_handoff", "blocked"}


class RecoveryRequest:
    """定义一次恢复请求的最小控制字段。

    [参数] recovery_id：恢复操作标识；task_id_hash：脱敏任务标识；component_id：组件标识；
    scope：调用方拥有的组件作用域；idempotency_class：原操作幂等类别；
    failure_class：失败分类；success_criterion：原操作成功标准；idempotency_key：可选去重键。
    [返回] 不返回值；实例只保存控制信息，不应放入原始 prompt、响应或凭据。
    最近修改时间：2026-07-12 22:00:00；新增最小运行期恢复编排入口。
    """

    __slots__ = (
        "recovery_id",
        "task_id_hash",
        "component_id",
        "scope",
        "idempotency_class",
        "failure_class",
        "success_criterion",
        "idempotency_key",
        "metadata",
    )

    def __init__(
        self,
        recovery_id: str,
        task_id_hash: str,
        component_id: str,
        scope: str,
        idempotency_class: str,
        failure_class: str = "runtime_failure",
        success_criterion: str = "",
        idempotency_key: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        """初始化恢复请求，默认不保存可变元数据引用。

        [参数] 字段含义与类说明一致；metadata：可选脱敏控制元数据。
        [返回] 无；字段只作为 adapter 回调输入。
        最近修改时间：2026-07-12 22:05:00；兼容未注册模块的动态加载。
        """

        self.recovery_id = recovery_id
        self.task_id_hash = task_id_hash
        self.component_id = component_id
        self.scope = scope
        self.idempotency_class = idempotency_class
        self.failure_class = failure_class
        self.success_criterion = success_criterion
        self.idempotency_key = idempotency_key
        self.metadata = dict(metadata or {})


class InvocationResult:
    """归一化 adapter 操作结果，避免引擎依赖平台返回类型。

    [参数] ok：操作是否成功；healthy：探针/就绪检查是否健康；reason：脱敏原因；
    evidence：可选的非敏感诊断字段。
    [返回] 不返回值；实例供 `RecoveryEngine` 进行结果判断。
    最近修改时间：2026-07-12 22:00:00；新增 adapter 结果归一化。
    """

    __slots__ = ("ok", "healthy", "reason", "evidence", "success_criterion_verified")

    def __init__(
        self,
        ok: bool,
        healthy: bool | None = None,
        reason: str = "",
        evidence: Mapping[str, Any] | None = None,
        success_criterion_verified: bool | None = None,
    ) -> None:
        """初始化归一化 adapter 结果。

        [参数] ok：操作结果；healthy：健康结果；reason：脱敏原因；evidence：非敏感证据。
        [返回] 无；字段供引擎读取。
        最近修改时间：2026-07-12 22:05:00；兼容未注册模块的动态加载。
        """

        self.ok = ok
        self.healthy = healthy
        self.reason = reason
        self.evidence = dict(evidence or {})
        self.success_criterion_verified = success_criterion_verified


class RecoveryAdapter(Protocol):
    """平台 adapter 的最小运行时接口。"""

    contract: Mapping[str, Any]

    def invoke(
        self,
        operation: str,
        component: Mapping[str, Any],
        request: RecoveryRequest,
    ) -> InvocationResult | Mapping[str, Any] | bool:
        """执行 contract 已声明的单次操作。

        [参数] operation：操作名；component：组件声明；request：恢复请求。
        [返回] 操作结果，可为归一化结果、结构化字典或布尔值。
        最近修改时间：2026-07-12 22:10:00；补齐 adapter 接口注释元信息。
        """


class RecoveryEngine:
    """按照统一协议执行一次受控恢复，不负责重放原业务请求。"""

    def __init__(
        self,
        adapter: RecoveryAdapter,
        checkpoint_path: Path,
        state_module: Any = _STATE_MODULE,
    ) -> None:
        """初始化编排器。

        [参数] adapter：带 contract/invoke 的平台适配器；checkpoint_path：持久化检查点；
        state_module：可注入的检查点原语模块，默认加载本目录 `recovery_state.py`。
        [返回] 不返回值；仅保存依赖，不执行任何平台动作。
        最近修改时间：2026-07-12 22:00:00；新增最小运行期恢复编排入口。
        """

        self.adapter = adapter
        self.checkpoint_path = Path(checkpoint_path)
        self.state = state_module

    def recover(self, request: RecoveryRequest) -> dict[str, Any]:
        """执行探针、能力检查和最多一轮 L2-L4 恢复动作。

        [参数] request：本次故障的脱敏恢复请求。
        [返回] 结构化结果，`status` 仅为 `healthy`、`resumed`、`manual_handoff` 或 `blocked`；
        同时包含动作、探针计数和原因，供上层 agent 决定是否继续任务。
        最近修改时间：2026-07-12 22:00:00；新增恢复编排主流程。
        """

        request_error = self._validate_request(request)
        if request_error:
            return self._result("blocked", request_error, request)

        contract = getattr(self.adapter, "contract", None)
        component, contract_error = self._find_component(contract, request)
        if contract_error:
            return self._result("blocked", contract_error, request)
        assert component is not None

        limit_error = self._validate_limits(contract)
        if limit_error:
            return self._result("blocked", limit_error, request)
        if not self._operation_supported(contract, component, "probe", 1):
            return self._result("blocked", "probe_capability_missing", request)

        checkpoint_error = self._prepare_checkpoint(contract, component, request)
        if checkpoint_error:
            return self._result("blocked", checkpoint_error, request)

        try:
            lock_ttl = contract["limits"]["lock_ttl_seconds"]
            self.state.claim(self.checkpoint_path, request.recovery_id, ttl_seconds=lock_ttl)
        except (RuntimeError, ValueError, OSError):
            return self._result("blocked", "single_flight_lock_unavailable", request)

        attempted_actions: list[str] = []
        skipped_actions: list[str] = []
        probe_attempts = 0
        verification_attempts = 0
        try:
            # 1. 先做一次故障探针，再做一次不变复验；两次都失败才进入恢复态。
            first_probe = self._invoke("probe", component, request)
            probe_attempts += 1
            if self._is_healthy(first_probe):
                self._transition("healthy")
                return self._result("healthy", "probe_recovered", request, probe_attempts=probe_attempts)
            second_probe = self._invoke("probe", component, request)
            probe_attempts += 1
            if self._is_healthy(second_probe):
                self._transition("healthy")
                return self._result("healthy", "unchanged_reprobe_recovered", request, probe_attempts=probe_attempts)

            self._transition("diagnosed")
            if request.idempotency_class not in IDEMPOTENT_CLASSES:
                self._transition("manual_handoff")
                return self._result(
                    "manual_handoff",
                    "non_idempotent_or_unknown_operation",
                    request,
                    probe_attempts=probe_attempts,
                )
            if request.idempotency_class == "idempotent_with_key" and not request.idempotency_key:
                self._transition("manual_handoff")
                return self._result(
                    "manual_handoff",
                    "idempotency_key_missing",
                    request,
                    probe_attempts=probe_attempts,
                )

            self._transition("recovering")
            for level, operation, recovered_state in ACTION_LEVELS:
                if not self._operation_supported(contract, component, operation, level):
                    skipped_actions.append(operation)
                    continue
                if not self._operation_supported(contract, component, "wait_ready", 1):
                    skipped_actions.append("wait_ready")
                    break

                # 2. 每个恢复层最多调用一次；失败后才允许尝试更高一层。
                attempted_actions.append(operation)
                action_result = self._invoke(operation, component, request)
                if not action_result.ok:
                    continue
                ready_result = self._invoke("wait_ready", component, request)
                if not ready_result.ok:
                    continue
                verification = self._invoke("probe", component, request)
                verification_attempts += 1
                if not self._is_healthy(verification):
                    continue

                self._transition(recovered_state)
                self._transition("verified")
                l5_result = self._try_resume(component, contract, request)
                if l5_result is not None:
                    return self._result(
                        l5_result[0],
                        l5_result[1],
                        request,
                        attempted_actions=attempted_actions,
                        skipped_actions=skipped_actions,
                        probe_attempts=probe_attempts,
                        verification_attempts=verification_attempts,
                        recovery_level=level,
                    )
                # L2-L4 只证明工具链恢复；没有完整 L5 hook 时必须人工交接。
                self._transition("manual_handoff")
                return self._result(
                    "manual_handoff",
                    "tool_recovered_resume_not_supported",
                    request,
                    attempted_actions=attempted_actions,
                    skipped_actions=skipped_actions,
                    probe_attempts=probe_attempts,
                    verification_attempts=verification_attempts,
                    recovery_level=level,
                )

            self._transition("blocked")
            return self._result(
                "blocked",
                "recovery_budget_exhausted_or_capability_unavailable",
                request,
                attempted_actions=attempted_actions,
                skipped_actions=skipped_actions,
                probe_attempts=probe_attempts,
                verification_attempts=verification_attempts,
            )
        finally:
            try:
                self.state.release(self.checkpoint_path, request.recovery_id)
            except (RuntimeError, ValueError, OSError):
                # 3. 释放失败不伪造恢复成功；检查点中的锁 TTL 负责最终清理。
                pass

    def _validate_request(self, request: RecoveryRequest) -> str | None:
        """检查恢复请求的标识和幂等类别。

        [参数] request：待检查的恢复请求。
        [返回] 缺口原因；合法时返回 None。
        最近修改时间：2026-07-12 22:00:00；新增请求准入检查。
        """

        for name in ("recovery_id", "task_id_hash", "component_id", "scope"):
            if not isinstance(getattr(request, name, None), str) or not getattr(request, name):
                return f"request_{name}_missing"
        if request.idempotency_class not in IDEMPOTENT_CLASSES | {"non_idempotent"}:
            return "idempotency_class_unknown"
        return None

    def _find_component(
        self,
        contract: Mapping[str, Any] | None,
        request: RecoveryRequest,
    ) -> tuple[Mapping[str, Any] | None, str | None]:
        """从 adapter 契约中查找并校验当前任务拥有的组件作用域。

        [参数] contract：adapter 声明；request：当前恢复请求。
        [返回] `(component, error)`；作用域不完全匹配或契约缺失时返回错误。
        最近修改时间：2026-07-12 22:00:00；新增 capability 与 scope 准入。
        """

        if not isinstance(contract, Mapping):
            return None, "adapter_contract_missing"
        for field_name in ("adapter_id", "platform_id", "version", "components", "operations", "limits"):
            if field_name not in contract:
                return None, f"adapter_contract_{field_name}_missing"
        components = contract.get("components")
        if not isinstance(components, list):
            return None, "adapter_components_invalid"
        for item in components:
            if not isinstance(item, Mapping) or item.get("component_id") != request.component_id:
                continue
            if item.get("scope") != request.scope:
                return None, "component_scope_mismatch"
            capability_level = item.get("capability_level")
            if not isinstance(capability_level, int) or not 0 <= capability_level <= 5:
                return None, "component_capability_level_invalid"
            if not isinstance(item.get("capabilities", []), list):
                return None, "component_capabilities_invalid"
            return item, None
        return None, "component_not_registered"

    def _validate_limits(self, contract: Mapping[str, Any]) -> str | None:
        """拒绝突破全局单次预算的 adapter 声明。

        [参数] contract：待检查的 adapter 契约。
        [返回] 预算错误原因；合法时返回 None。
        最近修改时间：2026-07-12 22:00:00；新增预算上限保护。
        """

        limits = contract.get("limits")
        if not isinstance(limits, Mapping):
            return "adapter_limits_invalid"
        for name in ("max_probe_attempts", "max_retries_per_level", "cooldown_seconds", "lock_ttl_seconds"):
            if not isinstance(limits.get(name), int) or limits[name] < 1:
                return f"adapter_limit_{name}_invalid"
        if limits["max_probe_attempts"] > 1 or limits["max_retries_per_level"] > 1:
            return "adapter_limits_exceed_global_budget"
        return None

    def _operation_supported(
        self,
        contract: Mapping[str, Any],
        component: Mapping[str, Any],
        operation: str,
        minimum_level: int,
    ) -> bool:
        """同时检查组件等级、能力列表和操作声明。

        [参数] contract：adapter 契约；component：目标组件；operation：操作名；minimum_level：最低等级。
        [返回] 只有三项均真实声明并支持时返回 True。
        最近修改时间：2026-07-12 22:00:00；新增动作准入检查。
        """

        if component.get("capability_level", 0) < minimum_level:
            return False
        capabilities = component.get("capabilities", [])
        if operation not in capabilities:
            return False
        operations = contract.get("operations")
        operation_spec = operations.get(operation) if isinstance(operations, Mapping) else None
        return (
            isinstance(operation_spec, Mapping)
            and operation_spec.get("supported") is True
            and isinstance(operation_spec.get("entrypoint"), str)
            and bool(operation_spec.get("entrypoint"))
            and isinstance(operation_spec.get("success_criteria"), str)
            and bool(operation_spec.get("success_criteria"))
        )

    def _prepare_checkpoint(
        self,
        contract: Mapping[str, Any],
        component: Mapping[str, Any],
        request: RecoveryRequest,
    ) -> str | None:
        """创建或复用同一恢复标识的检查点，并拒绝覆盖其他任务状态。

        [参数] contract：adapter 契约；component：目标组件；request：当前恢复请求。
        [返回] 检查点冲突原因；可创建或复用时返回 None。
        最近修改时间：2026-07-12 22:00:00；新增检查点生命周期接入。
        """

        if self.checkpoint_path.exists():
            try:
                reader = getattr(self.state, "read_checkpoint", None)
                if not callable(reader):
                    reader = getattr(self.state, "_read", None)
                if not callable(reader):
                    return "checkpoint_reader_missing"
                record = reader(self.checkpoint_path)
            except (OSError, ValueError, TypeError):
                return "checkpoint_invalid"
            if record.get("recovery_id") != request.recovery_id:
                return "checkpoint_owned_by_other_recovery"
            if record.get("state") in {"healthy", "resumed", "manual_handoff", "blocked"}:
                return "checkpoint_terminal"
            return None
        payload = {
            "recovery_id": request.recovery_id,
            "task_id_hash": request.task_id_hash,
            "component_id": request.component_id,
            "scope_hash": hashlib.sha256(request.scope.encode("utf-8")).hexdigest(),
            "idempotency_class": request.idempotency_class,
            "platform_id": contract.get("platform_id"),
            "adapter_id": contract.get("adapter_id"),
            "failure_class": request.failure_class,
        }
        try:
            self.state.create_checkpoint(self.checkpoint_path, payload)
        except (ValueError, OSError, TypeError):
            return "checkpoint_create_failed"
        return None

    def _invoke(
        self,
        operation: str,
        component: Mapping[str, Any],
        request: RecoveryRequest,
    ) -> InvocationResult:
        """调用 adapter 一次并把异常归一化为失败结果。

        [参数] operation：已准入的操作；component：组件声明；request：恢复请求。
        [返回] 不抛出 adapter 异常，统一返回 `InvocationResult`。
        最近修改时间：2026-07-12 22:00:00；新增单次 adapter 调用边界。
        """

        invoke: Callable[..., Any] | None = getattr(self.adapter, "invoke", None)
        if not callable(invoke):
            return InvocationResult(False, reason="adapter_invoke_missing")
        try:
            raw = invoke(operation, component, request)
        except Exception as exc:  # noqa: BLE001 - adapter 边界必须隔离平台异常。
            return InvocationResult(False, reason=f"{operation}_exception:{type(exc).__name__}")
        if isinstance(raw, InvocationResult):
            return raw
        if isinstance(raw, bool):
            return InvocationResult(raw, healthy=raw)
        if isinstance(raw, Mapping):
            ok = raw.get("ok")
            healthy = raw.get("healthy")
            if not isinstance(ok, bool):
                ok = bool(healthy) if isinstance(healthy, bool) else False
            if not isinstance(healthy, (bool, type(None))):
                healthy = None
            criterion_verified = raw.get("success_criterion_verified")
            if not isinstance(criterion_verified, (bool, type(None))):
                criterion_verified = None
            return InvocationResult(
                ok,
                healthy=healthy,
                reason=str(raw.get("reason", "")),
                evidence={},
                success_criterion_verified=criterion_verified,
            )
        return InvocationResult(False, reason="adapter_result_invalid")

    def _try_resume(
        self,
        component: Mapping[str, Any],
        contract: Mapping[str, Any],
        request: RecoveryRequest,
    ) -> tuple[str, str] | None:
        """尝试 L5 检查点续接并要求 adapter 明确验证原成功标准。

        [参数] component：已恢复的组件；contract：adapter 契约；request：原恢复请求。
        [返回] `(status, reason)` 终态；缺少 L5 能力时返回 None，由调用方转人工交接。
        最近修改时间：2026-07-12 22:10:00；新增检查点续接编排。
        """

        if not request.success_criterion:
            return None
        if request.idempotency_class not in IDEMPOTENT_CLASSES:
            return None
        if request.idempotency_class == "idempotent_with_key" and not request.idempotency_key:
            return None
        if not self._operation_supported(contract, component, "checkpoint", 5):
            return None
        if not self._operation_supported(contract, component, "resume", 5):
            return None

        checkpoint_result = self._invoke("checkpoint", component, request)
        if not checkpoint_result.ok:
            self._transition("manual_handoff")
            return "manual_handoff", "checkpoint_action_failed"
        resume_result = self._invoke("resume", component, request)
        if not resume_result.ok:
            self._transition("manual_handoff")
            return "manual_handoff", "resume_action_failed"
        if resume_result.success_criterion_verified is not True:
            self._transition("manual_handoff")
            return "manual_handoff", "resume_success_criterion_unverified"
        self._transition("resumed")
        return "resumed", "checkpoint_resume_success_criterion_verified"

    @staticmethod
    def _is_healthy(result: InvocationResult) -> bool:
        """判断探针或最小健康调用是否通过。

        [参数] result：归一化 adapter 结果。
        [返回] 显式 healthy 优先，否则使用 ok。
        最近修改时间：2026-07-12 22:00:00；新增健康结果判断。
        """

        return result.healthy if result.healthy is not None else result.ok

    def _transition(self, target: str) -> None:
        """尝试推进检查点状态，保留状态机拒绝而不伪造成功。

        [参数] target：状态机允许的目标状态。
        [返回] 无；状态迁移失败由调用方的终态处理覆盖。
        最近修改时间：2026-07-12 22:00:00；新增状态机编排辅助。
        """

        self.state.transition(self.checkpoint_path, target)

    @staticmethod
    def _result(status: str, reason: str, request: RecoveryRequest, **extra: Any) -> dict[str, Any]:
        """构造不含原始请求内容的结构化编排结果。

        [参数] status：恢复终态；reason：脱敏原因；request：恢复请求；extra：计数和动作信息。
        [返回] 可序列化的结果字典。
        最近修改时间：2026-07-12 22:00:00；新增统一结果格式。
        """

        result: dict[str, Any] = {
            "status": status if status in TERMINAL_RESULTS else "blocked",
            "reason": reason,
            "recovery_id": request.recovery_id,
            "component_id": request.component_id,
        }
        result.update(extra)
        return result


__all__ = ["InvocationResult", "RecoveryAdapter", "RecoveryEngine", "RecoveryRequest"]
