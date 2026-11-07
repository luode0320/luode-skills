#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 死契约守卫：找出声明了却从未被使用的 props / emits。
[边界] 只判「声明了没人用」，不判「用了但没用对」。命中即 FAIL，须人工确认后删声明或补使用。
[说明] 计数前会把「类型字面量」与「withDefaults 默认值对象」整块遮蔽，
       否则只在默认值里回过一次名的 prop 会被误判成已使用——这是这类扫描最主要的漏报源。
[用法] python scripts/check_component_contracts.py
       python scripts/check_component_contracts.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "component-library" / "src" / "components"

TOP_KEY_RE = re.compile(r"^\s{2}([A-Za-z_$][\w$]*)\??\s*:", re.M)
EMIT_KEY_RE = re.compile(r"'([\w:-]+)'")
EMITS_RE = re.compile(r"defineEmits<\{(.*?)\}>\(\)", re.S)
PLAIN_PROPS_RE = re.compile(r"defineProps<\{")


def strip_comments(text: str) -> str:
    """去掉块注释与整行行注释，避免注释里的字符串被当成引用。"""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    return text


def split_blocks(src: str) -> tuple[str, str]:
    """把 SFC 切成 (脚本区, 模板+样式区)。"""
    m = re.search(r"</script>", src)
    if not m:
        return src, ""
    return src[: m.end()], src[m.end():]


def match_brace(text: str, open_idx: int, open_ch: str = "{", close_ch: str = "}") -> int:
    """[参数] text 全文, open_idx 开括号位置 [返回] 配对闭括号下标（找不到返回 -1）。"""
    depth = 0
    for i in range(open_idx, len(text)):
        ch = text[i]
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i
    return -1


def decl_regions(script: str) -> list[tuple[int, int]]:
    """返回所有需要遮蔽的声明区（props 类型字面量 + withDefaults 默认值对象）。"""
    regions: list[tuple[int, int]] = []
    i = 0
    while True:
        m = PLAIN_PROPS_RE.search(script, i)
        if not m:
            break
        brace = m.end() - 1                       # 指向 `{`
        close = match_brace(script, brace)
        if close == -1:
            break
        regions.append((brace, close + 1))
        # 外面是否套着 withDefaults(...)
        head = script.rfind("withDefaults(", 0, m.start())
        if head != -1:
            wd_open = script.index("(", head)
            wd_close = match_brace(script, wd_open, "(", ")")
            if wd_close != -1:
                # defineProps<...>() 结束到 withDefaults 收尾之间即默认值对象
                gt = script.find(">()", close)
                if gt != -1:
                    regions.append((gt + 3, wd_close))
        i = close + 1
    return regions


def mask(text: str, regions: list[tuple[int, int]]) -> str:
    """[参数] text 原文, regions 待遮蔽区 [返回] 同长度的空白替身（偏移不变）。"""
    chars = list(text)
    for start, end in regions:
        for k in range(start, min(end, len(chars))):
            if chars[k] != "\n":
                chars[k] = " "
    return "".join(chars)


def occurrences(name: str, text: str) -> int:
    return len(re.findall(r"(?<![\w$])" + re.escape(name) + r"(?![\w$])", text))


def audit_source(label: str, raw: str) -> list[str]:
    """[参数] label 报告用的文件名, raw 整个 SFC 文本 [返回] 死契约清单。"""
    script_raw, rest = split_blocks(raw)
    script = strip_comments(script_raw)
    prop_regions = decl_regions(script)
    emit_regions = [(m.start(1), m.end(1)) for m in EMITS_RE.finditer(script)]
    # 声明区一律遮蔽：否则 prop/event 会在自己的声明里被数成一次「使用」
    body = mask(script, prop_regions + emit_regions)
    scope = body + "\n" + rest                    # 模板里的引用同样算使用

    findings: list[str] = []

    # props：类型字面量内的顶层 key
    for start, end in prop_regions:
        block = script[start:end]
        if not block.startswith("{"):
            continue                              # 跳过默认值对象区
        for key_match in TOP_KEY_RE.finditer(block):
            name = key_match.group(1)
            if occurrences(name, scope) == 0:
                findings.append(f"PROP_UNUSED   {label} :: {name}")

    # emits
    for m in EMITS_RE.finditer(script):
        for name in sorted(set(EMIT_KEY_RE.findall(m.group(1)))):
            if occurrences(name, scope) == 0:
                findings.append(f"EMIT_UNUSED   {label} :: {name}")

    return findings


# ---- 阳性对照样本 ----------------------------------------------------------
# 三类必须报：彻底没用过的 prop、只在 withDefaults 默认值里出现过的 prop、没派发过的 emit。
# 同时放一个正常组件，证明判据不会把「都在用」误判成死契约。
SELFTEST_BAD = '''<script setup lang="ts">
const props = withDefaults(defineProps<{
  label?: string
  deadProp?: boolean
  onlyInDefaults?: number
}>(), { label: 'x', onlyInDefaults: 3 })
const emit = defineEmits<{ (e: 'change', v: number): void; (e: 'deadEvent', v: number): void }>()
emit('change', 1)
</script>
<template><span :title="props.label">{{ label }}</span></template>
'''

SELFTEST_GOOD = '''<script setup lang="ts">
const props = defineProps<{ label?: string; size?: string }>()
const emit = defineEmits<{ (e: 'change', v: number): void }>()
emit('change', 1)
</script>
<template><span :title="label" :data-size="size">{{ props.label }}</span></template>
'''


def selftest() -> int:
    """[返回] 0 表示判据自证通过。"""
    bad = audit_source("bad.vue", SELFTEST_BAD)
    good = audit_source("good.vue", SELFTEST_GOOD)
    want = {"deadProp", "onlyInDefaults", "deadEvent"}
    got = {line.split("::")[1].strip() for line in bad}
    fails: list[str] = []
    if got != want:
        fails.append(f"阳性对照命中不符：期望 {sorted(want)}，实得 {sorted(got)}")
    if len(bad) != 3:
        fails.append(f"阳性对照条数不符：期望 3，实得 {len(bad)}")
    if good:
        fails.append(f"阴性对照误报：{good}")

    if fails:
        print("CONTRACTS_SELFTEST: FAIL")
        for f in fails:
            print("  - " + f)
        return 1
    print("CONTRACTS_SELFTEST: PASS（死 prop / 只在默认值出现的 prop / 死 emit 三类必报，正常组件零误报）")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    files = sorted(ROOT.rglob("*.vue"))
    if len(files) < 100:
        print(f"CONTRACTS: FAIL（只扫到 {len(files)} 个组件，目录或发现逻辑异常）")
        return 1

    findings: list[str] = []
    for path in files:
        try:
            rel = path.relative_to(ROOT.parent)
        except ValueError:
            rel = path
        findings.extend(audit_source(str(rel), path.read_text(encoding="utf-8")))

    if not findings:
        print(f"CONTRACTS: PASS ({len(files)} 个组件，无死契约)")
        return 0

    print(f"CONTRACTS: FAIL ({len(findings)} 项死契约，扫描 {len(files)} 个组件)")
    for line in findings:
        print("  " + line)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
