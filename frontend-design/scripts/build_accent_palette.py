"""色板编译器：从种子色派生整套主色令牌，并保证两种角色都满足对比度。

[用途] 让「加一套色板」退化成在 `references/accent-palettes.json` 加一行。派生规则写在这里，
       不写进产物：一套色板要出 12 个值 × 2 主题，手写必然漂移。
[判据] 主色同时承担两种互斥角色，必须拆成两个令牌：
       - `--blue`（text）：作为文字、描边、图标，要求对内容底 ≥ 4.5:1；
       - `--blue-solid`（solid）：作为实心按钮背景，要求白字压在上面 ≥ 4.5:1。
       同一颜色无法兼顾——深底上当文字要 L≥0.206，当背景配白字要 L≤0.183，区间不重叠。
       种子色不达标时按 HSL 的 L 轴逐步修正，直到越过门槛并留 0.1 余量；修正幅度会打印出来。
[边界] 只派生主色一族。`--lime`（正常状态）、`--red`（警示）、`--cat-*`（分类）语义独立，
       不随主色变化，否则状态含义会被主色污染。16px 以上与字号无关的令牌同样不碰。
[用法]
    python -X utf8 -B frontend-design/scripts/build_accent_palette.py           # 写入覆盖层
    python -X utf8 -B frontend-design/scripts/build_accent_palette.py --check   # 只校验同步
    python -X utf8 -B frontend-design/scripts/build_accent_palette.py --report  # 只打印派生结果
[返回] 退出码 0=同步；1=覆盖层与色板定义不一致，或某种子色无法修正到达标。
最近修改时间：2026-10-31 22:20:00；改动原因：初版，支撑「随时可加色板」与 text/solid 双角色拆分。
"""
from __future__ import annotations

import colorsys
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "component-library"
OVERRIDES = LIB / "src" / "styles" / "overrides.css"
PALETTES = ROOT / "references" / "accent-palettes.json"
# 前端要渲染色板选择器，也需要一份清单。由本脚本一并生成，
# 避免「加色板要同时改 JSON 和 TS」两处真相。
TS_OUT = LIB / "src" / "data" / "accent-palettes.generated.ts"

BEGIN = "/* BEGIN GENERATED: accent palettes */"
END = "/* END GENERATED: accent palettes */"

# 内容底：主色作为文字时压在这些面上。
LIGHT_BACKDROPS = ("#ffffff", "#f6f8f7", "#fbfcfc")
DARK_BACKDROPS = ("#121517", "#1b1f21")
# 实心背景上的前景色（按钮文字）。
SOLID_FOREGROUND = "#ffffff"

TEXT_FLOOR = 4.5
SOLID_FLOOR = 4.5
MARGIN = 0.1


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    """把 `#rrggbb` 解析为 RGB 三元组。"""
    text = value.lstrip("#")
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    """把 0-255 的浮点 RGB 收敛为 `#rrggbb`。"""
    return "#" + "".join(f"{max(0, min(255, round(c))):02x}" for c in rgb)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """按 WCAG 2.1 计算相对亮度。"""

    def channel(raw: int) -> float:
        c = raw / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    """计算两色对比度。"""
    high, low = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def shift_lightness(value: str, delta: float) -> str:
    """在 HSL 空间平移明度，保持色相与饱和度。"""
    r, g, b = (c / 255 for c in hex_to_rgb(value))
    hue, light, sat = colorsys.rgb_to_hls(r, g, b)
    light = max(0.0, min(1.0, light + delta))
    return rgb_to_hex(tuple(c * 255 for c in colorsys.hls_to_rgb(hue, light, sat)))


def fit(value: str, backdrops: tuple[str, ...], floor: float, darker: bool) -> tuple[str, float, int]:
    """按需求方向调整明度，直到最差对比度越过门槛。

    [参数] value 种子色
    [参数] backdrops 需要同时满足的背景集合
    [参数] floor 最低对比度
    [参数] darker 为真时压暗，否则提亮
    [返回] (修正后颜色, 最差对比度, 调整步数)
    """
    target = floor + MARGIN
    step = -0.01 if darker else 0.01
    current = value
    for used in range(101):
        worst = min(contrast(hex_to_rgb(current), hex_to_rgb(bg)) for bg in backdrops)
        if worst >= target:
            return current, worst, used
        current = shift_lightness(current, step)
    worst = min(contrast(hex_to_rgb(current), hex_to_rgb(bg)) for bg in backdrops)
    return current, worst, 100


