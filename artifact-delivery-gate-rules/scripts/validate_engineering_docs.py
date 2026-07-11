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
)
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*$")
FENCE_PATTERN = re.compile(r"^\s*```([\w-]*)\s*$")
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


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
    return [match.group(1).strip() for line in text.splitlines() if (match := HEADING_PATTERN.match(line))]


def section_bodies(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    sections: Dict[str, List[str]] = {}
    current = ""
    for line in lines:
        match = HEADING_PATTERN.match(line)
        if match:
            current = match.group(1).strip()
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


def check_frontmatter(text: str, errors: List[str]) -> None:
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
    for field in ("schema_version", "doc_id", "doc_type", "source_ids", "status", "version", "current_slice", "updated_at"):
        value = metadata.get(field)
        if value in (None, "", []):
            errors.append(f"front matter missing non-empty field: {field}")


def check_fences(text: str, errors: List[str]) -> None:
    fences = [line for line in text.splitlines() if line.strip().startswith("```")]
    if len(fences) % 2:
        errors.append("unclosed Markdown code fence")


def check_sections(text: str, profile: Dict[str, Any], errors: List[str]) -> None:
    existing = set(headings(text))
    bodies = section_bodies(text)
    for section in profile.get("required_sections", []):
        if section not in existing:
            errors.append(f"missing required section: {section}")
        elif not bodies.get(section):
            errors.append(f"required section is empty: {section}")


def check_ids(text: str, profile: Dict[str, Any], errors: List[str]) -> List[str]:
    ids = ID_PATTERN.findall(text)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append(f"duplicate stable IDs: {duplicates}")
    prefixes = tuple(f"{prefix}-" for prefix in profile.get("id_prefixes", []))
    if prefixes and not any(item.startswith(prefixes) for item in ids):
        errors.append(f"no IDs found for profile prefixes: {list(prefixes)}")
    return sorted(set(ids))


def check_placeholders(text: str, payload: Dict[str, Any], errors: List[str]) -> None:
    lowered = text.lower()
    hits = [term for term in payload.get("placeholder_terms", []) if term.lower() in lowered]
    if hits:
        errors.append(f"placeholder or vague terms found: {sorted(set(hits))}")


def check_na_reasons(text: str, errors: List[str]) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.search(r"\bN/A\b|不适用", line) and not re.search(r"原因|证据|依据", line):
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


def validate_document(path: Path, profile_name: str, profile: Dict[str, Any], profile_payload: Dict[str, Any], root: Path) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    text, read_errors = read_document(path)
    errors.extend(read_errors)
    if not errors:
        check_frontmatter(text, errors)
        check_fences(text, errors)
        check_sections(text, profile, errors)
        ids = check_ids(text, profile, errors)
        check_placeholders(text, profile_payload, errors)
        check_na_reasons(text, errors)
        check_links(text, root, path, errors)
        diagrams = check_diagrams(text, profile, errors)
    else:
        ids = []
        diagrams = {}
    return {
        "valid": not errors,
        "profile": profile_name,
        "document": str(path),
        "ids": ids,
        "diagrams": diagrams,
        "errors": list(dict.fromkeys(errors)),
        "warnings": list(dict.fromkeys(warnings)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate engineering Markdown document completeness")
    parser.add_argument("--profile", required=True, choices=("requirement", "acceptance", "implementation_overview", "implementation_cycle"))
    parser.add_argument("--doc", required=True, type=Path, help="Markdown document to validate")
    parser.add_argument("--root", type=Path, default=None, help="Root used for local link containment")
    parser.add_argument("--profile-file", type=Path, default=None, help="Quality profile YAML path")
    parser.add_argument("--json-out", type=Path, default=None, help="Optional JSON report path")
    args = parser.parse_args()

    document = args.doc.resolve()
    root = (args.root or document.parent).resolve()
    profile_file = (args.profile_file or Path(__file__).resolve().parents[1] / "references" / "document-quality-profiles.yaml").resolve()
    payload = load_profiles(profile_file)
    profile = payload["profiles"].get(args.profile)
    if not isinstance(profile, dict):
        raise SystemExit(f"unknown profile: {args.profile}")
    result = validate_document(document, args.profile, profile, payload, root)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        args.json_out.write_text(output + "\n", encoding="utf-8")
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
