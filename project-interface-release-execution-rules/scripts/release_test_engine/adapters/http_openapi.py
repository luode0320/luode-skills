"""OpenAPI 文件发现适配器。

该模块提供可独立调用的 adapter API；主 discovery 仍保留旧解析入口以兼容
历史脚本。
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from ..model import InterfaceIR, ParameterIR
from .base import DiscoveryContext, make_interface


class OpenAPIAdapter:
    """解析 OpenAPI/Swagger paths 并保留参数 schema。"""

    protocol = "http"
    name = "builtin.http-openapi"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: OpenAPI YAML/JSON 上下文；[返回] HTTP 入口 IR；最近修改时间: 2026-07-12 19:35:00 暴露独立 OpenAPI adapter。"""

        document = self._load(context.content)
        paths = document.get("paths", {}) if isinstance(document, dict) else {}
        if not isinstance(paths, dict):
            return
        for route, operations in paths.items():
            if not isinstance(operations, dict):
                continue
            for method, spec in operations.items():
                if method.lower() not in {"get", "post", "put", "patch", "delete", "head", "options"} or not isinstance(spec, dict):
                    continue
                parameters = [ParameterIR(name=str(item["name"]), location=str(item.get("in", "query")), required=bool(item.get("required", False)), schema=dict(item.get("schema", {}))) for item in spec.get("parameters", []) if isinstance(item, dict) and item.get("name")]
                yield make_interface(context, "http", str(spec.get("operationId") or f"{method}_{route}"), {"method": method.upper(), "path": str(route), "base_url_ref": "local_config"}, parameters=parameters, request_schema=dict(spec.get("requestBody", {})), response_schema=dict(spec.get("responses", {})), completeness="complete", confidence=0.99, adapter=self.name, risk="P1" if method.lower() in {"post", "put", "patch", "delete"} else "P2")

    @staticmethod
    def _load(content: str) -> dict[str, Any]:
        """[参数] content: 文档文本；[返回] 解析对象；最近修改时间: 2026-07-12 19:35:00 使用可选 YAML 和标准 JSON。"""

        try:
            import yaml
            value = yaml.safe_load(content)
        except (ImportError, ValueError):
            try:
                value = json.loads(content)
            except ValueError:
                value = {}
        return value if isinstance(value, dict) else {}


ADAPTER = OpenAPIAdapter()
