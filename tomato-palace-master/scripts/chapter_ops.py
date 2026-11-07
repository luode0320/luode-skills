#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄殿堂作家 · 章节作战表工具

用法：
    python chapter_ops.py --gen 30                 # 生成 30 章作战表骨架（Markdown）
    python chapter_ops.py --check 章节作战表.md     # 校验节奏合规性
    python chapter_ops.py --check 章节作战表.md --json

校验规则（源自番茄留存机制与 2026-08-31 赛道雷达）：
    R1  每 3 章至少一次小高潮标记
    R2  每 10 章至少一次大反转标记
    R3  连续 3 章同类型爽点 → 警告（读者审美疲劳）
    R4  连续 3 章钩子强度为"弱" → 警告
    R5  第 3 章前未出现高强度爽点（身份反转/生死博弈）→ 警告
    R6  爽点类型分布 → 提示身份反转占比（目标 ≥15%）
    R7  受气/憋屈类章节后 3 章内必须有释放类爽点
    R8  单章字数偏离目标区间（1800-3200）→ 提示

零第三方依赖，仅标准库。
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOOK_STRENGTH = {"强": 3, "中": 2, "弱": 1}

HIGH_IMPACT = ["身份反转", "生死博弈", "打脸", "逆转"]
RELEASE = ["身份反转", "生死博弈", "信息差碾压", "规则破局", "情绪宣泄", "打脸", "逆转", "碾压"]
SUPPRESS = ["憋屈", "受挫", "绝境", "压制", "隐忍", "危机"]

HEADER_ALIASES = {
    "章号": "no",
    "章节": "no",
    "核心事件": "event",
    "事件": "event",
    "爽点类型": "spark",
    "爽点": "spark",
    "章末钩子": "hook",
    "钩子": "hook",
    "钩子强度": "hook",
    "伏笔动作": "foreshadow",
    "伏笔": "foreshadow",
    "字数目标": "words",
    "字数": "words",
}


def parse_table(path):
    text = None
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as f:
                text = f.read()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if text is None:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    rows = []
    header_map = None
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if header_map is None:
            mapped = []
            for c in cells:
                key = None
                for alias, k in HEADER_ALIASES.items():
                    if alias in c:
                        key = k
                        break
                mapped.append(key)
            if sum(1 for m in mapped if m) >= 2:
                header_map = mapped
            continue
        row = {}
        for i, c in enumerate(cells):
            if i < len(header_map) and header_map[i]:
                row[header_map[i]] = c
        if row.get("no"):
            rows.append(row)
    return rows


def to_int(s):
    m = re.search(r"\d+", s or "")
    return int(m.group(0)) if m else None


def normalize_spark(s):
    s = (s or "").strip()
    for k in ["身份反转", "生死博弈", "信息差碾压", "信息差", "规则破局", "情绪宣泄",
              "打脸", "逆转", "碾压", "绝境", "异象", "悬念", "铺垫", "憋屈"]:
        if k in s:
            return k
    return s or "未标注"


def normalize_hook(s):
    s = (s or "").strip()
    for k in ["强", "中", "弱"]:
        if k in s:
            return k
    return "中"


