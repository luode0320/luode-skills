"""追加式运行事件契约。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


class EventValidationError(ValueError):
    """事件缺少必填字段或字段类型不正确。"""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class BaselineEvent:
    """事件日志的稳定线格式；payload 允许由未来 adapter 扩展。"""

    run_id: str
    event_type: str
    payload: Mapping[str, Any]
    event_id: str = field(default_factory=lambda: uuid4().hex)
    occurred_at: str = field(default_factory=utc_now)
    schema_version: str = "2.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "run_id": self.run_id,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at,
            "payload": dict(self.payload),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "BaselineEvent":
        required = ("run_id", "event_type", "payload", "event_id", "occurred_at")
        missing = [field for field in required if not value.get(field)]
        if missing:
            raise EventValidationError("missing event fields: " + ", ".join(missing))
        if not isinstance(value["payload"], Mapping):
            raise EventValidationError("event payload must be an object")
        return cls(
            schema_version=str(value.get("schema_version", "2.0")),
            event_id=str(value["event_id"]),
            run_id=str(value["run_id"]),
            event_type=str(value["event_type"]),
            occurred_at=str(value["occurred_at"]),
            payload=dict(value["payload"]),
        )
