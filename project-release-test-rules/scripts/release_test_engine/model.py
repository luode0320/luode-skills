"""版本化统一入口模型。

模型保持协议中立；具体 adapter 只负责把项目事实转换为此结构，后续执行器不再
依赖框架名称或源码文件格式。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from .schema_registry import IR_SCHEMA, SchemaValidationError, validate_document

IR_SCHEMA_VERSION = "2.0"
ALLOWED_PROTOCOLS = {
    "http",
    "graphql",
    "grpc",
    "websocket",
    "soap",
    "jsonrpc",
    "message",
    "cli",
    "scheduler",
    "event",
}
ALLOWED_LOCATIONS = {
    "path",
    "query",
    "header",
    "cookie",
    "body",
    "form",
    "multipart",
    "message",
    "cli",
    "env",
}


class IRValidationError(ValueError):
    """统一入口模型不符合版本化契约。"""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("invalid IR: " + "; ".join(errors))


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class ParameterIR:
    """单个参数的稳定命名空间和来源描述。"""

    name: str
    location: str
    required: bool = False
    schema: Mapping[str, Any] = field(default_factory=dict)
    source: Mapping[str, Any] | None = None
    sensitive: bool = False

    def to_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "name": self.name,
            "location": self.location,
            "required": self.required,
            "schema": dict(self.schema),
            "sensitive": self.sensitive,
        }
        if self.source is not None:
            value["source"] = dict(self.source)
        return value


@dataclass(frozen=True)
class InterfaceIR:
    """统一的接口/任务入口描述，适配器输出该对象。"""

    project_fingerprint: str
    service_id: str
    operation_id: str
    protocol: str
    entrypoint: Mapping[str, Any]
    parameters: tuple[ParameterIR, ...] = ()
    request_schema: Mapping[str, Any] = field(default_factory=dict)
    response_schema: Mapping[str, Any] = field(default_factory=dict)
    auth: Mapping[str, Any] = field(default_factory=dict)
    side_effects: tuple[str, ...] = ()
    cleanup: Mapping[str, Any] = field(default_factory=dict)
    evidence: tuple[Mapping[str, Any], ...] = ()
    completeness: str = "partial"
    confidence: float = 0.0
    adapter: str = "unknown"
    adapter_version: str = "0"
    risk: str = "P2"
    discovered_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_fingerprint": self.project_fingerprint,
            "service_id": self.service_id,
            "operation_id": self.operation_id,
            "protocol": self.protocol,
            "entrypoint": dict(self.entrypoint),
            "parameters": [item.to_dict() for item in self.parameters],
            "request_schema": dict(self.request_schema),
            "response_schema": dict(self.response_schema),
            "auth": dict(self.auth),
            "side_effects": list(self.side_effects),
            "cleanup": dict(self.cleanup),
            "evidence": [dict(item) for item in self.evidence],
            "completeness": self.completeness,
            "confidence": self.confidence,
            "adapter": self.adapter,
            "adapter_version": self.adapter_version,
            "risk": self.risk,
            "discovered_at": self.discovered_at,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "InterfaceIR":
        validate_ir({"schema_version": IR_SCHEMA_VERSION, "interfaces": [value], "project_fingerprint": value.get("project_fingerprint", "")})
        return cls(
            project_fingerprint=str(value["project_fingerprint"]),
            service_id=str(value["service_id"]),
            operation_id=str(value["operation_id"]),
            protocol=str(value["protocol"]),
            entrypoint=dict(value["entrypoint"]),
            parameters=tuple(ParameterIR(**item) for item in value.get("parameters", [])),
            request_schema=dict(value.get("request_schema", {})),
            response_schema=dict(value.get("response_schema", {})),
            auth=dict(value.get("auth", {})),
            side_effects=tuple(value.get("side_effects", [])),
            cleanup=dict(value.get("cleanup", {})),
            evidence=tuple(dict(item) for item in value.get("evidence", [])),
            completeness=str(value.get("completeness", "partial")),
            confidence=float(value.get("confidence", 0.0)),
            adapter=str(value.get("adapter", "unknown")),
            adapter_version=str(value.get("adapter_version", "0")),
            risk=str(value.get("risk", "P2")),
            discovered_at=str(value.get("discovered_at", _now())),
        )


def validate_ir(document: Mapping[str, Any]) -> None:
    """校验统一 IR；失败时抛出包含所有路径的 ``IRValidationError``。"""

    errors: list[str] = []
    if not isinstance(document, Mapping):
        raise IRValidationError(["$ must be an object"])
    try:
        validate_document(document, IR_SCHEMA)
    except SchemaValidationError as exc:
        errors.extend(exc.errors)
    if document.get("schema_version") != IR_SCHEMA_VERSION:
        errors.append("schema_version must be 2.0")
    for index, item in enumerate(document.get("interfaces", [])):
        prefix = f"interfaces[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{prefix} must be an object")
            continue
        if item.get("protocol") not in ALLOWED_PROTOCOLS:
            errors.append(f"{prefix}.protocol is unsupported")
        confidence = item.get("confidence")
        if isinstance(confidence, (int, float)) and not 0 <= confidence <= 1:
            errors.append(f"{prefix}.confidence must be between 0 and 1")
        for parameter_index, parameter in enumerate(item.get("parameters", [])):
            if parameter.get("location") not in ALLOWED_LOCATIONS:
                errors.append(f"{prefix}.parameters[{parameter_index}].location is unsupported")
    if errors:
        raise IRValidationError(errors)
