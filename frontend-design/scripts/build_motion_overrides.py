#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 从冻结的 src/styles/*.css 机械派生「动效语言覆盖块」，写入 overrides.css 的受管区。
       冻结样式一个字节都不改：同特异度选择器 + overrides.css 最后加载即可生效。
[边界] 只处理 transition 的缓动，不改属性与时长。linear / 自定义 bezier / --ease-* 一律原样保留。
       @media 内的规则必须原样复刻包裹，提到外层会改变生效条件。
       prefers-reduced-motion 整块排除（那里是刻意的 !important 兜底）。
[用法] python -X utf8 -B frontend-design/scripts/build_motion_overrides.py
       python -X utf8 -B frontend-design/scripts/build_motion_overrides.py --check
       python -X utf8 -B frontend-design/scripts/build_motion_overrides.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import motion_language as ml  # noqa: E402
from motion_language import strip_comments, timings_for  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
STYLES = SKILL / "component-library" / "src" / "styles"
TARGET = STYLES / "overrides.css"

BEGIN = "/* BEGIN GENERATED: motion language overrides */"
END = "/* END GENERATED: motion language overrides */"

# 冻结面按 src/main.ts 的真实加载顺序登记；overrides.css 自己不能被扫描，否则自我引用。
# 漏登记一个样式文件会静默少派生一整层，所以 collect() 里有覆盖断言兜底。
SOURCE_FILES = (
    "tokens.css", "base.css", "materials.css", "components.css",
    "instruments.css", "layout.css", "pages.css",
)
SKIP_AT = {"keyframes", "-webkit-keyframes", "font-face", "property"}


def match_brace(text: str, open_idx: int) -> int:
    depth = 0
    for i in range(open_idx, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def parse_rules(css: str, context: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], str, str]]:
    """[参数] CSS 文本与当前媒体上下文 [返回] [(context, 选择器, 声明块)]。"""
    out: list[tuple[tuple[str, ...], str, str]] = []
    i, n = 0, len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            break
        semi = css.find(";", i)
        if semi != -1 and semi < brace:
            i = semi + 1                     # @import 这类无块语句
            continue
        prelude = " ".join(css[i:brace].split())
        close = match_brace(css, brace)
        if close == -1:
            break
        body = css[brace + 1:close]
        if prelude.startswith("@"):
            name = re.match(r"@([\w-]+)", prelude)
            kind = name.group(1).lower() if name else ""
            if kind in ("media", "supports"):
                if "prefers-reduced-motion" not in prelude:
                    out.extend(parse_rules(body, context + (prelude,)))
            elif kind in SKIP_AT:
                pass                          # 整块丢弃
        else:
            out.append((context, prelude, body))
        i = close + 1
    return out


def collect() -> list[tuple[tuple[str, ...], str, list[str]]]:
    """[返回] 需要重定时的规则：[(context, 选择器, 缓动列表)]，按首次出现顺序去重。"""
    # 冻结层新增文件却没登记时，派生会静默少一整层。宁可在这里炸掉。
    on_disk = {p.name for p in STYLES.glob("*.css")} - {"overrides.css"}
    missing = on_disk - set(SOURCE_FILES)
    if missing:
        raise SystemExit(
            f"MOTION_OVERRIDES: FAIL（src/styles 下有未登记的样式文件 {sorted(missing)}，"
            f"请按 main.ts 的加载顺序补进 SOURCE_FILES）"
        )

    seen: dict[tuple[tuple[str, ...], str], list[str]] = {}
    order: list[tuple[tuple[str, ...], str]] = []
    for name in SOURCE_FILES:
        path = STYLES / name
        if not path.exists():
            continue
        css = strip_comments(path.read_text(encoding="utf-8"))
        for context, selector, body in parse_rules(css):
            values = timings_for(selector, body)
            if not values:
                continue
            key = (context, selector)
            if key not in seen:
                order.append(key)
            seen[key] = values            # 同名选择器以最后一份为准（层叠语义）
    return [(ctx, sel, seen[(ctx, sel)]) for ctx, sel in order]


