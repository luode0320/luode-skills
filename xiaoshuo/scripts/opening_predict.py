#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄殿堂作家 · 开篇留存预测器（开篇 100 分制 + 十二类低留存检测）

依据 references/opening-engineering-2026.md：
  · 四时间窗口（前 300 字 / 第一章 / 前三章 / 前三万字）
  · 开篇 100 分评分表（8 模块）
  · 十二类低留存开篇自检清单
  · 3 秒停留率与前三句公式

用法：
    python opening_predict.py <稿件文件或目录>
    python opening_predict.py 第01章.md --json
    python opening_predict.py ./稿件 --window 300

输出：
    1. 总分（/100）与判定（<70 优先重构 / 70-84 定向修订 / >=85 可交付）
    2. 八模块逐项得分与依据
    3. 十二类低留存问题命中清单（逐条定位）
    4. 前三句体检
    5. 定向修订建议（三轮法）

零第三方依赖，仅标准库。
"""

import argparse
import glob
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── 判定用词库 ──────────────────────────────────────────────────
GENRE_WORDS = {
    "玄幻": ["修仙", "灵根", "宗门", "元婴", "功法", "仙", "道", "境界", "灵石"],
    "都市": ["公司", "老板", "同事", "手机", "地铁", "医院", "派出所", "合同", "写字楼"],
    "悬疑": ["线索", "证物", "尸", "凶手", "监控", "报警", "真相", "密室", "失踪"],
    "言情": ["他", "她", "婚", "爱", "手", "心跳", "吻", "情侣", "结婚"],
    "年代": ["公社", "粮票", "收音机", "喇叭裤", "供销社", "下乡", "工分", "八零", "七零"],
    "末世": ["丧尸", "末日", "物资", "安全区", "变异", "废墟", "幸存"],
    "历史": ["陛下", "朝", "将军", "县令", "奏折", "军", "城", "王爷"],
    "系统": ["系统", "面板", "提示", "任务", "奖励", "宿主"],
}

CONFLICT_WORDS = [
    "死", "刀", "血", "打", "砸", "抓", "骂", "逼", "抢", "烧", "绑", "追",
    "吼", "摔", "掐", "撞", "砸烂", "撕", "反手", "爆炸", "倒计时", "危",
]

COST_WORDS = [
    "失去", "代价", "否则", "不然", "就完了", "会死", "活不过", "赔", "抵押",
    "只剩", "最后", "再没有", "永远", "别想", "救不", "做不到",
]

CHANGE_WORDS = [
    "变了", "再也", "从此", "不一样", "回不去", "不在", "原来", "竟然",
    "发现", "打开", "亮起", "响了", "推门", "出现", "不见",
]

MECH_WORDS = [
    "系统", "能够", "可以看到", "能力", "可以", "只要", "就能", "规则",
    "察觉", "预知", "看见", "听见", "读到", "翻译", "回溯",
]

# 暴露性铺陈（AI 与新人共性）标记
EXPOSITION_MARKS = [
    "这是一个", "在这个世界", "相传", "据说", "很久很久以前", "自古以来",
    "传说", "大陆", "位面", "等级划分", "分为", "共分", "体系", "历史",
    "出生于", "从那以后", "自此",
]

WEATHER_OPEN = re.compile(r"^[\s　]*(天空|天色|夜色|阳光|月光|雨|风|云|雪|清晨|傍晚|黄昏|夕阳|天气)")
DREAM_OPEN = re.compile(r"^(我)?(做|梦见)了一个梦|^梦里|^梦中|^他梦见|^她梦见")
MEETING_MARKS = re.compile(r"(会议室|大会上|大厅里|众人|所有人|纷纷|依次|介绍|点了名|报名)")
PASSIVE_MARKS = re.compile(r"(被通知|被告知|被叫|被安排|被命令|被带|被拉着|被推)")
SUFFER_MARKS = re.compile(r"(跪下|道歉|打脸|羞辱|嘲笑|讥讽|看不起|滚出去|废物)")
MYSTERY_MARKS = re.compile(r"(秘密|真相|谜|不知为何|莫名|隐隐|似乎藏|说不清)")
FREE_LUNCH_MARKS = re.compile(r"(无所不能|无敌|一键|瞬间解决|轻松搞定|不费吹灰之力)")
FLASHBACK_MARKS = re.compile(r"(回忆起|想起小的时候|那年冬天|小时候|童年|当年)")
APOLOGY_MARKS = re.compile(r"(新人|第一次写|慢热|文笔不好|写得不好|请见谅|轻喷|求包容)")

HOOK_PATTERNS = {
    "未完成行动": re.compile(r"(抬起手|伸手|按下了|拨出|拉开|推开门|举起了|掏出|写下)"),
    "意外信息": re.compile(r"(上面写着|背面|纸条|屏幕上显示|短信|突然响|照片上)"),
    "不可撤回选择": re.compile(r"(扔进|签下|烧了|删掉|撕了|按下了确认|挂了电话)"),
    "后果扩大": re.compile(r"(警笛|门外|身后的|更糟|而这时|与此同时|另一边)"),
}


def read(path):
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def collect(path):
    if os.path.isdir(path):
        files = sorted(glob.glob(os.path.join(path, "*.md")) + glob.glob(os.path.join(path, "*.txt")))
        if not files:
            return None, "目录下未找到 .md/.txt 稿件"
        return files, None
    if os.path.isfile(path):
        return [path], None
    return None, "路径不存在：%s" % path


def split_chapters(text):
    """按「第N章」或「# 」标题切分。"""
    parts = re.split(r"\n(?=\s*(?:第[零一二三四五六七八九十百\d]+章|#{1,3}\s))", text)
    parts = [p for p in parts if p.strip()]
    return parts or [text]


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[。！？!?…])", text) if s.strip()]


