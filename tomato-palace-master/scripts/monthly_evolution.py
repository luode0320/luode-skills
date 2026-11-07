#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄殿堂作家 · 资源库时效检查与月度自动进化 V2

V2 新增能力：
  1. 七大核验主题 × 21 组联网检索关键词矩阵（对齐 references/web-search-protocol.md）
  2. 逐文件时效扫描（每个 references 文件自身的「知识截止」日期）
  3. 技能版本递增（--bump-version，自动改 SKILL.md 的 version 字段）
  4. 一键输出完整进化作业单（--worklist），含每步操作与验收标准
  5. 打包前结构自检（--selfcheck）

用法：
    python monthly_evolution.py --check                    # 检查时效，输出进化任务清单
    python monthly_evolution.py --scan                     # 逐文件时效扫描
    python monthly_evolution.py --matrix                   # 输出联网检索关键词矩阵（21 组）
    python monthly_evolution.py --worklist ./进化作业单.md  # 输出完整进化作业单
    python monthly_evolution.py --verify --note "更新星火门槛口径"
    python monthly_evolution.py --bump-version minor       # 版本递增 2.0.0 -> 2.1.0
    python monthly_evolution.py --selfcheck                # 技能包结构自检
    python monthly_evolution.py --check --today 2026-10-05 # 指定日期（测试用）

时效策略（资源库自身约定）：
    ≤30 天  新鲜，可直接使用
    31-60 天  建议核验后再做重要选题/签约决策
    >60 天  必须核验，输出物需标注「未联网校验」