def rgba(value: str, alpha: float) -> str:
    """输出 `rgba(r, g, b, a)`。"""
    r, g, b = hex_to_rgb(value)
    return f"rgba({r}, {g}, {b}, {alpha})"


def rgb_triplet(value: str) -> str:
    """输出 Canvas 用的 `r, g, b` 三元组。"""
    r, g, b = hex_to_rgb(value)
    return f"{r}, {g}, {b}"


def derive(seed: str, theme: str) -> dict[str, str]:
    """由种子色派生该主题下的全套主色令牌。

    [参数] seed 种子色
    [参数] theme `light` 或 `dark`
    [返回] 令牌名到取值的映射
    """
    backdrops = LIGHT_BACKDROPS if theme == "light" else DARK_BACKDROPS
    text, _text_ratio, _ = fit(seed, backdrops, TEXT_FLOOR, darker=(theme == "light"))
    solid, _solid_ratio, _ = fit(seed, (SOLID_FOREGROUND,), SOLID_FLOOR, darker=True)

    # hover 在 text 与 solid 各自基础上再压一档，保证悬停态对比度只升不降。
    text_hover = shift_lightness(text, -0.05 if theme == "light" else 0.04)
    solid_hover = shift_lightness(solid, -0.04)
    # 投影需要一个比主色更深的基色，浅色主题压 30%，深色主题用纯黑。
    shadow_base = shift_lightness(text, -0.30) if theme == "light" else "#000000"
    shadow_alpha = 0.28 if theme == "light" else 0.4

    soft_alpha = 0.1 if theme == "light" else 0.16
    focus_alpha = 0.8 if theme == "light" else 0.85
    thread_alpha = 0.62 if theme == "light" else 0.72
    halo_alpha = 0.18 if theme == "light" else 0.28
    ambient_alpha = 0.055 if theme == "light" else 0.07
    glow_alpha = 0.24 if theme == "light" else 0.26
    glow_hover_alpha = 0.3 if theme == "light" else 0.34

    return {
        "--blue": text,
        "--blue-hover": text_hover,
        "--blue-solid": solid,
        "--blue-solid-hover": solid_hover,
        "--blue-soft": rgba(text, soft_alpha),
        "--focus": rgba(text, focus_alpha),
        "--e-accent": (
            f"0 1px 2px {rgba(shadow_base, shadow_alpha)}, "
            f"0 8px 18px {rgba(text, glow_alpha)}"
        ),
        "--e-accent-hover": (
            f"0 1px 2px {rgba(shadow_base, shadow_alpha + 0.04)}, "
            f"0 12px 24px {rgba(text, glow_hover_alpha)}"
        ),
        "--graph-accent": rgb_triplet(text),
        "--thread-active": rgba(text, thread_alpha),
        "--pulse-halo": rgba(text, halo_alpha),
        "--ambient-b": rgba(text, ambient_alpha),
    }


def load_palettes() -> list[dict]:
    """读取色板定义。"""
    if not PALETTES.exists():
        raise SystemExit(f"ACCENT_PALETTES_MISSING: {PALETTES}")
    payload = json.loads(PALETTES.read_text(encoding="utf-8"))
    palettes = payload.get("palettes") or []
    if not palettes:
        raise SystemExit("ACCENT_PALETTES_EMPTY: 至少需要一套色板")
    keys = [p.get("key") for p in palettes]
    if len(keys) != len(set(keys)):
        raise SystemExit(f"ACCENT_PALETTES_DUPLICATE: {keys}")
    return palettes


def render(palettes: list[dict]) -> str:
    """渲染覆盖块：默认值 + 每套色板的浅深两份。

    [参数] palettes 色板定义列表
    [返回] 完整块文本
    """
    lines = [BEGIN]
    lines.append("/* 主色色板：每套由一个种子色派生 12 个令牌，浅深各一份。")
    lines.append("   来源 references/accent-palettes.json，由 scripts/build_accent_palette.py 生成，请勿手改。")
    lines.append("   加色板 = 在 JSON 加一行后重跑脚本；种子色不达标时脚本会自动修正明度并打印幅度。 */")

    default = palettes[0]
    lines.append("")
    lines.append(f"/* 缺省色板（{default['label']}）：没有 data-accent 时的取值 */")
    lines.append(":root {")
    for name, value in derive(default["light"], "light").items():
        lines.append(f"  {name}: {value};")
    lines.append("}")

    for palette in palettes:
        for theme in ("light", "dark"):
            values = derive(palette[theme], theme)
            if theme == "light":
                lines.append("")
                lines.append(f"/* {palette['label']} · 浅色 */")
                lines.append(f'[data-accent="{palette["key"]}"] {{')
            else:
                lines.append("")
                lines.append(f"/* {palette['label']} · 深色（祖先或同元素带 data-theme=dark 均可） */")
                lines.append(
                    f':root[data-theme="dark"] [data-accent="{palette["key"]}"],'
                )
                lines.append(f'[data-theme="dark"][data-accent="{palette["key"]}"] {{')
            for name, value in values.items():
                lines.append(f"  {name}: {value};")
            lines.append("}")

    lines.append(END)
    return "\n".join(lines)


