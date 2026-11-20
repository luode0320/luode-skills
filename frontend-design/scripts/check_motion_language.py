#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[用途] 动效语言守卫：禁止新增浏览器默认 ease，并确认冻结层的默认 ease 都被覆盖块接住。
       三条判据：
       ① 可写层（components/extend、components/workspace）的 transition 必须用具名曲线；
       ② 冻结层（src/styles/*.css）的默认 ease 段必须被 build_motion_overrides 的派生块覆盖；
       ③ 全 src 的 keyframes animation 若带默认 ease / 未声明缓动，必须有对应的
          animation-timing-function 覆盖，或本身就是 linear / --ease-*。
[边界] 只判缓动，不判时长与曲线选择是否合适——那要靠慢放人眼验收。
[用法] python -X utf8 -B frontend-design/scripts/check_motion_language.py
       python -X utf8 -B frontend-design/scripts/check_motion_language.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import motion_language as ml  # noqa: E402
import build_motion_overrides as bmo  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
LIB = SKILL / "component-library"
SRC = LIB / "src"
WRITABLE = ("src/components/extend", "src/components/workspace")

ANIMATION_RE = re.compile(r"(animation\s*:\s*)([^;}]+)(;?)")
NONE_VALUE = re.compile(r"^\s*none\s*$", re.I)


def style_blocks(path: Path) -> list[str]:
    """[返回] .vue 的 <style> 内容；.css 返回全文。"""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".css":
        return [text]
    return [m.group(1) for m in re.finditer(r"<style\b[^>]*>(.*?)</style>", text, re.S)]


def audit_transitions(label: str, css: str) -> list[str]:
    """[参数] 来源标签与样式文本 [返回] 仍是默认 ease 的段。"""
    out: list[str] = []
    for m in ml.TRANSITION_RE.finditer(css):
        for part in ml.split_parts(m.group(2)):
            prop, _dur, timing = ml.parse_part(part)
            if ml.needs_rewrite(timing):
                out.append(f"DEFAULT_EASE     {label} :: {prop} 用 {timing or '缺省 ease'}")
    return out


def covered_selectors() -> set[str]:
    """[返回] 动效覆盖块已接住的 (context, selector) 里的选择器集合。"""
    return {sel.strip() for _ctx, sel, _values in bmo.collect()}


def animated_overrides() -> set[str]:
    """[返回] overrides.css 里已经手写 animation-timing-function 的选择器集合。"""
    text = ml.strip_comments((LIB / "src" / "styles" / "overrides.css").read_text(encoding="utf-8"))
    found: set[str] = set()
    for ctx, selector, body in bmo.parse_rules(text):
        if "animation-timing-function" in body:
            found.update(s.strip() for s in selector.split(","))
    return found


def audit_animations(label: str, css: str, whitelisted: set[str]) -> list[str]:
    """[参数] 来源、样式文本、已有覆盖的选择器 [返回] 缺缓动的动画。"""
    out: list[str] = []
    for m in ANIMATION_RE.finditer(css):
        value = m.group(2).strip()
        if NONE_VALUE.match(value):
            continue
        if "var(--ease-" in value or re.search(r"\blinear\b", value):
            continue
        timing = next((t for t in value.split() if t in ml.EASE_FAMILY), None)
        # 取该音符所在的规则选择器：从上一个 `}` 之后切到本条规则的 `{` 之前。
        # 没有前置 `}` 时要从 0 开始，从 1 开始会把选择器首字符吃掉（自证抓到过）。
        start = css.rfind("{", 0, m.start())
        if start == -1:
            start = 0
        head_start = css.rfind("}", 0, start)
        selector = " ".join(css[head_start + 1:start].split())
        names = {s.strip() for s in selector.split(",")}
        if names & whitelisted:
            continue
        out.append(f"ANIM_NO_CURVE    {label} :: {selector[:48]} 用 {timing or '缺省 ease'}")
    return out


def selftest() -> int:
    fails: list[str] = []
    bad_t = ".a { transition: color .2s ease; }\n.b { transition: opacity .2s; }"
    got = audit_transitions("t.css", ml.strip_comments(bad_t))
    if len(got) != 2:
        fails.append(f"可写层判据漏报：{got}")

    good_t = ".a { transition: color var(--ease-reveal) .2s; }\n.b { transition: width .3s linear; }"
    if audit_transitions("t.css", ml.strip_comments(good_t)):
        fails.append("可写层判据误报已具名曲线的规则")

    bad_a = ".spin { animation: spin .7s linear infinite; }\n.fade { animation: fade-in .2s ease both; }"
    got_a = audit_animations("a.css", ml.strip_comments(bad_a), set())
    if len(got_a) != 1 or "fade" not in got_a[0]:
        fails.append(f"动画判据不符：{got_a}")
    if audit_animations("a.css", ml.strip_comments(".x { animation: none; }"), set()):
        fails.append("animation: none 被误报")
    if audit_animations("a.css", ml.strip_comments(".fade { animation: fade-in .2s ease both; }"), {".fade"}):
        fails.append("已有覆盖的动画仍被误报")

    if fails:
        print("MOTION_LANGUAGE_SELFTEST: FAIL")
        for f in fails:
            print("  - " + f)
        return 1
    print("MOTION_LANGUAGE_SELFTEST: PASS（默认 ease 与缺省缓动必报、具名曲线与 linear 放行、animation:none 与已覆盖动画不误报）")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    findings: list[str] = []

    # ① 可写层：不允许默认 ease
    for rel in WRITABLE:
        for path in sorted((LIB / rel).glob("*.vue")):
            for css in style_blocks(path):
                findings.extend(audit_transitions(f"{rel}/{path.name}", ml.strip_comments(css)))

    # ② 冻结层：默认 ease 必须被派生块接住
    covered = covered_selectors()
    for name in bmo.SOURCE_FILES:
        path = SRC / "styles" / name
        if not path.exists():
            continue
        css = ml.strip_comments(path.read_text(encoding="utf-8"))
        for ctx, selector, body in bmo.parse_rules(css):
            if not bmo.timings_for(selector, body):
                continue
            if selector.strip() not in covered:
                findings.append(f"UNCOVERED        src/styles/{name} :: {selector[:48]} 未被覆盖块接住")
        _ = ctx

    # ③ 动画：默认 ease 必须有覆盖
    whitelisted = animated_overrides()
    for path in sorted(SRC.rglob("*")):
        if path.suffix not in (".vue", ".css") or path.name == "overrides.css":
            continue
        label = str(path.relative_to(LIB)).replace("\\", "/")
        for css in style_blocks(path):
            findings.extend(audit_animations(label, ml.strip_comments(css), whitelisted))

    if not findings:
        print(
            f"MOTION_LANGUAGE: PASS（可写层 {len(WRITABLE)} 个目录零默认 ease；"
            f"冻结层 {len(covered)} 条规则全部被覆盖块接住；动画均有具名曲线或覆盖）"
        )
        return 0

    print(f"MOTION_LANGUAGE: FAIL（{len(findings)} 项）")
    for line in findings:
        print("  " + line)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
