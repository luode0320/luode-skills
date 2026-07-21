"""Protocol Buffer gRPC service 发现适配器。"""

from __future__ import annotations

import re
from typing import Iterable

from ..model import InterfaceIR, ParameterIR
from .base import DiscoveryContext, evidence, line_number, make_interface


_SERVICE = re.compile(r"\bservice\s+(?P<service>[A-Za-z_]\w*)\s*\{(?P<body>.*?)\}", re.I | re.S)
_RPC = re.compile(r"\brpc\s+(?P<method>[A-Za-z_]\w*)\s*\((?P<request>[^)]+)\)\s*returns\s*(?:stream\s+)?\((?P<response>[^)]+)\)", re.I)
_RPC_SOURCE = re.compile(r"(?:grpc|rpc)\.(?:unary_unary|unary_stream|stream_unary|stream_stream)\s*\(\s*['\"](?P<path>/[^'\"]+)", re.I)


class GrpcAdapter:
    """解析 proto service/rpc，保存 stream 与消息类型证据。"""

    protocol = "grpc"
    name = "builtin.grpc"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: proto 或 gRPC 源码上下文；[返回] RPC 方法 IR；最近修改时间: 2026-07-12 19:20:00 支持 unary/stream 声明。"""

        services = list(_SERVICE.finditer(context.content))
        for service in services:
            for rpc in _RPC.finditer(service.group("body")):
                method = rpc.group("method")
                stream = "stream" in rpc.group(0).lower()
                request_type = rpc.group("request").replace("stream", "").strip()
                response_type = rpc.group("response").strip()
                yield make_interface(
                    context,
                    "grpc",
                    f"{service.group('service')}.{method}",
                    {
                        "target_ref": "local_config",
                        "service": service.group("service"),
                        "method": method,
                        "request_type": request_type,
                        "response_type": response_type,
                        "stream": stream,
                    },
                    parameters=(ParameterIR(name="request", location="body", required=True, schema={"$ref": request_type}),),
                    request_schema={"$ref": request_type},
                    response_schema={"$ref": response_type},
                    evidence_items=evidence(context, f"service {service.group('service')} rpc {method}", line=line_number(context.content, service.start()), kind="protobuf"),
                    completeness="complete",
                    confidence=0.98,
                    risk="P1" if method.lower().startswith(("create", "update", "delete", "set")) else "P2",
                )
        if not services:
            for match in _RPC_SOURCE.finditer(context.content):
                path = match.group("path")
                method = path.rsplit("/", 1)[-1]
                yield make_interface(
                    context,
                    "grpc",
                    method,
                    {"target_ref": "local_config", "method_path": path, "method": method},
                    parameters=(ParameterIR(name="request", location="body", required=True, schema={"type": "object"}),),
                    evidence_items=evidence(context, f"gRPC call {path}", line=line_number(context.content, match.start()), kind="grpc-source"),
                    confidence=0.75,
                )


ADAPTER = GrpcAdapter()
