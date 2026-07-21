"""项目入口发现器。

发现器只负责收集证据并转换为统一 IR；无法确认协议或调用方式时输出
``PENDING`` 所需的证据，不把猜测伪装成可执行接口。
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .model import InterfaceIR, ParameterIR
from .adapters import adapter_status, discovery_adapters
from .adapters.base import DiscoveryContext


def _asset_provenance(path: Path, *, source_type: str, status: str, reason: str = "") -> dict[str, Any]:
    """生成契约资产来源证据；读取失败时不伪造内容或哈希。

    [参数] path/source_type/status/reason: 资产路径、来源类别、读取状态和失败原因。
    [返回] 可写入报告的 provenance 字典。
    最近修改时间: 2026-07-12 23:10:00 新增三方契约资产来源审计证据。
    """

    resolved = path.resolve()
    evidence: dict[str, Any] = {
        "path": str(resolved),
        "sha256": "",
        "loaded_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_type": source_type,
        "status": status,
    }
    if reason:
        evidence["reason"] = reason
    if status == "loaded":
        try:
            evidence["sha256"] = hashlib.sha256(resolved.read_bytes()).hexdigest()
        except OSError as exc:
            evidence["status"] = "blocked"
            evidence["reason"] = f"asset read failed: {exc}"
    return evidence


def load_inventory(path: str | Path | None, *, project_root: str | Path | None = None) -> dict[str, Any]:
    """加载接口 inventory，区分缺失、非法 YAML、形状错误和非 local 路径。

    返回值始终是结构化对象，调用方不得把 ``records`` 为空误判为同步通过。

    [参数] path/project_root: inventory 路径和 local 项目根目录。
    [返回] records、provenance、status、failure_type 组成的加载结果。
    最近修改时间: 2026-07-12 23:10:00 新增缺失/非法/非 local 分类。
    """

    if not path:
        return {"records": [], "provenance": {"path": "", "sha256": "", "loaded_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "source_type": "inventory", "status": "missing", "reason": "inventory path not configured"}, "status": "BLOCKED", "failure_type": "missing_inventory"}
    inventory_path = Path(path).resolve()
    root = Path(project_root).resolve() if project_root else inventory_path.parent
    try:
        inventory_path.relative_to(root)
    except ValueError:
        provenance = _asset_provenance(inventory_path, source_type="inventory", status="blocked", reason="asset path is outside local project root")
        return {"records": [], "provenance": provenance, "status": "BLOCKED", "failure_type": "NON_LOCAL_ASSET"}
    if not inventory_path.exists():
        provenance = _asset_provenance(inventory_path, source_type="inventory", status="missing", reason="inventory file does not exist")
        return {"records": [], "provenance": provenance, "status": "BLOCKED", "failure_type": "missing_inventory"}
    try:
        import yaml
        document = yaml.safe_load(inventory_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        provenance = _asset_provenance(inventory_path, source_type="inventory", status="blocked", reason=str(exc))
        return {"records": [], "provenance": provenance, "status": "BLOCKED", "failure_type": "BASELINE_INVALID"}
    except Exception as exc:  # yaml.YAMLError is version-specific; keep the public failure stable.
        provenance = _asset_provenance(inventory_path, source_type="inventory", status="blocked", reason=f"invalid YAML: {exc}")
        return {"records": [], "provenance": provenance, "status": "BLOCKED", "failure_type": "BASELINE_INVALID"}
    if not isinstance(document, list):
        provenance = _asset_provenance(inventory_path, source_type="inventory", status="blocked", reason="inventory root must be a list")
        return {"records": [], "provenance": provenance, "status": "BLOCKED", "failure_type": "BASELINE_INVALID"}
    if any(not isinstance(item, dict) for item in document):
        provenance = _asset_provenance(inventory_path, source_type="inventory", status="blocked", reason="inventory records must be objects")
        return {"records": [], "provenance": provenance, "status": "BLOCKED", "failure_type": "BASELINE_INVALID"}
    provenance = _asset_provenance(inventory_path, source_type="inventory", status="loaded")
    return {"records": document, "provenance": provenance, "status": "PASS", "failure_type": ""}


@dataclass(frozen=True)
class DiscoveryResult:
    project_fingerprint: str
    interfaces: tuple[InterfaceIR, ...]
    unsupported: tuple[dict[str, Any], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "2.0",
            "project_fingerprint": self.project_fingerprint,
            "interfaces": [item.to_dict() for item in self.interfaces],
            "unsupported": list(self.unsupported),
        }


_HTTP_CALL = re.compile(
    r"(?P<method>GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s*"
    r"(?:\(|[:=,\s\"'])+\s*(?P<path>/[A-Za-z0-9_./:{}?=&-]+)", re.I
)
_HTTP_CHAIN = re.compile(r"\.(?P<method>get|post|put|patch|delete)\s*\(\s*['\"](?P<path>/[^'\"]+)", re.I)
_GRPC = re.compile(r"rpc\s+(?P<name>[A-Za-z_]\w*)\s*\((?P<request>[^)]+)\)\s*returns\s*\((?P<response>[^)]+)\)", re.I)
_GRAPHQL = re.compile(r"(?:type\s+Query|type\s+Mutation|type\s+Subscription)\s*\{(?P<body>[^}]+)\}", re.I | re.S)
_PROTOCOL_MARKERS = {
    "graphql": re.compile(r"\b(?:type\s+(?:Query|Mutation|Subscription)|graphql\.)", re.I),
    "websocket": re.compile(r"\b(?:websocket|web_socket|socket\.io)\b", re.I),
    "soap": re.compile(r"\b(?:wsdl|soap:Envelope|SOAPAction)\b", re.I),
    "jsonrpc": re.compile(r"\b(?:jsonrpc|JsonRpc)\b", re.I),
    "message": re.compile(r"\b(?:kafka|rabbitmq|amqp|consumer|message[_ -]?handler)\b", re.I),
    "scheduler": re.compile(r"\b(?:cron|scheduled|schedule\(|定时任务)\b", re.I),
    "event": re.compile(r"\b(?:event[_ -]?handler|on_event|subscribe\()\b", re.I),
}


def _fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(_candidate_files(root)):
        try:
            digest.update(str(path.relative_to(root)).encode("utf-8"))
            digest.update(path.read_bytes())
        except OSError:
            continue
    return digest.hexdigest()


def _candidate_files(root: Path) -> Iterable[Path]:
    ignored = {".git", "node_modules", "vendor", "dist", "build", "coverage", ".venv"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored for part in path.parts):
            continue
        if path.suffix.lower() in {".py", ".go", ".java", ".kt", ".ts", ".tsx", ".js", ".jsx", ".rb", ".php", ".proto", ".graphql", ".gql", ".wsdl", ".xml", ".yaml", ".yml", ".json"}:
            yield path


def _interface(project: str, root: Path, path: Path, protocol: str, operation: str, entrypoint: dict[str, Any], *, evidence: str, parameters: list[ParameterIR] | None = None, request_schema: dict[str, Any] | None = None, response_schema: dict[str, Any] | None = None, completeness: str = "partial", confidence: float = 0.6, risk: str = "P2") -> InterfaceIR:
    return InterfaceIR(
        project_fingerprint=project,
        service_id=path.parent.name or "default",
        operation_id=operation,
        protocol=protocol,
        entrypoint=entrypoint,
        parameters=tuple(parameters or ()),
        request_schema=request_schema or {},
        response_schema=response_schema or {},
        evidence=({"source": str(path.relative_to(root)), "evidence": evidence},),
        completeness=completeness,
        confidence=confidence,
        adapter=f"builtin.{protocol}",
        adapter_version="2.0",
        risk=risk,
    )


def _parse_openapi(root: Path, project: str, path: Path) -> list[InterfaceIR]:
    try:
        import yaml
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (ImportError, OSError, ValueError):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []
    if not isinstance(document, dict) or not isinstance(document.get("paths"), dict):
        return []
    result: list[InterfaceIR] = []
    for route, operations in document["paths"].items():
        if not isinstance(operations, dict):
            continue
        for method, spec in operations.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete", "head", "options"} or not isinstance(spec, dict):
                continue
            params = []
            for item in spec.get("parameters", []) or []:
                if isinstance(item, dict) and item.get("name"):
                    params.append(ParameterIR(name=str(item["name"]), location=str(item.get("in", "query")), required=bool(item.get("required", False)), schema=dict(item.get("schema", {})), sensitive=str(item.get("name")).lower() in {"token", "password", "secret", "authorization"}))
            response_schema: dict[str, Any] = {}
            responses = spec.get("responses", {})
            success = responses.get("200", responses.get("201", {})) if isinstance(responses, dict) else {}
            content = success.get("content", {}) if isinstance(success, dict) else {}
            application_json = content.get("application/json", {}) if isinstance(content, dict) else {}
            schema = application_json.get("schema", {}) if isinstance(application_json, dict) else {}
            if isinstance(schema, dict):
                response_schema = dict(schema)
            result.append(_interface(project, root, path, "http", str(spec.get("operationId") or f"{method}_{route}"), {"method": method.upper(), "path": str(route), "base_url_ref": "local_config"}, evidence=f"openapi.paths.{route}.{method}", parameters=params, response_schema=response_schema, completeness="complete", confidence=0.98, risk="P1" if method.lower() in {"post", "put", "patch", "delete"} else "P2"))
    return result


def discover_project(project_root: str | Path) -> DiscoveryResult:
    """[参数] project_root: 被测项目根目录；[返回] 发现结果；最近修改时间: 2026-07-12 19:17:12 修复无 gRPC 匹配时复用未绑定入口。"""

    root = Path(project_root).resolve()
    project = _fingerprint(root)
    discovered: dict[tuple[str, str, str], InterfaceIR] = {}
    unsupported: list[dict[str, Any]] = []
    for path in _candidate_files(root):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        suffix = path.suffix.lower()
        if suffix in {".yaml", ".yml", ".json"} and path.name.lower() in {"openapi.yaml", "openapi.yml", "swagger.yaml", "swagger.yml", "openapi.json", "swagger.json"}:
            for item in _parse_openapi(root, project, path):
                discovered[(item.protocol, str(path.relative_to(root)), str(item.entrypoint))] = item
        for match in _HTTP_CALL.finditer(content):
            method, route = match.group("method").upper(), match.group("path")
            item = _interface(project, root, path, "http", f"{method}_{route}", {"method": method, "path": route, "base_url_ref": "local_config"}, evidence=f"line {content[:match.start()].count(chr(10)) + 1}", completeness="partial", confidence=0.65, risk="P1" if method in {"POST", "PUT", "PATCH", "DELETE"} else "P2")
            discovered.setdefault((item.protocol, str(path.relative_to(root)), str(item.entrypoint)), item)
        for match in _HTTP_CHAIN.finditer(content):
            method, route = match.group("method").upper(), match.group("path")
            item = _interface(project, root, path, "http", f"{method}_{route}", {"method": method, "path": route, "base_url_ref": "local_config"}, evidence=f"line {content[:match.start()].count(chr(10)) + 1}", confidence=0.62, risk="P1" if method in {"POST", "PUT", "PATCH", "DELETE"} else "P2")
            discovered.setdefault((item.protocol, str(path.relative_to(root)), str(item.entrypoint)), item)
        # 3. 只有当前文件存在 gRPC 声明时才写入入口，避免无匹配时引用未绑定的 item。
        if suffix != ".proto":
            for match in _GRPC.finditer(content):
                item = _interface(project, root, path, "grpc", match.group("name"), {"service": path.stem, "method": match.group("name"), "request_type": match.group("request").strip(), "response_type": match.group("response").strip()}, evidence=f"line {content[:match.start()].count(chr(10)) + 1}", confidence=0.9)
                # 4. 以 source + entrypoint 去重，保留同名但来自不同文件的 gRPC 入口。
                discovered.setdefault((item.protocol, str(path.relative_to(root)), str(item.entrypoint)), item)
        # 1. 标准协议 adapter 只读取与自身相关的声明，避免 README/历史报告造成误报。
        for adapter in discovery_adapters():
            if not _adapter_relevant(adapter.protocol, path, content):
                continue
            try:
                items = adapter.discover(DiscoveryContext(root=root, project_fingerprint=project, path=path, content=content))
            except (OSError, ValueError, TypeError):
                # 2. 单个声明解析失败不能污染其他协议；证据由 unsupported 记录。
                unsupported.append(_unsupported(path, getattr(adapter, "protocol", "unknown"), "adapter parse failed", adapter_status(getattr(adapter, "protocol", "unknown"))))
                continue
            for item in items:
                discovered[(item.protocol, str(path.relative_to(root)), str(item.entrypoint))] = item
        if suffix in {".proto", ".graphql", ".gql"} and not any(item.evidence[0].get("source") == str(path.relative_to(root)) for item in discovered.values()):
            protocol = "grpc" if suffix == ".proto" else "graphql"
            unsupported.append(_unsupported(path, protocol, "entrypoint requires adapter parsing", adapter_status(protocol), root))
        for protocol, marker in _PROTOCOL_MARKERS.items():
            has_discovered = any(item.protocol == protocol and item.evidence and item.evidence[0].get("source") == str(path.relative_to(root)) for item in discovered.values())
            if marker.search(content) and not has_discovered and not any(item.get("protocol") == protocol and item.get("source") == str(path.relative_to(root)) for item in unsupported):
                unsupported.append(_unsupported(path, protocol, "entrypoint detected but execution adapter is pending", adapter_status(protocol), root))
    interfaces = tuple(sorted(discovered.values(), key=lambda item: (item.protocol, item.service_id, item.operation_id)))
    return DiscoveryResult(project, interfaces, tuple(unsupported))


def _unsupported(path: Path, protocol: str, reason: str, status: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    """[参数] path/protocol/reason/status: 未支持入口事实；root: 项目根目录；[返回] 结构化 PENDING 记录；最近修改时间: 2026-07-12 19:20:00 统一降级状态。"""

    return {"status": "PENDING", "failure_type": "UNSUPPORTED_ADAPTER", "protocol": protocol, "source": str(path.relative_to(root or path.parent)), "reason": reason, "adapter": status}


def _adapter_relevant(protocol: str, path: Path, content: str) -> bool:
    """[参数] protocol/path/content: 当前候选文件事实；[返回] 是否交给 adapter；最近修改时间: 2026-07-12 19:20:00 限制发现误报。"""

    suffix = path.suffix.lower()
    marker = content.lower()
    checks = {
        "graphql": suffix in {".graphql", ".gql"} or "type query" in marker or "@query" in marker or "graphql" in marker,
        "grpc": suffix == ".proto" or "rpc." in marker or "service " in marker and " rpc " in marker,
        "websocket": any(item in marker for item in ("websocket", "web_socket", "socket.io", "new websocket")),
        "soap-jsonrpc": suffix in {".wsdl", ".xml", ".json"} or any(item in marker for item in ("soapaction", "soap:envelope", "jsonrpc", "json-rpc")),
        "message": any(item in marker for item in ("kafkalistener", "rabbitlistener", "rabbitmq", "kafka", "consumer", "subscribe(", "publish(")),
        "cli": "add_parser" in marker or "click.command" in marker or "typer.command" in marker or "@command" in marker,
        "scheduler": any(item in marker for item in ("@scheduled", "cron", "add_job", "schedule(")),
        "event": any(item in marker for item in ("event_handler", "on_event", "event_bus.subscribe", "@receiver")),
    }
    return checks.get(protocol, False)
