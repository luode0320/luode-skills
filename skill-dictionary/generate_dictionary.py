from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "skill-dictionary"
DATA_FILE = OUTPUT_DIR / "data.js"
MARKDOWN_FILE = ROOT / "字典.md"


@dataclass(frozen=True)
class DomainConfig:
    id: str
    label: str
    description: str


DOMAIN_ORDER = [
    DomainConfig("orchestration", "总控层", "流程分流、冲突裁决、阶段阻断与全局基础约定"),
    DomainConfig("memory", "记忆域", "新会话近期预热、跨会话历史检索、项目演进回顾、长期上下文补全"),
    DomainConfig("requirement", "需求域", "需求澄清、缺口识别、边界确认、验收前置"),
    DomainConfig("bug", "Bug 域", "问题录入、定位、运行时诊断、修复建议"),
    DomainConfig("baseline", "编码基线域", "开始编码即并行生效的基础质量规则"),
    DomainConfig("location", "代码位点域", "按改动位置叠加触发的实现规则"),
    DomainConfig("review", "编码审查域", "测试前的静态自审、语法检查、清理归位"),
    DomainConfig("test", "测试域", "策略、资源、功能验证、浏览器联动与回归"),
    DomainConfig("delivery", "交付域", "Git 协作与交付说明"),
    DomainConfig("seed", "扩展种子", "已入库但未并入主规划的参考 skill"),
]

DOMAIN_SECTION_MATCH = {
    "总控层": "总控层",
    "记忆域": "记忆域",
    "需求域": "需求域",
    "Bug 域": "Bug 域",
    "编码基线域": "编码基线域",
    "代码位点域": "代码位点域",
    "编码审查域": "编码审查域",
    "测试域": "测试域",
    "交付域": "交付域",
}

STATUS_META = {
    "implemented": {"label": "已实现", "rank": 1},
    "planned": {"label": "规划中", "rank": 2},
    "seed": {"label": "扩展种子", "rank": 3},
}

DOC_KIND_ORDER = {
    "总规划": 1,
    "实施记录": 2,
    "巡检记录": 3,
    "验证样例": 4,
    "复盘记录": 5,
    "遗留问题": 6,
    "其他文档": 7,
}

CHINESE_NUMERAL_MAP = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def second_level_headings(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}

    match = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not match:
        return {}

    frontmatter = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter


def collect_relative_files(directory: Path) -> list[str]:
    if not directory.exists():
        return []
    return sorted(normalize_path(path) for path in directory.rglob("*") if path.is_file())


def parse_markdown_tables(section_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in section_text.splitlines():
        if not line.strip().startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip().split("|")[1:-1]]
        if len(cells) < 3:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue

        skill_match = re.search(r"`([^`]+)`", cells[0])
        if not skill_match:
            continue

        rows.append(
            {
                "name": skill_match.group(1),
                "trigger": cells[1],
                "responsibility": cells[2],
            }
        )
    return rows


def split_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for match in re.finditer(r"^##\s+([^\n]+)\n(.*?)(?=^##\s+|\Z)", text, re.M | re.S):
        title = match.group(1).strip()
        body = match.group(2).strip()
        sections[title] = body
    return sections


def parse_plan_document() -> tuple[Path, dict[str, list[dict[str, str]]]]:
    candidates = sorted(path for path in ROOT.glob("*skill.md") if path.is_file())
    if not candidates:
        raise FileNotFoundError("未找到编码总规划文档（*skill.md）。")

    plan_path = candidates[0]
    text = read_text(plan_path)
    raw_sections = split_sections(text)

    plan_domains: dict[str, list[dict[str, str]]] = {}
    for domain_label, section_marker in DOMAIN_SECTION_MATCH.items():
        matched_title = next((title for title in raw_sections if section_marker in title), None)
        if not matched_title:
            plan_domains[domain_label] = []
            continue
        plan_domains[domain_label] = parse_markdown_tables(raw_sections[matched_title])

    return plan_path, plan_domains


