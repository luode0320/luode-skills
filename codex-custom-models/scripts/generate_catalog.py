# -*- coding: utf-8 -*-
"""Generate the Codex model catalog (ModelsResponse schema) from the luode.vip model list.

Companion script of the `codex-custom-models` skill.
Source of truth : user's relay model list (default D:\\谷歌云盘\\workbuddy-model\\models.json)
Output          : ~/.codex/model-catalog.json (+ mirror beside the source list)

Usage:
    python generate_catalog.py [--src <models.json>] [--out <catalog.json>]

Behavior:
- GPT-family slugs (gpt-6-astra / gpt-5.6-sol / gpt-5.6-terra / gpt-5.6-luna):
  base = same-slug entry from the existing catalog (keeps official capability flags
  stable across updates), else fetched from the official codex models.json, else a
  minimal built-in template.
- Third-party slugs: base = catalog's gpt-5.6-luna entry (a verified-working combo
  against the relay, wire_api=responses), with neutral base_instructions injected so
  the model does not self-identify as GPT-5.
"""
import argparse
import json
import os
import shutil
import sys
import urllib.request

CODEX_HOME = os.path.expanduser(r"~\.codex")
DEFAULT_SRC = r"D:\谷歌云盘\workbuddy-model\models.json"
MIRROR_NAME = "codex-model-catalog.json"
OFFICIAL_URL = ("https://raw.githubusercontent.com/openai/codex/HEAD/"
                "codex-rs/models-manager/models.json")

NEUTRAL_INSTRUCTIONS = (
    "You are Codex, an AI coding agent. You and the user share one workspace, "
    "and your job is to collaborate with them until their intended goal is "
    "completely handled."
)


def load_json(path, desc):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"[ok] read {desc}: {path} ({os.path.getsize(path)} bytes)")
    return data


def fetch_official_models():
    print(f"[..] fetching official codex models.json: {OFFICIAL_URL}")
    with urllib.request.urlopen(OFFICIAL_URL, timeout=30) as r:
        return json.load(r)["models"]


def pick_base_template(slug, existing, official, builtin_luna):
    """Pick the best capability template for a slug, in priority order."""
    if existing is not None:
        hit = next((m for m in existing.get("models", []) if m["slug"] == slug), None)
        if hit:
            return hit
    if official is not None:
        hit = next((m for m in official if m["slug"] == slug), None)
        if hit:
            return hit
    return builtin_luna  # minimal fallback


def builtin_luna_template():
    """Minimal fallback template. Only used when neither an existing catalog nor
    the official file is reachable — prefer the richer bases above."""
    return {
        "slug": "gpt-5.6-luna",
        "display_name": "gpt-5.6-luna",
        "description": "relay model",
        "default_reasoning_level": "medium",
        "supported_reasoning_levels": [
            {"effort": e, "description": d} for e, d in [
                ("low", "Fast responses with lighter reasoning"),
                ("medium", "Balances speed and reasoning depth for everyday tasks"),
                ("high", "Greater reasoning depth for complex problems"),
                ("xhigh", "Extra high reasoning depth for complex problems"),
                ("max", "Maximum reasoning depth for the hardest problems"),
            ]
        ],
        "shell_type": "unified_exec",
        "visibility": "list",
        "supported_in_api": True,
        "priority": 8,
        "support_verbosity": True,
        "default_verbosity": "low",
        "default_reasoning_summary": "none",
        "supports_reasoning_summary_parameter": True,
        "apply_patch_tool_type": "freeform",
        "input_modalities": ["text", "image"],
        "web_search_tool_type": "text_and_image",
        "truncation_policy": {"mode": "tokens", "limit": 10000},
        "supports_parallel_tool_calls": True,
        "tool_mode": "code_mode_only",
        "context_window": 400000,
        "max_context_window": 872000,
        "auto_compact_token_limit": None,
        "base_instructions": NEUTRAL_INSTRUCTIONS,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--out", default=os.path.join(CODEX_HOME, "model-catalog.json"))
    args = ap.parse_args()

    src = load_json(args.src, "source model list")
    existing = None
    if os.path.exists(args.out):
        existing = load_json(args.out, "existing catalog")
    elif os.path.exists(DEFAULT_SRC.replace("models.json", MIRROR_NAME)):
        existing = load_json(DEFAULT_SRC.replace("models.json", MIRROR_NAME),
                             "existing catalog mirror")

    official = None
    try:
        official = fetch_official_models()
    except Exception as e:  # network optional
        print(f"[warn] official models.json unreachable ({e}); "
              f"falling back to existing/minimal templates")

    gpt_ctx = 400000        # GPT-family declared window (relay supports large ctx)
    third_ctx = 262144      # third-party window == user list maxInputTokens

    catalog, builtin = [], builtin_luna_template()
    for entry in src:
        slug = entry.get("id") or entry.get("name")
        if not slug:
            continue
        is_gpt = slug.startswith("gpt-")
        m = pick_base_template(slug, existing, official, builtin)
        m = json.loads(json.dumps(m))  # deep copy
        m["slug"] = slug
        m["display_name"] = slug
        m["description"] = "luode.vip relay · OpenAI-compatible"
        m["context_window"] = gpt_ctx if is_gpt else third_ctx
        m["max_context_window"] = m["context_window"]
        m["auto_compact_token_limit"] = None
        m["default_reasoning_level"] = entry.get("reasoning", {}).get(
            "defaultEffort", "high")
        if not is_gpt:
            # neutral identity for non-OpenAI models
            m.pop("model_messages", None)
            m["base_instructions"] = NEUTRAL_INSTRUCTIONS
        m["priority"] = entry.get("priority", 20)
        catalog.append(m)
        print(f"[..] {slug:<24} ctx={m['context_window']:<7} "
              f"default_effort={m['default_reasoning_level']}")

    out = {"models": catalog}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"[ok] wrote catalog: {args.out} ({os.path.getsize(args.out)} bytes, "
          f"{len(catalog)} models)")

    mirror = os.path.join(os.path.dirname(args.src), MIRROR_NAME)
    try:
        shutil.copy2(args.out, mirror)
        print(f"[ok] mirrored to: {mirror}")
    except OSError as e:
        print(f"[warn] mirror failed: {e}")

    # quick self-check: every model needs instructions
    bad = [m["slug"] for m in catalog
           if not m.get("base_instructions")
           and not (m.get("model_messages") or {}).get("instructions_template")]
    if bad:
        print(f"[ERROR] models missing instructions: {bad}", file=sys.stderr)
        sys.exit(1)
    print("[ok] all models carry base_instructions / model_messages")


if __name__ == "__main__":
    main()
