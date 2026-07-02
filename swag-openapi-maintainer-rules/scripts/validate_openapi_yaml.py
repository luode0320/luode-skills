#!/usr/bin/env python3
"""
Validate swag OpenAPI / Swagger YAML assets.

The script checks YAML parsing, OpenAPI / Swagger version, manifest mappings,
single-interface file count, operation count, and `$ref` sibling usage.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import yaml


REF_ALLOWED_KEYS = {"$ref"}


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
    operation_count = count_operations(openapi_doc if isinstance(openapi_doc, dict) else {})
    if operation_count != expected_count:
        errors.append(f"operation count mismatch: openapi={operation_count}, manifest={expected_count}")

    single_files = [item.get("file") for item in interfaces if item.get("file")]
    if len(single_files) != expected_count:
        errors.append("some manifest interfaces are missing file")

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