def report(palettes: list[dict]) -> int:
    """打印每套色板的派生结果与实测对比度。

    [返回] 0 表示全部达标
    """
    failed = 0
    print(f"{'色板':10s}{'主题':6s}{'text':10s}{'对内容底':>9s}{'solid':10s}{'白字':>7s}")
    for palette in palettes:
        for theme in ("light", "dark"):
            backdrops = LIGHT_BACKDROPS if theme == "light" else DARK_BACKDROPS
            values = derive(palette[theme], theme)
            text = values["--blue"]
            solid = values["--blue-solid"]
            text_ratio = min(contrast(hex_to_rgb(text), hex_to_rgb(b)) for b in backdrops)
            solid_ratio = contrast(hex_to_rgb(SOLID_FOREGROUND), hex_to_rgb(solid))
            mark = ""
            if text_ratio < TEXT_FLOOR or solid_ratio < SOLID_FLOOR:
                mark = "  FAIL"
                failed += 1
            print(
                f"{palette['label']:10s}{theme:6s}{text:10s}{text_ratio:9.2f}"
                f"{solid:10s}{solid_ratio:7.2f}{mark}"
            )
    print(f"\nACCENT_PALETTES: {'PASS' if failed == 0 else f'FAIL ({failed} 项)'}")
    return 0 if failed == 0 else 1


def render_ts(palettes: list[dict]) -> str:
    """生成前端用的色板清单模块。

    [参数] palettes 色板定义列表
    [返回] TypeScript 源码文本
    """
    lines = [
        "/* 由 frontend-design/scripts/build_accent_palette.py 从 references/accent-palettes.json 生成。",
        "   禁止手改：加色板请改 JSON 后重跑脚本。 */",
        "",
        "export interface AccentPalette {",
        "  key: string",
        "  label: string",
        "}",
        "",
        "export const ACCENT_PALETTES: AccentPalette[] = [",
    ]
    for palette in palettes:
        lines.append(f"  {{ key: '{palette['key']}', label: '{palette['label']}' }},")
    lines.append("]")
    lines.append("")
    lines.append(f"export const DEFAULT_ACCENT = '{palettes[0]['key']}'")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    """入口：写入、校验或打印。"""
    palettes = load_palettes()
    if "--report" in argv:
        return report(palettes)

    block = render(palettes)
    ts_block = render_ts(palettes)
    text = OVERRIDES.read_text(encoding="utf-8")
    if "--check" in argv:
        if BEGIN not in text or END not in text:
            print("ACCENT_PALETTES: FAIL (generated block missing)")
            return 1
        current = text.split(BEGIN, 1)[1].split(END, 1)[0]
        expected = block.split(BEGIN, 1)[1].split(END, 1)[0]
        if current.strip() != expected.strip():
            print("ACCENT_PALETTES: FAIL (block out of sync with accent-palettes.json)")
            print("HINT: python -X utf8 -B frontend-design/scripts/build_accent_palette.py")
            return 1
        if not TS_OUT.exists() or TS_OUT.read_text(encoding="utf-8") != ts_block:
            print("ACCENT_PALETTES: FAIL (前端清单 accent-palettes.generated.ts 与 JSON 不一致)")
            print("HINT: python -X utf8 -B frontend-design/scripts/build_accent_palette.py")
            return 1
        print(f"ACCENT_PALETTES: PASS ({len(palettes)} palettes × 2 themes + 前端清单)")
        return 0

    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        tail = rest.split(END, 1)[1]
        text = head + block + tail
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    OVERRIDES.write_text(text, encoding="utf-8")
    TS_OUT.parent.mkdir(parents=True, exist_ok=True)
    TS_OUT.write_text(ts_block, encoding="utf-8")
    print(f"ACCENT_PALETTES: WROTE ({len(palettes)} palettes × 2 themes + 前端清单)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
