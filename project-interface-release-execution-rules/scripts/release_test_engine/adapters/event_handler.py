"""事件处理器声明发现适配器。"""

from __future__ import annotations

import re
from typing import Iterable

from ..model import InterfaceIR, ParameterIR
from .base import DiscoveryContext, evidence, line_number, make_interface


_EVENT = re.compile(r"(?:@(?:event_handler|receiver)\s*\([^)]*['\"](?P<decorator>[A-Za-z0-9_.:/-]+)|(?:on_event|event_bus\.subscribe|subscribe)\s*\(\s*['\"](?P<call>[A-Za-z0-9_.:/-]+))", re.I)


class EventHandlerAdapter:
    """发现事件总线 handler 和订阅入口。"""

    protocol = "event"
    name = "builtin.event"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: 事件处理器上下文；[返回] event IR；最近修改时间: 2026-07-12 19:20:00 记录事件名和清理要求。"""

        seen: set[str] = set()
        for match in _EVENT.finditer(context.content):
            name = match.group("decorator") or match.group("call")
            if not name or name in seen:
                continue
            seen.add(name)
            yield make_interface(context, "event", f"event_{name}", {"bus_ref": "local_config", "event": name}, parameters=(ParameterIR(name="payload", location="message", required=True, schema={"type": "object"}),), side_effects=("event_handler",), cleanup={"required": True}, evidence_items=evidence(context, f"event handler {name}", line=line_number(context.content, match.start()), kind="event"), completeness="partial", confidence=0.82, risk="P1")


ADAPTER = EventHandlerAdapter()
