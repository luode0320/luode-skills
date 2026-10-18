#!/usr/bin/env python3
"""Arco 品类对齐守卫：核对珍珠玻璃组件库是否覆盖 Arco Design Vue 的全部组件品类。

[用途] 把「按 Arco 补齐、不得遗漏」变成机器可判定项：读 references/arco-parity.json，
       逐条校验 status 与 ours 组件文件是否真实存在，缺口一律判 FAIL。
       并对账 references/arco-categories.json（真实 Arco 包品类清单），
       双向抓出「清单写了 Arco 没有的虚构品类」与「Arco 有但清单漏登的品类」。
[边界] 两份清单来源都是 npm 包 @arco-design/web-vue 的 es/ 目录（权威、可回指、可按记录命令重建），
       不是文档站抓取。本脚本只判定覆盖度，不判定组件实现质量（质量由核对页与还原度守卫负责）。
最近修改时间：2026-10-15 20:23:00；改动原因：一度误录 Arco 不存在的 `segmented` 品类，补真实品类参照与双向对账以杜绝虚构条目。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "component-library"
PARITY = ROOT / "references" / "arco-parity.json"
CATEGORIES = ROOT / "references" / "arco-categories.json"

STATUS_COVERED = "covered"
STATUS_GAP = "gap"
VALID_STATUS = {STATUS_COVERED, STATUS_GAP}


def load_manifest() -> dict:
    """读取对齐清单。

    [参数] 无
    [返回] dict 清单对象；文件缺失或 JSON 非法时返回 None
    """
    if not PARITY.exists():
        print(f"PARITY_MANIFEST_MISSING: {PARITY}")
        return None
    try:
        return json.loads(PARITY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"PARITY_MANIFEST_INVALID: JSON 解析失败 {exc}")
        return None


def load_categories() -> set[str] | None:
    """读取真实 Arco 包品类参照清单，用于抓出虚构条目与漏登品类。

    [参数] 无
    [返回] 品类名集合；参照文件缺失或非法时返回 None（此时跳过对账而非误判）
    """
    if not CATEGORIES.exists():
        return None
    try:
        data = json.loads(CATEGORIES.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return set(data.get("categories") or [])


def find_component_files(name: str) -> list[Path]:
    """按组件名在组件库 src/components 下检索实现文件。

    [参数] name: 组件名（PascalCase）或点号路径（如 composables/appearance.ts）
    [返回] 命中的文件列表，未命中返回空列表
    """
    if "." in name:
        target = LIB / "src" / name
        return [target] if target.exists() else []
    hits: list[Path] = []
    for path in (LIB / "src" / "components").rglob(f"{name}.vue"):
        hits.append(path)
    return hits


def main() -> int:
    """执行对齐校验并输出结论。

    [参数] 无
    [返回] 退出码：0 全部覆盖，1 存在缺口或清单非法
    """
    manifest = load_manifest()
    if manifest is None:
        return 1

    categories = manifest.get("categories") or []
    if not categories:
        print("PARITY: FAIL (清单为空)")
        return 1

    seen: set[str] = set()
    gaps: list[str] = []
    dangling: list[str] = []
    stale: list[str] = []

    for item in categories:
        arco = item.get("arco", "").strip()
        status = item.get("status", "").strip()
        ours = item.get("ours") or []

        if not arco:
            dangling.append("<空品类名>")
            continue
        if arco in seen:
            dangling.append(f"{arco}（清单重复项）")
            continue
        seen.add(arco)

        if status not in VALID_STATUS:
            dangling.append(f"{arco}（status 非法：{status or '缺失'}）")
            continue
        if not ours:
            dangling.append(f"{arco}（未登记任何候选实现）")
            continue

        hits = {name: find_component_files(name) for name in ours}
        missing = [name for name, found in hits.items() if not found]

        if status == STATUS_GAP:
            # 双向漂移：标 gap 但实现已落盘，说明清单没跟上，必须回写状态而非静默通过
            if not missing:
                stale.append(f"{arco}（已实现：{'/'.join(ours)}）")
            else:
                gaps.append(arco)
            continue

        for name in missing:
            dangling.append(f"{arco}::{name}")

    print(f"MODE: Arco 品类对齐（清单 {len(categories)} 条，去重后 {len(seen)} 条）")
    for line in dangling:
        print(f"DANGLING: {line}")
    for line in stale:
        print(f"STALE_GAP: {line}")
    for line in gaps:
        print(f"COVERAGE_GAP: {line}")

    # 与真实 Arco 包品类对账：抓出虚构条目（写了 Arco 没有的）与漏登品类（Arco 有但没写）
    real = load_categories()
    phantom: list[str] = []
    missing_category: list[str] = []
    if real is None:
        print("CATEGORIES_REFERENCE_MISSING: 跳过真实品类对账（references/arco-categories.json 不可用）")
    else:
        phantom = sorted(seen - real)
        missing_category = sorted(real - seen)
        for name in phantom:
            print(f"PHANTOM_CATEGORY: {name}（Arco 包无此品类，疑似虚构）")
        for name in missing_category:
            print(f"MISSING_CATEGORY: {name}（Arco 有但清单漏登）")

    if dangling or gaps or stale or phantom or missing_category:
        print(
            "PARITY: FAIL "
            f"(缺口 {len(gaps)}，失效登记 {len(dangling)}，状态滞后 {len(stale)}，"
            f"虚构品类 {len(phantom)}，漏登品类 {len(missing_category)})"
        )
        return 1

    groups: dict[str, int] = {}
    for item in categories:
        groups[item.get("group", "other")] = groups.get(item.get("group", "other"), 0) + 1
    summary = " ".join(f"{k}:{v}" for k, v in sorted(groups.items()))
    print(f"PARITY: PASS ({len(seen)} 个 Arco 品类全覆盖; {summary})")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
