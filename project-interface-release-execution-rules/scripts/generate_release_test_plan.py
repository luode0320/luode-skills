#!/usr/bin/env python3
"""
上线前接口测试资产初始化与计划生成工具

能力：
1. bootstrap-inventory: 冷启动扫描项目接口，生成初版接口基线
2. reconcile-inventory: 扫描当前接口事实并与已有基线对账
3. generate-plan: 基于更新后的接口基线生成测试计划
4. init-release-test-task: 初始化上线前接口测试任务目录骨架
5. init-baseline-assets: 初始化项目长期基线资产库
6. build-dependency-graph: 根据接口清单和参数来源生成依赖图
7. validate-reusable-params: 校验可复用参数生命周期结构
8. resolve-test-data: 解析可复用 / fixture / rule 参数并生成依赖追踪
9. update-baseline-assets: 按事件持续回写基线资产
10. sync-interface-contract-assets: 对账当前代码、swag manifest 与接口测试基线
11. doctor: 检查 local 环境、依赖与 adapter 支持矩阵
12. run: 调用新内核执行完整上线测试流水线
"""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

import yaml


ROUTE_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    (
        "route",
        re.compile(
            r"""(?ix)
            (?P<method>GET|POST|PUT|PATCH|DELETE)\s*
            [(:=,\s"']+
            (?P<path>/[A-Za-z0-9_\-./:{}]+)
            """
        ),
    ),
    (
        "route",
        re.compile(
            r"""(?ix)
            \.(?P<method>GET|POST|PUT|PATCH|DELETE)\s*
            \(\s*
            ["'](?P<path>/[A-Za-z0-9_\-./:{}]+)["']
            """
        ),
    ),
    (
        "swagger",
        re.compile(
            r"""(?mx)
            ^\s*(?P<path>/[A-Za-z0-9_\-./:{}]+)\s*:\s*$
            """
        ),
    ),
]

METHOD_PATH_LINE_PATTERN = re.compile(
    r"""(?ix)
    (?P<method>GET|POST|PUT|PATCH|DELETE)\s+
    (?P<path>/[A-Za-z0-9_\-./:{}]+)
    """
)

PATH_HINT_PATTERN = re.compile(r"/[A-Za-z0-9_\-./:{}]+")
CHANGED_FILE_MODULE_HINT = re.compile(r"[/\\](api|apis|controller|controllers|handler|handlers|router|routes?)[/\\]")

DEFAULT_RISK_BY_KEYWORD = {
    "支付": "P0",
    "退款": "P0",
    "结算": "P0",
    "交易": "P0",
    "订单": "P0",
    "登录": "P0",
    "鉴权": "P0",
    "权限": "P0",
    "auth": "P0",
    "login": "P0",
    "pay": "P0",
    "order": "P0",
}

ALLOWED_REUSABLE_PARAM_STATUSES = {
    "candidate",
    "reusable",
    "stale",
    "invalid",
    "quarantined",
    "retired",
}

ALLOWED_REUSABLE_PARAM_FAILURE_TYPES = {
    "",
    None,
    "not_found",
    "expired",
    "state_changed",
    "permission_denied",
    "schema_changed",
    "business_rule_changed",
    "environment_blocked",
    "unknown",
}

DEFAULT_SCRIPT_ADAPTER = {
    "base_url_source": "local_config",
    "auth": {
        "provider": "",
        "token_path": "",
        "credential_ref": "",
    },
    "response_wrapper": {
        "code_path": "$.code",
        "success_values": [0, "0", True],
        "message_path": "$.message",
        "data_path": "$.data",
    },
    "masking": {
        "sensitive_keys": [
            "token",
            "password",
            "secret",
            "phone",
            "idCard",
            "bankCard",
            "authorization",
        ],
    },
}


def utc_now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_yaml(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return default if data is None else data


def write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)


def write_text_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def write_yaml_if_missing(path: Path, data) -> bool:
    if path.exists():
        return False
    write_yaml(path, data)
    return True


def load_interface_inventory(inventory_path: Path) -> List[Dict]:
    inventory = read_yaml(inventory_path, [])
    if not isinstance(inventory, list):
        raise ValueError(f"接口基线文件格式非法，应为列表：{inventory_path}")
    return inventory


def normalize_path(path: str) -> str:
    normalized = path.strip()
    if not normalized.startswith("/"):
        normalized = f"/{normalized.lstrip('/')}"
    return normalized


def infer_module(path: str, file_path: Path) -> str:
    parts = [segment for segment in normalize_path(path).split("/") if segment]
    if len(parts) >= 2 and parts[0].lower() in {"api", "openapi", "rest"}:
        return parts[1]
    if parts:
        return parts[0]

    file_parts = [part.lower() for part in file_path.parts]
    for index, part in enumerate(file_parts):
        if part in {"controller", "controllers", "handler", "handlers", "router", "routers", "routes"} and index + 1 < len(file_parts):
            return file_path.parts[index + 1]
    return file_path.parent.name or "unknown"


def infer_risk(interface_name: str, path: str) -> str:
    text = f"{interface_name} {path}".lower()
    for keyword, level in DEFAULT_RISK_BY_KEYWORD.items():
        if keyword.lower() in text:
            return level
    return "P1" if any(word in text for word in ("create", "update", "delete", "submit")) else "P2"


def build_interface_id(module: str, path: str, method: str) -> str:
    cleaned_path = normalize_path(path).strip("/").replace("/", "_").replace("{", "").replace("}", "").replace(":", "")
    cleaned_module = re.sub(r"[^a-zA-Z0-9_]+", "_", module or "unknown")
    return f"{cleaned_module}_{cleaned_path or 'root'}_{method.upper()}".strip("_")


def build_interface_name(path: str, method: str, module: str) -> str:
    tail = normalize_path(path).strip("/").split("/")[-1] or "root"
    return f"{module}模块{tail}接口({method.upper()})"


def inventory_record(method: str, path: str, source: str, evidence: str, file_path: Path) -> Dict:
    normalized_path = normalize_path(path)
    module = infer_module(normalized_path, file_path)
    interface_id = build_interface_id(module, normalized_path, method)
    interface_name = build_interface_name(normalized_path, method, module)
    risk_level = infer_risk(interface_name, normalized_path)

    return {
        "接口标识": interface_id,
        "接口名称": interface_name,
        "HTTP 方法": method.upper(),
        "接口路径": normalized_path,
        "所属模块": module,
        "鉴权要求": "待确认",
        "请求参数 schema": "{}",
        "响应结构摘要": "{}",
        "业务成功判定": "待确认",
        "业务失败判定": "待确认",
        "依赖数据": "待确认",
        "数据副作用": "待确认",
        "清理方式": "待确认",
        "风险等级": risk_level,
        "是否上线必测": "是" if risk_level == "P0" else "否",
        "最近扫描时间": utc_now_str(),
        "最近测试时间": "",
        "最近测试结论": "待确认",
        "接口角色": ["consumer"],
        "可提供字段": {},
        "参数来源": {},
        "依赖接口": [],
        "依赖失败策略": "PARAM_UNRESOLVED",
        "可复用参数影响字段": [],
        "发现来源": source,
        "发现证据": evidence,
        "完整度": "部分",
        "待确认项": [
            "鉴权要求",
            "请求参数 schema",
            "响应结构摘要",
            "业务成功判定",
            "业务失败判定",
            "依赖数据",
            "数据副作用",
            "清理方式",
            "参数来源",
        ],
        "最近扫描提交": "",
    }


def is_candidate_file(file_path: Path) -> bool:
    if any(part.startswith(".") and part != ".github" for part in file_path.parts):
        return False
    if any(part in {"node_modules", "vendor", "dist", "build", "coverage", ".git"} for part in file_path.parts):
        return False
    return file_path.suffix.lower() in {
        ".go",
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".java",
        ".kt",
        ".py",
        ".php",
        ".rb",
        ".yaml",
        ".yml",
        ".json",
        ".md",
    }


