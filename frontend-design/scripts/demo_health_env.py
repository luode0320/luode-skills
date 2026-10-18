"""示例页健康扫描的运行环境：路由派生、已登录页面装配与页内量测脚本。

[职责] 只回答「扫哪些页、怎么把浏览器摆到可量测状态、在页面里量什么」，
  不含命中裁决（见 demo_health_judges.py）、阳性对照（见 demo_health_selftest.py）
  与全量流程（见 check_demo_health.py）。
[口径] 路由全部从分类真相源派生，守卫不自己手写路由清单；
  九类判据的页内实现集中在 PROBE 一处，改动必须与 judges 侧的裁决口径同步。
最近修改时间：2026-10-18 19:32:00；改动原因：6-review 发现 check_demo_health.py 379 行超 200 行基准，按 diamond 拆分，判据字节未改写。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_SOURCE = ROOT / "component-library" / "src" / "data" / "component-categories.ts"

def derive_routes() -> list[str]:
    """从分类真相源派生全部示例页路由。

    [参数] 无 [返回] 路由列表；每个父分类下的每个子分组对应一个三级路径。
    """
    source = CATEGORY_SOURCE.read_text(encoding="utf-8")
    data_files = re.findall(r"from '\./(component-categories\.[a-z]+\.ts)'", source)
    routes: list[str] = []
    for name in data_files:
        text = (CATEGORY_SOURCE.parent / name).read_text(encoding="utf-8")
        for block in re.split(r"\n  \{\n", text):
            cat = re.search(r"key: '([a-z-]+)'", block)
            if not cat:
                continue
            for sub in re.findall(r"key: '([a-z-]+)'", block)[1:]:
                routes.append(f"/gallery/{cat.group(1)}/{sub}")
    return routes

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

# 主题由 src/composables/appearance.ts 从 localStorage 读取后写到 <html data-theme>，
# 因此必须在应用脚本执行前写入，事后改 dataset 会被组件的 watch 覆盖回去。
THEME_JS = """(theme) => {
    let cur = {}
    try { cur = JSON.parse(localStorage.getItem('scaffold.appearance') || '{}') } catch (e) { cur = {} }
    localStorage.setItem('scaffold.appearance', JSON.stringify({
        density: 'regular', railCollapsed: false, ...cur, theme,
    }))
}"""

def open_page(pw, base: str, theme: str = "light"):
    """建一个已登录、主题已指定的页面。

    [参数] pw playwright 实例、base 本地服务地址、theme 主题（light / dark）
    [返回] (browser, page, logs, errors)
    """
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    logs: list[dict] = []
    errors: list[dict] = []
    page.on("console", lambda m: logs.append({"type": m.type, "text": m.text[:300]}))
    page.on("pageerror", lambda e: errors.append({"type": "pageerror", "text": str(e)[:300]}))
    page.goto(base + "/login", wait_until="domcontentloaded", timeout=60000)
    page.evaluate(SIGN_IN, base)
    page.evaluate(THEME_JS, theme)
    return browser, page, logs, errors

PROBE = r"""() => {
  const BAD = [
    ['NaN', /\bNaN\b/],
    ['undefined', /\bundefined\b/],
    ['invalid-date', /Invalid Date/],
    ['object-object', /\[object Object\]/],
    ['object-promise', /\[object Promise\]/],
  ]
  const INTERACTIVE = 'button, a[href], input, select, textarea, [role="button"], [role="switch"], [role="tab"], [role="checkbox"], [role="radio"], [role="menuitem"], [tabindex]:not([tabindex="-1"])'
  // 视觉隐藏：绝对定位且宽高≤1px，或 clip 生效。这类元素本来就不给人眼看，不参与裁切判定。
  const isVisualHidden = (cs, r) => cs.position === 'absolute' && (r.width <= 1 || r.height <= 1 || (cs.clip !== 'auto' && cs.clip !== ''))
  const rgba = (s) => {
    const m = /rgba?\(([^)]+)\)/.exec(s || '')
    if (!m) return null
    const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number)
    return [p[0] || 0, p[1] || 0, p[2] || 0, p.length > 3 ? p[3] : 1]
  }
  const lum = (c) => {
    const f = c.slice(0, 3).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4) })
    return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2]
  }
  // 有效背景：沿祖先链把每一层半透明背景按 alpha 合成下去，直到遇到不透明层。
  // 只取「第一个不透明祖先」会跳过半透明遮罩——遮罩恰恰是决定文字可读性的那一层，
  // 跳过它会把「白字压深色遮罩」误算成「白字压白卡」，报出根本不存在的缺陷。
  const bgOf = (el) => {
    const layers = []
    let base = [255, 255, 255, 1]
    let painted = false
    for (let n = el; n; n = n.parentElement) {
      const cs2 = getComputedStyle(n)
      // 渐变或图片背景的实际底色取决于色标与图像内容，backgroundColor 读不到；
      // 这种层一旦出现在文字与不透明底之间，对比度就无法可靠测量，标记后跳过该元素。
      if (cs2.backgroundImage && cs2.backgroundImage !== 'none') painted = true
      const c = rgba(cs2.backgroundColor)
      if (!c) continue
      if (c[3] >= 0.999) { base = c; break }
      if (c[3] > 0) layers.push(c)
    }
    let out = base.slice(0, 3)
    for (let i = layers.length - 1; i >= 0; i--) {
      const c = layers[i]
      out = out.map((v, k) => c[k] * c[3] + v * (1 - c[3]))
    }
    return { rgb: out.concat(1), measurable: !painted }
  }
  const contrast = (fg, bg) => {
    const a = lum(fg) + 0.05, b = lum(bg) + 0.05
    return a > b ? a / b : b / a
  }
  const out = { cells: 0, renderError: [], badText: [], brokenImg: [], zeroIcon: [], clipped: [], noName: [], lowContrast: [], overflowX: 0 }
  out.overflowX = Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)

  for (const cell of document.querySelectorAll('.g-cell')) {
    out.cells++
    const name = (cell.querySelector('.g-cell-name')?.childNodes[0]?.textContent || '').trim()
    const variant = (cell.querySelector('.g-cell-variant')?.textContent || '').trim()
    const tag = name + (variant ? '#' + variant : '')
    if (cell.querySelector('.g-cell-status.is-bad')) {
      out.renderError.push({ tag, detail: (cell.querySelector('.g-cell-err')?.textContent || '').trim().slice(0, 200) })
    }
    const body = cell.querySelector('.g-cell-body')
    if (!body) continue

    const tw = document.createTreeWalker(body, NodeFilter.SHOW_TEXT)
    let node
    while ((node = tw.nextNode())) {
      const t = (node.nodeValue || '').trim()
      if (!t) continue
      for (const [kind, re] of BAD) {
        if (re.test(t)) { out.badText.push({ tag, kind, text: t.slice(0, 90) }); break }
      }
    }

    for (const img of body.querySelectorAll('img')) {
      if (img.complete && img.naturalWidth === 0) {
        out.brokenImg.push({ tag, src: (img.currentSrc || img.src || '').slice(0, 140), alt: img.alt || '' })
      }
    }

    for (const svg of body.querySelectorAll('svg')) {
      const cs = getComputedStyle(svg)
      if (cs.display === 'none' || cs.visibility === 'hidden') continue
      const r = svg.getBoundingClientRect()
      if (r.width < 2 || r.height < 2) out.zeroIcon.push({ tag, cls: (svg.getAttribute('class') || '').slice(0, 60) })
    }

    for (const el of body.querySelectorAll('*')) {
      const text = (el.textContent || '').trim()
      const cs = getComputedStyle(el)
      const r = el.getBoundingClientRect()
      if (isVisualHidden(cs, r)) continue
      // 只看承载文本的叶子：容器宽度由子元素决定，拿它判裁切会把正常布局报成缺陷
      const leafText = [...el.childNodes].some((n) => n.nodeType === 3 && (n.nodeValue || '').trim())
      if (leafText && text) {
        const scrollable = ['auto', 'scroll'].includes(cs.overflowX) || ['auto', 'scroll'].includes(cs.overflow)
        const ellipsed = cs.textOverflow === 'ellipsis' || cs.webkitLineClamp !== 'none'
        if (!scrollable && !ellipsed && ['hidden', 'clip'].includes(cs.overflowX) && el.scrollWidth - el.clientWidth > 2 && el.clientWidth > 0) {
          out.clipped.push({ tag, sel: el.tagName + '.' + String(el.className || '').split(/\s+/)[0], gap: el.scrollWidth - el.clientWidth, text: text.slice(0, 60) })
        }
      }
      // 低对比：半透明与禁用态的低对比是设计意图，不判
      const faded = Number(cs.opacity) < 0.9 || el.closest('[disabled], .is-disabled, [aria-disabled="true"]')
      const fg = rgba(cs.color)
      if (leafText && text && !faded && fg) {
        const back = bgOf(el)
        if (back.measurable) {
          const bg = back.rgb
          // 文字色自身也可能半透明（如 rgba(255,255,255,.56)），必须先合成到背景上再算对比度
          const solid = fg[3] >= 0.999 ? fg.slice(0, 3) : bg.slice(0, 3).map((v, k) => fg[k] * fg[3] + v * (1 - fg[3]))
          const ratio = contrast(solid.concat(1), bg)
          if (ratio < 1.5) out.lowContrast.push({ tag, sel: el.tagName + '.' + String(el.className || '').split(/\s+/)[0], ratio: Math.round(ratio * 100) / 100, text: text.slice(0, 40) })
        }
      }
    }

    for (const el of body.querySelectorAll(INTERACTIVE)) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') continue
      const nm = (el.getAttribute('aria-label') || el.textContent || el.getAttribute('title') || '').trim()
      if (!nm && !el.querySelector('img[alt]:not([alt=""])')) {
        out.noName.push({ tag, sel: el.tagName + '.' + String(el.className || '').split(/\s+/)[0] })
      }
    }
  }
  return out
}"""
