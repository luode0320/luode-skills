#!/usr/bin/env python3
"""只读巡检知识库目录，输出待处置的冲突、过期与孤儿笔记候选。"""

from __future__ import annotations
import argparse
import ast
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

KB_ROOT = Path("D:/谷歌云盘/知识库")
# 主题落点根目录。巡检默认扫全库，本常量只用于主题推导，不再作为默认扫描范围。
KNOWLEDGE_FOLDER = "20-Knowledge"
TITLE_SIMILARITY_THRESHOLD = 0.72
ACTIVE_STATUS = "active"
EXECUTION_CASE_PREFIX = "20-Knowledge/execution-failure-cases/"
# 归组时要求的最小共享标签数。原先共享 1 个标签即归组，实测 30 对候选里几乎全是误报
# （把「Go 编码规范」和「ellipal_stat cron 任务」归为一组），因此提高到 2 并叠加同主题条件。
MIN_SHARED_TAGS = 2
# 导航笔记类型：同家族分册天生同主题同标签，参与冲突归组只会制造误报。
MOC_TYPE = "moc"
# 落点规则声明的固定主题。定义放在本模块，供索引脚本单向复用，避免两处各推一套主题口径。
DECLARED_THEMES = (
    "项目",
    "代码规则",
    "工程实践",
    "研发流程",
    "AI协作",
    "数据清洗",
    "开发环境",
)
# 契约固定落点：被其它 skill 硬编码引用，不参与主题中文化，也不算违规目录。
CONTRACT_DIRS = (
    "execution-failure-cases",
    "project-rules",
    "code-style",
)


@dataclass
class NoteFacts:
    path: str
    title: str = ""
    status: str = ""
    note_type: str = ""
    topics: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    superseded_by: tuple[str, ...] = ()
    related: tuple[str, ...] = ()
    is_orphan: bool = False
    read_error: str = ""
    aliases: tuple[str, ...] = field(default=())


def parse_frontmatter(text: str) -> dict[str, Any]:
    """解析笔记头部的 YAML frontmatter 标量字段。

    [参数] text: 笔记全文。
    [返回] dict[str, Any]: 标量字段字典；无头部或格式不合法时返回空字典。
    最近修改时间: 2026-08-12 补齐函数头注释。
    """
    result = {}
    text = text.lstrip("﻿")
    if not text.startswith("---"):
        return result
    parts = text.split("---", 2)
    if len(parts) < 3:
        return result
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if value == "" or value.startswith("["):
            continue
        result[key] = value
    return result


def parse_list_field(text: str, field: str) -> tuple[str, ...]:
    """读取头部的列表字段，兼容行内数组、块状条目与单值标量三种写法。

    [参数] text: 笔记全文；field: 目标字段名。
    [返回] tuple[str, ...]: 归一后的字符串元组；字段缺失时返回空元组。
    最近修改时间: 2026-08-12 行内数组补无引号降级解析，修复别名丢失。
    """
    text = text.lstrip("﻿")
    if not text.startswith("---"):
        return ()
    parts = text.split("---", 2)
    if len(parts) < 3:
        return ()
    in_field = False
    items = []
    for line in parts[1].strip().splitlines():
        stripped = line.strip()
        if stripped.startswith(field + ":"):
            value = stripped[len(field) + 1 :].strip()
            if value.startswith("["):
                try:
                    parsed = ast.literal_eval(value)
                    if isinstance(parsed, (list, tuple)):
                        return tuple(str(i) for i in parsed)
                except (ValueError, SyntaxError):
                    # YAML 允许 [a, b] 这种无引号行内数组，但它不是合法 Python 字面量。
                    # 不降级解析会让这类别名与标签整段丢失，直接影响检索召回。
                    inner = value.strip()[1:].rsplit("]", 1)[0]
                    fallback = [item.strip().strip("'\"") for item in inner.split(",")]
                    return tuple(item for item in fallback if item)
            elif value:
                return (value,)
            in_field = True
        elif in_field and stripped.startswith("- "):
            items.append(stripped[2:].strip())
        elif in_field and not stripped.startswith("- "):
            break
    return tuple(items)