def iter_skill_directories() -> list[Path]:
    directories: list[Path] = []
    parents = [ROOT, ROOT / "downloaded-seeds"]

    for parent in parents:
        if not parent.exists():
            continue
        for directory in sorted(parent.iterdir()):
            if directory.is_dir() and (directory / "SKILL.md").exists():
                directories.append(directory)

    return directories


def has_license_file(directory: Path) -> bool:
    return any(path.is_file() for path in directory.glob("LICENSE*"))


def parse_actual_skills() -> dict[str, dict]:
    skills: dict[str, dict] = {}

    for directory in iter_skill_directories():
        skill_path = directory / "SKILL.md"
        text = read_text(skill_path)
        frontmatter = parse_frontmatter(text)
        name = frontmatter.get("name", directory.name)
        skills[name] = {
            "name": name,
            "directory": directory.name,
            "title": first_heading(text) or name,
            "description": frontmatter.get("description", ""),
            "skill_path": normalize_path(skill_path),
            "directory_path": normalize_path(directory),
            "sections": second_level_headings(text),
            "references": collect_relative_files(directory / "references"),
            "agents": collect_relative_files(directory / "agents"),
            "has_license": has_license_file(directory),
        }

    return skills


def to_wave_number(value: str) -> int:
    if value.isdigit():
        return int(value)
    total = 0
    for char in value:
        total += CHINESE_NUMERAL_MAP.get(char, 0)
    return total or 999


def classify_doc(name: str) -> str:
    if name.endswith("编码skill.md"):
        return "总规划"
    if "实施计划闭环记录" in name:
        return "实施记录"
    if "巡检" in name:
        return "巡检记录"
    if "验证样例" in name:
        return "验证样例"
    if "复盘记录" in name:
        return "复盘记录"
    if "遗留问题" in name:
        return "遗留问题"
    return "其他文档"


def wave_sort_key(name: str) -> tuple[int, int]:
    match = re.search(r"第([一二三四五六七八九十0-9]+)波", name)
    if not match:
        return (0, 0)
    return (1, to_wave_number(match.group(1)))


def collect_project_docs(plan_path: Path) -> list[dict]:
    docs = []
    for path in sorted(ROOT.iterdir()):
        if not path.is_file() or path.suffix.lower() != ".md":
            continue
        if path.name == MARKDOWN_FILE.name:
            continue

        text = read_text(path)
        docs.append(
            {
                "id": f"doc:{path.stem}",
                "name": path.stem,
                "file_name": path.name,
                "title": first_heading(text) or path.stem,
                "kind": classify_doc(path.name),
                "path": normalize_path(path),
                "is_plan_doc": path == plan_path,
            }
        )

    docs.sort(
        key=lambda item: (
            DOC_KIND_ORDER[item["kind"]],
            wave_sort_key(item["file_name"]),
            item["file_name"],
        )
    )
    return docs


def build_focus_points(item: dict) -> list[str]:
    status = item["status"]
    domain = item["domain_label"]
    points: list[str] = []

    if status == "planned":
        points.append("先补齐触发 description、邻接边界和最小 references，再决定是否正式建目录。")
        points.append("优先确认它与同域相邻 skill 的拆分边界，避免新建后职责重叠。")
    elif status == "seed":
        points.append("先决定它是并入主规划、保持外部种子，还是拆成多个更窄的内部 skill。")
        points.append("如果准备纳入体系，先补上与主规划域的映射关系和落位说明。")
    else:
        points.append("优先检查 description 是否具体到触发信号，而不是只写抽象用途。")
        points.append("检查 references 是否足以承接复杂场景，避免 SKILL.md 过厚或过空。")

    domain_points = {
        "总控层": "重点看是否只做分流、阻断或全局基础约定，没有越权覆盖单域 skill。",
        "记忆域": "重点看它是否只补近期或历史上下文，不越权代替当前需求、Bug、编码或交付判断。",
        "需求域": "重点看是否能区分需求缺口、边界变化、验收偏差和历史 Bug。",
        "Bug 域": "重点看静态定位与运行时诊断的切换条件是否清楚。",
        "编码基线域": "重点看它是否能并行生效，并且不抢位点域或审查域职责。",
        "代码位点域": "重点看主位点与横切位点是否可并行叠加，而不是互相覆盖。",
        "编码审查域": "重点看它是否只处理静态质量问题，不越界替代测试。",
        "测试域": "重点看测试策略、资源、功能验证、联调、回归是否已经拆开。",
        "交付域": "重点看 Git 协作与交付说明是否已分层收口，并且不越界替代测试或发布流程。",
        "扩展种子": "重点看这个种子是否真的能落入主规划，还是保持独立参考更合适。",
    }
    points.append(domain_points[domain])

    if item["status"] == "implemented" and not item["references"]:
        points.append("当前没有 references，可考虑补最小示例或边界文档以降低后续维护成本。")

    return points


