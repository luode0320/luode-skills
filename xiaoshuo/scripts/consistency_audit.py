#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""百万字小说一致性校验器（确定性、纯 stdlib、可复跑）。

扫描 manuscript 与 bible，抓 11 类问题：
  C1 名字一致性  C2 时间线冲突  C3 在场性漂移  C4 设定违反  C5 伏笔未回收
  C6 仙侠境界倒退  C7 物证状态链  C8 关系称谓冲突  C9 线索/证据状态链  C10 游戏系统面板一致性
  C11 首版 AI 味探测（机械套路，供二遍改写参考，非逻辑错误）

用法:
  python consistency_audit.py --bible <bible_dir> --ms <manuscript_dir> [--json report.json]

退出码: 0=运行成功(无论有无发现)  2=用法错误
报告含 ERROR/WARN 计数；每条附章节定位、证据、误报提示。
"""
import argparse
import json
import os
import re
import sys
from difflib import SequenceMatcher

CJK = re.compile(r"[\u4e00-\u9fff]")
DATE_PAT = re.compile(r"(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?|纪元\s*\d+\s*年|开篇后第\s*\d+\s*天|[\u4e00-\u9fff]{1,3}[元一二三四五六七八九十百零\d]+年)")
# 日期前的动词/介词噪声（生于/卒于/到了/在…），提取后剥离，避免被当年号一部分
DATE_NOISE = set("生于出死卒坐陨降诞结娶嫁登继退于在自至到距从向对为了对了着把被及与和")
NAME_TOKEN = re.compile(r"[\u4e00-\u9fff]{2,4}")


def _norm_date(s):
    s = s.strip()
    while s and s[0] in DATE_NOISE:
        s = s[1:]
    return s


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def list_ms(ms_dir):
    out = []
    for root, _, files in os.walk(ms_dir):
        for fn in files:
            if fn.lower().endswith((".md", ".txt")):
                out.append(os.path.join(root, fn))
    return sorted(out)


# ---------- bible 解析 ----------
def parse_characters(bible_dir):
    chars = {}
    cdir = os.path.join(bible_dir, "characters")
    if not os.path.isdir(cdir):
        return chars
    for fn in sorted(os.listdir(cdir)):
        if not fn.lower().endswith((".md",)):
            continue
        t = read_text(os.path.join(cdir, fn))
        m = re.search(r"^#\s*人物[:：]\s*(.+)$", t, re.M)
        if not m:
            continue
        name = m.group(1).strip()
        aliases = []
        for am in re.finditer(r"别名/曾用名[:：]\s*(.+)", t):
            val = am.group(1).strip()
            if val and val != "无":
                aliases.append(val)
        status = ""
        sm = re.search(r"当前状态[:：]\s*(.+)", t)
        if sm:
            status = sm.group(1).strip()
        realm = ""
        rm = re.search(r"当前境界[:：]\s*(.+)", t)
        if rm:
            realm = rm.group(1).strip()
        chars[name] = {"aliases": aliases, "status": status, "realm": realm, "file": fn}
    return chars


def parse_rules(bible_dir):
    wb = read_text(os.path.join(bible_dir, "world-bible.md"))
    rules = []
    for m in re.finditer(r"规则\s*(R\d+)[:：]\s*(.+)", wb):
        rules.append((m.group(1), m.group(2).strip()))
    return rules


def parse_timeline(bible_dir):
    tl = read_text(os.path.join(bible_dir, "timeline.md"))
    events = []
    for m in re.finditer(r"(T\d+)[:：]\s*(.+?)\s*—\s*事件[:：]\s*(.+)", tl):
        events.append({"id": m.group(1), "time": m.group(2).strip(), "event": m.group(3).strip()})
    return events


def parse_plotboard(bible_dir):
    pb = read_text(os.path.join(bible_dir, "plot-board.md"))
    fores = []
    for m in re.finditer(r"(F\d+)[:：]\s*(.+?)\s*—\s*埋于[:：]第(\d+)卷\s*—\s*状态[:：](待回收|已回收)", pb):
        fores.append({"id": m.group(1), "desc": m.group(2).strip(), "buried": int(m.group(3)), "status": m.group(4)})
    return fores


def parse_cultivation(bible_dir):
    """仙侠：解析 world-bible 中的境界序列（如 炼气<筑基<金丹<元婴<化神）。"""
    wb = read_text(os.path.join(bible_dir, "world-bible.md"))
    m = re.search(r"境界序列[:：]\s*([^\n]+)", wb)
    if not m:
        return []
    seq = [x.strip() for x in re.split(r"[<〈＜]", m.group(1)) if x.strip()]
    return seq


REALM_REGRESS = re.compile(r"(跌落至|跌回|被打落|退至|掉落至|散落到|跌为|沦为|跌落回)\s*([\u4e00-\u9fff]{2,4})")
REALM_EXEMPT = re.compile(r"(散功|废去修为|自废|兵解|重修|封印修为|境界被废)")


def c6_realm_regress(chars, realm_seq, ms_texts):
    """C6 仙侠境界倒退：角色当前境界 > 正文出现『倒退至 X』且 X 在序列中更靠前。

    豁免：同上下文含散功/自废/兵解/重修等明确设定（属正常情节）。
    """
    findings = []
    if not realm_seq:
        return findings
    order = {r: i for i, r in enumerate(realm_seq)}
    for name, info in chars.items():
        cur = info.get("realm", "")
        if not cur or cur not in order:
            continue
        for path, text in ms_texts:
            for m in re.finditer(re.escape(name), text):
                window = text[m.start(): m.start() + 40]
                rm = REALM_REGRESS.search(window)
                if not rm:
                    continue
                target = rm.group(2)
                if target in order and order[target] < order[cur]:
                    ctx = text[max(0, m.start() - 12): m.start() + 50]
                    if REALM_EXEMPT.search(ctx):
                        continue
                    findings.append({
                        "rule": "C6", "level": "ERROR", "file": os.path.basename(path),
                        "msg": "境界倒退矛盾：『%s』当前境界『%s』，正文出现『%s』" % (name, cur, target),
                        "hint": "若属散功/自废/兵解/重修等明确设定，请确认该段已写明",
                    })
                    break
    return findings


# ---------- 科幻 / 悬疑：物证状态链 ----------
ARTIFACT_BAD = ("损毁", "毁坏", "报废", "遗失", "丢失", "湮灭", "摧毁", "熔毁")
ARTIFACT_GOOD = re.compile(r"(恢复|重启|重新启动|重新运转|完好无损|完好|无损|再次运转|重新激活|修好|正常运作|再度亮起|重新亮起)")
ARTIFACT_EXEMPT = re.compile(r"(修复|重铸|复制|克隆|替换|重建|复原|再造|重生|备份|再造体|替身)")


def parse_artifacts(bible_dir):
    """科幻/悬疑：解析 world-bible 中的关键物品/设备终态。

    格式：- 物品：曲速核心 | 终态：已损毁 | 损毁于：星历3015年
    """
    wb = read_text(os.path.join(bible_dir, "world-bible.md"))
    arts = []
    for m in re.finditer(r"物品[:：]\s*([^|\n]+?)\s*\|\s*终态[:：]\s*([^|\n]+)", wb):
        arts.append({"name": m.group(1).strip(), "state": m.group(2).strip()})
    return arts


def c7_artifact_state(artifacts, ms_texts):
    """C7 物证状态链：bible 记『物品X终态=损毁/遗失』，正文却出现 X 恢复/运转且无修复豁免 → WARN。

    误报边界：损毁前章节（如『事故前它正常运转』）属正常，需作者确认时点；故定 WARN 级，
    不报 ERROR；上下文含修复/重铸/克隆替换豁免词则不报。
    """
    findings = []
    for a in artifacts:
        state = a["state"]
        if not any(w in state for w in ARTIFACT_BAD):
            continue
        name = a["name"]
        if len(name) < 2:
            continue
        for path, text in ms_texts:
            idx = text.find(name)
            while idx != -1:
                window = text[idx: idx + 40]
                pre = text[max(0, idx - 15): idx + 40]
                if ARTIFACT_GOOD.search(window) and not ARTIFACT_EXEMPT.search(pre):
                    findings.append({
                        "rule": "C7", "level": "WARN", "file": os.path.basename(path),
                        "msg": "物证状态疑似矛盾：『%s』bible 终态『%s』，正文出现其恢复/运转" % (name, state),
                        "hint": "请确认该段时点是否在损毁之前，或是否已写明修复/重铸/克隆替换",
                    })
                    break
                idx = text.find(name, idx + 1)
    return findings


# ---------- 悬疑 / 推理：线索(证据)状态链 ----------
CLUE_BAD = ("销毁", "损毁", "遗失", "丢失", "灭失", "焚毁", "湮灭", "粉碎", " confiscat", "没收", "封存入库", "封存")
CLUE_GOOD = re.compile(r"(重现|再次出现|重新出现|再度出现|被找到|被发现|被检验|被化验|被出示|被提交|浮出水面|再度现世|重见天日)")
CLUE_EXEMPT = re.compile(r"(伪造|调包|复制|仿制|新发现|另寻|重新取得|调査|调查|新线索|新证据|备份|复印件|影印件)")


def parse_clues(bible_dir):
    """悬疑/推理：解析 world-bible 中的线索/证据终态。

    格式：- 线索：带血手帕 | 终态：已销毁 | 销毁于：案发现场焚化炉
    支持『线索/证物/证据』三种行首写法。
    """
    wb = read_text(os.path.join(bible_dir, "world-bible.md"))
    clues = []
    for m in re.finditer(r"(线索|证物|证据)[:：]\s*([^|\n]+?)\s*\|\s*终态[:：]\s*([^|\n]+)", wb):
        clues.append({"name": m.group(2).strip(), "state": m.group(3).strip()})
    return clues


def c9_clue_state(clues, ms_texts):
    """C9 线索/证据状态链：bible 记『线索X终态=销毁/遗失』，正文却出现 X 重现/被检验且无伪造豁免 → WARN。

    误报边界：线索在更早章节已出现属正常，故定 WARN 级不报 ERROR；
    上下文含伪造/调包/新发现豁免词（说明是另一份或新证据）则不报。未登记线索则自动跳过。
    """
    findings = []
    for c in clues:
        state = c["state"]
        if not any(w in state for w in CLUE_BAD):
            continue
        name = c["name"]
        if len(name) < 2:
            continue
        for path, text in ms_texts:
            idx = text.find(name)
            while idx != -1:
                window = text[idx: idx + 40]
                pre = text[max(0, idx - 15): idx + 40]
                if CLUE_GOOD.search(window) and not CLUE_EXEMPT.search(pre):
                    findings.append({
                        "rule": "C9", "level": "WARN", "file": os.path.basename(path),
                        "msg": "线索状态疑似矛盾：『%s』bible 终态『%s』，正文出现其重现/被检验" % (name, state),
                        "hint": "请确认该段时点是否在销毁之前，或是否已写明伪造/调包/新发现",
                    })
                    break
                idx = text.find(name, idx + 1)
    return findings


# ---------- 游戏异界 / 系统向：系统面板一致性 ----------

def parse_system(bible_dir):
    """游戏异界：解析 world-bible 中的系统面板（角色等级/已学技能）。

    格式：- 角色：沈砚 | 等级：Lv.5 | 属性：力量50/敏捷30 | 已学技能：火球术, 治愈术
    等级解析容错：Lv.5 / 等级5 / 5级 均识别；中文数字（五）无法解析则 level=None 跳过该项。
    """
    wb = read_text(os.path.join(bible_dir, "world-bible.md"))
    panels = []
    for m in re.finditer(r"-\s*角色[:：]\s*([^\n|]+?)\s*\|\s*等级[:：]\s*([^|\n]+)", wb):
        name = m.group(1).strip()
        lvl_txt = re.sub(r"[^0-9]", "", m.group(2).strip())
        level = int(lvl_txt) if lvl_txt else None
        skills = set()
        ms = re.search(r"已学技能[:：]\s*([^\n|]+)", wb[m.end():m.end() + 200])
        if ms:
            for s in re.split(r"[、,，\s]+", ms.group(1)):
                s = s.strip().strip("。")
                if s:
                    skills.add(s)
        panels.append({"name": name, "level": level, "skills": skills})
    return panels


SYS_REGRESS = re.compile(r"(跌落|跌回|退至|降级至|掉到|降为|回落|退回到|贬至|掉回)")
SYS_EXEMPT = re.compile(r"(自废|封印|重置|重生|转生|试炼|历练|降级历练|刻意压低|伪装|轮回)")
SYS_LVL = r"(?:(?:Lv\.?|等级)\s*(\d+)\s*级?|(\d+)\s*级)"
SYS_SKILL_VERB = r"(施展|释放|使用|施放|发动|催动)"
SYS_SKILL_LIKE = re.compile(r"[术法技咒击斩波焰冰雷箭刃掌拳]$")
SYS_SKILL_GENERIC = {"魔法", "法术", "灵术", "仙术", "道术", "武技", "剑技", "刀法", "剑法", "拳法", "掌法"}


def c10_system_state(panels, ms_texts):
    """C10 游戏系统面板一致性：

    - 等级倒退 (ERROR)：bible 记 角色X 等级=N，正文却出现 X 等级跌落/退至/掉回 M 且 M<N。
    - 未学技能使用 (WARN)：bible 记 X 已学技能=[...]，正文却「X 施展/释放 <技能>」且该技能不在列表（且像技能名）。
    豁免：自废/封印/重置/重生/转生/试炼 等明确设定；无等级/无技能列表则跳过该项。
    精确等级正则避免「第3层」「50米」等误报（必须 Lv./等级/级 上下文）。
    注意：SYS_REGRESS / SYS_SKILL_VERB 嵌入后成为捕获组，故等级数字取 mm.group(2)或(3)、技能名取 mm.group(2)。
    """
    findings = []
    for p in panels:
        name = p["name"]
        if len(name) < 2:
            continue
        # 等级倒退 (ERROR)
        if p["level"] is not None:
            for path, text in ms_texts:
                hit = None
                for mm in re.finditer(r"%s[^。]{0,20}?%s[^。]{0,12}?%s" % (re.escape(name), SYS_REGRESS.pattern, SYS_LVL), text):
                    window = text[max(0, mm.start() - 5): mm.end() + 5]
                    if SYS_EXEMPT.search(window):
                        continue
                    m = mm.group(2) or mm.group(3)
                    try:
                        m = int(m)
                    except (ValueError, TypeError):
                        continue
                    if m < p["level"]:
                        hit = mm
                        break
                if hit:
                    findings.append({
                        "rule": "C10", "level": "ERROR", "file": os.path.basename(path),
                        "msg": "系统面板等级倒退矛盾：『%s』面板等级 Lv.%d，正文出现『%s』" % (name, p["level"], hit.group(0)[len(name):].strip()[:24]),
                        "hint": "若属自废/封印/重生/试炼等明确设定，请确认该段已写明豁免词",
                    })
        # 未学技能使用 (WARN)
        if p["skills"]:
            for path, text in ms_texts:
                hit = None
                for mm in re.finditer(r"%s[^。]{0,15}?%s[了着过出]?\s*([\u4e00-\u9fff]{2,4})" % (re.escape(name), SYS_SKILL_VERB), text):
                    token = mm.group(2)
                    if token in p["skills"] or token in SYS_SKILL_GENERIC:
                        continue
                    if SYS_SKILL_LIKE.search(token):
                        hit = token
                        break
                if hit:
                    findings.append({
                        "rule": "C10", "level": "WARN", "file": os.path.basename(path),
                        "msg": "系统面板技能矛盾：『%s』已学技能无『%s』，正文却施展该技能" % (name, hit),
                        "hint": "请确认是否漏登记技能，或该段为回忆/误写",
                    })
    return findings


# ---------- 言情 / 关系向：关系称谓冲突 ----------
REL_PAT = re.compile(r"-\s*([\u4e00-\u9fff]{2,4})\s*[—\-~]\s*([\u4e00-\u9fff]{2,4})\s*[:：]\s*([^\n]+)")
SPOUSE_W = ("妻子", "老公", "丈夫", "太太", "夫人", "媳妇", "夫君", "爱妻", "爱人", "伴侣")
EX_W = ("前妻", "前夫", "前男友", "前女友", "旧爱", "ex", "前恋人")
LOVER_W = ("恋人", "男友", "女友", "心上人", "在一起")
KIN_W = ("父亲", "母亲", "儿子", "女儿", "哥哥", "弟弟", "姐姐", "妹妹", "父子", "母女", "兄弟", "姐妹")
REL_EXEMPT = re.compile(r"(回忆|想起|当年|曾经|听说|传闻|梦见|以为|仿佛|恍惚|旧日|往昔|故事里)")


def classify_rel(label):
    """将关系标签归为冲突类别集合。"""
    cats = set()
    s = label
    if any(w in s for w in ("前", "旧", "ex", "已分手", "分手后")):
        cats.add("ex")
    if any(w in s for w in ("妻", "夫", "配偶", "老公", "太太", "夫人", "媳妇", "夫君", "爱妻", "爱人", "伴侣")):
        cats.add("spouse")
    if any(w in s for w in ("恋", "男友", "女友", "心上人", "在一起")):
        cats.add("lover")
    if any(w in s for w in ("父", "母", "子", "女", "兄", "弟", "姐", "妹", "亲属", "亲戚")):
        cats.add("kin")
    if any(w in s for w in ("陌生", "素不相识", "毫无关系", "不相识")):
        cats.add("stranger")
    return cats


def parse_relations(bible_dir):
    """解析 world-bible.md 的『人物关系网』节，格式：
    - 林月 — 顾言：前任（已分手）
    - 林月 — 苏白：现任恋人
    """
    wb = read_text(os.path.join(bible_dir, "world-bible.md"))
    rels = []
    for m in REL_PAT.finditer(wb):
        rels.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
    return rels


CONFLICT = {
    "ex": {"spouse"},
    "spouse": {"ex"},
    "stranger": {"spouse", "lover", "kin"},
}


def c8_relation_conflict(rels, ms_texts):
    """C8 关系称谓冲突：bible 标注两人关系（如前任/陌生人），正文却以互斥称谓（如妻子/恋人/亲属）指称 → WARN。

    误报边界：纯文本无时点，回忆/倒叙/传闻中提及旧称谓属正常，故定 WARN 级；
    上下文含回忆豁免词（回忆/想起/当年/听说…）则不报。每个 (pair,file) 至多报一次。
    """
    findings = []
    pairs = {}
    for a, b, label in rels:
        cats = classify_rel(label)
        if not cats:
            continue
        key = frozenset({a, b})
        pairs.setdefault(key, set()).update(cats)

    for key, cats in pairs.items():
        conflict_cats = set()
        for c in cats:
            conflict_cats |= CONFLICT.get(c, set())
        if not conflict_cats:
            continue
        detect = []
        if "spouse" in conflict_cats:
            detect += SPOUSE_W
        if "ex" in conflict_cats:
            detect += EX_W
        if "lover" in conflict_cats:
            detect += LOVER_W
        if "kin" in conflict_cats:
            detect += KIN_W
        if not detect:
            continue
        members = list(key)
        for path, text in ms_texts:
            if not all(m in text for m in members):
                continue
            reported = False
            for w in detect:
                if reported:
                    break
                idx = text.find(w)
                while idx != -1:
                    window = text[max(0, idx - 22): idx + 22]
                    if all(m in window for m in members):
                        if REL_EXEMPT.search(window):
                            idx = text.find(w, idx + 1)
                            continue
                        findings.append({
                            "rule": "C8", "level": "WARN", "file": os.path.basename(path),
                            "msg": "关系称谓疑似冲突：bible 标注『%s』关系，正文却以『%s』称谓指称两人" % ("/".join(sorted(cats)), w),
                            "hint": "请确认该段是否回忆/倒叙/传闻；若确为时间线矛盾请修正 bible 或正文",
                        })
                        reported = True
                        break
                    idx = text.find(w, idx + 1)
    return findings


# ---------- 规则实现 ----------
def c1_name_variants(chars, ms_texts):
    findings = []
    canonical = set(chars.keys())
    alias_set = set()
    for c in chars.values():
        alias_set.update(c["aliases"])
    for path, text in ms_texts:
        for tok in NAME_TOKEN.findall(text):
            if tok in canonical or tok in alias_set:
                continue
            # 跳过「规范名+后续字」的误切分（如 玄霄子将 = 玄霄子+将）
            if any(tok.startswith(n) for n in canonical) or any(tok.startswith(a) for a in alias_set):
                continue
            if len(tok) < 2:
                continue
            for name in canonical:
                ratio = SequenceMatcher(None, tok, name).ratio()
                # 中文单字替换（如 张三→张二）difflib 仅 0.5，单列编辑距离=1 高置信
                one_char_diff = (len(tok) == len(name) and len(tok) >= 2
                                 and sum(1 for a, b in zip(tok, name) if a != b) == 1)
                if (ratio >= 0.75 or one_char_diff) and tok != name:
                    findings.append({
                        "rule": "C1", "level": "WARN", "file": os.path.basename(path),
                        "msg": "疑似名字变体：规范『%s』/ 疑似『%s』(相似度%.2f)" % (name, tok, ratio),
                        "hint": "若为昵称/代号，请加入人物卡别名白名单",
                    })
                    break
    return findings


LIFECYCLE = re.compile(r"(降生|出生|生于|诞生|呱呱坠地|去世|死亡|卒于|坐化|陨落|入门|拜师|出师|结婚|成婚|出嫁|登基|继位|退位)")
NAME_TOKEN2 = re.compile(r"[\u4e00-\u9fff]{2,4}")


def _entity_before(text, pos):
    """谓语 pos 之前最近的一个名字 token（跳过谓语首字，如 出/生/死）。"""
    prefix = text[:pos]
    cands = list(NAME_TOKEN2.finditer(prefix))
    return cands[-1].group(0) if cands else None


def c2_timeline(timeline_events, ms_texts):
    findings = []
    for ev in timeline_events:
        lm = LIFECYCLE.search(ev["event"])
        if not lm:
            continue
        entity = _entity_before(ev["event"], lm.start())
        if not entity:
            continue
        bible_dates = set(_norm_date(x) for x in DATE_PAT.findall(ev["time"])) | \
                      set(_norm_date(x) for x in DATE_PAT.findall(ev["event"]))
        if not bible_dates:
            continue
        for path, text in ms_texts:
            for m in LIFECYCLE.finditer(text):
                em = _entity_before(text, m.start())
                if not em or em != entity:
                    continue
                window = text[m.start(): m.start() + 30]
                conflict = None
                for dm in DATE_PAT.finditer(window):
                    d = _norm_date(dm.group(0))
                    if d not in bible_dates:
                        conflict = d
                        break
                if conflict:
                    findings.append({
                        "rule": "C2", "level": "WARN", "file": os.path.basename(path),
                        "msg": "时间线冲突：实体『%s』bible 时点『%s』，正文断言出现『%s』" % (entity, " / ".join(bible_dates), conflict),
                        "hint": "倒叙/多视角时间差属正常误报，请人工确认",
                    })
                    break
    return findings


def c3_presence(chars, ms_texts):
    findings = []
    for name, info in chars.items():
        st = info["status"]
        dead = ("已故" in st) or ("失踪" in st) or ("流放" in st)
        if not dead:
            continue
        for path, text in ms_texts:
            if name in text:
                findings.append({
                    "rule": "C3", "level": "ERROR", "file": os.path.basename(path),
                    "msg": "在场性漂移：『%s』状态『%s』却在正文出场" % (name, st),
                    "hint": "若为回忆/幻觉/明确复活设定段落，请排除",
                })
                break
    return findings


def c4_rules(rules, ms_texts):
    findings = []
    for rid, rule in rules:
        if len(rule) < 6 or not CJK.search(rule):
            findings.append({
                "rule": "C4", "level": "WARN", "file": "(bible)",
                "msg": "规则 %s 表述偏模糊，难以机判：『%s』" % (rid, rule),
                "hint": "建议改写为『主体+条件+结果』可判定形式",
            })
            continue
        # 轻量矛盾扫描：规则含禁止词时，检查正文是否出现「禁止动作+肯定态」
        forbid = re.search(r"(禁止|不得|不能|不可|严禁)(.+)", rule)
        if forbid:
            # 取「禁止」后、到首个标点/否则 之前的动作短语，避免截到「否则…」尾巴
            action_full = re.split(r"[，。；、否则]", forbid.group(2).strip())[0]
            action_core = action_full[-4:] if len(action_full) >= 4 else action_full
            if len(action_core) >= 2:
                for path, text in ms_texts:
                    if action_full in text or action_core in text:
                        findings.append({
                            "rule": "C4", "level": "ERROR", "file": os.path.basename(path),
                            "msg": "疑似设定违反 %s：正文出现被禁动作『%s』" % (rid, action_core),
                            "hint": "需作者确认是否真违反或属例外设定",
                        })
                        break
    return findings


def c5_foreshadow(fores, ms_texts):
    findings = []
    for f in fores:
        if f["status"] == "待回收":
            findings.append({
                "rule": "C5", "level": "WARN", "file": "(plot-board)",
                "msg": "伏笔 %s 仍『待回收』：%s（埋于第%d卷）" % (f["id"], f["desc"][:20], f["buried"]),
                "hint": "长线伏笔允许跨多卷；若已过预期回收卷请补回收",
            })
    return findings


# ---------- 去 AI 味：首版机械套路探测器 ----------
# 仅抓「确定性高、误报低」的套路信号；真正去味需在 references/06-去AI味.md 指导下做二遍改写。
AI_SIMILE = re.compile(r"(仿佛|似乎|宛若|犹如|宛如|好像|如同|恰似|一如|像\.\.\.一样|像\.\.\.般)")
AI_FILLER = re.compile(r"(不知何时|不知不觉|不知过了多久|恍然|蓦然|陡然|忽而|倏然|霎时|转瞬之间|与此同时|就在这时|话说|且说|却说)")
AI_EMOTION = re.compile(r"(他感到(无比|十分|非常|一阵|一股)?|他(心中|内心|心底)(涌起|充满|泛起|升起)|一种(莫名|难以名状)的(悲|喜|恐惧|愤怒|酸楚|温暖|感动))")
AI_MORAL = re.compile(r"(他(终于|这才|忽然|猛然|渐渐)?(明白|懂得|意识到|恍然大悟|豁然开朗|醒悟)了?(一个道理)?|那一刻(，|,)?他|从此(以后|，|,)?他|一种(莫名|难以名状|说不清)的)")
AI_INFOOPEN = re.compile(r"(这(是一|故事发生在)|话说|且说|却说|在(那|遥远)个(时候|年代|地方))")
AI_IMPERSONAL = re.compile(r"(令人|让人|使人|教人)([不一禁住]?(由得)?(感到|觉得|想|心头|鼻酸|心酸|震撼|动容|难忘|唏嘘))")
AI_SUDDEN = re.compile(r"(突然|忽然|猛地|骤然|陡地|倏地)")

C11_THRESHOLDS = {
    "simile": 3,    # 比喻连接词 每章上限
    "emdash": 5,    # 破折号「——」每章上限
    "filler": 3,    # 套路填充词 每章上限
    "emotion": 2,   # 情绪直给标签 每章上限
    "impersonal": 2,  # 无人称感受句 每章上限
    "sudden": 3,    # 突发转场词 每章上限
}


def c11_ai_flavor(ms_texts):
    """C11 去 AI 味：逐章探测首版常见机械套路（WARN 级，供作者二遍改写，非逻辑错误）。

    覆盖八类确定性高的信号：比喻连接词滥用 / 破折号滥用 / 套路填充词 / 情绪直给标签 /
    说教-总结式收尾 / 信息交代式开头 / 无人称感受句（令人…）/ 突发转场词滥用。
    阈值见 C11_THRESHOLDS，可据文风微调。探测器只做「探雷」，真正的去味是
    references/06-去AI味.md 的二遍改写。
    """
    findings = []
    for path, text in ms_texts:
        # 去掉标题行只统计正文，避免章节标题干扰计数
        body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
        fname = os.path.basename(path)

        n_sim = len(AI_SIMILE.findall(body))
        n_em = body.count("——")
        n_fill = len(AI_FILLER.findall(body))
        n_emo = len(AI_EMOTION.findall(body))
        n_moral = len(AI_MORAL.findall(body))
        n_info = len(AI_INFOOPEN.findall(body.strip()))
        n_imp = len(AI_IMPERSONAL.findall(body))
        n_sud = len(AI_SUDDEN.findall(body))

        checks = [
            ("比喻连接词", n_sim, C11_THRESHOLDS["simile"]),
            ("破折号", n_em, C11_THRESHOLDS["emdash"]),
            ("套路填充词", n_fill, C11_THRESHOLDS["filler"]),
            ("情绪直给标签", n_emo, C11_THRESHOLDS["emotion"]),
            ("说教/总结式收尾", n_moral, 1),
            ("信息交代式开头", n_info, 1),
            ("无人称感受句", n_imp, C11_THRESHOLDS["impersonal"]),
            ("突发转场词", n_sud, C11_THRESHOLDS["sudden"]),
        ]
        for label, n, th in checks:
            if n >= th:
                findings.append({
                    "rule": "C11", "level": "WARN", "file": fname,
                    "msg": "AI 味信号【%s】本章出现 %d 次（阈值 %d），建议二遍去味" % (label, n, th),
                    "hint": "参见 references/06-去AI味.md 对应范式做改写；若属有意为之可忽略",
                })
    return findings


def main():
    ap = argparse.ArgumentParser(description="小说一致性校验器")
    ap.add_argument("--bible", required=True, help="bible 目录")
    ap.add_argument("--ms", required=True, help="manuscript 目录（可含子目录）")
    ap.add_argument("--json", default="", help="输出 JSON 报告路径（可选）")
    args = ap.parse_args()

    if not os.path.isdir(args.bible):
        sys.stderr.write("ERROR: bible 目录不存在: %s\n" % args.bible)
        return 2
    if not os.path.isdir(args.ms):
        sys.stderr.write("ERROR: manuscript 目录不存在: %s\n" % args.ms)
        return 2

    ms_files = list_ms(args.ms)
    if not ms_files:
        sys.stderr.write("ERROR: manuscript 目录无 .md/.txt 文件\n")
        return 2
    ms_texts = [(p, read_text(p)) for p in ms_files]

    chars = parse_characters(args.bible)
    rules = parse_rules(args.bible)
    timeline_events = parse_timeline(args.bible)
    fores = parse_plotboard(args.bible)
    realm_seq = parse_cultivation(args.bible)
    artifacts = parse_artifacts(args.bible)
    rels = parse_relations(args.bible)
    clues = parse_clues(args.bible)
    panels = parse_system(args.bible)

    findings = []
    findings += c1_name_variants(chars, ms_texts)
    findings += c2_timeline(timeline_events, ms_texts)
    findings += c3_presence(chars, ms_texts)
    findings += c4_rules(rules, ms_texts)
    findings += c5_foreshadow(fores, ms_texts)
    findings += c6_realm_regress(chars, realm_seq, ms_texts)
    findings += c7_artifact_state(artifacts, ms_texts)
    findings += c8_relation_conflict(rels, ms_texts)
    findings += c9_clue_state(clues, ms_texts)
    findings += c10_system_state(panels, ms_texts)
    findings += c11_ai_flavor(ms_texts)

    errors = [f for f in findings if f["level"] == "ERROR"]
    warns = [f for f in findings if f["level"] == "WARN"]

    lines = []
    lines.append("# 一致性审计报告")
    lines.append("")
    lines.append("## 汇总：ERROR %d / WARN %d" % (len(errors), len(warns)))
    lines.append("")
    lines.append("    bible 人物数: %d | 规则数: %d | 时间线事件: %d | 伏笔: %d | 关键物品: %d | 线索: %d | 系统面板: %d | 正文文件: %d | 去AI味信号: %d"
                 % (len(chars), len(rules), len(timeline_events), len(fores), len(artifacts), len(clues), len(panels), len(ms_files), sum(1 for f in findings if f["rule"] == "C11")))
    lines.append("")
    for f in findings:
        lines.append("- **[%s/%s]** %s | %s" % (f["rule"], f["level"], f["file"], f["msg"]))
        lines.append("  - 误报提示：%s" % f["hint"])
    report = "\n".join(lines) + "\n"

    print(report)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fp:
            json.dump({"errors": len(errors), "warns": len(warns), "findings": findings},
                      fp, ensure_ascii=False, indent=2)
        print("JSON 报告已写入: %s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
