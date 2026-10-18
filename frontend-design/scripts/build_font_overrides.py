"""从上游冻结样式里派生「非整数字号」选择器清单，生成覆盖层规则并做同步校验。

[判据] 只读 src/styles/*.css（139 文件冻结面内），提取所有带非整数字号的规则选择器；
  映射表固定：10.5→11、11.5→12、12.5→13、13.5→14、14.5→15，全部落到整数像素。
[用法]
    python -X utf8 -B frontend-design/scripts/build_font_overrides.py           # 写入覆盖层
    python -X utf8 -B frontend-design/scripts/build_font_overrides.py --check   # 只校验是否同步
[返回] 退出码 0=同步；1=覆盖层与冻结源不一致（上游新增/删除了非整数字号）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "component-library"
STYLES = LIB / "src" / "styles"
OVERRIDES = STYLES / "overrides.css"

FROZEN_FILES = ["components.css", "instruments.css", "layout.css", "pages.css"]
# 非整数 → 整数：就近取整，辅助字号因此提到 12px 下限
ROUND = {
    "10.5": "11px",
    "11.5": "12px",
    "12.5": "13px",
    "13.5": "14px",
    "14.5": "15px",
}
BEGIN = "/* BEGIN GENERATED: fractional font-size overrides */"
END = "/* END GENERATED: fractional font-size overrides */"


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def collect():
    """按目标字号归组选择器；同一选择器只保留一次。"""
    groups = {}
    for name in FROZEN_FILES:
        css = strip_comments((STYLES / name).read_text(encoding="utf-8"))
        for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
            body = match.group(2)
            size = re.search(r"font-size:\s*(\d+\.\d+)px", body)
            if not size or size.group(1) not in ROUND:
                continue
            selector = " ".join(match.group(1).split())
            if not selector or selector.startswith("@"):
                continue
            groups.setdefault(ROUND[size.group(1)], set()).add(selector)
    return groups


def render(groups):
    lines = [BEGIN]
    lines.append("/* 上游冻结样式里的非整数字号会让字形落在半像素栅格上；")
    lines.append("   本段由 scripts/build_font_overrides.py 从冻结源自动派生，请勿手改。")
    lines.append("   映射：10.5→11 / 11.5→12 / 12.5→13 / 13.5→14 / 14.5→15（px）。 */")
    for target in sorted(groups, key=lambda s: float(s[:-2])):
        sels = sorted(groups[target])
        lines.append(f"{',\n'.join(sels)} {{")
        lines.append(f"  font-size: {target};")
        lines.append("}")
    lines.append(END)
    return "\n".join(lines)


def main(argv):
    check = "--check" in argv
    groups = collect()
    block = render(groups)
    text = OVERRIDES.read_text(encoding="utf-8")

    if check:
        if BEGIN not in text or END not in text:
            print("FONT_OVERRIDES: FAIL (generated block missing)")
            return 1
        current = text.split(BEGIN, 1)[1].split(END, 1)[0]
        expected = block.split(BEGIN, 1)[1].split(END, 1)[0]
        if current.strip() != expected.strip():
            print("FONT_OVERRIDES: FAIL (block out of sync with frozen styles)")
            print("HINT: python -X utf8 -B frontend-design/scripts/build_font_overrides.py")
            return 1
        total = sum(len(v) for v in groups.values())
        print(f"FONT_OVERRIDES: PASS ({total} selectors, {len(groups)} size groups)")
        return 0

    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        tail = rest.split(END, 1)[1]
        text = head + block + tail
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    OVERRIDES.write_text(text, encoding="utf-8")
    total = sum(len(v) for v in groups.values())
    print(f"FONT_OVERRIDES: WROTE ({total} selectors, {len(groups)} size groups)")
    return 0


sys.exit(main(sys.argv[1:]))