def normalize_wikilink(raw: str) -> str:
    """把 wikilink 内容归一成不含显示名与锚点的目标本体。

    双链既可能写 `[[路径|显示名]]`，也可能写 `[[标题#小节]]`。孤儿检测、接替关系校验与
    已裁决候选豁免三个消费方必须用同一套归一口径，否则同一条链接会被判出不同目标。

    frontmatter 的块状条目常写成 `- "[[目标]]"`，YAML 引号必须先剥掉再剥方括号；
    实测漏剥引号会让三组已双向关联的笔记归一失败，继续被误报成未裁决候选。

    [参数] raw: `[[` 与 `]]` 之间的原始内容，或关联/接替字段里的原始取值。
    [返回] str: 去掉引号、方括号、显示名与锚点后的目标本体；空目标返回空串。
    最近修改时间: 2026-08-12 补剥 YAML 引号，修复带引号 wikilink 归一失败。
    """
    return raw.strip().strip("\"'").strip("[]").split("|", 1)[0].split("#", 1)[0].strip()


def collect_note_facts(filepath: Path) -> NoteFacts:
    """读取单篇笔记，抽取巡检所需的最小事实集。

    [参数] filepath: 笔记的绝对路径。
    [返回] NoteFacts: 含裸相对路径、标题、状态与接替关系的事实对象；读取失败时记录读取错误。
    最近修改时间: 2026-08-12 新增笔记类型字段，供导航笔记退出冲突归组使用。
    """
    rel = filepath.relative_to(KB_ROOT).as_posix()
    facts = NoteFacts(path=rel)
    try:
        # 用 utf-8-sig 读：Windows 工具可能写入 BOM，BOM 会让 frontmatter 判定失败、字段全丢。
        text = filepath.read_text(encoding="utf-8-sig")
    except Exception as e:
        facts.read_error = str(e)[:120]
        return facts
    fm = parse_frontmatter(text)
    facts.title = fm.get("title", filepath.stem)
    facts.status = fm.get("status", "")
    facts.note_type = fm.get("type", "")
    facts.topics = parse_list_field(text, "topics")
    facts.tags = parse_list_field(text, "tags")
    facts.aliases = parse_list_field(text, "aliases")
    facts.superseded_by = parse_list_field(text, "superseded_by")
    facts.related = parse_list_field(text, "related")
    if not text.startswith("---"):
        facts.read_error = "no frontmatter"
    return facts


def title_similarity(left: str, right: str) -> float:
    """计算两个标题的相似度，用于识别疑似重复主题。

    [参数] left: 标题一；right: 标题二。
    [返回] float: 0 到 1 之间的相似度比值。
    最近修改时间: 2026-08-12 补齐函数头注释。
    """
    return difflib.SequenceMatcher(None, left, right).ratio()


def note_theme(rel_path: str) -> str:
    """从笔记的裸相对路径推导归一化主题。

    本函数是主题口径的唯一实现，索引脚本单向复用它，避免巡检与索引各推一套导致分叉。

    [参数] rel_path: 相对知识库根的裸相对路径。
    [返回] str: 主题名；根入口返回 root，其它顶层目录返回自身，未登记主题返回 unknown。
    最近修改时间: 2026-08-12 从索引脚本下移，供两处共用。
    """
    parts = rel_path.split("/")
    if len(parts) == 1:
        # 知识库根下的入口文件（如 INDEX.md），不属于任何主题。
        return "root"
    if parts[0] != KNOWLEDGE_FOLDER:
        # 30-MOCs、50-Sources、90-Archive 等按顶层目录本身作为主题。
        return parts[0]
    if len(parts) < 3:
        # 直接落在 20-Knowledge 根下的散落笔记，落点规则不允许，标出来便于巡检。
        return "unknown"
    second = parts[1]
    if second in DECLARED_THEMES or second in CONTRACT_DIRS:
        return second
    return "unknown"


