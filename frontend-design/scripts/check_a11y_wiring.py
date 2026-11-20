#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 无障碍接线的静态守卫，两类判据：
       ① 派发了未在 defineEmits 里声明的事件（运行时会告警，父组件 v-on 收不到）；
       ② 绑了 @click 却没有 role / tabindex 的元素（键盘到不了，读屏不认）。
[边界] 只判静态接线，不判键位是否真的能用——键盘行为由 ../scripts/_verify_keyboard.py 在浏览器里实测。
       豁免口径写在 exempt_reason()，与 LOCAL-GUIDE「交互无障碍」一节逐条对应，改一边必须改另一边。
[用法] python scripts/check_a11y_wiring.py
       python scripts/check_a11y_wiring.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "component-library" / "src" / "components"

EMITS_TYPE_RE = re.compile(r"const\s+(\w+)\s*=\s*defineEmits<\{(.*?)\}>\(\)", re.S)
EMITS_ARR_RE = re.compile(r"const\s+(\w+)\s*=\s*defineEmits\(\[(.*?)\]\)", re.S)
EMIT_KEY_RE = re.compile(r"'([\w:-]+)'")

# 模板里的开标签。只收「本该由开发者补语义」的容器标签；
# button / a / input 这类原生可交互元素不进列表，天然豁免。
TAG_RE = re.compile(r"<(div|span|li|td|tr|section|article|p|i|em|strong)\b([^>]*)>", re.S)
CLICK_RE = re.compile(r"@click(?:\.\w+)?\s*=")
ROLE_RE = re.compile(r"\brole\s*=")
TAB_RE = re.compile(r"\btabindex\s*=")
CLASS_RE = re.compile(r'class="([^"]*)"')

# 微型动作：紧贴输入框 / 标签 / 选项卡的清除、关闭、展开箭头。主操作已在键盘上完成，
# 为这些可选微操作在每张表单里多插一个 Tab 停靠点不划算（与 Arco 口径一致）。
MICRO_ACTION = {"input-clear", "x-tag-x", "x-tabs-close", "x-tree-arrow"}


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    return text


def split_template(src: str) -> tuple[str, str]:
    """返回 (脚本区, 模板区)；样式区丢弃。"""
    script = ""
    template = ""
    m = re.search(r"(<script\b.*?</script>)", src, re.S)
    if m:
        script = m.group(1)
    m = re.search(r"(<template\b.*?</template>)", src, re.S)
    if m:
        template = m.group(1)
    return script, template


def class_tokens(classes: str) -> set[str]:
    """[参数] class 属性原值（可能含 ``:class="[...]"``）[返回] 归一后的类名集合。"""
    cleaned = re.sub(r"[\['\]\(\)\{\},]", " ", classes).replace('"', " ").replace("'", " ")
    return {t for t in cleaned.split() if t and not t.startswith("`")}


def exempt_reason(tag: str, attrs: str, classes: str) -> str | None:
    """[参数] tag 标签名, attrs 全部属性, classes class 串 [返回] 豁免理由，不豁免返回 None。"""
    tokens = class_tokens(classes)
    if tokens & MICRO_ACTION:
        return "微型动作不占 Tab 位"
    if "input-shell" in tokens:
        return "点击壳只为把焦点交给内部 input，键盘可直接 Tab 到 input"
    if re.search(r'role="(option|treeitem)"', attrs):
        return "combobox / tree 容器内的项，由上层方向键驱动"
    if tag == "li" and TAB_RE.search(attrs):
        return "列表项模式：保留列表语义，只补 tabindex"
    if any(t.endswith("-trigger") for t in tokens):
        return "触发器包装层，可访问元素由插槽内容提供"
    if any(("mask" in t) or ("scrim" in t) for t in tokens):
        return "遮罩点击关闭，Esc 覆盖同一操作"
    return None


