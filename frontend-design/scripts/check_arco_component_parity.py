#!/usr/bin/env python3
"""Arco 组件粒度对齐守卫：核对本地实现是否覆盖 Arco 全部对外导出组件。

[用途] 把「不要遗漏」从品类粒度推进到组件粒度：arco-parity.json 只对齐到 74 个品类目录，
       但 Arco 实际对外导出 131 个组件名（含 Col/Row、InputSearch、RangePicker、MonthPicker 等子组件）。
       本脚本读 references/arco-component-parity.json，逐条校验 kind 与 ours 文件是否真实存在，
       并强制任何 kind=gap 的条目必须清零，否则判 FAIL。
[边界] 两份真相源都取自 npm 包 @arco-design/web-vue@2.58.0 的 es/index.js（可按文件内 extract_command 重建）。
       本脚本只判定覆盖度与登记一致性，不判定组件实现质量（质量由核对页与还原度守卫负责）。
最近修改时间：2026-10-15 20:40:00；改动原因：品类粒度守卫无法发现「目录已对齐但子组件缺失」，新增组件粒度对账。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "component-library"
PARITY = ROOT / "references" / "arco-component-parity.json"
COMPONENTS = ROOT / "references" / "arco-components.json"

KIND_COVERED = "covered"
KIND_MERGED = "merged"
KIND_GAP = "gap"
VALID_KINDS = {KIND_COVERED, KIND_MERGED, KIND_GAP}


def load_json(path: Path) -> dict | None:
    """读取 JSON 清单。

    [参数] path: 清单文件路径
    [返回] dict 清单对象；文件缺失或 JSON 非法时返回 None
    """
    if not path.exists():
        print(f"MANIFEST_MISSING: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"MANIFEST_INVALID: {path} 解析失败 {exc}")
        return None


def find_component(name: str) -> bool:
    """在组件库各层检索实现文件是否存在。

    [参数] name: 组件名（PascalCase）或点号路径（如 composables/appearance.ts）
    [返回] 命中任意一层返回 True，否则 False
    """
    if "." in name:
        return (LIB / "src" / name).exists()
    layers = ["ui", "business", "workspace", "extend", "charts", "layout"]
    if (LIB / "src" / "components" / f"{name}.vue").exists():
        return True
    return any((LIB / "src" / "components" / layer / f"{name}.vue").exists() for layer in layers)


def main() -> int:
    """执行组件粒度对齐校验并输出结论。

    [参数] 无
    [返回] 退出码：0 全覆盖，1 存在缺口或登记不一致
    """
    manifest = load_json(PARITY)
    reference = load_json(COMPONENTS)
    if manifest is None or reference is None:
        return 1

    items = manifest.get("components") or []
    if not items:
        print("COMPONENT_PARITY: FAIL (清单为空)")
        return 1

    real = set(reference.get("top_level") or {}) | set(reference.get("sub_components") or {})
    if not real:
        print("COMPONENT_PARITY: FAIL (参照清单 arco-components.json 为空)")
        return 1

    seen: set[str] = set()
    gaps: list[str] = []
    dangling: list[str] = []
    stale: list[str] = []
    invalid: list[str] = []

    for item in items:
        arco = (item.get("arco") or "").strip()
        kind = (item.get("kind") or "").strip()
        ours = item.get("ours") or []

        if not arco:
            invalid.append("<空组件名>")
            continue
        if arco in seen:
            invalid.append(f"{arco}（清单重复项）")
            continue
        seen.add(arco)

        if kind not in VALID_KINDS:
            invalid.append(f"{arco}（kind 非法：{kind or '缺失'}）")
            continue
        # gap 允许空 ours（尚未登记候选实现），covered/merged 必须写明由谁覆盖
        if kind == KIND_GAP and not ours:
            gaps.append(arco)
            continue
        if not ours:
            invalid.append(f"{arco}（kind={kind} 但未登记候选实现）")
            continue

        missing = [name for name in ours if not find_component(name)]

        if kind == KIND_GAP:
            # 双向漂移：标 gap 但实现已落盘，说明清单没跟上，必须回写而非静默通过
            if ours and not missing:
                stale.append(f"{arco}（已实现：{'/'.join(ours)}）")
            else:
                gaps.append(arco)
            continue

        for name in missing:
            dangling.append(f"{arco}::{name}")

    phantom = sorted(seen - real)
    missing_component = sorted(real - seen)

    print(f"MODE: Arco 组件粒度对齐（清单 {len(items)} 条，参照 {len(real)} 条）")
    for line in invalid:
        print(f"INVALID: {line}")
    for line in dangling:
        print(f"DANGLING: {line}")
    for line in stale:
        print(f"STALE_GAP: {line}")
    for line in phantom:
        print(f"PHANTOM_COMPONENT: {line}（Arco 未导出此名，疑似虚构）")
    for line in missing_component:
        print(f"MISSING_COMPONENT: {line}（Arco 有但清单漏登）")
    for line in gaps:
        print(f"COVERAGE_GAP: {line}")

    if invalid or dangling or stale or phantom or missing_component or gaps:
        print(
            "COMPONENT_PARITY: FAIL "
            f"(缺口 {len(gaps)}，失效登记 {len(dangling)}，状态滞后 {len(stale)}，"
            f"非法条目 {len(invalid)}，虚构 {len(phantom)}，漏登 {len(missing_component)})"
        )
        return 1

    counts: dict[str, int] = {}
    for item in items:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1
    summary = " ".join(f"{k}:{v}" for k, v in sorted(counts.items()))
    print(f"COMPONENT_PARITY: PASS ({len(seen)} 个 Arco 导出组件全覆盖; {summary})")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
