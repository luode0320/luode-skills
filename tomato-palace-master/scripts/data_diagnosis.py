#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄殿堂作家 · 数据回填诊断器

把一个作者后台数据快照，翻译成「阶段判定 → 未达标清单 → 病因排序 → 修复处方 → 7 天动作」。

依据 references/traffic-pool-and-diagnosis.md：
  · 四阶段 + 长线池流量漏斗
  · 阶段及格线（书架比 35% / 追读率 30% / 10 万字完读率 15% / 前 10 章 8% / 7 日追更 12%）
  · 修复顺序铁律：书名简介 → 前 300 字 → 第一章 → 前三章 → 10 万字完读 → 更新稳定

用法（二选一）：
    # 1) 交互式逐项录入
    python data_diagnosis.py

    # 2) 从数据文件读取（key: value 每行一条）
    python data_diagnosis.py --input 后台数据.md

数据文件示例：
    当前字数: 120000
    日均更新字数: 6000
    断更天数: 0
    万字完读率: 13.5
    前10章完读率: 7.2
    七日追更率: 11.0
    书架比: 8.5
    在读人数: 3200
    当月听读收益: 680
    作品评分: 8.2

可选：--json 输出 JSON；--out 报告.md 落盘 Markdown 报告。

零第三方依赖，仅标准库。
"""

import argparse
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FIELDS = [
    ("words", "当前字数", "int", "作品管理页"),
    ("daily", "日均更新字数", "int", "打卡日历（有效过审正文字数）"),
    ("gap_days", "断更天数", "int", "打卡日历"),
    ("wan_read", "10万字完读率(%)", "float", "数据概览（若无填 0）"),
    ("ch10_read", "前10章完读率(%)", "float", "章级数据（若无填 0）"),
    ("follow7", "7日追更率(%)", "float", "数据概览"),
    ("shelf", "书架比（加入书架:阅读=1:x）", "float", "数据概览（填 x 值）"),
    ("readers", "在读人数", "int", "数据概览"),
    ("income", "当月听读收益(元)", "float", "收益中心"),
    ("score", "作品评分", "float", "作品页"),
]

ALIASES = {
    "words": ["当前字数", "字数"], "daily": ["日均更新字数", "日均更新", "日更"],
    "gap_days": ["断更天数", "断更"], "wan_read": ["10万字完读率", "万字完读率", "完读率"],
    "ch10_read": ["前10章完读率", "前十章完读率", "前10章"], "follow7": ["7日追更率", "追更率", "七日追更率"],
    "shelf": ["书架比"], "readers": ["在读人数", "在读"], "income": ["听读收益", "当月听读收益"],
    "score": ["作品评分", "评分"],
}

# 阈值（取自 traffic-pool-and-diagnosis.md，取严口径）
TH = {
    "shelf": 10.0,       # 书架比：1:10 以内为及格（>10 警戒）
    "follow7": 12.0,     # 7 日追更率 >= 12%
    "wan_read": 15.0,    # 10 万字完读率 >= 15%
    "ch10_read": 8.0,    # 前 10 章完读率 >= 8%
    "daily": 4000,       # 验证期日更 >= 4000
    "daily_show": 6000,  # 首秀期日更 => 6000
    "income": 1000.0,    # 星火门槛
    "score": 8.0,        # 作品评分门槛（落笔成笺）
}


def _match_table():
    """构建「别名 -> 字段」匹配表，按别名长度降序，保证更具体的别名优先命中
    （例如「前10章完读率」必须先于通用的「完读率」被匹配）。"""
    pairs = []
    for fid, label, _typ, _src in FIELDS:
        for alias in ALIASES[fid]:
            pairs.append((alias, fid))
        pairs.append((label, fid))
    pairs.sort(key=lambda p: -len(p[0]))
    return pairs


MATCH_TABLE = _match_table()
TYP_OF = dict((f[0], f[2]) for f in FIELDS)


def parse_file(path):
    data = {}
    if not os.path.exists(path):
        return None, "文件不存在：%s" % path
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if ":" not in line and "：" not in line:
                continue
            raw = line.strip().lstrip("-*# ").strip()
            parts = re.split(r"[:：]", raw, maxsplit=1)
            if len(parts) != 2:
                continue
            key, val = parts[0].strip(), parts[1].strip()
            num = re.search(r"-?\d+(?:\.\d+)?", val)
            if not num:
                continue
            for alias, fid in MATCH_TABLE:
                if alias in key:
                    v = float(num.group(0))
                    data[fid] = int(v) if TYP_OF[fid] == "int" else v
                    break
    return data, None


def ask_interactive():
    print("=" * 74)
    print("番茄殿堂作家 · 数据回填诊断（交互式录入）")
    print("=" * 74)
    print("直接回车表示未知/无该项。\n")
    data = {}
    for fid, label, typ, src in FIELDS:
        while True:
            raw = input("%s（%s）：" % (label, src)).strip()
            if raw == "":
                break
            num = re.search(r"-?\d+(?:\.\d+)?", raw)
            if num:
                v = float(num.group(0))
                data[fid] = int(v) if typ == "int" else v
                break
            print("  请输入数字，或直接回车跳过。")
    return data


def stage_of(words):
    if words < 80000:
        return ("L1 冷启动期（1—8 万字）", "点击率（书名/封面/简介）")
    if words < 100000:
        return ("L2 推荐验证期（8—10 万字）", "书架比 35% / 追读率 30% / 10 万字完读率")
    if words < 200000:
        return ("L3 首秀期（10—20 万字）", "10 万字完读 15% / 前 10 章 8% / 7 日追更 12%")
    if words < 500000:
        return ("L4 书测翻盘期（20—50 万字）", "素材点击率 + 完读率")
    if words < 1000000:
        return ("L5 长线加码期（50—100 万字）", "长线完读率 + 追更人数")
    return ("L6 百万字加码期（100 万字+）", "综合数据 + 第二轮书测")


def diagnose(data):
    words = data.get("words", 0)
    stage, stage_kpi = stage_of(words)
    issues = []      # (指标, 实测, 达标线, 严重度)
    causes = []      # (病因, 处方)
    actions = []     # 7 天动作

    # ── 更新稳定性（最高优先，先修最前端）──────────────
    if data.get("gap_days", 0) and data["gap_days"] >= 3:
        issues.append(("断更天数", "%d 天" % data["gap_days"], "0 天", "严重"))
        causes.append((
            "断更 ≥3 天 —— 算法对连载稳定性权重极高，断更三天以上流量断崖式下跌",
            "立刻恢复日更，固定时段（避开 22:00—24:00），此后绝不断更；提前储备 3—7 天存稿"))
        actions.append("今天立刻恢复更新，并写出未来 3 天存稿")
    elif data.get("gap_days", 0) in (1, 2):
        issues.append(("断更天数", "%d 天" % data["gap_days"], "0 天", "警告"))
        causes.append(("存在断更 —— 验证期任意一天断更会直接终止本次验证",
                       "固定更新时段，储备存稿"))
        actions.append("恢复日更并建立 3 天存稿缓冲")

    daily = data.get("daily", 0)
    if daily and daily < TH["daily"]:
        need = TH["daily_show"] if words >= 100000 else TH["daily"]
        issues.append(("日均更新字数", "%d 字" % daily, "≥%d 字" % need, "严重"))
        causes.append(("日均更新不足 —— 验证期要求每天 ≥4000 字；首秀期建议 6000 字",
                       "把日更提到 %d 字，拆成 2—3 章发布，单章不低于 1000 字" % need))
        actions.append("把日更稳定到 %d 字以上" % need)

    # ── 冷启动期：门面 ───────────────────────────────
    if words < 80000:
        causes.append(("冷启动期只测点击率，不考核长留存",
                       "书名必须带赛道热词；封面主体清晰可辨；简介用「人物+变化+代价」句式"))
        actions.append("自检书名/封面/简介：书名最醒目的词，前三章是否真的出现？")

    # ── 书架比 ──────────────────────────────────────
    shelf = data.get("shelf")
    if shelf:
        if shelf > 18:
            issues.append(("书架比", "1:%.1f" % shelf, "≤1:10", "严重"))
            causes.append(("书架比极差 —— 开篇承诺与正文不符，读者「存了不看」",
                           "统一书名/简介与前三章的承诺；提升第一章局面变化强度；重写前 300 字"))
        elif shelf > 10:
            issues.append(("书架比", "1:%.1f" % shelf, "≤1:10", "警告"))
            causes.append(("书架比警戒 —— 加入书架的读者没有转化为持续阅读",
                           "前 10 章补足每章钩子与情绪回报；砍掉无推进过渡段"))
            actions.append("重排未来 10 章细纲，每章补一个章尾钩子")
        elif shelf <= 5:
            causes.append(("书架比优秀（≤1:5）✓ —— 门面承接能力强", "保持现有书名/封面/简介，按计划推进书测与长线加码"))

    # ── 10 万字完读率 ───────────────────────────────
    wr = data.get("wan_read")
    if wr is not None:
        if wr < TH["wan_read"]:
            sev = "严重" if wr < 10 else "警告"
            issues.append(("10 万字完读率", "%.1f%%" % wr, "≥15%", sev))
            causes.append(("10 万字完读率不足 —— 中段注水 / 核心机制未真正运转 / 主线迟迟不立",
                           "砍过渡章，提前第一阶段闭环，让核心卖点多次兑现；每 2 章一次小爽点"))
            actions.append("定位完读率断崖的章节区段，重写该区段的事件密度")
        else:
            causes.append(("10 万字完读率达标（%.1f%%）✓" % wr,
                           "完读率 ≥25% 可争取大推；<25% 继续优化剧情密度"))

    # ── 前 10 章完读率 ──────────────────────────────
    cr = data.get("ch10_read")
    if cr is not None:
        if cr < TH["ch10_read"]:
            issues.append(("前 10 章完读率", "%.1f%%" % cr, "≥8%", "严重"))
            causes.append(("前 10 章完读率低于 8%（腰斩线）—— 开篇与章节钩子系统性不足",
                           "跑 opening_predict.py 重构前三章；前 10 章逐章补三钩制"))
            actions.append("对前 3 章做结构轮重写；第 4—10 章逐章补章尾钩子")

    # ── 7 日追更率 ──────────────────────────────────
    f7 = data.get("follow7")
    if f7 is not None:
        if f7 < TH["follow7"]:
            issues.append(("7 日追更率", "%.1f%%" % f7, "≥12%", "严重"))
            causes.append(("追更率不足 —— 更新不稳定 / 章末钩子同质化 / 情绪回报不足",
                           "固定更新时段；章尾四写法轮换（未完成行动/意外信息/不可撤回选择/后果扩大）；"
                           "每 2 章一次小爽点"))
            actions.append("检查最近 10 章的章尾钩子类型，是否出现连续同类型")
        else:
            causes.append(("7 日追更率达标（%.1f%%）✓" % f7, "保持节奏，注意钩子类型轮换"))

    # ── 作品评分 ────────────────────────────────────
    sc = data.get("score")
    if sc is not None and sc < TH["score"]:
        issues.append(("作品评分", "%.1f" % sc, "≥8.0", "警告"))
        causes.append(("作品评分低于 8.0 —— 结构性问题（逻辑、人设、文笔）已反映到读者打分",
                       "跑 quality-rubric.md 100 分制全面体检；重点修人设一致性与逻辑漏洞；"
                       "跑 tomato_audit.py 做文风体检"))
        actions.append("做一次全书逻辑与人设一致性复盘，列出前 5 个读者会挑的问题")

    # ── 听读收益 ────────────────────────────────────
    inc = data.get("income")
    if inc is not None and inc < TH["income"]:
        causes.append(("听读收益 %.0f 元，低于星火计划 1000 元门槛" % inc,
                       "先修完读率再冲字数档位 —— 先堆字数后修质量等于把钱堆在漏桶里"))

    # ── 处方排序：遵循「先修最前端」铁律（按明确签名提权，避免关键词互相污染）──
    PRIO_RULES = [
        ("断更", 1),
        ("日均更新不足", 2),
        ("冷启动期只测点击率", 3),
        ("书架比极差", 4),
        ("书架比警戒", 5),
        ("前 10 章完读率低于", 6),
        ("10 万字完读率不足", 7),
        ("追更率不足", 8),
        ("作品评分低于", 9),
        ("听读收益", 10),
    ]

    def rank(c):
        text = c[0]
        for key, p in PRIO_RULES:
            if key in text:
                return p
        return 50  # 达标/说明类信息排在最后

    causes_sorted = sorted(causes, key=rank)

    return {
        "stage": stage, "stage_kpi": stage_kpi,
        "issues": issues, "causes": causes_sorted, "actions": actions,
        "data": data,
    }


def md_report(rep, today=""):
    d = rep["data"]
    L = ["# 番茄殿堂作家 · 数据回填诊断报告", "",
         "- 生成日期：%s" % today,
         "- 当前字数：%s" % d.get("words", "未知"),
         "- 所处阶段：**%s**" % rep["stage"],
         "- 本阶段考核指标：%s" % rep["stage_kpi"], "",
         "---", "", "## 一、数据快照", "",
         "| 指标 | 数值 | 达标线 | 判定 |", "|---|---|---|---|"]
    sev_of = {name.replace(" ", ""): sev for name, _m, _l, sev in rep["issues"]}
    judge_rules = {
        # fid: (阈值文案, 判定函数)
        "shelf": ("≤1:10", lambda v: v <= 10),
        "follow7": ("≥12%", lambda v: v >= 12),
        "wan_read": ("≥15%", lambda v: v >= 15),
        "ch10_read": ("≥8%", lambda v: v >= 8),
        "daily": ("≥4000 字", lambda v: v >= 4000),
        "income": ("≥1000 元", lambda v: v >= 1000),
        "score": ("≥8.0", lambda v: v >= 8.0),
        "gap_days": ("0 天", lambda v: v == 0),
    }
    for fid, label, _t, _s in FIELDS:
        if fid not in d:
            continue
        val = d[fid]
        if fid not in judge_rules:
            L.append("| %s | %s | - | - |" % (label, val))
            continue
        th, ok = judge_rules[fid]
        sev = None
        for n, s in sev_of.items():
            if n.replace("(", "").replace(")", "") in label.replace(" ", ""):
                sev = s
                break
            if label.split("(")[0].replace(" ", "") in n:
                sev = s
                break
        if sev:
            judge = "❌ %s" % sev
        elif ok(val):
            judge = "✅ 达标"
        else:
            judge = "⚠️ 未达标"
        L.append("| %s | %s | %s | %s |" % (label, val, th, judge))

    L += ["", "---", "", "## 二、未达标指标清单", ""]
    if rep["issues"]:
        L += ["| 指标 | 实测 | 达标线 | 严重度 |", "|---|---|---|---|"]
        for name, measured, line, sev in rep["issues"]:
            L.append("| %s | %s | %s | %s |" % (name, measured, line, sev))
    else:
        L.append("- 未发现低于阈值的指标（或数据不足）。")

    L += ["", "---", "", "## 三、病因与处方（按修复优先级排序）", "",
          "> 修复顺序铁律：书名简介承诺 → 前 300 字 → 第一章局面变化 → 前三章核心玩法",
          "> → 10 万字完读率 → 更新稳定性 → 更长线结构。**先修最前端的洞。**", ""]
    for i, (cause, fix) in enumerate(rep["causes"], 1):
        L.append("### %d. %s" % (i, cause))
        L.append("")
        L.append("**处方**：%s" % fix)
        L.append("")

    L += ["---", "", "## 四、未来 7 天动作清单", ""]
    if rep["actions"]:
        for i, a in enumerate(rep["actions"], 1):
            L.append("- [ ] Day %d：%s" % (i, a))
    else:
        L.append("- 数据基本健康，保持现有节奏；每 24 小时同一时段记录一次数据用于对比。")

    L += ["", "---", "", "## 五、注意事项", "",
          "- 数据校验建议每 24 小时在**同一时段**对比，避免误判正常波动；",
          "- **验证期与首秀期严禁大改正文、换封面、重写简介**（系统判异常降权）；",
          "- 修改已发布章节会导致**历史数据归零、系统重新评估**，务必谨慎；",
          "- 首秀期前不要开启 3 万字「书荒测试」，会分流验证期关键流量；",
          "- 更新时段避开 22:00—24:00（易卡审导致数据腰斩）。", "",
          "> 本报告为创作侧参考，平台阈值以当期公告与作者后台为准。", ""]
    return "\n".join(L)


def print_report(rep):
    print("=" * 74)
    print("番茄殿堂作家 · 数据回填诊断")
    print("=" * 74)
    print("所处阶段：%s" % rep["stage"])
    print("本阶段考核：%s" % rep["stage_kpi"])
    print("-" * 74)

    print("\n【未达标指标】")
    if rep["issues"]:
        for name, measured, line, sev in rep["issues"]:
            print("  [%s] %s：实测 %s ｜ 达标线 %s" % (sev, name, measured, line))
    else:
        print("  未发现低于阈值的指标（或数据不足）")

    print("\n" + "-" * 74)
    print("【病因与处方】按修复优先级排序（先修最前端）")
    print("-" * 74)
    for i, (cause, fix) in enumerate(rep["causes"], 1):
        print("%d. %s" % (i, cause))
        print("   处方：%s" % fix)
        print()

    print("-" * 74)
    print("【未来 7 天动作】")
    if rep["actions"]:
        for i, a in enumerate(rep["actions"], 1):
            print("  Day %d：%s" % (i, a))
    else:
        print("  数据基本健康，保持节奏；每 24 小时同时段记录一次数据用于对比。")

    print("\n" + "=" * 74)
    print("提醒：验证期/首秀期严禁大改正文·封面·简介；改已发布章节会致历史数据归零。")
    print("=" * 74)


def main():
    ap = argparse.ArgumentParser(description="番茄殿堂作家 · 数据回填诊断器")
    ap.add_argument("--input", metavar="FILE", help="后台数据文件（key: value 每行一条）")
    ap.add_argument("--out", metavar="FILE", help="输出 Markdown 报告")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    if args.input:
        data, err = parse_file(args.input)
        if err:
            print("[X] %s" % err)
            sys.exit(2)
        if not data:
            print("[X] 未从文件中解析出任何指标，请检查格式（如「当前字数: 120000」）")
            sys.exit(2)
    else:
        data = ask_interactive()

    if not data:
        print("[X] 未录入任何数据")
        sys.exit(2)

    rep = diagnose(data)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print_report(rep)

    if args.out:
        import datetime
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md_report(rep, datetime.date.today().isoformat()))
        print("\n[OK] 诊断报告已写入：%s" % args.out)


if __name__ == "__main__":
    main()
