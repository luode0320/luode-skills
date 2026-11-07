#!/usr/bin/env python3
"""浮层入场统一：组件不得绕过 overlayMenuEnter 直接指定入场形态。

[为什么需要] `overlayEnter` 的两个分支差别极大，而且**对应两种不同的语义**：
- `pop`：`y -6 + scale 0.98`，缩放幅度 1.4%，实测等同于没有动画——只有淡入。
- `modal`：从面板几何算轴心、`scale 0.86`、`expo.out` 380ms，长尾明显（262ms 才到 0.995）。

菜单/下拉这两个分支都不合适：用 `pop` 等于没动画；用 `modal` 则轴心可能落在面板中部、
收尾拖沓。所以本地在 `morph.ts` 包了 `overlayMenuEnter` / `overlayMenuLeave`：
按面板里**有没有可操作项**分派，内容面板走「顶边轴心 + 280ms + power4.out + will-change」
的优化版缩放，纯文字提示走上游 `pop`。

[判据] 组件里出现 `overlayEnter(..., '<kind>')` / `overlayLeave(..., '<kind>')` 即为绕过规则。

[豁免] 真正的弹窗与遮罩层——它们从中心升起、铺满视口，`modal` 分支正是为此设计的：
- `ui/Drawer.vue`：抽屉，用 `drawer` 分支的共享元素 ghost，不能被菜单形态替代

弹窗与图片预览不需要豁免：它们走 `overlayDialogEnter`，与菜单同一套参数规格、只换轴心。
- `composables/morph.ts`：分派实现自身
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "component-library" / "src"

# 直写入场形态的调用（任意 kind）
RAW_KIND = re.compile(r"overlay(?:Enter|Leave)\s*\([^)]*'(?:pop|modal|drawer)'")

ALLOW = {
    LIB / "composables" / "morph.ts",
    # 抽屉用 'drawer' 分支的共享元素 ghost（从被点的行长成抽屉），是它专属的形变
    LIB / "components" / "ui" / "Drawer.vue",
}


def main() -> int:
    comps = LIB / "components"
    if not comps.exists():
        print(f"OVERLAY_MOTION: SKIP（组件目录不存在 {comps}）")
        return 0

    bad: list[tuple[str, int]] = []
    for path in sorted(comps.rglob("*.vue")):
        if path in ALLOW:
            continue
        text = path.read_text(encoding="utf-8")
        for m in RAW_KIND.finditer(text):
            bad.append((str(path.relative_to(ROOT)), text[: m.start()].count("\n") + 1))

    if bad:
        print(f"OVERLAY_MOTION: FAIL（{len(bad)} 处绕过统一入口，浮层形态会与设计不符）")
        for name, line in bad:
            print(f"  {name}:{line}")
        print("  修法：改成 @enter=\"overlayMenuEnter\" @leave=\"overlayMenuLeave\"，")
        print("        由 morph.ts 按「面板内有无可操作项」自动分派。")
        print("        若确实是居中弹窗/全屏遮罩，把它加进本脚本的 ALLOW 并写明理由。")
        return 1

    print("OVERLAY_MOTION: PASS（浮层入场全部走统一入口）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
