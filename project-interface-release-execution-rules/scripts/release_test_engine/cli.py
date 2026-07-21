"""统一 doctor/run 入口，保留可被旧脚本调用的纯函数契约。"""

from __future__ import annotations

import uuid
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .discovery import discover_project
from .graph import build_dependency_graph
from .gate import aggregate_gate
from .judge import judge
from .model import InterfaceIR
from .report import project_execution_to_baseline, write_report
from .resolver import resolve_parameters
from .runner import execute
from .topology import infer_edges
from .dependency_diagnostics import diagnose
from .graph import topological_order
from .adapters import adapter_matrix_status
from .discovery import load_inventory
from .graph import reconcile_contract_assets


def _contract_provenance(path: Path, *, source_type: str, status: str, reason: str = "") -> dict[str, Any]:
    """[参数] path/source_type/status/reason: 来源路径、类型、状态和原因；[返回] provenance 字典；最近修改时间: 2026-07-12 23:10:00 新增资产审计元数据。"""
    evidence: dict[str, Any] = {
        "path": str(path.resolve()),
        "sha256": "",
        "loaded_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_type": source_type,
        "status": status,
    }
    if reason:
        evidence["reason"] = reason
    if status == "loaded":
        try:
            evidence["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            evidence["status"] = "blocked"
            evidence["reason"] = f"asset read failed: {exc}"
    return evidence


def _load_contract_mapping(path: Path, *, source_type: str, root: Path, required_key: str | None = None, required_shape: type = list) -> dict[str, Any]:
    """[参数] path/source_type/root/required_key/required_shape: 资产位置、类型、根和结构约束；[返回] typed mapping 加载结果；最近修改时间: 2026-07-12 23:10:00 新增严格 YAML 结构校验。"""
    try:
        path.relative_to(root)
    except ValueError:
        return {"data": {}, "provenance": _contract_provenance(path, source_type=source_type, status="blocked", reason="asset path is outside local project root"), "status": "BLOCKED", "failure_type": "NON_LOCAL_ASSET"}
    if not path.exists():
        return {"data": {}, "provenance": _contract_provenance(path, source_type=source_type, status="missing", reason=f"{source_type} file does not exist"), "status": "BLOCKED", "failure_type": f"missing_{source_type}"}
    try:
        import yaml
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"data": {}, "provenance": _contract_provenance(path, source_type=source_type, status="blocked", reason=f"invalid YAML: {exc}"), "status": "BLOCKED", "failure_type": "BASELINE_INVALID"}
    if not isinstance(document, Mapping):
        return {"data": {}, "provenance": _contract_provenance(path, source_type=source_type, status="blocked", reason="asset root must be an object"), "status": "BLOCKED", "failure_type": "BASELINE_INVALID"}
    if required_key and not isinstance(document.get(required_key), required_shape):
        return {"data": dict(document), "provenance": _contract_provenance(path, source_type=source_type, status="blocked", reason=f"{required_key} must be a {required_shape.__name__}"), "status": "BLOCKED", "failure_type": "BASELINE_INVALID"}
    return {"data": dict(document), "provenance": _contract_provenance(path, source_type=source_type, status="loaded"), "status": "PASS", "failure_type": ""}


def _contract_identity(item: Mapping[str, Any]) -> str:
    """[参数] item: manifest 或 inventory 记录；[返回] 规范化 method+path 标识；最近修改时间: 2026-07-12 23:10:00 固定三方身份格式。"""
    method = str(item.get("method", item.get("HTTP 方法", ""))).upper().strip()
    path = str(item.get("path", item.get("接口路径", ""))).strip() or "/"
    if not path.startswith("/"):
        path = "/" + path
    return f"{method} {path}"