def count_hits(text, words):
    return sum(text.count(w) for w in words)


def dense_paragraphs(text, limit=150):
    out = []
    for p in re.split(r"\n\s*\n|\n", text):
        p = p.strip()
        if len(p) > limit:
            out.append(p[:40] + "…（%d 字）" % len(p))
    return out


def score_module_a(front, all_text):
    """A 类型与卖点清晰 15"""
    detail = []
    hits = {}
    for genre, words in GENRE_WORDS.items():
        c = count_hits(front, words)
        if c:
            hits[genre] = c
    if hits:
        top = max(hits, key=hits.get)
        pts = 12 if len(hits) == 1 else 9
        detail.append("前 300 字命中类型词：%s（%d 次）" % (top, hits[top]))
        if len(hits) == 1:
            pts += 3
            detail.append("类型指向单一清晰 ✓")
        else:
            detail.append("命中多类型（%s），类型指向略杂 → 建议收敛" % "、".join(hits))
    else:
        pts = 4
        detail.append("前 300 字未见明确类型词 → 读者可能无法判断题材")
    return min(pts, 15), detail


def score_module_b(front, first_chapters):
    """B 主角可跟随 15"""
    detail = []
    pts = 0
    # 视角识别
    fp = len(re.findall(r"(^|[。！？\n\"“])我[^们]", front))
    tp = len(re.findall(r"(他|她)", front))
    if fp > tp:
        pts += 4
        detail.append("第一人称视角清楚 ✓")
    elif tp >= 3:
        pts += 4
        detail.append("第三人称视角清楚（他/她出现 %d 次）✓" % tp)
    else:
        pts += 1
        detail.append("主视角不明确 → 读者容易走神")

    # 主角主动动作
    act = len(re.findall(r"(他|她|我)(说|问|抓|跑|拿|推|扔|走|站|坐|抬|伸|咬|喊|看|盯|夺)", front))
    if act >= 4:
        pts += 7
        detail.append("前 300 字主角主动动作 %d 次，主角在做事 ✓" % act)
    elif act >= 2:
        pts += 4
        detail.append("前 300 字主角主动动作 %d 次，偏少" % act)
    else:
        detail.append("前 300 字主角几乎没有主动动作 → 疑似被剧情搬运")

    # 欲望/目标词
    want = len(re.findall(r"(要|想|必须|得|一定要|不能|别想|求|为了)", front))
    if want >= 3:
        pts += 4
        detail.append("出现明确欲望/目标表述 %d 次 ✓" % want)
    elif want >= 1:
        pts += 2
        detail.append("欲望/目标表述较弱（%d 次）" % want)
    else:
        detail.append("未出现渴望/目标 → 读者不知主角要什么")
    return min(pts, 15), detail


