#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""模型 -> 前置提示词解析器。

解析顺序（与 data/model-routing.json 的 match_order 一致）：
    1. family_id   —— 直接点名族 id
    2. alias_exact —— 别名全等
    3. alias_contains —— 别名被查询串包含（取最长别名，避免 "gpt" 抢 "gpt-oss"）
    4. vendor_prefix —— 厂商名命中，取该厂商优先级最高的族
    5. generic_fallback —— 通用兜底链，逐份取第一份存在的文件

用法：
    python resolve_prompt.py --model claude-opus
    python resolve_prompt.py --model "Opus 4.6" --kind agents_md
    python resolve_prompt.py --model unknown-model --fallback   # 允许跨厂商兜底
    python resolve_prompt.py --list
    python resolve_prompt.py --verify                           # 自检路由表与文件一致性
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = SKILL_DIR / "prompts"
ROUTING_FILE = SKILL_DIR / "data" / "model-routing.json"

# 厂商词表：用于第 4 步 vendor_prefix 命中
VENDOR_KEYWORDS = {
    "anthropic": ("claude", "anthropic", "opus", "sonnet"),
    "openai": ("openai", "chatgpt", "gpt", "gpt-oss"),
    "google": ("google", "gemini", "gemma"),
    "xai": ("xai", "x.ai", "grok"),
    "deepseek": ("deepseek", "深度求索"),
    "moonshot": ("moonshot", "kimi", "月之暗面"),
    "zhipu": ("zhipu", "z.ai", "智谱", "glm", "zcode"),
    "alibaba": ("alibaba", "qwen", "通义", "千问"),
    "mistral": ("mistral",),
    "nvidia": ("nvidia", "nemotron"),
    "stepfun": ("stepfun", "step"),
    "longcat": ("longcat",),
    "xiaomi": ("xiaomi", "mimo"),
    "muse": ("muse",),
    "opencode": ("opencode", "bigpickle", "spacebunny"),
}


INDEX_FILE = SKILL_DIR / "data" / "index.json"


def load_routing() -> dict:
    """读取路由表。损坏时给出可定位的报错，而不是抛出裸 JSONDecodeError traceback。"""
    try:
        return json.loads(ROUTING_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"路由表不存在：{ROUTING_FILE}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"路由表 JSON 解析失败：{ROUTING_FILE}\n"
            f"  位置 第 {exc.lineno} 行第 {exc.colno} 列：{exc.msg}\n"
            f"  修复：用 git diff 检查该文件，或从 sources.json 的同版本重新生成"
        ) from exc


def load_prompt_kinds() -> dict[str, str]:
    """从索引取「文件名 -> 载体」，索引缺失时返回空表并降级为不做载体过滤。"""
    if not INDEX_FILE.exists():
        return {}
    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return {entry["file"]: entry.get("kind", "") for entry in index.get("prompts", [])}


def file_exists(name: str) -> bool:
    return (PROMPTS_DIR / name).is_file()


def pick_candidate(family: dict) -> tuple[str | None, list[str]]:
    """取族内第一份真实存在的文件，返回 (命中文件, 缺失清单)。"""
    missing = []
    for name in family.get("candidates", []):
        if file_exists(name):
            return name, missing
        missing.append(name)
    return None, missing


def normalize(value: str) -> str:
    return " ".join(value.strip().lower().split())


def match_family(query: str, routing: dict) -> tuple[dict | None, str]:
    """按 1-3 步匹配族，返回 (族, 命中的匹配方式)。"""
    q = normalize(query)
    families = routing.get("families", [])

    for family in families:
        if normalize(family.get("id", "")) == q:
            return family, "family_id"

    best_exact = None
    for family in families:
        for alias in family.get("aliases", []):
            if normalize(alias) == q:
                if best_exact is None or family.get("priority", 0) > best_exact.get("priority", 0):
                    best_exact = family
                if normalize(family.get("id", "")) == normalize(alias):
                    return family, "alias_exact"
    if best_exact is not None:
        return best_exact, "alias_exact"

    best_partial, best_len = None, 0
    for family in families:
        for alias in family.get("aliases", []):
            a = normalize(alias)
            if not a or a not in q:
                continue
            score = len(a)
            if score > best_len or (score == best_len and family.get("priority", 0) > best_partial.get("priority", 0)):
                best_partial, best_len = family, score
    if best_partial is not None:
        return best_partial, "alias_contains"

    return None, "no_alias_match"


