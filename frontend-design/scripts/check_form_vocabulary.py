#!/usr/bin/env python3
"""表单词汇守卫：三块本地补齐的表单形态必须留在覆盖层，且不许长出第二层描边。

[为什么需要] 2026-11 复盘了一套后台的组件缺陷，那里暴露的问题组件库答对了三个
（单层描边、标签不塌、空态不画灰盒），真正缺的是三种真实表单形态的词汇：数量带单位、
选一个文件、危险操作要手抄确认。缺词汇的代价不是画错，而是每个业务方各写一套——
单位靠 span 硬凑、原生 file 控件裸奔、危险区拿红按钮代替确认。这些词汇补在
`overrides.css`，冻结层零改动；但补出来的东西没有任何组件引用，删掉不会有测试红，
所以必须有一道守卫盯着它还在不在。

[判据] 四组：
  ① 词汇齐备：三块形态的关键规则与关键属性都还在覆盖层里；
  ② 词汇不外溢：本地独占的类名不许出现在七个冻结样式层——那意味着有人绕开覆盖层
     直接改上游，逐字节一致会立刻破；
  ③ 单层描边不变量：外壳变体的内层 input 不许补 border / border-radius /
     box-shadow / background。冻结层已给内层 border:0，补回去就是「药丸套药丸」；
  ④ 两条基线不许倒退：`.empty` 不许回到虚线灰盒，`.page.is-contained` 必须同时
     有 max-width 与 margin-inline（缺 margin-inline 就是宽屏下贴左留一条死白）。

[边界] 只判「词汇在不在、有没有越界」，不判配色与间距取值好不好看——那要靠真机截图。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES = ROOT / "component-library" / "src" / "styles"
OVERRIDES = STYLES / "overrides.css"

# 本地独占词汇：只允许出现在覆盖层
LOCAL_VOCABULARY = ("is-unit", "shell-affix", "is-file", "danger-zone", "is-contained", "content-max")

# 必须存在的关键规则 → 该规则体内必须出现的属性
REQUIRED_RULES: dict[str, tuple[str, ...]] = {
    ".input-shell.is-unit": ("min-width", "gap"),
    ".shell-affix": ("flex", "font-size", "color"),
    ".input-shell.is-file": ("height", "min-height", "padding"),
    '.input-shell.is-file > input[type="file"]': ("height", "padding"),
    '.input-shell.is-file > input[type="file"]::file-selector-button': ("border", "border-radius", "background"),
    ".danger-zone": ("padding", "background", "box-shadow"),
    ".danger-zone .field": ("max-width",),
    ".page.is-contained": ("max-width", "margin-inline"),
}

# 内层控件：只提供内容与光标，描边一律归外壳
INNER_SELECTORS = (".input-shell.is-unit > input", '.input-shell.is-file > input[type="file"]')
INNER_FORBIDDEN = ("border", "border-radius", "box-shadow", "background")

RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")
PROP_RE = re.compile(r"(--?[a-z0-9-]+|[a-z-]+)\s*:")


def rules_of(css: str) -> dict[str, str]:
    """[参数] css 样式文本 [返回] 选择器 → 规则体（同选择器多次出现时后者覆盖前者）。"""
    out: dict[str, str] = {}
    for m in RULE_RE.finditer(strip_comments(css)):
        selector = " ".join(m.group(1).split())
        out[selector] = m.group(2)
    return out


def props_of(body: str) -> set[str]:
    """[参数] 规则体 [返回] 该体内出现的属性名集合（去掉前导 --）。"""
    return {name.lstrip("-") for name in PROP_RE.findall(body)}


def strip_comments(css: str) -> str:
    """[参数] css 样式文本 [返回] 去掉注释后的文本（注释里的花括号会打乱规则切分）。"""
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def check_required(rules: dict[str, str]) -> list[str]:
    """[参数] 覆盖层规则表 [返回] 缺失的规则或属性说明。"""
    problems: list[str] = []
    for selector, wanted in REQUIRED_RULES.items():
        body = rules.get(selector)
        if body is None:
            problems.append(f"MISSING_RULE     {selector}")
            continue
        have = props_of(body)
        for prop in wanted:
            if prop not in have:
                problems.append(f"MISSING_PROP     {selector} :: {prop}")
    return problems


def check_no_overflow() -> list[str]:
    """[返回] 冻结样式层里出现本地独占词汇的位置。"""
    problems: list[str] = []
    for path in sorted(STYLES.glob("*.css")):
        if path.name == OVERRIDES.name:
            continue
        text = strip_comments(path.read_text(encoding="utf-8"))
        for word in LOCAL_VOCABULARY:
            for line_no, line in enumerate(text.splitlines(), 1):
                if word in line:
                    problems.append(f"LEAKED_LAYER     src/styles/{path.name}:{line_no} :: {word} :: {line.strip()[:60]}")
    return problems


def check_single_border(rules: dict[str, str]) -> list[str]:
    """[参数] 覆盖层规则表 [返回] 内层控件被补上描边的规则。"""
    problems: list[str] = []
    for selector in INNER_SELECTORS:
        body = rules.get(selector)
        if body is None:
            problems.append(f"MISSING_RULE     {selector}")
            continue
        have = props_of(body)
        for prop in INNER_FORBIDDEN:
            if prop in have:
                problems.append(f"DOUBLE_BORDER    {selector} :: 不许出现 {prop}，描边与背景归外壳")
    return problems


def check_baselines(rules: dict[str, str]) -> list[str]:
    """[参数] 覆盖层规则表 [返回] 两条视觉基线被改回去的说明。"""
    problems: list[str] = []
    empty = rules.get(".empty")
    if empty is not None:
        for word in ("dashed", "groove-bg", "groove-inset"):
            if word in empty:
                problems.append(f"GRAY_BOX         .empty 又变回灰盒子（含 {word}），空态应当是留白 + 图标")
    contained = rules.get(".page.is-contained") or ""
    if "margin-inline" in props_of(contained) and "auto" not in contained:
        problems.append("NOT_CENTERED     .page.is-contained 的 margin-inline 不是 auto，宽屏下会贴左")
    return problems


def selftest() -> int:
    """[返回] 0 表示四组判据都能抓到对应的坏样本。"""
    ok = True

    broken = rules_of(OVERRIDES.read_text(encoding="utf-8"))
    broken = dict(broken)
    broken.pop(".shell-affix", None)
    if not check_required(broken):
        print("SELFTEST FAIL  删掉 .shell-affix 规则没有被抓到")
        ok = False

    broken = dict(rules_of(OVERRIDES.read_text(encoding="utf-8")))
    broken[".input-shell.is-unit > input"] += " border: 1px solid red;"
    if not check_single_border(broken):
        print("SELFTEST FAIL  给内层 input 补 border 没有被抓到")
        ok = False

    broken = dict(rules_of(OVERRIDES.read_text(encoding="utf-8")))
    broken[".empty"] = "border: 1px dashed rgba(0,0,0,.2);"
    if not check_baselines(broken):
        print("SELFTEST FAIL  .empty 改回虚线灰盒没有被抓到")
        ok = False

    if check_no_overflow():
        print("SELFTEST FAIL  当前冻结层本不该有本地词汇，却报了泄漏")
        ok = False

    print("FORM_VOCABULARY_SELFTEST: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()

    if not OVERRIDES.exists():
        print(f"FORM_VOCABULARY: FAIL（找不到 {OVERRIDES}）")
        return 1

    rules = rules_of(OVERRIDES.read_text(encoding="utf-8"))
    problems = (
        check_required(rules)
        + check_no_overflow()
        + check_single_border(rules)
        + check_baselines(rules)
    )

    if problems:
        print(f"FORM_VOCABULARY: FAIL（{len(problems)} 处）")
        for item in problems:
            print(f"  {item}")
        return 1

    print(
        "FORM_VOCABULARY: PASS（"
        f"{len(REQUIRED_RULES)} 组词汇齐备；冻结层零泄漏；内层单层描边；空态与居中基线未倒退）"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