def scan_project_interfaces(project_root: Path) -> List[Dict]:
    discovered: Dict[Tuple[str, str], Dict] = {}

    for file_path in project_root.rglob("*"):
        if not file_path.is_file() or not is_candidate_file(file_path):
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for source, pattern in ROUTE_PATTERNS:
            for match in pattern.finditer(content):
                method = match.groupdict().get("method")
                path = match.groupdict().get("path")
                if not path:
                    continue
                if not method:
                    method = "GET" if source == "swagger" else "UNKNOWN"
                key = (method.upper(), normalize_path(path))
                evidence = f"{file_path.relative_to(project_root)}:{content[: match.start()].count(chr(10)) + 1}"
                record = inventory_record(method, path, source, evidence, file_path)
                existing = discovered.get(key)
                if existing:
                    if source not in existing["发现来源"].split(","):
                        existing["发现来源"] = f"{existing['发现来源']},{source}"
                    if evidence not in existing["发现证据"]:
                        existing["发现证据"] = f"{existing['发现证据']}; {evidence}"
                else:
                    discovered[key] = record

        for line_number, line in enumerate(content.splitlines(), 1):
            match = METHOD_PATH_LINE_PATTERN.search(line)
            if not match:
                continue
            key = (match.group("method").upper(), normalize_path(match.group("path")))
            evidence = f"{file_path.relative_to(project_root)}:{line_number}"
            record = inventory_record(match.group("method"), match.group("path"), "doc", evidence, file_path)
            existing = discovered.get(key)
            if existing:
                if "doc" not in existing["发现来源"].split(","):
                    existing["发现来源"] = f"{existing['发现来源']},doc"
                if evidence not in existing["发现证据"]:
                    existing["发现证据"] = f"{existing['发现证据']}; {evidence}"
            else:
                discovered[key] = record

    return sorted(discovered.values(), key=lambda item: (item["所属模块"], item["接口路径"], item["HTTP 方法"]))


def key_by_identity(interface: Dict) -> Tuple[str, str]:
    return interface["HTTP 方法"].upper(), normalize_path(interface["接口路径"])


def key_from_method_path(method: str, path: str) -> Tuple[str, str]:
    return method.upper(), normalize_path(path)


def stable_hash(value: Any) -> str:
    if value in (None, "", {}, []):
        return ""
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    import hashlib

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_swag_manifest(manifest_path: Path) -> Dict[str, Any]:
    manifest = read_yaml(manifest_path, {})
    if not isinstance(manifest, dict):
        raise ValueError(f"swag manifest 格式非法，应为对象：{manifest_path}")
    return manifest