def links_to(src: NoteFacts, dst: NoteFacts) -> bool:
    """判断源笔记的 related 是否指向目标笔记。

    [参数] src: 源笔记事实；dst: 目标笔记事实。
    [返回] bool: 指向目标笔记时为真。
    最近修改时间: 2026-08-12 新增，供已裁决候选退出归组使用。
    """
    targets = {normalize_wikilink(item) for item in src.related}
    # 双链可能写完整路径、无后缀路径、标题或文件名，四种形态都要能命中同一篇笔记。
    aliases = {dst.path, dst.path.removesuffix(".md"), dst.title, Path(dst.path).stem}
    return bool(targets & aliases)


def group_conflict_candidates(notes: Iterable[NoteFacts]) -> list[dict[str, Any]]:
    """把同主题且标签高度重叠、或标题高度相似的当前有效笔记归为冲突候选组。

    归组条件是「(同主题 且 共享标签数 >= MIN_SHARED_TAGS) 或 标题相似度 >= 阈值」。
    标题相似度单独成条，作为跨主题例外通道：标题高度相似基本就是同一篇的重复写入，
    即使被分到不同主题也要报出来。

    导航笔记（type: moc）不参与归组：同一家族的分册 MOC 天生同主题同标签，实测
    30-MOCs/blog-data/ 下 10 篇分册会被归成一组，把真候选淹没。MOC 仍参与孤儿检测。

    已互相写入 `related` 的两篇也不再归组：双向关联是「判为补充」留下的裁决痕迹，
    没有这条豁免，判过补充的组每轮都会重新报出来，使用者很快就会学会忽略这份报告。
    真正重复的内容应走取代并写接替字段，不会停在互相关联的状态。

    [参数] notes: 参与判定的笔记事实集合。
    [返回] list[dict[str, Any]]: 候选组列表；只输出候选，不做任何处置。
    最近修改时间: 2026-08-12 已双向关联的笔记退出归组，避免判过补充的组反复重报。
    """
    active = [n for n in notes if n.status == ACTIVE_STATUS and n.note_type != MOC_TYPE]
    grouped: list[dict[str, Any]] = []
    consumed: set[str] = set()
    for index, note in enumerate(active):
        if note.path in consumed:
            continue
        members = [note]
        for other in active[index + 1 :]:
            if other.path in consumed:
                continue
            # 互相写入 related 即视为已裁决为补充，不再作为候选重复报出。
            if links_to(note, other) and links_to(other, note):
                continue
            shared = (set(note.topics) | set(note.tags)) & (set(other.topics) | set(other.tags))
            similarity = title_similarity(note.title, other.title)
            same_theme = note_theme(note.path) == note_theme(other.path)
            if (same_theme and len(shared) >= MIN_SHARED_TAGS) or similarity >= TITLE_SIMILARITY_THRESHOLD:
                members.append(other)
        if len(members) < 2:
            continue
        for member in members:
            consumed.add(member.path)
        grouped.append(
            {
                "reason": "同主题且标签高度重叠，或标题高度相似，且均为当前有效，需判定是补充、矛盾未裁决还是取代",
                "members": [
                    {"path": m.path, "title": m.title, "status": m.status, "is_orphan": m.is_orphan}
                    for m in members
                ],
            }
        )
    return grouped


def find_orphans(all_notes: list[NoteFacts]) -> list[str]:
    """找出全库范围内没有任何笔记链接指向的孤儿笔记。

    [参数] all_notes: 参与判定的笔记事实列表。
    [返回] list[str]: 无入链笔记的裸相对路径列表。
    最近修改时间: 2026-08-12 双链归一改调用共用函数，与接替校验统一口径。
    """
    # 1. 扫描全库每篇笔记的双链，收集所有被指向的目标。
    #    双链既可能写完整相对路径，也可能只写标题或文件名，因此两种形态都要归一到笔记路径。
    linked: set[str] = set()
    for filepath in sorted(KB_ROOT.rglob("*.md")):
        try:
            text = filepath.read_text(encoding="utf-8-sig")
        except OSError:
            continue
        for match in re.finditer(r"\[\[([^\]]+)\]\]", text):
            target = normalize_wikilink(match.group(1))
            if not target:
                continue
            for note in all_notes:
                if target in (note.path, note.path.removesuffix(".md"), note.title, Path(note.path).stem):
                    linked.add(note.path)
    # 2. 入口笔记本身不需要入链，否则 INDEX 永远会被报成孤儿。
    entries = {"INDEX.md"}
    return [n.path for n in all_notes if n.path not in linked and n.path not in entries]


