#!/usr/bin/env python3
"""
Validate swag OpenAPI / Swagger YAML assets.

The script checks YAML parsing, OpenAPI / Swagger version, manifest mappings,
single-interface file count, operation count, single-file tags, single-file
filename policy, Chinese descriptions, and `$ref` sibling usage.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


REF_ALLOWED_KEYS = {"$ref"}
CJK_PATTERN = re.compile(r"[\u3400-\u9fff]")
FILENAME_ILLEGAL_CHARS = re.compile(r'[\\/:*?"<>|]+')
WHITESPACE_PATTERN = re.compile(r"\s+")
MULTI_UNDERSCORE_PATTERN = re.compile(r"_+")
LEADING_SUMMARY_ENUM_PATTERN = re.compile(
    r"^\s*(?:[\(\[（【]?\s*\d+\s*[\)\]）】]?\s*[.、:：_\-]*\s*)+"
)
LEADING_SUMMARY_DECORATION_PATTERN = re.compile(r"^[\s._\-·、,:：;；\(\)（）【】\[\]]+")
SUMMARY_SUFFIX_MAX_LEN = 24


def read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def is_openapi_document(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    openapi = str(data.get("openapi", ""))
    swagger = str(data.get("swagger", ""))
    return openapi.startswith("3.0.") or openapi.startswith("3.1.") or swagger == "2.0"


def count_operations(document: Dict[str, Any]) -> int:
    paths = document.get("paths", {})
    if not isinstance(paths, dict):
        return 0
    methods = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
    count = 0
    for path_item in paths.values():
        if not isinstance(path_item, dict):
            continue
        count += sum(1 for method in path_item if str(method).lower() in methods)
    return count


def has_chinese_description(value: Any) -> bool:
    return isinstance(value, str) and bool(CJK_PATTERN.search(value))


def sanitize_path_segment(path: str) -> str:
    value = path.strip()
    if value.startswith("/"):
        value = value[1:]
    value = value.replace("/", "_")
    value = value.replace("{", "").replace("}", "")
    value = value.replace(":", "")
    return value or "root"


def sanitize_summary_suffix(summary: Any) -> str:
    if not isinstance(summary, str):
        return ""
    value = summary.strip()
    value = LEADING_SUMMARY_ENUM_PATTERN.sub("", value)
    value = LEADING_SUMMARY_DECORATION_PATTERN.sub("", value)
    value = WHITESPACE_PATTERN.sub("_", value)
    value = FILENAME_ILLEGAL_CHARS.sub("_", value)
    value = MULTI_UNDERSCORE_PATTERN.sub("_", value)
    value = value.strip(" _.-·、,:：;；")
    if len(value) > SUMMARY_SUFFIX_MAX_LEN:
        value = value[:SUMMARY_SUFFIX_MAX_LEN].rstrip(" _.-·、,:：;；")
    return value


def build_base_filename(path: str, method: str, path_method_counts: Dict[str, int]) -> str:
    base_name = sanitize_path_segment(path)
    if path_method_counts.get(path, 0) > 1:
        base_name = f"{base_name}_{str(method).lower()}"
    return base_name


def expected_interface_filename(interface: Dict[str, Any], path_method_counts: Dict[str, int]) -> Tuple[str, List[str]]:
    issues: List[str] = []
    path = str(interface.get("path", ""))
    method = str(interface.get("method", ""))
    summary = interface.get("summary", "")
    summary_source = str(interface.get("summary_source", "")).strip() or "missing"

    base_name = build_base_filename(path, method, path_method_counts)
    suffix = sanitize_summary_suffix(summary)

    if summary_source == "unresolved":
        if summary not in ("", None):
            issues.append(f"{method} {path}: unresolved summary_source should use empty summary")
        return f"{base_name}.yaml", issues

    if summary_source == "missing":
        issues.append(f"{method} {path}: manifest missing summary_source")
    if not isinstance(summary, str) or not summary.strip():
        issues.append(f"{method} {path}: manifest missing summary")
    elif not has_chinese_description(summary):
        issues.append(f"{method} {path}: summary must contain Chinese text")
    if not suffix:
        issues.append(f"{method} {path}: summary cannot produce valid filename suffix")
        return f"{base_name}.yaml", issues
    return f"{base_name}_{suffix}.yaml", issues


def resolve_local_ref(document: Dict[str, Any], ref: str) -> Any:
    if not ref.startswith("#/"):
        return None
    current: Any = document
    for segment in ref[2:].split("/"):
        if not isinstance(current, dict):
            return None
        current = current.get(segment)
    return current


def iter_operations(document: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    operations: List[Tuple[str, Dict[str, Any]]] = []
    paths = document.get("paths", {})
    if not isinstance(paths, dict):
        return operations
    methods = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
    for path_name, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if str(method).lower() not in methods or not isinstance(operation, dict):
                continue
            operations.append((f"{str(method).upper()} {path_name}", operation))
    return operations


def validate_parameter_description(document: Dict[str, Any], parameter: Any, location: str, errors: List[str]) -> None:
    if isinstance(parameter, dict) and "$ref" in parameter:
        resolved = resolve_local_ref(document, str(parameter["$ref"]))
        if resolved is None:
            errors.append(f"{location}: unresolved parameter ref {parameter['$ref']}")
            return
        validate_parameter_description(document, resolved, f"{location}->{parameter['$ref']}", errors)
        return
    if not isinstance(parameter, dict):
        return
    if not has_chinese_description(parameter.get("description", "")):
        errors.append(f"{location}: parameter {parameter.get('name', '<unknown>')} missing Chinese description")


def validate_security_schemes(document: Dict[str, Any], errors: List[str]) -> None:
    components = document.get("components", {})
    if isinstance(components, dict):
        schemes = components.get("securitySchemes", {})
        if isinstance(schemes, dict):
            for name, scheme in schemes.items():
                if not isinstance(scheme, dict):
                    continue
                if not has_chinese_description(scheme.get("description", "")):
                    errors.append(f"components.securitySchemes.{name}: missing Chinese description")

    definitions = document.get("securityDefinitions", {})
    if isinstance(definitions, dict):
        for name, scheme in definitions.items():
            if not isinstance(scheme, dict):
                continue
            if not has_chinese_description(scheme.get("description", "")):
                errors.append(f"securityDefinitions.{name}: missing Chinese description")


def validate_schema_node(
    document: Dict[str, Any],
    schema: Any,
    location: str,
    errors: List[str],
    visited_refs: set[str],
    require_self_description: bool = False,
) -> None:
    if isinstance(schema, dict) and "$ref" in schema:
        ref = str(schema["$ref"])
        resolved = resolve_local_ref(document, ref)
        if resolved is None:
            errors.append(f"{location}: unresolved schema ref {ref}")
            return
        if ref in visited_refs:
            return
        visited_refs.add(ref)
        validate_schema_node(document, resolved, f"{location}->{ref}", errors, visited_refs, require_self_description=True)
        return

    if not isinstance(schema, dict):
        return

    if require_self_description:
        description = schema.get("description", "")
        title = schema.get("title", "")
        if not has_chinese_description(description) and not has_chinese_description(title):
            errors.append(f"{location}: schema missing Chinese description")

    properties = schema.get("properties", {})
    if isinstance(properties, dict):
        for prop_name, prop_schema in properties.items():
            if isinstance(prop_schema, dict) and "$ref" in prop_schema:
                validate_schema_node(document, prop_schema, f"{location}.{prop_name}", errors, visited_refs, require_self_description=True)
                continue
            if not isinstance(prop_schema, dict):
                continue
            if not has_chinese_description(prop_schema.get("description", "")):
                errors.append(f"{location}.{prop_name}: property missing Chinese description")
            validate_schema_node(document, prop_schema, f"{location}.{prop_name}", errors, visited_refs)

    items = schema.get("items")
    if items is not None:
        validate_schema_node(document, items, f"{location}[]", errors, visited_refs, require_self_description=False)

    for keyword in ("allOf", "anyOf", "oneOf"):
        variants = schema.get(keyword)
        if isinstance(variants, list):
            for index, variant in enumerate(variants):
                validate_schema_node(document, variant, f"{location}.{keyword}[{index}]", errors, visited_refs, require_self_description=True)


def validate_operation_content(document: Dict[str, Any], operation_label: str, operation: Dict[str, Any], errors: List[str]) -> None:
    for index, parameter in enumerate(operation.get("parameters", []) or []):
        validate_parameter_description(document, parameter, f"{operation_label}.parameters[{index}]", errors)

    request_body = operation.get("requestBody")
    if isinstance(request_body, dict):
        if "$ref" in request_body:
            resolved = resolve_local_ref(document, str(request_body["$ref"]))
            if resolved is None:
                errors.append(f"{operation_label}.requestBody: unresolved ref {request_body['$ref']}")
            else:
                request_body = resolved
        content = request_body.get("content", {})
        if isinstance(content, dict):
            for media_type, media_value in content.items():
                if not isinstance(media_value, dict):
                    continue
                schema = media_value.get("schema")
                if schema is None:
                    continue
                validate_schema_node(
                    document,
                    schema,
                    f"{operation_label}.requestBody[{media_type}]",
                    errors,
                    set(),
                    require_self_description=True,
                )

    responses = operation.get("responses", {})
    if isinstance(responses, dict):
        for status_code, response in responses.items():
            if isinstance(response, dict) and "$ref" in response:
                resolved = resolve_local_ref(document, str(response["$ref"]))
                if resolved is None:
                    errors.append(f"{operation_label}.responses.{status_code}: unresolved ref {response['$ref']}")
                    continue
                response = resolved
            if not isinstance(response, dict):
                continue
            content = response.get("content", {})
            if isinstance(content, dict):
                for media_type, media_value in content.items():
                    if not isinstance(media_value, dict):
                        continue
                    schema = media_value.get("schema")
                    if schema is None:
                        continue
                    validate_schema_node(
                        document,
                        schema,
                        f"{operation_label}.responses.{status_code}[{media_type}]",
                        errors,
                        set(),
                        require_self_description=True,
                    )


def validate_descriptions(document: Dict[str, Any], errors: List[str], single_file: bool) -> None:
    validate_security_schemes(document, errors)
    for operation_label, operation in iter_operations(document):
        if single_file and operation.get("tags"):
            errors.append(f"{operation_label}: single-interface YAML must not define tags; import should not create parent folder")
        validate_operation_content(document, operation_label, operation, errors)


def find_ref_siblings(value: Any, location: str, errors: List[str]) -> None:
    if isinstance(value, dict):
        if "$ref" in value:
            siblings = set(value) - REF_ALLOWED_KEYS
            if siblings:
                errors.append(f"{location}: $ref has sibling fields: {sorted(siblings)}")
        for key, child in value.items():
            find_ref_siblings(child, f"{location}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            find_ref_siblings(child, f"{location}[{index}]", errors)


def manifest_interfaces(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    interfaces = manifest.get("interfaces", [])
    if not isinstance(interfaces, list):
        return []
    return [item for item in interfaces if isinstance(item, dict) and item.get("generated", True)]


def build_path_method_counts(interfaces: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in interfaces:
        path = str(item.get("path", ""))
        counts[path] = counts.get(path, 0) + 1
    return counts


def validate_swag_dir(swag_dir: Path) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    openapi_path = swag_dir / "openapi.yaml"
    manifest_path = swag_dir / ".swag-manifest.yaml"
    if not openapi_path.exists():
        errors.append("missing swag/openapi.yaml")
    if not manifest_path.exists():
        errors.append("missing swag/.swag-manifest.yaml")
    if errors:
        return {"valid": False, "errors": errors, "warnings": warnings}

    try:
        openapi_doc = read_yaml(openapi_path)
        manifest = read_yaml(manifest_path)
    except yaml.YAMLError as error:
        return {"valid": False, "errors": [f"YAML parse error: {error}"], "warnings": warnings}

    if not is_openapi_document(openapi_doc):
        errors.append("swag/openapi.yaml has invalid OpenAPI / Swagger version")
    if not isinstance(manifest, dict):
        errors.append(".swag-manifest.yaml must be a YAML object")
        manifest = {}

    interfaces = manifest_interfaces(manifest)
    expected_count = len(interfaces)
    path_method_counts = build_path_method_counts(interfaces)
    operation_count = count_operations(openapi_doc if isinstance(openapi_doc, dict) else {})
    if operation_count != expected_count:
        errors.append(f"operation count mismatch: openapi={operation_count}, manifest={expected_count}")
    validate_descriptions(openapi_doc if isinstance(openapi_doc, dict) else {}, errors, single_file=False)

    single_files = [item.get("file") for item in interfaces if item.get("file")]
    if len(single_files) != expected_count:
        errors.append("some manifest interfaces are missing file")

    expected_filenames: List[str] = []
    for interface in interfaces:
        expected_filename, filename_issues = expected_interface_filename(interface, path_method_counts)
        expected_filenames.append(expected_filename)
        errors.extend(filename_issues)
        actual_filename = str(interface.get("file", ""))
        if actual_filename and actual_filename != expected_filename:
            errors.append(
                f"{interface.get('method', '<unknown>')} {interface.get('path', '<unknown>')}: "
                f"manifest file mismatch, expected {expected_filename}, got {actual_filename}"
            )

    duplicate_filenames = sorted({name for name in expected_filenames if expected_filenames.count(name) > 1})
    if duplicate_filenames:
        errors.append(f"manifest interface files must be unique: {duplicate_filenames}")

    for filename in single_files:
        path = (swag_dir / str(filename)).resolve()
        try:
            path.relative_to(swag_dir.resolve())
        except ValueError:
            errors.append(f"manifest file escapes swag dir: {filename}")
            continue
        if path.name in {"openapi.yaml", ".swag-manifest.yaml"}:
            errors.append(f"manifest interface file cannot be reserved file: {filename}")
            continue
        if not path.exists():
            errors.append(f"missing single-interface YAML: {filename}")
            continue
        try:
            doc = read_yaml(path)
        except yaml.YAMLError as error:
            errors.append(f"{filename}: YAML parse error: {error}")
            continue
        if not is_openapi_document(doc):
            errors.append(f"{filename}: invalid OpenAPI / Swagger version")
        operation_in_file = count_operations(doc if isinstance(doc, dict) else {})
        if operation_in_file < 1:
            errors.append(f"{filename}: no operation found")
        validate_descriptions(doc if isinstance(doc, dict) else {}, errors, single_file=True)
        find_ref_siblings(doc, filename, errors)

    find_ref_siblings(openapi_doc, "openapi.yaml", errors)

    generated_yaml_files = [
        path.name
        for path in swag_dir.glob("*.yaml")
        if path.name not in {"openapi.yaml", ".swag-manifest.yaml"}
    ]
    manifest_file_set = {str(filename) for filename in single_files}
    extra_files = sorted(set(generated_yaml_files) - manifest_file_set)
    if extra_files:
        warnings.append(f"YAML files not listed in manifest: {extra_files}")

    errors = list(dict.fromkeys(errors))
    warnings = list(dict.fromkeys(warnings))

    return {
        "valid": not errors,
        "operation_count": operation_count,
        "manifest_interface_count": expected_count,
        "single_file_count": len(single_files),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate swag OpenAPI / Swagger YAML assets")
    parser.add_argument("--swag-dir", required=True, help="Path to project swag directory")
    args = parser.parse_args()

    result = validate_swag_dir(Path(args.swag_dir).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
