"""扫描全部示例页：找出「控件 / 可见容器内部，文字字形贴到自身内边缘」的组件。

[判据] 全部取自运行时几何与计算样式，不读源码：
  1. 候选容器 = 示例卡内带非 none 边框、或带非透明背景的元素，以及 button 等交互控件；
  2. 检查范围含控件内部：交互控件自带内边距，字形贴到自身内边缘仍是可见的排版缺陷；
  3. 文本盒与容器内边缘（边框内侧）的间距 < 4px 即判定贴边；
  4. 排除 `position: fixed/absolute` 的浮层、可滚动容器、表格与分栏结构。
[用法] python -X utf8 -B frontend-design/scripts/check_content_padding.py --base http://localhost:5173
[返回] 退出码 0=无贴边；1=存在贴边。输出 CONTENT_PADDING: PASS/FAIL 与命中清单。
"""
import argparse
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_SOURCE = ROOT / "component-library" / "src" / "data" / "component-categories.ts"

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

# 在页面内跑的探针：返回每张示例卡的贴边命中
PROBE = """() => {
  const hits = []
  const cells = [...document.querySelectorAll('.g-cell')]
  for (const cell of cells) {
    const nameEl = cell.querySelector('.g-cell-name')
    const name = (nameEl?.childNodes[0]?.textContent || nameEl?.textContent || '').trim()
    const body = cell.querySelector('.g-cell-body')
    if (!body) continue

    // 1. 收集候选容器：只取「可见容器」——四边都有可见边框，或有非透明背景。
    //    只有单边描线的分隔条（如 .hero-readouts 的 border-top）不算：它的内容本来就
    //    从分隔线起点排布，贴边是栅格语义，不是留白缺失。
    const containers = [body, ...body.querySelectorAll('*')].filter((el) => {
      const cs = getComputedStyle(el)
      if (cs.position === 'fixed' || cs.position === 'absolute') return false
      if (cs.display === 'none' || cs.visibility === 'hidden') return false
      const sides = ['Top', 'Right', 'Bottom', 'Left'].map((s) => ({
        w: parseFloat(cs['border' + s + 'Width']) || 0,
        style: cs['border' + s + 'Style'],
      }))
      const fullBorder = sides.every((s) => s.w > 0 && s.style !== 'none')
      const bg = cs.backgroundColor
      const hasBg = bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent'
      // 交互控件即使没有背景与边框也要查：它的可点区域就是用户看到的选项块，
      // 文字贴到可点区域边缘与贴到底色块边缘是同一类视觉缺陷。
      const interactive = el.matches('button, [role="menuitem"], [role="option"], [role="tab"]')
      return fullBorder || hasBg || interactive
    })

    for (const box of containers) {
      const bs = getComputedStyle(box)
      const br = box.getBoundingClientRect()
      if (br.width < 24 || br.height < 12) continue
      // 内容宽于容器时由自身滚动承接，贴边是滚动语义而非留白缺陷。
      if (box.scrollWidth > box.clientWidth + 1 || box.scrollHeight > box.clientHeight + 1) continue
      const insetL = br.left + (parseFloat(bs.borderLeftWidth) || 0)
      const insetR = br.right - (parseFloat(bs.borderRightWidth) || 0)
      // 判据只在容器「自身有可见边界」时成立：有非透明背景或完整边框。
      // 纯文字按钮（如 x-transfer-link、btn-text）与无底色的布局 div 没有可见边界，
      // 文字贴到自身盒边是流式排版的正常结果，按边框内沿量会把它们全部误报。
      const bgColor = bs.backgroundColor
      const hasVisibleBg = bgColor && bgColor !== 'rgba(0, 0, 0, 0)' && bgColor !== 'transparent'
      const sides = ['Top', 'Right', 'Bottom', 'Left'].map((s) => ({
        w: parseFloat(bs['border' + s + 'Width']) || 0,
        style: bs['border' + s + 'Style'],
      }))
      const hasVisibleBorder = sides.some((s) => s.w > 0 && s.style !== 'none')
      if (!hasVisibleBg && !hasVisibleBorder) continue
      // 圆形容器（头像、圆形徽标）豁免：字形受弧线约束，左右间距天然小于矩形块，
      // 贴边在视觉上被圆弧吃掉，不构成「文字末尾贴到选项边缘」这类缺陷。
      const radius = parseFloat(bs.borderTopLeftRadius) || 0
      if (radius >= br.height / 2 - 0.5) continue

      // 2. 直接子元素优先；交互控件没有子元素承载文字时回退到控件自身的文本节点。
      const targets = []
      for (const child of [...box.children]) {
        const cs = getComputedStyle(child)
        if (cs.position === 'fixed' || cs.position === 'absolute') continue
        if (cs.display === 'none' || cs.visibility === 'hidden') continue
        // 分栏 / 表格结构按列排布，贴边是布局语义
        if (child.closest('table, tr, td, th, thead, tbody, .swim-lane, .pager')) continue
        targets.push(child)
      }
      // 控件内部的文字常直接挂在控件下，此时把控件自身作为文本承载者。
      if (!targets.length) targets.push(box)

      for (const child of targets) {
        const textRect = textBounds(child)
        if (!textRect || textRect.width < 4 || textRect.height < 4) continue
        const padL = Math.round(textRect.left - insetL)
        const padR = Math.round(insetR - textRect.right)
        // 判据只取左右：横向贴边是肉眼可见的错位。
        // 上下不判——标签、头像、徽标这类小控件靠行高与行内对齐把字形居中，
        // 底部只余 2–3px 属排版结果而非留白缺陷，纳入判据会把它们全部误报。
        const minPad = Math.min(padL, padR)
        if (minPad < 4) {
          hits.push({
            card: name,
            container: box.className && typeof box.className === 'string'
              ? box.className.split(/\\s+/).filter(Boolean).slice(0, 3).join('.')
              : box.tagName,
            child: child.tagName + (child.className && typeof child.className === 'string'
              ? '.' + child.className.split(/\\s+/)[0] : ''),
            text: (child.textContent || '').trim().slice(0, 28),
            pads: { l: padL, r: padR },
          })
        }
      }
    }
  }

  // 取元素内第一个文本节点的字形矩形；没有文本时返回 null
  function textBounds(el) {
    const range = document.createRange()
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT)
    let node
    while ((node = walker.nextNode())) {
      if (!node.textContent.trim()) continue
      range.selectNodeContents(node)
      const rects = [...range.getClientRects()]
      if (!rects.length) return null
      const box = rects.reduce((acc, r) => ({
        left: Math.min(acc.left, r.left), right: Math.max(acc.right, r.right),
        top: Math.min(acc.top, r.top), bottom: Math.max(acc.bottom, r.bottom),
      }), { left: Infinity, right: -Infinity, top: Infinity, bottom: -Infinity })
      return { ...box, width: box.right - box.left, height: box.bottom - box.top }
    }
    return null
  }
  return { cells: cells.length, hits }
}"""


