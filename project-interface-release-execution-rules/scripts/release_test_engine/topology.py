"""依赖评分、拓扑排序和 provider 失败传播。"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, Iterable, Mapping


class TopologyError(ValueError):
    """依赖图不完整、存在低置信边或循环。"""


def infer_edges(interfaces: Iterable[Any]) -> list[dict[str, Any]]:
    items = list(interfaces)
    providers_by_field: dict[str, list[str]] = defaultdict(list)
    for interface in items:
        schema = getattr(interface, "response_schema", {}) or {}
        properties = schema.get("properties", {}) if isinstance(schema, Mapping) else {}
        for field in properties:
            providers_by_field[str(field)].append(interface.operation_id)
    edges: list[dict[str, Any]] = []
    for consumer in items:
        for parameter in getattr(consumer, "parameters", ()):
            source = parameter.source or {}
            explicit = source.get("interface") if isinstance(source, Mapping) else None
            if explicit:
                edges.append({"provider": str(explicit), "consumer": consumer.operation_id, "field": parameter.name, "confidence": 1.0, "reason": "explicit parameter source"})
                continue
            providers = [provider for provider in providers_by_field.get(parameter.name, []) if provider != consumer.operation_id]
            if len(providers) == 1:
                edges.append({"provider": providers[0], "consumer": consumer.operation_id, "field": parameter.name, "confidence": 0.65, "reason": "unique response field match"})
    return edges


def ordered_nodes(nodes: Iterable[str], edges: Iterable[Mapping[str, Any]], *, min_confidence: float = 0.0) -> list[str]:
    node_set = set(nodes)
    outgoing: dict[str, set[str]] = defaultdict(set)
    indegree = {node: 0 for node in node_set}
    for edge in edges:
        confidence = float(edge.get("confidence", 1.0))
        provider, consumer = str(edge.get("provider", "")), str(edge.get("consumer", ""))
        if confidence < min_confidence:
            continue
        if provider not in node_set or consumer not in node_set:
            raise TopologyError(f"edge references unknown node: {provider}->{consumer}")
        if consumer not in outgoing[provider]:
            outgoing[provider].add(consumer)
            indegree[consumer] += 1
    queue = deque(sorted(item for item, degree in indegree.items() if degree == 0))
    result: list[str] = []
    while queue:
        current = queue.popleft()
        result.append(current)
        for child in sorted(outgoing[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(result) != len(node_set):
        raise TopologyError("dependency graph contains a cycle")
    return result


def dependency_status(provider_status: str, *, consumer: str, provider: str) -> dict[str, Any]:
    if provider_status == "PASS":
        return {"consumer": consumer, "provider": provider, "status": "READY"}
    return {"consumer": consumer, "provider": provider, "status": "BLOCKED", "failure_type": "BLOCKED_BY_DEPENDENCY", "reason": f"provider status is {provider_status}"}
