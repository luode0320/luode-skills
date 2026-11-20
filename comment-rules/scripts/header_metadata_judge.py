"""函数头元信息判据：按 comment-rules 校验 [参数]/[返回]/最近修改时间。

覆盖三种结论：
- PASS：已带元信息且顺序与格式成立。
- MISSING：无 docstring 或无元信息（存量可豁免，新增必须补齐）。
- INVALID：有元信息但顺序、格式或一句话说明不成立。
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from header_metadata_parser import FunctionHeader

TIMESTAMP_PATTERN = re.compile(r"最近修改时间[:：]\s*(\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2}:\d{2})?)\s*[,，]?\s*(\S.*)?$", re.M)
VAGUE_WORDS = ("优化一下", "调整逻辑", "修改代码", "更新代码", "修复问题")


@dataclass(frozen=True)
class HeaderVerdict:
    """单个函数头的校验结论。

    [参数] header: 被校验的函数头；status: PASS/INVALID/MISSING；reasons: 不通过原因。
    [返回] 无：本类为纯数据容器。
    最近修改时间：2026-10-31 22:40:00；新增校验结论结构。
    """

    header: FunctionHeader
    status: str
    reasons: tuple[str, ...]


def _order_valid(doc: str) -> bool:
    """判断三个元信息字段是否按约定顺序出现。

    [参数] doc: 函数头 docstring 原文。
    [返回] bool：顺序为 `[参数]` → `[返回]` → `最近修改时间` 时为 True。
    最近修改时间：2026-10-31 22:40:00；新增元信息顺序判据。
    """
    try:
        positions = [doc.index(label) for label in ("[参数]", "[返回]", "最近修改时间")]
    except ValueError:
        return False
    return positions == sorted(positions)


def _test_entry_exempted(header: FunctionHeader) -> bool:
    """判断测试入口函数是否适用免写 `[参数]`/`[返回]` 的例外。

    [参数] header: 被校验的函数头。
    [返回] bool：函数名以 test/Test/Benchmark 开头且只写了 `最近修改时间` 时为 True。
    最近修改时间：2026-10-31 22:40:00；新增测试入口豁免判据。
    """
    name = header.name
    if not name.startswith(("test", "Test", "Benchmark")):
        return False
    return "[参数]" not in header.doc and "[返回]" not in header.doc and "最近修改时间" in header.doc


def judge(header: FunctionHeader) -> HeaderVerdict:
    """判定单个函数头是否满足元信息契约。

    [参数] header: 被校验的函数头。
    [返回] HeaderVerdict：结论与不通过原因列表。
    最近修改时间：2026-10-31 22:40:00；新增元信息合规判定。
    """
    if not header.doc.strip():
        return HeaderVerdict(header, "MISSING", ("无 docstring",))
    if not header.has_metadata:
        return HeaderVerdict(header, "MISSING", ("docstring 未包含任何元信息字段",))

    reasons: list[str] = []
    if not _test_entry_exempted(header):
        for label in ("[参数]", "[返回]"):
            if label not in header.doc:
                reasons.append(f"缺少 {label}")
    if "最近修改时间" not in header.doc:
        reasons.append("缺少 最近修改时间")
    else:
        if not _order_valid(header.doc) and not _test_entry_exempted(header):
            reasons.append("元信息顺序不是 [参数] → [返回] → 最近修改时间")
        match = TIMESTAMP_PATTERN.search(header.doc)
        if not match:
            reasons.append("最近修改时间格式不是 yyyy-MM-dd[ HH:mm:ss]")
        else:
            note = (match.group(2) or "").strip()
            if not note:
                reasons.append("最近修改时间缺少一句话改动说明")
            elif any(word in note for word in VAGUE_WORDS):
                reasons.append("最近修改时间的说明过于空泛")

    return HeaderVerdict(header, "INVALID" if reasons else "PASS", tuple(reasons))
