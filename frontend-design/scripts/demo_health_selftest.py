"""示例页健康守卫的阳性对照：注入违例样本并逐判据断言守卫真的会报。

[职责] 守卫全绿本身不构成证据，必须先证明「真有缺陷时它确实会报」。
  本文件承载注入物与自测流程，不含全量扫描。
[覆盖] 八类 DOM 与控制台判据逐项核对期望命中数，并额外核验扫描根覆盖：
  注入前后示例卡数必须加一，否则说明阳性对照只在被注入的那一小片上生效。
最近修改时间：2026-10-18 19:32:00；改动原因：6-review 发现 check_demo_health.py 379 行超 200 行基准，按 diamond 拆分，判据字节未改写。
"""
from playwright.sync_api import sync_playwright

from demo_health_env import PROBE, derive_routes, open_page
from demo_health_judges import judge_console

# 阳性对照：一张卡里放齐每条 DOM 判据的违例样本，逐条断言守卫真的会报
INJECT_BAD = r"""() => {
  const cell = document.createElement('div')
  cell.className = 'g-cell'
  cell.id = 'probe-bad-cell'
  cell.innerHTML = `
    <div class="g-cell-head"><span class="g-cell-name">ProbeBad<em class="g-cell-variant">控制组</em></span>
      <span class="g-cell-status is-bad">渲染异常</span></div>
    <div class="g-cell-path">probe/bad.vue</div>
    <div class="g-cell-err">TypeError: 人为注入的渲染异常</div>
    <div class="g-cell-body">
      <span>取值 NaN 未定义</span>
      <span>结果是 undefined</span>
      <span>Invalid Date</span>
      <span>[object Object]</span>
      <img src="/definitely-missing-404.png" alt="">
      <svg width="0" height="0" viewBox="0 0 1 1"><rect width="1" height="1"/></svg>
      <div style="width:40px;white-space:nowrap;overflow:hidden">这段文字远超容器宽度必然被裁掉</div>
      <div style="background:#ffffff;color:#fdfdfd">与背景几乎同色的文字</div>
      <button type="button"></button>
    </div>`
  document.querySelector('.g-grid, main, #app').appendChild(cell)
  return document.querySelectorAll('.g-cell').length
}"""

# 控制台判据的阳性对照：真实打一条 error 与一条 Vue 风格 warning
INJECT_CONSOLE = """() => { console.error('probe-console-error'); console.warn('[Vue warn]: Invalid prop: probe'); }"""

EXPECT = {"renderError": 1, "badText": 4, "brokenImg": 1, "zeroIcon": 1, "clipped": 1, "lowContrast": 1, "noName": 1}

def selftest(base: str, theme: str = "light") -> int:
    """跑阳性对照：注入坏卡与坏控制台消息，逐条断言判据真的会报。"""
    with sync_playwright() as pw:
        browser, page, logs, _ = open_page(pw, base, theme)
        routes = derive_routes()
        page.goto(base + routes[0], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector(".g-cell", timeout=60000)
        page.wait_for_timeout(500)
        before = page.evaluate("() => document.querySelectorAll('.g-cell').length")
        after = page.evaluate(INJECT_BAD)
        logs.clear()
        page.evaluate(INJECT_CONSOLE)
        page.wait_for_timeout(200)
        probe = page.evaluate(PROBE)
        browser.close()

    ok = after == before + 1
    print(f"扫描根覆盖: 注入前 {before} 卡 -> 注入后 {after} 卡（注入卡被本次扫描计入 = {ok}）")
    hits = {k: [x for x in probe.get(k, []) if "ProbeBad" in str(x.get("tag", ""))] for k in EXPECT}
    for key, want in EXPECT.items():
        got = len(hits[key])
        good = got == want
        ok &= good
        print(f"  判据 {key}: 期望 {want} 命中 {got} -> {'OK' if good else 'FAIL'}")
    console_hits = judge_console(logs)
    good = len(console_hits) == 2
    ok &= good
    print(f"  判据 console: 期望 2 命中 {len(console_hits)} -> {'OK' if good else 'FAIL'}")
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1
