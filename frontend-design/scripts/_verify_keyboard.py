#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 验证 Steps 与 Cascader 的键盘可达性是否真的等价于鼠标操作。
[边界] 一次性验证脚本，不参与守卫家族；需要 dev server 与 C:/Python314/python.exe（带 playwright）。
[用法] python scripts/_verify_keyboard.py [--base http://localhost:5173]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from demo_health_env import open_page  # noqa: E402  复用已登录会话，避免被踢回登录页

STEPS_URL = "/gallery/navigation/steps"
CASCADER_URL = "/gallery/inputs/cascader"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://localhost:5173")
    args = ap.parse_args()
    fails: list[str] = []

    with sync_playwright() as p:
        browser, page, logs, errors = open_page(p, args.base, "light")

        # ── Steps：可点步骤应可聚焦且 Enter/Space 能激活 ──
        page.goto(args.base + STEPS_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector(".x-step", timeout=30000)
        steps = page.locator(".x-step")
        focusable = page.locator('.x-step[tabindex="0"]')
        n_focus = focusable.count()
        print(f"Steps: 共 {steps.count()} 个步骤，其中可聚焦 {n_focus} 个")
        if n_focus == 0:
            fails.append("Steps 可点步骤没有 tabindex，键盘到不了")

        if n_focus:
            first = focusable.first
            before = page.locator(".x-step.is-active .x-step-title").first.inner_text()
            first.focus()
            focused_ok = page.evaluate("document.activeElement?.classList.contains('x-step')")
            print(f"Steps: 焦点落在步骤上 = {focused_ok}（激活前 {before}）")
            if not focused_ok:
                fails.append("Steps 步骤拿不到焦点")
            page.keyboard.press("Enter")
            page.wait_for_timeout(200)
            after = page.locator(".x-step.is-active .x-step-title").first.inner_text()
            print(f"Steps: Enter 后当前步 = {after}")
            if after == before:
                fails.append("Steps Enter 未切换当前步")
            # 焦点环可见性：outline 宽度应大于 0
            ring = page.evaluate(
                """() => {
                    const el = document.querySelector('.x-step[tabindex="0"]');
                    if (!el) return null;
                    el.focus();
                    const s = getComputedStyle(el);
                    return { style: s.outlineStyle, width: s.outlineWidth };
                }"""
            )
            print(f"Steps: 焦点环 = {ring}")
            if ring and (ring["style"] == "none" or ring["width"] in ("0px", "0")):
                fails.append("Steps 可聚焦但看不到焦点环")

        # ── Cascader：方向键应能移动光标、Enter 落定、Esc 关闭并还焦点 ──
        page.goto(args.base + CASCADER_URL, wait_until="domcontentloaded", timeout=60000)
        trigger = page.locator(".x-cas").first
        trigger.wait_for(timeout=30000)
        trigger.focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        menu_open = page.locator(".x-cas-menu").count() > 0
        print(f"Cascader: Enter 打开菜单 = {menu_open}")
        if not menu_open:
            fails.append("Cascader Enter 未打开菜单")

        if menu_open:
            active = page.evaluate(
                "() => document.querySelector('.x-cas')?.getAttribute('aria-activedescendant')"
            )
            print(f"Cascader: aria-activedescendant = {active}")
            if not active:
                fails.append("Cascader 缺 aria-activedescendant")

            marked = page.locator(".x-cas-option.is-focus").count()
            print(f"Cascader: 有键盘光标的项 = {marked}")
            if marked == 0:
                fails.append("Cascader 打开后没有键盘光标位置")

            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(150)
            moved = page.evaluate(
                "() => document.querySelector('.x-cas')?.getAttribute('aria-activedescendant')"
            )
            print(f"Cascader: ArrowDown 后 = {moved}")
            if moved == active:
                fails.append("Cascader ArrowDown 未移动光标")

            # ArrowLeft 退回上一列：示例数据 modelValue=[1,11]，打开时在第 2 层
            page.keyboard.press("ArrowLeft")
            page.wait_for_timeout(200)
            back = page.evaluate(
                "() => document.querySelector('.x-cas')?.getAttribute('aria-activedescendant')"
            )
            back_depth = back.rsplit("-", 2)[1] if back else None
            print(f"Cascader: ArrowLeft 后 = {back}（层级 {back_depth}）")
            if back_depth != "0":
                fails.append("Cascader ArrowLeft 未退回上级列")

            # ArrowRight 落在「总部」这一有子级的分支上，应进入下级而不是关闭
            cols_before = page.locator(".x-cas-col").count()
            page.keyboard.press("ArrowRight")
            page.wait_for_timeout(300)
            still_open = page.locator(".x-cas-menu").count() > 0
            fwd = page.evaluate(
                "() => document.querySelector('.x-cas')?.getAttribute('aria-activedescendant')"
            )
            fwd_depth = fwd.rsplit("-", 2)[1] if fwd else None
            cols_after = page.locator(".x-cas-col").count()
            print(f"Cascader: ArrowRight 后 = {fwd}，列数 {cols_before} → {cols_after}，菜单仍在 = {still_open}")
            if not still_open:
                fails.append("Cascader 在有子级的项上 ArrowRight 误关闭了菜单")
            elif fwd_depth != "1":
                fails.append("Cascader ArrowRight 未进入下级列")

            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            closed = page.locator(".x-cas-menu").count() == 0
            refocused = page.evaluate("document.activeElement?.classList.contains('x-cas')")
            print(f"Cascader: Esc 关闭 = {closed}，焦点回到触发器 = {refocused}")
            if not closed:
                fails.append("Cascader Esc 未关闭菜单")
            if not refocused:
                fails.append("Cascader 关闭后焦点未回到触发器")

        browser.close()

    if errors:
        print(f"\n页面运行时报错 {len(errors)} 条：")
        for e in errors[:5]:
            print("  - " + e["text"])
        fails.append(f"页面有 {len(errors)} 条运行时报错")

    if fails:
        print("\nKEYBOARD_VERIFY: FAIL")
        for f in fails:
            print("  - " + f)
        return 1
    print("\nKEYBOARD_VERIFY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
