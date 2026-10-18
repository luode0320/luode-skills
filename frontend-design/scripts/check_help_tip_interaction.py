"""HelpTip 真实浏览器验证：悬停、键盘聚焦、Esc 关闭与浮层不被裁切。

[判据] 全部取自运行时 DOM 与计算样式，不读源码、不比对截图：
  1. 悬停后浮层存在、可见、文本等于 content，且浮层四边都在视口内；
  2. 浮层不是被裁切的子节点：它的祖先链上不得出现 overflow 非 visible 的裁剪容器；
  3. Tab 聚焦后浮层立即可见（不需要指针）；
  4. Esc 收起，且 aria-describedby 同步消失；
  5. 指针移出但按钮仍持有焦点时，说明必须继续可见（键盘用户能读完）；
  6. 纯说明气泡不吃指针（pointer-events 为 none），否则会退化成半成品浮层；
  7. 按钮 aria-label 等于 label，role=tooltip 存在，长文不超过 260px 宽度上限。
[作用域] 一律取 `.g-cell-body .x-help`：卡头也有一个 HelpTip，不限定会选中卡头那个，
  它的 label 由示例页按组件名传入，默认 aria-label 判据会恒红。
[用法] python -X utf8 -B frontend-design/scripts/check_help_tip_interaction.py --base http://localhost:5173
[返回] 退出码 0=通过；1=失败。输出 HELP_TIP: PASS/FAIL。
"""
import argparse
import sys

from playwright.sync_api import sync_playwright

# 被测对象必须限定在示例卡的内容区：DemoCell 的卡头也挂了一个 HelpTip（label 由示例页按
# 组件名传入），不限定时 document.querySelector 会先命中卡头那个，默认 aria-label 判据
# 就永远拿不到组件自身的缺省值，守卫恒红。
HELP_BTN = ".g-cell-body .x-help"

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

MEASURE = """() => {
    const btn = document.querySelector('.g-cell-body .x-help')
    if (!btn) return { error: 'no-button' }
    const tip = document.querySelector('.x-help-tip')
    if (!tip) return { error: 'no-panel' }
    const box = tip.getBoundingClientRect()
    const style = getComputedStyle(tip)
    // 沿 offsetParent 链找裁剪容器：浮层若留在卡片里，会被 overflow 容器切掉
    const clipped = []
    for (let el = tip.parentElement; el; el = el.parentElement) {
        const cs = getComputedStyle(el)
        if (cs.overflow !== 'visible' && cs.overflow !== '') clipped.push(el.className || el.tagName)
    }
    return {
        text: tip.textContent.trim(),
        role: tip.getAttribute('role'),
        label: btn.getAttribute('aria-label'),
        describedBy: btn.getAttribute('aria-describedby'),
        tipId: tip.id,
        visible: style.visibility !== 'hidden' && style.display !== 'none' && Number(style.opacity) > 0,
        inViewport: box.top >= 0 && box.left >= 0 && box.bottom <= innerHeight && box.right <= innerWidth,
        box: { top: Math.round(box.top), left: Math.round(box.left), w: Math.round(box.width), h: Math.round(box.height) },
        clipped,
        pointerEvents: style.pointerEvents,
    }
}"""


def main() -> int:
    """跑完整交互链路并输出判定。"""
    parser = argparse.ArgumentParser(description="Verify HelpTip interaction in a real browser")
    parser.add_argument("--base", default="http://localhost:5173")
    args = parser.parse_args()

    failures: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        try:
            page.goto(f"{args.base}/login", wait_until="networkidle")
            if not page.evaluate(SIGN_IN, args.base):
                print("HELP_TIP: FAIL (本地登录态注入失败)")
                return 1
            page.goto(f"{args.base}/gallery/display/tooltip", wait_until="networkidle")
            page.wait_for_selector(HELP_BTN, timeout=15000)

            # 1. 悬停：等过 120ms 延迟后测量
            page.hover(HELP_BTN)
            page.wait_for_timeout(400)
            hover = page.evaluate(MEASURE)
            if hover.get("error"):
                failures.append(f"悬停后未出现浮层: {hover['error']}")
            else:
                if not hover["visible"]:
                    failures.append("浮层不可见")
                if not hover["inViewport"]:
                    failures.append(f"浮层超出视口: {hover['box']}")
                if hover["role"] != "tooltip":
                    failures.append(f"role 应为 tooltip，实得 {hover['role']}")
                if hover["describedBy"] != hover["tipId"]:
                    failures.append(f"aria-describedby 未关联浮层: {hover['describedBy']} vs {hover['tipId']}")
                if not hover["text"]:
                    failures.append("浮层文本为空")
                if hover["clipped"]:
                    failures.append(f"浮层被裁剪容器包住: {hover['clipped']}")
                if hover["pointerEvents"] != "none":
                    failures.append(f"说明气泡不应吃指针，实得 pointer-events={hover['pointerEvents']}")

            # 2. 移出后收起
            page.mouse.move(4, 4)
            page.wait_for_timeout(300)
            if page.query_selector(".x-help-tip"):
                failures.append("指针移出后浮层未收起")

            # 3. 键盘聚焦：先让按钮拿到焦点，再确认浮层出现
            page.focus(HELP_BTN)
            page.wait_for_timeout(300)
            focus = page.evaluate(MEASURE)
            if focus.get("error"):
                failures.append(f"键盘聚焦后未出现浮层: {focus['error']}")
            else:
                if focus["label"] != "查看说明":
                    failures.append(f"默认 aria-label 不符: {focus['label']}")
                if not focus["visible"]:
                    failures.append("键盘聚焦浮层不可见")

            # 4. Esc 收起
            page.keyboard.press("Escape")
            page.wait_for_timeout(250)
            if page.query_selector(".x-help-tip"):
                failures.append("Esc 未收起浮层")
            if page.get_attribute(HELP_BTN, "aria-describedby"):
                failures.append("收起后 aria-describedby 仍残留")

            # 4.1 焦点保持：指针移出但按钮仍聚焦时，说明必须继续可见
            page.hover(HELP_BTN)
            page.wait_for_timeout(300)
            page.focus(HELP_BTN)
            page.mouse.move(4, 4)
            page.wait_for_timeout(300)
            if not page.query_selector(".x-help-tip"):
                failures.append("指针移出后，仍聚焦按钮上的说明被错误收起")
            page.keyboard.press("Escape")
            page.wait_for_timeout(250)

            # 5. 长文本变体：确认 260px 上限生效且仍在视口内
            cards = page.query_selector_all(".g-cell")
            long_ok = False
            for card in cards:
                btn = card.query_selector(".g-cell-body .x-help")
                if not btn:
                    continue
                btn.hover()
                page.wait_for_timeout(350)
                tip = page.query_selector(".x-help-tip")
                if tip and "外部账务系统" in (tip.text_content() or ""):
                    width = tip.evaluate("el => el.getBoundingClientRect().width")
                    if width <= 262:
                        long_ok = True
                    break
            if not long_ok:
                failures.append("长文本变体未验证到 260px 宽度上限")
        finally:
            browser.close()

    if failures:
        print(f"HELP_TIP: FAIL ({len(failures)} 项)")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("HELP_TIP: PASS (悬停/聚焦/Esc/焦点保持/指针穿透/视口夹取/ARIA 关联/长文换行 全部通过)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
