#!/usr/bin/env python3
"""构建并查询知识库机器索引，让检索第一跳不再依赖手写导航或猜关键词。

手写 INDEX.md 只覆盖约三分之一笔记，30-MOCs 也未覆盖活跃主题，导致检索实际退化成
靠猜关键词全文扫描。本脚本把全库 frontmatter 抽成 `_index.json`，并提供按标题、别名、
标签、topics、主题目录、路径六类字段的查询入口。

笔记解析直接复用同目录 `audit_vault_knowledge.py` 的实现，不重复一份 frontmatter 解析。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


AUDIT_PATH = Path(__file__).with_name("audit_vault_knowledge.py")
INDEX_NAME = "_index.json"
SCHEMA_VERSION = 1
# note-schema.md 要求新笔记必须含完整 frontmatter，但该要求原先无机器校验，实测填充率只有 70%~82%。
REQUIRED_FIELDS = ("id", "type", "title", "status", "created", "updated")
# note-schema.md 声明的状态枚举。集中定义供 check 与巡检共用，避免两处各维护一套。
DECLARED_STATUS = (
    "active",
    "superseded",
    "archived",
    "conflicted",
    "stale",
    "deprecated",
    "retired",
)
# 执行案例笔记的追加式状态，由 execution-case-notes.md 的状态机定义。
CASE_STATUS = ("candidate", "rejected")
# 只读历史归档：不参与 frontmatter 合规校验，避免为历史测试残留补字段。
CHECK_EXEMPT_PREFIXES = ("90-Archive/",)


def load_audit() -> Any:
    """按文件路径加载巡检模块，复用其 frontmatter 解析实现。

    [参数] 无。
    [返回] Any: 已加载的巡检模块对象。
    最近修改时间: 2026-08-12 新增机器索引脚本。
    """
    name = "audit_vault_knowledge_for_index"
    spec = importlib.util.spec_from_file_location(name, AUDIT_PATH)
    module = importlib.util.module_from_spec(spec)
    # 先注册再执行：巡检内的 dataclass 装饰器会按模块名回查命名空间。
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


AUDIT = load_audit()
KB_ROOT: Path = AUDIT.KB_ROOT
# 主题口径与巡检共用同一实现，避免两处各推一套导致索引与巡检对同一篇笔记判出不同主题。
note_theme = AUDIT.note_theme
DECLARED_THEMES = AUDIT.DECLARED_THEMES
CONTRACT_DIRS = AUDIT.CONTRACT_DIRS
ACTIVE_STATUS = AUDIT.ACTIVE_STATUS


def build_index() -> dict[str, Any]:
    """扫描全库笔记，生成结构化索引对象。

    [参数] 无。
    [返回] dict[str, Any]: 含 schema 版本、笔记数与逐篇字段的索引。
    最近修改时间: 2026-08-12 新增机器索引脚本。
    """
    notes: list[dict[str, Any]] = []
    latest_mtime = 0.0
    for filepath in sorted(KB_ROOT.rglob("*.md")):
        if filepath.name.startswith("."):
            continue
        facts = AUDIT.collect_note_facts(filepath)
        mtime = filepath.stat().st_mtime
        latest_mtime = max(latest_mtime, mtime)
        # frontmatter 缺失或字段不全的笔记也要入索引：用文件名兜底标题，避免漏检。
        partial = not facts.title or not facts.status
        notes.append(
            {
                "path": facts.path,
                "title": facts.title or filepath.stem,
                "aliases": list(facts.aliases),
                "tags": list(facts.tags),
                "topics": list(facts.topics),
                "status": facts.status,
                "theme": note_theme(facts.path),
                "superseded_by": list(facts.superseded_by),
                "mtime": round(mtime, 3),
                "partial": partial,
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "notes_count": len(notes),
        "latest_mtime": round(latest_mtime, 3),
        "notes": notes,
    }


def write_index(index: dict[str, Any]) -> Path:
    """把索引写入知识库根并回读校验。

    [参数] index: 待写入的索引对象。
    [返回] Path: 索引文件路径。
    最近修改时间: 2026-08-12 新增机器索引脚本。
    """
    target = KB_ROOT / INDEX_NAME
    payload = json.dumps(index, ensure_ascii=False, indent=2)
    target.write_text(payload, encoding="utf-8")
    # 写后回读，确保落盘内容与预期一致。
    back = json.loads(target.read_text(encoding="utf-8"))
    if back.get("notes_count") != index["notes_count"]:
        raise RuntimeError("索引回读校验失败：笔记数不一致")
    return target


def current_kb_state() -> tuple[int, float]:
    """统计当前知识库的笔记数与最新修改时间，用于索引新鲜度判断。

    [参数] 无。
    [返回] tuple[int, float]: 笔记数与最新 mtime。
    最近修改时间: 2026-08-12 新增机器索引脚本。
    """
    count = 0
    latest = 0.0
    for filepath in KB_ROOT.rglob("*.md"):
        if filepath.name.startswith("."):
            continue
        count += 1
        latest = max(latest, filepath.stat().st_mtime)
    return count, round(latest, 3)


def load_index(auto_rebuild: bool = True) -> dict[str, Any]:
    """读取索引；缺失或过期时自动重建，避免检索命中过期数据。

    [参数] auto_rebuild: 索引缺失或过期时是否自动重建。
    [返回] dict[str, Any]: 可用的索引对象。
    最近修改时间: 2026-08-12 新增机器索引脚本。
    """
    target = KB_ROOT / INDEX_NAME
    if target.exists():
        try:
            index = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            index = None
        if index is not None:
            count, latest = current_kb_state()
            fresh = index.get("notes_count") == count and index.get("latest_mtime", 0) >= latest
            if fresh or not auto_rebuild:
                return index
    if not auto_rebuild:
        raise RuntimeError("索引不存在或不可解析")
    index = build_index()
    write_index(index)
    return index


def query_index(index: dict[str, Any], keyword: str) -> list[dict[str, Any]]:
    """按六类结构化字段加正文匹配关键词，并给出命中原因。

    结构化字段只覆盖 frontmatter，实测会漏掉「正文讲了但标签没写」的笔记，
    因此始终附带一次正文扫描并合并结果，保证查询结果是结构化命中与全文命中的超集。

    [参数] index: 索引对象；keyword: 查询关键词，大小写不敏感。
    [返回] list[dict[str, Any]]: 命中笔记列表，按命中字段数降序。
    最近修改时间: 2026-08-12 补正文兜底，修复纯 frontmatter 索引的召回损失。
    """
    needle = keyword.strip().lower()
    if not needle:
        return []
    results = []
    for note in index["notes"]:
        reasons = []
        if needle in note["title"].lower():
            reasons.append("title")
        if any(needle in str(a).lower() for a in note["aliases"]):
            reasons.append("aliases")
        if any(needle in str(t).lower() for t in note["tags"]):
            reasons.append("tags")
        if any(needle in str(t).lower() for t in note["topics"]):
            reasons.append("topics")
        if needle in note["theme"].lower():
            reasons.append("theme")
        if needle in note["path"].lower():
            reasons.append("path")
        # 正文兜底：结构化字段未命中时也要看正文，避免漏掉未打标签的相关笔记。
        filepath = KB_ROOT / note["path"]
        try:
            if needle in filepath.read_text(encoding="utf-8-sig").lower():
                reasons.append("body")
        except OSError:
            pass
        if reasons:
            results.append(
                {
                    "path": note["path"],
                    "title": note["title"],
                    "theme": note["theme"],
                    "status": note["status"],
                    "matched": reasons,
                    "partial": note["partial"],
                    "superseded_by": note["superseded_by"],
                }
            )
    # 结构化命中比纯正文命中更相关：先按非 body 命中数降序，再按总命中数，最后按路径稳定排序。
    results.sort(
        key=lambda item: (
            -len([r for r in item["matched"] if r != "body"]),
            -len(item["matched"]),
            item["path"],
        )
    )
    return results


def check_frontmatter() -> dict[str, Any]:
    """校验活动区笔记的 frontmatter 必填字段与状态枚举合规性。

    `note-schema.md` 要求新笔记含完整 frontmatter，但该要求原先只是文字约定、
    漏填不报错，实测导致约三成笔记不合规、状态枚举还漂移出未声明值。
    本函数把它变成可机器校验的闸门。

    归档区豁免只覆盖「有没有头部」与「必填字段齐不齐」——不为历史残留补字段；
    但状态值合法性对全库生效：归档退场本身要写 `status: archived`，整体豁免会让
    归档区变成枚举盲区，实测该区曾长期存在未声明的 `test-fixture` 而零告警。

    [参数] 无。
    [返回] dict[str, Any]: 含三类不合规清单与统计的报告。
    最近修改时间: 2026-08-12 归档豁免收窄，状态值合法性改为对全库生效。
    """
    allowed_status = set(DECLARED_STATUS) | set(CASE_STATUS)
    missing_frontmatter: list[str] = []
    missing_fields: list[dict[str, Any]] = []
    bad_status: list[dict[str, str]] = []
    checked = 0
    exempt = 0

    for filepath in sorted(KB_ROOT.rglob("*.md")):
        if filepath.name.startswith("."):
            continue
        rel = filepath.relative_to(KB_ROOT).as_posix()
        is_exempt = rel.startswith(CHECK_EXEMPT_PREFIXES)
        if is_exempt:
            exempt += 1
        else:
            checked += 1
        # 与巡检口径一致：utf-8-sig 容忍 BOM，避免带 BOM 的笔记被误判为无 frontmatter。
        text = filepath.read_text(encoding="utf-8-sig")
        if not text.startswith("---"):
            if not is_exempt:
                missing_frontmatter.append(rel)
            continue
        fields = AUDIT.parse_frontmatter(text)
        if not is_exempt:
            absent = [name for name in REQUIRED_FIELDS if name not in fields]
            if absent:
                missing_fields.append({"path": rel, "missing": absent})
        # 状态值合法性不随归档豁免：写了状态就必须是声明过的枚举值。
        status = fields.get("status", "")
        if status and status not in allowed_status:
            bad_status.append({"path": rel, "status": status})

    total_bad = len(missing_frontmatter) + len(missing_fields) + len(bad_status)
    return {
        "ok": total_bad == 0,
        "checked_notes": checked,
        "exempt_notes": exempt,
        "violation_count": total_bad,
        "missing_frontmatter": missing_frontmatter,
        "missing_required_fields": missing_fields,
        "status_out_of_enum": bad_status,
        "allowed_status": sorted(allowed_status),
    }


def build_alias_map() -> dict[str, str]:
    """建立笔记的四种可引用形态到裸相对路径的映射。

    双链可能写完整路径、无后缀路径、标题或文件名。接替关系校验与死链校验都要按同一套
    形态解析目标，定义放在一处，避免两处各维护一份导致同一条链接被判出不同结果。

    [参数] 无。
    [返回] dict[str, str]: 别名到裸相对路径的映射；同名冲突时保留先扫到的那篇。
    最近修改时间: 2026-08-12 新增，供接替关系校验与死链校验共用。
    """
    alias_to_path: dict[str, str] = {}
    # 1. 逐篇取标题，标题缺失时留空，由路径与文件名两种形态兜底。
    for filepath in sorted(KB_ROOT.rglob("*.md")):
        if filepath.name.startswith("."):
            continue
        rel = filepath.relative_to(KB_ROOT).as_posix()
        text = filepath.read_text(encoding="utf-8-sig")
        title = AUDIT.parse_frontmatter(text).get("title", "") if text.startswith("---") else ""
        # 2. 四种形态都登记；setdefault 保证同名冲突时不覆盖先扫到的那篇。
        for alias in (rel, rel.removesuffix(".md"), title, Path(rel).stem):
            if alias:
                alias_to_path.setdefault(alias, rel)
    return alias_to_path


def strip_code_spans(text: str) -> str:
    """抹掉围栏代码块与行内代码，只保留正文可链接区域。

    笔记正文经常用代码片段举例说明双链写法本身（例如解释 `- "[[目标]]"` 这种 YAML 引号
    问题）。不排除这些区域，写文档说明链接格式就会被判成死链，实测已出现过 1 例误报。

    [参数] text: 笔记全文。
    [返回] str: 代码区域已替换为空的文本，行数保持不变便于定位。
    最近修改时间: 2026-08-12 新增，供死链校验排除文档示例。
    """
    lines = []
    fence = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        # 1. 围栏进出判定：只认与开启符号同类的围栏收尾，避免嵌套围栏提前退出。
        if fence:
            if stripped.startswith(fence):
                fence = ""
            lines.append("")
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = stripped[:3]
            lines.append("")
            continue
        # 2. 行内代码：反引号成对包裹的片段整段抹掉，不跨行匹配。
        lines.append(re.sub(r"`[^`\n]*`", "", line))
    return "\n".join(lines)


def check_dead_links() -> dict[str, Any]:
    """校验全库双链目标是否都能解析到真实笔记。

    双链是知识库的核心导航机制，但此前四类校验（frontmatter 契约、接替关系、孤儿、
    冲突归组）都不覆盖它。实测全库 160 条双链里有 18 处解析不到目标，占 11%，其中 8 处
    指向 `note-schema` 曾要求写 wikilink、而落点从未创建的实体笔记。人工核对不可靠：
    上一轮口头判断「无新增死链」时，实际自己引入了 1 处。

    [参数] 无。
    [返回] dict[str, Any]: 含死链清单与统计的报告；按目标聚合，附来源笔记。
    最近修改时间: 2026-08-12 新增死链校验。
    """
    alias_to_path = build_alias_map()
    dead: dict[str, list[str]] = {}
    checked_links = 0
    # 1. 逐篇扫描正文双链，先抹掉代码区域再匹配，避免把写法示例判成死链。
    for filepath in sorted(KB_ROOT.rglob("*.md")):
        if filepath.name.startswith("."):
            continue
        rel = filepath.relative_to(KB_ROOT).as_posix()
        body = strip_code_spans(filepath.read_text(encoding="utf-8-sig"))
        for match in re.finditer(r"\[\[([^\]]+)\]\]", body):
            target = AUDIT.normalize_wikilink(match.group(1))
            if not target:
                continue
            checked_links += 1
            if target not in alias_to_path:
                dead.setdefault(target, []).append(rel)
    # 2. 按目标聚合并附来源笔记，便于一次定位同一个坏目标的全部引用点。
    entries = [
        {"target": target, "referenced_by": sorted(set(sources)), "hit_count": len(sources)}
        for target, sources in sorted(dead.items())
    ]
    return {
        "ok": not entries,
        "checked_links": checked_links,
        "dead_link_count": sum(e["hit_count"] for e in entries),
        "dead_links": entries,
    }


def check_supersession() -> dict[str, Any]:
    """校验接替关系是否双向，以及已被接替的笔记状态是否仍是 active。

    `note-schema.md` 声明「接替关系必须双向」与「superseded_by 非空时 status 不得为 active」，
    但两条此前只是文字约定。实测全库 `supersedes` 与 `superseded_by` 出现 0 次——iterate
    环节从未被执行；一旦开始执行，缺少机器校验会让单侧接替静默留存，检索顺不到接替笔记。
    归档区不豁免：归档退场本身就要写 `superseded_by`，豁免会让接替链在归档后断掉不报。

    [参数] 无。
    [返回] dict[str, Any]: 含两类违规清单与统计的报告。
    最近修改时间: 2026-08-12 别名映射改用共用函数，与死链校验统一解析口径。
    """
    notes: dict[str, dict[str, Any]] = {}
    alias_to_path = build_alias_map()
    # 1. 扫描全库，抽出每篇笔记的状态与两个方向的接替字段。
    for filepath in sorted(KB_ROOT.rglob("*.md")):
        if filepath.name.startswith("."):
            continue
        rel = filepath.relative_to(KB_ROOT).as_posix()
        text = filepath.read_text(encoding="utf-8-sig")
        if not text.startswith("---"):
            continue
        fields = AUDIT.parse_frontmatter(text)
        notes[rel] = {
            "status": fields.get("status", ""),
            "supersedes": {
                target
                for target in (
                    AUDIT.normalize_wikilink(v) for v in AUDIT.parse_list_field(text, "supersedes")
                )
                if target
            },
            "superseded_by": {
                target
                for target in (
                    AUDIT.normalize_wikilink(v)
                    for v in AUDIT.parse_list_field(text, "superseded_by")
                )
                if target
            },
            "resolved_supersedes": set(),
            "resolved_superseded_by": set(),
        }

    dangling: list[dict[str, str]] = []
    active_with_pointer: list[dict[str, str]] = []
    # 2. 把两个方向的目标解析成笔记路径，解析不到的直接记为悬空。
    for rel, entry in notes.items():
        for field in ("supersedes", "superseded_by"):
            for target in entry[field]:
                resolved = alias_to_path.get(target)
                if resolved is None:
                    dangling.append(
                        {"path": rel, "field": field, "target": target, "reason": "目标笔记不存在"}
                    )
                else:
                    entry["resolved_" + field].add(resolved)
    # 3. 按路径比对双向：任一方向缺对侧都算治理未闭环。
    for rel, entry in notes.items():
        if entry["superseded_by"] and entry["status"] == ACTIVE_STATUS:
            active_with_pointer.append({"path": rel, "status": entry["status"]})
        for target in entry["resolved_superseded_by"]:
            if rel not in notes[target]["resolved_supersedes"]:
                dangling.append(
                    {
                        "path": rel,
                        "field": "superseded_by",
                        "target": target,
                        "reason": "对侧未写 supersedes",
                    }
                )
        for target in entry["resolved_supersedes"]:
            if rel not in notes[target]["resolved_superseded_by"]:
                dangling.append(
                    {
                        "path": rel,
                        "field": "supersedes",
                        "target": target,
                        "reason": "对侧未写 superseded_by",
                    }
                )

    total_bad = len(dangling) + len(active_with_pointer)
    return {
        "ok": total_bad == 0,
        "supersession_violation_count": total_bad,
        "dangling_supersession": dangling,
        "active_with_superseded_by": active_with_pointer,
    }


def parse_args() -> argparse.Namespace:
    """解析命令行参数。

    [参数] 无。
    [返回] argparse.Namespace: 含子命令与查询关键词的参数对象。
    最近修改时间: 2026-08-12 check 帮助文案补双链有效性校验。
    """
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="扫描全库并重建 _index.json")
    query = sub.add_parser("query", help="按关键词检索索引，索引过期时自动重建")
    query.add_argument("--keyword", required=True, help="查询关键词，匹配标题/别名/标签/topics/主题/路径")
    query.add_argument("--limit", type=int, default=0, help="限制返回条数，0 表示不限制")
    sub.add_parser("stats", help="输出索引覆盖与主题分布统计")
    sub.add_parser("check", help="校验 frontmatter 必填字段、状态枚举、接替关系双向性与双链有效性")
    return parser.parse_args()


def main() -> int:
    """执行索引构建、查询或统计。

    [参数] 无。
    [返回] int: 0 表示成功，4 表示知识库根目录不可达。
    最近修改时间: 2026-08-12 check 分支合并死链校验报告。
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parse_args()
    if not KB_ROOT.exists():
        print(json.dumps({"ok": False, "code": "KB_ROOT_NOT_FOUND"}, ensure_ascii=False))
        return 4

    if args.command == "build":
        index = build_index()
        target = write_index(index)
        print(
            json.dumps(
                {"ok": True, "index": target.name, "notes_count": index["notes_count"]},
                ensure_ascii=False,
            )
        )
        return 0

    if args.command == "check":
        frontmatter = check_frontmatter()
        supersession = check_supersession()
        dead_links = check_dead_links()
        # 三份报告扁平合并：调用方按具体违规键定位，不必区分是哪一类校验报出的。
        report = {
            **frontmatter,
            **{k: v for k, v in supersession.items() if k != "ok"},
            **{k: v for k, v in dead_links.items() if k != "ok"},
            "ok": frontmatter["ok"] and supersession["ok"] and dead_links["ok"],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        # 不合规时以非零退出码返回，便于当作闸门使用。
        return 0 if report["ok"] else 5

    if args.command == "query":
        index = load_index()
        hits = query_index(index, args.keyword)
        if args.limit > 0:
            hits = hits[: args.limit]
        print(
            json.dumps(
                {"ok": True, "keyword": args.keyword, "hit_count": len(hits), "hits": hits},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    index = load_index()
    themes: dict[str, int] = {}
    partial = 0
    for note in index["notes"]:
        themes[note["theme"]] = themes.get(note["theme"], 0) + 1
        if note["partial"]:
            partial += 1
    print(
        json.dumps(
            {
                "ok": True,
                "notes_count": index["notes_count"],
                "partial_notes": partial,
                "themes": dict(sorted(themes.items(), key=lambda kv: -kv[1])),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
