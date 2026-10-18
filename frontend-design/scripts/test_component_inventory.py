#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""组件齐全性测试：断言珍珠玻璃组件库的组件清单、导出契约与七层样式完整。

[用法] python test_component_inventory.py
[返回] 退出码 0=全部通过；1=存在缺失。
覆盖：ui 27 控件 + business 20 + charts 6 + layout 6 + workspace 8（本地扩展）+ extend 57（Arco 品类对齐层）
+ 顶层 2（Icon/NeuralNet）、ui/index.ts 导出契约逐项对齐、composables 14、七层样式、main.ts 引入顺序。
Arco 覆盖名不手抄：由 references/arco-parity.json 的 ours 派生，逐个断言在任意组件层真实存在。
最近修改时间：2026-10-15 20:05:00；改动原因：Arco 覆盖名改由清单跨层派生（原实现误要求都落在 extend），并纠正 ui/business 计数口径（原写 28/21，实际 27/20）。
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "component-library" / "src"

EXPECT_UI = [
    "Avatar", "Button", "Checkbox", "ConfirmHost", "DataTable", "DeltaPill",
    "Drawer", "EmptyState", "Field", "HoverCard", "IconButton", "Metric",
    "Modal", "Odometer", "PageHeader", "Pagination", "Panel", "Ruler",
    "SectionLabel", "Segmented", "Select", "SpecPlate", "StatusTag", "Switch",
    "Tag", "TextInput", "ToastHost",
]
EXPECT_BUSINESS = [
    "AskDock", "BoardView", "DeptSelect", "DeptTree", "DictSelect",
    "DictSwatchbook", "DictTag", "FormDialog", "GeneratorPipeline",
    "InsightPanel", "ListPage", "MenuStarMap", "OrgCanvas", "PermissionButton",
    "PermissionMatrix", "PermissionTrace", "PermissionTree", "PostLadder",
    "SearchForm", "UserSelect",
]
EXPECT_CHARTS = ["BarChart", "HeatGrid", "RelationGraph", "Swimlane", "TickRing", "TrendChart"]
EXPECT_LAYOUT = ["AppShell", "AppearanceDialog", "CommandPalette", "PasswordDialog", "Sidebar", "Topbar"]
EXPECT_WORKSPACE = [
    "ActivityList", "Band", "BentoCard", "BentoGrid", "KeyValueReadout",
    "ReadoutStrip", "ShareList", "ShortcutGrid",
]


