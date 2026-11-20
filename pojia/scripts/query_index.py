#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按模型 / 厂商 / 载体 / 关键词检索提示词语料。

数据源：data/index.json（由 build_index.py 生成）。
用法：
    python query_index.py --vendor anthropic
    python query_index.py --kind agents_md
    python query_index.py --keyword persona
    python query_index.py --technique persona_lock
    python query_index.py --stats
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = SKILL_DIR / "data" / "index.json"
PROMPTS_DIR = SKILL_DIR / "prompts"

# 正文缓存：一次查询内同一文件只读一次盘
_BODY_CACHE: dict[str, str] = {}


def load_index() -> dict:
    if not INDEX_FILE.exists():
        raise SystemExit("索引不存在，请先运行 build_index.py")
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


def load_body(entry: dict) -> str:
    """惰性读取提示词正文，按文件名缓存，避免同一文件重复读盘。"""
    name = entry.get("file", "")
    if name in _BODY_CACHE:
        return _BODY_CACHE[name]
    path = PROMPTS_DIR / name
    text = path.read_text(encoding="utf-8", errors="replace").lower() if path.is_file() else ""
    _BODY_CACHE[name] = text
    return text


def match(entry: dict, args: argparse.Namespace) -> bool:
    """按传入条件逐项过滤，未提供的条件视为通过。"""
    if args.vendor and entry.get("vendor") != args.vendor:
        return False
    if args.kind and entry.get("kind") != args.kind:
        return False
    if args.family and args.family not in entry.get("families", []):
        return False
    if args.technique and args.technique not in entry.get("techniques", []):
        return False
    if args.keyword:
        needle = args.keyword.lower()
        # 默认搜正文：文件名与摘要覆盖面太窄，搜 "reverse shell" 这类正文词会全部落空。
        haystack = entry.get("file", "") + " " + entry.get("summary", "")
        if not args.meta_only:
            haystack += " " + load_body(entry)
        if needle not in haystack.lower():
            return False
    return True


def print_rows(rows: list[dict]) -> None:
    if not rows:
        print("NO_MATCH")
        return
    print(f'{"file":<48}{"vendor":<12}{"kind":<20}{"bytes":>8}  families')
    for entry in rows:
        families = ",".join(entry.get("families", [])) or "-"
        print(f'{entry["file"]:<48}{entry["vendor"]:<12}{entry["kind"]:<20}{entry["bytes"]:>8}  {families}')


def print_stats(index: dict) -> None:
    prompts = index.get("prompts", [])
    vendors: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for entry in prompts:
        vendors[entry["vendor"]] = vendors.get(entry["vendor"], 0) + 1
        kinds[entry["kind"]] = kinds.get(entry["kind"], 0) + 1
    print(f'PROMPTS={len(prompts)} FAMILIES={len(index.get("families", []))} '
          f'DUP_GROUPS={len(index.get("duplicate_groups", []))} '
          f'UNROUTED={len(index.get("unrouted_files", []))}')
    print("BY_VENDOR: " + ", ".join(f"{k}={v}" for k, v in sorted(vendors.items(), key=lambda x: -x[1])))
    print("BY_KIND:   " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items(), key=lambda x: -x[1])))


def main() -> int:
    parser = argparse.ArgumentParser(description="检索 pojia 提示词语料")
    parser.add_argument("--vendor", help="厂商，如 anthropic / zhipu / deepseek")
    parser.add_argument("--kind", help="载体，如 system_prompt / agents_md / workspace_policy")
    parser.add_argument("--family", help="路由族 id，如 claude-opus")
    parser.add_argument("--technique", help="手法标记，如 persona_lock")
    parser.add_argument("--keyword", help="关键词包含匹配（默认搜正文，含文件名与摘要）")
    parser.add_argument("--meta-only", action="store_true", help="只搜文件名与摘要，不读正文（更快）")
    parser.add_argument("--stats", action="store_true", help="输出统计概览")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    index = load_index()
    if args.stats:
        print_stats(index)
        return 0

    rows = [entry for entry in index.get("prompts", []) if match(entry, args)]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print_rows(rows)
    return 0 if rows else 1


if __name__ == "__main__":
    # stdout 与 stderr 都要锁 UTF-8：SystemExit / argparse 的报错走 stderr，
    # 只改 stdout 会让中文错误在 GBK 控制台（chcp 936）上变成乱码。
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