def _resolve_contract_path(root: Path, value: str | Path | None, default: Path) -> Path:
    """[参数] root/value/default: 项目根、用户路径和默认路径；[返回] 项目根约束下的绝对路径；最近修改时间: 2026-07-12 23:10:00 修复相对路径解析漂移。"""
    if value in (None, ""):
        return default.resolve()
    candidate = Path(value)
    return (root / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()


def load_interface_contract_assets(project_root: str | Path, *, manifest: str | Path | None = None, inventory: str | Path | None = None, reusable_params: str | Path | None = None) -> dict[str, Any]:
    """加载三方契约索引并返回可审计同步元数据；缺失资产永远不是 PASS。

    [参数] project_root/manifest/inventory/reusable_params: local 项目根和三方资产路径。
    [返回] 三方加载结果及聚合同步 metadata。
    最近修改时间: 2026-07-12 23:10:00 接入 strict contract gate 和报告透传。
    """

    root = Path(project_root).resolve()
    manifest_path = _resolve_contract_path(root, manifest, root / "swag" / ".swag-manifest.yaml")
    inventory_path = _resolve_contract_path(root, inventory, root / "doc" / "5-tests" / "基线" / "interface-inventory.yaml")
    reusable_path = _resolve_contract_path(root, reusable_params, root / "doc" / "5-tests" / "基线" / "reusable-params.yaml")
    manifest_result = _load_contract_mapping(manifest_path, source_type="manifest", root=root, required_key="interfaces")
    inventory_result = load_inventory(inventory_path, project_root=root)
    reusable_result = _load_contract_mapping(reusable_path, source_type="reusable_params", root=root, required_key="params", required_shape=Mapping)
    manifest_items = [item for item in manifest_result["data"].get("interfaces", []) if isinstance(item, Mapping)]
    inventory_items = [item for item in inventory_result.get("records", []) if isinstance(item, Mapping)]
    manifest_ids = sorted({_contract_identity(item) for item in manifest_items if item.get("method", item.get("HTTP 方法")) and item.get("path", item.get("接口路径"))})
    inventory_ids = sorted({_contract_identity(item) for item in inventory_items if item.get("method", item.get("HTTP 方法")) and item.get("path", item.get("接口路径"))})
    failures = [item["failure_type"] for item in (manifest_result, inventory_result, reusable_result) if item.get("failure_type")]
    metadata = {
        "code_interfaces": [],
        "manifest_interfaces": manifest_ids,
        "inventory_interfaces": inventory_ids,
        "manifest_provenance": manifest_result["provenance"],
        "inventory_provenance": inventory_result["provenance"],
        "reusable_params_provenance": reusable_result["provenance"],
        "missing_manifest": manifest_result["failure_type"] == "missing_manifest",
        "missing_inventory": inventory_result.get("failure_type") == "missing_inventory",
        "missing_reusable_params": reusable_result["failure_type"] == "missing_reusable_params",
        "status": "PASS" if not failures else "BLOCKED",
        "failure_types": sorted(set(failures)),
    }
    metadata["requires_refresh"] = bool(failures)
    return {"manifest": manifest_result, "inventory": inventory_result, "reusable_params": reusable_result, "metadata": metadata}


def sync_interface_contract_assets(project_root: str | Path, *, manifest: str | Path | None = None, inventory: str | Path | None = None, reusable_params: str | Path | None = None, output: str | Path | None = None) -> dict[str, Any]:
    """执行只读三方契约对账，并把结果写入指定报告文件，不覆盖输入资产。

    [参数] project_root/manifest/inventory/reusable_params/output: local 项目根、三方资产和报告路径。
    [返回] 包含 provenance、集合差异、schema 漂移和 reusable 投影的对账结果。
    最近修改时间: 2026-07-13 00:10:00 新增 C09-02 兼容 CLI 对账入口。
    """

    root = Path(project_root).resolve()
    assets = load_interface_contract_assets(root, manifest=manifest, inventory=inventory, reusable_params=reusable_params)
    discovery = discover_project(root)
    reconciliation = reconcile_contract_assets(
        discovery.interfaces,
        assets["manifest"].get("data", {}),
        assets["inventory"].get("records", []),
        assets["reusable_params"].get("data", {}),
    )
    metadata = dict(assets["metadata"])
    metadata.update({key: reconciliation[key] for key in ("code_interfaces", "manifest_interfaces", "inventory_interfaces", "drift", "schema_changed", "duplicate_interface_ids", "synced_interfaces", "stale_param_keys", "stale_param_count")})
    metadata["contract_status"] = reconciliation["status"] if metadata["status"] == "PASS" else metadata["status"]
    metadata["status"] = metadata["contract_status"]
    metadata["requires_refresh"] = bool(metadata.get("requires_refresh") or reconciliation["requires_dual_refresh"])
    result = {"mode": "sync-interface-contract-assets", "project_root": str(root), "metadata": metadata, "reconciliation": reconciliation, "assets": assets}
    if output:
        output_path = Path(output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            import yaml
            output_path.write_text(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), encoding="utf-8")
        except ImportError:
            output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        result["output"] = str(output_path)
    return result


def _extract_path(value: Any, path: str) -> Any:
    current = value
    for part in str(path or "").lstrip("$").strip(".").split("."):
        if not part:
            continue
        if isinstance(current, Mapping):
            current = current.get(part)
        else:
            return None
    return current


def _load_asset(path: str | Path | None) -> Mapping[str, Any]:
    if not path:
        return {}
    file_path = Path(path)
    if not file_path.exists():
        return {}
    try:
        import yaml
        value = yaml.safe_load(file_path.read_text(encoding="utf-8"))
    except (ImportError, OSError, ValueError):
        try:
            value = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
    return value if isinstance(value, Mapping) else {}


def _options(value: str | Path | Mapping[str, Any]) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {"project_root": value}


def run_doctor(project_root: str | Path | Mapping[str, Any], *, environment: str = "local", strict_fixture: bool = False) -> dict[str, Any]:
    options = _options(project_root)
    root = Path(options.get("project_root", ".")).resolve()
    environment = str(options.get("environment", environment))
    strict_fixture = bool(options.get("strict_fixture", strict_fixture))
    if not root.is_dir():
        return {"mode": "doctor", "status": "FAIL", "reason": "project root does not exist", "project_root": str(root)}
    result = discover_project(root)
    protocols = sorted({item.protocol for item in result.interfaces})
    # 1. 按当前发现入口补齐 fixture 能力；静态协议表不能替代真实入口证据。
    matrix = {
        protocol: adapter_matrix_status(protocol, [item for item in result.interfaces if item.protocol == protocol], strict_fixture=strict_fixture)
        for protocol in protocols
    }
    for capability in matrix.values():
        interface_failures = [
            str(item.get("failure_type", ""))
            for item in capability.get("interfaces", [])
            if isinstance(item, Mapping) and item.get("failure_type")
        ]
        if interface_failures:
            capability["failure_type"] = interface_failures[0]
    execution_pending = any(item.get("execution_status") != "ready" for item in matrix.values())
    status = "PENDING" if not result.interfaces or execution_pending else ("PARTIAL" if result.unsupported else "PASS")
    return {"mode": "doctor", "status": status, "project_root": str(root), "project_fingerprint": result.project_fingerprint, "interface_count": len(result.interfaces), "unsupported_count": len(result.unsupported), "environment": environment, "strict_fixture": bool(strict_fixture), "adapter_matrix": matrix}


def run_pipeline(project_root: str | Path | Mapping[str, Any], *, output_dir: str | Path = "doc/5-tests", environment: str = "local", reusable: Mapping[str, Any] | None = None, sources: Mapping[str, Any] | None = None, baseline_path: str | Path | None = None, baseline_root: str | Path | None = None, config: str | Path | Mapping[str, Any] | None = None, inventory: str | Path | None = None, manifest: str | Path | None = None, reusable_params: str | Path | None = None, plan: str | Path | None = None, modules: list[str] | None = None, adapters: list[str] | None = None, include_p2: bool = False, continue_on_failure: bool = False, dry_run: bool = False, strict_fixture: bool = False, strict_contracts: bool = False, env: Mapping[str, str] | None = None, **_: Any) -> dict[str, Any]:
    """执行本地项目级接口测试并归档报告。

    [参数] project_root: 项目根目录或选项映射；其余参数控制环境、资产、基线和输出。
    [返回] 包含接口、依赖图、门禁和产物路径的执行结果。
    最近修改时间: 2026-07-13 01:05:00 改动原因: 让映射入口严格透传 fixture 生命周期和契约门禁开关。
    """

    options = _options(project_root)
    root = Path(options.get("project_root", ".")).resolve()
    output_dir = options.get("output_dir", output_dir)
    default_output = "output_dir" not in options and str(output_dir) == "doc/5-tests"
    if default_output:
        output_dir = Path(output_dir) / f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_上线前项目接口测试"
    environment = str(options.get("environment", environment))
    baseline_path = options.get("baseline_path", baseline_path)
    baseline_root = options.get("baseline_root", baseline_root)
    config = options.get("config", config)
    inventory = options.get("inventory", inventory)
    manifest = options.get("manifest", manifest)
    reusable_params = options.get("reusable_params", reusable_params)
    plan = options.get("plan", plan)
    modules = options.get("modules", modules) or []
    adapters = options.get("adapters", adapters) or []
    strict_fixture = bool(options.get("strict_fixture", strict_fixture))
    strict_contracts = bool(options.get("strict_contracts", strict_contracts))
    reusable = reusable or _load_asset(options.get("reusable_params"))
    sources = sources or _load_asset(options.get("parameter_sources"))
    config_data = _load_asset(config) if config else {}
    env = dict(env or options.get("env", {}) or config_data.get("env", {}) or {})
    if not baseline_path and baseline_root:
        baseline_path = Path(baseline_root) / "execution-history.yaml"
    dry_run = bool(options.get("dry_run", dry_run))
    discovery = discover_project(root)
    contract_assets = load_interface_contract_assets(root, manifest=manifest, inventory=inventory, reusable_params=reusable_params)
    sync_metadata = dict(contract_assets["metadata"])
    sync_metadata["contract_status"] = sync_metadata.get("status")
    if not strict_contracts and sync_metadata.get("status") == "BLOCKED" and not any((manifest, inventory, reusable_params)):
        sync_metadata["status"] = "not_configured"
    sync_metadata["code_interfaces"] = sorted(
        {
            f"{str(item.entrypoint.get('method', '')).upper()} {str(item.entrypoint.get('path', item.entrypoint.get('url', '/')))}"
            for item in discovery.interfaces
            if isinstance(item.entrypoint, Mapping)
        }
    )
    if not reusable and contract_assets["reusable_params"].get("status") == "PASS":
        reusable = contract_assets["reusable_params"]["data"]
    reconciliation = reconcile_contract_assets(
        discovery.interfaces,
        contract_assets["manifest"].get("data", {}),
        contract_assets["inventory"].get("records", []),
        reusable or contract_assets["reusable_params"].get("data", {}),
    )
    sync_metadata.update(
        {
            "drift": reconciliation["drift"],
            "schema_changed": reconciliation["schema_changed"],
            "duplicate_interface_ids": reconciliation["duplicate_interface_ids"],
            "synced_interfaces": reconciliation["synced_interfaces"],
            "stale_param_keys": reconciliation["stale_param_keys"],
            "stale_param_count": reconciliation["stale_param_count"],
            "requires_refresh": bool(sync_metadata.get("requires_refresh") or reconciliation["requires_dual_refresh"]),
        }
    )
    if sync_metadata.get("contract_status") == "PASS":
        sync_metadata["contract_status"] = reconciliation["status"]
    if strict_contracts or any((manifest, inventory, reusable_params)):
        sync_metadata["status"] = sync_metadata["contract_status"]
    if adapters and "auto" not in adapters:
        allowed = {str(item) for item in adapters}
        discovery = type(discovery)(discovery.project_fingerprint, tuple(item for item in discovery.interfaces if item.protocol in allowed or item.adapter in allowed), discovery.unsupported)
    graph = build_dependency_graph(discovery.interfaces)
    # 显式绑定优先；无绑定时补充唯一字段匹配，并保持确定性排序。
    existing = {(edge.get("provider"), edge.get("consumer"), edge.get("field")) for edge in graph["edges"]}
    for edge in infer_edges(discovery.interfaces):
        marker = (edge.get("provider"), edge.get("consumer"), edge.get("field"))
        if marker not in existing:
            graph["edges"].append(edge)
    graph["order"] = topological_order(graph["nodes"], graph["edges"])
    by_id = {item.operation_id: item for item in discovery.interfaces}
    pipeline_run_id = uuid.uuid4().hex
    raw_results = []
    for operation_id in graph["order"]:
        interface = by_id[operation_id]
        runtime_sources = dict(sources)
        for edge in graph["edges"]:
            if edge.get("consumer") != operation_id:
                continue
            provider_id = str(edge.get("provider", ""))
            provider_result = next((item for item in raw_results if item.get("operation_id") == provider_id), None)
            if provider_result is None:
                continue
            diagnosis = diagnose(provider_result, operation_id)
            if diagnosis.get("status") == "BLOCKED":
                raw_results.append({"operation_id": operation_id, "status": "BLOCKED", "request": {}, "response": {}, "evidence": diagnosis, "failure_type": "BLOCKED_BY_DEPENDENCY"})
                break
            bindings = edge.get("bindings", [])
            field = edge.get("field", "")
            for binding in bindings or [{"target": field, "response_path": f"$.body.data.{field}"}]:
                target = str(binding.get("target", binding.get("field", field)))
                response_path = str(binding.get("response_path", f"$.body.data.{target}"))
                value = _extract_path(provider_result.get("response", {}), response_path)
                if value is not None:
                    runtime_sources[target] = [{"type": "upstream_api", "value": value, "value_ref": f"{provider_id}{response_path}"}]
        else:
            resolved = resolve_parameters(interface, reusable, runtime_sources, project_root=root)
            if dry_run:
                raw_results.append({"operation_id": operation_id, "status": "PENDING", "request": {"params": resolved["resolved"]}, "response": {}, "evidence": {"reason": "dry-run; request not sent", "dependency_trace": resolved["dependency_trace"]}, "failure_type": "DRY_RUN"})
                continue
            if resolved["unresolved"]:
                raw_results.append({"operation_id": operation_id, "status": "PENDING", "request": {"params": resolved["resolved"]}, "response": {}, "evidence": {"reason": "required parameters unresolved", "dependency_trace": resolved["dependency_trace"]}, "failure_type": "PARAM_UNRESOLVED"})
                continue
            raw_results.append(execute(interface, resolved["resolved"], environment=environment, env=env, strict_fixture=strict_fixture, run_id=pipeline_run_id).to_dict())
            continue
    judged = [judge(item, by_id.get(item.get("operation_id"))) for item in raw_results]
    gate = aggregate_gate(judged, discovery.interfaces, unsupported=discovery.unsupported)
    if strict_contracts and sync_metadata.get("status") != "PASS":
        gate = dict(gate)
        gate["gate"] = "BLOCKED"
        gate["allow_release"] = False
        gate["contract_sync_blocked"] = True
        gate["contract_sync_failures"] = list(sync_metadata.get("failure_types", []))
    run_id = pipeline_run_id
    baseline_projection: dict[str, Any] | None = None
    if baseline_path:
        # 1. 先完成事件追加和原子投影，再把真实事件/投影状态写入报告，避免报告声称已更新但基线尚未落盘。
        baseline_projection = project_execution_to_baseline(
            baseline_path,
            run_id,
            gate,
            interfaces=[item.to_dict() for item in discovery.interfaces],
            dependency_graph=graph,
            results=judged,
        )
    artifacts = write_report(
        output_dir,
        judged,
        gate,
        run_id=run_id,
        interfaces=[item.to_dict() for item in discovery.interfaces],
        dependency_graph=graph,
        environment=environment,
        canonical_layout=default_output,
        baseline_summary={
            "updated": baseline_projection is not None,
            "projection_status": "PASS" if baseline_projection is not None else "not_requested",
            "path": str(baseline_path) if baseline_path else "doc/5-tests/基线/",
            "event_count": len(baseline_projection.get("events", [])) if baseline_projection else 0,
            "latest_gate": baseline_projection.get("latest_gate", {}) if baseline_projection else {},
        },
        sync_metadata=sync_metadata,
        runtime_matrix={
            "strict_fixture": strict_fixture,
            "strict_contracts": strict_contracts,
            "interfaces": [item.to_dict() for item in discovery.interfaces],
        },
    )
    baseline_updated = baseline_projection is not None
    return {"mode": "run", "status": gate["gate"], "run_id": run_id, "project_fingerprint": discovery.project_fingerprint, "interfaces": [item.to_dict() for item in discovery.interfaces], "unsupported": list(discovery.unsupported), "dependency_graph": graph, "gate": gate, "artifacts": artifacts, "baseline_path": str(baseline_path) if baseline_path else "", "baseline_updated": baseline_updated, "inventory": str(inventory or ""), "manifest": str(manifest or ""), "reusable_params": str(reusable_params or ""), "contract_assets": contract_assets, "sync_metadata": sync_metadata, "plan": str(plan or ""), "modules": list(modules), "include_p2": bool(include_p2), "continue_on_failure": bool(continue_on_failure), "strict_fixture": bool(strict_fixture), "strict_contracts": bool(strict_contracts)}
