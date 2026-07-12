"""参数来源解析和依赖追踪。"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Mapping


SOURCE_PRIORITY = ("reusable_param", "upstream_api", "local_database", "local_cache", "openapi_example", "fixture", "rule")


def _local_provider_value(source: Mapping[str, Any], *, project_root: str | Path | None) -> tuple[Any, str]:
    """[参数] source/project_root: provider 声明与 local 根目录；[返回] 值和失败原因；最近修改时间: 2026-07-12 支持只读参数查询。"""

    source_type = str(source.get("type", ""))
    if source_type == "local_cache":
        cache = source.get("cache")
        if isinstance(cache, Mapping):
            value = cache.get(str(source.get("key", "")))
            return (value, "") if value is not None else (None, "cache key not found")
        return None, "local cache mapping is missing"
    if source_type != "local_database":
        return None, ""
    query = str(source.get("query", "")).strip()
    if not re.match(r"^(SELECT|WITH)\b", query, re.I):
        return None, "local database provider only permits SELECT/WITH"
    database = source.get("database")
    if not database:
        return None, "local database path is missing"
    database_path = Path(str(database)).resolve()
    root = Path(project_root).resolve() if project_root else None
    if root is not None and root not in database_path.parents and database_path != root:
        return None, "local database path is outside project root"
    connection = None
    try:
        connection = sqlite3.connect(f"file:{database_path.as_posix()}?mode=ro", uri=True)
        row = connection.execute(query, tuple(source.get("query_params", ()) or ())).fetchone()
    except (OSError, sqlite3.Error) as exc:
        return None, f"local database query failed: {type(exc).__name__}"
    finally:
        if connection is not None:
            connection.close()
    if row is None:
        return None, "local database query returned no rows"
    selector = source.get("selector", 0)
    if isinstance(selector, int):
        return (row[selector], "") if selector < len(row) else (None, "selector index out of range")
    return None, "local database selector must be an integer"


def _masked(value: Any, sensitive: bool = False) -> str:
    if sensitive:
        return "***"
    return json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value


def resolve_parameters(interface: Any, reusable: Mapping[str, Any] | None = None, sources: Mapping[str, Any] | None = None, *, project_root: str | Path | None = None) -> dict[str, Any]:
    reusable = reusable or {}
    sources = sources or {}
    samples = reusable.get("params", {}) if isinstance(reusable, Mapping) else {}
    resolved: dict[str, Any] = {}
    trace: list[dict[str, Any]] = []
    for parameter in interface.parameters:
        name = parameter.name
        configs = sources.get(name, []) if isinstance(sources, Mapping) else []
        if isinstance(configs, Mapping):
            configs = configs.get("providers", [])
        candidates = list(configs) if isinstance(configs, list) else []
        for sample in samples.get(name, []) if isinstance(samples, Mapping) else []:
            if isinstance(sample, Mapping) and sample.get("status") == "reusable":
                candidates.insert(0, {"type": "reusable_param", **sample})
        priority = {name: index for index, name in enumerate(SOURCE_PRIORITY)}
        candidates.sort(key=lambda item: priority.get(str(item.get("type", "")), len(priority)) if isinstance(item, Mapping) else len(priority))
        chosen = None
        for source in candidates:
            if not isinstance(source, Mapping):
                continue
            source_type = str(source.get("type", ""))
            if source_type not in SOURCE_PRIORITY:
                continue
            value = source.get("value", source.get("example"))
            provider_reason = ""
            if source_type in {"local_database", "local_cache"} and value is None:
                value, provider_reason = _local_provider_value(source, project_root=project_root)
            if source_type == "reusable_param" and "value_ref" not in source and value is None:
                continue
            if source_type == "local_database" and not source.get("query"):
                continue
            if source_type in {"upstream_api", "local_database", "local_cache"} and value is None:
                trace.append({"target": interface.operation_id, "parameter": name, "source_type": source_type, "resolved": False, "reason": provider_reason or "runtime provider required"})
                continue
            if value is None:
                continue
            chosen = (source_type, value, source)
            break
        if chosen:
            source_type, value, source = chosen
            resolved[name] = value
            trace.append({"target": interface.operation_id, "parameter": name, "source_type": source_type, "resolved": True, "value_ref": source.get("value_ref", ""), "value_masked": _masked(value, parameter.sensitive)})
        elif parameter.required:
            trace.append({"target": interface.operation_id, "parameter": name, "resolved": False, "failure_type": "PARAM_UNRESOLVED"})
    return {"resolved": resolved, "dependency_trace": trace, "unresolved": [item["parameter"] for item in trace if not item.get("resolved") and item.get("parameter")]}