def score_module_c(front, three):
    """C 冲突与代价 15"""
    detail = []
    pts = 0
    c = count_hits(front, CONFLICT_WORDS)
    if c >= 5:
        pts += 8
        detail.append("前 300 字冲突词 %d 次，压迫感强 ✓" % c)
    elif c >= 2:
        pts += 5
        detail.append("前 300 字冲突词 %d 次，偏弱" % c)
    else:
        detail.append("前 300 字几乎无冲突信号 → 3 秒停留率危险")

    cost = count_hits(three, COST_WORDS)
    if cost >= 3:
        pts += 7
        detail.append("前三章出现失败代价表述 %d 次 ✓" % cost)
    elif cost >= 1:
        pts += 4
        detail.append("失败代价表述不足（%d 次）" % cost)
    else:
        detail.append("未写明失败代价 → 危险只是灾难展示，读者不会关心后果")
    return min(pts, 15), detail


def score_module_d(ch1, three):
    """D 局面变化 15"""
    detail = []
    pts = 0
    c1 = count_hits(ch1, CHANGE_WORDS)
    if c1 >= 4:
        pts += 8
        detail.append("第一章出现局面变化信号 %d 次 ✓" % c1)
    elif c1 >= 2:
        pts += 5
        detail.append("第一章局面变化信号偏少（%d 次）" % c1)
    else:
        detail.append("第一章未见明显局面变化 → 删掉本章故事是否毫无损失？")

    c3 = count_hits(three, CHANGE_WORDS)
    if c3 >= 10:
        pts += 7
        detail.append("前三章变化信号密集（%d 次）✓" % c3)
    elif c3 >= 5:
        pts += 4
        detail.append("前三章变化信号中等（%d 次）" % c3)
    else:
        detail.append("前三章局面推进不足（%d 次）" % c3)
    return min(pts, 15), detail


def score_module_e(three):
    """E 核心机制兑现 15"""
    detail = []
    m = count_hits(three, MECH_WORDS)
    if m >= 6:
        pts = 13
        detail.append("核心机制词出现 %d 次，机制已运转 ✓" % m)
    elif m >= 3:
        pts = 9
        detail.append("核心机制词出现 %d 次，偏" % m)
    elif m >= 1:
        pts = 5
        detail.append("核心机制仅被提到（%d 次）→ 需一次实际运转" % m)
    else:
        pts = 2
        detail.append("前三章未见核心机制 → 读者无法说出「这本书主要看什么」")
    if re.search(r"(代价|限制|只能|必须|反噬|冷却|不能)", three):
        pts += 2
        detail.append("检出机制代价/限制表述 ✓")
    else:
        detail.append("未见机制代价 → 无代价金手指是 2026 同质化第一死因")
    return min(pts, 15), detail


def score_module_f(ch1):
    """F 信息控制 10"""
    detail = []
    pts = 10
    dense = dense_paragraphs(ch1, 150)
    if dense:
        cut = min(len(dense) * 2, 6)
        pts -= cut
        detail.append("第一章节级长段（>150 字）%d 处 → 前 300 字最忌大段说明" % len(dense))
        for d in dense[:3]:
            detail.append("    · %s" % d)
    exp = count_hits(ch1, EXPOSITION_MARKS)
    if exp >= 2:
        pts -= min(exp, 3)
        detail.append("铺陈性表述 %d 处（世界观说明书风险）" % exp)
    # 专有名词密度
    proper = len(set(re.findall(r"[\u4e00-\u9fa5]{2,4}(?=（|：)", ch1)))
    if proper >= 8:
        pts -= 2
        detail.append("疑似专有名词/角色名过多（%d 个）→ 概念密度超载" % proper)
    if not dense and exp == 0:
        detail.append("无明显大段说明，信息按需释放 ✓")
    return max(pts, 0), detail


def score_module_g(ch1, three):
    """G 节奏与章尾 10"""
    detail = []
    pts = 0
    paras = [p for p in re.split(r"\n+", ch1) if p.strip()]
    if paras:
        lens = [len(p) for p in paras]
        avg = sum(lens) / len(lens)
        spread = max(lens) - min(lens)
        if spread >= 60:
            pts += 4
            detail.append("段落长短错落（极差 %d 字）✓" % spread)
        else:
            pts += 2
            detail.append("段落长度偏均齐（极差 %d 字）→ 有模板化风险" % spread)
        if avg <= 120:
            pts += 1
            detail.append("平均段长 %.0f 字，手机阅读友好 ✓" % avg)
        else:
            detail.append("平均段长 %.0f 字偏长 → 建议拆段" % avg)

    tail = three[-260:] if len(three) > 260 else three
    found = [k for k, p in HOOK_PATTERNS.items() if p.search(tail)]
    if found:
        pts += 5
        detail.append("章尾钩子类型：%s ✓" % "、".join(found))
    else:
        pts += 0
        detail.append("章尾未见明确钩子 → 追读率会掉；请用四种安全写法之一")
    if re.search(r"(猛然回头|竟然是|竟然会是)", tail):
        detail.append("检测到「猛然回头/竟然是」同质化截断 → 换写法")
    return min(pts, 10), detail


