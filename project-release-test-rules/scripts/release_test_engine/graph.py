"""接口字段依赖图和确定性执行顺序。"""

from __future__ import annotations

from collections import defaultdict, deque
from copy import deepcopy
import hashlib
import json
from typing import Any, Iterable, Mapping


class DependencyGraphError(ValueError):
    """依赖图存在循环或引用不存在的入口。"""


def _contract_identity(value: Any) -> str:
    """[参数] value: InterfaceIR 或 manifest/inventory 记录；[返回] 规范化 method+path 标识；最近修改时间: 2026-07-13 00:05:00 固定 C09-02 三方身份算法。"""

    entrypoint = getattr(value, "entrypoint", None)
    item = entrypoint if isinstance(entrypoint, Mapping) else value if isinstance(value, Mapping) else {}
    method = str(item.get("method", item.get("HTTP 方法", ""))).upper().strip()
    path = str(item.get("path", item.get("接口路径", ""))).strip()
    if not method or not path:
        return ""
    if not path.startswith("/"):
        path = "/" + path
    return f"{method} {path}"


def _contract_hash(value: Any) -> str:
    """[参数] value: schema 对象或 JSON 字符串；[返回] 稳定 SHA-256 或空值；最近修改时间: 2026-07-13 00:05:00 固定 schema hash 版本。"""

    if value in (None, "", {}, []):
        return ""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            value = value.strip()
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _schema_hash(value: Any, prefix: str) -> str:
    """[参数] value/prefix: 三方记录和 request/response 前缀；[返回] 规范化 schema hash；最近修改时间: 2026-07-13 00:05:00 支持显式 hash 与 schema 回退。"""

    item = value if isinstance(value, Mapping) else {}
    explicit = item.get(f"{prefix}_schema_hash")
    if explicit:
        return str(explicit)
    if prefix == "request":
        candidates = ("request_schema", "requestSchema", "request_body", "requestBody", "请求参数 schema")
    else:
        candidates = ("response_schema", "responseSchema", "response_body", "responseBody", "响应结构摘要")
    for field in candidates:
        if field in item:
            return _contract_hash(item.get(field))
    return ""


def _duplicate_values(records: Iterable[Any], field_names: tuple[str, ...]) -> list[str]:
    """[参数] records/field_names: 三方记录和候选标识字段；[返回] 重复标识列表；最近修改时间: 2026-07-13 00:05:00 增加重复契约阻断。"""

    seen: dict[str, int] = defaultdict(int)
    for record in records:
        if not isinstance(record, Mapping):
            continue
        identifier = ""
        for field in field_names:
            if record.get(field):
                identifier = str(record[field])
                break
        if identifier:
            seen[identifier] += 1
    return sorted(identifier for identifier, count in seen.items() if count > 1)