def manifest_interface_records(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    interfaces = manifest.get("interfaces", [])
    if not isinstance(interfaces, list):
        return []
    return [
        item
        for item in interfaces
        if isinstance(item, dict) and item.get("method") and item.get("path") and item.get("generated", True)
    ]


def manifest_identity_map(manifest: Dict[str, Any]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    result: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for item in manifest_interface_records(manifest):
        result[key_from_method_path(str(item["method"]), str(item["path"]))] = item
    return result


def schema_hash_from_manifest(item: Dict[str, Any], prefix: str) -> str:
    explicit = item.get(f"{prefix}_schema_hash")
    if explicit:
        return str(explicit)
    for field in (f"{prefix}_schema", f"{prefix}Schema", f"{prefix}_body", f"{prefix}Body"):
        if field in item:
            return stable_hash(item.get(field))
    return ""


def ensure_openapi_sync_fields(interface: Dict[str, Any]) -> None:
    interface.setdefault("openapi_operation_id", "")
    interface.setdefault("openapi_file", "")
    interface.setdefault("openapi_manifest_updated_at", "")
    interface.setdefault("request_schema_hash", "")
    interface.setdefault("response_schema_hash", "")
    interface.setdefault("schema_sync_status", "blocked")


def manifest_to_inventory_record(
    key: Tuple[str, str],
    manifest_item: Dict[str, Any],
    scanned_item: Dict[str, Any] | None,
    manifest_updated_at: str,
    project_root: Path,
) -> Dict[str, Any]:
    if scanned_item:
        record = dict(scanned_item)
    else:
        method, path = key
        evidence = manifest_item.get("source_router_file") or manifest_item.get("source_controller_file") or "swag/.swag-manifest.yaml"
        record = inventory_record(
            method,
            path,
            "swagger",
            str(evidence),
            project_root / str(evidence).split(":", 1)[0],
        )
    ensure_openapi_sync_fields(record)
    record["openapi_operation_id"] = manifest_item.get("operationId", "")
    record["openapi_file"] = manifest_item.get("file", "")
    record["openapi_manifest_updated_at"] = manifest_updated_at
    record["request_schema_hash"] = schema_hash_from_manifest(manifest_item, "request")
    record["response_schema_hash"] = schema_hash_from_manifest(manifest_item, "response")
    return record


def affected_reusable_param_keys(interface: Dict[str, Any]) -> List[str]:
    values = interface.get("可复用参数影响字段") or []
    if isinstance(values, str):
        return [values]
    if isinstance(values, list):
        return [str(value) for value in values if value]
    return []


def mark_reusable_params_stale(reusable_params_path: Path, affected_keys: Set[str], reason: str) -> int:
    if not reusable_params_path.exists() or not affected_keys:
        return 0
    payload = read_yaml(reusable_params_path, {"params": {}})
    params = payload.get("params", {})
    if not isinstance(params, dict):
        return 0

    changed = 0
    for key in affected_keys:
        samples = params.get(key, [])
        if not isinstance(samples, list):
            continue
        for sample in samples:
            if not isinstance(sample, dict):
                continue
            if sample.get("status") in {"candidate", "reusable"}:
                sample["status"] = "stale"
                sample["failure_type"] = "schema_changed"
                sample["invalidation_reason"] = reason
                sample["last_failed_at"] = utc_now_str()
                changed += 1

    if changed:
        write_yaml(reusable_params_path, payload)
    return changed


def sync_inventory_with_openapi_assets(
    project_root: Path,
    manifest_path: Path,
    inventory_path: Path,
    reusable_params_path: Path | None = None,
) -> Dict[str, Any]:
    scanned_inventory = scan_project_interfaces(project_root)
    scanned_map = {key_by_identity(item): item for item in scanned_inventory}
    inventory_exists = inventory_path.exists()
    existing_inventory = load_interface_inventory(inventory_path) if inventory_exists else []
    inventory_map = {key_by_identity(item): item for item in existing_inventory}
    manifest_exists = manifest_path.exists()
    manifest = load_swag_manifest(manifest_path) if manifest_exists else {}
    manifest_map = manifest_identity_map(manifest) if manifest_exists else {}
    manifest_updated_at = str(manifest.get("updated_at", "")) if manifest_exists else ""

    updated_inventory: List[Dict[str, Any]] = []
    missing_in_swag: List[Dict[str, Any]] = []
    missing_in_inventory: List[Dict[str, Any]] = []
    missing_in_code: List[Dict[str, Any]] = []
    schema_changed: List[Dict[str, Any]] = []
    synced: List[Dict[str, Any]] = []
    affected_param_keys: Set[str] = set()

    all_keys = sorted(set(scanned_map) | set(manifest_map) | set(inventory_map))
    for key in all_keys:
        scanned = scanned_map.get(key)
        manifest_item = manifest_map.get(key)
        existing = inventory_map.get(key)
        method, path = key

        if manifest_item is None:
            record = dict(existing or scanned or {})
            if not record:
                continue
            ensure_openapi_sync_fields(record)
            record["schema_sync_status"] = "missing_in_swag" if scanned else "deprecated"
            record["最近扫描时间"] = utc_now_str()
            if scanned is None:
                missing_in_code.append({"method": method, "path": path, "source": "inventory"})
            else:
                missing_in_swag.append({"method": method, "path": path})
            updated_inventory.append(record)
            continue

        record = manifest_to_inventory_record(key, manifest_item, scanned, manifest_updated_at, project_root)
        if existing:
            merged = dict(existing)
            merged.update(
                {
                    "HTTP 方法": method,
                    "接口路径": path,
                    "openapi_operation_id": record.get("openapi_operation_id", ""),
                    "openapi_file": record.get("openapi_file", ""),
                    "openapi_manifest_updated_at": record.get("openapi_manifest_updated_at", ""),
                    "最近扫描时间": utc_now_str(),
                }
            )
            for field in ("发现来源", "发现证据", "最近扫描提交"):
                if scanned and scanned.get(field):
                    merged[field] = scanned[field]
            request_hash = record.get("request_schema_hash", "")
            response_hash = record.get("response_schema_hash", "")
            old_request_hash = existing.get("request_schema_hash", "")
            old_response_hash = existing.get("response_schema_hash", "")
            merged["request_schema_hash"] = request_hash
            merged["response_schema_hash"] = response_hash
            if (old_request_hash and old_request_hash != request_hash) or (old_response_hash and old_response_hash != response_hash):
                merged["schema_sync_status"] = "schema_changed"
                changed_item = {"method": method, "path": path, "interface_id": merged.get("接口标识", "")}
                schema_changed.append(changed_item)
                affected_param_keys.update(affected_reusable_param_keys(merged))
                merged["最近测试结论"] = "待重测"
            elif scanned is None:
                merged["schema_sync_status"] = "deprecated"
                merged["完整度"] = "待确认"
                merged["待确认项"] = sorted(set(merged.get("待确认项", [])) | {"当前代码缺少接口"})
                missing_in_code.append({"method": method, "path": path, "source": "manifest"})
            else:
                merged["schema_sync_status"] = "synced"
                synced.append({"method": method, "path": path, "interface_id": merged.get("接口标识", "")})
            updated_inventory.append(merged)
        else:
            record["schema_sync_status"] = "missing_in_inventory"
            record["完整度"] = "待确认"
            record["待确认项"] = sorted(set(record.get("待确认项", [])) | {"接口基线缺少 OpenAPI 同步记录"})
            missing_in_inventory.append({"method": method, "path": path, "operationId": record.get("openapi_operation_id", "")})
            updated_inventory.append(record)

    updated_inventory.sort(key=lambda item: (item.get("所属模块", ""), item.get("接口路径", ""), item.get("HTTP 方法", "")))
    write_yaml(inventory_path, updated_inventory)

    stale_param_count = 0
    if reusable_params_path is not None:
        stale_param_count = mark_reusable_params_stale(
            reusable_params_path,
            affected_param_keys,
            "OpenAPI schema changed during interface contract sync",
        )

    requires_dual_refresh = (
        not manifest_exists
        or not inventory_exists
        or bool(missing_in_swag)
        or bool(missing_in_inventory)
        or bool(missing_in_code)
    )
    return {
        "summary": {
            "scanned_interface_count": len(scanned_map),
            "manifest_interface_count": len(manifest_map),
            "inventory_interface_count": len(inventory_map),
            "updated_inventory_count": len(updated_inventory),
            "missing_manifest": not manifest_exists,
            "missing_inventory": not inventory_exists,
            "requires_dual_refresh": requires_dual_refresh,
            "schema_changed_count": len(schema_changed),
            "affected_reusable_param_count": stale_param_count,
            "synced_count": len(synced),
            "updated_at": utc_now_str(),
        },
        "missing_in_swag": missing_in_swag,
        "missing_in_inventory": missing_in_inventory,
        "missing_in_code": missing_in_code,
        "schema_changed": schema_changed,
        "affected_reusable_params": sorted(affected_param_keys),
        "synced": synced,
    }


def reconcile_inventory(existing_inventory: List[Dict], scanned_inventory: List[Dict], current_revision: str) -> Dict:
    existing_map = {key_by_identity(item): item for item in existing_inventory}
    scanned_map = {key_by_identity(item): item for item in scanned_inventory}

    additions: List[Dict] = []
    removals: List[Dict] = []
    changes: List[Dict] = []
    pending: List[Dict] = []
    updated_inventory: List[Dict] = []

    all_keys = sorted(set(existing_map) | set(scanned_map))
    tracked_fields = [
        "接口标识",
        "接口名称",
        "所属模块",
        "鉴权要求",
        "请求参数 schema",
        "响应结构摘要",
        "业务成功判定",
        "业务失败判定",
        "依赖数据",
        "数据副作用",
        "清理方式",
        "风险等级",
        "是否上线必测",
    ]

    for key in all_keys:
        existing = existing_map.get(key)
        scanned = scanned_map.get(key)

        if existing is None and scanned is not None:
            scanned["最近扫描提交"] = current_revision
            additions.append(
                {
                    "接口标识": scanned["接口标识"],
                    "HTTP 方法": scanned["HTTP 方法"],
                    "接口路径": scanned["接口路径"],
                    "差异类型": "新增",
                    "来源证据": scanned["发现证据"],
                }
            )
            if scanned.get("待确认项"):
                pending.append(
                    {
                        "接口标识": scanned["接口标识"],
                        "HTTP 方法": scanned["HTTP 方法"],
                        "接口路径": scanned["接口路径"],
                        "差异类型": "待确认",
                        "待确认项": scanned["待确认项"],
                    }
                )
            updated_inventory.append(scanned)
            continue

        if existing is not None and scanned is None:
            retired = dict(existing)
            retired["完整度"] = "待确认"
            retired["待确认项"] = sorted(set(retired.get("待确认项", [])) | {"废弃标记"})
            retired["最近扫描时间"] = utc_now_str()
            retired["最近扫描提交"] = current_revision
            removals.append(
                {
                    "接口标识": retired["接口标识"],
                    "HTTP 方法": retired["HTTP 方法"],
                    "接口路径": retired["接口路径"],
                    "差异类型": "删除",
                }
            )
            updated_inventory.append(retired)
            continue

        assert existing is not None and scanned is not None

        merged = dict(existing)
        merged["最近扫描时间"] = utc_now_str()
        merged["最近扫描提交"] = current_revision
        merged["发现来源"] = scanned["发现来源"]
        merged["发现证据"] = scanned["发现证据"]

        changed_fields: List[str] = []
        for field in tracked_fields:
            if existing.get(field) != scanned.get(field) and scanned.get(field) not in {"待确认", "{}", "", None}:
                merged[field] = scanned[field]
                changed_fields.append(field)

        if changed_fields:
            changes.append(
                {
                    "接口标识": merged["接口标识"],
                    "HTTP 方法": merged["HTTP 方法"],
                    "接口路径": merged["接口路径"],
                    "差异类型": "变更",
                    "变更字段": changed_fields,
                }
            )

        pending_items = list(dict.fromkeys(scanned.get("待确认项", []) + existing.get("待确认项", [])))
        if pending_items:
            pending.append(
                {
                    "接口标识": merged["接口标识"],
                    "HTTP 方法": merged["HTTP 方法"],
                    "接口路径": merged["接口路径"],
                    "差异类型": "待确认",
                    "待确认项": pending_items,
                }
            )
        merged["待确认项"] = pending_items
        merged["完整度"] = "完整" if not pending_items else "待确认"
        updated_inventory.append(merged)

    updated_inventory.sort(key=lambda item: (item["所属模块"], item["接口路径"], item["HTTP 方法"]))
    return {
        "summary": {
            "新增接口数": len(additions),
            "删除接口数": len(removals),
            "变更接口数": len(changes),
            "待确认接口数": len(pending),
            "扫描时间": utc_now_str(),
            "最近扫描提交": current_revision,
        },
        "additions": additions,
        "removals": removals,
        "changes": changes,
        "pending": pending,
        "updated_inventory": updated_inventory,
    }


def changed_modules_from_inventory(inventory: List[Dict], changed_modules: List[str]) -> List[str]:
    if changed_modules:
        return changed_modules
    return sorted({item.get("所属模块", "unknown") for item in inventory if item.get("所属模块")})


def filter_test_interfaces(inventory: List[Dict], changed_modules: List[str], include_p2: bool = False) -> Dict:
    p0_list: List[Dict] = []
    p1_list: List[Dict] = []
    p2_list: List[Dict] = []
    skipped_list: List[Dict] = []

    changed_modules = changed_modules_from_inventory(inventory, changed_modules)

    for interface in inventory:
        risk_level = interface.get("风险等级", "P2")
        module = interface.get("所属模块", "")
        must_test = interface.get("是否上线必测", "否") == "是"

        if risk_level == "P0":
            p0_list.append(interface)
            continue

        if risk_level == "P1":
            if module in changed_modules or must_test:
                p1_list.append(interface)
            else:
                skipped_list.append({"接口": interface["接口标识"], "理由": "非改动模块 P1 接口，本次跳过"})
            continue

        if include_p2 and (module in changed_modules or must_test):
            p2_list.append(interface)
        else:
            skipped_list.append({"接口": interface["接口标识"], "理由": "非改动模块 P2 接口，本次跳过"})

    return {
        "summary": {
            "总接口数": len(inventory),
            "必测P0接口数": len(p0_list),
            "必测P1接口数": len(p1_list),
            "必测P2接口数": len(p2_list),
            "跳过接口数": len(skipped_list),
            "本次改动模块": changed_modules,
        },
        "p0_interfaces": p0_list,
        "p1_interfaces": p1_list,
        "p2_interfaces": p2_list,
        "skipped_interfaces": skipped_list,
    }


def ensure_release_task_root(task_root: Path, title: str) -> Dict[str, str]:
    task_root.mkdir(parents=True, exist_ok=True)
    chinese_dir = task_root / title
    ascii_dir = task_root / "ascii-artifacts"
    artifacts_dir = ascii_dir / "artifacts"
    logs_dir = artifacts_dir / "logs"
    raw_request_dir = artifacts_dir / "raw-request"
    raw_response_dir = artifacts_dir / "raw-response"
    masked_response_dir = artifacts_dir / "masked-response"
    dependency_trace_dir = artifacts_dir / "dependency-trace"
    resolved_params_dir = artifacts_dir / "resolved-params"
    scripts_dir = ascii_dir / "scripts"
    plan_path = ascii_dir / "release-test-plan.yaml"
    sync_report_path = ascii_dir / "interface-sync-report.yaml"
    reconcile_path = ascii_dir / "inventory-reconcile.yaml"
    results_path = ascii_dir / "interface-test-results.md"
    execute_log_path = logs_dir / "execute.log"

    for directory in (
        chinese_dir,
        ascii_dir,
        artifacts_dir,
        logs_dir,
        raw_request_dir,
        raw_response_dir,
        masked_response_dir,
        dependency_trace_dir,
        resolved_params_dir,
        scripts_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    readme_path = chinese_dir / "README.md"
    if not readme_path.exists():
        readme_path.write_text(
            "\n".join(
                [
                    "# 上线前项目接口测试",
                    "",
                    "## 说明",
                    f"- 创建时间：{utc_now_str()}",
                    "- 当前目录用于承接项目级上线接口测试门禁。",
                    "- 若本次为冷启动，请在此记录扫描来源、对账结果与待确认项。",
                ]
            ),
            encoding="utf-8",
        )

    if not plan_path.exists():
        plan_path.write_text(
            "\n".join(
                [
                    "summary:",
                    "  总接口数: 0",
                    "  必测P0接口数: 0",
                    "  必测P1接口数: 0",
                    "  必测P2接口数: 0",
                    "  跳过接口数: 0",
                    "  本次改动模块: []",
                    "p0_interfaces: []",
                    "p1_interfaces: []",
                    "p2_interfaces: []",
                    "skipped_interfaces: []",
                ]
            ),
            encoding="utf-8",
        )

    if not reconcile_path.exists():
        reconcile_path.write_text(
            "\n".join(
                [
                    "summary:",
                    "  新增接口数: 0",
                    "  删除接口数: 0",
                    "  变更接口数: 0",
                    "  待确认接口数: 0",
                    "  扫描时间: ''",
                    "  最近扫描提交: ''",
                    "additions: []",
                    "removals: []",
                    "changes: []",
                    "pending: []",
                ]
            ),
            encoding="utf-8",
        )

    if not sync_report_path.exists():
        sync_report_path.write_text(
            "\n".join(
                [
                    "summary:",
                    "  scanned_interface_count: 0",
                    "  manifest_interface_count: 0",
                    "  inventory_interface_count: 0",
                    "  updated_inventory_count: 0",
                    "  missing_manifest: false",
                    "  missing_inventory: false",
                    "  requires_dual_refresh: false",
                    "  schema_changed_count: 0",
                    "  affected_reusable_param_count: 0",
                    "  synced_count: 0",
                    "  updated_at: ''",
                    "missing_in_swag: []",
                    "missing_in_inventory: []",
                    "missing_in_code: []",
                    "schema_changed: []",
                    "affected_reusable_params: []",
                    "synced: []",
                ]
            ),
            encoding="utf-8",
        )

    if not results_path.exists():
        results_path.write_text(
            "\n".join(
                [
                    "# 接口测试明细",
                    "",
                    "## 说明",
                    "- 本文件用于记录接口级测试结果，禁止改为 Markdown 表格。",
                    "- 每个接口使用块状格式记录请求参数、简要响应、判定理由和最终结论。",
                ]
            ),
            encoding="utf-8",
        )

    if not execute_log_path.exists():
        execute_log_path.write_text("", encoding="utf-8")

    return {
        "task_root": str(task_root),
        "readme": str(readme_path),
        "ascii_dir": str(ascii_dir),
        "logs_dir": str(logs_dir),
        "dependency_trace_dir": str(dependency_trace_dir),
        "resolved_params_dir": str(resolved_params_dir),
        "plan": str(plan_path),
        "sync_report": str(sync_report_path),
        "reconcile": str(reconcile_path),
        "results": str(results_path),
    }


def ensure_baseline_assets(baseline_root: Path) -> Dict[str, Any]:
    created: List[str] = []
    existing: List[str] = []

    defaults = {
        "interface-inventory.yaml": [],
        "dependency-graph.yaml": {"interfaces": {}, "scenarios": []},
        "parameter-sources.yaml": {"parameters": {}},
        "reusable-params.yaml": {"params": {}},
        "scenario-catalog.yaml": {"scenarios": {}},
        "script-adapter.yaml": DEFAULT_SCRIPT_ADAPTER,
        "execution-history.yaml": {"history": []},
    }

    for filename, payload in defaults.items():
        path = baseline_root / filename
        if write_yaml_if_missing(path, payload):
            created.append(filename)
        else:
            existing.append(filename)

    readme = "\n".join(
        [
            "# 上线测试基线资产库",
            "",
            "本目录用于长期维护项目级上线接口测试资产。",
            "",
            "## 文件说明",
            "- `interface-inventory.yaml`：接口清单与契约。",
            "- `dependency-graph.yaml`：provider / consumer 依赖图。",
            "- `parameter-sources.yaml`：请求参数来源规则。",
            "- `reusable-params.yaml`：已验证可复用参数及生命周期。",
            "- `scenario-catalog.yaml`：可复用接口场景。",
            "- `script-adapter.yaml`：项目对通用脚本的适配。",
            "- `execution-history.yaml`：历次上线测试摘要。",
            "- `baseline-change-log.md`：人可读变更记录。",
            "",
            "## 安全约束",
            "- 禁止保存明文 token、密码、手机号、身份证号、银行卡号、密钥。",
            "- 禁止保存 test / prod / staging 等非 local 环境连接信息。",
        ]
    )
    if write_text_if_missing(baseline_root / "README.md", readme):
        created.append("README.md")
    else:
        existing.append("README.md")

    change_log = "\n".join(
        [
            "# 基线变更记录",
            "",
            f"- {utc_now_str()} 初始化基线资产目录。",
        ]
    )
    if write_text_if_missing(baseline_root / "baseline-change-log.md", change_log):
        created.append("baseline-change-log.md")
    else:
        existing.append("baseline-change-log.md")

    return {
        "baseline_root": str(baseline_root),
        "created": created,
        "existing": existing,
    }


def interface_roles(interface: Dict) -> List[str]:
    roles = interface.get("接口角色", [])
    if isinstance(roles, str):
        return [roles]
    if isinstance(roles, list):
        return [str(role) for role in roles]
    return []


def build_dependency_graph(inventory: List[Dict], parameter_sources: Dict) -> Dict[str, Any]:
    graph: Dict[str, Any] = {"interfaces": {}, "scenarios": []}

    for interface in inventory:
        interface_id = interface.get("接口标识")
        if not interface_id:
            continue
        depends_on = interface.get("依赖接口") or []
        if isinstance(depends_on, str):
            depends_on = [depends_on]

        consumes: Dict[str, Any] = {}
        param_sources = interface.get("参数来源") or {}
        if isinstance(param_sources, dict):
            for param_name, source_key in param_sources.items():
                consumes[param_name] = {
                    "from": source_key,
                    "param_key": param_name,
                }

        node: Dict[str, Any] = {
            "role": interface_roles(interface) or ["consumer"],
            "depends_on": depends_on,
            "consumes": consumes,
            "provides": interface.get("可提供字段") or {},
            "blocked_policy": interface.get("依赖失败策略") or "PARAM_UNRESOLVED",
        }
        graph["interfaces"][interface_id] = node

    for param_name, config in (parameter_sources.get("parameters") or {}).items():
        if not isinstance(config, dict):
            continue
        for provider in config.get("providers", []) or []:
            if not isinstance(provider, dict) or provider.get("type") != "upstream_api":
                continue
            provider_interface = provider.get("interface")
            if not provider_interface:
                continue
            graph["interfaces"].setdefault(
                provider_interface,
                {
                    "role": ["provider"],
                    "depends_on": [],
                    "consumes": {},
                    "provides": {},
                    "blocked_policy": "BLOCKED_BY_DEPENDENCY",
                },
            )
            graph["interfaces"][provider_interface]["provides"][param_name] = {
                "response_path": provider.get("response_path", ""),
                "selector": provider.get("selector", ""),
                "extract": provider.get("extract", ""),
            }

    return graph


def validate_dependency_graph(graph: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    interfaces = graph.get("interfaces", {})
    if not isinstance(interfaces, dict):
        return ["dependency graph 的 interfaces 必须是对象"]

    for interface_id, node in interfaces.items():
        if not isinstance(node, dict):
            errors.append(f"{interface_id}: 节点必须是对象")
            continue
        for dependency in node.get("depends_on", []) or []:
            if dependency not in interfaces:
                errors.append(f"{interface_id}: 依赖接口不存在 {dependency}")
        if node.get("blocked_policy") not in {"BLOCKED_BY_DEPENDENCY", "PARAM_UNRESOLVED", "PENDING", "FAIL"}:
            errors.append(f"{interface_id}: 依赖失败策略非法 {node.get('blocked_policy')}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(interface_id: str, path: List[str]) -> None:
        if interface_id in visited:
            return
        if interface_id in visiting:
            errors.append(f"存在循环依赖: {' -> '.join(path + [interface_id])}")
            return
        visiting.add(interface_id)
        node = interfaces.get(interface_id, {})
        for dependency in node.get("depends_on", []) or []:
            visit(dependency, path + [interface_id])
        visiting.remove(interface_id)
        visited.add(interface_id)

    for interface_id in interfaces:
        visit(interface_id, [])
    return errors


def validate_reusable_params_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    params = payload.get("params", {})
    if not isinstance(params, dict):
        return {"valid": False, "errors": ["reusable-params.yaml 的 params 必须是对象"], "warnings": []}

    checked = 0
    for param_name, samples in params.items():
        if not isinstance(samples, list):
            errors.append(f"{param_name}: 参数样本必须是列表")
            continue
        for index, sample in enumerate(samples):
            checked += 1
            prefix = f"{param_name}[{index}]"
            if not isinstance(sample, dict):
                errors.append(f"{prefix}: 样本必须是对象")
                continue
            status = sample.get("status")
            if status not in ALLOWED_REUSABLE_PARAM_STATUSES:
                errors.append(f"{prefix}: status 非法 {status}")
            failure_type = sample.get("failure_type", "")
            if failure_type not in ALLOWED_REUSABLE_PARAM_FAILURE_TYPES:
                errors.append(f"{prefix}: failure_type 非法 {failure_type}")
            if status in {"reusable", "stale"} and not sample.get("last_verified_at"):
                warnings.append(f"{prefix}: {status} 缺少 last_verified_at")
            if status in {"invalid", "quarantined"} and not sample.get("invalidation_reason"):
                warnings.append(f"{prefix}: {status} 缺少 invalidation_reason")
            if sample.get("value") and not sample.get("value_ref"):
                warnings.append(f"{prefix}: 建议不要保存明文 value，改用 value_masked + value_ref")
            for count_field in ("success_count", "fail_count"):
                value = sample.get(count_field, 0)
                if not isinstance(value, int) or value < 0:
                    errors.append(f"{prefix}: {count_field} 必须是非负整数")

    return {"valid": not errors, "checked": checked, "errors": errors, "warnings": warnings}


def append_change_log(baseline_root: Path, message: str) -> None:
    path = baseline_root / "baseline-change-log.md"
    if not path.exists():
        path.write_text("# 基线变更记录\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as file:
        file.write(f"\n- {utc_now_str()} {message}\n")


def current_revision(project_root: Path) -> str:
    git_head = project_root / ".git"
    return "working-tree" if not git_head.exists() else os.environ.get("GIT_REVISION", "working-tree")


def print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _load_engine_entrypoint(name: str):
    """加载新内核入口；兼容层缺少内核时继续支持旧资产命令。"""
    try:
        module = importlib.import_module("release_test_engine.cli")
    except ImportError:
        return None
    entrypoint = getattr(module, name, None)
    return entrypoint if callable(entrypoint) else None


def _invoke_engine(name: str, args: argparse.Namespace, **extra: Any) -> bool:
    """调用新内核并输出机器可读结果，返回是否已完成委派。"""
    entrypoint = _load_engine_entrypoint(name)
    if entrypoint is None:
        return False
    payload = vars(args).copy()
    payload.pop("func", None)
    payload.update(extra)
    parameters = inspect.signature(entrypoint).parameters
    accepts_extra = any(parameter.kind == inspect.Parameter.VAR_KEYWORD for parameter in parameters.values())
    expects_project_root = "project_root" in parameters and parameters["project_root"].kind in {
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
    }
    if "compat_command" in payload and expects_project_root and "compat_command" not in parameters and not accepts_extra:
        return False
    if payload.get("dry_run") and expects_project_root and "dry_run" not in parameters and not accepts_extra:
        return False
    if expects_project_root:
        if accepts_extra:
            # 位置参数入口声明 **kwargs 时，必须保留未显式列出的 CLI 选项，
            # 否则 baseline/config 等兼容参数会在签名过滤阶段静默丢失。
            keyword_payload = {
                key: value
                for key, value in payload.items()
                if key not in {"project_root", "func"}
            }
        else:
            keyword_payload = {
                key: value
                for key, value in payload.items()
                if key in parameters and key != "project_root" and key != "func"
            }
        if "reusable" in parameters and payload.get("reusable_params"):
            keyword_payload["reusable"] = read_yaml(Path(payload["reusable_params"]).resolve(), {})
        if "sources" in parameters and payload.get("parameter_sources"):
            keyword_payload["sources"] = read_yaml(Path(payload["parameter_sources"]).resolve(), {})
        if "baseline_path" in parameters and payload.get("inventory"):
            keyword_payload["baseline_path"] = str(Path(payload["inventory"]).resolve())
        if "output_dir" in parameters and "output_dir" not in keyword_payload:
            keyword_payload["output_dir"] = payload.get("output_dir", "doc/5-tests")
        result = entrypoint(payload.get("project_root", "."), **keyword_payload)
    else:
        result = entrypoint(payload)
    if result is None:
        result = {"status": "PENDING", "reason": f"{name} returned no result"}
    if not isinstance(result, dict):
        result = {"status": "FAIL", "error": f"{name} must return a JSON object"}
    if payload.get("output"):
        output_path = Path(payload["output"]).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print_json(result)
    return True


def _delegate_legacy_command(command: str, args: argparse.Namespace) -> bool:
    """把旧命令映射到新内核；无内核时由原实现负责兼容回退。"""
    # 旧十命令拥有独立输出契约，不能把它们误当成一次完整 run；仅在未来
    # 提供显式 compat handler 时委派，当前稳定回退到原实现。
    return _invoke_engine(
        f"compat_{command.replace('-', '_')}",
        args,
        compat_command=command,
    )


def command_bootstrap_inventory(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("bootstrap-inventory", args):
        return
    project_root = Path(args.project_root).resolve()
    inventory_path = Path(args.inventory).resolve()
    scanned_inventory = scan_project_interfaces(project_root)
    revision = current_revision(project_root)
    for item in scanned_inventory:
        item["最近扫描提交"] = revision
    write_yaml(inventory_path, scanned_inventory)
    print_json(
        {
            "mode": "bootstrap-inventory",
            "inventory_path": str(inventory_path),
            "interface_count": len(scanned_inventory),
            "recent_scan_revision": revision,
        }
    )


def command_reconcile_inventory(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("reconcile-inventory", args):
        return
    project_root = Path(args.project_root).resolve()
    inventory_path = Path(args.inventory).resolve()
    reconcile_output = Path(args.output).resolve()
    existing_inventory = load_interface_inventory(inventory_path) if inventory_path.exists() else []
    scanned_inventory = scan_project_interfaces(project_root)
    revision = current_revision(project_root)
    reconcile_result = reconcile_inventory(existing_inventory, scanned_inventory, revision)
    write_yaml(inventory_path, reconcile_result["updated_inventory"])
    reconcile_payload = {key: value for key, value in reconcile_result.items() if key != "updated_inventory"}
    write_yaml(reconcile_output, reconcile_payload)
    print_json(
        {
            "mode": "reconcile-inventory",
            "inventory_path": str(inventory_path),
            "reconcile_output": str(reconcile_output),
            **reconcile_result["summary"],
        }
    )


def command_generate_plan(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("generate-plan", args):
        return
    inventory_path = Path(args.inventory).resolve()
    output_path = Path(args.output).resolve()
    inventory = load_interface_inventory(inventory_path)
    changed_modules = args.modules or []
    test_plan = filter_test_interfaces(inventory, changed_modules, args.include_p2)
    write_yaml(output_path, test_plan)
    print_json(
        {
            "mode": "generate-plan",
            "output_path": str(output_path),
            **test_plan["summary"],
        }
    )


def command_init_release_test_task(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("init-release-test-task", args):
        return
    task_root = Path(args.task_root).resolve()
    result = ensure_release_task_root(task_root, args.title)
    print_json({"mode": "init-release-test-task", **result})


def command_init_baseline_assets(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("init-baseline-assets", args):
        return
    baseline_root = Path(args.baseline_root).resolve()
    result = ensure_baseline_assets(baseline_root)
    print_json({"mode": "init-baseline-assets", **result})


def command_build_dependency_graph(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("build-dependency-graph", args):
        return
    inventory = load_interface_inventory(Path(args.inventory).resolve())
    parameter_sources = read_yaml(Path(args.parameter_sources).resolve(), {"parameters": {}})
    graph = build_dependency_graph(inventory, parameter_sources)
    errors = validate_dependency_graph(graph)
    if errors and args.validate:
        print_json({"mode": "build-dependency-graph", "valid": False, "errors": errors})
        raise SystemExit(1)
    output_path = Path(args.output).resolve()
    write_yaml(output_path, graph)
    print_json(
        {
            "mode": "build-dependency-graph",
            "output_path": str(output_path),
            "interface_count": len(graph.get("interfaces", {})),
            "valid": not errors,
            "errors": errors,
        }
    )


def command_validate_reusable_params(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("validate-reusable-params", args):
        return
    reusable_path = Path(args.reusable_params).resolve()
    payload = read_yaml(reusable_path, {"params": {}})
    result = validate_reusable_params_payload(payload)
    print_json({"mode": "validate-reusable-params", "reusable_params": str(reusable_path), **result})
    if not result["valid"]:
        raise SystemExit(1)


def sorted_providers(param_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    priority = param_config.get("priority") or []
    providers = [provider for provider in param_config.get("providers", []) or [] if isinstance(provider, dict)]
    if not priority:
        return providers
    priority_index = {name: index for index, name in enumerate(priority)}
    return sorted(providers, key=lambda item: priority_index.get(item.get("type"), len(priority_index)))


def find_reusable_sample(reusable_params: Dict[str, Any], key: str) -> Dict[str, Any] | None:
    for sample in reusable_params.get("params", {}).get(key, []) or []:
        if not isinstance(sample, dict):
            continue
        if sample.get("status") == "reusable":
            return sample
    return None


def resolve_parameters(parameter_sources: Dict[str, Any], reusable_params: Dict[str, Any], interface_id: str) -> Dict[str, Any]:
    resolved: Dict[str, Any] = {}
    traces: List[Dict[str, Any]] = []

    for param_name, param_config in (parameter_sources.get("parameters") or {}).items():
        if not isinstance(param_config, dict):
            continue
        trace_base = {
            "target_interface": interface_id,
            "param": param_name,
            "resolved": False,
            "failure_type": "PARAM_UNRESOLVED",
        }
        for provider in sorted_providers(param_config):
            source_type = provider.get("type", "")
            trace = dict(trace_base)
            trace["source_type"] = source_type

            if source_type == "reusable_param":
                key = provider.get("key") or param_name
                sample = find_reusable_sample(reusable_params, key)
                trace["source_key"] = key
                if sample:
                    resolved[param_name] = {
                        "source_type": "reusable_param",
                        "value_masked": sample.get("value_masked", ""),
                        "value_ref": sample.get("value_ref", ""),
                        "last_verified_at": sample.get("last_verified_at", ""),
                    }
                    trace.update({"resolved": True, "failure_type": "", "value_ref": sample.get("value_ref", "")})
                    traces.append(trace)
                    break
                trace["reason"] = "no reusable sample"
                traces.append(trace)
                continue

            if source_type in {"openapi_example", "fixture", "rule"}:
                value_ref = provider.get("value_ref", "")
                value = provider.get("value", provider.get("example", ""))
                if value_ref or value != "":
                    resolved[param_name] = {
                        "source_type": source_type,
                        "value_masked": provider.get("value_masked", "***" if value != "" else ""),
                        "value_ref": value_ref,
                    }
                    trace.update({"resolved": True, "failure_type": "", "value_ref": value_ref})
                    traces.append(trace)
                    break
                trace["reason"] = f"{source_type} missing value or value_ref"
                traces.append(trace)
                continue

            trace.update(
                {
                    "source_interface": provider.get("interface", ""),
                    "source_table": provider.get("table", ""),
                    "response_path": provider.get("response_path", ""),
                    "selector": provider.get("selector", ""),
                    "extract": provider.get("extract", ""),
                    "reason": "requires runtime execution or local data query",
                }
            )
            traces.append(trace)

    return {"interface_id": interface_id, "resolved_params": resolved, "dependency_trace": traces}


def command_resolve_test_data(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("resolve-test-data", args):
        return
    parameter_sources = read_yaml(Path(args.parameter_sources).resolve(), {"parameters": {}})
    reusable_params = read_yaml(Path(args.reusable_params).resolve(), {"params": {}})
    output_dir = Path(args.output_dir).resolve()
    resolved_dir = output_dir / "resolved-params"
    trace_dir = output_dir / "dependency-trace"
    resolved_dir.mkdir(parents=True, exist_ok=True)
    trace_dir.mkdir(parents=True, exist_ok=True)

    result = resolve_parameters(parameter_sources, reusable_params, args.interface_id)
    resolved_path = resolved_dir / f"{args.interface_id}.json"
    trace_path = trace_dir / f"{args.interface_id}.json"
    resolved_path.write_text(json.dumps(result["resolved_params"], ensure_ascii=False, indent=2), encoding="utf-8")
    trace_path.write_text(json.dumps(result["dependency_trace"], ensure_ascii=False, indent=2), encoding="utf-8")
    print_json(
        {
            "mode": "resolve-test-data",
            "interface_id": args.interface_id,
            "resolved_count": len(result["resolved_params"]),
            "trace_count": len(result["dependency_trace"]),
            "resolved_path": str(resolved_path),
            "trace_path": str(trace_path),
        }
    )


def apply_reusable_param_events(reusable_params: Dict[str, Any], events: List[Dict[str, Any]]) -> int:
    params = reusable_params.setdefault("params", {})
    applied = 0
    for event in events:
        if not isinstance(event, dict):
            continue
        param_name = event.get("param")
        if not param_name:
            continue
        sample = event.get("sample") or {}
        if not isinstance(sample, dict):
            continue
        status = sample.get("status", event.get("status", "candidate"))
        if status not in ALLOWED_REUSABLE_PARAM_STATUSES:
            status = "quarantined"
            sample["invalidation_reason"] = "invalid status from event"
        sample["status"] = status
        sample.setdefault("first_verified_at", utc_now_str())
        sample.setdefault("last_verified_at", "" if status != "reusable" else utc_now_str())
        sample.setdefault("success_count", 0)
        sample.setdefault("fail_count", 0)
        sample.setdefault("failure_type", "")
        sample.setdefault("invalidation_reason", "")

        existing_samples = params.setdefault(param_name, [])
        value_ref = sample.get("value_ref")
        replaced = False
        if value_ref:
            for index, existing in enumerate(existing_samples):
                if isinstance(existing, dict) and existing.get("value_ref") == value_ref:
                    existing_samples[index] = {**existing, **sample}
                    replaced = True
                    break
        if not replaced:
            existing_samples.append(sample)
        applied += 1
    return applied


def command_update_baseline_assets(args: argparse.Namespace) -> None:
    if _delegate_legacy_command("update-baseline-assets", args):
        return
    baseline_root = Path(args.baseline_root).resolve()
    event_path = Path(args.event_file).resolve()
    output_path = Path(args.output).resolve()
    events_payload = read_yaml(event_path, {})
    ensure_baseline_assets(baseline_root)

    reusable_path = baseline_root / "reusable-params.yaml"
    reusable_params = read_yaml(reusable_path, {"params": {}})
    reusable_events = events_payload.get("reusable_param_events", []) or []
    applied_reusable_events = apply_reusable_param_events(reusable_params, reusable_events)
    write_yaml(reusable_path, reusable_params)

    history_path = baseline_root / "execution-history.yaml"
    history = read_yaml(history_path, {"history": []})
    execution_summary = events_payload.get("execution_summary")
    if execution_summary:
        history.setdefault("history", []).append(execution_summary)
        write_yaml(history_path, history)

    change_message = events_payload.get("change_message") or f"应用基线更新事件 {event_path.name}"
    append_change_log(baseline_root, change_message)

    summary = {
        "mode": "update-baseline-assets",
        "baseline_root": str(baseline_root),
        "event_file": str(event_path),
        "applied_reusable_param_events": applied_reusable_events,
        "history_appended": bool(execution_summary),
        "updated_at": utc_now_str(),
    }
    write_yaml(output_path, summary)
    print_json({**summary, "output": str(output_path)})


def command_sync_interface_contract_assets(args: argparse.Namespace) -> None:
    if _invoke_engine("sync_interface_contract_assets", args, command="sync-interface-contract-assets"):
        return
    if _delegate_legacy_command("sync-interface-contract-assets", args):
        return
    project_root = Path(args.project_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    inventory_path = Path(args.inventory).resolve()
    output_path = Path(args.output).resolve()
    reusable_params_path = Path(args.reusable_params).resolve() if args.reusable_params else None
    result = sync_inventory_with_openapi_assets(
        project_root,
        manifest_path,
        inventory_path,
        reusable_params_path,
    )
    write_yaml(output_path, result)
    print_json(
        {
            "mode": "sync-interface-contract-assets",
            "manifest": str(manifest_path),
            "inventory": str(inventory_path),
            "output": str(output_path),
            **result["summary"],
        }
    )


def command_doctor(args: argparse.Namespace) -> None:
    """检查项目、local 配置和可用 adapter，输出新内核诊断结果。"""
    if args.environment != "local":
        print_json({"mode": "doctor", "status": "BLOCKED", "failure_type": "ENV_BLOCKED", "environment": args.environment})
        return
    if _invoke_engine("run_doctor", args, command="doctor"):
        return
    project_root = Path(args.project_root).resolve()
    checks = {
        "project_root_exists": project_root.is_dir(),
        "local_only": True,
        "engine_available": False,
        "environment": args.environment,
    }
    result = {
        "mode": "doctor",
        "status": "PENDING",
        "project_root": str(project_root),
        "checks": checks,
        "reason": "release_test_engine.cli.run_doctor unavailable",
    }
    if not checks["project_root_exists"]:
        result["status"] = "FAIL"
        result["reason"] = "project_root does not exist"
    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print_json(result)


def command_run(args: argparse.Namespace) -> None:
    """执行新内核全链路；内核缺失时返回结构化不可用结果。"""
    if args.environment != "local":
        print_json({"mode": "run", "status": "BLOCKED", "failure_type": "ENV_BLOCKED", "environment": args.environment})
        return
    if _invoke_engine("run_pipeline", args, command="run"):
        return
    engine_available = _load_engine_entrypoint("run_pipeline") is not None
    failure_type = "UNSUPPORTED_DRY_RUN" if engine_available and args.dry_run else "UNSUPPORTED_ENGINE"
    reason = (
        "current release_test_engine does not expose a dry-run execution mode"
        if failure_type == "UNSUPPORTED_DRY_RUN"
        else "release_test_engine.cli.run_pipeline unavailable"
    )
    print_json(
        {
            "mode": "run",
            "status": "PENDING",
            "failure_type": failure_type,
            "reason": reason,
            "project_root": str(Path(args.project_root).resolve()),
        }
    )


def command_migrate_baseline(args: argparse.Namespace) -> None:
    """[参数] input/output/project_fingerprint: v1 基线迁移输入；[返回] JSON 状态；最近修改时间: 2026-07-12 接入 v2 迁移。"""
    from release_test_engine.migrate_baseline import migrate_v1_to_v2

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    try:
        document = read_yaml(input_path, None)
        if not isinstance(document, dict):
            raise ValueError("v1 baseline must be an object")
        migrated = migrate_v1_to_v2(document, project_fingerprint=args.project_fingerprint, source_revision=args.source_revision)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(migrated, ensure_ascii=False, indent=2), encoding="utf-8")
    except (OSError, TypeError, ValueError) as exc:
        print_json({"mode": "migrate-baseline", "status": "BLOCKED", "failure_type": "INVALID_V1_BASELINE", "reason": str(exc), "input": str(input_path), "output": str(output_path)})
        return
    print_json({"mode": "migrate-baseline", "status": "PASS", "input": str(input_path), "output": str(output_path), "schema_version": migrated.get("schema_version"), "source_revision": args.source_revision})
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="上线前接口测试资产初始化与计划生成工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap-inventory", help="冷启动扫描项目接口并生成初版接口基线")
    bootstrap_parser.add_argument("--project-root", required=True, help="项目根目录")
    bootstrap_parser.add_argument("--inventory", required=True, help="输出接口基线文件路径")
    bootstrap_parser.set_defaults(func=command_bootstrap_inventory)

    reconcile_parser = subparsers.add_parser("reconcile-inventory", help="扫描当前接口事实并与已有基线对账")
    reconcile_parser.add_argument("--project-root", required=True, help="项目根目录")
    reconcile_parser.add_argument("--inventory", required=True, help="接口基线文件路径")
    reconcile_parser.add_argument("--output", default="inventory-reconcile.yaml", help="对账结果输出路径")
    reconcile_parser.set_defaults(func=command_reconcile_inventory)

    generate_parser = subparsers.add_parser("generate-plan", help="基于更新后的接口基线生成测试计划")
    generate_parser.add_argument("--inventory", required=True, help="接口基线文件路径")
    generate_parser.add_argument("--modules", nargs="*", default=[], help="本次上线改动的模块列表，空格分隔")
    generate_parser.add_argument("--include-p2", action="store_true", help="是否包含改动模块的 P2 接口，默认不包含")
    generate_parser.add_argument("--output", default="release-test-plan.yaml", help="输出测试计划文件路径")
    generate_parser.set_defaults(func=command_generate_plan)

    init_parser = subparsers.add_parser("init-release-test-task", help="初始化上线前接口测试任务目录骨架")
    init_parser.add_argument("--task-root", required=True, help="测试任务时间戳根目录路径")
    init_parser.add_argument("--title", default="上线前项目接口测试", help="中文说明目录名")
    init_parser.set_defaults(func=command_init_release_test_task)

    baseline_parser = subparsers.add_parser("init-baseline-assets", help="初始化项目上线测试长期基线资产库")
    baseline_parser.add_argument("--baseline-root", required=True, help="基线目录路径，例如 doc/5-tests/基线")
    baseline_parser.set_defaults(func=command_init_baseline_assets)

    graph_parser = subparsers.add_parser("build-dependency-graph", help="根据接口清单和参数来源生成依赖图")
    graph_parser.add_argument("--inventory", required=True, help="接口基线文件路径")
    graph_parser.add_argument("--parameter-sources", required=True, help="参数来源文件路径")
    graph_parser.add_argument("--output", required=True, help="依赖图输出路径")
    graph_parser.add_argument("--validate", action="store_true", help="存在依赖图错误时返回非零退出码")
    graph_parser.set_defaults(func=command_build_dependency_graph)

    reusable_parser = subparsers.add_parser("validate-reusable-params", help="校验可复用参数生命周期结构")
    reusable_parser.add_argument("--reusable-params", required=True, help="reusable-params.yaml 路径")
    reusable_parser.set_defaults(func=command_validate_reusable_params)

    resolve_parser = subparsers.add_parser("resolve-test-data", help="按参数来源规则解析可复用/OpenAPI示例/fixture/rule 参数并写依赖追踪")
    resolve_parser.add_argument("--parameter-sources", required=True, help="parameter-sources.yaml 路径")
    resolve_parser.add_argument("--reusable-params", required=True, help="reusable-params.yaml 路径")
    resolve_parser.add_argument("--interface-id", required=True, help="目标接口标识")
    resolve_parser.add_argument("--output-dir", required=True, help="输出目录，通常为当轮 ASCII artifacts 目录")
    resolve_parser.set_defaults(func=command_resolve_test_data)

    update_parser = subparsers.add_parser("update-baseline-assets", help="按事件文件持续回写基线资产")
    update_parser.add_argument("--baseline-root", required=True, help="基线目录路径")
    update_parser.add_argument("--event-file", required=True, help="基线更新事件 YAML")
    update_parser.add_argument("--output", default="baseline-update-summary.yaml", help="更新摘要输出路径")
    update_parser.set_defaults(func=command_update_baseline_assets)

    sync_parser = subparsers.add_parser(
        "sync-interface-contract-assets",
        help="对账当前代码、swag manifest 与接口测试基线，输出接口契约同步报告",
    )
    sync_parser.add_argument("--project-root", required=True, help="项目根目录")
    sync_parser.add_argument("--manifest", required=True, help="swag/.swag-manifest.yaml 路径")
    sync_parser.add_argument("--inventory", required=True, help="doc/5-tests/基线/interface-inventory.yaml 路径")
    sync_parser.add_argument("--output", required=True, help="interface-sync-report.yaml 输出路径")
    sync_parser.add_argument("--reusable-params", default="", help="可选：reusable-params.yaml 路径，用于 schema 漂移时标记 stale")
    sync_parser.set_defaults(func=command_sync_interface_contract_assets)

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="检查项目根目录、local 配置、依赖和 adapter 支持矩阵",
    )
    doctor_parser.add_argument("--project-root", required=True, help="被测项目根目录")
    doctor_parser.add_argument("--baseline-root", default="doc/5-tests/基线", help="长期基线目录")
    doctor_parser.add_argument("--config", default="", help="可选的 local 配置或 adapter 配置文件")
    doctor_parser.add_argument("--adapters", nargs="*", default=["auto"], help="限定检查的 adapter，默认 auto")
    doctor_parser.add_argument("--environment", default="local", help="连接环境；仅 local 允许执行")
    doctor_parser.add_argument("--strict-fixture", action="store_true", help="要求非 HTTP fixture 声明 local provenance、run_id、启动句柄和 cleanup")
    doctor_parser.add_argument("--output", default="", help="可选的诊断 JSON 输出路径")
    doctor_parser.set_defaults(func=command_doctor)

    run_parser = subparsers.add_parser(
        "run",
        help="调用新内核执行发现、参数解析、依赖执行、判定和门禁报告",
    )
    run_parser.add_argument("--project-root", required=True, help="被测项目根目录")
    run_parser.add_argument("--baseline-root", default="doc/5-tests/基线", help="长期基线目录")
    run_parser.add_argument("--output-dir", default="doc/5-tests", help="本轮测试证据输出目录")
    run_parser.add_argument("--config", default="", help="local 配置或 adapter 配置文件")
    run_parser.add_argument("--environment", default="local", help="连接环境；仅 local 允许执行")
    run_parser.add_argument("--inventory", default="", help="可选的接口基线文件；缺省时由内核自动发现")
    run_parser.add_argument("--manifest", default="", help="可选的 swag manifest 文件")
    run_parser.add_argument("--parameter-sources", default="", help="可选的参数来源文件")
    run_parser.add_argument("--reusable-params", default="", help="可选的可复用参数文件")
    run_parser.add_argument("--plan", default="", help="可选的既有测试计划文件")
    run_parser.add_argument("--modules", nargs="*", default=[], help="限定本次上线模块")
    run_parser.add_argument("--adapters", nargs="*", default=["auto"], help="限定执行的 adapter，默认 auto")
    run_parser.add_argument("--include-p2", action="store_true", help="包含改动模块的 P2 接口")
    run_parser.add_argument("--continue-on-failure", action="store_true", help="依赖失败后继续执行无关场景")
    run_parser.add_argument("--dry-run", action="store_true", help="仅生成执行图和参数计划，不发送请求")
    run_parser.add_argument("--strict-contracts", action="store_true", help="要求 manifest/inventory/reusable 三方契约资产完整且可审计")
    run_parser.set_defaults(func=command_run)

    migration_parser = subparsers.add_parser("migrate-baseline", help="将 v1 基线迁移为 v2 并保留迁移证据")
    migration_parser.add_argument("--input", required=True, help="v1 基线文件")
    migration_parser.add_argument("--output", required=True, help="v2 输出文件")
    migration_parser.add_argument("--project-fingerprint", required=True, help="项目指纹")
    migration_parser.add_argument("--source-revision", default="", help="源版本或提交标识")
    migration_parser.set_defaults(func=command_migrate_baseline)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
