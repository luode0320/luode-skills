"""从接口与消费者事实生成不可直接放行的候选场景。"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .scenario_loader import source_fingerprint
from .scenario_model import SCENARIO_SCHEMA_VERSION


def generate_candidates(interfaces: Iterable[Mapping[str, Any]], *, consumer: str, source_name: str) -> dict[str, Any]:
    """为 HTTP 入口生成最小 candidate；生成结果必须另行 verify。

    [参数] interfaces: 接口事实集合；consumer: 消费者标识；source_name: local 来源资产名称。
    [返回] external-scenario/1.0 候选目录，生命周期固定为 candidate。
    最近修改时间：2026-07-25 20:50:00，补齐候选生成边界并强调不能直接进入门禁。
    """

    # 1. 只从 HTTP 接口事实生成最小请求骨架，未知协议和缺少身份的记录直接跳过。
    scenarios: dict[str, Any] = {}
    for item in interfaces:
        # 1.1 每条事实先过滤协议和身份，再生成不可放行的最小请求骨架。
        if str(item.get("protocol", "")) != "http":
            continue
        operation_id = str(item.get("operation_id", "")).strip()
        entrypoint = item.get("entrypoint", {})
        if not operation_id or not isinstance(entrypoint, Mapping):
            continue
        evidence = [{"source": source_name, "operation_id": operation_id, "adapter": item.get("adapter", "unknown")}]
        scenarios[operation_id] = {
            "scenario_id": operation_id,
            "risk": str(item.get("risk", "P2")),
            "consumers": [consumer],
            "source_evidence": evidence,
            "source_fingerprint": source_fingerprint(evidence),
            "lifecycle": "candidate",
            "preconditions": [{"environment": "local"}],
            "steps": [{"step_id": "request", "action": "http.request", "config": {"method": entrypoint.get("method", "GET"), "url_ref": operation_id}, "captures": {}, "assertions": [], "parallel_group": ""}],
            "assertions": [],
            "cleanup": [],
            "verification": {"contract_valid": False, "positive_passed": False, "fault_detected": False, "cleanup_passed": False, "source_current": True},
        }
    # 2. 生成器只输出未验证候选，所有验证门槛默认关闭。
    return {"schema_version": SCENARIO_SCHEMA_VERSION, "scenarios": scenarios}
