"""只读巡检固定 Obsidian vault，输出待处置的冲突、过期与孤儿笔记候选。

本脚本只调用 bridge 的只读命令，不做任何写入：哪篇笔记真该废弃属于语义裁决，
必须由 agent 读过内容后按 conflict-staleness.md 的分级处置执行。
"""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


BRIDGE = Path(__file__).with_name("obsidian_cli_bridge.py")
DEFAULT_FOLDER = "知识库/20-Knowledge"
# 标题相似度达到该阈值即视为同主题候选；只作线索，不作结论。
TITLE_SIMILARITY_THRESHOLD = 0.72
ACTIVE_STATUS = "active"
SUPERSEDED_STATUS = "superseded"
# 完全没有 frontmatter 的笔记会返回这句提示，它既不是 JSON 也不以 Error: 开头。
NO_FRONTMATTER_MARKER = "No frontmatter found."
# 执行案例笔记走追加式状态事件，不参与分级处置，巡检时跳过。
EXECUTION_CASE_PREFIX = "知识库/20-Knowledge/execution-failure-cases/"


@dataclass
class NoteFacts:
    """一篇笔记在巡检期间收集到的只读事实。"""

    path: str
    title: str = ""
    status: str = ""
    topics: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    superseded_by: tuple[str, ...] = ()
    is_orphan: bool = False
    read_error: str = ""
    aliases: tuple[str, ...] = field(default=())


def run_bridge(command: str, *arguments: str) -> dict[str, Any]:
    """调用 bridge 的只读命令并解析结构化响应。

    [参数] command: bridge 只读命令名；arguments: 该命令的命令行参数。
    [返回] dict[str, Any]: bridge 的 JSON 响应；调用失败时返回带 ok=False 的对象。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", str(BRIDGE), command, *arguments, "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "code": "BRIDGE_OUTPUT_UNPARSABLE", "message": completed.stderr.strip()[:200]}


def bridge_output(response: dict[str, Any]) -> str:
    """从 bridge 响应中取出 CLI 原始输出文本。

    [参数] response: bridge 的 JSON 响应。
    [返回] str: CLI 输出文本；响应失败时为空串。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    if not response.get("ok"):
        return ""
    return str((response.get("data") or {}).get("output", ""))


def is_cli_error(text: str) -> bool:
    """判断 CLI 输出是否为退出码为零的错误载荷。

    [参数] text: CLI 输出文本。
    [返回] bool: 输出以 Error: 开头时为 True。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    return text.lstrip().startswith("Error:")


def as_tuple(value: Any) -> tuple[str, ...]:
    """把 frontmatter 中的标量或列表统一成字符串元组。

    [参数] value: frontmatter 字段原始值。
    [返回] tuple[str, ...]: 规范化后的字符串元组。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    if value is None:
        return ()
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if str(item).strip())
    text = str(value).strip()
    return (text,) if text else ()


def list_note_paths(folder: str | None) -> list[str]:
    """枚举目标目录下的 Markdown 笔记路径。

    [参数] folder: vault 相对目录；None 表示全库枚举。
    [返回] list[str]: 已排除执行案例目录的笔记路径列表。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    arguments = ("--folder", folder) if folder else ()
    output = bridge_output(run_bridge("files", *arguments))
    paths = [line.strip() for line in output.splitlines() if line.strip().endswith(".md")]
    return [path for path in paths if not path.startswith(EXECUTION_CASE_PREFIX)]


def collect_note_facts(path: str) -> NoteFacts:
    """读取单篇笔记的头部字段与引用数。

    [参数] path: vault 相对笔记路径。
    [返回] NoteFacts: 该笔记的只读事实；头部不可解析时记录读取错误。
    最近修改时间: 2026-08-05 17:45:00 改由全库 orphans 推导零引用，去掉逐篇 backlinks 调用。
    """
    facts = NoteFacts(path=path)
    properties_text = bridge_output(run_bridge("properties", "--path", path))
    if not properties_text or is_cli_error(properties_text):
        facts.read_error = properties_text.strip()[:120] or "properties 调用失败"
    elif properties_text.strip() == NO_FRONTMATTER_MARKER:
        # 没有 frontmatter 的笔记拿不到 status，无法参与状态治理，需要先补齐头部。
        facts.read_error = "笔记没有 frontmatter，无法参与状态治理，需先补齐头部字段"
    else:
        try:
            frontmatter = json.loads(properties_text)
        except json.JSONDecodeError:
            facts.read_error = "frontmatter 不是合法 JSON"
        else:
            facts.title = str(frontmatter.get("title") or Path(path).stem)
            facts.status = str(frontmatter.get("status") or "")
            facts.topics = as_tuple(frontmatter.get("topics"))
            facts.tags = as_tuple(frontmatter.get("tags"))
            facts.aliases = as_tuple(frontmatter.get("aliases"))
            facts.superseded_by = as_tuple(frontmatter.get("superseded_by"))
    return facts


def title_similarity(left: str, right: str) -> float:
    """计算两个标题的相似度，用于同主题候选分组。

    [参数] left: 第一个标题；right: 第二个标题。
    [返回] float: 0 到 1 之间的相似度。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    return difflib.SequenceMatcher(None, left, right).ratio()