def check(rows):
    issues = []
    stats = {"total": len(rows), "spark_dist": Counter(), "hook_dist": Counter(), "words": []}
    sparks, hooks, nos = [], [], []

    for r in rows:
        no = to_int(r.get("no"))
        if no is None:
            continue
        nos.append(no)
        spark = normalize_spark(r.get("spark"))
        hook = normalize_hook(r.get("hook"))
        sparks.append(spark)
        hooks.append(hook)
        stats["spark_dist"][spark] += 1
        stats["hook_dist"][hook] += 1
        w = to_int(r.get("words"))
        if w:
            stats["words"].append(w)

    # R1 每 3 章至少一次小高潮
    high_set = set(HIGH_IMPACT)
    for i in range(0, len(rows), 3):
        window = sparks[i:i + 3]
        if window and not any(s in high_set or s in RELEASE for s in window):
            issues.append(("R1", "警告", "第 %s-%s 章连续 3 章无高强度爽点，违反「每 3 章一小高潮」"
                           % (nos[i], nos[min(i + 2, len(nos) - 1)])))

    # R2 每 10 章一次大反转
    for i in range(0, len(rows), 10):
        window = sparks[i:i + 10]
        if window and not any(s in high_set for s in window):
            issues.append(("R2", "警告", "第 %s-%s 章无身份反转或生死博弈，缺「每 10 章一大反转」"
                           % (nos[i], nos[min(i + 9, len(nos) - 1)])))

    # R3 连续 3 章同类型
    for i in range(len(sparks) - 2):
        if sparks[i] == sparks[i + 1] == sparks[i + 2] and sparks[i] not in ("未标注",):
            issues.append(("R3", "提示", "第 %s-%s 章连续 3 章同为「%s」，建议换爽点类型"
                           % (nos[i], nos[i + 2], sparks[i])))

    # R4 连续 3 章弱钩子
    for i in range(len(hooks) - 2):
        if hooks[i] == hooks[i + 1] == hooks[i + 2] == "弱":
            issues.append(("R4", "警告", "第 %s-%s 章连续弱钩子，追更比会受损"
                           % (nos[i], nos[i + 2])))

    # R5 前三章高强度爽点
    first3 = sparks[:3]
    if first3 and not any(s in high_set for s in first3):
        issues.append(("R5", "严重", "第 1-3 章未出现「身份反转/生死博弈/打脸/逆转」，"
                       "未满足 2026 年第一钩子要求（身份反转占榜单 32%）"))

    # R6 身份反转占比
    total = max(len(sparks), 1)
    id_ratio = stats["spark_dist"].get("身份反转", 0) / total
    if id_ratio < 0.10:
        issues.append(("R6", "提示", "身份反转占比 %.0f%%（建议 ≥15%%），当前为 2026 年第一钩子"
                       % (id_ratio * 100)))

    # R7 憋屈后 3 章内释放
    for i, s in enumerate(sparks):
        if s in SUPPRESS or "憋屈" in s:
            window = sparks[i + 1:i + 4]
            if window and not any(x in RELEASE for x in window):
                issues.append(("R7", "警告", "第 %s 章憋屈/受挫后 3 章内无释放，"
                               "违反「受气→反击 ≤3 章」" % nos[i]))

    # R8 字数偏离
    for i, w in enumerate(stats["words"]):
        if w < 1800 or w > 3200:
            issues.append(("R8", "提示", "第 %s 章字数目标 %d，建议落在 1800-3200"
                           % (nos[i] if i < len(nos) else i + 1, w)))

    report = {
        "chapters": len(rows),
        "spark_distribution": dict(stats["spark_dist"]),
        "hook_distribution": dict(stats["hook_dist"]),
        "identity_twist_ratio": round(id_ratio, 3),
        "avg_words": round(sum(stats["words"]) / len(stats["words"]), 1) if stats["words"] else 0,
        "issue_count": len(issues),
        "issues": [{"rule": r, "level": lv, "message": m} for r, lv, m in issues],
    }
    return report


GEN_TEMPLATE_SPARKS = [
    ("主角入局 + 核心困局", "绝境", "强"),
    ("金手指首次触发（带代价）", "信息差碾压", "强"),
    ("第一次打脸 / 逆转", "身份反转", "强"),
    ("敌人升级，主角试探边界", "生死博弈", "中"),
    ("拿到关键资源或盟友", "信息差碾压", "中"),
    ("危机爆发，主角受挫（≤3 章内必须还手）", "憋屈", "强"),
    ("反击成功，建立第一次威望", "规则破局", "中"),
    ("更大势力登场，格局拉开", "悬念", "强"),
    ("主角主动出击，展示成长", "信息差碾压", "中"),
    ("卷一大高潮：第一个大反转", "身份反转", "强"),
]