def build_report(notes: list[NoteFacts], orphan_paths: list[str]) -> dict[str, Any]:
    """汇总四类候选与不可读笔记，输出只读巡检报告。

    [参数] notes: 全部笔记事实；orphan_paths: 已判定的孤儿笔记路径。
    [返回] dict[str, Any]: 结构化报告；执行案例目录不参与孤儿候选。
    最近修改时间: 2026-08-12 补齐函数头注释。
    """
    inactive = [
        {"path": n.path, "title": n.title, "status": n.status, "is_orphan": n.is_orphan}
        for n in notes
        if n.status and n.status != ACTIVE_STATUS
    ]
    dangling = [
        {"path": n.path, "title": n.title, "status": n.status, "is_orphan": n.is_orphan}
        for n in notes
        if n.status == "superseded" and not n.superseded_by
    ]
    unreadable = [{"path": n.path, "error": n.read_error} for n in notes if n.read_error]
    scanned = {n.path for n in notes}
    return {
        "schema_version": 1,
        "scanned_notes": len(notes),
        "candidates": {
            "conflict_groups": group_conflict_candidates(notes),
            "non_active_status": inactive,
            "orphans": [
                {"path": p, "in_scanned_scope": p in scanned}
                for p in orphan_paths
                if not p.startswith(EXECUTION_CASE_PREFIX)
            ],
            "superseded_without_pointer": dangling,
        },
        "unreadable_notes": unreadable,
        "disposition_hint": "仅为候选清单；处置前必须先读笔记正文，并按分级处置规则决定标记取代、归档还是删除",
    }


def parse_args() -> argparse.Namespace:
    """解析巡检命令行参数。

    [参数] 无。
    [返回] argparse.Namespace: 含扫描范围与输出格式的参数对象。
    最近修改时间: 2026-08-12 默认扫描范围由单个子目录改为全库，避免局部结论被当成全库结论。
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", default="", help="限定扫描的子目录；默认扫全库")
    parser.add_argument("--all", action="store_true", help="显式声明扫全库；默认已是全库，保留以兼容既有调用")
    parser.add_argument("--json", action="store_true", help="以 JSON 结构化输出，便于机器消费")
    return parser.parse_args()


def main() -> int:
    """执行只读巡检并输出候选报告。

    [参数] 无。
    [返回] int: 0 表示成功，4 表示知识库根目录不可达。
    最近修改时间: 2026-08-12 补齐函数头注释并改中文输出。
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parse_args()
    folder = args.folder if not args.all else None
    root = KB_ROOT / folder if folder else KB_ROOT
    if not root.exists():
        print(json.dumps({"ok": False, "code": "KB_ROOT_NOT_FOUND"}, ensure_ascii=False))
        return 4
    notes = []
    for fp in sorted(root.rglob("*.md")):
        if fp.name.startswith("."):
            continue
        rel = fp.relative_to(KB_ROOT).as_posix()
        if rel.startswith(EXECUTION_CASE_PREFIX):
            continue
        facts = collect_note_facts(fp)
        notes.append(facts)
    orphan_paths = find_orphans(notes)
    for n in notes:
        n.is_orphan = n.path in orphan_paths
    report = build_report(notes, orphan_paths)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    candidates = report["candidates"]
    print(f"扫描笔记数: {report['scanned_notes']}")
    print(f"冲突候选组: {len(candidates['conflict_groups'])}")
    print(f"非当前有效状态: {len(candidates['non_active_status'])}")
    print(f"孤儿笔记: {len(candidates['orphans'])}")
    print(f"标了已取代但缺接替者: {len(candidates['superseded_without_pointer'])}")
    print(f"不可读笔记: {len(report['unreadable_notes'])}")
    print(report["disposition_hint"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
