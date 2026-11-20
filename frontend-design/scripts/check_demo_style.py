#!/usr/bin/env python3
"""示例层视觉一致性：示例里的内联样式必须成材，不能只刷一层背景色。

[为什么需要] 示例卡是组件库的脸面，不是调试沙盘。`demo-slots.ts` 里曾用
`style: 'padding:8px;background:var(--blue-soft)'` 拼栅格占位块——没有圆角、没有描边、
没有材质，在一屏玻璃/面板里看着像调试残留，用户一眼就指出「和我们的风格不一致」。

[判据] 示例层的内联 style 里出现 `background`，必须同时给出 `border-radius`（或整体
交给 `.m-*` 材质类）。只刷背景不带形状的，一律判为裸色块。

[边界] 只管示例层（`src/views/gallery/*.ts`）。组件自身的样式走另一套守卫
（材质、投影、对比度），不在这里重复判定。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMO = ROOT / "component-library" / "src" / "views" / "gallery"

# 内联 style 字符串字面量（单引号或反引号，允许内部有转义）
STYLE_LITERAL = re.compile(r"style\s*:\s*(['\"`])((?:\\.|(?!\1).)*)\1", re.S)
HAS_BG = re.compile(r"background(?:-color)?\s*:", re.I)
HAS_SHAPE = re.compile(r"border-radius\s*:|border\s*:|class\s*:", re.I)


def scan(path: Path) -> list[tuple[int, str]]:
    """[参数] 文件路径 [返回] [(行号, 摘录)]：只刷背景没有形状的内联样式。"""
    text = path.read_text(encoding="utf-8")
    bad: list[tuple[int, str]] = []
    for m in STYLE_LITERAL.finditer(text):
        body = m.group(2)
        if not HAS_BG.search(body):
            continue
        if HAS_SHAPE.search(body):
            continue
        line = text[: m.start()].count("\n") + 1
        bad.append((line, body.strip()[:70]))
    return bad


def main() -> int:
    if not DEMO.exists():
        print(f"DEMO_STYLE: SKIP（示例目录不存在 {DEMO}）")
        return 0

    problems: list[tuple[str, int, str]] = []
    for path in sorted(DEMO.glob("*.ts")):
        for line, body in scan(path):
            problems.append((path.name, line, body))

    if problems:
        print(f"DEMO_STYLE: FAIL（{len(problems)} 处内联背景缺少形状，示例会看起来像调试占位）")
        for name, line, body in problems:
            print(f"  {name}:{line}  {body}")
        print("  修法：补 border-radius，或改用库内材质类（如 .m-groove）。")
        return 1

    print("DEMO_STYLE: PASS（示例层无裸色块）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
