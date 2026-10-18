"""对账：组件 defineEmits 声明的事件 vs 示例格实际绑定的处理器。

[职责] 只承载全量流程：派生路由、逐页逐格取运行时绑定、汇总缺口并按扫描根下限裁决。
  页内量测脚本、豁免面与缺口判定在同目录 demo_event_wiring_probe.py。
[背景] 示例层只自动接 `update:<样本已有键>`；组件其余声明事件（close / select / submit / confirm 等）
  没人接时，示例卡上的按钮点了完全没有反馈，看起来像坏控件。装配层现按派生事件表
  （scripts/build_demo_events.mjs）统一接上一次可见反馈，本守卫负责守住这条接线不回退。
[用法] python -X utf8 -B frontend-design/scripts/check_demo_event_wiring.py --base http://localhost:5173
       加 --selftest 只跑判据阳性对照，不扫全量。
[返回] 退出码 0=通过；1=存在缺口、扫描根不全或阳性对照失效。输出 EVENT_WIRING: PASS/FAIL。
最近修改时间：2026-10-18 19:36:00；改动原因：6-review 发现 check_demo_event_wiring.py 251 行超 200 行基准，按 diamond 拆分，判据字节未改写。
"""
import argparse
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from demo_event_wiring_probe import (
    NO_FEEDBACK,
    PROBE,
    SIGN_IN,
    load_events_table,
    missing_events,
)

ROOT = Path(__file__).resolve().parents[1]
CL = ROOT / "component-library"
CATEGORY_SOURCE = CL / "src" / "data" / "component-categories.ts"

# 示例卡数量下限：扫描根不全时缺口为 0 会被误读成「全部通过」
MIN_CELLS = 600

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



def selftest() -> int:
    """判据阳性对照：用合成夹具证明缺口判得出、接上了不报、带横线事件名不误报。"""
    cases = [
        ("未接任何处理器必须报缺口", ["close"], [], ["close"], True),
        ("接上 onClose 后不报", ["close"], ["onClose"], [], True),
        ("带横线事件名按 camelize 归一", ["create-item", "edit-type"], ["onCreateItem", "onEditType"], [], True),
        ("update:* 不在本判据范围", ["update:modelValue"], [], [], True),
        ("多事件里漏一个只报漏的那个", ["confirm", "cancel", "ok"], ["onConfirm", "onOk"], ["cancel"], True),
    ]
    ok = True
    for label, emits, bound, expect, _ in cases:
        got = missing_events(emits, bound)
        good = got == expect
        ok &= good
        print(f"  {'OK  ' if good else 'FAIL'} {label}: 期望 {expect} 实得 {got}")
    # 反向对照：豁免面必须都是派生事件表里真实存在的条目，否则豁免面已经腐烂
    table = load_events_table()
    stale = [k for k in NO_FEEDBACK if k.split(".", 1)[1] not in table.get(k.split(".", 1)[0], [])]
    good = not stale
    ok &= good
    print(f"  {'OK  ' if good else 'FAIL'} 豁免面无失效条目: {stale or '无'}")
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

def main() -> int:
    """逐页逐格对账事件接线；--selftest 时只跑判据阳性对照。"""
    parser = argparse.ArgumentParser(description="Verify demo cells bind every declared component event")
    parser.add_argument("--base", default="http://localhost:5173")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    table = load_events_table()
    if not table:
        print("EVENT_WIRING: FAIL (派生事件表读不到条目，先跑 node scripts/build_demo_events.mjs)")
        return 1
    routes = derive_routes()
    gaps: list[str] = []
    cells = 0
    checked = 0
    exempt = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(args.base + "/login", wait_until="domcontentloaded", timeout=60000)
        page.evaluate(SIGN_IN, args.base)
        for route in routes:
            page.goto(args.base + route, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector(".g-cell", timeout=60000)
            page.wait_for_timeout(300)
            # 静止态即可判定：绑定关系挂在 vnode 上，与弹层是否展开、内容是否被传送无关
            merged: dict[str, set] = {}
            order: list[str] = []
            for row in page.evaluate(PROBE):
                key = f"{row['name']}#{row['variant']}"
                if key not in merged:
                    merged[key] = set()
                    order.append(key)
                merged[key].update(row["bound"])
            for key in order:
                cells += 1
                name = key.split("#", 1)[0]
                emits = table.get(name, [])
                # update:* 由样本状态写回负责，不计入本判据的受检面
                subject = [e for e in emits if not e.startswith("update:")]
                miss = missing_events(emits, sorted(merged[key]))
                for event in miss:
                    if f"{name}.{event}" in NO_FEEDBACK:
                        exempt += 1
                        continue
                    gaps.append(f"{route} {key} 未接 {event}（声明 {emits}，已绑 {sorted(merged[key])}）")
                checked += len(subject)
        browser.close()

    if cells < MIN_CELLS:
        print(f"EVENT_WIRING: FAIL (扫描根不全：只扫到 {cells} 张示例卡，低于下限 {MIN_CELLS})")
        return 1
    if checked <= 0:
        print("EVENT_WIRING: FAIL (受检事件数为 0，判据没有真正覆盖被验面)")
        return 1
    if gaps:
        seen: dict[str, int] = {}
        for g in gaps:
            key = re.sub(r"#\S+", "", g.split(" 未接 ")[0]) + " 未接 " + g.split(" 未接 ")[1].split("（")[0]
            seen[key] = seen.get(key, 0) + 1
        print(f"EVENT_WIRING: FAIL ({len(gaps)} 格存在未接事件，去重后 {len(seen)} 类；扫描 {len(routes)} 页 {cells} 卡，受检事件 {checked} 条，豁免 {exempt} 条)")
        for key, n in sorted(seen.items(), key=lambda kv: -kv[1])[:40]:
            print(f"  - {n:3d} 格 {key}")
        return 1
    print(f"EVENT_WIRING: PASS (扫描 {len(routes)} 页 {cells} 卡，受检事件 {checked} 条全部已接；豁免 {exempt} 条（{len(NO_FEEDBACK)} 类非手势事件）)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
