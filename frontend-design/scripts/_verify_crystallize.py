#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 验证确认落定动画在浏览器里真的逐拍跑：收拢宽度、描环、画勾、回弹。
[边界] 需要 dev server 与 C:/Python314/python.exe（带 playwright）。只验动画过程，不验视觉审美。
[用法] python scripts/_verify_crystallize.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from demo_health_env import open_page  # noqa: E402

URL = "/gallery/general/button"


def main() -> int:
    fails: list[str] = []
    with sync_playwright() as p:
        browser, page, logs, errors = open_page(p, "http://localhost:5173", "light")
        page.goto("http://localhost:5173" + URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector(".g-cell", timeout=30000)

        # 自驱模式的基础示例：块级、带文案、未落定
        btn = page.locator(".cx-btn").first
        btn.wait_for(state="visible", timeout=15000)
        box = btn.bounding_box()
        print(f"落定前按钮宽度 = {box['width']:.1f}px")

        # 点一下，逐帧采样 1.4s（点击前先挂好采集器，保证 t0 从点击那一帧起算）
        page.evaluate(
            """() => {
                window.__cx = [];
                document.addEventListener('click', () => {
                    const t0 = performance.now();
                    const tick = () => {
                        const b = document.querySelector('.cx-btn');
                        const orb = b && b.querySelector('.cx-orb');
                        const ring = b && b.querySelector('circle');
                        const check = b && b.querySelector('path');
                        window.__cx.push({
                            t: Math.round(performance.now() - t0),
                            done: b ? b.classList.contains('is-done') : false,
                            w: orb ? +orb.getBoundingClientRect().width.toFixed(1) : null,
                            h: orb ? +orb.getBoundingClientRect().height.toFixed(1) : null,
                            ring: ring ? +parseFloat(getComputedStyle(ring).strokeDashoffset) : null,
                            check: check ? +parseFloat(getComputedStyle(check).strokeDashoffset) : null,
                            scale: orb ? getComputedStyle(orb).transform : null,
                        });
                        if (performance.now() - t0 < 2400) requestAnimationFrame(tick);
                    };
                    requestAnimationFrame(tick);
                }, { once: true, capture: true });
            }"""
        )
        btn.click()
        page.wait_for_timeout(2700)
        series = page.evaluate("() => window.__cx")

        widths = [s["w"] for s in series if s["w"] is not None]
        rings = [s["ring"] for s in series if s["ring"] is not None]
        checks = [s["check"] for s in series if s["check"] is not None]
        scales = [s["scale"] for s in series if s["scale"] not in (None, "none")]
        print(f"采集帧数 = {len(series)}；落定帧 = {sum(1 for s in series if s['done'])}")
        print(f"宽度轨迹（去重）: {sorted(set(widths), reverse=True)[:8]}")
        print(f"圆环 dashoffset 去重数 = {len(set(rings))}，范围 {min(rings) if rings else '-'}~{max(rings) if rings else '-'}")
        print(f"对勾 dashoffset 去重数 = {len(set(checks))}，范围 {min(checks) if checks else '-'}~{max(checks) if checks else '-'}")
        print(f"回弹缩放帧数 = {len(scales)}")

        # 判据 1：进入落定态，宽度渐变收拢，且收成正圆
        if not any(s["done"] for s in series):
            fails.append("点击后没有进入 is-done 落定态")
        if not widths:
            fails.append("落定态没有出现 .cx-orb")
        else:
            if not (widths[-1] < box["width"] - 40):
                fails.append(f"宽度没有收拢：{box['width']:.0f} → {widths[-1]:.0f}")
            if len(set(widths)) < 5:
                fails.append(f"宽度是跳变而不是渐变，只有 {len(set(widths))} 个不同值")
            last = series[-1]
            if last["h"]:
                ratio = last["w"] / last["h"]
                print(f"收拢后 宽/高 = {ratio:.2f}")
                if abs(ratio - 1) > 0.12:
                    fails.append(f"收拢后不是正圆：宽 {last['w']} 高 {last['h']}")

        # 判据 2：两笔描线都有过程，且对勾晚于圆环起笔
        if len(set(rings)) < 3:
            fails.append(f"圆环描线没有过程，只有 {len(set(rings))} 个不同值")
        if len(set(checks)) < 2:
            fails.append(f"对勾描线没有过程，只有 {len(set(checks))} 个不同值")
        ring_start = next((s["t"] for s in series if s["ring"] is not None and s["ring"] < 126), None)
        check_start = next((s["t"] for s in series if s["check"] is not None and s["check"] < 24), None)
        print(f"圆环起笔 {ring_start}ms，对勾起笔 {check_start}ms")
        if ring_start is not None and check_start is not None and check_start <= ring_start:
            fails.append("对勾没有晚于圆环起笔，笔顺感丢失")

        # 判据 3：回弹确实发生过（出现过非 1 的缩放）
        if len(scales) < 2:
            fails.append("没有捕捉到回弹（scale 始终为 1）")

        # 判据 4：动画走完必须描满
        final = page.evaluate(
            """() => {
                const b = document.querySelector('.cx-btn');
                const orb = b?.querySelector('.cx-orb');
                const ring = b?.querySelector('circle');
                const check = b?.querySelector('path');
                return {
                    done: b?.classList.contains('is-done') || false,
                    w: orb ? +orb.getBoundingClientRect().width.toFixed(1) : null,
                    h: orb ? +orb.getBoundingClientRect().height.toFixed(1) : null,
                    ring: ring ? +parseFloat(getComputedStyle(ring).strokeDashoffset) : null,
                    check: check ? +parseFloat(getComputedStyle(check).strokeDashoffset) : null,
                };
            }"""
        )
        print(f"动画走完 → {final}")
        if final["done"]:
            if final["ring"] not in (0, 0.0):
                fails.append(f"圆环未描满，dashoffset 停在 {final['ring']}")
            if final["check"] not in (0, 0.0):
                fails.append(f"对勾未画完，dashoffset 停在 {final['check']}")

        # 判据 5：自驱模式要能复位回可点击态，否则演示只能看一次
        page.wait_for_timeout(1600)
        reset = page.evaluate(
            """() => {
                const b = document.querySelector('.cx-btn');
                return { done: b ? b.classList.contains('is-done') : null,
                         text: b ? b.textContent.trim() : null,
                         disabled: b ? b.disabled : null };
            }"""
        )
        print(f"复位 → {reset}")
        if reset["done"] or not reset["text"] or reset["disabled"]:
            fails.append(f"自驱模式没有复位回可点击状态：{reset}")

        browser.close()

    if errors:
        for e in errors[:3]:
            print("  运行时报错: " + e["text"][:160])
        fails.append(f"页面有 {len(errors)} 条运行时报错")

    if fails:
        print("\nCRYSTALLIZE_VERIFY: FAIL")
        for f in fails:
            print("  - " + f)
        return 1
    print("\nCRYSTALLIZE_VERIFY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