def gen(n):
    lines = ["| 章号 | 核心事件 | 爽点类型 | 章末钩子 | 伏笔动作 | 字数目标 |",
             "|---|---|---|---|---|---|"]
    for i in range(1, n + 1):
        if i <= len(GEN_TEMPLATE_SPARKS):
            ev, sp, hk = GEN_TEMPLATE_SPARKS[i - 1]
        else:
            pos = (i - 1) % 10
            if pos == 3:
                ev, sp, hk = "冲突升级：主角做出关键选择", "生死博弈", "强"
            elif pos == 6:
                ev, sp, hk = "阶段性反击：代价与战果同时到账", "情绪宣泄", "中"
            elif pos == 9:
                ev, sp, hk = "十章大反转：格局级变化", "身份反转", "强"
            else:
                ev, sp, hk = "推进主线，制造信息增量", "信息差碾压", "中"
        fs = "埋 F%d" % (i // 10 + 1) if i % 10 == 3 else ("回收 F%d" % (i // 10) if i % 10 == 8 and i >= 8 else "—")
        lines.append("| %d | %s | %s | %s | %s | 2400 |" % (i, ev, sp, hk, fs))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="番茄殿堂作家 · 章节作战表工具")
    ap.add_argument("--gen", type=int, metavar="N", help="生成 N 章作战表骨架")
    ap.add_argument("--check", metavar="FILE", help="校验作战表 Markdown 文件")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--out", help="输出到文件")
    args = ap.parse_args()

    if args.gen:
        table = gen(args.gen)
        header = "# 章节作战表（%d 章）\n\n> 爽点类型优先级：身份反转 > 生死博弈 > 信息差碾压 > 规则破局 > 情绪宣泄\n" \
                 "> 校验命令：python chapter_ops.py --check 本文件.md\n\n" % args.gen
        content = header + table + "\n"
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(content)
            print("[OK] 已生成 %d 章作战表：%s" % (args.gen, args.out))
        else:
            print(content)
        return

    if not args.check:
        ap.print_help()
        sys.exit(1)

    if not os.path.exists(args.check):
        print("[X] 文件不存在：%s" % args.check)
        sys.exit(2)

    rows = parse_table(args.check)
    if not rows:
        print("[X] 未解析到章节数据。请确认表格含「章号 / 核心事件 / 爽点类型 / 章末钩子」表头。")
        sys.exit(2)

    rep = check(rows)

    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print("=" * 66)
        print("章节作战表校验报告")
        print("=" * 66)
        print("章节数：%d" % rep["chapters"])
        print("爽点类型分布：")
        for k, v in sorted(rep["spark_distribution"].items(), key=lambda x: -x[1]):
            print("   %-12s %d 章" % (k, v))
        print("钩子强度分布：")
        for k in ("强", "中", "弱"):
            if k in rep["hook_distribution"]:
                print("   %-4s %d 章" % (k, rep["hook_distribution"][k]))
        print("身份反转占比：%.0f%%" % (rep["identity_twist_ratio"] * 100))
        print("单章均字数目标：%s" % rep["avg_words"])
        print("-" * 66)
        if rep["issues"]:
            print("发现 %d 项问题：" % rep["issue_count"])
            for it in rep["issues"]:
                print("  [%s][%s] %s" % (it["level"], it["rule"], it["message"]))
        else:
            print("[OK] 未发现问题，节奏合规。")
        print("=" * 66)
        print("规则来源：番茄留存机制 + 2026-08-31 赛道雷达（身份反转 32% / 生死博弈 26%）")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(json.dumps(rep, ensure_ascii=False, indent=2))
        print("[OK] 报告已写入：%s" % args.out)


if __name__ == "__main__":
    main()
