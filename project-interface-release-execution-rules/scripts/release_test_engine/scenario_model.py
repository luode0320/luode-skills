"""外部消费者场景的版本化模型。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


SCENARIO_SCHEMA_VERSION = "external-scenario/1.0"
SCENARIO_LIFECYCLES = {"candidate", "verified", "stale", "quarantined", "retired"}
SCENARIO_RISKS = {"P0", "P1", "P2"}
SCENARIO_ACTIONS = {
    "http.request",
    "sse.expect",
    "ws.connect",
    "ws.send",
    "ws.expect",
    "ws.close",
    "socketio.connect",
    "socketio.emit",
    "socketio.expect",
    "socketio.disconnect",
    "state.probe",
    "cleanup",
}


class ScenarioValidationError(ValueError):
    """场景资产不符合白名单契约。"""

    def __init__(self, errors: list[str]):
        """保存全部场景契约错误并生成稳定异常摘要。

        [参数] errors: loader 聚合的契约错误列表。
        [返回] 无。
        最近修改时间：2026-07-25 21:00:00，补齐契约异常的聚合输入说明。
        """

        self.errors = errors
        super().__init__("invalid external scenario: " + "; ".join(errors))


@dataclass(frozen=True)
class ScenarioStep:
    """一个可执行的白名单场景步骤。"""

    step_id: str
    action: str
    config: Mapping[str, Any] = field(default_factory=dict)
    captures: Mapping[str, str] = field(default_factory=dict)
    assertions: tuple[Mapping[str, Any], ...] = ()
    parallel_group: str = ""

    def to_dict(self) -> dict[str, Any]:
        """把不可变步骤转换为可序列化契约映射。

        [参数] 无。
        [返回] 保留动作、配置、捕获、断言和并行组的步骤映射。
        最近修改时间：2026-07-25 21:00:00，补齐步骤序列化字段边界。
        """

        # 1. 身份、动作和执行配置作为同一字段组稳定输出。
        return {
            "step_id": self.step_id,
            "action": self.action,
            "config": dict(self.config),
            # 2. 捕获、断言和并行声明作为结果处理字段组输出。
            "captures": dict(self.captures),
            "assertions": [dict(item) for item in self.assertions],
            "parallel_group": self.parallel_group,
        }


@dataclass(frozen=True)
class ExternalScenario:
    """一个消费者视角的端到端场景。"""

    scenario_id: str
    risk: str
    consumers: tuple[str, ...]
    source_evidence: tuple[Mapping[str, Any], ...]
    source_fingerprint: str
    lifecycle: str
    preconditions: tuple[Mapping[str, Any], ...]
    steps: tuple[ScenarioStep, ...]
    assertions: tuple[Mapping[str, Any], ...]
    cleanup: tuple[Mapping[str, Any], ...]
    verification: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """把消费者场景转换为 external-scenario/1.0 场景映射。

        [参数] 无。
        [返回] 包含身份、来源、生命周期、步骤、清理和验证门槛的映射。
        最近修改时间：2026-07-25 21:00:00，补齐场景序列化字段分组和完整性说明。
        """

        # 1. 先输出场景身份、风险和消费者。
        return {
            "scenario_id": self.scenario_id,
            "risk": self.risk,
            "consumers": list(self.consumers),
            # 2. 来源证据、指纹和生命周期共同决定场景是否仍可执行。
            "source_evidence": [dict(item) for item in self.source_evidence],
            "source_fingerprint": self.source_fingerprint,
            "lifecycle": self.lifecycle,
            # 3. 前置条件、主步骤、整体断言和清理定义执行闭环。
            "preconditions": [dict(item) for item in self.preconditions],
            "steps": [item.to_dict() for item in self.steps],
            "assertions": [dict(item) for item in self.assertions],
            "cleanup": [dict(item) for item in self.cleanup],
            # 4. 五项验证门槛作为生命周期晋级证据单独输出。
            "verification": dict(self.verification),
        }


def scenario_requires_cleanup(scenario: ExternalScenario) -> bool:
    """判断场景是否包含必须清理的 HTTP 写入。

    [参数] scenario: 已加载的外部消费者场景。
    [返回] 任一步骤使用非安全 HTTP 方法时返回 True。
    最近修改时间: 2026-07-25 19:30:00 改动原因: 清理门禁不能把写场景的空清理数组解释为成功。
    """

    # 1. GET/HEAD/OPTIONS 视为只读，其余 HTTP 方法都要求声明并执行清理。
    safe_methods = {"GET", "HEAD", "OPTIONS"}
    return any(
        step.action == "http.request" and str(step.config.get("method", "GET")).upper() not in safe_methods
        for step in scenario.steps
    )


@dataclass(frozen=True)
class ScenarioCatalog:
    """同一 schema 版本下的场景集合。"""

    schema_version: str
    scenarios: Mapping[str, ExternalScenario]

    def to_dict(self) -> dict[str, Any]:
        """把场景目录转换为版本化可序列化映射。

        [参数] 无。
        [返回] schema 版本和按场景 ID 索引的场景映射。
        最近修改时间：2026-07-25 21:00:00，补齐目录序列化契约。
        """

        # 1. 版本与场景集合必须同时输出，避免资产脱离 schema 命名空间。
        return {
            "schema_version": self.schema_version,
            "scenarios": {key: value.to_dict() for key, value in self.scenarios.items()},
        }