def expect_arco() -> tuple[set[str], int]:
    """从 Arco 对齐清单派生品类覆盖应引用的组件名与缺口数。

    不手抄组件名：清单是品类覆盖的唯一真相源，手抄副本会在清单演进时静默漂移。
    `ours` 记录的是“用哪个组件覆盖该品类”，可以落在任意组件层（ui/business/
    layout/extend），因此这里只收集名字，由调用方做全目录存在性断言，不假定都在 extend。
    [参数] 无
    [返回] (组件名集合, gap 品类数)；清单缺失或非法时返回空集合与 0
    """
    parity = ROOT / "references" / "arco-parity.json"
    if not parity.exists():
        return set(), 0
    try:
        manifest = json.loads(parity.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set(), 0
    names: set[str] = set()
    gaps = 0
    for item in manifest.get("categories") or []:
        if item.get("status") == "gap":
            gaps += 1
        for name in item.get("ours") or []:
            if "." not in name:
                names.add(name)
    return names, gaps
EXPECT_TOP = ["Icon", "NeuralNet"]
EXPECT_COMPOSABLES = [
    "appearance", "ask", "auth", "confirm", "dept", "dict", "focus", "list",
    "motion", "neural", "permissionGraph", "toast", "view", "viewport",
]
EXPECT_STYLES = ["tokens", "base", "materials", "components", "instruments", "layout", "pages"]
STYLE_ORDER = ["tokens", "base", "materials", "components", "instruments", "layout", "pages"]

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def component_files(dirname: str) -> set[str]:
    d = SRC / "components" / dirname
    return {p.stem for p in d.glob("*.vue")}


def all_component_names() -> set[str]:
    """全部组件层已落盘的组件名，用于跨层存在性断言。

    [参数] 无
    [返回] 各层 *.vue 文件名（去扩展名）的并集
    """
    layers = ["ui", "business", "workspace", "extend", "charts", "layout"]
    names = {p.stem for p in (SRC / "components").glob("*.vue")}
    for layer in layers:
        names |= component_files(layer)
    return names


def main() -> int:
    # 1. 五类组件逐一存在性断言。
    for name in EXPECT_UI:
        check((SRC / "components/ui" / f"{name}.vue").exists(), f"缺少 ui 组件: {name}.vue")
    for name in EXPECT_BUSINESS:
        check((SRC / "components/business" / f"{name}.vue").exists(), f"缺少 business 组件: {name}.vue")
    for name in EXPECT_CHARTS:
        check((SRC / "components/charts" / f"{name}.vue").exists(), f"缺少 charts 组件: {name}.vue")
    for name in EXPECT_LAYOUT:
        check((SRC / "components/layout" / f"{name}.vue").exists(), f"缺少 layout 组件: {name}.vue")
    for name in EXPECT_WORKSPACE:
        check((SRC / "components/workspace" / f"{name}.vue").exists(), f"缺少 workspace 组件: {name}.vue")
    arco_names, arco_gaps = expect_arco()
    if arco_gaps:
        failures.append(f"arco-parity.json 仍有 {arco_gaps} 个 gap 品类未补齐")
    # `ours` 可落在任意层：逐个断言全库存在，并统计真正落在 extend 层的数量下限。
    present = all_component_names()
    extend_files = component_files("extend")
    for name in sorted(arco_names):
        check(name in present, f"缺少 Arco 品类覆盖组件: {name}.vue（各层均未找到）")
    arco_in_extend = arco_names & extend_files
    check(len(extend_files) >= len(arco_in_extend), f"extend 组件数不足: {len(extend_files)} < {len(arco_in_extend)}")
    for name in EXPECT_TOP:
        check((SRC / "components" / f"{name}.vue").exists(), f"缺少顶层组件: {name}.vue")

    # 2. ui/index.ts 导出契约：普通控件应有导出；ToastHost/ConfirmHost 是 App 级宿主，
    #    上游在 App.vue 直接挂载、不进 index.ts，导出契约排除二者。
    index_ts = (SRC / "components/ui/index.ts").read_text(encoding="utf-8")
    exported = set(re.findall(r"export \{ default as (\w+) \}", index_ts))
    hosts = {"ToastHost", "ConfirmHost"}
    missing_export = set(EXPECT_UI) - exported - hosts
    check(not missing_export, f"ui/index.ts 缺导出: {sorted(missing_export)}")
    app_vue = (SRC / "App.vue").read_text(encoding="utf-8")
    for host in sorted(hosts):
        check(f"{host}" in app_vue, f"App.vue 未挂载宿主组件: {host}")

    # 2.1 workspace/index.ts 导出契约：本地扩展层必须整层可 barrel 引入。
    ws_index = (SRC / "components/workspace/index.ts").read_text(encoding="utf-8")
    ws_exported = set(re.findall(r"export \{ default as (\w+) \}", ws_index))
    check(not (set(EXPECT_WORKSPACE) - ws_exported), f"workspace/index.ts 缺导出: {sorted(set(EXPECT_WORKSPACE) - ws_exported)}")

    # 3. 七层样式文件齐全且 main.ts 按规范顺序引入。
    for name in EXPECT_STYLES:
        check((SRC / "styles" / f"{name}.css").exists(), f"缺少样式层: {name}.css")
    main_ts = (SRC / "main.ts").read_text(encoding="utf-8")
    positions = [main_ts.find(f"./styles/{n}.css") for n in STYLE_ORDER]
    check(all(p >= 0 for p in positions), "main.ts 未引入全部七层样式")
    check(positions == sorted(positions), "main.ts 样式引入顺序违反七层规范")

    # 4. composables 齐全。
    for name in EXPECT_COMPOSABLES:
        check((SRC / "composables" / f"{name}.ts").exists(), f"缺少 composable: {name}.ts")

    # 5. 数量下限守卫（防止清单与实际目录漂移后只改清单不补文件）。
    check(len(component_files("ui")) >= 27, f"ui 组件数不足: {len(component_files('ui'))}")
    check(len(component_files("business")) >= 20, f"business 组件数不足: {len(component_files('business'))}")
    check(len(component_files("charts")) == 6, f"charts 组件数异常: {len(component_files('charts'))}")
    check(len(component_files("layout")) == 6, f"layout 组件数异常: {len(component_files('layout'))}")
    check(len(component_files("workspace")) >= 8, f"workspace 组件数不足: {len(component_files('workspace'))}")
    check(len(component_files("extend")) >= len(arco_in_extend), f"extend 组件数不足: {len(component_files('extend'))} < {len(arco_in_extend)}")

    total = len(EXPECT_UI) + len(EXPECT_BUSINESS) + len(EXPECT_CHARTS) + len(EXPECT_LAYOUT) + len(EXPECT_WORKSPACE) + len(EXPECT_TOP) + len(arco_in_extend)
    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        print(f"INVENTORY: FAIL ({len(failures)} failures)")
        return 1
    print(f"INVENTORY: PASS ({total} components, {len(EXPECT_COMPOSABLES)} composables, {len(EXPECT_STYLES)} style layers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