def merge_dictionary(plan_domains: dict[str, list[dict[str, str]]], actual_skills: dict[str, dict]) -> list[dict]:
    actual_remaining = dict(actual_skills)
    items: list[dict] = []

    for domain_index, config in enumerate(DOMAIN_ORDER[:-1], start=1):
        planned_items = plan_domains.get(config.label, [])
        for item_index, planned in enumerate(planned_items, start=1):
            actual = actual_remaining.pop(planned["name"], None)
            status = "implemented" if actual else "planned"
            merged = {
                "id": planned["name"],
                "name": planned["name"],
                "title": actual["title"] if actual else planned["name"],
                "status": status,
                "status_label": STATUS_META[status]["label"],
                "domain_id": config.id,
                "domain_label": config.label,
                "domain_description": config.description,
                "domain_order": domain_index,
                "item_order": item_index,
                "auto_trigger": actual["description"] if actual else planned["trigger"],
                "core_responsibility": planned["responsibility"],
                "skill_path": actual["skill_path"] if actual else "",
                "directory_path": actual["directory_path"] if actual else "",
                "directory": actual["directory"] if actual else "",
                "sections": actual["sections"] if actual else [],
                "references": actual["references"] if actual else [],
                "agents": actual["agents"] if actual else [],
                "has_license": actual["has_license"] if actual else False,
            }
            merged["focus_points"] = build_focus_points(merged)
            items.append(merged)

    seed_config = DOMAIN_ORDER[-1]
    for seed_index, actual in enumerate(sorted(actual_remaining.values(), key=lambda value: value["name"]), start=1):
        merged = {
            "id": actual["name"],
            "name": actual["name"],
            "title": actual["title"],
            "status": "seed",
            "status_label": STATUS_META["seed"]["label"],
            "domain_id": seed_config.id,
            "domain_label": seed_config.label,
            "domain_description": seed_config.description,
            "domain_order": len(DOMAIN_ORDER),
            "item_order": seed_index,
            "auto_trigger": actual["description"],
            "core_responsibility": "当前已在仓库中，但尚未并入主规划域表。",
            "skill_path": actual["skill_path"],
            "directory_path": actual["directory_path"],
            "directory": actual["directory"],
            "sections": actual["sections"],
            "references": actual["references"],
            "agents": actual["agents"],
            "has_license": actual["has_license"],
        }
        merged["focus_points"] = build_focus_points(merged)
        items.append(merged)

    return items


