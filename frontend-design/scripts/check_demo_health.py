"""扫描全部示例页的运行时健康信号，汇总命中并裁决。

[职责] 只承载全量流程：派生路由、建已登录页面、逐页跑探针、汇总命中、按扫描根下限裁决。
  页内量测脚本见 demo_health_env.py，命中判定与豁免面见 demo_health_judges.py，
  阳性对照见 demo_health_selftest.py。
[判据] 九类：渲染异常、框架告警、坏文本、坏图、零尺寸图标、缺可访问名、文字裁切、
  页面横向溢出、低对比文字；全部取自运行时 DOM、计算样式与控制台，不读组件源码、不比对截图。
[用法] python -X utf8 -B frontend-design/scripts/check_demo_health.py --base http://localhost:5173
       加 --theme dark 扫暗色主题；加 --selftest 只跑阳性对照，不扫全量。
[返回] 退出码 0=全部通过；1=存在命中、扫描根不全或阳性对照失效。输出 DEMO_HEALTH: PASS/FAIL。
最近修改时间：2026-10-18 19:32:00；改动原因：6-review 发现 check_demo_health.py 379 行超 200 行基准，按 diamond 拆分，判据字节未改写。
"""
import argparse
import json
import sys

from playwright.sync_api import sync_playwright

from demo_health_env import PROBE, derive_routes, open_page
from demo_health_judges import KNOWN_CONSOLE_ALLOW, judge_console
from demo_health_selftest import selftest

# 示例卡数量下限：扫描根不全时命中为 0 会被误读成「全部通过」
MIN_CELLS = 600

def main() -> int:
    """逐页扫描示例页并汇总命中；--selftest 时只跑阳性对照。"""
    parser = argparse.ArgumentParser(description="Scan demo pages for runtime health defects")
    parser.add_argument("--base", default="http://localhost:5173")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--theme", default="light", choices=["light", "dark"], help="扫描所用主题")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    if args.selftest:
        return selftest(args.base, args.theme)

    routes = derive_routes()
    findings: list[str] = []
    cells = 0
    counts = {k: 0 for k in ("renderError", "badText", "brokenImg", "zeroIcon", "clipped", "noName", "lowContrast", "console", "overflowX")}
    raw: dict = {}
    with sync_playwright() as pw:
        browser, page, logs, errors = open_page(pw, args.base, args.theme)
        for route in routes:
            logs.clear()
            errors.clear()
            page.goto(args.base + route, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector(".g-cell", timeout=60000)
            page.wait_for_timeout(320)
            probe = page.evaluate(PROBE)
            cells += probe["cells"]
            raw[route] = probe
            for key in ("renderError", "badText", "brokenImg", "zeroIcon", "clipped", "noName", "lowContrast"):
                for item in probe.get(key, []):
                    counts[key] += 1
                    findings.append(f"{key} {route} {item.get('tag')} {json.dumps({k: v for k, v in item.items() if k != 'tag'}, ensure_ascii=False)[:160]}")
            for hit in judge_console(logs + errors):
                counts["console"] += 1
                findings.append(f"console {route} {hit}")
            if probe.get("overflowX", 0) > 0:
                counts["overflowX"] += 1
                findings.append(f"overflowX {route} 溢出 {probe['overflowX']}px")
        browser.close()

    if args.json:
        print(json.dumps(raw, ensure_ascii=False, indent=1))
    if cells < MIN_CELLS:
        print(f"DEMO_HEALTH: FAIL (扫描根不全：只扫到 {cells} 张示例卡，低于下限 {MIN_CELLS})")
        return 1
    if findings:
        print(f"DEMO_HEALTH: FAIL ({len(findings)} 项；主题 {args.theme}，扫描 {len(routes)} 页 {cells} 张示例卡)")
        for line in findings[:80]:
            print("  -", line)
        if len(findings) > 80:
            print(f"  ... 另有 {len(findings) - 80} 项")
        return 1
    print(f"DEMO_HEALTH: PASS (主题 {args.theme}，扫描 {len(routes)} 页 {cells} 张示例卡，九类判据零命中；豁免 {len(KNOWN_CONSOLE_ALLOW)} 条已登记)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
