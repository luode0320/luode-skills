"""测试执行前的极端破坏性操作阻断。"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    rule: str = ""
    reason: str = ""


class SafetyViolation(RuntimeError):
    """请求命中测试引擎的不可执行安全规则。"""

    def __init__(self, decision: SafetyDecision):
        self.decision = decision
        super().__init__(decision.reason)


_RULES: tuple[tuple[str, re.Pattern[str], str], ...] = (
    ("sql.drop", re.compile(r"\bDROP\s+(?:DATABASE|SCHEMA|TABLE|INDEX|VIEW|TYPE)\b", re.I), "禁止删除数据库结构"),
    ("sql.truncate", re.compile(r"\bTRUNCATE\s+(?:TABLE|DATABASE|SCHEMA)\b", re.I), "禁止清空数据库结构或数据"),
    ("sql.alter_drop", re.compile(r"\bALTER\s+(?:TABLE|DATABASE|SCHEMA)\b[^;]*\bDROP\b", re.I), "禁止通过 ALTER 删除结构"),
    ("infra.destroy", re.compile(r"\b(?:terraform\s+destroy|kubectl\s+delete\s+namespace|docker\s+system\s+prune)\b", re.I), "禁止摧毁基础设施"),
    ("filesystem.root_delete", re.compile(r"(?:rm\s+-[rf]{1,2}\s+/(?:\s|$)|(?:rm|del|Remove-Item)\s+(?:-[^\s]+\s+)*(?:[^\r\n]*[/\\])?(?:src|source|project|\.git)(?:[/\\\s]|$))", re.I), "禁止删除根目录或项目源码"),
    ("filesystem.python_rmtree", re.compile(r"\b(?:shutil\.rmtree|os\.system\s*\(\s*['\"]rm\s+-rf)", re.I), "禁止脚本递归删除文件"),
    ("filesystem.git_clean", re.compile(r"\bgit\s+clean\s+-[^\r\n]*f[^\r\n]*d", re.I), "禁止清理项目源码文件"),
)


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, Mapping):
        result: list[str] = []
        for key, child in value.items():
            result.extend(_strings(key))
            result.extend(_strings(child))
        return result
    if isinstance(value, (list, tuple, set)):
        result = []
        for child in value:
            result.extend(_strings(child))
        return result
    return []


def check_operation(operation: Any, *, environment: str | None = None) -> SafetyDecision:
    """返回安全决策；普通业务 DELETE/DML 不会因方法名被误阻断。"""

    if environment and environment.lower() not in {"local", "local-dev", "development"}:
        return SafetyDecision(False, "environment.non_local", "测试执行仅允许 local 环境配置")
    for text in _strings(operation):
        for rule, pattern, reason in _RULES:
            if pattern.search(text):
                return SafetyDecision(False, rule, reason)
    return SafetyDecision(True)


def assert_safe(operation: Any, *, environment: str | None = None) -> None:
    decision = check_operation(operation, environment=environment)
    if not decision.allowed:
        raise SafetyViolation(decision)
