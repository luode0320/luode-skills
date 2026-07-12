"""GraphQL schema 与常见 resolver 声明发现适配器。"""

from __future__ import annotations

import re
from typing import Iterable

from ..model import InterfaceIR, ParameterIR
from .base import DiscoveryContext, DiscoveryAdapter, evidence, line_number, make_interface


_ROOT = re.compile(r"\btype\s+(?P<kind>Query|Mutation|Subscription)\s*\{(?P<body>.*?)\}", re.I | re.S)
_FIELD = re.compile(r"(?P<name>[A-Za-z_]\w*)\s*(?:\((?P<args>[^)]*)\))?\s*:\s*(?P<type>[\[\]!A-Za-z0-9_]+)")
_ARG = re.compile(r"(?P<name>[A-Za-z_]\w*)\s*:\s*(?P<type>[\[\]!A-Za-z0-9_]+)(?:\s*=\s*(?P<default>[^,]+))?")
_DECORATOR = re.compile(r"@(?:Query|Mutation|Subscription)\s*\(?\s*['\"]?(?P<name>[A-Za-z_]\w*)", re.I)


class GraphQLAdapter:
    """解析 GraphQL root field，执行能力由 HTTP runner 或外部 adapter 提供。"""

    protocol = "graphql"
    name = "builtin.graphql"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: 当前项目文件上下文；[返回] GraphQL root field IR；最近修改时间: 2026-07-12 19:20:00 支持 schema 和 resolver 声明。"""

        matches = list(_ROOT.finditer(context.content))
        if not matches:
            matches = self._resolver_fields(context)
        for root in matches:
            kind = root.groupdict().get("kind", "Query").lower()
            body = root.group("body")
            for field in _FIELD.finditer(body):
                name = field.group("name")
                args = self._parameters(field.group("args") or "")
                yield make_interface(
                    context,
                    "graphql",
                    f"{kind}_{name}",
                    {
                        "endpoint_ref": "local_config",
                        "operation_type": kind,
                        "field": name,
                        "query": self._query(kind, name, args),
                    },
                    parameters=args,
                    request_schema={"type": "object", "properties": {item.name: dict(item.schema) for item in args}},
                    response_schema={"type": "object", "field": name, "graphql_type": field.group("type")},
                    evidence_items=evidence(context, f"type {root.group('kind')} field {name}", line=line_number(context.content, root.start()), kind="graphql-schema"),
                    completeness="complete",
                    confidence=0.96,
                    risk="P1" if kind == "mutation" else "P2",
                )

    def _resolver_fields(self, context: DiscoveryContext) -> list[re.Match[str]]:
        """[参数] context: resolver 文件上下文；[返回] 转换后的 root field 匹配；最近修改时间: 2026-07-12 19:20:00 兼容装饰器声明。"""

        result: list[re.Match[str]] = []
        for match in _DECORATOR.finditer(context.content):
            # resolver 没有完整 schema 时，构造同一字段解析器可消费的最小对象。
            field = match.group("name")
            fake = f"type Query {{ {field}: JSON }}"
            result.extend(_ROOT.finditer(fake))
        return result

    @staticmethod
    def _parameters(value: str) -> list[ParameterIR]:
        """[参数] value: GraphQL 参数片段；[返回] 参数 IR；最近修改时间: 2026-07-12 19:20:00 解析 required 与默认值。"""

        result: list[ParameterIR] = []
        for match in _ARG.finditer(value):
            graphql_type = match.group("type")
            result.append(ParameterIR(name=match.group("name"), location="body", required=graphql_type.endswith("!"), schema={"type": graphql_type.rstrip("!")}, source={"type": "graphql_schema", "example": match.group("default")} if match.group("default") else None))
        return result

    @staticmethod
    def _query(kind: str, name: str, args: list[ParameterIR]) -> str:
        """[参数] kind/name/args: root field 信息；[返回] 可复用查询模板；最近修改时间: 2026-07-12 19:20:00 生成参数化请求模板。"""

        variables = ", ".join(f"${item.name}: {item.schema.get('type', 'String')}" for item in args)
        call = ", ".join(f"{item.name}: ${item.name}" for item in args)
        header = f"{kind} {name}({variables})" if variables else kind
        return f"{header} {{ {name}({call}) {{ __typename }} }}" if call else f"{header} {{ {name} {{ __typename }} }}"


ADAPTER = GraphQLAdapter()
