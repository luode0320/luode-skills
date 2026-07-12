"""v1 基线迁移到 v2，保留来源和迁移证据。"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Mapping


def migrate_v1_to_v2(document: Mapping[str, Any], *, project_fingerprint: str, source_revision: str = "") -> dict[str, Any]:
    if str(document.get("schema_version", "1")) == "2.0":
        return deepcopy(dict(document))
    result = deepcopy(dict(document))
    result["schema_version"] = "2.0"
    result["project_fingerprint"] = project_fingerprint
    result["source_revision"] = source_revision
    result["migrated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    result["migration"] = {"from": str(document.get("schema_version", "1")), "to": "2.0", "lossless": True}
    result.setdefault("adapter", {"name": "legacy-v1", "version": "1"})
    result.setdefault("evidence", [])
    if isinstance(result["evidence"], list):
        result["evidence"].append({"type": "migration", "source_schema": str(document.get("schema_version", "1")), "source_revision": source_revision})
    return result
