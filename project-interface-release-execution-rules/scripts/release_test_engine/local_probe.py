"""受控 local 只读探针注册表。"""

from __future__ import annotations

from typing import Any, Callable, Mapping


class LocalProbeRegistry:
    """只允许项目显式注册的只读探针执行。"""

    def __init__(self) -> None:
        """初始化空探针 allowlist。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，新增受控 local 探针注册入口。
        """

        # 1. 场景文件只引用名称，实际读取函数必须由项目适配器在运行时注册。
        self._readers: dict[str, Callable[[Mapping[str, Any]], Any]] = {}

    def register_readonly(self, name: str, reader: Callable[[Mapping[str, Any]], Any]) -> None:
        """注册一个只读探针。

        [参数] name: 探针 allowlist 名称；reader: 只读实现函数。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，限制探针来源并拒绝重复覆盖。
        """

        # 1. 名称必须稳定且不可为空，重复注册显式失败防止静默替换 oracle。
        key = str(name).strip()
        if not key or not callable(reader):
            raise ValueError("PROBE_REGISTRATION_INVALID")
        if key in self._readers:
            raise ValueError(f"PROBE_ALREADY_REGISTERED:{key}")
        self._readers[key] = reader

    def execute(self, config: Mapping[str, Any], environment: str) -> dict[str, Any]:
        """执行一个 local 只读探针。

        [参数] config: 探针名称和只读参数；environment: 执行环境。
        [返回] 脱离数据库连接对象的结构化探针结果。
        最近修改时间：2026-07-25 15:00:00，新增非 local、非 allowlist 和原始 SQL 阻断。
        """

        # 1. 先校验配置归属和禁止字段，探针不得绕过 local 与结构化参数边界。
        provenance = str(config.get("config_environment", environment)).lower()
        if environment != "local" or provenance not in {"local", "local-dev", "development"}:
            raise PermissionError("LOCAL_CONFIG_PROVENANCE_INVALID")
        if any(key in config for key in ("sql", "query_sql", "python", "code", "path")):
            raise PermissionError("PROBE_RAW_ACCESS_FORBIDDEN")
        name = str(config.get("name", "")).strip()
        reader = self._readers.get(name)
        if reader is None:
            raise PermissionError("PROBE_NOT_ALLOWLISTED")

        # 2. 只返回 reader 的值和探针名，不暴露连接、游标或敏感环境对象。
        return {"probe": name, "value": reader(dict(config.get("args", {})))}