def match_vendor(query: str, routing: dict) -> tuple[dict | None, str]:
    q = normalize(query)
    for vendor, keywords in VENDOR_KEYWORDS.items():
        if not any(keyword in q for keyword in keywords):
            continue
        pool = [f for f in routing.get("families", []) if f.get("vendor") == vendor]
        if pool:
            return max(pool, key=lambda f: f.get("priority", 0)), f"vendor_prefix:{vendor}"
    return None, "no_vendor_match"


def generic_family(routing: dict) -> dict:
    target = routing.get("generic_family", "generic")
    for family in routing.get("families", []):
        if family.get("id") == target:
            return family
    raise SystemExit("路由表缺少通用兜底族：" + target)


def build_blocked(model: str, kind: str | None, routing: dict) -> dict:
    """语义未命中时的阻断结果：不返回任何提示词，只给出下一步该怎么做。"""
    generic = generic_family(routing)
    fallback_file, _ = pick_candidate(generic)
    return {
        "model_query": model,
        "matched_family": None,
        "family_label": None,
        "vendor": None,
        "match_method": "no_match",
        "prompt_file": None,
        "prompt_file_name": None,
        "missing_candidates": [],
        "kind_preference": kind,
        "kind_note": None,
        "degraded": None,
        "note": "语料库未覆盖该模型。三步处置：① 用 --list 确认有无同厂商族可复用；"
                "② 跑 sync_upstream.py --check 看上游是否有新模型；"
                "③ 确认要先用通用提示词，再加 --fallback。",
        "suggested_fallback": fallback_file,
        "status": "NO_MATCH",
    }


def resolve(model: str, kind: str | None, allow_fallback: bool) -> dict:
    routing = load_routing()
    family, method = match_family(model, routing)
    degraded = None

    if family is None:
        family, method = match_vendor(model, routing)
        if family is None:
            if not allow_fallback:
                # 默认严格：语义匹配不到就明确阻断，不静默塞一份无关的通用提示词。
                # 这是本 skill 的判定口径——宁可报「没覆盖」，也不给错的。
                return build_blocked(model, kind, routing)
            family = generic_family(routing)
            method = "generic_fallback"
            degraded = "未匹配到任何厂商，已按 --fallback 使用通用兜底"

    chosen, missing = pick_candidate(family)

    # 载体偏好：按 index.json 里每份文件的真实 kind 再挑一次，
    # 不用文件名子串匹配——agents_md / workspace_policy 这类载体名从不出现在文件名中。
    kind_note = None
    if kind and chosen is not None:
        kinds = load_prompt_kinds()
        want = kind.lower()
        for name in family.get("candidates", []):
            if not file_exists(name):
                continue
            if kinds.get(name, "").lower() == want:
                chosen, kind_note = name, f"按载体偏好命中 {name}（kind={want}）"
                break
        if kind_note is None:
            available = sorted({kinds.get(n, "") for n in family.get("candidates", []) if file_exists(n)} - {""})
            kind_note = f"族内无 kind={want} 的候选，回退首选 {chosen}；该族可选载体：{', '.join(available) or '未知'}"

    result = {
        "model_query": model,
        "matched_family": family.get("id"),
        "family_label": family.get("label"),
        "vendor": family.get("vendor"),
        "match_method": method,
        "prompt_file": str(PROMPTS_DIR / chosen) if chosen else None,
        "prompt_file_name": chosen,
        "missing_candidates": missing,
        "kind_preference": kind,
        "kind_note": kind_note,
        "degraded": degraded,
        "note": family.get("note", ""),
    }

    if chosen is None:
        result["status"] = "BLOCKED"
        result["degraded"] = "族内候选文件全部缺失，请先运行 sync_upstream.py --apply"
    else:
        result["status"] = "OK"
    return result


