"""按入口命名空间保存参数候选，避免同名字段跨接口串用。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


class ParameterStoreError(ValueError):
    """参数命名空间或候选来源不符合契约。"""


def namespace_key(service_id: str, operation_id: str, location: str, field: str) -> str:
    values = (service_id, operation_id, location, field)
    if any(not str(value).strip() for value in values):
        raise ParameterStoreError("parameter namespace fields must be non-empty")
    return ".".join(str(value).strip() for value in values)


@dataclass(frozen=True)
class ParameterCandidate:
    key: str
    value: Any
    source_type: str
    source_ref: str = ""
    confidence: float = 0.0
    trace: Mapping[str, Any] | None = None
    sensitive: bool = False

    def to_trace(self) -> dict[str, Any]:
        return {
            "parameter_key": self.key,
            "source_type": self.source_type,
            "source_ref": self.source_ref,
            "confidence": self.confidence,
            "trace": dict(self.trace or {}),
            "sensitive": self.sensitive,
            "value_masked": "***" if self.sensitive else self.value,
        }


class ParameterStore:
    """只在完整命名空间内写入和读取候选参数。"""

    def __init__(self) -> None:
        self._values: dict[str, list[ParameterCandidate]] = {}

    def put(self, candidate: ParameterCandidate) -> None:
        if not candidate.key or not candidate.source_type:
            raise ParameterStoreError("candidate key and source_type are required")
        if not 0 <= candidate.confidence <= 1:
            raise ParameterStoreError("candidate confidence must be between 0 and 1")
        self._values.setdefault(candidate.key, []).append(candidate)

    def candidates(self, key: str) -> tuple[ParameterCandidate, ...]:
        return tuple(self._values.get(key, ()))

    def best(self, key: str, *, source_priority: tuple[str, ...] = ()) -> ParameterCandidate | None:
        candidates = list(self.candidates(key))
        if not candidates:
            return None
        priority = {name: index for index, name in enumerate(source_priority)}
        candidates.sort(key=lambda item: (priority.get(item.source_type, len(priority)), -item.confidence))
        return candidates[0]

    def trace(self) -> list[dict[str, Any]]:
        return [candidate.to_trace() for key in sorted(self._values) for candidate in self._values[key]]

    def clear(self) -> None:
        self._values.clear()
