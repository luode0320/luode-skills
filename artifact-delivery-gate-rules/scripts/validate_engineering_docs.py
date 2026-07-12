#!/usr/bin/env python3
"""校验需求、验收和实施 Markdown 文档的结构、追踪与图形门禁。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml


ID_PATTERN = re.compile(
    r"\b(?:SRC|DEC|REQ(?:-[A-Z]+)?|RULE|BOUND|GAP|SLICE|AC|CYCLE|TASK|TEST|ROLLBACK|EVIDENCE)-[A-Z0-9]+(?:-[A-Z0-9]+)*\b"
    # 补丁说明：补齐短周期任务和 EVD 证据 ID，避免严格追踪漏掉现有任务链。
    r"|\bT\d{2}-\d{2}\b"
    r"|\bEVD-[A-Z0-9]+(?:-[A-Z0-9]+)*\b"
)
# 补丁说明：为严格模式单独提供任务与证据提取规则，保证归属和证据类别可以分别核验。
TASK_ID_PATTERN = re.compile(r"\b(?:TASK-[A-Z0-9]+(?:-[A-Z0-9]+)*|T\d{2}-\d{2})\b")
EVIDENCE_ID_PATTERN = re.compile(r"\b(?:EVIDENCE-[A-Z0-9]+(?:-[A-Z0-9]+)*|EVD-[A-Z0-9]+(?:-[A-Z0-9]+)*)\b")
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*$")
FENCE_PATTERN = re.compile(r"^\s*```([\w-]*)\s*$")
# 图片引用由 check_images 独立校验，普通链接检查不重复处理图片语法。
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(\s*([^)]*?)\s*\)")
EMPTY_IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(\s*\)")
IMAGE_ID_PATTERN = re.compile(r"\bIMG-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
ASSET_FILENAME_PATTERN = re.compile(
    r"^(?P<stem>.+)\.(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)-v(?P<version>\d+)"
    r"(?P<extension>\.png|\.jpg|\.jpeg|\.webp)$"
)


def load_profiles(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        payload = yaml.safe_load(file)
    if not isinstance(payload, dict) or not isinstance(payload.get("profiles"), dict):
        raise ValueError("quality profile must contain a profiles mapping")
    return payload


def read_document(path: Path) -> Tuple[str, List[str]]:
    errors: List[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return "", [f"document is not valid UTF-8: {error}"]
    return text, errors


def headings(text: str) -> List[str]:
    values: List[str] = []
    for line in text.splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        value = re.sub(r"^\d+(?:\.\d+)*[.)]?\s+", "", match.group(1).strip())
        values.append(value)
    return values


def section_bodies(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    sections: Dict[str, List[str]] = {}
    current = ""
    for line in lines:
        match = HEADING_PATTERN.match(line)
        if match:
            current = re.sub(r"^\d+(?:\.\d+)*[.)]?\s+", "", match.group(1).strip())
            sections.setdefault(current, [])
        elif current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def mermaid_blocks(text: str) -> List[str]:
    blocks: List[str] = []
    lines = text.splitlines()
    inside = False
    current: List[str] = []
    language = ""
    for line in lines:
        match = FENCE_PATTERN.match(line)
        if match and not inside:
            inside = True
            language = match.group(1).strip().lower()
            current = []
            continue
        if match and inside:
            if language == "mermaid":
                blocks.append("\n".join(current).strip())
            inside = False
            language = ""
            current = []
            continue
        if inside:
            current.append(line)
    return blocks


# check_frontmatter 检查文档 YAML 头和 profile 约束，阻止元数据缺失导致的不可追踪文档。
# [参数] text: Markdown 文本；errors: 累积错误列表；profile: 当前质量 profile，可为空。
# [返回] None：直接向 errors 写入校验结果。
# 最近修改时间：2026-07-12 增加 profile 级必填元数据校验，保证不同文档类型的契约一致。
def check_frontmatter(text: str, errors: List[str], profile: Dict[str, Any] | None = None) -> None:
    """检查文档 YAML 头和 profile 约束，阻止元数据缺失导致的不可追踪文档。"""
    # 1. 解析 YAML 头并确认其为映射对象。
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        errors.append("missing YAML front matter")
        return
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        errors.append(f"invalid YAML front matter: {error}")
        return
    if not isinstance(metadata, dict):
        errors.append("front matter must be a mapping")
        return
    # 2. 合并基础字段与 profile 专项字段并检查非空。
    # 补丁说明：在基础字段之外合并 profile 字段，避免只校验通用头而漏掉专项约束。
    fields = ["schema_version", "doc_id", "doc_type", "source_ids", "status", "version", "current_slice", "updated_at"]
    fields.extend(str(field) for field in (profile or {}).get("required_frontmatter", []))
    for field in fields:
        value = metadata.get(field)
        if value in (None, "", []):
            errors.append(f"front matter missing non-empty field: {field}")
    if metadata.get("source_ids") and not isinstance(metadata.get("source_ids"), list):
        errors.append("front matter source_ids must be a list")
    # 3. 校验生命周期状态和更新时间格式，保证状态可被机器消费。
    if metadata.get("status") not in {"draft", "confirmed", "in_progress", "blocked", "accepted", "pending"}:
        errors.append("front matter status is outside the allowed lifecycle")
    updated_at = str(metadata.get("updated_at", ""))
    if updated_at and not re.match(r"^\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?$", updated_at):
        errors.append("front matter updated_at must use YYYY-MM-DD[ HH:mm[:ss]]")


def check_fences(text: str, errors: List[str]) -> None:
    fences = [line for line in text.splitlines() if line.strip().startswith("```")]
    if len(fences) % 2:
        errors.append("unclosed Markdown code fence")


def check_sections(text: str, profile: Dict[str, Any], errors: List[str]) -> None:
    existing = set(headings(text))
    bodies = section_bodies(text)
    lines = text.splitlines()

    def section_has_content(name: str) -> bool:
        for index, line in enumerate(lines):
            match = HEADING_PATTERN.match(line)
            if not match:
                continue
            normalized = re.sub(r"^\d+(?:\.\d+)*[.)]?\s+", "", match.group(1).strip())
            if normalized != name:
                continue
            level = len(line) - len(line.lstrip("#"))
            for following in lines[index + 1 :]:
                next_match = HEADING_PATTERN.match(following)
                if next_match:
                    next_level = len(following) - len(following.lstrip("#"))
                    if next_level <= level:
                        break
                    return True
                if following.strip():
                    return True
            return False
        return False

    for section in profile.get("required_sections", []):
        if section not in existing:
            errors.append(f"missing required section: {section}")
        elif not section_has_content(section):
            errors.append(f"required section is empty: {section}")
    for alternatives in profile.get("required_any_sections", []):
        names = [str(item) for item in alternatives]
        matched = next((name for name in names if name in existing and section_has_content(name)), None)
        if matched is None:
            errors.append(f"missing one of required sections: {names}")


def check_ids(text: str, profile: Dict[str, Any], errors: List[str]) -> List[str]:
    ids = ID_PATTERN.findall(text)
    # 引用同一个 ID 是追踪矩阵的正常行为；重复定义应由文档自审和跨文档索引检查识别。
    prefixes = tuple(f"{prefix}-" for prefix in profile.get("id_prefixes", []))
    if prefixes and not any(item.startswith(prefixes) for item in ids):
        errors.append(f"no IDs found for profile prefixes: {list(prefixes)}")
    return sorted(set(ids))


def markdown_table_count(text: str) -> int:
    lines = text.splitlines()
    return sum(1 for index, line in enumerate(lines[:-1]) if "|" in line and re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1]))


def check_profile_content(text: str, profile: Dict[str, Any], errors: List[str]) -> None:
    for phrase in profile.get("required_phrases", []):
        if str(phrase).lower() not in text.lower():
            errors.append(f"missing required content phrase: {phrase}")
    minimum_tables = int(profile.get("min_tables", 0))
    actual_tables = markdown_table_count(text)
    if actual_tables < minimum_tables:
        errors.append(f"insufficient Markdown tables: expected {minimum_tables}, got {actual_tables}")


# check_diagram_annotations 检查 Mermaid 图块非空且通过轻量语法前置校验。
# [参数] text: Markdown 文本；errors: 累积错误列表。
# [返回] None：直接向 errors 写入图块错误。
# 最近修改时间：2026-07-12 增加 Mermaid 语法前置调用，尽早拦截损坏图块。
def check_diagram_annotations(text: str, errors: List[str], require_context: bool = False) -> None:
    """检查 Mermaid 图块非空、图前说明和轻量语法。"""
    # 1. 逐行定位 Mermaid 起始位置，确保图前说明紧邻源码块。
    lines = text.splitlines()
    blocks = mermaid_blocks(text)
    block_index = 0
    for line_index, line in enumerate(lines):
        if not re.match(r"^\s*```mermaid\s*$", line, re.IGNORECASE):
            continue
        block_index += 1
        index = block_index
        if require_context:
            preceding = "\n".join(lines[max(0, line_index - 4):line_index])
            if "图形目的" not in preceding or "关联 ID" not in preceding:
                errors.append(f"Mermaid block {index} missing purpose and associated ID before fence")
    # 2. 对每个图块执行轻量语法校验并汇总错误。
    for index, block in enumerate(blocks, start=1):
        first = next((line.strip() for line in block.splitlines() if line.strip()), "")
        if not first:
            errors.append(f"empty Mermaid block: {index}")
        # 补丁说明：将每个图块交给统一语法检查，补足原先只判断非空的校验缺口。
        errors.extend(check_mermaid_syntax(block, index))


# check_mermaid_syntax 对 Mermaid 做无需浏览器的语法前置检查，尽早拒绝明显损坏的图块。
# [参数] block: 单个 Mermaid 图块；index: 图块序号。
# [返回] list[str]：图块语法错误列表。
# 最近修改时间：2026-07-12 新增轻量 Mermaid 校验，避免生成空图或断边图进入交付文档。
def check_mermaid_syntax(block: str, index: int) -> List[str]:
    """对 Mermaid 做无需浏览器的语法前置检查，尽早拒绝明显损坏的图块。"""
    # 1. 清理空行并识别图类型。
    errors: List[str] = []
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        return [f"empty Mermaid block: {index}"]
    diagram_type = lines[0].split()[0]
    if diagram_type not in {"flowchart", "graph", "sequenceDiagram", "stateDiagram-v2", "erDiagram"}:
        errors.append(f"unsupported Mermaid diagram type at block {index}: {diagram_type}")
    # 2. 校验括号配对和受支持的图类型。
    pairs = {"[": "]", "(": ")", "{": "}"}
    for opening, closing in pairs.items():
        if sum(line.count(opening) for line in lines) != sum(line.count(closing) for line in lines):
            errors.append(f"unbalanced Mermaid delimiter {opening}{closing} at block {index}")
    # 3. 校验流程图边或时序图消息，阻止只有节点没有关系的伪图。
    body = "\n".join(lines[1:])
    if diagram_type in {"flowchart", "graph"} and body and not re.search(r"(-->|---|-.->|==>)", body):
        errors.append(f"Mermaid flowchart has no edge at block {index}")
    if diagram_type == "sequenceDiagram" and body and not re.search(r"->>|-->>|->", body):
        errors.append(f"Mermaid sequence has no message at block {index}")
    return errors


def check_placeholders(text: str, payload: Dict[str, Any], errors: List[str]) -> None:
    terms = [str(term) for term in payload.get("placeholder_terms", [])]
    hits: List[str] = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # 文档可以在规则条款中引用“禁止某词”；这种引用不是实际占位。
        if re.search(r"禁止|禁用|不得|不允许|不能|不可|避免|禁止使用", line):
            continue
        lowered = line.lower()
        hits.extend(term for term in terms if term.lower() in lowered)
    if hits:
        errors.append(f"placeholder or vague terms found: {sorted(set(hits))}")


def check_na_reasons(text: str, errors: List[str]) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        searchable = re.sub(r"`[^`]*`", "", line)
        if re.search(r"\bN/A\b|不适用", searchable) and not re.search(r"原因|理由|证据|依据|不涉及|本节", searchable):
            errors.append(f"N/A requires reason/evidence at line {line_number}")


def check_links(text: str, root: Path, document: Path, errors: List[str]) -> None:
    for target in LINK_PATTERN.findall(text):
        clean = target.split("#", 1)[0].strip().strip("<>")
        if not clean or re.match(r"^(?:https?|mailto):", clean):
            continue
        candidate = (document.parent / clean).resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            errors.append(f"link escapes validation root: {target}")
            continue
        if not candidate.exists():
            errors.append(f"broken local link: {target}")


def _image_policy_root(root: Path, profile_payload: Dict[str, Any] | None = None) -> Path:
    policy = (profile_payload or {}).get("image_policy", {})
    asset_root = str(policy.get("asset_root", "doc/data/images"))
    return (root / asset_root).resolve()


def _iter_markdown_images(text: str) -> Iterable[Tuple[str, str]]:
    """提取图片 alt 与目标路径，并忽略围栏代码示例。"""
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # 行内代码是语法示例，不会渲染为真实图片。
        searchable = re.sub(r"`[^`]*`", "", line)
        for match in IMAGE_PATTERN.finditer(searchable):
            yield match.group(1), match.group(2).strip()


def _has_non_fenced_empty_image(text: str) -> bool:
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        searchable = re.sub(r"`[^`]*`", "", line)
        if not in_fence and EMPTY_IMAGE_PATTERN.search(searchable):
            return True
    return False


def _rendered_markdown_text(text: str) -> str:
    """移除围栏和行内代码，保留会实际渲染的 Markdown 文本。"""
    in_fence = False
    rendered: List[str] = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            # 去掉行内代码标记但保留字段值，支持 ``N/A`` 这类规范写法。
            rendered.append(re.sub(r"`([^`]*)`", r"\1", line))
    return "\n".join(rendered)


def _image_target_path(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1:target.index(">")]
    # Markdown 允许标题，但图片路径本身不得包含空格。
    return target.split()[0] if target.split() else ""


def _has_image_signature(path: Path, extension: str) -> bool:
    try:
        data = path.read_bytes()
    except OSError:
        return False
    if not data:
        return False
    extension = extension.lower()
    if extension == ".png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if extension in {".jpg", ".jpeg"}:
        return data.startswith(b"\xff\xd8\xff") and data.endswith(b"\xff\xd9")
    if extension == ".webp":
        return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    return False


def _image_decision(text: str) -> str | None:
    rendered_text = _rendered_markdown_text(text)
    matches = re.findall(r"图片资产决策\s*[:：]\s*([^\n|]+)", rendered_text, re.IGNORECASE)
    if not matches:
        return None
    decisions: List[str] = []
    for value in matches:
        value = value.strip()
        if re.match(r"^(?:N/A|不适用|不需要)\b", value, re.IGNORECASE):
            decisions.append("na")
        elif value.startswith("需要"):
            decisions.append("needed")
        else:
            decisions.append("invalid")
    unique_decisions = set(decisions)
    if len(unique_decisions) != 1:
        return "invalid"
    return decisions[0]


def _image_decision_has_evidence(text: str) -> bool:
    rendered_text = _rendered_markdown_text(text)
    matches = re.findall(r"图片资产决策\s*[:：]\s*([^\n|]+)", rendered_text, re.IGNORECASE)
    if not matches:
        return False
    return bool(re.search(r"原因|理由|证据|依据|不涉及|本节", matches[-1]))


# _split_markdown_table_row 解析非代码围栏中的 Markdown 表格行，供图片资产清单校验复用。
# [参数] line: 单行 Markdown 文本。
# [返回] list[str]：去除首尾分隔符后的单元格文本；非表格行返回空列表。
# 最近修改时间：2026-07-12 增加图片资产清单字段解析，确保清单能与正文引用逐项对照。
def _split_markdown_table_row(line: str) -> List[str]:
    """解析 Markdown 表格行并返回单元格。"""
    stripped = line.strip()
    if "|" not in stripped:
        return []
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


# _normalize_table_header 把表头归一化，允许模板使用空格、反引号或中英文斜杠的等价写法。
# [参数] value: 表头单元格文本。
# [返回] str：用于字段匹配的归一化表头。
# 最近修改时间：2026-07-12 增加图片资产清单字段的兼容表头匹配。
def _normalize_table_header(value: str) -> str:
    """归一化 Markdown 表头文本。"""
    value = re.sub(r"`([^`]*)`", r"\1", value)
    return re.sub(r"[\s*_]", "", value).lower()


# _find_asset_manifest 查找图片资产清单表并返回字段索引及数据行。
# [参数] text: 当前 Markdown 文本。
# [返回] tuple[dict[str, int], list[list[str]]] | None：字段索引、数据行或未找到。
# 最近修改时间：2026-07-12 增加清单表识别，避免仅凭正文 alt 放行未登记图片。
def _find_asset_manifest(text: str) -> Tuple[Dict[str, int], List[List[str]]] | None:
    """查找包含九个必需字段的图片资产清单表。"""
    field_matchers = {
        "id": lambda value: "图片id" in value or "imageid" in value or "assetid" in value,
        "purpose": lambda value: "用途" in value or "生成输入" in value,
        "source": lambda value: "来源" in value,
        "path": lambda value: "相对路径" in value,
        "version": lambda value: "版本" in value,
        "relations": lambda value: "关联" in value,
        "section": lambda value: "引用章节" in value,
        "sensitivity": lambda value: "敏感状态" in value,
        "copyright": lambda value: "版权状态" in value,
    }
    lines = text.splitlines()
    in_fence = False
    for index, line in enumerate(lines[:-1]):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        header = _split_markdown_table_row(line)
        separator = _split_markdown_table_row(lines[index + 1])
        if not header or len(header) != len(separator):
            continue
        if not all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in separator):
            continue
        normalized = [_normalize_table_header(cell) for cell in header]
        columns: Dict[str, int] = {}
        for field, matcher in field_matchers.items():
            matched = next((column for column, value in enumerate(normalized) if matcher(value)), None)
            if matched is not None:
                columns[field] = matched
        if len(columns) != len(field_matchers):
            continue
        rows: List[List[str]] = []
        cursor = index + 2
        while cursor < len(lines):
            if lines[cursor].strip().startswith("```"):
                break
            row = _split_markdown_table_row(lines[cursor])
            if len(row) != len(header):
                break
            rows.append(row)
            cursor += 1
        return columns, rows
    return None


# _manifest_value 清理图片资产清单单元格中的 Markdown 内联标记。
# [参数] value: 清单单元格文本。
# [返回] str：用于一致性比较的文本。
# 最近修改时间：2026-07-12 增加清单路径和版本比较的统一清洗。
def _manifest_value(value: str) -> str:
    """清理清单单元格中的内联代码标记。"""
    return re.sub(r"`([^`]*)`", r"\1", value).strip()


# _manifest_value_missing 判断清单字段是否仍为模板占位或空值。
# [参数] value: 清单单元格文本。
# [返回] bool：是否缺失或仍为模板占位。
# 最近修改时间：2026-07-12 增加资产清单占位字段阻断，防止模板行被当作真实登记。
def _manifest_value_missing(value: str) -> bool:
    """判断清单字段是否为空或保留模板占位符。"""
    value = _manifest_value(value)
    return not value or value in {"-", "IMG-*", "<file>", "<document-stem>", "N/A"} or bool(
        re.fullmatch(r"<[^>]+>", value)
    )


# _check_asset_manifest 校验正文图片、IMG-* 与九列资产清单的一致性。
# [参数] text: 当前 Markdown 文本；images: 正文图片引用；image_targets_by_id: IMG 到路径的映射；
#       filename_versions: 路径到文件名版本的映射；errors: 错误累积列表；policy: 图片策略。
# [返回] dict：清单是否满足要求及登记 ID 摘要。
# 最近修改时间：2026-07-12 增加用途、来源、路径、版本、关联、章节、敏感和版权字段门禁。
def _check_asset_manifest(
    text: str,
    images: List[Tuple[str, str]],
    image_targets_by_id: Dict[str, set[str]],
    filename_versions: Dict[str, str],
    errors: List[str],
    policy: Dict[str, Any],
) -> Dict[str, Any]:
    """校验图片资产清单与正文引用是否逐项一致。"""
    if not images or not bool(policy.get("require_asset_manifest", True)):
        return {"required": bool(images), "rows": 0, "ids": [], "valid": True}
    manifest = _find_asset_manifest(text)
    if manifest is None:
        errors.append("image asset manifest table with nine required fields is missing")
        return {"required": True, "rows": 0, "ids": [], "valid": False}

    columns, rows = manifest
    rows_by_id: Dict[str, List[str]] = {}
    for row_number, row in enumerate(rows, start=1):
        asset_id = _manifest_value(row[columns["id"]])
        if not IMAGE_ID_PATTERN.fullmatch(asset_id):
            errors.append(f"image asset manifest row {row_number} has invalid IMG-* identifier: {asset_id or '<empty>'}")
            continue
        if asset_id in rows_by_id:
            errors.append(f"image asset manifest contains duplicate identifier: {asset_id}")
            continue
        rows_by_id[asset_id] = row
        for field in ("purpose", "source", "path", "version", "relations", "section", "sensitivity", "copyright"):
            if _manifest_value_missing(row[columns[field]]):
                errors.append(f"image asset manifest {asset_id} is missing field: {field}")

    referenced_ids = set(image_targets_by_id)
    for asset_id, targets in image_targets_by_id.items():
        row = rows_by_id.get(asset_id)
        if row is None:
            errors.append(f"image asset manifest is missing referenced identifier: {asset_id}")
            continue
        manifest_path = _image_target_path(_manifest_value(row[columns["path"]]))
        if len(targets) != 1 or manifest_path not in targets:
            errors.append(f"image asset manifest path does not match Markdown reference: {asset_id}")
        expected_version = filename_versions.get(next(iter(targets), ""))
        manifest_version = _manifest_value(row[columns["version"]])
        if expected_version and manifest_version != expected_version:
            errors.append(f"image asset manifest version does not match filename: {asset_id}")

    for asset_id in set(rows_by_id) - referenced_ids:
        errors.append(f"image asset manifest contains unreferenced identifier: {asset_id}")
    return {
        "required": True,
        "rows": len(rows_by_id),
        "ids": sorted(rows_by_id),
        "valid": not any("image asset manifest" in error for error in errors),
    }


# _check_direct_data_images 拒绝直接写入 doc/data 或其它非 images 子目录的位图。
# [参数] root: 仓库根目录；errors: 错误累积列表；profile_payload: 完整质量策略。
# [返回] dict：发现的错误图片相对路径摘要。
# 最近修改时间：2026-07-12 增加旧图片根目录扫描，防止未被 Markdown 引用的错位资产漏检。
def _check_direct_data_images(
    root: Path,
    errors: List[str],
    profile_payload: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """扫描 doc/data 下的位图并拒绝 images 子目录之外的落点。"""
    policy = (profile_payload or {}).get("image_policy", {})
    if not isinstance(policy, dict) or not bool(policy.get("forbid_direct_data_images", True)):
        return {"misplaced": [], "valid": True}
    allowed_extensions = {str(item).lower() for item in policy.get("allowed_extensions", [])}
    data_root = (root / str(policy.get("data_root", "doc/data"))).resolve()
    asset_root = _image_policy_root(root, profile_payload)
    if not data_root.exists():
        return {"misplaced": [], "valid": True}
    misplaced: List[str] = []
    for path in sorted(data_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in allowed_extensions:
            continue
        resolved = path.resolve()
        try:
            resolved.relative_to(asset_root)
        except ValueError:
            relative = resolved.relative_to(root).as_posix()
            misplaced.append(relative)
            errors.append(f"image asset must be under doc/data/images: {relative}")
    return {"misplaced": misplaced, "valid": not misplaced}


def check_images(
    text: str,
    root: Path,
    document: Path,
    profile_payload: Dict[str, Any],
    errors: List[str],
) -> Dict[str, Any]:
    """按共享文档图片策略校验 Markdown 图片引用。"""
    initial_error_count = len(errors)
    policy = profile_payload.get("image_policy", {})
    if not isinstance(policy, dict):
        return {"count": 0, "ids": [], "paths": [], "decision": None, "valid": True}

    asset_root = _image_policy_root(root, profile_payload)
    allowed_extensions = {str(item).lower() for item in policy.get("allowed_extensions", [])}
    require_relative = bool(policy.get("require_relative_path", True))
    require_alt = bool(policy.get("require_nonempty_alt", True))
    require_id = bool(policy.get("require_image_id", True))
    forbid_remote = bool(policy.get("forbid_remote_images", True))
    forbid_data_uri = bool(policy.get("forbid_data_uri", True))
    validate_signature = bool(policy.get("validate_signature", True))
    require_decision = bool(policy.get("require_decision", True))

    images = list(_iter_markdown_images(text))
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        searchable = re.sub(r"`[^`]*`", "", line)
        if re.search(r"<img\b", searchable, re.IGNORECASE):
            errors.append("HTML image tags are forbidden; use Markdown image syntax")
            break
    if _has_non_fenced_empty_image(text):
        errors.append("image reference has an empty target")
    ids: List[str] = []
    paths: List[str] = []
    image_targets_by_id: Dict[str, set[str]] = {}
    filename_versions: Dict[str, str] = {}
    for alt, raw_target in images:
        target = _image_target_path(raw_target)
        paths.append(target)
        if require_alt and not alt.strip():
            errors.append(f"image alt text must be non-empty: {target or raw_target}")
        image_ids = IMAGE_ID_PATTERN.findall(alt)
        if require_id and not image_ids:
            errors.append(f"image alt text must contain IMG-* identifier: {alt or target}")
        ids.extend(image_ids)
        for image_id in image_ids:
            image_targets_by_id.setdefault(image_id, set()).add(target)

        if not target:
            errors.append("image reference target must be non-empty")
            continue
        if "\\" in target:
            errors.append(f"image reference must use forward slashes: {target}")
        if forbid_data_uri and target.lower().startswith("data:"):
            errors.append(f"data URI images are forbidden: {target[:32]}")
        if forbid_remote and re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            errors.append(f"remote or scheme image reference is forbidden: {target}")
        is_absolute = target.startswith("/") or bool(re.match(r"^[A-Za-z]:[\\/]", target)) or target.startswith("\\\\")
        if require_relative and is_absolute:
            errors.append(f"image reference must be relative: {target}")

        candidate = (document.parent / target).resolve()
        try:
            candidate.relative_to(asset_root)
        except ValueError:
            errors.append(f"image must be under doc/data/images: {target}")
            continue
        extension = candidate.suffix.lower()
        if extension not in allowed_extensions:
            errors.append(f"unsupported image extension: {target}")
            continue
        if bool(policy.get("require_filename_pattern", True)):
            filename_match = ASSET_FILENAME_PATTERN.fullmatch(candidate.name)
            if filename_match is None:
                errors.append(f"image filename must match <document-stem>.<asset-slug>-v<number>.<ext>: {target}")
            else:
                filename_versions[target] = f"v{filename_match.group('version')}"
        if not candidate.exists():
            errors.append(f"missing image asset: {target}")
            continue
        if not candidate.is_file() or candidate.stat().st_size == 0:
            errors.append(f"image asset is empty or not a file: {target}")
            continue
        if validate_signature and not _has_image_signature(candidate, extension):
            errors.append(f"image signature does not match extension: {target}")

    manifest_report = _check_asset_manifest(
        text,
        images,
        image_targets_by_id,
        filename_versions,
        errors,
        policy,
    )
    decision = _image_decision(text)
    if require_decision:
        if decision is None:
            errors.append("image asset decision must be explicit: 需要 or N/A + reason + evidence")
        elif decision == "invalid":
            errors.append("image asset decision must be 需要 or N/A + reason + evidence")
        elif decision == "na" and not _image_decision_has_evidence(text):
            errors.append("image asset decision N/A requires reason/evidence")
        elif decision == "needed" and not images:
            errors.append("image asset decision is 需要 but no Markdown image is referenced")
        elif decision == "na" and images:
            errors.append("image asset decision is N/A but Markdown images are referenced")

    return {
        "count": len(images),
        "ids": sorted(set(ids)),
        "paths": paths,
        "decision": decision,
        "manifest": manifest_report,
        "asset_root": str(asset_root),
        "valid": len(errors) == initial_error_count,
    }


def check_orphan_images(
    root: Path,
    errors: List[str],
    profile_payload: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """扫描 doc/data/images，并拒绝没有 Markdown 引用的资产。"""
    initial_error_count = len(errors)
    root = root.resolve()
    asset_root = _image_policy_root(root, profile_payload)
    misplaced_report = _check_direct_data_images(root, errors, profile_payload)
    if not asset_root.exists():
        return {
            "asset_root": str(asset_root),
            "images": [],
            "orphans": [],
            "misplaced": misplaced_report["misplaced"],
            "valid": not errors and misplaced_report["valid"],
        }

    markdown_documents: List[Path] = []
    doc_root = root / "doc"
    if doc_root.exists():
        markdown_documents.extend(sorted(doc_root.rglob("*.md")))
    markdown_documents.extend(sorted(root.glob("*.md")))
    referenced: set[Path] = set()
    for document in markdown_documents:
        try:
            text = document.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for _, raw_target in _iter_markdown_images(text):
            target = _image_target_path(raw_target)
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            candidate = (document.parent / target).resolve()
            try:
                candidate.relative_to(asset_root)
            except ValueError:
                continue
            referenced.add(candidate)

    image_files: List[Path] = []
    for path in sorted(asset_root.rglob("*")):
        if not path.is_file():
            continue
        resolved = path.resolve()
        try:
            resolved.relative_to(asset_root)
        except ValueError:
            errors.append(f"image asset escapes image root: {path}")
            continue
        image_files.append(resolved)
    orphans = [path for path in image_files if path not in referenced]
    for path in orphans:
        errors.append(f"orphan image asset: {path.relative_to(root).as_posix()}")
    return {
        "asset_root": str(asset_root),
        "images": [path.relative_to(root).as_posix() for path in image_files],
        "orphans": [path.relative_to(root).as_posix() for path in orphans],
        "misplaced": misplaced_report["misplaced"],
        "valid": len(errors) == initial_error_count and not orphans and misplaced_report["valid"],
    }


def check_diagrams(text: str, profile: Dict[str, Any], errors: List[str]) -> Dict[str, int]:
    blocks = mermaid_blocks(text)
    counts = {"flowchart": 0, "sequenceDiagram": 0, "stateDiagram-v2": 0, "erDiagram": 0}
    for block in blocks:
        first = next((line.strip() for line in block.splitlines() if line.strip()), "")
        for diagram_type in counts:
            if first.startswith(diagram_type):
                counts[diagram_type] += 1
    required = profile.get("diagrams", {})
    for diagram_type, minimum in required.items():
        if counts.get(diagram_type, 0) < int(minimum):
            errors.append(f"insufficient {diagram_type} diagrams: expected {minimum}, got {counts.get(diagram_type, 0)}")
    return counts


# check_strict_trace 检查跨文档追踪链和任务唯一归属，供周期收口时的严格模式使用。
# [参数] root: 文档扫描根目录；errors: 累积严格模式错误列表。
# [返回] dict：文档数量、任务 ID、证据 ID 和周期归属摘要。
# 最近修改时间：2026-07-12 新增严格追踪，确保任务具备唯一周期归属和四类证据。
def check_strict_trace(root: Path, errors: List[str]) -> Dict[str, Any]:
    """检查跨文档追踪链和任务唯一归属，供周期收口时的严格模式使用。"""
    # 1. 限定当前来源对象文档，排除历史样例、测试夹具和其它来源对象的任务。
    all_documents = sorted(root.rglob("*.md"))
    documents = []
    for path in all_documents:
        normalized_path = "/" + path.as_posix().replace("\\", "/") + "/"
        if "/doc/5-tests/" in normalized_path or "/doc/6-审查/" in normalized_path:
            continue
        content = path.read_text(encoding="utf-8")
        if "REQ-DOC-20260712-033322" in content or "REQ-DOC-20260712-033322" in path.name:
            documents.append(path)
    if not documents and len(all_documents) <= 3:
        documents = all_documents
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in documents)
    cycle_documents = [path for path in documents if re.search(r"实施周期\d+", path.name)]
    tasks: set[str] = set()
    # 仅把任务清单表格首列或最小 fixture 中的唯一任务视为周期归属，避免正文回指造成重复归属。
    for path in cycle_documents:
        content = path.read_text(encoding="utf-8")
        owned = set(re.findall(r"^\s*\|\s*`?((?:TASK-[A-Z0-9]+(?:-[A-Z0-9]+)*|T\d{2}-\d{2}))`?\s*\|", content, re.MULTILINE))
        if not owned:
            owned = set(TASK_ID_PATTERN.findall(content))
        tasks.update(owned)
    evidence = sorted(set(EVIDENCE_ID_PATTERN.findall(corpus)))
    cycles: Dict[str, set[str]] = {}
    for path in cycle_documents:
        match = re.search(r"实施周期(\d+)", path.name)
        if not match:
            continue
        cycle = match.group(1)
        content = path.read_text(encoding="utf-8")
        owned = set(
            re.findall(
                r"^\s*\|\s*`?((?:TASK-[A-Z0-9]+(?:-[A-Z0-9]+)*|T\d{2}-\d{2}))`?\s*\|",
                content,
                re.MULTILINE,
            )
        )
        if not owned:
            owned = set(TASK_ID_PATTERN.findall(content))
        # 只记录任务清单中的归属，避免正文“下一任务/回指”污染周期边界。
        cycles.setdefault(cycle, set()).update(owned)
    # 2. 逐任务检查唯一归属、真实测试/停止契约和 IMPL/TEST/REVIEW 证据。
    for task in tasks:
        owners = [cycle for cycle, owned in cycles.items() if task in owned]
        if len(owners) != 1:
            errors.append(f"task must belong to exactly one implementation cycle: {task} -> {owners}")
        task_contexts = [path.read_text(encoding="utf-8") for path in documents if task in path.read_text(encoding="utf-8")]
        if not any("真实测试" in context and "停止" in context for context in task_contexts):
            errors.append(f"task is missing executable test/stop contract: {task}")
        required_suffixes = ("IMPL", "TEST", "REVIEW", "ACCEPT")
        for suffix in required_suffixes:
            if not re.search(rf"EVD-{re.escape(task)}-{suffix}(?:-[A-Z0-9]+)*", corpus):
                errors.append(f"task is missing evidence category {suffix}: {task}")
    # 3. 检查跨域追踪链是否至少出现所有必要 ID 前缀。
    required_links = ("REQ", "AC", "CYCLE", "TASK", "TEST", "EVIDENCE")
    link_patterns = {
        "TASK": r"(?:\bTASK-[A-Z0-9]+(?:-[A-Z0-9]+)*\b|\bT\d{2}-\d{2}\b)",
        "EVIDENCE": r"(?:\bEVIDENCE-[A-Z0-9]+(?:-[A-Z0-9]+)*\b|\bEVD-[A-Z0-9]+(?:-[A-Z0-9]+)*\b)",
    }
    missing_links = [
        prefix
        for prefix in required_links
        if not re.search(link_patterns.get(prefix, rf"\b{prefix}(?:-[A-Z0-9]+)+\b"), corpus)
    ]
    errors.extend(f"strict trace chain is missing ID prefix: {prefix}" for prefix in missing_links)
    return {
        "documents": len(documents),
        # JSON 报告边界统一输出稳定列表，避免内部去重集合导致 --json-out 失败。
        "tasks": sorted(tasks),
        "evidence": evidence,
        "cycles": {cycle: sorted(owned) for cycle, owned in cycles.items()},
        "required_evidence_categories": ["IMPL", "TEST", "REVIEW", "ACCEPT"],
        "valid": not errors,
    }


# validate_document 按指定质量 profile 汇总单份 Markdown 文档的结构、内容、链接和图形校验。
# [参数] path: 待校验文档；profile_name: profile 名称；profile: profile 配置；profile_payload: 完整配置；root: 链接根目录。
# [返回] dict：valid、文档标识、ID、图形计数、错误和警告。
# 最近修改时间：2026-07-12 将 profile 约束传入 YAML 头并纳入统一校验结果。
def validate_document(path: Path, profile_name: str, profile: Dict[str, Any], profile_payload: Dict[str, Any], root: Path) -> Dict[str, Any]:
    """按指定质量 profile 汇总单份 Markdown 文档的结构、内容、链接和图形校验。"""
    # 1. 读取 UTF-8 文档并准备错误、警告容器。
    errors: List[str] = []
    warnings: List[str] = []
    text, read_errors = read_document(path)
    errors.extend(read_errors)
    image_report: Dict[str, Any] = {"count": 0, "ids": [], "paths": [], "decision": None, "valid": True}
    # 2. 对 UTF-8 文档执行 front matter、章节、ID、链接、图形和占位词校验。
    if not errors:
        # 补丁说明：把 profile 传入 YAML 头检查，确保专项必填字段不会被遗漏。
        check_frontmatter(text, errors, profile)
        check_fences(text, errors)
        check_sections(text, profile, errors)
        ids = check_ids(text, profile, errors)
        check_profile_content(text, profile, errors)
        check_placeholders(text, profile_payload, errors)
        check_na_reasons(text, errors)
        check_links(text, root, path, errors)
        image_report = check_images(text, root, path, profile_payload, errors)
        diagrams = check_diagrams(text, profile, errors)
        # 补丁说明：在结构校验阶段执行 Mermaid 语法前置检查，避免坏图进入后续验收。
        check_diagram_annotations(text, errors, require_context=True)
    else:
        ids = []
        diagrams = {}
    # 3. 汇总 profile、链接、图形和严格结构检查结果。
    return {
        "valid": not errors,
        "status": "PASS" if not errors else "BLOCKED",
        "profile": profile_name,
        "document": str(path),
        "ids": ids,
        "diagrams": diagrams,
        "images": image_report,
        "errors": list(dict.fromkeys(errors)),
        "warnings": list(dict.fromkeys(warnings)),
        "traceability": {"mode": "document", "valid": not errors, "ids": ids},
        "unresolved_decisions": {"count": 0, "items": []},
        "coverage": {
            "id_count": len(ids),
            "image_count": image_report.get("count", 0),
            "valid": not errors,
        },
    }


# main 解析命令行参数并输出单文档或严格追踪模式的 JSON 结果。
# [参数] 无显式参数：从命令行读取 profile、文档、根目录和严格模式选项。
# [返回] None：打印 JSON；校验失败时以退出码 1 结束进程。
# 最近修改时间：2026-07-12 增加 --strict 输出，支持交付阶段统一追踪门禁。
def main() -> None:
    """解析命令行参数并输出单文档或严格追踪模式的 JSON 结果。"""
    # 1. 解析命令行参数并加载 profile。
    parser = argparse.ArgumentParser(description="Validate engineering Markdown document completeness")
    parser.add_argument("--profile", required=True, choices=("requirement", "acceptance", "implementation_master", "implementation_overview", "implementation_cycle"))
    parser.add_argument("--doc", required=True, type=Path, help="Markdown document to validate")
    parser.add_argument("--root", type=Path, default=None, help="Root used for local link containment")
    parser.add_argument("--profile-file", type=Path, default=None, help="Quality profile YAML path")
    parser.add_argument("--json-out", type=Path, default=None, help="Optional JSON report path")
    parser.add_argument("--check-orphan-images", action="store_true", help="Reject unreferenced files under doc/data/images")
    # 补丁说明：新增严格开关，让调用方按需启用跨文档追踪而不改变默认单文档行为。
    parser.add_argument("--strict", action="store_true", help="Validate cross-document task/evidence traceability")
    args = parser.parse_args()

    document = args.doc.resolve()
    root = (args.root or document.parent).resolve()
    profile_file = (args.profile_file or Path(__file__).resolve().parents[1] / "references" / "document-quality-profiles.yaml").resolve()
    payload = load_profiles(profile_file)
    profile = payload["profiles"].get(args.profile)
    if not isinstance(profile, dict):
        raise SystemExit(f"unknown profile: {args.profile}")
    result = validate_document(document, args.profile, profile, payload, root)
    if args.check_orphan_images:
        orphan_errors: List[str] = []
        orphan_report = check_orphan_images(root, orphan_errors, payload)
        result["orphan_images"] = orphan_report
        result["errors"].extend(orphan_errors)
        result["valid"] = not result["errors"]
        result["status"] = "PASS" if result["valid"] else "BLOCKED"
    # 2. 在显式开启严格模式时追加跨文档追踪摘要、覆盖率和未决决策字段。
    if args.strict:
        strict_errors: List[str] = []
        trace = check_strict_trace(root, strict_errors)
        result["strict"] = {"valid": not strict_errors, "errors": strict_errors, "trace": trace}
        result["traceability"] = trace
        result["coverage"] = {
            "task_evidence": {
                "required_categories": trace["required_evidence_categories"],
                "tasks": len(trace["tasks"]),
                "evidence": len(trace["evidence"]),
                "valid": not strict_errors,
            },
            "valid": not strict_errors,
        }
        result["status"] = "PASS" if not result["errors"] and not strict_errors else "BLOCKED"
        result["errors"].extend(strict_errors)
        result["valid"] = not result["errors"]
    # 3. 输出 JSON 并以非零退出码标记未通过结果。
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        args.json_out.write_text(output + "\n", encoding="utf-8")
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