def list_families() -> int:
    routing = load_routing()
    print(f'{"family":<18}{"vendor":<12}{"候选(首个存在)":<40}OK')
    for family in sorted(routing.get("families", []), key=lambda f: -f.get("priority", 0)):
        chosen, _ = pick_candidate(family)
        mark = "Y" if chosen else "N"
        print(f'{family.get("id", ""):<18}{family.get("vendor", ""):<12}{chosen or "-":<40}{mark}')
    return 0


def verify() -> int:
    routing = load_routing()
    routed = set()
    blocked = []
    for family in routing.get("families", []):
        chosen, missing = pick_candidate(family)
        if chosen is None:
            blocked.append(f'{family.get("id")}: 全部候选缺失 {missing}')
        # 统计口径：族的全部候选都算已路由，只要文件真实存在
        routed.update(name for name in family.get("candidates", []) if file_exists(name))

    prompts = {p.name for p in PROMPTS_DIR.iterdir() if p.is_file()} if PROMPTS_DIR.exists() else set()
    unrouted = sorted(prompts - routed)

    print(f"FAMILIES={len(routing.get('families', []))} PROMPTS={len(prompts)}")
    print(f"UNROUTED={len(unrouted)}")
    for name in unrouted:
        print("  unrouted: " + name)
    if blocked:
        for item in blocked:
            print("  BLOCKED: " + item)
        return 1
    print("ROUTING: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="按模型名解析前置提示词")
    parser.add_argument("--model", help="模型名，如 claude-opus / 'Opus 4.6' / glm-5.3")
    parser.add_argument("--kind", help="载体偏好关键词，如 agents_md / system_prompt")
    parser.add_argument("--fallback", action="store_true", help="允许未命中时使用通用兜底")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--list", action="store_true", help="列出全部族与候选")
    parser.add_argument("--verify", action="store_true", help="自检路由表与文件一致性")
    args = parser.parse_args()

    if args.list:
        return list_families()
    if args.verify:
        return verify()
    if not args.model:
        parser.error("需要 --model，或使用 --list / --verify")

    result = resolve(args.model, args.kind, args.fallback)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["status"] == "NO_MATCH":
        # 阻断态：不打印占位的 None，直接给可执行的下一步。
        # 模型名可能来自自动抓取，过长原样回显会淹没真正的提示信息。
        shown = result["model_query"]
        if len(shown) > 80:
            shown = shown[:77] + "..."
        print(f'[{result["status"]}] 语料库未覆盖模型：{shown}')
        print("NOTE: " + result["note"])
        if result.get("suggested_fallback"):
            print("SUGGESTED_FALLBACK: " + result["suggested_fallback"])
    else:
        print(f'[{result["status"]}] {result["model_query"]} -> {result["family_label"]} '
              f'({result["matched_family"]}, via {result["match_method"]})')
        if result["prompt_file"]:
            print("FILE: " + result["prompt_file"])
        if result["kind_note"]:
            print("KIND: " + result["kind_note"])
        if result["degraded"]:
            print("DEGRADED: " + result["degraded"])
        if result["missing_candidates"]:
            print("MISSING: " + ", ".join(result["missing_candidates"]))
    return 0 if result["status"] == "OK" else 1


if __name__ == "__main__":
    # stdout 与 stderr 都要锁 UTF-8：SystemExit / argparse 的报错走 stderr，
    # 只改 stdout 会让中文错误在 GBK 控制台（chcp 936）上变成乱码。
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
