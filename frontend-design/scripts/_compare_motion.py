#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 动效升级的慢放对比：把 transition-duration 放大 10 倍做真慢放，逐帧采样计算值，
       同一交互分别跑「旧（浏览器默认 ease）」与「新（语态令牌）」，还原进度曲线。
       先自动探测哪些交互真有可见色变，再取前 6 个，避免凭猜测选场景。
[边界] 只量单条过渡的进度形状；时长被刻意放大，不代表实际速度，只代表曲线形状。观感仍需人眼看。
[用法] python scripts/_compare_motion.py
       python scripts/_compare_motion.py --limit 6 --verbose
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from demo_health_env import open_page  # noqa: E402

SLOW_MS = 2000
SAMPLE_MS = SLOW_MS + 700
BASE = "http://localhost:5173"

# 候选：够多才挑得出 6 个「真的有可见色变」的
CANDIDATES = [
    ("按钮 悬停着色", "/gallery/general/button", ".btn-primary", "backgroundColor", "hover"),
    ("复选框 选中", "/gallery/inputs/checkbox", ".checkbox-box", "backgroundColor", "click"),
    ("选项卡 切换", "/gallery/navigation/tabs", ".x-tabs-tab", "backgroundColor", "class:is-active"),
    ("日期格 选中", "/gallery/inputs/date", ".x-date-cell", "", "class:is-selected", ".x-date"),
    ("级联选项 选中", "/gallery/inputs/cascader", ".x-cas-option", "", "class:is-active", ".x-cas"),
    ("树行 选中", "/gallery/display/tree", ".tree-row", "", "class:is-selected", ""),
    ("图标按钮 悬停", "/gallery/general/button", ".icon-btn", "backgroundColor", "hover"),
    ("表格行 悬停", "/gallery/display/table", ".table tbody tr", "backgroundColor", "hover"),
    ("输入壳 悬停", "/gallery/inputs/text", ".input-shell", "borderColor", "hover"),
]

SLOW = "*, *::before, *::after { transition-duration: %dms !important; }" % SLOW_MS
OLD_EASE = "*, *::before, *::after { transition-timing-function: ease !important; }"

START = """(cfg) => {
  window.__motion = [];
  const t0 = performance.now();
  const tick = () => {
    const el = document.querySelectorAll(cfg.selector)[cfg.index || 0];
    if (el) {
      const cs = getComputedStyle(el);
      window.__motion.push([performance.now() - t0, cs.backgroundColor, cs.color, cs.borderColor]);
    }
    if (performance.now() - t0 < cfg.until) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}"""

PROPS = ("backgroundColor", "color", "borderColor")

# 挑第一个「还没带这个状态类」的实例：第一个往往本来就选中，加类等于没加
PICK_UNSET = """(cfg) => {
  const list = Array.from(document.querySelectorAll(cfg.selector));
  const idx = list.findIndex(el => !el.classList.contains(cfg.cls));
  if (idx === -1) return -1;
  list[idx].classList.add(cfg.cls);
  return idx;
}"""


def parse_rgb(value: str) -> list[float] | None:
    v = (value or "").strip()
    if not v.startswith("rgb"):
        return None
    inner = v[v.index("(") + 1: v.rindex(")")]
    parts = [p for p in inner.replace("/", " ").replace(",", " ").split() if p]
    try:
        nums = [float(p.replace("%", "")) for p in parts]
    except ValueError:
        return None
    return nums[:3] if len(nums) >= 3 else None


def progress(a: list[float], b: list[float], cur: list[float]) -> float | None:
    vec = [b[i] - a[i] for i in range(3)]
    diff = [cur[i] - a[i] for i in range(3)]
    denom = sum(v * v for v in vec)
    if denom < 1e-6:
        return None
    return max(0.0, min(1.0, sum(vec[i] * diff[i] for i in range(3)) / denom))


def prepare(page, route: str) -> bool:
    page.goto(BASE + route, wait_until="domcontentloaded", timeout=60000)
    try:
        page.wait_for_selector(".g-cell", timeout=20000)
        return True
    except Exception:
        return False