def build_domain_summary(items: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        grouped[item["domain_label"]].append(item)

    summary = []
    for order, config in enumerate(DOMAIN_ORDER, start=1):
        domain_items = sorted(grouped.get(config.label, []), key=lambda value: value["item_order"])
        summary.append(
            {
                "id": config.id,
                "label": config.label,
                "description": config.description,
                "order": order,
                "implemented_count": sum(1 for item in domain_items if item["status"] == "implemented"),
                "planned_count": sum(1 for item in domain_items if item["status"] == "planned"),
                "seed_count": sum(1 for item in domain_items if item["status"] == "seed"),
                "total_count": len(domain_items),
                "items": domain_items,
            }
        )
    return summary


def build_recommendations(domain_summary: list[dict]) -> list[str]:
    summary_by_label = {item["label"]: item for item in domain_summary}
    recommendations = []

    requirement_missing = summary_by_label["需求域"]["planned_count"]
    bug_missing = summary_by_label["Bug 域"]["planned_count"]
    test_missing = summary_by_label["测试域"]["planned_count"]
    delivery_missing = summary_by_label["交付域"]["planned_count"]
    total_planned = sum(
        item["implemented_count"] + item["planned_count"] for item in domain_summary if item["label"] != "扩展种子"
    )
    total_missing = sum(
        item["planned_count"] for item in domain_summary if item["label"] != "扩展种子"
    )
    seed_items = {item["name"] for item in summary_by_label["扩展种子"]["items"]}
    all_items = {item["name"] for domain in domain_summary for item in domain["items"]}

    if total_missing == 0:
        recommendations.append(
            f"{total_planned} 个规划 skill 已全部独立落地，后续优化优先检查 description 命中率、相邻 skill 边界和 references 的信息密度。"
        )
    elif requirement_missing:
        recommendations.append(
            f"优先补齐需求域缺口，目前仍缺 {requirement_missing} 个规划 skill，后续需求澄清和验收会继续压在总控层。"
        )

    if bug_missing:
        recommendations.append(
            f"Bug 域还缺 {bug_missing} 个环节，尤其是复现、范围界定、诊断日志和修复后验证，建议补完整闭环。"
        )
    if test_missing or delivery_missing:
        recommendations.append(
            f"测试域缺 {test_missing} 个、交付域缺 {delivery_missing} 个，建议先补 `test-strategy-rules` 和交付域三件套。"
        )

    if {"frontend-ui-visual-rules", "frontend-component-rules"} <= all_items:
        recommendations.append(
            "当前规划同时包含 `frontend-component-rules` 与 `frontend-ui-visual-rules`，建议前者聚焦组件工程与状态边界，后者聚焦页面视觉与交互体验，避免触发歧义。"
        )
    if "security-best-practices" in seed_items:
        recommendations.append(
            "评估 `security-best-practices` 是否保持为体系外种子，还是拆分吸收到现有位点类规则。"
        )
    if total_missing == 0:
        recommendations.append(
            "可以开始按域做第二轮巡检：先审触发 description 是否足够具体，再审 references 是否过厚、过空或与相邻 skill 重叠。"
        )

    return recommendations[:5]


def build_downloaded_seed_state() -> dict:
    seed_dir = ROOT / "downloaded-seeds"
    children = sorted(path.name for path in seed_dir.iterdir()) if seed_dir.exists() else []
    return {
        "path": normalize_path(seed_dir) if seed_dir.exists() else "downloaded-seeds",
        "exists": seed_dir.exists(),
        "entry_count": len(children),
        "entries": children,
    }


def build_payload() -> dict:
    plan_path, plan_domains = parse_plan_document()
    actual_skills = parse_actual_skills()
    items = merge_dictionary(plan_domains, actual_skills)
    domain_summary = build_domain_summary(items)
    docs = collect_project_docs(plan_path)

    planned_total = sum(
        1
        for item in items
        if item["status"] in {"implemented", "planned"} and item["domain_label"] != "扩展种子"
    )
    implemented_total = sum(1 for item in items if item["status"] == "implemented")
    planned_missing = sum(1 for item in items if item["status"] == "planned")
    seed_total = sum(1 for item in items if item["status"] == "seed")
    references_total = sum(len(item["references"]) for item in items if item["status"] != "planned")
    agents_total = sum(len(item["agents"]) for item in items if item["status"] != "planned")

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "repo_root": str(ROOT),
        "plan_doc": normalize_path(plan_path),
        "plan_doc_name": plan_path.name,
        "summary": {
            "planned_total": planned_total,
            "implemented_total": implemented_total,
            "planned_missing": planned_missing,
            "seed_total": seed_total,
            "doc_total": len(docs),
            "references_total": references_total,
            "agents_total": agents_total,
        },
        "downloaded_seeds": build_downloaded_seed_state(),
        "domains": domain_summary,
        "items": sorted(
            items,
            key=lambda item: (item["domain_order"], STATUS_META[item["status"]]["rank"], item["item_order"], item["name"]),
        ),
        "docs": docs,
        "recommendations": build_recommendations(domain_summary),
    }


