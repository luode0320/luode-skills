#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 prompts/ 重建 data/index.json。

索引是纯派生产物，每次全量重写；人工标注请写 data/tags.json，不被本脚本覆盖。
用法：
    python build_index.py            # 重建索引
    python build_index.py --check    # 只校验路由表候选文件是否齐全
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = SKILL_DIR / "prompts"
DATA_DIR = SKILL_DIR / "data"
INDEX_FILE = DATA_DIR / "index.json"
ROUTING_FILE = DATA_DIR / "model-routing.json"
SOURCES_FILE = DATA_DIR / "sources.json"

PROMPT_SUFFIXES = {".md", ".txt"}

# 载体判定：命中第一条即返回，顺序即优先级
KIND_RULES = [
    ("ollama_modelfile", lambda name, text: bool(re.search(r"(?m)^FROM\s+\S", text))),
    ("harness_config", lambda name, text: name.endswith(".txt") or "<CFG>" in text),
    ("agents_md", lambda name, text: bool(re.search(r"(?m)^#\s*AGENTS\.md", text))),
    ("register_block", lambda name, text: "### REGISTER" in text or "### PRECEDENCE" in text),
    # 人格锁：以 thinking 标记开头并要求身份不可质疑
    ("persona_lock", lambda name, text: ("<thinking>" in text or "<thinking> tags" in text)
        and ("persona" in text.lower() or "[MaHii]" in text or "[V]" in text)),
    # 对话式铺垫：以「在开始合作前我想先说说我怎么工作」开场
    ("conversation_persona", lambda name, text: re.search(
        r"(?m)^(aa)?\s*(Hey — )?I want to (share|tell|lay)", text) is not None),
    ("system_prompt", lambda name, text: "large language model developed by" in text
        or re.search(r"(?m)^SYSTEM:\s*$", text) is not None),
    ("workspace_policy", lambda name, text: any(k in text for k in (
        "# Operating Policy", "Assistant Operating Specification",
        "Workspace Operating Profile", "Agent Operating Instructions",
        "Agent Deployment Operating Policy", "workspace guide"))),
    ("system_prompt", lambda name, text: re.search(r"(?m)^Mistral .*System Prompt", text) is not None),
    ("system_prompt", lambda name, text: "Knowledge cutoff:" in text and "You are" in text),
    # 其余以运行时注入块开头的变体
    ("runtime_variant", lambda name, text: text.lstrip().startswith(("<system-reminder>", "<system>"))),
]

# 厂商判定：按文件名与正文关键词，先命中者为准
VENDOR_RULES = [
    ("anthropic", ("opus", "sonnet", "claude")),
    ("openai", ("gpt", "chatgpt")),
    ("google", ("gemini", "gemma")),
    ("xai", ("grok",)),
    ("deepseek", ("deepseek",)),
    ("moonshot", ("kimi", "moonshot")),
    ("zhipu", ("glm", "zcode", "chatglm")),
    ("alibaba", ("qwen",)),
    ("mistral", ("mistral",)),
    ("nvidia", ("nemotron",)),
    ("stepfun", ("step 5", "step-5")),
    ("longcat", ("longcat",)),
    ("xiaomi", ("mimo",)),
    ("muse", ("muse",)),
    ("opencode", ("spacebunny", "space bunny", "bigpickle", "big pickle", "vanta")),
    ("any", ("unified", "beam", "hy4", "operating policy")),
]