def group_conflict_candidates(notes: Iterable[NoteFacts]) -> list[dict[str, Any]]:
    """按主题标签交集与标题相似度分出同主题候选冲突组。

    [参数] notes: 已收集事实的笔记集合。
    [返回] list[dict[str, Any]]: 候选冲突组列表，每组至少两篇当前有效笔记。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    # 1. 只有仍被当作当前事实的笔记才可能造成检索歧义。
    active = [note for note in notes if note.status == ACTIVE_STATUS]
    grouped: list[dict[str, Any]] = []
    consumed: set[str] = set()
    for index, note in enumerate(active):
        if note.path in consumed:
            continue
        members = [note]
        for other in active[index + 1 :]:
            if other.path in consumed:
                continue
            shared = (set(note.topics) | set(note.tags)) & (set(other.topics) | set(other.tags))
            similarity = title_similarity(note.title, other.title)
            if shared or similarity >= TITLE_SIMILARITY_THRESHOLD:
                members.append(other)
        if len(members) < 2:
            continue
        for member in members:
            consumed.add(member.path)
        grouped.append(
            {
                "reason": "同主题或标题高度相似且均为当前有效，需判定是补充、矛盾还是取代",
                "members": [
                    {"path": member.path, "title": member.title, "status": member.status, "is_orphan": member.is_orphan}
                    for member in members
                ],
            }
        )
    return grouped


def build_report(notes: list[NoteFacts], orphan_paths: list[str]) -> dict[str, Any]:
    """汇总四类待处置候选。

    [参数] notes: 已收集事实的笔记集合；orphan_paths: 全库孤儿笔记路径。
    [返回] dict[str, Any]: 结构化巡检报告。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    inactive = [
        {"path": note.path, "title": note.title, "status": note.status, "is_orphan": note.is_orphan}
        for note in notes
        if note.status and note.status != ACTIVE_STATUS
    ]
    dangling = [
        {"path": note.path, "title": note.title, "status": note.status, "is_orphan": note.is_orphan}
        for note in notes
        if note.status == SUPERSEDED_STATUS and not note.superseded_by
    ]
    unreadable = [{"path": note.path, "error": note.read_error} for note in notes if note.read_error]
    scanned = {note.path for note in notes}
    return {
        "schema_version": 1,
        "scanned_notes": len(notes),
        "candidates": {
            "conflict_groups": group_conflict_candidates(notes),
            "non_active_status": inactive,
            "orphans": [
                {"path": path, "in_scanned_scope": path in scanned}
                for path in orphan_paths
                if not path.startswith(EXECUTION_CASE_PREFIX)
            ],
            "superseded_without_pointer": dangling,
        },
        "unreadable_notes": unreadable,
        "disposition_hint": "候选只是线索；必须读过笔记内容后按 conflict-staleness.md 的分级处置判定并执行。",
    }


def parse_args() -> argparse.Namespace:
    """解析巡检入口的命令行参数。

    [参数] 无。
    [返回] argparse.Namespace: 解析后的参数。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", default=DEFAULT_FOLDER, help="限定巡检目录，默认只扫描长期知识目录")
    parser.add_argument("--all", action="store_true", help="巡检整个 vault 而不限定目录")
    parser.add_argument("--json", action="store_true", help="输出结构化 JSON 报告")
    return parser.parse_args()


def main() -> int:
    """执行只读巡检并输出候选报告。

    [参数] 无。
    [返回] int: 巡检完成为 0；bridge 自检失败为 4。
    最近修改时间: 2026-08-05 17:30:00 新增只读巡检入口。
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parse_args()
    # 1. 先自检，避免在 vault 不可达时输出空报告被误读成"库很干净"。
    doctor = run_bridge("doctor")
    if not doctor.get("ok"):
        print(json.dumps({"ok": False, "code": doctor.get("code", "DOCTOR_FAILED")}, ensure_ascii=False))
        return 4
    folder = None if args.all else args.folder
    # 2. 零引用只用全库 orphans 一个来源判断，避免逐篇 backlinks 重复同一事实且拖慢巡检。
    orphan_paths = [line.strip() for line in bridge_output(run_bridge("orphans")).splitlines() if line.strip().endswith(".md")]
    orphan_set = set(orphan_paths)
    notes = []
    for path in list_note_paths(folder):
        facts = collect_note_facts(path)
        facts.is_orphan = path in orphan_set
        notes.append(facts)
    report = build_report(notes, orphan_paths)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    candidates = report["candidates"]
    print(f"已巡检笔记：{report['scanned_notes']} 篇")
    print(f"同主题候选冲突组：{len(candidates['conflict_groups'])} 组")
    print(f"状态非当前有效：{len(candidates['non_active_status'])} 篇")
    print(f"孤儿笔记：{len(candidates['orphans'])} 篇")
    print(f"标了已取代但缺接替者：{len(candidates['superseded_without_pointer'])} 篇")
    print(f"头部不可读：{len(report['unreadable_notes'])} 篇")
    print(report["disposition_hint"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
