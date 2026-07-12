"""SOAP/WSDL 与 JSON-RPC 声明发现适配器。"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

from ..model import InterfaceIR, ParameterIR
from .base import DiscoveryContext, evidence, line_number, make_interface


_RPC_SOURCE = re.compile(r"(?:jsonrpc|JSONRPC|rpc)\.(?:method|register|route)\s*\(\s*['\"](?P<method>[A-Za-z0-9_.:/-]+)", re.I)
_RPC_OBJECT = re.compile(r"[\"']jsonrpc[\"']\s*[:=]\s*[\"']2\.0[\"'].*?[\"']method[\"']\s*[:=]\s*[\"'](?P<method>[A-Za-z0-9_.:/-]+)", re.I | re.S)
_SOAP_MARKER = re.compile(r"\b(?:SOAPAction|soap:Envelope|wsdl:definitions|@WebService|@WebMethod)\b", re.I)


def _local(tag: str) -> str:
    """[参数] tag: XML QName；[返回] 本地标签名；最近修改时间: 2026-07-12 19:20:00 兼容带命名空间的 WSDL。"""

    return tag.rsplit("}", 1)[-1]


class SoapJsonRpcAdapter:
    """解析 WSDL operation 与 JSON-RPC method；不依赖第三方 XML/JSON 库。"""

    protocol = "soap-jsonrpc"
    name = "builtin.soap-jsonrpc"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: WSDL、JSON 或 RPC 源码上下文；[返回] SOAP/JSON-RPC IR；最近修改时间: 2026-07-12 19:20:00 归一化两类 RPC 入口。"""

        if context.path.suffix.lower() in {".wsdl", ".xml"} or "<wsdl:" in context.content.lower() or "<definitions" in context.content.lower():
            yield from self._wsdl(context)
        yield from self._jsonrpc(context)

    def _wsdl(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: WSDL 上下文；[返回] SOAP operation IR；最近修改时间: 2026-07-12 19:20:00 解析 service/portType。"""

        try:
            root = ET.fromstring(context.content)
        except ET.ParseError:
            return
        services = {item.attrib.get("name", "default") for item in root.iter() if _local(item.tag) == "service"}
        service = next(iter(services), context.path.stem)
        for port_type in root.iter():
            if _local(port_type.tag) != "portType":
                continue
            service_name = port_type.attrib.get("name", service)
            for operation in port_type:
                if _local(operation.tag) != "operation" or not operation.attrib.get("name"):
                    continue
                name = operation.attrib["name"]
                yield make_interface(
                    context,
                    "soap",
                    f"{service_name}.{name}",
                    {"endpoint_ref": "local_config", "service": service_name, "method": name, "soap_action_ref": f"{service_name}/{name}"},
                    parameters=(ParameterIR(name="request", location="body", required=True, schema={"type": "object"}),),
                    request_schema={"type": "object", "wsdl_operation": name},
                    response_schema={"type": "object"},
                    evidence_items=evidence(context, f"WSDL operation {service_name}.{name}", kind="wsdl"),
                    completeness="complete",
                    confidence=0.98,
                    risk="P1" if name.lower().startswith(("create", "update", "delete", "submit")) else "P2",
                )

    def _jsonrpc(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: JSON-RPC 文件或源码上下文；[返回] method IR；最近修改时间: 2026-07-12 19:20:00 解析 method 声明和请求样例。"""

        methods: list[tuple[str, int, str]] = []
        if context.path.suffix.lower() == ".json":
            try:
                document = json.loads(context.content)
            except (TypeError, ValueError):
                document = {}
            values = document if isinstance(document, list) else [document]
            for item in values:
                if isinstance(item, dict) and item.get("jsonrpc") == "2.0" and item.get("method"):
                    methods.append((str(item["method"]), 1, "json-rpc request"))
        for pattern in (_RPC_SOURCE, _RPC_OBJECT):
            methods.extend((match.group("method"), line_number(context.content, match.start()), "JSON-RPC method declaration") for match in pattern.finditer(context.content))
        seen: set[str] = set()
        for method, line, description in methods:
            if method in seen:
                continue
            seen.add(method)
            yield make_interface(
                context,
                "jsonrpc",
                method,
                {"endpoint_ref": "local_config", "method": method, "jsonrpc": "2.0"},
                parameters=(ParameterIR(name="params", location="body", required=False, schema={"type": ["object", "array", "null"]}),),
                request_schema={"type": "object", "required": ["jsonrpc", "method"], "properties": {"jsonrpc": {"const": "2.0"}, "method": {"const": method}}},
                response_schema={"type": "object", "required": ["jsonrpc", "id"]},
                evidence_items=evidence(context, description + f": {method}", line=line, kind="jsonrpc"),
                completeness="complete",
                confidence=0.94,
            )


ADAPTER = SoapJsonRpcAdapter()
