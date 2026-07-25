"""旧场景结果资产的只读兼容迁移。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .report_support import redact_evidence


def load_compatible_scenario_results(source: str | Path | Mapping[str, Any] | list[Any]) -> dict[str, Any]:
    """加载新旧两种场景结果形状并标记旧资产。

    [参数] source: JSON 文件路径、新版对象、旧版列表或已解析映射。
    [返回] 统一的场景结果对象，包含弃用状态和迁移提示。
    最近修改时间: 2026-07-25 17:35:00 改动原因: 保留旧报告读取能力且阻止接口结果冒充场景通过。
    """

    # 1. 只读加载输入，旧文件不原地覆盖，避免兼容读取破坏历史证据。
    document: Any = source
    if isinstance(source, (str, Path)):
        document = json.loads(Path(source).read_text(encoding="utf-8"))
    if isinstance(document, list):
        # 2. 旧列表每一项都是接口结果，迁移后固定为 PENDING 而不是沿用旧 PASS。
        items = [_legacy_item(item) for item in document if isinstance(item, Mapping)]
        return {"schema_version": "external-scenario/1.0", "status": "deprecated", "deprecated": True, "migration": "legacy-interface-results", "results": items}
    if not isinstance(document, Mapping):
        raise ValueError("scenario result document must be an object or array")
    result = dict(document)
    result.setdefault("schema_version", "external-scenario/1.0")
    result.setdefault("results", [])
    result.setdefault("deprecated", False)
    result.setdefault("status", "not_configured" if not result["results"] else "PENDING")
    return result


def migrate_scenario_results(source: str | Path | Mapping[str, Any] | list[Any], output: str | Path) -> dict[str, Any]:
    """把旧场景结果迁移为新对象并写入独立 UTF-8 文件。

    [参数] source: 旧或新场景结果输入；output: 项目根内的迁移输出路径。
    [返回] 迁移摘要和输出路径。
    最近修改时间: 2026-07-25 23:37:04 改动原因: 迁移写盘前统一脱敏新旧结果。
    """

    # 1. 迁移输出不覆盖输入；写盘点再次递归脱敏，防止新旧输入携带原始凭据。
    loaded = load_compatible_scenario_results(source)
    result = dict(redact_evidence(loaded))
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "PASS", "deprecated": bool(result.get("deprecated")), "output": str(output_path), "scenario_count": len(result.get("results", [])), "migration": result.get("migration", "none")}


def _legacy_item(item: Mapping[str, Any]) -> dict[str, Any]:
    """将一条旧接口结果包装为不可放行的待验证场景结果。

    [参数] item: 旧版接口结果。
    [返回] 带旧来源标识的待验证场景结果。
    最近修改时间: 2026-07-25 23:37:04 改动原因: 旧结果包装时立即移除凭据和原始失败文本。
    """

    # 1. 保留脱敏后的旧结果作为证据摘要，不复制为真实步骤事件。
    operation_id = str(item.get("operation_id", "legacy-unknown"))
    return {"scenario_id": f"legacy:{operation_id}", "risk": str(item.get("risk", "P2")), "consumers": [], "status": "PENDING", "failure_type": "LEGACY_INTERFACE_RESULT", "reason": "legacy interface result requires external scenario verification", "legacy_result": dict(redact_evidence(dict(item))), "steps": [], "cleanup": []}
