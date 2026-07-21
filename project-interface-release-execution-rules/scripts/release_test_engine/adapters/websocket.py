"""WebSocket 路径、事件和订阅声明发现适配器。"""

from __future__ import annotations

import re
from typing import Iterable

from ..model import InterfaceIR, ParameterIR
from .base import DiscoveryContext, evidence, line_number, make_interface


_PATH = re.compile(
    r"(?:@(?:app\.)?websocket\s*\(\s*['\"](?P<decorator>[^'\"]+)['\"]|"
    r"(?:new\s+WebSocket|WebSocket|socket\.io\.connect)\s*\(\s*['\"](?P<client>[^'\"]+)['\"]|"
    r"(?:websocket|ws)\.(?:route|register|connect)\s*\(\s*['\"](?P<route>[^'\"]+)['\"])",
    re.I,
)
_EVENT = re.compile(r"(?:on|emit|subscribe|send)\s*\(\s*['\"](?P<event>[A-Za-z0-9_.:/-]+)['\"]", re.I)


class WebSocketAdapter:
    """发现 WebSocket 连接入口和消息事件，不猜测传输地址。"""

    protocol = "websocket"
    name = "builtin.websocket"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: WebSocket 源码上下文；[返回] 连接/事件 IR；最近修改时间: 2026-07-12 19:20:00 归一化路径与事件。"""

        seen: set[tuple[str, str]] = set()
        for match in _PATH.finditer(context.content):
            path = match.group("decorator") or match.group("client") or match.group("route")
            if not path:
                continue
            key = ("connect", path)
            if key in seen:
                continue
            seen.add(key)
            yield make_interface(
                context,
                "websocket",
                f"connect_{self._slug(path)}",
                {"target_ref": "local_config", "path": path, "message_mode": "request-response"},
                parameters=(ParameterIR(name="message", location="message", required=False, schema={"type": "object"}),),
                request_schema={"type": "object"},
                evidence_items=evidence(context, f"WebSocket endpoint {path}", line=line_number(context.content, match.start()), kind="websocket"),
                confidence=0.9,
            )
        for match in _EVENT.finditer(context.content):
            event = match.group("event")
            key = ("event", event)
            if key in seen:
                continue
            seen.add(key)
            yield make_interface(
                context,
                "websocket",
                f"event_{self._slug(event)}",
                {"target_ref": "local_config", "event": event, "message_mode": "event"},
                parameters=(ParameterIR(name="message", location="message", required=False, schema={"type": "object"}),),
                request_schema={"type": "object"},
                evidence_items=evidence(context, f"WebSocket event {event}", line=line_number(context.content, match.start()), kind="websocket-event"),
                confidence=0.78,
            )

    @staticmethod
    def _slug(value: str) -> str:
        """[参数] value: 路径或事件名；[返回] 稳定 operation 片段；最近修改时间: 2026-07-12 19:20:00 统一去重键。"""

        return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_") or "socket"


ADAPTER = WebSocketAdapter()