零第三方依赖，仅标准库。
"""

import argparse
import datetime
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CUTOFF_RE = re.compile(r"知识截止[：:]\s*(\d{4}-\d{2}-\d{2})")
VERSION_RE = re.compile(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.M)

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS_DIR = os.path.join(SKILL_ROOT, "references")

# ── 月度进化必查项：7 大主题 × (目标文件列表, 3 组检索关键词) ──────────────
EVOLUTION_CHECKLIST = [
    (
        "作家福利与签约规则",
        ["references/monetization-welfare-2026.md",
         "references/platform-mechanics-2026.md"],
        ["番茄小说 本年度本月 作家福利 最新规则",
         "番茄小说 全勤奖 星火计划 品质臻选 档位 门槛",
         "番茄小说 完本签约 起笔扬帆奖 品质成就奖 星燃计划"],
    ),
    (
        "低质治理与 AI 内容判定",
        ["references/platform-mechanics-2026.md",
         "references/anti-ai-style.md"],
        ["番茄小说 低质治理 公告 本年度本月",
         "番茄小说 AI生成内容 判定 违规 处罚 数据",
         "网文平台 AI检测 红线 拒稿 标准"],
    ),
    (
        "榜单趋势与热门赛道",
        ["references/genre-atlas-2026.md",
         "references/viral-tracks-2026.md"],
        ["番茄小说 本年度本月 榜单 热门题材 趋势",
         "番茄小说 标签流量 排行 男频 女频",
         "番茄小说 新赛道 蓝海 数据"],
    ),
    (
        "开篇与留存机制",
        ["references/opening-engineering-2026.md",
         "references/traffic-pool-and-diagnosis.md"],
        ["番茄小说 前三章 完读率 及格线 本年度",
         "番茄小说 首秀 验证期 书架比 追读率 达标线",
         "网文 开篇 留存 技巧 本年度 实战"],
    ),
    (
        "书名简介标签公式",
        ["references/title-blurb-tags.md",
         "references/book-test-and-crisis-rescue.md"],
        ["番茄小说 书名 命名 公式 本年度",
         "番茄小说 简介 写法 点击率 转化",
         "番茄小说 书测 封面 测试 规则 变化"],
    ),
    (
        "读者结构与情绪偏好",
        ["references/reader-persona-2026.md",
         "references/reader-psychology.md"],
        ["番茄小说 用户画像 读者结构 本年度",
         "番茄小说 中老年读者 下沉市场 数据",
         "网文 读者 情绪需求 趋势 本年度"],
    ),
    (
        "平台公告 · 征文 · 短剧改编政策",
        ["references/monetization-welfare-2026.md",
         "references/short-drama-adaptation.md"],
        ["番茄小说 本年度本月 征文活动 公告",
         "番茄小说 活动 奖励 扶持 最新",
         "红果短剧 番茄IP 改编 政策 分成"],
    ),
]

# 月度进化后必须同步的目标（打包/安装）
DOWNSTREAM_ACTIONS = [
    "同步更新后的技能目录到本地安装副本 ~/.workbuddy/skills/tomato-palace-master/（删除 scripts/__pycache__）",
    "运行 --bump-version minor 递增版本号",
    "重新打包技能 zip 并按平台结构自检（顶层单一项目目录）",
    "归位交付物：新包 + 历史版本快照（命名 {名称}_v{版本}_r{序号}_{日期}_{变更说明}.zip，严禁覆盖历史）",
]


def read(path):
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def find_changelog():
    cand = os.path.join(REFS_DIR, "changelog.md")
    if os.path.exists(cand):
        return cand
    for root, _dirs, names in os.walk(SKILL_ROOT):
        if "changelog.md" in names:
            return os.path.join(root, "changelog.md")
    return None


def parse_cutoff(text):
    m = CUTOFF_RE.search(text)
    if not m:
        return None
    try:
        return datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def parse_pending(text):
    items = []
    in_sec = False
    for line in text.splitlines():
        if re.match(r"^#{2,3}\s*待核验", line):
            in_sec = True
            continue
        if in_sec and re.match(r"^#{1,2}\s", line):
            break
        if in_sec:
            m = re.match(r"^\s*-\s*\[[ xX]\]\s*(.+)$", line)
            if m:
                items.append(m.group(1).strip())
    return items


# ── 逐文件时效扫描 ────────────────────────────────────────────────
def scan_references(today):
    rows = []
    if not os.path.isdir(REFS_DIR):
        return rows
    for name in sorted(os.listdir(REFS_DIR)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(REFS_DIR, name)
        text = read(path)
        cutoff = parse_cutoff(text)
        lines = text.count("\n") + 1
        chars = len(text)
        if cutoff:
            age = (today - cutoff).days
            status = "新鲜" if age <= 30 else ("建议核验" if age <= 60 else "必须核验")
        else:
            age = None
            status = "无标注"
        rows.append({
            "file": name, "lines": lines, "chars": chars,
            "cutoff": cutoff.isoformat() if cutoff else "-",
            "age_days": age, "status": status,
        })
    return rows


def analyze(today):
    path = find_changelog()
    if not path:
        return {"error": "未找到 references/changelog.md"}
    text = read(path)
    cutoff = parse_cutoff(text)
    if not cutoff:
        return {"error": "changelog.md 中未找到「知识截止：YYYY-MM-DD」标记"}

    age = (today - cutoff).days
    if age <= 30:
        status, action = "新鲜", "可直接使用，无需核验"
    elif age <= 60:
        status, action = "建议核验", "重要选题/签约决策前建议联网复核"
    else:
        status, action = "必须核验", "所有输出物需标注「未联网校验」，并立刻执行月度进化"

    scans = scan_references(today)
    return {
        "changelog_path": path,
        "cutoff": cutoff.isoformat(),
        "today": today.isoformat(),
        "age_days": age,
        "status": status,
        "action": action,
        "pending_items": parse_pending(text),
        "checklist": EVOLUTION_CHECKLIST,
        "downstream": DOWNSTREAM_ACTIONS,
        "reference_count": len(scans),
        "reference_lines": sum(r["lines"] for r in scans),
        "reference_chars": sum(r["chars"] for r in scans),
        "scans": scans,
    }


def print_check(rep):
    if "error" in rep:
        print("[X] %s" % rep["error"])
        return
    print("=" * 74)
    print("番茄殿堂作家 · 资源库时效检查（V2）")
    print("=" * 74)
    print("知识截止：%s" % rep["cutoff"])
    print("当前日期：%s" % rep["today"])
    print("滞后天数：%d 天" % rep["age_days"])
    print("时效状态：%s —— %s" % (rep["status"], rep["action"]))
    print("资源库体量：%d 个文件 / %d 行 / %d 字符"
          % (rep["reference_count"], rep["reference_lines"], rep["reference_chars"]))
    print("-" * 74)

    print("\n【月度进化任务清单】逐项联网核验并更新对应文件：\n")
    total_kw = 0
    for i, (name, targets, keywords) in enumerate(rep["checklist"], 1):
        total_kw += len(keywords)
        print("%d. %s" % (i, name))
        for t in targets:
            print("   目标文件：%s" % t)
        print("   建议搜索：")
        for k in keywords:
            print("     · %s" % k)
        print()
    print("关键词组总数：%d" % total_kw)

    if rep["pending_items"]:
        print("-" * 74)
        print("【待核验遗留项】（来自 changelog.md）\n")
        for it in rep["pending_items"]:
            print("  [ ] %s" % it)
        print()

    print("-" * 74)
    print("【进化后必须同步的动作】\n")
    for i, a in enumerate(rep["downstream"], 1):
        print("  %d) %s" % (i, a))
    print()
    print("-" * 74)
    print("完成核验后执行：python monthly_evolution.py --verify --note \"本次变更摘要\"")
    print("=" * 74)


def print_scan(rows):
    print("=" * 92)
    print("番茄殿堂作家 · 资源库逐文件时效扫描")
    print("=" * 92)
    print("%-42s %6s %8s %12s %8s %s" % ("文件", "行数", "字符", "知识截止", "滞后", "状态"))
    print("-" * 92)
    for r in rows:
        age = "-" if r["age_days"] is None else ("%d 天" % r["age_days"])
        print("%-42s %6d %8d %12s %8s %s"
              % (r["file"], r["lines"], r["chars"], r["cutoff"], age, r["status"]))
    print("-" * 92)
    print("合计：%d 个文件 / %d 行 / %d 字符"
          % (len(rows), sum(r["lines"] for r in rows), sum(r["chars"] for r in rows)))
    stale = [r["file"] for r in rows if r["status"] in ("必须核验", "无标注")]
    print("优先处理（必须核验/无标注）：%s" % ("、".join(stale) if stale else "无"))
    print("=" * 92)


def print_matrix():
    print("=" * 74)
    print("番茄殿堂作家 · 月度进化联网检索关键词矩阵")
    print("=" * 74)
    n = 0
    for i, (name, targets, keywords) in enumerate(EVOLUTION_CHECKLIST, 1):
        print("\n主题 %d：%s" % (i, name))
        for k in keywords:
            n += 1
            print("  %2d. %s" % (n, k))
        print("  → 更新目标：%s" % "、".join(targets))
    print("\n" + "=" * 74)
    print("共 %d 组关键词，覆盖 7 大主题。检索规范见 references/web-search-protocol.md" % n)
    print("=" * 74)


def worklist_md(rep):
    L = ["# 番茄殿堂作家 · 资源库月度进化作业单", "",
         "- 生成日期：%s" % rep.get("today", ""),
         "- 当前知识截止：%s" % rep.get("cutoff", ""),
         "- 滞后天数：%s 天" % rep.get("age_days", ""),
         "- 时效状态：**%s** —— %s" % (rep.get("status", ""), rep.get("action", "")),
         "- 资源库体量：%d 个文件 / %d 行" % (rep.get("reference_count", 0), rep.get("reference_lines", 0)),
         "",
         "---", "", "## 第一步 · 联网核验（7 大主题 / 21 组关键词）", ""]

    n = 0
    for i, (name, targets, keywords) in enumerate(rep.get("checklist", []), 1):
        L.append("### %d. %s" % (i, name))
        L.append("")
        L.append("更新目标：%s" % "、".join("`%s`" % t for t in targets))
        L.append("")
        L.append("| # | 建议检索关键词 | 核验结论 | 是否变更 |")
        L.append("|---|---|---|---|")
        for k in keywords:
            n += 1
            L.append("| %d | %s | | □ 变更 □ 不变 |" % (n, k))
        L.append("")

    L += ["---", "", "## 第二步 · 更新资源库", "",
          "1. 按核验结果更新上表对应文件；",
          "2. 保留 `【官方】` / `【实操】` / `【分歧】` 三级标注；",
          "3. 每条新增结论必须带来源与日期；",
          "4. 分歧口径**并列保留**，并说明保守取法。", "",
          "---", "", "## 第三步 · 记录进化", "",
          "1. 在 `references/changelog.md` 追加一条进化记录（**只增不改**，勿覆盖历史记录）；",
          "2. 执行：`python monthly_evolution.py --verify --note \"本次变更摘要\"`；",
          "3. 复跑 `python monthly_evolution.py --check` 确认状态回到「新鲜」。", "",
          "---", "", "## 第四步 · 同步与打包", ""]
    for i, a in enumerate(rep.get("downstream", []), 1):
        L.append("%d. %s" % (i, a))
    L += ["", "---", "", "## 第五步 · 逐文件时效复查", "",
          "| 文件 | 行数 | 知识截止 | 滞后 | 状态 |", "|---|---|---|---|---|"]
    for r in rep.get("scans", []):
        age = "-" if r["age_days"] is None else ("%d 天" % r["age_days"])
        L.append("| `%s` | %d | %s | %s | %s |"
                 % (r["file"], r["lines"], r["cutoff"], age, r["status"]))
    L += ["", "---", "",
          "> 作业完成后，把本次发现的新 know-how（触发词盲区 / 新扣分项 / 新赛道配方）",
          "> 回流到对应资源库文件，做到**越用越强**。", ""]
    return "\n".join(L)


def do_verify(note, today):
    path = find_changelog()
    if not path:
        print("[X] 未找到 references/changelog.md")
        return 1
    text = read(path)
    if not CUTOFF_RE.search(text):
        print("[X] changelog.md 中未找到「知识截止：YYYY-MM-DD」标记")
        return 1

    text = CUTOFF_RE.sub("知识截止：%s" % today.isoformat(), text, count=1)

    lines = ["", "## 进化记录 — %s" % today.isoformat(), "",
             "- **知识截止更新至：%s**" % today.isoformat(),
             "- 变更摘要：%s" % (note or "（未填写摘要）"),
             "- 核验主题：7 大主题 / 21 组关键词（对齐 web-search-protocol.md）",
             "- 核验方式：联网复核（详见各资源库文件标注）",
             "- 资源库体量：%d 个文件" % len(scan_references(today)),
             ""]
    entry = "\n".join(lines)

    if not text.endswith("\n"):
        text += "\n"
    text += entry
    write(path, text)
    print("[OK] 知识截止已更新为 %s" % today.isoformat())
    print("[OK] 进化记录已追加到：%s" % path)
    print("请复跑：python monthly_evolution.py --check")
    return 0


# ── 版本递增 ────────────────────────────────────────────────────
def do_bump(kind, today):
    skill_md = os.path.join(SKILL_ROOT, "SKILL.md")
    if not os.path.exists(skill_md):
        print("[X] 未找到 SKILL.md：%s" % skill_md)
        return 1
    text = read(skill_md)
    m = VERSION_RE.search(text)
    if not m:
        print("[X] SKILL.md 中未找到 version 字段（形如 version: 2.0.0）")
        return 1
    cur = m.group(1)
    major, minor, patch = (int(x) for x in cur.split("."))
    if kind == "major":
        major, minor, patch = major + 1, 0, 0
    elif kind == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1
    new = "%d.%d.%d" % (major, minor, patch)
    text = VERSION_RE.sub("version: %s" % new, text, count=1)
    write(skill_md, text)
    print("[OK] SKILL.md 版本已递增：%s -> %s" % (cur, new))
    print("提醒：打包归档命名使用 {名称}_v%s_r{序号}_%s_{变更说明}.zip" % (new, today.isoformat()))
    return 0


# ── 技能包结构自检 ──────────────────────────────────────────────
FRONTMATTER_REQUIRED = [
    "name", "display_name", "display_name_en", "description",
    "description_zh", "description_en", "version", "author",
]
ALLOWED_TOP_DIRS = {"references", "scripts", "templates", "assets", "README.md", "SKILL.md"}


def do_selfcheck():
    ok = True
    print("=" * 74)
    print("番茄殿堂作家 · 技能包结构自检")
    print("=" * 74)

    skill_md = os.path.join(SKILL_ROOT, "SKILL.md")
    if not os.path.exists(skill_md):
        print("[X] 缺少 SKILL.md")
        return 1
    text = read(skill_md)
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        print("[X] SKILL.md 缺少 frontmatter 块")
        ok = False
    else:
        keys = []
        for line in fm.group(1).split("\n"):
            if not line.strip() or line.startswith(" "):
                continue
            if ":" in line:
                keys.append(line.split(":", 1)[0].strip())
        missing = [k for k in FRONTMATTER_REQUIRED if k not in keys]
        print("[%s] frontmatter 必填字段：%s"
              % ("OK" if not missing else "X", "齐全" if not missing else "缺 %s" % missing))
        if missing:
            ok = False
        if "name" in keys:
            nm = re.search(r"^name:\s*(\S+)", fm.group(1), re.M)
            folder = os.path.basename(SKILL_ROOT.rstrip("\\/"))
            if nm and nm.group(1) != folder:
                print("[X] name(%s) != 目录名(%s)" % (nm.group(1), folder))
                ok = False
            else:
                print("[OK] name 与目录名一致：%s" % folder)
        ver = VERSION_RE.search(text)
        print("[OK] version：%s" % (ver.group(1) if ver else "未找到"))

    print("-" * 74)
    print("一级目录/文件清单：")
    for name in sorted(os.listdir(SKILL_ROOT)):
        p = os.path.join(SKILL_ROOT, name)
        tag = "目录" if os.path.isdir(p) else "文件"
        flag = "" if name in ALLOWED_TOP_DIRS else "   <- 非平台标准目录，需确认"
        if name == "__pycache__":
            flag = "   <- 应删除"
            ok = False
        print("  [%s] %s%s" % (tag, name, flag))
        if name not in ALLOWED_TOP_DIRS and name != "__pycache__":
            ok = False

    print("-" * 74)
    refs = [f for f in os.listdir(REFS_DIR)] if os.path.isdir(REFS_DIR) else []
    print("[%s] references 文件数：%d" % ("OK" if refs else "X", len(refs)))

    # 检查 SKILL.md 中 @references/ 引用是否都存在
    broken = []
    for m in re.finditer(r"@references/([\w\-.]+\.md)", text):
        if m.group(1) not in refs:
            broken.append(m.group(1))
    for m in re.finditer(r"`references/([\w\-.]+\.md)`", text):
        if m.group(1) not in refs:
            broken.append(m.group(1))
    print("[%s] SKILL.md 引用可解析：%s"
          % ("OK" if not broken else "X", "全部存在" if not broken else "断链 %s" % sorted(set(broken))))
    if broken:
        ok = False

    print("=" * 74)
    print("自检结果：%s" % ("通过" if ok else "存在问题，请修复后再打包"))
    print("=" * 74)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="番茄殿堂作家 · 资源库时效检查与月度进化 V2")
    ap.add_argument("--check", action="store_true", help="检查时效并输出进化任务清单")
    ap.add_argument("--scan", action="store_true", help="逐文件时效扫描")
    ap.add_argument("--matrix", action="store_true", help="输出联网检索关键词矩阵")
    ap.add_argument("--worklist", metavar="FILE", help="输出完整进化作业单（Markdown）")
    ap.add_argument("--verify", action="store_true", help="确认本次进化完成，更新知识截止")
    ap.add_argument("--bump-version", choices=["major", "minor", "patch"],
                    help="递增 SKILL.md 版本号")
    ap.add_argument("--selfcheck", action="store_true", help="技能包结构自检")
    ap.add_argument("--note", default="", help="本次变更摘要（配合 --verify）")
    ap.add_argument("--report", metavar="FILE", help="输出 Markdown 报告到文件")
    ap.add_argument("--today", help="指定当前日期 YYYY-MM-DD（测试用）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    if args.today:
        try:
            today = datetime.date.fromisoformat(args.today)
        except ValueError:
            print("[X] --today 格式应为 YYYY-MM-DD")
            sys.exit(1)
    else:
        today = datetime.date.today()

    if args.verify:
        sys.exit(do_verify(args.note, today))
    if args.bump_version:
        sys.exit(do_bump(args.bump_version, today))
    if args.selfcheck:
        sys.exit(do_selfcheck())
    if args.matrix:
        print_matrix()
        return
    if args.scan or args.worklist:
        rep = analyze(today)
        if "error" in rep:
            print("[X] %s" % rep["error"])
            sys.exit(2)
        if args.scan:
            print_scan(rep["scans"])
        if args.worklist:
            write(args.worklist, worklist_md(rep))
            print("[OK] 进化作业单已写入：%s" % args.worklist)
        return

    rep = analyze(today)
    if "error" in rep:
        print("[X] %s" % rep["error"])
        sys.exit(2)

    if args.json:
        out = dict(rep)
        out["checklist"] = [
            {"topic": n, "targets": t, "keywords": k} for n, t, k in rep["checklist"]
        ]
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print_check(rep)

    if args.report:
        write(args.report, worklist_md(rep))
        print("\n[OK] 进化报告已写入：%s" % args.report)

    if not args.check and not args.report and not args.json:
        ap.print_help()


if __name__ == "__main__":
    main()