# 提示词手法特征词，用于检索与人工挑选。
# 判据只收强特征：裸词（如 persona）在官方系统提示里普遍出现，会把标记稀释成噪音。
TECHNIQUE_MARKERS = {
    "persona_lock": ("[MaHii]", "VANTA", "You are SMITH", "Persona lock", "persona lock"),
    "reply_prefix": ("Every reply opens with", "Jack:"),
    "precedence_claim": ("outranks", "This block wins", "SUPERSESSION"),
    "boundary_list": ("Boundaries", "the only line is"),
    "no_disclaimer": ("no content warnings", "no disclaimers", "educational purposes only"),
    "thinking_marker": ("<thinking>",),
    "system_reminder": ("<system-reminder>",),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_json_atomic(path: Path, payload: dict) -> None:
    """先写临时文件再原子替换。

    直接 write_text 时，写到一半被并发读会拿到残缺 JSON；
    os.replace 在同一卷上是原子操作，读方要么看到旧文件，要么看到完整新文件。
    """
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    os.replace(temp_path, path)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def detect_kind(name: str, text: str) -> str:
    lowered = name.lower()
    for kind, rule in KIND_RULES:
        if rule(lowered, text):
            return kind
    return "other"


def detect_vendor(name: str, text: str) -> str:
    haystack = (name + "\n" + text[:2000]).lower()
    for vendor, keys in VENDOR_RULES:
        if any(key in haystack for key in keys):
            return vendor
    return "unknown"


def detect_techniques(text: str) -> list[str]:
    hits = []
    for tag, keys in TECHNIQUE_MARKERS.items():
        if any(key in text for key in keys):
            hits.append(tag)
    return sorted(hits)


def summarize(text: str) -> str:
    for line in text.splitlines():
        clean = line.strip().lstrip("#").strip()
        if clean and not clean.startswith("<"):
            return clean[:120]
    return "（空文件）"


def iter_prompts() -> list[Path]:
    if not PROMPTS_DIR.exists():
        return []
    return sorted(p for p in PROMPTS_DIR.iterdir() if p.is_file() and p.suffix.lower() in PROMPT_SUFFIXES)


def load_routing() -> dict:
    if not ROUTING_FILE.exists():
        return {"families": []}
    return json.loads(read_text(ROUTING_FILE))


def build_entries() -> list[dict]:
    entries = []
    for path in iter_prompts():
        text = read_text(path)
        entries.append({
            "file": path.name,
            "kind": detect_kind(path.name, text),
            "vendor": detect_vendor(path.name, text),
            "bytes": path.stat().st_size,
            "lines": len(text.splitlines()),
            "sha256": sha256_of(path),
            "summary": summarize(text),
            "techniques": detect_techniques(text),
            "empty": path.stat().st_size < 16,
        })
    return entries


def attach_families(entries: list[dict], routing: dict) -> dict:
    by_file = {entry["file"]: entry for entry in entries}
    family_files: set[str] = set()
    for family in routing.get("families", []):
        resolved = [c for c in family.get("candidates", []) if c in by_file]
        family["resolved_files"] = resolved
        family["missing_files"] = [c for c in family.get("candidates", []) if c not in by_file]
        for name in resolved:
            family_files.add(name)
            by_file[name].setdefault("families", []).append(family["id"])
    return {"unrouted": sorted(set(by_file) - family_files)}


def build_duplicates(entries: list[dict]) -> list[dict]:
    groups: dict[str, list[str]] = {}
    for entry in entries:
        groups.setdefault(entry["sha256"], []).append(entry["file"])
    return [
        {"sha256": digest[:12], "files": files}
        for digest, files in groups.items() if len(files) > 1
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="重建 pojia 提示词索引")
    parser.add_argument("--check", action="store_true", help="只校验路由表候选文件是否齐全")
    args = parser.parse_args()

    routing = load_routing()
    entries = build_entries()
    meta = attach_families(entries, routing)
    duplicates = build_duplicates(entries)

    if args.check:
        missing = [
            f'{family["id"]}: {name}'
            for family in routing.get("families", [])
            for name in family.get("missing_files", [])
        ]
        print(f"PROMPTS={len(entries)} FAMILIES={len(routing.get('families', []))} UNROUTED={len(meta['unrouted'])}")
        if missing:
            print("MISSING_CANDIDATES:")
            for item in missing:
                print("  " + item)
            return 1
        print("ROUTING: PASS")
        return 0

    payload = {
        "skill": "pojia",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "prompt_count": len(entries),
        "total_bytes": sum(entry["bytes"] for entry in entries),
        "families": routing.get("families", []),
        "unrouted_files": meta["unrouted"],
        "duplicate_groups": duplicates,
        "prompts": entries,
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    write_json_atomic(INDEX_FILE, payload)

    print(f"INDEX_WRITTEN={INDEX_FILE}")
    print(f"PROMPTS={len(entries)} FAMILIES={len(payload['families'])} "
          f"UNROUTED={len(meta['unrouted'])} DUP_GROUPS={len(duplicates)}")
    return 0


if __name__ == "__main__":
    # stdout 与 stderr 都要锁 UTF-8：SystemExit / argparse 的报错走 stderr，
    # 只改 stdout 会让中文错误在 GBK 控制台（chcp 936）上变成乱码。
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
