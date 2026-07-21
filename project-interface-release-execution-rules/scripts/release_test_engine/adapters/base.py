"""发现适配器的最小契约与共享构造函数。

适配器只负责把源码/声明转换为统一 ``InterfaceIR``。执行能力由 runner
单独声明；当某协议只有发现能力时，运行阶段必须返回结构化 ``PENDING``。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Protocol

from ..model import InterfaceIR, ParameterIR


@dataclass(frozen=True)
class DiscoveryContext:
    """适配器共享的项目扫描上下文。"""

    root: Path
    project_fingerprint: str
    path: Path
    content: str


class DiscoveryAdapter(Protocol):
    """发现适配器必须实现的协议。"""

    protocol: str
    name: str
    version: str

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: 当前文件和项目上下文；[返回] 发现到的入口；最近修改时间: 2026-07-12 19:20:00 定义适配器契约。"""


def line_number(content: str, offset: int) -> int:
    """[参数] content: 源码文本；offset: 匹配偏移；[返回] 1 起始行号；最近修改时间: 2026-07-12 19:20:00 统一证据位置。"""

    return content.count("\n", 0, offset) + 1


def evidence(context: DiscoveryContext, value: str, *, line: int | None = None, kind: str = "source") -> tuple[dict[str, Any], ...]:
    """[参数] context: 扫描上下文；value: 证据描述；line: 可选行号；kind: 证据类别；[返回] 脱敏证据列表；最近修改时间: 2026-07-12 19:20:00 统一证据结构。"""

    item: dict[str, Any] = {"source": str(context.path.relative_to(context.root)), "kind": kind, "evidence": value}
    if line is not None:
        item["line"] = line
    return (item,)


def make_interface(
    context: DiscoveryContext,
    protocol: str,
    operation_id: str,
    entrypoint: dict[str, Any],
    *,
    parameters: Iterable[ParameterIR] = (),
    request_schema: dict[str, Any] | None = None,
    response_schema: dict[str, Any] | None = None,
    auth: dict[str, Any] | None = None,
    side_effects: Iterable[str] = (),
    cleanup: dict[str, Any] | None = None,
    evidence_items: tuple[dict[str, Any], ...] | None = None,
    completeness: str = "partial",
    confidence: float = 0.7,
    adapter: str | None = None,
    adapter_version: str = "2.0",
    risk: str = "P2",
) -> InterfaceIR:
    """[参数] context/protocol/operation_id/entrypoint: 入口基础事实；其余参数: 契约补充字段；[返回] 统一入口 IR；最近修改时间: 2026-07-12 19:20:00 减少适配器重复构造。"""

    return InterfaceIR(
        project_fingerprint=context.project_fingerprint,
        service_id=context.path.parent.name or "default",
        operation_id=operation_id,
        protocol=protocol,
        entrypoint=entrypoint,
        parameters=tuple(parameters),
        request_schema=request_schema or {},
        response_schema=response_schema or {},
        auth=auth or {},
        side_effects=tuple(side_effects),
        cleanup=cleanup or {},
        evidence=evidence_items or evidence(context, operation_id),
        completeness=completeness,
        confidence=confidence,
        adapter=adapter or f"builtin.{protocol}",
        adapter_version=adapter_version,
        risk=risk,
    )


AdapterFactory = Callable[[], DiscoveryAdapter]
