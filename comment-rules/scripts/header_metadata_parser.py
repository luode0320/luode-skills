"""函数头元信息解析：定位每个函数、方法及其 docstring。

只做解析与字段提取，不做合规判定；判定在 judge 侧。
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

METADATA_LABELS = ("[参数]", "[返回]", "最近修改时间")


@dataclass(frozen=True)
class FunctionHeader:
    """单个函数的头部信息快照。

    [参数] path: 相对仓库根的 POSIX 路径；name: 函数名；line: 定义所在行号；doc: docstring 原文。
    [返回] 无：本类为纯数据容器。
    最近修改时间：2026-10-31 22:40:00；新增函数头元信息解析，供校验脚本复用。
    """

    path: str
    name: str
    line: int
    doc: str

    @property
    def has_metadata(self) -> bool:
        """判断 docstring 是否包含任一元信息字段。

        [参数] 无。
        [返回] bool：命中任一 `[参数]`/`[返回]`/`最近修改时间` 时为 True。
        最近修改时间：2026-10-31 22:40:00；新增元信息存在性判断。
        """
        return any(label in self.doc for label in METADATA_LABELS)


def _docstring_of(node: ast.AST) -> str:
    """提取函数节点的 docstring 文本。

    [参数] node: ast 函数定义节点。
    [返回] str：docstring 原文；无 docstring 时返回空串。
    最近修改时间：2026-10-31 22:40:00；新增 docstring 提取，兼容非字符串首语句。
    """
    body = getattr(node, "body", None) or []
    if not body:
        return ""
    first = body[0]
    if not isinstance(first, ast.Expr):
        return ""
    value = getattr(first, "value", None)
    if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
        return ""
    return value.value


def collect_headers(path: Path, root: Path) -> list[FunctionHeader]:
    """收集文件中全部函数与方法的头部信息。

    [参数] path: 目标 Python 文件；root: 仓库根，用于生成相对路径。
    [返回] list[FunctionHeader]：解析结果；语法错误时返回空列表。
    最近修改时间：2026-10-31 22:40:00；新增函数头批量收集。
    """
    try:
        source = path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return []
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.as_posix()
    headers: list[FunctionHeader] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            headers.append(FunctionHeader(rel, node.name, node.lineno, _docstring_of(node)))
    return headers
