#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""组件边角遮挡守卫：在真实浏览器里逐页检查圆角容器的角部是否被直角子元素盖住。

[判据] 当场从 DOM 几何与计算样式推导，不写死组件名：
  1. 父级有可见圆角（外弧 R ≥ 8px）与可见描边（w ≥ 3px）时，角部弧线以内区域本应由
     父级描边绘制；内弧 = R − w。若某个可见子元素以直角（该角圆角 < 内弧）贴到父级
     内角上，就会盖住描边，在角部露出与整体风格不一致的方角。
  2. 有背景的圆角父级若不裁剪（`overflow` 非 hidden/clip），子元素方角会直接露在父级
     外弧之外；子元素该角圆角必须 ≥ 父级该角圆角。
[边界] 只判定描边 ≥ 3px 的父级：1px 细描边被覆盖在视觉上不可辨，属正常实现。
  父级自身开启裁剪时子元素被裁到圆角内，不判。探针与页面操作见 corner_occlusion_probe.py。

[用法] 先启动本地开发服务，再运行
  python -X utf8 -B frontend-design/scripts/check_corner_occlusion.py [--base URL] [--limit N]
[返回] 退出码 0=无边角遮挡；1=存在遮挡。输出 CORNER_OCCLUSION: PASS/FAIL。
最近修改时间：2026-10-17 12:36:00；改动原因：测量体下沉独立模块，本文件回到仓库
  200 行文件基准内；拆分只做搬运，输出与拆分前逐项一致。
"""
import argparse
import sys

from playwright.sync_api import sync_playwright

from corner_occlusion_probe import PROBE, goto_label, menu_labels, sign_in


def scan(base, limit):
    """逐页扫描全部菜单页，返回（已扫页数，失败清单）。"""
    scanned = 0
    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        try:
            page.goto(f"{base}/login", wait_until="networkidle")
            session = sign_in(page, base)
            if not session.get("token"):
                return 0, [{"url": base, "label": "登录态注入", "findings": []}]
            page.goto(f"{base}/gallery/general/button", wait_until="networkidle")
            labels = menu_labels(page)
            if limit:
                labels = labels[:limit]
            for label in labels:
                if not goto_label(page, label):
                    continue
                page.wait_for_timeout(420)
                scanned += 1
                found = page.evaluate(PROBE)
                if found:
                    failures.append({"url": page.url, "label": label, "findings": found})
        finally:
            browser.close()
    return scanned, failures


def report(scanned, failures):
    """按扫描结果输出结论与明细，返回退出码。"""
    if not scanned:
        print("CORNER_OCCLUSION: FAIL (未扫描到任何菜单页，判据失效)")
        return 1
    if failures:
        total = sum(len(f["findings"]) for f in failures)
        print(f"CORNER_OCCLUSION: FAIL ({total} 处边角不一致，涉及 {len(failures)} 页)")
        for item in failures:
            for f in item["findings"]:
                print(
                    f"  {item['url']} :: {f['parent']} > {f['child']} @{f['side']} [{f['kind']}] "
                    f"→ 需要 {f['need']}px，实得 {f['actual']}px"
                )
        return 1
    print(f"CORNER_OCCLUSION: PASS (扫描 {scanned} 个菜单页，无描边被盖住、无子元素方角外露)")
    return 0


def main():
    """解析参数、执行扫描并输出裁决。"""
    parser = argparse.ArgumentParser(description="Check rounded-corner occlusion in the component gallery")
    parser.add_argument("--base", default="http://localhost:5173", help="local dev server base URL")
    parser.add_argument("--limit", type=int, default=0, help="only scan the first N menu pages (0 = all)")
    args = parser.parse_args()
    scanned, failures = scan(args.base, args.limit)
    return report(scanned, failures)


if __name__ == "__main__":
    sys.exit(main())
