"""从上游冻结样式派生「字号标度」覆盖块，让全站字号只有一处真相。

[判据] 扫描 `src/styles/` 下五个样式文件（`base`/`components`/`instruments`/`layout`/`pages`）
       的全部 `font-size` 声明，把 10–15px 区间的 21 种散值归并到 5 档令牌：
       `caption` 12 / `sm` 13 / `body` 14 / `lg` 15 / `title` 16。
       归并原则是「相邻 0.5px 档位合并」——10 与 10.5、11 与 11.5 这类差距在屏幕上本就
       无法分辨，是设计稿标注残留，不是刻意的层次。整体在此基础上上移一档，并把下限兜到 12px。
       16px 以上不进标度：大字区不承担「读不清」的问题，改动只有风险没有收益。
[边界] 只生成覆盖层，不改冻结样式一个字节。媒体查询块整体排除在扫描外（当前块内只有
       22px 与 44px 两处，都大于 15px）；一旦未来媒体查询里出现标度范围内字号，脚本直接报错，
       不静默漏掉——媒体查询必须保留断点上下文，平铺覆盖会放大作用范围。
[用法]
    python -X utf8 -B frontend-design/scripts/build_font_overrides.py           # 写入覆盖层
    python -X utf8 -B frontend-design/scripts/build_font_overrides.py --check   # 只校验是否同步
[返回] 退出码 0=同步；1=覆盖层与冻结源不一致，或媒体查询内出现标度范围内字号。
最近修改时间：2026-10-31 21:45:00；改动原因：由「非整数字号整数化」升级为「字号标度化 + 基准 13→14」，
  解除 REQ-FONT-CLARITY-001 的 BOUND-05（原冻结「不调整 13px 基准」），决策见 doc/2-需求/。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "component-library"
STYLES = LIB / "src" / "styles"
OVERRIDES = STYLES / "overrides.css"

STYLE_FILES = ["base.css", "components.css", "instruments.css", "layout.css", "pages.css"]

# 原字号 → 令牌名。相邻 0.5px 档位合并，整体上移一档。
SCALE = {
    "10": "caption", "10.5": "caption", "11": "caption",
    "11.5": "sm", "12": "sm",
    "12.5": "body", "13": "body",
    "13.5": "lg", "14": "lg",
    "14.5": "title", "15": "title",
}

# 字号三档：每档显式给整数，不用 calc 缩放——1.1 倍会算出 15.4px 半像素，
# 与「字号必须整数」的验收条件冲突。regular 是缺省档，也是无 data-font-scale 时的取值。
# 三档的 caption 一律不低于 12px：12px 是「辅助字号下限」这条验收条件本身，
# 不能因为用户选了紧凑档就破例，否则同一套系统里会存在两个不同的可读性底线。
SCALE_SETS = {
    "compact": [("caption", "12px"), ("sm", "12px"), ("body", "13px"), ("lg", "14px"), ("title", "15px")],
    "regular": [("caption", "12px"), ("sm", "13px"), ("body", "14px"), ("lg", "15px"), ("title", "16px")],
    "large": [("caption", "13px"), ("sm", "14px"), ("body", "15px"), ("lg", "16px"), ("title", "17px")],
}
DEFAULT_SCALE = "regular"
TOKEN_NAMES = [name for name, _value in SCALE_SETS[DEFAULT_SCALE]]

# 机械映射只看原值，会把「本来就靠 0.5px 差 0.5px 撑层次」的成对角色压成同一档，
# 反而丢掉语义。这里只修正那些压平后明显错的：表单校验提示必须弱于字段标签。
ROLE_OVERRIDES = {
    ".field-hint": "caption",
    ".field-error": "caption",
}

BEGIN = "/* BEGIN GENERATED: type scale overrides */"
END = "/* END GENERATED: type scale overrides */"

# 旧版「非整数字号整数化」块。它与新标度块会给同一批选择器写出不同字号
# （如 10.5px 旧版落 11px、新版落 12px），并存必然互相矛盾，必须迁移掉。
LEGACY_BEGIN = "/* BEGIN GENERATED: fractional font-size overrides */"
LEGACY_END = "/* END GENERATED: fractional font-size overrides */"

MEDIA_RE = re.compile(r"@media[^{]*\{")


def strip_comments(css: str) -> str:
    """去掉 CSS 注释，避免注释里的示例声明被当作真实规则。"""
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def split_media(css: str) -> tuple[str, list[str], list[str]]:
    """把样式拆成「非媒体查询部分」与「媒体查询块列表」。

    [参数] css 已去注释的样式文本
    [返回] (可覆盖部分, 媒体查询块原文列表, 媒体查询块内字号值列表)
    """
    plain_parts: list[str] = []
    media_blocks: list[str] = []
    media_sizes: list[str] = []
    cursor = 0
    while True:
        match = MEDIA_RE.search(css, cursor)
        if not match:
            plain_parts.append(css[cursor:])
            break
        plain_parts.append(css[cursor : match.start()])
        depth = 1
        index = match.end()
        while index < len(css) and depth > 0:
            if css[index] == "{":
                depth += 1
            elif css[index] == "}":
                depth -= 1
            index += 1
        block = css[match.end() : index - 1]
        media_blocks.append(block)
        media_sizes.extend(re.findall(r"font-size:\s*([\d.]+)px", block))
        cursor = index
    return " ".join(plain_parts), media_blocks, media_sizes


def collect() -> dict[str, str]:
    """按选择器收集目标令牌，同名选择器以后出现者为准（与浏览器层叠一致）。

    [参数] 无
    [返回] 选择器 → 令牌名 的映射；只含标度范围内的声明
    """
    latest: dict[str, str] = {}
    for name in STYLE_FILES:
        path = STYLES / name
        if not path.exists():
            continue
        plain, _blocks, media_sizes = split_media(strip_comments(path.read_text(encoding="utf-8")))
        offenders = [s for s in media_sizes if s in SCALE]
        if offenders:
            raise SystemExit(
                f"FONT_OVERRIDES: FAIL ({name} 的媒体查询里出现标度范围内字号 {offenders}，"
                "平铺覆盖会放大作用范围，需要先扩展脚本支持断点上下文)"
            )
        for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", plain):
            body = match.group(2)
            sizes = re.findall(r"font-size:\s*([\d.]+)px", body)
            if not sizes:
                continue
            selector = " ".join(match.group(1).split())
            if not selector or selector.startswith("@"):
                continue
            value = sizes[-1]
            if value in SCALE:
                latest[selector] = ROLE_OVERRIDES.get(selector, SCALE[value])
    return latest


def render(mapping: dict[str, str]) -> str:
    """渲染覆盖块：令牌定义在前，逐选择器覆盖在后。

    [参数] mapping 选择器 → 令牌名
    [返回] 完整块文本（含 BEGIN/END 标记）
    """
    lines = [BEGIN]
    lines.append("/* 字号标度：上游冻结样式在 10–15px 区间有 21 种散值，这里归并为 5 档令牌；")
    lines.append("   相邻 0.5px 档位合并（视觉本就无法分辨），整体上移一档，下限兜到 12px。")
    lines.append("   16px 以上不进标度。本段由 scripts/build_font_overrides.py 自动派生，请勿手改。 */")
    lines.append(":root,")
    lines.append(f'[data-font-scale="{DEFAULT_SCALE}"] {{')
    for name, value in SCALE_SETS[DEFAULT_SCALE]:
        lines.append(f"  --fs-{name}: {value};")
    lines.append("}")
    for scale in ("compact", "large"):
        lines.append("")
        lines.append(f"/* {scale} 档：打在任意容器上即对该子树生效 */")
        lines.append(f'[data-font-scale="{scale}"] {{')
        for name, value in SCALE_SETS[scale]:
            lines.append(f"  --fs-{name}: {value};")
        lines.append("}")
    for name in TOKEN_NAMES:
        selectors = sorted(sel for sel, token in mapping.items() if token == name)
        if not selectors:
            continue
        lines.append("")
        lines.append(f"/* {name} */")
        for selector in selectors:
            lines.append(f"{selector} {{ font-size: var(--fs-{name}); }}")
    lines.append(END)
    return "\n".join(lines)


def strip_legacy(text: str) -> str:
    """移除旧版「非整数字号整数化」块。

    [参数] text 覆盖层全文
    [返回] 去掉旧块后的文本；旧块不存在时原样返回
    """
    if LEGACY_BEGIN in text and LEGACY_END in text:
        head, rest = text.split(LEGACY_BEGIN, 1)
        tail = rest.split(LEGACY_END, 1)[1]
        return head + tail
    return text


def main(argv: list[str]) -> int:
    """入口：写入或校验覆盖块。

    [参数] argv 命令行参数，含 `--check` 时只校验
    [返回] 0 表示同步；1 表示失配
    """
    check = "--check" in argv
    mapping = collect()
    block = render(mapping)
    text = OVERRIDES.read_text(encoding="utf-8")

    if check:
        if LEGACY_BEGIN in text:
            print("FONT_OVERRIDES: FAIL (旧版整数化块仍在，会与新标度块写出矛盾字号)")
            print("HINT: python -X utf8 -B frontend-design/scripts/build_font_overrides.py")
            return 1
        if BEGIN not in text or END not in text:
            print("FONT_OVERRIDES: FAIL (generated block missing)")
            return 1
        current = text.split(BEGIN, 1)[1].split(END, 1)[0]
        expected = block.split(BEGIN, 1)[1].split(END, 1)[0]
        if current.strip() != expected.strip():
            print("FONT_OVERRIDES: FAIL (block out of sync with frozen styles)")
            print("HINT: python -X utf8 -B frontend-design/scripts/build_font_overrides.py")
            return 1
        groups = len({token for token in mapping.values()})
        print(f"FONT_OVERRIDES: PASS ({len(mapping)} selectors, {groups} size groups)")
        return 0

    text = strip_legacy(text)
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        tail = rest.split(END, 1)[1]
        text = head + block + tail
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    OVERRIDES.write_text(text, encoding="utf-8")
    groups = len({token for token in mapping.values()})
    print(f"FONT_OVERRIDES: WROTE ({len(mapping)} selectors, {groups} size groups)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
