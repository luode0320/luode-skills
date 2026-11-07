#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 批次 1 一次性工具：把 extend / workspace 里 scoped 样式的默认 ease 换成动效语态令牌。
[边界] 只改 transition 的缓动实参，不动属性、不动时长（退场类按 0.8 折算除外）。
       已有 --ease-premium / 自定义 cubic-bezier / linear 一律原样保留，视为已表达意图。
[用法] python scripts/_apply_motion_language.py --dry-run
       python scripts/_apply_motion_language.py --apply [--only DatePicker,MonthPicker]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "component-library"
TARGET_DIRS = ("src/components/extend", "src/components/workspace")

STYLE_RE = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.S)
RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
TRANSITION_RE = re.compile(r"(transition\s*:\s*)([^;}]+)(;)")

# 只信这些缓动是「已经表达过意图」的，不动
KEEP_RE = re.compile(r"var\(--ease-|cubic-bezier\(|^linear$|^steps\(")

COLOR_PROPS = {
    "color", "background", "background-color", "border-color", "box-shadow",
    "outline-color", "fill", "stroke", "opacity", "filter", "text-shadow",
}
MOTION_PROPS = {
    "transform", "translate", "rotate", "scale", "left", "top", "right", "bottom",
    "width", "height", "max-height", "min-height", "gap", "flex", "padding", "margin",
}

# 退场类：不仅换曲线，时长还要压到 0.8。关闭动画拖在手上比不做动画还难受。
EXIT_HINT = re.compile(r"(leave|exit|close|collapse|-out\b|is-closing|fade-out)", re.I)
# 交接类：开合、选中、滑块。只在属性判不出语义时兜底。
SWAP_HINT = re.compile(r"(is-on|is-active|is-selected|is-checked|thumb|checked|is-open|\bopen\b)", re.I)


def split_parts(value: str) -> list[str]:
    """[参数] transition 的实参串 [返回] 按顶层逗号切开的子属性（cubic-bezier 内的逗号不算）。"""
    parts, depth, buf = [], 0, ""
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    parts.append(buf)
    return [p.strip() for p in parts if p.strip()]


def parse_part(part: str) -> tuple[str, str | None, str | None]:
    """[参数] 单段子属性 [返回] (属性名, 时长, 缓动)。缓动为 None 表示未声明。"""
    tokens = part.split()
    prop = tokens[0]
    dur = next((t for t in tokens[1:] if re.fullmatch(r"[\d.]+m?s", t)), None)
    timing = next(
        (t for t in tokens[1:] if KEEP_RE.search(t) or t in ("ease", "ease-in", "ease-out", "ease-in-out")),
        None,
    )
    return prop, dur, timing


def pick_ease(selector: str, props: list[str], is_exit: bool) -> str:
    """[参数] 选择器、涉及属性、是否退场 [返回] 应使用的缓动令牌名。"""
    if is_exit:
        return "--ease-exit"
    lower = {p.lower() for p in props}
    if lower & MOTION_PROPS:
        return "--ease-glide"
    if lower and lower <= COLOR_PROPS:
        return "--ease-reveal"
    # 属性判不出语义（如 all / 混合），退回选择器兜底
    if SWAP_HINT.search(selector):
        return "--ease-swap"
    return "--ease-reveal"


def scale_duration(dur: str) -> str:
    """[参数] 形如 .2s / 200ms [返回] 乘 0.8 后的同单位时长。"""
    m = re.fullmatch(r"([\d.]+)(m?s)", dur)
    if not m:
        return dur
    value, unit = float(m.group(1)), m.group(2)
    out = round(value * 0.8, 3)
    text = f"{out:g}"
    return f"{text}{unit}"


def strip_comments(text: str) -> str:
    """[参数] 任意文本 [返回] 去掉 /* */ 注释后的文本（用于语义判定，不用于回写）。"""
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def rewrite_style(selector: str, body: str) -> tuple[str, list[str]]:
    """[参数] 规则选择器与声明块 [返回] (新声明块, 变更说明列表)。"""
    notes: list[str] = []
    # 注释里可能出现 close / exit 这类词，判定前先剥掉，否则会误判成退场
    clean_sel = strip_comments(selector).strip()
    is_exit = bool(EXIT_HINT.search(clean_sel))
    short = " ".join(clean_sel.split())[:46]

    def repl(m: re.Match[str]) -> str:
        parts = split_parts(m.group(2))
        parsed = [parse_part(p) for p in parts]
        # 已有显式缓动的段不动：那是已表达过的意图
        targets = [i for i, (_, _, timing) in enumerate(parsed) if timing in (None, "ease", "ease-in", "ease-out", "ease-in-out")]
        if not targets:
            return m.group(0)
        rebuilt: list[str] = []
        for i, (prop, dur, timing) in enumerate(parsed):
            if i not in targets:
                rebuilt.append(parts[i])
                continue
            # 逐段按自己的属性判语义：`width .3s ease, background .3s ease`
            # 两段语义不同，一起判会把着色也拖成位移曲线。
            token = pick_ease(clean_sel, [prop], is_exit)
            # 原地替换而不是重排：既有 56 行都写成 `property <easing> <duration>`，
            # 重排成 `property <duration> <easing>` 会让同一文件出现两种笔法。
            toks = parts[i].split()
            if timing and timing in toks:
                toks[toks.index(timing)] = f"var({token})"
            else:
                toks.insert(1, f"var({token})")
            new_dur = scale_duration(dur) if (is_exit and dur and dur in toks) else dur
            if new_dur != dur and dur in toks:
                toks[toks.index(dur)] = new_dur
            rebuilt.append(" ".join(toks))
            notes.append(f"{short:<46} {prop:<14} {timing or '(缺省ease)':>12} → var({token}){'  时长 ' + dur + '→' + new_dur if new_dur != dur else ''}")
        return m.group(1) + ", ".join(rebuilt) + m.group(3)

    new_body = TRANSITION_RE.sub(repl, body)
    return new_body, notes


def process(path: Path, apply: bool) -> list[str]:
    # newline="" 让读写都不做换行转换：否则 Windows 上会把混合换行统一成 CRLF，
    # 让 30 个文件在 git 里变成整篇差异。
    with path.open(encoding="utf-8", newline="") as fh:
        text = fh.read()
    notes: list[str] = []

    def repl_style(m: re.Match[str]) -> str:
        inner = m.group(2)

        def repl_rule(rm: re.Match[str]) -> str:
            sel, body = rm.group(1), rm.group(2)
            new_body, local = rewrite_style(sel, body)
            notes.extend(local)
            return sel + "{" + new_body + "}"

        return m.group(1) + RULE_RE.sub(repl_rule, inner) + m.group(3)

    updated = STYLE_RE.sub(repl_style, text)
    if apply and notes and updated != text:
        with path.open("w", encoding="utf-8", newline="") as fh:
            fh.write(updated)
    return notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    only = {s.strip() for s in args.only.split(",") if s.strip()}

    files: list[Path] = []
    for d in TARGET_DIRS:
        files.extend(sorted((LIB / d).glob("*.vue")))

    total, touched = 0, 0
    for path in files:
        if only and path.stem not in only:
            continue
        notes = process(path, args.apply)
        if not notes:
            continue
        touched += 1
        total += len(notes)
        print(f"\n── {path.relative_to(LIB)}")
        for n in notes:
            print("   " + n)

    mode = "已写入" if args.apply else "dry-run（未写入）"
    print(f"\nMOTION_APPLY: {mode}｜{touched} 个文件，{total} 段缓动")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