def audit_source(label: str, raw: str) -> list[str]:
    """[参数] label 报告用的文件名, raw 整个 SFC 文本 [返回] 接线缺陷清单。"""
    script_raw, template = split_template(raw)
    script = strip_comments(script_raw)
    findings: list[str] = []

    # ---- ① 未声明就派发的事件 ----
    emit_vars: dict[str, set[str]] = {}
    for m in EMITS_TYPE_RE.finditer(script):
        emit_vars[m.group(1)] = set(EMIT_KEY_RE.findall(m.group(2)))
    for m in EMITS_ARR_RE.finditer(script):
        emit_vars[m.group(1)] = set(EMIT_KEY_RE.findall(m.group(2)))

    for var, names in emit_vars.items():
        for call in re.finditer(r"(?<![\w$.])" + re.escape(var) + r"\(\s*'([\w:-]+)'", script):
            name = call.group(1)
            if name not in names:
                findings.append(f"EMIT_UNDECLARED  {label} :: {name}（{var} 未声明）")

    # ---- ② 可点击但键盘到不了 ----
    for tag in TAG_RE.finditer(template):
        attrs = tag.group(2)
        if not CLICK_RE.search(attrs):
            continue
        if ROLE_RE.search(attrs) and TAB_RE.search(attrs):
            continue
        name = CLASS_RE.search(attrs)
        classes = name.group(1) if name else ""
        if exempt_reason(tag.group(1), attrs, classes):
            continue
        missing = []
        if not ROLE_RE.search(attrs):
            missing.append("role")
        if not TAB_RE.search(attrs):
            missing.append("tabindex")
        tokens = sorted(class_tokens(classes))
        label_cls = tokens[0] if tokens else tag.group(1)
        findings.append(
            f"CLICK_NO_KEY     {label} :: <{tag.group(1)} class=\"{label_cls}\"> 缺 {'/'.join(missing)}"
        )

    return findings


# ---- 阳性对照样本 ----------------------------------------------------------
# 必须报 2 项：没声明就 emit 的 ghost、没有 role/tabindex 的 plain-card。
# 其余六个都是「看着像缺口但按口径豁免」的，报出来即说明豁免表被改坏了。
SELFTEST_BAD = '''<script setup lang="ts">
const emit = defineEmits<{ (e: 'change', v: number): void }>()
emit('change', 1)
emit('ghost', 2)
</script>
<template>
  <div @click="noop" class="plain-card">x</div>
  <span @click="clear" class="input-clear">x</span>
  <span @click="focusInput" :class="['input-shell']">x</span>
  <div role="option" @click="pick">x</div>
  <li tabindex="0" @click="pick">x</li>
  <span class="x-pop-trigger" @click="open">x</span>
  <div class="rail-scrim" @click="close">x</div>
  <button @click="ok">原生按钮不判</button>
</template>
'''

SELFTEST_GOOD = '''<script setup lang="ts">
const emit = defineEmits<{ (e: 'change', v: number): void }>()
emit('change', 1)
</script>
<template>
  <div role="button" tabindex="0" @click="go">x</div>
</template>
'''


def selftest() -> int:
    """[返回] 0 表示判据自证通过。"""
    bad = audit_source("bad.vue", SELFTEST_BAD)
    good = audit_source("good.vue", SELFTEST_GOOD)
    fails: list[str] = []

    undeclared = [line for line in bad if line.startswith("EMIT_UNDECLARED")]
    clickless = [line for line in bad if line.startswith("CLICK_NO_KEY")]
    if len(undeclared) != 1 or "ghost" not in undeclared[0]:
        fails.append(f"阳性对照：未声明事件应只报 ghost，实得 {undeclared}")
    if len(clickless) != 1 or "plain-card" not in clickless[0]:
        fails.append(f"阳性对照：可点击无键盘应只报 plain-card，实得 {clickless}")
    if len(bad) != 2:
        fails.append(f"阳性对照条数不符：期望 2（豁免项不得上抛），实得 {len(bad)}")
    if good:
        fails.append(f"阴性对照误报：{good}")

    if fails:
        print("A11Y_WIRING_SELFTEST: FAIL")
        for f in fails:
            print("  - " + f)
        return 1
    print(
        "A11Y_WIRING_SELFTEST: PASS"
        "（未声明事件与可点击无键盘各报 1 项；微型动作 / 输入壳 / option / li+tabindex / 触发器包装 / 遮罩 / 原生按钮 七类豁免零上抛）"
    )
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    files = sorted(ROOT.rglob("*.vue"))
    if len(files) < 100:
        print(f"A11Y_WIRING: FAIL（只扫到 {len(files)} 个组件，目录或发现逻辑异常）")
        return 1

    findings: list[str] = []
    for path in files:
        try:
            rel = path.relative_to(ROOT.parent)
        except ValueError:
            rel = path
        findings.extend(audit_source(str(rel), path.read_text(encoding="utf-8")))

    if not findings:
        print(f"A11Y_WIRING: PASS ({len(files)} 个组件，无未声明事件、无可点击无键盘项)")
        return 0

    emits = [i for i in findings if i.startswith("EMIT_UNDECLARED")]
    clicks = [i for i in findings if i.startswith("CLICK_NO_KEY")]
    print(f"A11Y_WIRING: FAIL ({len(findings)} 项，扫描 {len(files)} 个组件）")
    print(f"  未声明事件 {len(emits)} 项")
    for line in emits:
        print("    " + line)
    print(f"  可点击无键盘 {len(clicks)} 项")
    for line in clicks:
        print("    " + line)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
