"""Kafka/RabbitMQ/AMQP 消费者和发布者发现适配器。"""

from __future__ import annotations

import re
from typing import Iterable

from ..model import InterfaceIR, ParameterIR
from .base import DiscoveryContext, evidence, line_number, make_interface


_DECL = re.compile(r"(?:@(?:KafkaListener|RabbitListener)\s*\([^)]*(?:topics|queues?)\s*=\s*[\[\(]?\s*['\"](?P<decorator>[A-Za-z0-9_.:/-]+)|(?:subscribe|consume|publish|send)\s*\(\s*['\"](?P<call>[A-Za-z0-9_.:/-]+))", re.I)
_CONFIG = re.compile(r"\b(?:topic|queue|routing[_-]?key|channel)\s*[:=]\s*['\"]?(?P<name>[A-Za-z0-9_.:/-]+)", re.I)


class MessagingAdapter:
    """发现消息 topic/queue；连接与消费由 local broker adapter 负责。"""

    protocol = "message"
    name = "builtin.messaging"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: 消息声明上下文；[返回] topic/queue IR；最近修改时间: 2026-07-12 19:20:00 记录方向和 broker。"""

        matches = list(_DECL.finditer(context.content))
        if not matches:
            matches = list(_CONFIG.finditer(context.content))
        seen: set[str] = set()
        for match in matches:
            name = match.groupdict().get("decorator") or match.groupdict().get("call") or match.group("name")
            if not name or name in seen:
                continue
            seen.add(name)
            yield make_interface(
                context,
                "message",
                f"message_{self._slug(name)}",
                {"broker_ref": "local_config", "destination": name, "direction": self._direction(match.group(0))},
                parameters=(ParameterIR(name="message", location="message", required=True, schema={"type": "object"}),),
                request_schema={"type": "object"},
                response_schema={"type": "object", "ack": True},
                side_effects=("publish_or_consume_message",),
                cleanup={"required": True, "destination": name},
                evidence_items=evidence(context, f"message destination {name}", line=line_number(context.content, match.start()), kind="message"),
                completeness="complete",
                confidence=0.86,
                risk="P1",
            )

    @staticmethod
    def _direction(value: str) -> str:
        """[参数] value: 声明文本；[返回] publish/consume/unknown；最近修改时间: 2026-07-12 19:20:00 保留消息方向证据。"""

        lowered = value.lower()
        return "consume" if any(item in lowered for item in ("listener", "subscribe", "consume")) else "publish" if any(item in lowered for item in ("publish", "send")) else "unknown"

    @staticmethod
    def _slug(value: str) -> str:
        """[参数] value: destination；[返回] 稳定 ID 片段；最近修改时间: 2026-07-12 19:20:00 生成去重键。"""

        return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_") or "destination"


ADAPTER = MessagingAdapter()