# 人工确认的补建名单。自动识别只能回答「谁在硬跳」，回答不了「该不该动」——
# 比如 `.rg-node .rg-body::before` 这类会改图形结构的，补过渡反而更糟；
# `.btn-primary:not(:disabled)` 这类元素同时带着已有过渡的 `.btn`，补一条 shorthand
# 会把原有的 color/border/shadow 整条重置掉。
# 名单里的属性仍由生成器从状态规则里机械读取，不手抄。
CURATED_BASES = (
    # ── 第一批：表单与基础控件 ──
    ".checkbox",
    ".checkbox .checkbox-box",
    ".switch",
    ".switch .switch-knob",
    ".tree-toggle",
    ".x-alert .x-alert-ico",
    ".input-shell .input-clear",
    ".table th",
    ".delta-pill",
    ".odo-cell",
    ".x-datalist",
    ".x-rate",
    ".x-vcode",
    ".heat-legend i",
    ".org-toggle",
    # ── 第二批：交互控件（输入 / 选择 / 表格 / 列表 / 芯片） ──
    # 这些元素的状态也在变，但从来没有过渡。图形类（.rg-* / .heat-* / .org-* / .bar-*）
    # 和已经带基础类过渡的（.btn-* / .pill-btn）不在此列——前者补过渡会改图形结构，
    # 后者补一条 shorthand 会把原有过渡整条重置。
    ".input-shell-within",
    ".select-trigger .select-value",
    ".table .sort-ico",
    ".table th.is-sortable",
    ".table tbody tr td.col-actions",
    ".board-menu-btn",
    ".board-menu .menu-item",
    ".settings-nav-item",
    ".nav-preview-item",
    ".stage-chip",
    ".legend-toggle",
    ".scope-option .scope-radio",
    ".cmd-item .cmd-ico",
    ".cmd-item .cmd-go",
    ".quick-link .quick-go",
    ".mx-cell .mx-mark",
    ".swatch",
    ".swatch .tag",
    ".swatch-def",
    ".trace-crumb",
    ".ask-form-within",
    ".preview-file .preview-name",
)

# 图形类没有进 CURATED_BASES：它们的基选择器带变体类（`.rg-node.is-item` / `.mx-row.is-hover`），
# 按选择器匹配会漏，而且每个变体都要单列一条。这里直接按「元素 + 属性」写死，
# 覆盖面反而更稳：一条规则管住同一个元素的所有变体。
EXTRA_RULES = {
    # 关系图节点：悬停时描边与投影加强，现在是一下跳出来
    ".rg-node .rg-body": ["border-color", "box-shadow"],
    # 权限矩阵行：悬停时整行底色浮起
    ".mx-row .mx-label": ["background-color"],
}


def selector_is_valid(sel: str) -> bool:
    """[参数] 选择器 [返回] 能否安全写进样式表。

    自动派生的基选择器可能留下 `:has()` / `:not()` 空参或括号不配平。这类选择器一旦
    落盘，浏览器会从它开始丢弃后续规则，整段覆盖直接失效——比不改更糟。
    """
    if not sel or sel.count("(") != sel.count(")") or sel.count("[") != sel.count("]"):
        return False
    return not re.search(r":(not|has|is|where)\s*\(\s*\)", sel)


def audit_missing() -> list[str]:
    """[返回] 所有「状态会变但没有过渡」的基选择器（诊断用，不参与生成）。"""
    has_transition, states = _scan_states()
    out: list[str] = []
    for sel, _body in states:
        base = ml.base_selector(sel)
        if not base or base in ml.ELEMENT_ONLY:
            continue
        if not selector_is_valid(base) or ml.CHROME_HINT.search(base):
            continue
        if base in has_transition or base in out or base in CURATED_BASES:
            continue          # 已有过渡 / 重复 / 本轮已补，都不该出现在待评估清单里
        out.append(base)
    return out


def _scan_states() -> tuple[set[str], list[tuple[str, str]]]:
    """[返回] (已有 transition 的选择器集合, [(状态选择器, 声明块)])。"""
    has_transition: set[str] = set()
    states: list[tuple[str, str]] = []
    for name in SOURCE_FILES:
        path = STYLES / name
        if not path.exists():
            continue
        css = strip_comments(path.read_text(encoding="utf-8"))
        for _ctx, selector, body in parse_rules(css):
            sel = " ".join(selector.split())
            if ml.TRANSITION_RE.search(body):
                has_transition.add(sel)
                has_transition.add(ml.base_selector(sel))
            if ml.STATE_MARK.search(sel) and ml.visual_props(body):
                for part in ml.split_selectors(sel):   # 逗号分组要拆开，否则基选择器对不上
                    states.append((part, body))
    return has_transition, states


