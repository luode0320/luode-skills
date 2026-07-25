"""隔离上线测试工具环境的只读 doctor。"""

from __future__ import annotations

import importlib
import importlib.metadata
import platform
import sys
from typing import Any, Mapping


REQUIRED_PACKAGES = {
    "PyYAML": ("yaml", "6.0.2"),
    "jsonschema": ("jsonschema", "4.25.1"),
    "websockets": ("websockets", "15.0.1"),
    "python-socketio": ("socketio", "5.16.3"),
    "aiohttp": ("aiohttp", "3.12.15"),
    "requests": ("requests", "2.32.4"),
    "websocket-client": ("websocket", "1.8.0"),
}


def inspect_tool_environment(*, required_packages: Mapping[str, tuple[str, str]] = REQUIRED_PACKAGES) -> dict[str, Any]:
    """只读检查 Python 版本、依赖版本和实时协议 runtime。

    [参数] required_packages: distribution 名称到导入模块和最低锁定版本的映射。
    [返回] 可归档的工具环境状态、版本明细和缺口分类。
    最近修改时间: 2026-07-25 18:05:00 改动原因: 为 C18-02 提供隔离工具环境 doctor。
    """

    # 1. 先检查解释器主版本；低于 Python 3.11 时不允许继续协议测试。
    python_ready = sys.version_info >= (3, 11)
    packages: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    mismatched: list[str] = []
    for distribution, (module_name, expected) in required_packages.items():
        # 1.1 每个依赖分别核对已安装版本和可导入性，两项都满足才标记 ready。
        # 1.2 依赖记录固定包含身份、期望版本、实际版本、可导入性和状态。
        record: dict[str, Any] = {"distribution": distribution, "module": module_name, "expected": expected, "installed": "", "importable": False, "status": "missing"}
        try:
            record["installed"] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            missing.append(distribution)
        try:
            importlib.import_module(module_name)
            record["importable"] = True
        except ImportError:
            pass
        if record["installed"] and record["installed"] != expected:
            mismatched.append(distribution)
        if record["installed"] == expected and record["importable"]:
            record["status"] = "ready"
        elif distribution not in missing:
            record["status"] = "mismatch"
        packages[distribution] = record
    # 2. 只输出协议 runtime 能力，不发起网络连接或启动服务。
    # 2.1 自定义探针可能只传入部分依赖；缺少 runtime 映射必须报告 False，不能抛出 KeyError。
    runtime = {name: packages.get(distribution, {"status": "missing"})["status"] == "ready" for name, distribution in {"http": "requests", "sse": "requests", "websocket": "websockets", "socketio": "python-socketio"}.items()}
    blocked = not python_ready or bool(missing) or bool(mismatched)
    # 3. doctor 结果固定输出总状态、解释器、依赖、协议能力和零项目依赖变更证明。
    return {
        # 3.1 总状态与解释器字段组。
        "status": "BLOCKED" if blocked else "PASS",
        "python": {"executable": sys.executable, "version": platform.python_version(), "required": ">=3.11", "ready": python_ready},
        # 3.2 依赖明细、缺失和版本不匹配字段组。
        "packages": packages,
        "missing_packages": missing,
        "mismatched_packages": mismatched,
        # 3.3 协议能力与安全执行边界字段组。
        "protocol_runtime": runtime,
        "network_access": "not_attempted",
        "project_dependency_mutation": False,
    }