def score_module_h(three):
    """H 语言与格式 5"""
    detail = []
    pts = 5
    total = len(three)
    if total == 0:
        return 0, ["稿件为空"]
    quotes = three.count("“") + three.count("」")
    dialogue_ratio = quotes * 2 / total if total else 0
    if 0.006 <= dialogue_ratio <= 0.03:
        detail.append("对话密度合理 ✓")
    elif dialogue_ratio < 0.006:
        pts -= 2
        detail.append("对话偏少 → 多用对话推进剧情")
    else:
        detail.append("对话偏多，注意叙事节奏")

    # 半角标点混用
    if re.search(r"[a-zA-Z0-9][,;:!?]\s|[,.](?=[\u4e00-\u9fa5])", three):
        pts -= 1
        detail.append("检测到中文正文中混用半角标点 → 统一为全角")

    dash = three.count("——")
    ell = three.count("……")
    per_k = max(total / 1000.0, 1)
    if dash / per_k > 6:
        pts -= 1
        detail.append("破折号密度偏高（%.1f/千字）→ 建议 ≤2/章" % (dash / per_k))
    if ell / per_k > 8:
        pts -= 1
        detail.append("省略号密度偏高（%.1f/千字）→ 建议 ≤3/章" % (ell / per_k))
    if pts == 5:
        detail.append("基础格式未见问题 ✓")
    return max(pts, 0), detail


def detect_low_retention(front, ch1, three):
    """十二类低留存开篇检测"""
    hits = []
    tests = [
        ("1 世界观说明书", lambda: count_hits(ch1, EXPOSITION_MARKS) >= 3
         or len(dense_paragraphs(ch1, 150)) >= 3,
         "把历史/制度/等级/地图移出第一章；只留人物当前决策必需信息"),
        ("2 天气镜头", lambda: bool(WEATHER_OPEN.match(front.strip())),
         "让环境直接妨碍或帮助人物完成任务，而不是从天空/街道远景推入"),
        ("3 梦醒开局", lambda: bool(DREAM_OPEN.search(front)),
         "从醒来后的异常、证据或必须处理的结果切入"),
        ("4 会议点名册", lambda: len(MEETING_MARKS.findall(front)) >= 2,
         "选一个有明确利益冲突的中心人物与中心议题"),
        ("5 被动主角", lambda: len(PASSIVE_MARKS.findall(front)) >= 2,
         "让主角提出方案、拒绝安排或承担风险"),
        ("6 苦难堆叠", lambda: len(SUFFER_MARKS.findall(ch1)) >= 4
         and not re.search(r"(反击|反手|还回去|一巴掌|把.{0,6}摔)", ch1),
         "缩短压迫段落，尽快展示选择与反制（受气→反击 ≤3 章）"),
        ("7 神秘欠账", lambda: len(MYSTERY_MARKS.findall(three)) >= 4
         and count_hits(three, CHANGE_WORDS) < 3,
         "一边提出新问题，一边回收旧问题；前三章至少给一次小兑现"),
        ("8 无代价金手指", lambda: bool(re.search(r"(系统|金手指|能力|外挂)", three))
         and not re.search(r"(代价|限制|只能|必须|反噬|冷却|不能)", three),
         "设置边界、误差、成本或选择冲突"),
        ("9 回忆抢戏", lambda: len(FLASHBACK_MARKS.findall(ch1)) >= 2,
         "先完成当前冲突，把过去拆成触发式信息"),
        ("10 伪冲突", lambda: len(re.findall(r"(吵|争执|生气|冷战)", ch1)) >= 3
         and not re.search(r"(决定|换来|失去|拿到|签了|走了)", ch1),
         "让争执决定资源、关系或下一步行动"),
        ("11 书名简介错配", lambda: False,
         "统一封面承诺与前三章实际内容（需人工比对书名简介）"),
        ("12 作者自我劝退", lambda: bool(APOLOGY_MARKS.search(three)),
         "删掉道歉，把作品价值直接呈现"),
    ]
    for name, fn, fix in tests:
        try:
            if fn():
                hits.append((name, fix))
        except Exception:
            continue
    return hits