def collect_missing() -> list[tuple[str, str]]:
    """[返回] 需要补建 transition 的规则：[(基选择器, transition 值)]。

    判据：某条状态规则（`:hover` / `.is-*`）声明了可视属性，而它的基选择器在冻结层里
    从来没有出现过 `transition` —— 这类状态切换是硬跳，用户看到的是瞬间闪变。

    为什么不会误伤已有过渡：组件若在自己的 scoped 样式里定义过过渡，那条选择器带
    `[data-v]` 属性，优先级高于这里的全局规则，本段根本压不过它。
    """
    has_transition, states = _scan_states()

    # 同一个基选择器可能对应多条状态规则（`:hover` 一条、`.is-*` 一条），
    # 属性取并集：只取第一条会漏掉真正变化最多的那个属性。
    acc: dict[str, list[str]] = {}
    for sel, body in states:
        base = ml.base_selector(sel)
        if base not in CURATED_BASES or base in has_transition:
            continue
        props = ml.visual_props(body)
        if not props:
            continue
        bucket = acc.setdefault(base, [])
        for prop in props:
            if prop not in bucket:
                bucket.append(prop)

    for base, props in EXTRA_RULES.items():      # 图形类：显式规则，不走推导
        acc.setdefault(base, [])
        for prop in props:
            if prop not in acc[base]:
                acc[base].append(prop)

    ordered = list(CURATED_BASES) + [b for b in EXTRA_RULES if b not in CURATED_BASES]
    return [(base, ml.transition_for(base, acc[base])) for base in ordered if acc.get(base)]


def render(entries: list[tuple[tuple[str, ...], str, list[str]]], missing: list[tuple[str, str]]) -> str:
    # 段数动态算：写死的数字迟早和派生结果对不上
    rewritten = sum(1 for _c, _s, values in entries for v in values if not v.startswith("var(--ease-premium)"))
    lines = [
        BEGIN,
        "/* 由 scripts/build_motion_overrides.py 从冻结样式机械派生，请勿手改。",
        f"   冻结层有 {rewritten} 段 transition 仍跑在浏览器默认 ease 上；这里按「属性优先、选择器兜底」",
        "   分派到五条语态曲线。同特异度 + 本文件最后加载 = 生效，冻结样式零改动。",
        "   linear / 自定义 bezier / --ease-* 不在派生范围内；prefers-reduced-motion 整块排除。 */",
        "",
    ]
    open_ctx: tuple[str, ...] | None = ()
    for context, selector, values in entries:
        if context != open_ctx:
            if open_ctx:
                lines.append("}")
                lines.append("")
            if context:
                for layer in context:
                    lines.append(f"{layer} {{")
            open_ctx = context
        indent = "  " if context else ""
        lines.append(f"{indent}{selector} {{ transition-timing-function: {', '.join(values)}; }}")
    if open_ctx:
        lines.append("}")
    lines.append("")
    lines.append("/* ── 补建过渡 ────────────────────────────────────────────────────────")
    lines.append("   下列元素的状态确实在变（:hover / .is-* 声明了可视属性），但冻结层从来没有给它们")
    lines.append("   写过 transition —— 表现是瞬间闪变。这里补上声明；组件若在 scoped 样式里已定义过渡，")
    lines.append("   那条带 [data-v] 属性、优先级更高，本段压不过它，因此不会重复接管。 */")
    lines.append("")
    for base, value in missing:
        if not selector_is_valid(base):      # 兜底：非法选择器宁可不出，也不能污染样式表
            continue
        lines.append(f"{base} {{ transition: {value}; }}")
    lines.append(END)
    return "\n".join(lines) + "\n"


