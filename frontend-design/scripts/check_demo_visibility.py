"""扫描全部示例页：找出「组件在示例卡内不可见」的格子。

[判据] 全部取自运行时几何与计算样式，不读源码：
  1. 空白卡：内容区可见元素数为 0（如整块被 v-show 隐藏）；
  2. 出卡：组件根元素完全落在内容区可视矩形之外（如 position: fixed 浮层飘到视口角落）；
  3. 塌缩：内容区有元素，但可见宽与高都小于 4px（如没有邻居撑开的纵向分割线）。
[用法] python -X utf8 -B frontend-design/scripts/check_demo_visibility.py --base http://localhost:5173
[返回] 退出码 0=全部可见；1=存在不可见格子。输出 DEMO_VISIBILITY: PASS/FAIL 与命中清单。
[约束] 判据只判「完全不可见」，部分遮挡不在范围；线状元素（分割线）按宽或高任一达标即不算塌缩，
  否则 1px 竖线会被误判——它本来就是一条线。
"""
import argparse
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_SOURCE = ROOT / "component-library" / "src" / "data" / "component-categories.ts"
# 示例卡数量下限：扫描根不全时 findings 为 0 会被误读成「全部通过」
MIN_CELLS = 600

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
    const nameEl = cell.querySelector('.g-cell-name')
    const name = (nameEl?.childNodes[0]?.textContent || nameEl?.textContent || '').trim()
    const variant = (cell.querySelector('.g-cell-variant')?.textContent || '').trim()
    const body = cell.querySelector('.g-cell-body')
    if (!body) { out.push({ name, variant, kind: 'no-body', detail: '' }); continue }
    const br = body.getBoundingClientRect()
    const els = [...body.querySelectorAll('*')]
    if (!els.length) { out.push({ name, variant, kind: 'empty', detail: '' }); continue }
    let visible = 0, outside = 0, tiny = 0
    let sample = ''
    for (const el of els) {
      const cs = getComputedStyle(el)
      if (cs.display === 'none' || cs.visibility === 'hidden') continue
      const r = el.getBoundingClientRect()
      if (r.width < 1 && r.height < 1) continue
      // 定位包装层不算内容：它自身铺满内容区，会把真正飘到卡外的浮层盖住。
      // 只排除「有定位且完全铺满内容区」的元素，正常布局容器仍参与判定。
      const isShell = (cs.position === 'absolute' || cs.position === 'fixed') &&
        Math.abs(r.left - br.left) <= 1 && Math.abs(r.top - br.top) <= 1 &&
        Math.abs(r.right - br.right) <= 1 && Math.abs(r.bottom - br.bottom) <= 1
      if (isShell) continue
      visible++
      // 完全落在内容区可视矩形之外
      const disjoint = r.right <= br.left || r.left >= br.right || r.bottom <= br.top || r.top >= br.bottom
      if (disjoint) { outside++; if (!sample) sample = el.tagName + '.' + (typeof el.className === 'string' ? el.className.split(/\\s+/)[0] : '') }
      // 宽与高都小于 4px 才算塌缩：1px 竖线是线状组件的正常形态
      if (r.width < 4 && r.height < 4) tiny++
    }
    if (visible === 0) out.push({ name, variant, kind: 'all-hidden', detail: '' })
    else if (outside === visible) out.push({ name, variant, kind: 'all-outside', detail: sample })
    else if (tiny === visible) out.push({ name, variant, kind: 'all-tiny', detail: sample })
  }
  return out
}"""

# 阳性对照：给内容区追加一个视口固定元素，出卡判据必须报出它
CONTROL_OUTSIDE = """() => {
  const body = document.querySelector('.g-cell-body')
  const el = document.createElement('div')
  el.id = 'probe-outside'
  el.style.cssText = 'position:fixed;right:0;bottom:0;width:42px;height:42px'
  body.appendChild(el)
  const br = body.getBoundingClientRect()
  const r = el.getBoundingClientRect()
  const disjoint = r.right <= br.left || r.left >= br.right || r.bottom <= br.top || r.top >= br.bottom
  el.remove()
  return disjoint
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


def main() -> int:
    """逐页扫描示例页并汇总不可见命中。"""
    parser = argparse.ArgumentParser(description="Detect demo cards whose component is invisible")
    parser.add_argument("--base", default="http://localhost:5173")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    routes = derive_routes()
    if len(routes) < 20:
        print(f"DEMO_VISIBILITY: FAIL (分类真相源只解析出 {len(routes)} 个示例页，扫描根不可信)")
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        try:
            page.goto(f"{args.base}/login", wait_until="networkidle")
            if not page.evaluate(SIGN_IN, args.base):
                print("DEMO_VISIBILITY: FAIL (登录态注入失败)")
                return 1

            # 阳性对照先跑：判据本身失效时不能把全量扫描的 0 命中读成通过
            page.goto(f"{args.base}{routes[0]}", wait_until="networkidle")
            page.wait_for_timeout(600)
            if not page.evaluate(CONTROL_OUTSIDE):
                print("DEMO_VISIBILITY: FAIL (阳性对照未命中：出卡判据自身失效)")
                return 1

            findings = []
            total_cells = 0
            empty_pages = []
            for route in routes:
                page.goto(f"{args.base}{route}", wait_until="networkidle")
                page.wait_for_timeout(700)
                hits = page.evaluate(PROBE)
                cells = page.query_selector_all(".g-cell")
                total_cells += len(cells)
                if not cells:
                    empty_pages.append(route)
                for hit in hits:
                    hit["page"] = route
                    findings.append(hit)

            if empty_pages:
                print(f"DEMO_VISIBILITY: FAIL ({len(empty_pages)} 个示例页渲染 0 张卡，扫描结果不可信)")
                for route in empty_pages[:10]:
                    print(f"  - 空页: {route}")
                return 1
            if total_cells < MIN_CELLS:
                print(f"DEMO_VISIBILITY: FAIL (只扫描到 {total_cells} 张示例卡，低于下限 {MIN_CELLS}，扫描根不可信)")
                return 1

            if args.json:
                print(json.dumps({"cells": total_cells, "findings": findings}, ensure_ascii=False, indent=2))
            if findings:
                print(f"DEMO_VISIBILITY: FAIL ({len(findings)} 处不可见 / 扫描 {total_cells} 张示例卡)")
                for hit in findings:
                    print(f"  - [{hit['page']}] {hit['name']} {hit['variant']} | {hit['kind']} | {hit['detail']}")
                return 1
            print(f"DEMO_VISIBILITY: PASS (扫描 {len(routes)} 页 {total_cells} 张示例卡，组件全部在卡内可见)")
            return 0
        finally:
            browser.close()


if __name__ == "__main__":
    sys.exit(main())
