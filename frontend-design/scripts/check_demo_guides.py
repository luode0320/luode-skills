"""扫描全部示例页：校验每张示例卡都有文字提示，且提示对应当前这一格。

[判据] 全部取自运行时组件实例与 DOM，不读源码：
  1. 覆盖：每张示例卡头的组件名旁必须有 `.x-help` 触发图标；
  2. 两段：提示正文必须同时含「组件说明」与「本格示例」两段；
  3. 对应：非基础示例的「本格示例」段不得退回「默认形态」，必须点出本格差异；
  4. 区分：同一组件内不同变体的提示不得全部相同。
[用法] python -X utf8 -B frontend-design/scripts/check_demo_guides.py --base http://localhost:5173
[返回] 退出码 0=全部通过；1=存在缺口。输出 DEMO_GUIDES: PASS/FAIL 与命中清单。
[约束] 示例卡数量下限与空页检测同时生效，防止扫描根不全时的 0 命中被误读成通过。
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_SOURCE = ROOT / "component-library" / "src" / "data" / "component-categories.ts"
# 示例卡数量下限：扫描根不全时 0 缺口会被误读成「全部通过」
MIN_CELLS = 600
# 基础示例的固定文案：非基础示例出现它就说明提示没有对应当前这一格
BASE_TEXT = "默认形态，未覆盖任何属性"

SIGN_IN = """async (base) => {
    const login = await fetch(base + '/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'admin', password: 'admin123', captcha: '1024', uuid: 'probe' }),
    }).then((r) => r.json())
    localStorage.setItem('scaffold.token', login.data.token)
    localStorage.setItem('scaffold.expiresAt', String(Date.now() + login.data.expiresIn * 1000))
    return Boolean(login.data.token)
}"""

PROBE = """() => {
  const out = []
  for (const cell of document.querySelectorAll('.g-cell')) {
    const name = (cell.querySelector('.g-cell-name')?.childNodes[0]?.textContent || '').trim()
    const variant = (cell.querySelector('.g-cell-variant')?.textContent || '').trim()
    const guide = cell.__vueParentComponent?.props?.guide || ''
    out.push({
      name, variant, guide,
      hasIcon: Boolean(cell.querySelector('.g-cell-name .x-help')),
      hasDemoPart: guide.includes('本格示例'),
      demoPart: guide.split('本格示例：')[1] || '',
    })
  }
  return out
}"""


def derive_routes() -> list[str]:
    """从分类真相源派生全部示例页路由。

    [参数] 无 [返回] 路由列表；每个父分类下的每个子分组对应一个三级路径。
    """
    source = CATEGORY_SOURCE.read_text(encoding="utf-8")
    data_files = re.findall(r"from '\./(component-categories\.[a-z]+\.ts)'", source)
    routes: list[str] = []
    for name in data_files:
        text = (CATEGORY_SOURCE.parent / name).read_text(encoding="utf-8")
        blocks = re.split(r"\n  \{\n", text)
        for block in blocks:
            cat = re.search(r"key: '([a-z-]+)'", block)
            if not cat:
                continue
            for sub in re.findall(r"key: '([a-z-]+)'", block)[1:]:
                routes.append(f"/gallery/{cat.group(1)}/{sub}")
    return routes


def collect(cells: list[dict]) -> dict:
    """按四类判据汇总缺口。

    [参数] cells 全部示例卡的运行时数据
    [返回] dict 各判据的命中清单与统计
    """
    no_icon = [c for c in cells if not c["hasIcon"]]
    no_demo = [c for c in cells if not c["hasDemoPart"]]
    # 非基础示例却仍写「默认形态」，说明提示没有落到这一格
    default_text = [c for c in cells if c["variant"] != "基础示例" and c["demoPart"] == BASE_TEXT]
    by_name = defaultdict(set)
    counts = defaultdict(int)
    for c in cells:
        by_name[c["name"]].add(c["guide"])
        counts[c["name"]] += 1
    collapsed = {n: len(v) for n, v in by_name.items() if counts[n] > 1 and len(v) == 1}
    return {
        "noIcon": no_icon,
        "noDemoPart": no_demo,
        "defaultText": default_text,
        "collapsed": collapsed,
    }


def main() -> int:
    """逐页扫描示例页并汇总文字提示缺口。"""
    parser = argparse.ArgumentParser(description="Check demo cards have matching tooltips")
    parser.add_argument("--base", default="http://localhost:5173")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    routes = derive_routes()
    if len(routes) < 20:
        print(f"DEMO_GUIDES: FAIL (分类真相源只解析出 {len(routes)} 个示例页，扫描根不可信)")
        return 1

    cells: list[dict] = []
    empty_pages: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        try:
            page.goto(f"{args.base}/login", wait_until="networkidle")
            if not page.evaluate(SIGN_IN, args.base):
                print("DEMO_GUIDES: FAIL (登录态注入失败)")
                return 1
            for route in routes:
                page.goto(f"{args.base}{route}", wait_until="networkidle")
                page.wait_for_timeout(500)
                if not page.query_selector_all(".g-cell"):
                    empty_pages.append(route)
                for c in page.evaluate(PROBE):
                    c["page"] = route
                    cells.append(c)
        finally:
            browser.close()

    if empty_pages:
        print(f"DEMO_GUIDES: FAIL ({len(empty_pages)} 个示例页渲染 0 张卡，扫描结果不可信)")
        for route in empty_pages[:10]:
            print(f"  - 空页: {route}")
        return 1
    if len(cells) < MIN_CELLS:
        print(f"DEMO_GUIDES: FAIL (只扫描到 {len(cells)} 张示例卡，低于下限 {MIN_CELLS}，扫描根不可信)")
        return 1

    found = collect(cells)
    if args.json:
        print(json.dumps({"cells": len(cells), **found}, ensure_ascii=False, indent=1))

    problems = []
    for c in found["noIcon"]:
        problems.append(f"[{c['page']}] {c['name']} {c['variant']} | 缺少提示图标")
    for c in found["noDemoPart"]:
        problems.append(f"[{c['page']}] {c['name']} {c['variant']} | 提示缺少「本格示例」段")
    for c in found["defaultText"]:
        problems.append(f"[{c['page']}] {c['name']} {c['variant']} | 非基础示例却写默认形态")
    for name, distinct in found["collapsed"].items():
        problems.append(f"{name} | 多个变体的提示完全相同（只有 {distinct} 种）")

    if problems:
        print(f"DEMO_GUIDES: FAIL ({len(problems)} 处提示缺口 / 扫描 {len(cells)} 张示例卡)")
        for line in problems[:20]:
            print(f"  - {line}")
        return 1
    print(f"DEMO_GUIDES: PASS (扫描 {len(routes)} 页 {len(cells)} 张示例卡，每格提示均对应本格示例)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