def reconcile_contract_assets(code_interfaces: Iterable[Any], manifest: Mapping[str, Any], inventory: Iterable[Mapping[str, Any]], reusable_params: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """对账代码、manifest、inventory 和 reusable params，纯内存返回结果，不修改输入文件。

    [参数] code_interfaces/manifest/inventory/reusable_params: 当前 IR、manifest 对象、inventory 记录和可复用参数对象。
    [返回] 稳定集合、schema 漂移、重复标识、stale 事件和门禁状态。
    最近修改时间: 2026-07-13 00:05:00 新增 C09-02 三方对账。
    """

    code_list = list(code_interfaces)
    manifest_items = [item for item in manifest.get("interfaces", []) if isinstance(item, Mapping)] if isinstance(manifest, Mapping) else []
    inventory_items = [item for item in inventory if isinstance(item, Mapping)]
    code_map: dict[str, Any] = {}
    manifest_map: dict[str, Mapping[str, Any]] = {}
    inventory_map: dict[str, Mapping[str, Any]] = {}
    for item in code_list:
        identity = _contract_identity(item)
        if identity:
            code_map.setdefault(identity, item)
    for item in manifest_items:
        identity = _contract_identity(item)
        if identity:
            manifest_map.setdefault(identity, item)
    for item in inventory_items:
        identity = _contract_identity(item)
        if identity:
            inventory_map.setdefault(identity, item)

    duplicate_ids = sorted(set(_duplicate_values(manifest_items, ("interface_id", "operationId", "接口标识"))) | set(_duplicate_values(inventory_items, ("接口标识", "interface_id", "operation_id"))))
    drift: list[dict[str, Any]] = []
    synced: list[str] = []
    schema_changed: list[dict[str, Any]] = []
    all_identities = sorted(set(code_map) | set(manifest_map) | set(inventory_map))
    for identity in all_identities:
        present = {"code": identity in code_map, "manifest": identity in manifest_map, "inventory": identity in inventory_map}
        missing = [source for source, exists in present.items() if not exists]
        for source in missing:
            drift.append({"identity": identity, "type": f"missing_in_{source}"})
        if missing:
            continue
        hashes = {
            "code_request": _contract_hash(getattr(code_map[identity], "request_schema", {})),
            "code_response": _contract_hash(getattr(code_map[identity], "response_schema", {})),
            "manifest_request": _schema_hash(manifest_map[identity], "request"),
            "manifest_response": _schema_hash(manifest_map[identity], "response"),
            "inventory_request": _schema_hash(inventory_map[identity], "request"),
            "inventory_response": _schema_hash(inventory_map[identity], "response"),
        }
        for direction in ("request", "response"):
            values = {key: value for key, value in hashes.items() if key.endswith(direction) and value}
            if len(set(values.values())) > 1:
                changed = {"identity": identity, "type": "schema_changed", "direction": direction, "hashes": values}
                drift.append(changed)
                schema_changed.append(changed)
        if not any(item.get("identity") == identity and item.get("type") == "schema_changed" for item in schema_changed):
            synced.append(identity)

    reusable_projection = deepcopy(reusable_params or {"params": {}})
    params = reusable_projection.get("params", {}) if isinstance(reusable_projection, Mapping) else {}
    stale_keys: set[str] = set()
    for changed in schema_changed:
        identity = changed["identity"]
        record = inventory_map.get(identity, {})
        refs = record.get("可复用参数影响字段", record.get("reusable_param_refs", [])) if isinstance(record, Mapping) else []
        if isinstance(refs, str):
            refs = [refs]
        stale_keys.update(str(ref) for ref in refs if ref)
    stale_count = 0
    if isinstance(params, Mapping):
        for key in sorted(stale_keys):
            samples = params.get(key, [])
            if not isinstance(samples, list):
                continue
            for sample in samples:
                if isinstance(sample, dict) and sample.get("status") in {"candidate", "reusable"}:
                    sample["status"] = "stale"
                    sample["failure_type"] = "schema_changed"
                    sample["invalidation_reason"] = "schema hash changed during contract reconciliation"
                    stale_count += 1

    if duplicate_ids:
        drift.extend({"type": "duplicate_interface_id", "interface_id": identifier} for identifier in duplicate_ids)
    complete = bool(code_map and manifest_map and inventory_map)
    status = "PASS" if complete and not drift else ("BLOCKED" if drift or not complete else "PENDING")
    return {
        "status": status,
        "synced": not drift and complete,
        "requires_dual_refresh": bool(drift),
        "code_interfaces": sorted(code_map),
        "manifest_interfaces": sorted(manifest_map),
        "inventory_interfaces": sorted(inventory_map),
        "synced_interfaces": synced,
        "drift": drift,
        "schema_changed": schema_changed,
        "duplicate_interface_ids": duplicate_ids,
        "stale_param_keys": sorted(stale_keys),
        "stale_param_count": stale_count,
        "reusable_params_projection": reusable_projection,
    }


def build_dependency_graph(interfaces: Iterable[Any], explicit: Mapping[str, Any] | None = None) -> dict[str, Any]:
    items = list(interfaces)
    ids = {item.operation_id for item in items}
    edges: list[dict[str, Any]] = []
    explicit = explicit or {}
    for item in items:
        config = explicit.get(item.operation_id, {}) if isinstance(explicit, Mapping) else {}
        for dependency in config.get("depends_on", []) if isinstance(config, Mapping) else []:
            if isinstance(dependency, str):
                edges.append({"provider": dependency, "consumer": item.operation_id, "bindings": []})
            elif isinstance(dependency, Mapping):
                edges.append({"provider": str(dependency.get("provider", "")), "consumer": item.operation_id, "bindings": list(dependency.get("bindings", []))})
        for parameter in item.parameters:
            source = parameter.source or {}
            provider = source.get("interface") if isinstance(source, Mapping) else None
            if provider:
                edges.append({"provider": str(provider), "consumer": item.operation_id, "bindings": [{"target": parameter.name, "response_path": source.get("response_path", ""), "selector": source.get("selector", "first")} ]})
    for edge in edges:
        if edge["provider"] not in ids:
            raise DependencyGraphError(f"unknown provider: {edge['provider']}")
    return {"schema_version": "2.0", "nodes": sorted(ids), "edges": edges, "order": topological_order(ids, edges)}


def topological_order(nodes: Iterable[str], edges: Iterable[Mapping[str, Any]]) -> list[str]:
    nodes = set(nodes)
    outgoing: dict[str, set[str]] = defaultdict(set)
    indegree = {node: 0 for node in nodes}
    for edge in edges:
        provider, consumer = str(edge["provider"]), str(edge["consumer"])
        if consumer not in outgoing[provider]:
            outgoing[provider].add(consumer)
            indegree[consumer] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    result: list[str] = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for child in sorted(outgoing[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(result) != len(nodes):
        raise DependencyGraphError("dependency graph contains a cycle")
    return result


def validate_dependency_graph(graph: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    nodes = set(graph.get("nodes", []))
    try:
        order = topological_order(nodes, graph.get("edges", []))
    except (KeyError, TypeError, DependencyGraphError) as exc:
        errors.append(str(exc))
        order = []
    if graph.get("order") != order:
        errors.append("order does not match deterministic topological order")
    for edge in graph.get("edges", []):
        if edge.get("provider") not in nodes or edge.get("consumer") not in nodes:
            errors.append("edge references unknown node")
    return errors
