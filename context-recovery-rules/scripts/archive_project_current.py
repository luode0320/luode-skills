#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] PROJECT_CURRENT.md 的自动归档：把已完结的日期小节迁进 PROJECT_HISTORY.md，
       只在新文件里留最近的几个交接点，避免当前状态文档无限膨胀。
[边界] 只搬「日期小节」（`## YYYY-MM-DD ...`）。非日期小节（如「最近 5 个同项目会话」）
       原地保留，不当历史处理。迁入内容逐字搬运，只把 `##` 降成 `###` 以嵌进档案区。
[触发] 不需要用户提醒：`--check` 在「日期小节超过 KEEP 且字节超过 SOFT_LIMIT」时退出 1，
       把「忘了归档」变成红灯。收口时跑一次 `--apply` 即可。
[用法] python scripts/archive_project_current.py            # 只打印计划
       python scripts/archive_project_current.py --apply    # 执行归档
       python scripts/archive_project_current.py --check    # 闸门：超限即退出 1
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "PROJECT_CURRENT.md"
HISTORY = ROOT / "PROJECT_HISTORY.md"

KEEP_SECTIONS = 3          # 当前文档保留的最新日期小节数
SOFT_LIMIT = 40000         # 超过此字节数即要求归档
HARD_LIMIT = 51200         # 规则硬上限
ARCHIVE_CAP = 20           # 档案区最多保留的迁入小节数

ARCHIVE_HEADING = "## 交接档案（自 PROJECT_CURRENT 迁入）"
ARCHIVE_NOTE = (
    "> 由 `context-recovery-rules/scripts/archive_project_current.py` 自动迁入，"
    "新条目置顶、只保留最近 "
    f"{ARCHIVE_CAP} 条。当前交接点仍以 `PROJECT_CURRENT.md` 为准。"
)

DATED = re.compile(r"^## (\d{4}-\d{2}-\d{2})\b")


def read(path: Path) -> str:
    with path.open(encoding="utf-8", newline="") as fh:
        return fh.read()


def write(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def split_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """[参数] 全文 [返回] (首个小节之前的导语, [(标题行, 正文)])。"""
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if not starts:
        return text, []
    preamble = "\n".join(lines[: starts[0]])
    sections: list[tuple[str, str]] = []
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        block = lines[start:end]
        sections.append((block[0], "\n".join(block[1:])))
    return preamble, sections


def plan() -> tuple[str, list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    """[返回] (导语, 留在 CURRENT 的日期小节, 非日期小节, 待迁出的日期小节)。"""
    preamble, sections = split_sections(read(CURRENT))
    dated = [(h, b) for h, b in sections if DATED.match(h)]
    others = [(h, b) for h, b in sections if not DATED.match(h)]
    return preamble, dated[:KEEP_SECTIONS], others, dated[KEEP_SECTIONS:]


def rebuild_current(preamble: str, sections: list[tuple[str, str]]) -> str:
    body = "\n".join(f"{h}\n{b}".rstrip("\n") for h, b in sections)
    return (preamble.rstrip("\n") + "\n\n" + body).rstrip("\n") + "\n"


def archive_into_history(moved: list[tuple[str, str]]) -> tuple[str, int]:
    """[参数] 待迁入小节（新→旧）[返回] (新的 HISTORY 全文, 丢弃的旧档案条数)。"""
    text = read(HISTORY)
    if ARCHIVE_HEADING in text:
        head, rest = text.split(ARCHIVE_HEADING, 1)
        rest_lines = rest.split("\n")
        # 档案区到文件末尾；已有条目按 `### ` 切
        existing: list[str] = []
        buf: list[str] = []
        for line in rest_lines:
            if line.startswith("### ") and buf:
                existing.append("\n".join(buf).rstrip("\n"))
                buf = [line]
            elif line.startswith("### "):
                buf = [line]
            elif buf:
                buf.append(line)
        if buf:
            existing.append("\n".join(buf).rstrip("\n"))
        # 去掉尾随空行产生的空条目
        existing = [e for e in existing if e.strip()]
    else:
        head = text.rstrip("\n") + "\n\n"
        existing = []

    fresh = [f"### {h[3:]}\n{b}".rstrip("\n") for h, b in moved]
    merged = fresh + existing
    dropped = max(0, len(merged) - ARCHIVE_CAP)
    merged = merged[:ARCHIVE_CAP]

    block = [ARCHIVE_HEADING, "", ARCHIVE_NOTE, ""]
    for item in merged:
        block.append(item)
        block.append("")
    return head.rstrip("\n") + "\n\n" + "\n".join(block).rstrip("\n") + "\n", dropped


def main(argv: list[str]) -> int:
    if not CURRENT.exists():
        print("ARCHIVE: SKIP（无 PROJECT_CURRENT.md）")
        return 0

    size = CURRENT.stat().st_size
    preamble, keep_dated, others, move = plan()
    dated_total = len(keep_dated) + len(move)

    if "--check" in argv:
        over_hard = size > HARD_LIMIT
        overdue = dated_total > KEEP_SECTIONS and size > SOFT_LIMIT
        if over_hard or overdue:
            print(
                f"ARCHIVE: FAIL（PROJECT_CURRENT.md {size} 字节 / {dated_total} 个日期小节，"
                f"阈值 {SOFT_LIMIT}/{KEEP_SECTIONS}，上限 {HARD_LIMIT}；"
                f"应归档 {len(move)} 个：python scripts/archive_project_current.py --apply）"
            )
            return 1
        print(f"ARCHIVE: PASS（{size} 字节 / {dated_total} 个日期小节，未超阈值）")
        return 0

    if not move:
        print(f"ARCHIVE: SKIP（{size} 字节 / {dated_total} 个日期小节，无需归档）")
        return 0

    if "--apply" not in argv:
        print(f"ARCHIVE: 计划迁出 {len(move)} 个日期小节（{size} 字节 → 约 {len(rebuild_current(preamble, keep_dated + others).encode('utf-8'))} 字节）")
        for heading, _body in move:
            print("  - " + heading[3:])
        print("加 --apply 执行")
        return 0

    history_text, dropped = archive_into_history(move)
    write(HISTORY, history_text)
    write(CURRENT, rebuild_current(preamble, keep_dated + others))
    new_size = CURRENT.stat().st_size
    print(
        f"ARCHIVE_APPLIED: 迁出 {len(move)} 个日期小节；"
        f"PROJECT_CURRENT {size} → {new_size} 字节；"
        f"PROJECT_HISTORY 档案区保留 {ARCHIVE_CAP} 条"
        + (f"，丢弃最旧 {dropped} 条" if dropped else "")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