def first_three_sentences(front):
    ss = sentences(front)
    return ss[:3]


def analyze(path, window=300):
    files, err = collect(path)
    if err:
        return {"error": err}
    text = "\n\n".join(read(f) for f in files)
    # 去标题行（章节标题会干扰"前三句"提取与开篇镜头检测）
    plain = re.sub(r"^[ \t　]*(?:第[零一二三四五六七八九十百\d]+章[^\n]*|#{1,3}[^\n]*)[ \t　]*$",
                   "", text, flags=re.M)
    body = re.sub(r"^\s*#{1,3}.*$", "", plain, flags=re.M).strip()
    if not body:
        return {"error": "稿件内容为空"}

    front = body[:window]
    chs = split_chapters(body)
    ch1 = chs[0] if chs else body
    three = "\n".join(chs[:3]) if chs else body

    modules = []
    a = score_module_a(front, body)
    b = score_module_b(front, ch1)
    c = score_module_c(front, three)
    d = score_module_d(ch1, three)
    e = score_module_e(three)
    f = score_module_f(ch1)
    g = score_module_g(ch1, three)
    h = score_module_h(three)
    for label, mx, (pts, det) in [
        ("A 类型与卖点清晰", 15, a), ("B 主角可跟随", 15, b),
        ("C 冲突与代价", 15, c), ("D 局面变化", 15, d),
        ("E 核心机制兑现", 15, e), ("F 信息控制", 10, f),
        ("G 节奏与章尾", 10, g), ("H 语言与格式", 5, h),
    ]:
        modules.append({"module": label, "score": pts, "max": mx, "detail": det})

    total = sum(m["score"] for m in modules)
    if total < 70:
        verdict, advice = "优先重构", "按结构轮重排事件顺序，提前核心冲突"
    elif total < 85:
        verdict, advice = "定向修订", "按失分模块定向修改，重点补最前端的洞"
    else:
        verdict, advice = "可交付", "进入交付流程，同步跑 tomato_audit.py 做文风体检"

    return {
        "files": files,
        "chars": len(body),
        "chapters_detected": len(chs),
        "front_window": window,
        "first_three_sentences": first_three_sentences(front),
        "total": total,
        "verdict": verdict,
        "advice": advice,
        "modules": modules,
        "low_retention": detect_low_retention(front, ch1, three),
    }


def print_report(rep):
    if "error" in rep:
        print("[X] %s" % rep["error"])
        return
    print("=" * 74)
    print("番茄殿堂作家 · 开篇留存预测")
    print("=" * 74)
    print("稿件：%s" % "、".join(os.path.basename(f) for f in rep["files"]))
    print("正文字数：%d 字｜识别章节：%d 章｜分析窗口：前 %d 字"
          % (rep["chars"], rep["chapters_detected"], rep["front_window"]))

    print("\n【前三句体检】（3 秒停留率关键）")
    for i, s in enumerate(rep["first_three_sentences"], 1):
        print("  %d. %s" % (i, s))
    if not rep["first_three_sentences"]:
        print("  （未检测到完整句子）")

    print("\n" + "-" * 74)
    print("【八模块评分】")
    print("-" * 74)
    for m in rep["modules"]:
        bar = "█" * int(m["score"] / m["max"] * 20)
        print("%-18s %2d/%2d  %s" % (m["module"], m["score"], m["max"], bar))
        for d in m["detail"]:
            print("    · %s" % d)
        print()

    print("-" * 74)
    print("【十二类低留存检测】")
    if rep["low_retention"]:
        for name, fix in rep["low_retention"]:
            print("  [!] 命中：%s" % name)
            print("      修复：%s" % fix)
    else:
        print("  未命中任何低留存问题 ✓（第 11 项需人工比对书名/简介）")

    print("\n" + "=" * 74)
    print("开篇总分：%d / 100  → 判定：%s" % (rep["total"], rep["verdict"]))
    print("处置：%s" % rep["advice"])
    print("判定线：<70 优先重构｜70-84 定向修订｜>=85 可交付")
    print("=" * 74)


def main():
    ap = argparse.ArgumentParser(description="番茄殿堂作家 · 开篇留存预测器")
    ap.add_argument("path", help="稿件文件或目录")
    ap.add_argument("--window", type=int, default=300, help="前窗字数（默认 300）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    rep = analyze(args.path, args.window)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print_report(rep)
    sys.exit(1 if "error" in rep else 0)


if __name__ == "__main__":
    main()