def apply_block(rendered: str) -> tuple[str, bool]:
    """[参数] 渲染出的受管块 [返回] (新文件内容, 是否变化)。"""
    text = TARGET.read_text(encoding="utf-8")
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        _old, tail = rest.split(END, 1)
        updated = head + rendered + tail.split("\n", 1)[1] if "\n" in tail else head + rendered
        return updated, updated != text
    # 首次生成：插在字号标度受管块之前，保持「动效 → 字号 → 色板」的顺序
    anchor = "/* BEGIN GENERATED: type scale overrides */"
    if anchor in text:
        head, tail = text.split(anchor, 1)
        updated = head + rendered + "\n" + anchor + tail
    else:
        updated = text.rstrip("\n") + "\n\n" + rendered
    return updated, updated != text


def selftest() -> int:
    sample = """
.top { transition: background .2s ease, transform .3s ease; }
.plain { transition: opacity .2s linear; }
.premium { transition: color var(--ease-premium) .2s; }
@media (min-width: 640px) { .wide { transition: background .2s ease; } }
@media (prefers-reduced-motion: reduce) { .rm { transition: all .2s ease; } }
@keyframes spin { from { opacity: 0 } to { opacity: 1 } }
"""
    css = strip_comments(sample)
    entries = [(ctx, sel, v) for ctx, sel, body in parse_rules(css) if (v := timings_for(sel, body))]
    fails: list[str] = []

    names = {sel: (ctx, v) for ctx, sel, v in entries}
    if ".top" not in names:
        fails.append("顶层规则未收集")
    else:
        ctx, values = names[".top"]
        if ctx:
            fails.append(f"顶层规则被错误包进媒体查询：{ctx}")
        if values != ["var(--ease-reveal)", "var(--ease-glide)"]:
            fails.append(f"多属性分派错误：{values}")
    if ".plain" in names:
        fails.append("linear 规则被误纳入（会把匀速改成变速）")
    if ".premium" in names:
        fails.append("已显式缓动的规则被误纳入")
    if ".rm" in names:
        fails.append("prefers-reduced-motion 块未排除")
    if ".wide" not in names:
        fails.append("媒体查询内的规则未收集")
    elif names[".wide"][0] != ("@media (min-width: 640px)",):
        fails.append(f"媒体上下文未原样复刻：{names['.wide'][0]}")
    if any(sel in ("from", "to") for _ctx, sel, _v in entries):
        fails.append("keyframes 内部帧被误当成规则")

    if fails:
        print("MOTION_OVERRIDES_SELFTEST: FAIL")
        for f in fails:
            print("  - " + f)
        return 1
    print("MOTION_OVERRIDES_SELFTEST: PASS（多属性分派 / 媒体查询复刻 / linear 与 premium 排除 / reduced-motion 排除 / keyframes 排除）")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    if "--audit" in argv:
        cands = audit_missing()
        print(f"MOTION_MISSING_AUDIT: {len(cands)} 个基选择器状态会硬跳（未参与生成，需人工确认）")
        for base in cands:
            mark = "✓ 已确认" if base in CURATED_BASES else ""
            print(f"  {base} {mark}")
        return 0

    entries = collect()
    if len(entries) < 20:
        print(f"MOTION_OVERRIDES: FAIL（只派生出 {len(entries)} 条规则，来源或解析异常）")
        return 1
    missing = collect_missing()
    rendered = render(entries, missing)

    if "--check" in argv:
        text = TARGET.read_text(encoding="utf-8")
        if BEGIN not in text:
            print("MOTION_OVERRIDES: MISSING（受管块未生成，请运行生成命令）")
            return 1
        current = text.split(BEGIN, 1)[1].split(END, 1)[0]
        same = (BEGIN + current + END).strip() == rendered.strip()
        print(
            f"MOTION_OVERRIDES: PASS ({len(entries)} 条重定时 + {len(missing)} 条补建)" if same
            else "MOTION_OVERRIDES: STALE（冻结样式或判定规则变了，请重新生成）"
        )
        return 0 if same else 1

    updated, changed = apply_block(rendered)
    if changed:
        TARGET.write_text(updated, encoding="utf-8")
    print(f"MOTION_OVERRIDES_WRITTEN: {len(entries)} 条重定时 + {len(missing)} 条补建{'（内容未变）' if not changed else ''} -> src/styles/overrides.css")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