def render_markdown(payload: dict) -> str:
    lines: list[str] = []
    summary = payload["summary"]

    lines.append("# Skill 字典")
    lines.append("")
    lines.append("## 概览")
    lines.append("")
    lines.append(f"- 生成时间：{payload['generated_at']}")
    lines.append(f"- 静态页面：[`index.html`](index.html)")
    lines.append("- 刷新命令：`python skill-dictionary/generate_dictionary.py`")
    lines.append(f"- 主规划文档：[`{payload['plan_doc_name']}`]({payload['plan_doc']})")
    lines.append(f"- 已落地规划 skill：{summary['implemented_total']} / {summary['planned_total']}")
    lines.append(f"- 规划中待补 skill：{summary['planned_missing']}")
    lines.append(f"- 体系外扩展种子：{summary['seed_total']}")
    lines.append(f"- 根目录分析文档：{summary['doc_total']}")
    lines.append(f"- references 文件总数：{summary['references_total']}")
    lines.append(f"- agents 文件总数：{summary['agents_total']}")
    lines.append("")
    lines.append("## 技能目录树")
    lines.append("")
    for domain in payload["domains"]:
        lines.append(
            f"* **{domain['order']}.{domain['label']}**（已实现 {domain['implemented_count']} / 规划中 {domain['planned_count']} / 种子 {domain['seed_count']}）"
        )
        lines.append(f"  * 说明：{domain['description']}")
        if not domain["items"]:
            lines.append("  * 本分类暂无技能。")
            continue

        for item in domain["items"]:
            node_number = f"{domain['order']}.{item['item_order']}"
            lines.append(f"  * **{node_number} `{item['name']}`（{item['status_label']}）**")
            if item["skill_path"]:
                lines.append(f"    * [`{item['skill_path']}`]({item['skill_path']})")
            else:
                lines.append("    * 路径：待创建")
            lines.append(f"    * 核心职责：{item['core_responsibility']}")
        lines.append("")

    lines.append("## 项目文档目录")
    lines.append("")
    docs_by_kind: dict[str, list[dict]] = defaultdict(list)
    for doc in payload["docs"]:
        docs_by_kind[doc["kind"]].append(doc)

    for kind, docs in sorted(docs_by_kind.items(), key=lambda item: DOC_KIND_ORDER.get(item[0], 999)):
        lines.append(f"* **{kind}**")
        for index, doc in enumerate(docs, start=1):
            lines.append(f"  * **{index}.{doc['title']}**")
            lines.append(f"    * [`{doc['path']}`]({doc['path']})")
        lines.append("")

    lines.append("## 当前建议")
    lines.append("")
    for index, recommendation in enumerate(payload["recommendations"], start=1):
        lines.append(f"{index}. {recommendation}")
    lines.append("")

    lines.append("## downloaded-seeds 现状")
    lines.append("")
    if payload["downloaded_seeds"]["entry_count"]:
        lines.append(
            f"- 目录 [`{payload['downloaded_seeds']['path']}`]({payload['downloaded_seeds']['path']}) 当前有 {payload['downloaded_seeds']['entry_count']} 个条目。"
        )
    else:
        lines.append(
            f"- 目录 [`{payload['downloaded_seeds']['path']}`]({payload['downloaded_seeds']['path']}) 当前为空，页面中未收录外部 seed 文件。"
        )
    lines.append("")

    return "\n".join(lines)


def write_outputs(payload: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        "window.SKILL_DICTIONARY = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    MARKDOWN_FILE.write_text(render_markdown(payload), encoding="utf-8")


def main() -> None:
    payload = build_payload()
    write_outputs(payload)
    print(
        json.dumps(
            {
                "data_file": normalize_path(DATA_FILE),
                "markdown_file": normalize_path(MARKDOWN_FILE),
                "implemented_total": payload["summary"]["implemented_total"],
                "planned_missing": payload["summary"]["planned_missing"],
                "seed_total": payload["summary"]["seed_total"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
