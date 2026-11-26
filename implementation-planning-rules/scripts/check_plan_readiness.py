#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""计划完善度闸门机器校验：扫描计划文档，输出 READY / NEEDS_REFINEMENT / BLOCKED。

用法：
    check_plan_readiness.py <plan.md> [--tier full|lite] [--explain]

退出码：READY=0、NEEDS_REFINEMENT=1、BLOCKED=2。
判据细则见 implementation-planning-rules/references/plan-readiness-gate.md。
"""
import argparse
import re
import sys
from pathlib import Path

READY = 0
NEEDS_REFINEMENT = 1
BLOCKED = 2

# 未决标记：命中即 BLOCKED（决策未收敛，禁止开写）
UNDECIDED = re.compile(r"WAITING_DECISION|未决|待用户选择|待确认|\bTBD\b|\bTODO\b")
# 空话占位：完成条件等字段只有这类词视为不可测
VAGUE = re.compile(r"完成即可|正常即可|待补充|后面再|稍后|xxx|XXX")
# 可验证动作：完成条件必须出现其一，否则视为空话
VERIFIABLE = re.compile(r"运行|测试|验证|断言|assert|输出|通过标准|exit\s*=|pytest|curl")
# FEAS 方向级未验证：命中即 BLOCKED
FEAS_UNVERIFIED = re.compile(r"FEAS-[^\n]*(未验证|待验证|未探针)")


def auto_tier(text):
    """按 plan-output-gate 复杂判据自动定档：命中任一即 full。

    [参数] text: 计划文档全文。
    [返回] str：full 或 lite。
    最近修改时间：2026-11-26 23:31:00；新增计划完善度闸门机器校验脚本。
    """
    periods = set(re.findall(r"第[一二三四1-4]期|周期\s*[1-4一二三四]", text))
    if len(periods) >= 2:
        return "full"
    if len(re.findall(r"最小任务", text)) >= 3:
        return "full"
    if re.search(r"跨\s*[2-9两三四]\s*模块", text):
        return "full"
    if re.search(r"时序图|状态迁移|状态机", text):
        return "full"
    return "lite"


def evaluate(text, plan_path):
    """收集 lite 五项问题。

    [参数] text: 计划文档全文；plan_path: 计划文档路径。
    [返回] list[tuple[str, bool]]：(说明, 是否 BLOCKED) 列表。
    最近修改时间：2026-11-26 23:31:00；新增计划完善度闸门机器校验脚本。
    """
    issues = []
    refs = re.findall(r"([^\s`]+\.md)", text)
    base = plan_path.parent
    if not any((base / r).exists() or (Path.cwd() / r).exists() for r in refs):
        issues.append(("来源落盘：未引用真实存在的来源/主文档 .md 路径", False))
    if not re.search(r"^#{1,6}.*(边界|范围|归属)", text, re.M):
        issues.append(("边界清楚：缺少范围/边界/归属章节", False))
    if not re.search(r"(完成条件|验收条件|AC-\d|acceptance)", text):
        issues.append(("完成条件可测：缺少完成/验收条件标记", False))
    elif not VERIFIABLE.search(text) or VAGUE.search(text):
        issues.append(("完成条件可测：AC 缺少可验证动作或含空话占位", False))
    if UNDECIDED.search(text):
        issues.append(("决策无未决：存在 WAITING_DECISION / 未决 / 待确认 / TBD / TODO", True))
    if not re.search(r"(反方批判|反方|devils[- ]advocate|取舍反方)", text, re.I):
        issues.append(("反方批判：缺少反方批判结论段", False))
    return issues


def evaluate_full(text):
    """full 档在 lite 五项之外追加四项。

    [参数] text: 计划文档全文。
    [返回] list[tuple[str, bool]]：(说明, 是否 BLOCKED) 列表。
    最近修改时间：2026-11-26 23:31:00；新增计划完善度闸门机器校验脚本。
    """
    issues = []
    for marker, label in (
        (r"周期", "必填字段：缺实施周期"),
        (r"最小任务", "必填字段：缺最小任务拆分"),
        (r"(真实测试|测试入口)", "必填字段：缺真实测试安排"),
        (r"(验证点|验证步骤)", "必填字段：缺验证点"),
    ):
        if not re.search(marker, text):
            issues.append((label, False))
    if not re.search(r"FEAS-", text):
        issues.append(("FEAS-*：方向级假设缺少探针清单", False))
    elif FEAS_UNVERIFIED.search(text):
        issues.append(("FEAS-*：存在标记为未验证的方向级假设", True))
    chain = [m for m in ("REQ-", "AC-", "CYCLE-", "TASK-", "TEST-", "EVIDENCE-") if m in text]
    if len(chain) < 4:
        issues.append(("追踪链：REQ/AC/CYCLE/TASK/TEST/EVIDENCE 覆盖不足", False))
    if not re.search(r"(跨会话|交接|独立执行)", text):
        issues.append(("跨会话可执行性：缺交接/独立执行说明", False))
    return issues


def main():
    """解析命令行参数并输出三态校验结论。

    [参数] 无：全部参数来自命令行。
    [返回] int：READY=0 / NEEDS_REFINEMENT=1 / BLOCKED=2。
    最近修改时间：2026-11-26 23:31:00；新增计划完善度闸门机器校验脚本。
    """
    parser = argparse.ArgumentParser(description="计划完善度闸门机器校验")
    parser.add_argument("plan", type=Path, help="计划文档路径")
    parser.add_argument("--tier", choices=("full", "lite"), help="强制档位，缺省自动判定")
    parser.add_argument("--explain", action="store_true", help="列出每项的命中详情")
    args = parser.parse_args()

    if not args.plan.is_file():
        print("PLAN READINESS: BLOCKED (tier=N/A)")
        print("- 计划文档不存在：%s" % args.plan)
        return BLOCKED

    text = args.plan.read_text(encoding="utf-8")
    tier = args.tier or auto_tier(text)
    issues = evaluate(text, args.plan)
    if tier == "full":
        issues += evaluate_full(text)

    blocked = any(is_blk for _, is_blk in issues)
    if blocked:
        state, code = "BLOCKED", BLOCKED
    elif issues:
        state, code = "NEEDS_REFINEMENT", NEEDS_REFINEMENT
    else:
        state, code = "READY", READY

    print("PLAN READINESS: %s (tier=%s)" % (state, tier))
    for detail, is_blk in issues:
        print("- [MISS] %s" % detail)
    if args.explain:
        hit = {d.split("：")[0] for d, _ in issues}
        for label in (
            "来源落盘", "边界清楚", "完成条件可测", "决策无未决", "反方批判",
            "必填字段", "FEAS-*", "追踪链", "跨会话可执行性",
        ):
            if label not in hit:
                print("- [OK] %s" % label)
    return code


if __name__ == "__main__":
    sys.exit(main())