def derive_routes() -> list[str]:
    """从分类真相源派生全部示例页路由。

    [参数] 无 [返回] 路由列表；每个父分类下的每个子分组对应一个三级路径。
    最近修改时间：2026-10-18 00:45:00；改动原因：避免手写路由清单漏页。
    """
    # 1. 侧栏用 div + JS 跳转而不是 <a href>，DOM 派生拿不到链接，改读唯一真相源。
    source = CATEGORY_SOURCE.read_text(encoding="utf-8")
    # 2. 组装文件只 import 三个数据文件，逐个读它们里的 key。
    data_files = re.findall(r"from '\./(component-categories\.[a-z]+\.ts)'", source)
    routes: list[str] = []
    for name in data_files:
        text = (CATEGORY_SOURCE.parent / name).read_text(encoding="utf-8")
        # 3. 父分类 key 与子分组 key 在各自数据文件里成对出现，按出现顺序配对。
        blocks = re.split(r"\n  \{\n", text)
        for block in blocks:
            cat = re.search(r"key: '([a-z-]+)'", block)
            if not cat:
                continue
            for sub in re.findall(r"key: '([a-z-]+)'", block)[1:]:
                routes.append(f"/gallery/{cat.group(1)}/{sub}")
    return routes


def main() -> int:
    """逐页扫描示例页并汇总贴边命中。"""
    parser = argparse.ArgumentParser(description="Detect text flush against container inner edges")
    parser.add_argument("--base", default="http://localhost:5173")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    # 1. 路由从分类真相源派生：示例页是三级路径 /gallery/<分类>/<子分组>，
    #    侧栏用 div + JS 跳转、没有 <a href>，手写路由清单则会漏页并误报 PASS。
    routes = derive_routes()
    if len(routes) < 20:
        print(f"CONTENT_PADDING: FAIL (分类真相源只解析出 {len(routes)} 个示例页，扫描根不可信)")
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        try:
            page.goto(f"{args.base}/login", wait_until="networkidle")
            if not page.evaluate(SIGN_IN, args.base):
                print("CONTENT_PADDING: FAIL (登录态注入失败)")
                return 1

            all_hits = []
            total_cells = 0
            empty_pages = []
            for route in routes:
                page.goto(f"{args.base}{route}", wait_until="networkidle")
                page.wait_for_timeout(700)
                result = page.evaluate(PROBE)
                total_cells += result["cells"]
                if result["cells"] == 0:
                    empty_pages.append(route)
                for hit in result["hits"]:
                    hit["page"] = route
                    all_hits.append(hit)

            # 2. 空页必须单独计数：扫描根不全时 clips=0 会被误读成「全部通过」。
            if empty_pages:
                print(f"CONTENT_PADDING: FAIL ({len(empty_pages)} 个示例页渲染 0 张卡，扫描结果不可信)")
                for route in empty_pages[:10]:
                    print(f"  - 空页: {route}")
                return 1

            if args.json:
                print(json.dumps({"cells": total_cells, "hits": all_hits}, ensure_ascii=False, indent=2))
            if all_hits:
                print(f"CONTENT_PADDING: FAIL ({len(all_hits)} 处贴边 / 扫描 {total_cells} 张示例卡)")
                for hit in all_hits:
                    print(f"  - [{hit['page']}] {hit['card']} | {hit['container']} > {hit['child']}"
                          f" | pads={hit['pads']} | {hit['text']}")
                return 1
            print(f"CONTENT_PADDING: PASS (扫描 {total_cells} 张示例卡，无文本贴边)")
            return 0
        finally:
            browser.close()


if __name__ == "__main__":
    sys.exit(main())
