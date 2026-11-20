#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 动效语言的共享判定：transition 拆段、按属性判语义、选曲线。
       生成器（build_motion_overrides.py）与守卫（check_motion_language.py）共用同一套判定，
       避免「生成时按一套规则、校验时按另一套」的经典漂移。
[边界] 只做判定，不读写文件。曲线取值以 overrides.css 的动效校准层为唯一真相。
"""
from __future__ import annotations

import re

# 已表达过意图的缓动：不覆盖
KEEP_RE = re.compile(r"var\(--ease-|cubic-bezier\(|^linear$|^steps\(")
EASE_FAMILY = {"ease", "ease-in", "ease-out", "ease-in-out"}

COLOR_PROPS = {
    "color", "background", "background-color", "border-color", "box-shadow",
    "outline-color", "fill", "stroke", "opacity", "filter", "text-shadow",
    "background-image", "border", "border-top-color", "border-bottom-color",
}
MOTION_PROPS = {
    "transform", "translate", "rotate", "scale", "left", "top", "right", "bottom",
    "width", "height", "max-height", "min-height", "gap", "flex", "padding", "margin",
    "inset", "offset", "stroke-dashoffset", "stroke-dasharray",
}

# 退场：不仅换曲线，时长还要压到 0.8。关闭动画拖在手上比不做动画还难受。
EXIT_HINT = re.compile(r"(leave|exit|close|collapse|-out\b|is-closing|fade-out)", re.I)
# 交接：开合、选中、滑块。只在属性判不出语义时兜底。
SWAP_HINT = re.compile(r"(is-on|is-active|is-selected|is-checked|thumb|checked|is-open|\bopen\b)", re.I)

TRANSITION_RE = re.compile(r"(transition\s*:\s*)([^;}]+)(;?)")


def strip_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def split_parts(value: str) -> list[str]:
    """[参数] transition 实参串 [返回] 按顶层逗号切开的子属性（括号内逗号不算）。"""
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
    """[参数] 单段子属性 [返回] (属性名, 时长, 缓动)；缓动为 None 表示未声明。"""
    tokens = part.split()
    if not tokens:
        return "", None, None
    prop = tokens[0]
    dur = next((t for t in tokens[1:] if re.fullmatch(r"[\d.]+m?s", t)), None)
    timing = next((t for t in tokens[1:] if KEEP_RE.search(t) or t in EASE_FAMILY), None)
    return prop, dur, timing


def needs_rewrite(timing: str | None) -> bool:
    """[参数] 缓动 [返回] 是否属于「该换成语态令牌」的默认缓动。"""
    return timing is None or timing in EASE_FAMILY


def is_exit_selector(selector: str) -> bool:
    return bool(EXIT_HINT.search(strip_comments(selector)))


def pick_ease(selector: str, prop: str, exit_override: bool = False) -> str:
    """[参数] 选择器、单个属性、是否强制退场 [返回] 令牌名（不含 var()）。

    属性优先、选择器兜底：同一个 .card:hover，只改阴影是「着色」，改 transform 是「位移」。
    """
    if exit_override or is_exit_selector(selector):
        return "--ease-exit"
    lower = prop.lower()
    if lower in MOTION_PROPS:
        return "--ease-glide"
    if lower in COLOR_PROPS:
        return "--ease-reveal"
    if SWAP_HINT.search(strip_comments(selector)):
        return "--ease-swap"
    return "--ease-reveal"


def scale_duration(dur: str) -> str:
    """[参数] 形如 .2s / 200ms [返回] 乘 0.8 后的同单位时长。"""
    m = re.fullmatch(r"([\d.]+)(m?s)", dur)
    if not m:
        return dur
    return f"{round(float(m.group(1)) * 0.8, 3):g}{m.group(2)}"


def timings_for(selector: str, body: str) -> list[str] | None:
    """[参数] 选择器与声明块 [返回] 与 transition 属性顺序对齐的缓动列表；无需改写返回 None。"""
    decls = list(TRANSITION_RE.finditer(body))
    if not decls:
        return None
    last = decls[-1]          # 同一规则里多次声明时，以最后一条为准（CSS 层叠语义）
    values: list[str] = []
    changed = False
    exit_sel = is_exit_selector(selector)
    for part in split_parts(last.group(2)):
        prop, _dur, timing = parse_part(part)
        if needs_rewrite(timing):
            values.append(f"var({pick_ease(selector, prop, exit_sel)})")
            changed = True
        else:
            values.append(timing or "ease")   # 保留原值，维持与属性列表的对齐
    return values if changed else None


# ── 补建过渡：状态确实在变、却从来没有 transition 的元素 ─────────────────────
# 与「重定时」分开：那个是替换实参，这个是**新增**声明，风险不同，所以分两段生成。
VISUAL_DECL = re.compile(
    r"(?:^|;)\s*(color|background|background-color|border-color|box-shadow|opacity|"
    r"transform|translate|rotate|scale|filter)\s*:",
    re.I,
)
STATE_MARK = re.compile(
    r":hover|:focus-visible|:focus|"
    # 只认真正的「交互态」。`.is-info` / `.is-success` / `.is-bordered` / `.is-sm`
    # 这类是**变体**，它们在挂载时就确定，不随交互切换——给变体加过渡只会在首次渲染
    # 时闪一下，属于伪需求。早期判据没区分，把变体也算成硬跳，数字虚高。
    r"\.is-(?:on|active|selected|checked|open|closing|expanded|current|dragging|editing|hover)\b"
)
ELEMENT_ONLY = {
    "button", "a", "th", "td", "li", "i", "span", "dd", "dt", "p",
    "input", "label", "tr", "ul", "ol", "h1", "h2", "h3", "h4",
}
# 这些选择器属于画廊自身外壳，不是组件，补动效没有意义
CHROME_HINT = re.compile(r"\.g-cell|\.gallery|\.rail")


def split_selectors(selector: str) -> list[str]:
    """[参数] 可能含逗号分组的选择器 [返回] 逐条拆开的选择器。

    不拆开会出问题：`.a.is-on .b, .a.is-partial .b { background: … }` 整串拿去匹配
    基选择器时对不上，这条规则的属性就被静默漏掉——正是「复选框只补到 border-color、
    补不到 background-color」的原因。
    """
    return [p.strip() for p in split_parts(selector) if p.strip()]


def base_selector(selector: str) -> str:
    """[参数] 含状态的选择器 [返回] 去掉状态后的基选择器（保留 :not 等结构）。"""
    s = re.sub(r":hover|:focus-visible|:focus", "", selector)
    s = re.sub(r"\.is-(?:on|active|selected|checked|open|closing|expanded|current|dragging|editing|hover)\b", "", s)
    return " ".join(s.split())


def visual_props(body: str) -> list[str]:
    """[参数] 声明块 [返回] 需要参与过渡的可视属性（去重、保序）。"""
    out: list[str] = []
    for hit in VISUAL_DECL.finditer(body):
        name = hit.group(1).lower()
        prop = "background-color" if name == "background" else name
        if prop == "background-color" and "background-color" in out:
            continue
        if prop not in out:
            out.append(prop)
    return out


def transition_for(base: str, props: list[str]) -> str:
    """[参数] 基选择器与属性 [返回] 一条 transition 声明值（属性 / 时长 / 曲线）。

    只看属性、不看选择器：基选择器里可能带 `.is-sortable` 这类**能力标记**，
    按 `is-` 判「交接」会误判——那只是可排序，不是状态在切换。
    """
    moved = any(p in ("transform", "translate", "rotate", "scale") for p in props)
    ease = "--ease-swap" if moved else "--ease-reveal"
    dur = "--dur-swap" if moved else "--dur-hover"
    return ", ".join(f"{p} var({dur}) var({ease})" for p in props)
