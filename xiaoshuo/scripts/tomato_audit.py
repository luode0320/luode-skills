#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄殿堂作家 · 稿件殿堂体检脚本

用法：
    python tomato_audit.py <稿件文件或目录>            # 文本报告
    python tomato_audit.py <稿件文件或目录> --json     # JSON 输出
    python tomato_audit.py <稿件文件或目录> --strict   # 评分不达标时返回码 1

检测项：
    1. AI 腔高危句式逐句定位（对偶句/万能氛围句/模板微表情/程度副词链等）
    2. 计数一致性（"说了三个字：X X X" 类语义数目比对）
    3. 段落长度分布、句长分布、对话占比
    4. 章末钩子识别与强度分级
    5. 单章字数波动（过度整齐是 AI 特征）
    6. 综合 AI 味评分（0-100，越高越像手写）

零第三方依赖，仅标准库。
"""

import argparse
import json
import os
import re
import statistics
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------------------------------------------------------------------------
# 高危句式模式表：(正则, 名称, 单次扣分权重, 建议改法)
# ---------------------------------------------------------------------------
AI_PHRASE_PATTERNS = [
    (r"不是[^。！？\n]{1,20}而是", "对偶句式「不是…而是…」", 3.0, "拆成两句，或直接说后半句"),
    (r"不是[^，。！？\n]{1,24}，是", "对偶句式「不是…，是…」", 3.0, "删掉前半个否定"),
    (r"仿佛[^，。！？\n]{0,14}(?:一般|一样|似的)", "模糊限定「仿佛…一般」", 2.0, "换成确定的具体描写"),
    (r"(?:空气|气氛|时间)[^，。！？\n]{0,8}(?:凝固|凝滞|安静得可怕)", "万能氛围句", 3.0, "写具体反应：谁停了手、谁没抬头"),
    (r"眼中闪过(?:一丝|一抹|一道)", "模板化微表情", 3.0, "换成具体动作"),
    (r"嘴角(?:勾起|扬起|浮现)[^，。！？\n]{0,10}(?:弧度|笑意|冷笑)", "模板化微表情「嘴角弧度」", 3.0, "删或换成具体动作"),
    (r"深吸(?:了)?一口气", "模板化缓解动作", 1.5, "换其他身体反应，全书不超过 2 次"),
    (r"缓缓地?(?:睁开|闭上|说|走|转|抬|点)", "程度副词依赖「缓缓」", 1.5, "删掉副词"),
    (r"轻轻地?(?:说|放|叹|笑|摇头|点头)", "程度副词依赖「轻轻」", 1.0, "删掉副词"),
    (r"微微(?:一笑|一愣|点头|皱眉|摇头)", "程度副词依赖「微微」", 1.0, "删掉副词"),
    (r"淡淡(?:地)?(?:说|道|笑|开口)", "程度副词依赖「淡淡」", 1.0, "删掉副词"),
    (r"静静的?|静静地", "程度副词依赖「静静」", 1.0, "删掉副词"),
    (r"在这一刻|就在此时|与此同时|就在这时候", "廉价转场词", 2.0, "直接切场景或用动作衔接"),
    (r"这让他(?:想起|想到了)|脑海中(?:浮现|闪过)", "模型式联想", 2.0, "用物件/气味/声音触发"),
    (r"话音(?:落下|刚落)|此言一出|此话一出", "评书腔模板", 1.5, "直接接反应"),
    (r"无比(?:强大|震撼|愤怒|悲伤)|难以言喻|无法形容|说不出的", "抽象形容词堆砌", 2.0, "用具体场面代替"),
    (r"深深的?(?:震撼|愧疚|无力|疲惫|绝望)", "抽象情绪名词", 2.0, "用动作代替情绪说明"),
    (r"心中(?:涌起|泛起|升起)一股", "模板化情绪涌现", 2.0, "用动作或生理反应代替"),
    (r"眼神(?:变得|渐渐)?(?:复杂|深邃|幽深)", "模板化眼神描写", 1.5, "换成具体行为"),
    (r"(?:一切|所有)[^，。！？\n]{0,6}都(?:变得|显得)[^，。！？\n]{0,10}", "模板化总结句", 1.5, "删除或具体化"),
    (r"不禁(?:感慨|感叹|想到)", "模型式抒情", 1.5, "删除"),
    (r"他知道[^，。！？\n]{0,12}了", "信息直给句（高频）", 0.5, "控制频率，改用行动体现"),
    (r"（本章完）|（未完待续）", "章节尾注（多数平台不显示且显机械）", 1.0, "删除"),
]

# 章末钩子识别规则：(正则, 类型, 强度分)
HOOK_RULES = [
    (r"[？?]\s*$", "悬念未解（疑问收尾）", 3),
    (r"(危险|死了|来了|杀|血|枪|刀|塌|爆|崩|灭|逃|追|响|裂|倒)[^。！？\n]{0,12}[。！？!]\s*$",
     "危机降临", 3),
    (r"(究竟|到底|竟然|居然|原来|难道)", "悬念未解（未解词）", 3),
    (r"(不知道|还没有|还没|并未|无从)", "悬念未解（信息缺口）", 2),
    (r"(我要|我必|他要|必将|一定要|一定要)", "目标宣告", 2),
    (r"[……]{1,}[」』\"]?\s*$", "情绪余震（留白收尾）", 1),
]

CN_NUM = {
    "零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
}


def cn_to_int(s):
    """支持 一到二十、三十、一百 以内的中文数字（够用即可）。"""
    s = s.strip()
    if not s:
        return None
    if s.isdigit():
        return int(s)
    if s == "十":
        return 10
    if "十" in s:
        parts = s.split("十")
        head = CN_NUM.get(parts[0], 1) if parts[0] else 1
        tail = CN_NUM.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
        return head * 10 + tail
    total = 0
    for ch in s:
        if ch in CN_NUM:
            total = total * 10 + CN_NUM[ch] if total and ch != "零" else CN_NUM[ch]
    return total or None


def read_text(path):
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def collect_files(target):
    if os.path.isfile(target):
        return [target]
    files = []
    for root, _dirs, names in os.walk(target):
        for n in sorted(names):
            if n.lower().endswith((".md", ".txt")) and not n.startswith("."):
                files.append(os.path.join(root, n))
    return sorted(files)


def split_chapters(text):
    """按 '第X章' 切分；无章节标记时按 2400 字分块。"""
    pattern = re.compile(r"^[ \t]*#{0,4}[ \t]*第\s*[0-9一二三四五六七八九十百千零两]+\s*章[^\n]*$",
                         re.MULTILINE)
    marks = list(pattern.finditer(text))
    if len(marks) >= 2:
        chapters = []
        for i, m in enumerate(marks):
            start = m.end()
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            body = text[start:end].strip()
            chapters.append({"title": m.group(0).strip("# \t"), "body": body})
        return chapters, True
    # fallback：按 2400 字硬切
    body = re.sub(r"\s+", " ", text)
    size = 2400
    chunks = [body[i:i + size] for i in range(0, len(body), size)]
    return [{"title": "片段%d" % (i + 1), "body": c} for i, c in enumerate(chunks) if c.strip()], False


def analyze_hooks(chapters):
    results = []
    for ch in chapters:
        tail = ch["body"].strip()[-80:]
        hook_type, strength = "未识别", 0
        for pat, name, sc in HOOK_RULES:
            if re.search(pat, tail):
                hook_type, strength = name, sc
                break
        results.append({"chapter": ch["title"], "hook": hook_type, "strength": strength})
    return results


def analyze_counts(text):
    """计数一致性：'说了三个字：「XXX」' 类语义比对。"""
    issues = []
    pat = re.compile(r"([0-9一二三四五六七八九十两]{1,3})\s*个字\s*[：:，,]?\s*[「『\"“'‘]([^」』\"”'’]{1,30})[」』\"”'’]")
    for m in pat.finditer(text):
        declared = cn_to_int(m.group(1))
        # 按中文/英文字符计数，剔除标点与空白（"四个字：「不同意。」" 应为 3 字）
        actual = len(re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", m.group(2)))
        if declared is not None and actual != declared:
            line = text.count("\n", 0, m.start()) + 1
            issues.append({
                "line": line,
                "declared": declared,
                "actual": actual,
                "snippet": m.group(0)[:40],
            })
    return issues


def analyze_style(text):
    cn_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n|\n", text) if len(p.strip()) >= 2]
    paragraphs = [p for p in paragraphs if not p.startswith("#")]
    para_lens = [len(p) for p in paragraphs] or [1]

    sentences = [s for s in re.split(r"[。！？!?…]+", text) if len(s.strip()) >= 1]
    sent_lens = [len(s) for s in sentences] or [1]

    quote_chars = sum(len(q) for q in re.findall(r"[「『\"“][^」』\"”]{1,200}[」』\"”]", text))
    dialogue_ratio = round(quote_chars / max(cn_chars, 1), 3)

    # 连续破折号算一处：`——` 是中文破折号的规范写法，不能拆成两个半角计数。
    dash_count = len(re.findall(r"—+", text))
    ellipsis_count = len(re.findall(r"…{1,}|\.{3,}", text))
    adv_re = re.compile(r"缓缓|轻轻|微微|淡淡|静静|悄悄|慢慢")
    adv_count = len(adv_re.findall(text))

    def cv(vals):
        if len(vals) < 2:
            return 0.0
        mean = statistics.mean(vals) or 1
        return round(statistics.pstdev(vals) / mean, 3)

    return {
        "cn_chars": cn_chars,
        "paragraph_count": len(paragraphs),
        "avg_paragraph_len": round(statistics.mean(para_lens), 1),
        "max_paragraph_len": max(para_lens),
        "paragraph_cv": cv(para_lens),
        "sentence_count": len(sentences),
        "avg_sentence_len": round(statistics.mean(sent_lens), 1),
        "sentence_std": round(statistics.pstdev(sent_lens), 2) if len(sent_lens) > 1 else 0.0,
        "dialogue_ratio": dialogue_ratio,
        "dash_count": dash_count,
        "ellipsis_count": ellipsis_count,
        "degree_adverb_count": adv_count,
        "long_paragraph_ratio": round(
            sum(1 for p in para_lens if p > 200) / max(len(para_lens), 1), 3),
    }


def score_text(text, style, hits, chapters_info, hook_info, count_issues):
    """AI 味评分：100 = 完全像手写，0 = 高度机械。"""
    score = 100.0
    reasons = []
    per_k = max(style["cn_chars"] / 1000.0, 1.0)

    # 1. 高危句式密度
    hit_score = sum(h["weight"] for h in hits)
    density = hit_score / per_k
    deduct = min(36.0, density * 1.5)
    if deduct > 0.5:
        reasons.append("高危句式命中 %d 处（密度 %.2f/千字），扣 %.1f 分" % (len(hits), density, deduct))
    score -= deduct

    # 2. 程度副词密度
    adv_density = style["degree_adverb_count"] / per_k
    if adv_density > 2.0:
        d = min(8.0, (adv_density - 2.0) * 1.6)
        reasons.append("程度副词密度 %.1f/千字偏高，扣 %.1f 分" % (adv_density, d))
        score -= d

    # 3. 破折号 / 省略号
    if style["dash_count"] > 2 * per_k:
        d = min(5.0, (style["dash_count"] - 2 * per_k) * 0.8)
        reasons.append("破折号 %.1f 处/千字偏多，扣 %.1f 分" % (style["dash_count"] / per_k, d))
        score -= d
    if style["ellipsis_count"] > 3 * per_k:
        d = min(5.0, (style["ellipsis_count"] - 3 * per_k) * 0.5)
        reasons.append("省略号 %.1f 处/千字偏多，扣 %.1f 分" % (style["ellipsis_count"] / per_k, d))
        score -= d

    # 4. 段落均匀度（过于整齐 = 机械）
    if style["paragraph_cv"] and style["paragraph_cv"] < 0.25:
        reasons.append("段落长度过于整齐（CV=%.2f），扣 7 分" % style["paragraph_cv"])
        score -= 7.0

    # 5. 句长过于整齐
    if style["sentence_std"] and style["sentence_std"] < 6:
        reasons.append("句长分布过于集中（标准差=%.1f），扣 7 分" % style["sentence_std"])
        score -= 7.0

    # 6. 对话占比
    dr = style["dialogue_ratio"]
    if dr < 0.20:
        reasons.append("对话占比 %.0f%% 偏低（建议 30%%~45%%）" % (dr * 100))
        score -= 5.0
    elif dr > 0.55:
        reasons.append("对话占比 %.0f%% 偏高，叙事推进不足" % (dr * 100))
        score -= 3.0

    # 7. 超长段落
    if style["long_paragraph_ratio"] > 0.06:
        reasons.append("超长段落（>200 字）占比 %.0f%%，手机端阅读不友好" % (style["long_paragraph_ratio"] * 100))
        score -= 4.0

    # 8. 计数一致性
    if count_issues:
        d = min(8.0, len(count_issues) * 4.0)
        reasons.append("计数一致性疑点 %d 处，扣 %.1f 分（AI 最典型破绽）" % (len(count_issues), d))
        score -= d

    # 9. 单章字数过度整齐
    if chapters_info["split_by_marker"] and len(chapters_info["chapter_words"]) >= 4:
        lens = chapters_info["chapter_words"]
        mean = statistics.mean(lens) or 1
        c = statistics.pstdev(lens) / mean
        if c < 0.08:
            reasons.append("单章字数过度整齐（CV=%.3f），扣 6 分" % c)
            score -= 6.0

    # 10. 钩子强度
    if hook_info:
        weak = [h for h in hook_info if h["strength"] <= 1]
        if weak and len(weak) / len(hook_info) > 0.5:
            reasons.append("章末钩子偏弱（%d/%d 章为弱钩子）" % (len(weak), len(hook_info)))
            score -= 4.0

    score = max(0.0, min(100.0, score))
    return round(score, 1), reasons


def grade(score):
    if score >= 90:
        return "殿堂级（可交付）"
    if score >= 80:
        return "准殿堂（定向迭代一次）"
    if score >= 68:
        return "合格（建议按清单改写）"
    return "不合格（回炉重写）"


def build_report(target):
    files = collect_files(target)
    if not files:
        return {"error": "未找到可检测的 .md / .txt 文件：%s" % target}

    all_text_parts = []
    file_reports = []
    total_issues = []

    for fp in files:
        text = read_text(fp)
        if not text.strip():
            continue
        all_text_parts.append(text)
        hits = []
        for pat, name, weight, fix in AI_PHRASE_PATTERNS:
            for m in re.finditer(pat, text):
                hits.append({
                    "name": name,
                    "line": text.count("\n", 0, m.start()) + 1,
                    "snippet": m.group(0)[:30],
                    "fix": fix,
                    "weight": weight,
                })
        issues = analyze_counts(text)
        for it in issues:
            it["file"] = os.path.basename(fp)
        total_issues.extend(issues)
        style = analyze_style(text)
        chapters, by_marker = split_chapters(text)
        chapter_words = [len(re.findall(r"[\u4e00-\u9fff]", c["body"])) for c in chapters]
        hooks = analyze_hooks(chapters)
        sc, reasons = score_text(
            text, style,
            hits,
            {"split_by_marker": by_marker, "chapter_words": chapter_words},
            hooks, issues,
        )
        file_reports.append({
            "file": os.path.basename(fp),
            "path": fp,
            "score": sc,
            "grade": grade(sc),
            "style": style,
            "phrase_hit_count": len(hits),
            "phrase_hits": sorted(hits, key=lambda x: -x["weight"])[:40],
            "count_mismatches": issues,
            "chapter_count": len(chapters),
            "chapter_words": chapter_words,
            "chapter_word_avg": round(statistics.mean(chapter_words), 1) if chapter_words else 0,
            "hooks": hooks,
            "reasons": reasons,
        })

    if not file_reports:
        return {"error": "文件为空，无内容可检测：%s" % target}

    total_cn = sum(f["style"]["cn_chars"] for f in file_reports)
    overall = round(
        sum(f["score"] * f["style"]["cn_chars"] for f in file_reports) / max(total_cn, 1), 1)

    agg_hits = {}
    for f in file_reports:
        for h in f["phrase_hits"]:
            agg_hits[h["name"]] = agg_hits.get(h["name"], 0) + 1

    return {
        "target": target,
        "file_count": len(file_reports),
        "total_cn_chars": total_cn,
        "overall_score": overall,
        "overall_grade": grade(overall),
        "top_phrase_issues": sorted(agg_hits.items(), key=lambda x: -x[1])[:12],
        "total_count_mismatches": len(total_issues),
        "files": file_reports,
        "knowledge_cutoff": "2026-09-11",
    }


def print_report(rep):
    if "error" in rep:
        print("[X] %s" % rep["error"])
        return
    print("=" * 68)
    print("番茄殿堂作家 · 稿件殿堂体检报告")
    print("=" * 68)
    print("检测目标：%s" % rep["target"])
    print("文件数：%d    中文字数：%d" % (rep["file_count"], rep["total_cn_chars"]))
    print("综合 AI 味评分：%s / 100   [%s]" % (rep["overall_score"], rep["overall_grade"]))
    print("-" * 68)

    for f in rep["files"]:
        s = f["style"]
        print("\n【%s】评分 %s [%s]" % (f["file"], f["score"], f["grade"]))
        print("  章节数：%d    单章均字数：%s   对话占比：%.0f%%"
              % (f["chapter_count"], f["chapter_word_avg"], s["dialogue_ratio"] * 100))
        print("  平均句长：%s 字   句长标准差：%s   平均段长：%s 字（最长 %d）"
              % (s["avg_sentence_len"], s["sentence_std"], s["avg_paragraph_len"],
                 s["max_paragraph_len"]))
        print("  高危句式：%d 处   计数疑点：%d 处"
              % (f["phrase_hit_count"], len(f["count_mismatches"])))

        if f["reasons"]:
            print("  扣分项：")
            for r in f["reasons"]:
                print("    - %s" % r)

        if f["phrase_hits"]:
            print("  ▼ 逐句替换清单（按严重度排序，前 12 条）：")
            for h in f["phrase_hits"][:12]:
                print("    第 %d 行 | %s | 命中「%s」" % (h["line"], h["name"], h["snippet"]))
                print("            → 改法：%s" % h["fix"])

        if f["count_mismatches"]:
            print("  ▼ 计数一致性疑点（AI 最典型破绽）：")
            for it in f["count_mismatches"][:8]:
                print("    第 %d 行 | 声明 %d 字，实际 %d 字 | %s"
                      % (it["line"], it["declared"], it["actual"], it["snippet"]))

        weak = [h for h in f["hooks"] if h["strength"] <= 1]
        if weak:
            print("  ▼ 弱钩子章节：%s" % "、".join(h["chapter"] for h in weak[:8]))

    if rep["top_phrase_issues"]:
        print("\n" + "-" * 68)
        print("全局高频问题 TOP：")
        for name, cnt in rep["top_phrase_issues"]:
            print("  %-32s %d 处" % (name, cnt))

    print("\n" + "=" * 68)
    print("改法优先级：① 对偶句与万能氛围句（扣分最重）② 计数一致性 ③ 段落与句长节奏 ④ 程度副词")
    print("改写完成后请复跑本脚本，评分 ≥90 方可交付。")
    print("知识截止：%s（平台规则超 30 天建议联网复核）" % rep["knowledge_cutoff"])


def main():
    ap = argparse.ArgumentParser(description="番茄殿堂作家 · 稿件殿堂体检")
    ap.add_argument("target", help="稿件文件或目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--out", help="将报告写入指定文件")
    ap.add_argument("--strict", action="store_true", help="评分低于 90 时返回码 1")
    args = ap.parse_args()

    if not os.path.exists(args.target):
        print("[X] 路径不存在：%s" % args.target)
        sys.exit(2)

    rep = build_report(args.target)

    if args.json:
        out = json.dumps(rep, ensure_ascii=False, indent=2)
        print(out)
    else:
        print_report(rep)
        out = None

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(json.dumps(rep, ensure_ascii=False, indent=2))
        print("\n[OK] 报告已写入：%s" % args.out)

    if args.strict and "overall_score" in rep and rep["overall_score"] < 90:
        sys.exit(1)
    if "error" in rep:
        sys.exit(2)


if __name__ == "__main__":
    main()
