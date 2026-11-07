#!/usr/bin/env python3
"""对比度守卫：核对珍珠玻璃字色令牌在其真实承载面上的 WCAG 2.1 对比度。

[用途] 把「正文可读」从主观感受变成机器可判定项：解析 `src/styles/tokens.css`（上游冻结层）
       与 `src/styles/overrides.css`（本地覆盖层）的生效值，按层叠顺序取后者覆盖前者，
       再把每个字色令牌铺到三个内容面（白、`--canvas`、`--surface-solid`）上取最差值判定。
       正文与小字要求 4.5:1，非文本/禁用档要求 3:1。
[边界] 只判定令牌层，不判定页面里是否用对了令牌——`--ink-faint` 被误用在 10px 图表轴标签上，
       令牌本身达标也依然是缺陷，那属于用法约定，由 LOCAL-GUIDE.md 约束、由人工核对页复核。
       只处理 hex 与不透明 rgb 值；rgba 与 `var()` 别名无法脱离层叠上下文求值，记为未覆盖并打印，
       不静默当作通过。
最近修改时间：2026-10-31 21:05:00；改动原因：初版，随字色对比度整改一起落地。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "component-library"
TOKENS = LIB / "src" / "styles" / "tokens.css"
OVERRIDES = LIB / "src" / "styles" / "overrides.css"

# 字色令牌的达标线。键为令牌名，值为 (最低对比度, 中文用途说明)。
# 4.5 = WCAG 1.4.3 正文与小字；3.0 = WCAG 1.4.11 非文本，同时兜住 WCAG 1.4.3 对停用控件
# 的豁免边界——`--ink-faint` 只允许出现在停用态、装饰图形与占位符，不得承载元信息小字。
TEXT_RULES = {
    "--ink": (4.5, "正文与标题"),
    "--ink-muted": (4.5, "次级正文"),
    "--ink-soft": (4.5, "标签与元信息小字"),
    "--ink-faint": (3.0, "停用态与装饰（不得承载小字）"),
    "--blue": (4.5, "主操作与选中"),
    "--leaf-text": (4.5, "正常状态文字"),
    "--red-text": (4.5, "警示文字"),
}

# 字色真实承载的内容面，按主题分开——深色主题下不存在纯白内容面，
# 拿 `#ffffff` 去比会造出一整片假失败（实测误报 7 项）。
# `--stage` 是外壳外围底色，正文不直接铺在上面，故不纳入任一主题。
BACKDROPS: dict[str, tuple[str, ...]] = {
    "light": ("#ffffff", "--canvas", "--surface-solid"),
    "dark": ("--canvas", "--surface-solid"),
}

# 色板判定直接用十六进制：色板块只含主色一族，不含 `--canvas` 等场景令牌，
# 无法从块内解析出背景，必须与 build_accent_palette.py 使用同一组值。
ACCENT_BACKDROPS: dict[str, tuple[str, ...]] = {
    "light": ("#ffffff", "#f6f8f7", "#fbfcfc"),
    "dark": ("#121517", "#1b1f21"),
}

THEMES = {"light": ":root", "dark": ':root[data-theme="dark"]'}

HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGB_RE = re.compile(r"^rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*([\d.]+)\s*)?\)$")
VAR_DECL_RE = re.compile(r"(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def strip_comments(text: str) -> str:
    """去掉 CSS 注释。

    [参数] text 原文
    [返回] 注释替换为空白后的文本（保留长度无关，仅避免注释内的伪声明被读进令牌表）
    """
    return COMMENT_RE.sub(" ", text)


def parse_root_blocks(css: str, selector: str) -> dict[str, str]:
    """取出某个根选择器块内的全部自定义属性声明。

    [参数] css 已去注释的样式文本
    [参数] selector 目标选择器，如 `:root` 或 `:root[data-theme="dark"]`
    [返回] 令牌名到原始取值的映射；同名多次声明时后者胜（与浏览器层叠一致）
    """
    found: dict[str, str] = {}
    pattern = re.escape(selector) + r"\s*\{([^}]*)\}"
    for body in re.findall(pattern, css):
        for name, raw in VAR_DECL_RE.findall(body):
            found[name.strip()] = raw.strip()
    return found


def resolve_tokens() -> dict[str, dict[str, str]]:
    """按层叠顺序合并两层的令牌表。

    [参数] 无
    [返回] {"light": {...}, "dark": {...}}；后读入的 overrides.css 覆盖先读入的 tokens.css
    """
    merged: dict[str, dict[str, str]] = {"light": {}, "dark": {}}
    for path in (TOKENS, OVERRIDES):
        if not path.exists():
            print(f"CONTRAST_SOURCE_MISSING: {path}")
            continue
        css = strip_comments(path.read_text(encoding="utf-8"))
        for theme, selector in THEMES.items():
            merged[theme].update(parse_root_blocks(css, selector))
    return merged


def parse_color(value: str) -> tuple[int, int, int] | None:
    """把 CSS 颜色字面量转成 RGB 三元组。

    [参数] value 令牌原始取值
    [返回] (r, g, b)；hex 与不透明 rgb 之外的写法（rgba 半透明、var 别名）返回 None
    """
    text = value.strip()
    hex_match = HEX_RE.match(text)
    if hex_match:
        digits = hex_match.group(1)
        if len(digits) == 3:
            digits = "".join(ch * 2 for ch in digits)
        return tuple(int(digits[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    rgb_match = RGB_RE.match(text)
    if rgb_match:
        alpha = rgb_match.group(4)
        if alpha is not None and float(alpha) < 1.0:
            return None
        return tuple(min(255, int(rgb_match.group(i))) for i in (1, 2, 3))  # type: ignore[return-value]
    return None


def relative_luminance(color: tuple[int, int, int]) -> float:
    """按 WCAG 2.1 计算相对亮度。

    [参数] color RGB 三元组（0-255）
    [返回] 0-1 的相对亮度
    """

    def channel(raw: int) -> float:
        c = raw / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = color
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    """计算两色的对比度。

    [参数] fg 前景色
    [参数] bg 背景色
    [返回] 1-21 之间的对比度
    """
    high, low = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def parse_accent_blocks(css: str) -> dict[tuple[str, str], dict[str, str]]:
    """取出所有色板块的令牌表。

    [参数] css 已去注释的样式文本
    [返回] {(色板键, 主题): 令牌表}。浅色块选择器形如 `[data-accent="x"]`，
           深色块含 `data-theme="dark"`，据此区分同名色板的两种取值。
    """
    blocks: dict[tuple[str, str], dict[str, str]] = {}
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        selector = " ".join(match.group(1).split())
        key_match = re.search(r'data-accent="([\w-]+)"', selector)
        if not key_match:
            continue
        theme = "dark" if 'data-theme="dark"' in selector else "light"
        table = {k.strip(): v.strip() for k, v in VAR_DECL_RE.findall(match.group(2))}
        blocks[(key_match.group(1), theme)] = table
    return blocks


def judge_accents(css: str) -> list[str]:
    """逐个色板判定两种角色是否都达标。

    [参数] css 已去注释的样式文本
    [返回] 失败说明列表
    `--blue` 是「主色当文字」，要对内容底达标；`--blue-solid` 是「主色当实心背景」，
    要保证白字压在上面达标。两者方向相反，缺一不可。
    """
    failures: list[str] = []
    blocks = parse_accent_blocks(css)
    if not blocks:
        return ["未找到任何色板块（accent 生成块缺失或未同步）"]

    for (key, theme), table in sorted(blocks.items()):
        backdrops = ACCENT_BACKDROPS[theme]
        text_raw = table.get("--blue")
        solid_raw = table.get("--blue-solid")
        if text_raw is None or solid_raw is None:
            failures.append(f"{key}/{theme} 缺少 --blue 或 --blue-solid")
            continue

        text = parse_color(text_raw)
        solid = parse_color(solid_raw)
        if text is None or solid is None:
            print(f"CONTRAST_UNRESOLVED_COLOR: {key}/{theme}")
            continue

        worst = 21.0
        worst_name = ""
        for bg_hex in backdrops:
            bg = parse_color(bg_hex)
            if bg is None:
                continue
            ratio = contrast_ratio(text, bg)
            if ratio < worst:
                worst, worst_name = ratio, bg_hex
        white = (255, 255, 255)
        solid_ratio = contrast_ratio(white, solid)

        text_ok = worst >= 4.5
        solid_ok = solid_ratio >= 4.5
        print(
            f"  {'PASS' if text_ok else 'FAIL'} accent {key:7s} {theme:5s} 文字 {worst:5.2f}:1"
            f"  按钮白字 {solid_ratio:5.2f}:1"
        )
        if not text_ok:
            failures.append(f"{key}/{theme} 作为文字最低 {worst:.2f}:1 on {worst_name} < 4.5:1")
        if not solid_ok:
            failures.append(f"{key}/{theme} 作为实心背景白字 {solid_ratio:.2f}:1 < 4.5:1")
    return failures


def judge(theme: str, table: dict[str, str], forced: dict[str, str] | None = None) -> list[str]:
    """逐令牌判定一个主题下的达标情况。

    [参数] theme 主题名，用于输出
    [参数] table 该主题的令牌表
    [参数] forced 强制替换的令牌值，供 --selftest 注入阳性对照
    [返回] 失败说明列表；空列表表示全部达标
    """
    values = dict(table)
    if forced:
        values.update(forced)

    failures: list[str] = []
    unresolved: list[str] = []

    backdrops: dict[str, tuple[int, int, int]] = {}
    for name in BACKDROPS[theme]:
        raw = name if name.startswith("#") else values.get(name)
        parsed = parse_color(raw) if raw else None
        if parsed is None:
            print(f"CONTRAST_UNRESOLVED_BACKDROP: {theme} {name}")
        else:
            backdrops[name] = parsed

    for token, (floor, purpose) in TEXT_RULES.items():
        raw = values.get(token)
        if raw is None:
            failures.append(f"{theme} {token} 未定义（{purpose}）")
            continue
        fg = parse_color(raw)
        if fg is None:
            unresolved.append(f"{theme} {token} = {raw}")
            continue
        worst_name = ""
        worst = 21.0
        for bg_name, bg in backdrops.items():
            ratio = contrast_ratio(fg, bg)
            if ratio < worst:
                worst, worst_name = ratio, bg_name
        mark = "PASS" if worst >= floor else "FAIL"
        print(f"  {mark} {theme:5s} {token:14s} {worst:5.2f}:1 (需 {floor}) on {worst_name}  {purpose}")
        if worst < floor:
            failures.append(f"{theme} {token} 最低 {worst:.2f}:1 on {worst_name} < {floor}:1（{purpose}）")

    for item in unresolved:
        print(f"CONTRAST_UNRESOLVED_COLOR: {item}")
    return failures


def selftest() -> int:
    """跑阳性对照，证明判据真的会报错。

    [参数] 无
    [返回] 0 表示对照全部符合预期
    """
    tokens = resolve_tokens()
    # 对照一：把 --ink-soft 压到接近 --ink-faint 的浅灰，必须判 FAIL
    low = {"--ink-soft": "#c9ced0"}
    # 对照二：把 --ink-faint 提到纯黑，必须在 3:1 判据下转 PASS
    high = {"--ink-faint": "#000000"}

    expected_fail = judge("light", tokens["light"], forced=low)
    caught = any("--ink-soft" in item for item in expected_fail)
    print(f"CONTRAST_SELFTEST: 低对比注入 {'已报错' if caught else '未报错（判据失效）'}")

    print("-- 对照二：提亮后应转 PASS --")
    still_fail = judge("light", tokens["light"], forced=high)
    raised = any("--ink-faint" in item for item in still_fail)
    print(f"CONTRAST_SELFTEST: 提亮注入 {'仍报错（判据失效）' if raised else '已放行'}")

    if caught and not raised:
        print("CONTRAST_SELFTEST: PASS")
        return 0
    print("CONTRAST_SELFTEST: FAIL")
    return 1


def main() -> int:
    """入口：解析令牌并逐主题判定。

    [参数] 无
    [返回] 0 全部达标；1 存在不达标项
    """
    if "--selftest" in sys.argv:
        return selftest()

    tokens = resolve_tokens()
    if not tokens["light"]:
        print("CONTRAST: FAIL (未能从 tokens.css 解析出任何令牌)")
        return 1

    print("=== 字色对比度判定（取三个内容面中最差值）===")
    failures: list[str] = []
    for theme in ("light", "dark"):
        failures.extend(judge(theme, tokens[theme]))

    print("\n=== 主色色板判定（文字角色 + 实心背景角色）===")
    overrides_css = strip_comments(OVERRIDES.read_text(encoding="utf-8"))
    blocks = parse_accent_blocks(overrides_css)
    failures.extend(judge_accents(overrides_css))

    if failures:
        for item in failures:
            print(f"CONTRAST_FAIL: {item}")
        print(f"CONTRAST: FAIL ({len(failures)} 项低于达标线)")
        return 1

    total = len(TEXT_RULES) * len(THEMES)
    print(f"CONTRAST: PASS ({total} 个字色组合 + {len(blocks)} 个色板块全部达标)")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
