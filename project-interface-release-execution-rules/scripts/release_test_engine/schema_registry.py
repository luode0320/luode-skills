"""内置 JSON Schema 和可选 jsonschema 加速校验。"""

from __future__ import annotations

from typing import Any, Mapping

try:  # jsonschema 是可选增强依赖，核心在无网络环境也能工作。
    import jsonschema
except ImportError:  # pragma: no cover - 环境相关分支
    jsonschema = None


class SchemaValidationError(ValueError):
    """Schema 校验失败。"""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


IR_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["schema_version", "project_fingerprint", "interfaces"],
    "properties": {
        "schema_version": {"type": "string"},
        "project_fingerprint": {"type": "string", "minLength": 1},
        "interfaces": {"type": "array", "items": {"$ref": "#/$defs/interface"}},
    },
    "$defs": {
        "parameter": {
            "type": "object",
            "required": ["name", "location", "required", "schema", "sensitive"],
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "location": {"type": "string"},
                "required": {"type": "boolean"},
                "schema": {"type": "object"},
                "source": {"type": ["object", "null"]},
                "sensitive": {"type": "boolean"},
            },
            "additionalProperties": False,
        },
        "interface": {
            "type": "object",
            "required": [
                "project_fingerprint", "service_id", "operation_id", "protocol",
                "entrypoint", "parameters", "request_schema", "response_schema",
                "auth", "side_effects", "cleanup", "evidence", "completeness",
                "confidence", "adapter", "adapter_version", "risk", "discovered_at",
            ],
            "properties": {
                "project_fingerprint": {"type": "string", "minLength": 1},
                "service_id": {"type": "string", "minLength": 1},
                "operation_id": {"type": "string", "minLength": 1},
                "protocol": {"type": "string", "minLength": 1},
                "entrypoint": {"type": "object"},
                "parameters": {"type": "array", "items": {"$ref": "#/$defs/parameter"}},
                "request_schema": {"type": "object"},
                "response_schema": {"type": "object"},
                "auth": {"type": "object"},
                "side_effects": {"type": "array", "items": {"type": "string"}},
                "cleanup": {"type": "object"},
                "evidence": {"type": "array", "items": {"type": "object"}},
                "completeness": {"enum": ["complete", "partial", "pending"]},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "adapter": {"type": "string", "minLength": 1},
                "adapter_version": {"type": "string", "minLength": 1},
                "risk": {"enum": ["P0", "P1", "P2"]},
                "discovered_at": {"type": "string", "minLength": 1},
            },
            "additionalProperties": False,
        },
    },
    "additionalProperties": False,
}


def get_schema(name: str, version: str = "2.0") -> Mapping[str, Any]:
    """按契约名称和版本返回只读语义上的 schema 对象。"""

    if name == "ir" and version == "2.0":
        return IR_SCHEMA
    raise KeyError(f"unknown schema: {name}@{version}")


def _resolve_local_ref(schema: Mapping[str, Any], root: Mapping[str, Any]) -> Mapping[str, Any]:
    reference = schema.get("$ref")
    if not reference or not str(reference).startswith("#/"):
        return schema
    current: Any = root
    for part in str(reference)[2:].split("/"):
        current = current[part]
    return current


def _fallback(
    document: Any,
    schema: Mapping[str, Any],
    path: str = "$",
    errors: list[str] | None = None,
    root: Mapping[str, Any] | None = None,
) -> list[str]:
    errors = [] if errors is None else errors
    root = schema if root is None else root
    schema = _resolve_local_ref(schema, root)
    expected = schema.get("type")
    if isinstance(expected, list):
        expected_types = expected
    else:
        expected_types = [expected] if expected else []
    type_ok = True
    if expected_types:
        type_ok = any(
            (kind == "object" and isinstance(document, dict))
            or (kind == "array" and isinstance(document, list))
            or (kind == "string" and isinstance(document, str))
            or (kind == "boolean" and isinstance(document, bool))
            or (kind == "number" and isinstance(document, (int, float)) and not isinstance(document, bool))
            or (kind == "null" and document is None)
            for kind in expected_types
        )
        if not type_ok:
            errors.append(f"{path} expected {expected_types}")
            return errors
    if isinstance(document, dict):
        for key in schema.get("required", []):
            if key not in document:
                errors.append(f"{path}.{key} is required")
        for key, value in document.items():
            child = schema.get("properties", {}).get(key)
            if child is None:
                if schema.get("additionalProperties") is False:
                    errors.append(f"{path}.{key} is not allowed")
                continue
            _fallback(value, child, f"{path}.{key}", errors, root)
    elif isinstance(document, list):
        for index, value in enumerate(document):
            if "items" in schema:
                _fallback(value, schema["items"], f"{path}[{index}]", errors, root)
    if isinstance(document, str) and "minLength" in schema and len(document) < schema["minLength"]:
        errors.append(f"{path} must not be empty")
    if isinstance(document, (int, float)) and not isinstance(document, bool):
        if "minimum" in schema and document < schema["minimum"]:
            errors.append(f"{path} is below minimum")
        if "maximum" in schema and document > schema["maximum"]:
            errors.append(f"{path} is above maximum")
    if "enum" in schema and document not in schema["enum"]:
        errors.append(f"{path} must be one of {schema['enum']}")
    return errors


def validate_document(document: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    if jsonschema is not None:
        validator = jsonschema.Draft202012Validator(schema)
        errors = [f"{'.'.join(str(item) for item in error.path) or '$'}: {error.message}" for error in validator.iter_errors(document)]
    else:
        errors = _fallback(document, schema, root=schema)
    if errors:
        raise SchemaValidationError(errors)