def measure(page, case, force_old: bool) -> list | None:
    _, route, selector, prop, trigger = case[:5]
    pre = case[5] if len(case) > 5 else ""
    if not prepare(page, route):
        return None
    page.mouse.move(2, 2)
    page.wait_for_timeout(300)
    if pre:
        try:
            page.locator(pre).first.click(timeout=3000)
            page.wait_for_timeout(400)
        except Exception:
            return None
    page.add_style_tag(content=SLOW + ("\n" + OLD_EASE if force_old else ""))
    page.wait_for_timeout(200)
    box = None
    try:
        box = page.locator(selector).first.bounding_box(timeout=3000)
    except Exception:
        return None                 # 该选择器在此页不存在，交给探测环节跳过
    if not box:
        return None
    # 先把「要观察哪个实例」定下来（不改状态），采样从静止态开始
    index = 0
    if trigger.startswith("class:"):
        cls = trigger.split(":", 1)[1]
        index = page.evaluate(
            "(cfg) => Array.from(document.querySelectorAll(cfg.selector)).findIndex(el => !el.classList.contains(cfg.cls))",
            {"selector": selector, "cls": cls},
        )
        if index is None or index < 0:
            return None
        box = page.locator(selector).nth(index).bounding_box(timeout=3000)

    page.evaluate(START, {"selector": selector, "until": SAMPLE_MS, "index": index})
    cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    if trigger == "hover":
        page.mouse.move(cx, cy, steps=1)
    elif trigger == "click":
        page.mouse.move(cx, cy, steps=1)
        page.mouse.down()
        page.mouse.up()
    elif trigger.startswith("class:"):
        # 直接切组件自己的状态类：有些状态在演示卡里没有悬停入口，但过渡是真的
        page.evaluate(
            "(cfg) => document.querySelectorAll(cfg.selector)[cfg.index]?.classList.add(cfg.cls)",
            {"selector": selector, "cls": trigger.split(":", 1)[1], "index": index},
        )
    page.wait_for_timeout(SAMPLE_MS + 250)
    return page.evaluate("() => window.__motion") or []


def curve(series: list, force_prop: str | None = None) -> dict | None:
    """[参数] 逐帧 [t, bg, color, border] [返回] 变化最大的那个颜色通道的进度曲线。"""
    if len(series) < 10:
        return None
    best = None
    for offset, name in enumerate(PROPS, start=1):
        if force_prop and name != force_prop:
            continue
        pts = [(row[0], parse_rgb(row[offset])) for row in series if len(row) > offset]
        pts = [(t, c) for t, c in pts if c]
        if len(pts) < 10:
            continue
        start, end = pts[0][1], pts[-1][1]
        delta = sum((end[i] - start[i]) ** 2 for i in range(3))
        if delta < 4.0:                     # 变化太小，量不出可靠进度
            continue
        out = [(t, progress(start, end, c)) for t, c in pts]
        out = [(t, p) for t, p in out if p is not None]
        if len(out) < 10:
            continue
        # 起手 10% 时长内就到 90%：说明这属性没走过渡，量了也没意义
        early = min(out, key=lambda p: abs(p[0] - SLOW_MS * 0.1))
        if early[1] is not None and early[1] > 0.92:
            continue
        if best is None or delta > best["delta"]:
            best = {"points": out, "delta": delta, "prop": name}
    return best


def at(points, frac: float) -> float | None:
    target = SLOW_MS * frac
    best = min(points, key=lambda p: abs(p[0] - target))
    return None if abs(best[0] - target) > SLOW_MS * 0.15 else best[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=6)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    picked, skipped = [], []
    with sync_playwright() as p:
        browser, page, logs, errors = open_page(p, BASE, "light")
        for case in CANDIDATES:
            if len(picked) >= args.limit:
                break
            new = measure(page, case, False)
            cn = curve(new or [])
            if not cn:
                skipped.append(case[0])
                continue
            picked.append((case, cn))

        print(f"自动探测：命中 {len(picked)} 个，跳过 {len(skipped)} 个"
              + (f"（{'、'.join(skipped)}）" if skipped else ""))
        print()
        print(f"{'场景':<16}{'旧 ease 25/50/75%':<26}{'新语态 25/50/75%':<26}{'起步提速':>8}")
        print("-" * 82)
        for case, cn in picked:
            old = measure(page, case, True)
            co = curve(old or [], force_prop=cn["prop"])
            if not co:
                print(f"{case[0]:<16}旧曲线采样失败，跳过")
                continue
            fo = [at(co["points"], f) for f in (0.25, 0.5, 0.75)]
            fn = [at(cn["points"], f) for f in (0.25, 0.5, 0.75)]
            fmt = lambda vs: " / ".join("—" if v is None else f"{v*100:.0f}%" for v in vs)
            delta = ""
            if fo[0] is not None and fn[0] is not None:
                delta = f"{(fn[0]-fo[0])*100:+.0f}pt"
            print(f"{case[0]:<16}{fmt(fo):<26}{fmt(fn):<26}{delta:>8}")
            if args.verbose:
                print(f"    {case[2]} @ {case[1]}  ({case[4]})  量的是 {cn["prop"]}")
        browser.close()

    if errors:
        print(f"\n运行时报错 {len(errors)} 条：")
        for e in errors[:3]:
            print("  - " + e["text"][:150])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
