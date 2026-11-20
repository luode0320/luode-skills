#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄殿堂作家 · 书测素材套餐生成器

依据 references/book-test-and-crisis-rescue.md：
  · 5 组素材 = 5 种不同的「点击诱因」（不是 5 个随机名字）
  · A 热词直给 / B 身份反差 / C 冲突前置 / D 悬念提问 / E 情绪价值
  · 每组配封面方向 + 简介三句话骨架
  · 输出操作禁忌提醒（中途关闭消耗名额等）

用法：
    python book_test_gen.py --genre 古言 --hero 商户女 --twist 重生先知 \\
        --conflict 退婚 --tag "重生,退婚,空间" --out 书测套餐.md

零第三方依赖，仅标准库。
"""

import argparse
import datetime
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 5 组策略模板：{hero}=主角身份 {twist}=反转/机制 {conflict}=核心冲突 {key}=关键词
STRATEGIES = [
    {
        "code": "A",
        "name": "热词直给型",
        "goal": "直接命中平台大标签，最大化类型识别度",
        "titles": [
            "{twist}{genre}：从{conflict}开始",
            "{tag1}之{hero}",
            "{conflict}后，我{twist}",
        ],
        "cover": "人物特写；风格主流、识别度高；主体占画面 60% 以上，缩略图可辨",
        "blurb": [
            "{hero}{conflict}那天，整个{genre}圈都在等她的笑话。",
            "只有她知道，{twist}已经在倒计时。",
            "她要做的，是让每一个看笑话的人，都笑不出来。",
        ],
        "risk": "同质化风险最高，必须确保正文兑现标签承诺",
    },
    {
        "code": "B",
        "name": "身份反差型",
        "goal": "阶级/身份错位，制造「意料之外，情理之中」的认知缺口",
        "titles": [
            "所有人都不知道，{hero}其实是{twist}",
            "全{genre}都以为{hero}是废物",
            "表面{hero}，实则{twist}",
        ],
        "cover": "身份符号对比；服饰/道具对撞（素衣 vs 华服、旧物 vs 名器）",
        "blurb": [
            "所有人眼里，{hero}就是个{conflict}都撑不住的废物。",
            "没人知道，她的{twist}，已经算了三千遍。",
            "直到那天，等着看笑话的人，跪在了她面前。",
        ],
        "risk": "反差必须在前三章给出第一次兑现，否则读者视为标题党",
    },
    {
        "code": "C",
        "name": "冲突前置型",
        "goal": "把最激烈的场面直接写进标题，用画面感换点击",
        "titles": [
            "她把{conflict}甩在了众人脸上",
            "{conflict}那天，她只说了三个字",
            "当着全{genre}的面，她撕了{conflict}",
        ],
        "cover": "动作场面；动态感强；手部/道具特写优先，避免静止人像",
        "blurb": [
            "{conflict}的文书摔在桌上，声音很响。",
            "满堂的人都在等她哭。",
            "她笑了，然后把{twist}摆了出来。",
        ],
        "risk": "标题承诺的场面必须在前 3 章内出现，且强度不能缩水",
    },
    {
        "code": "D",
        "name": "悬念提问型",
        "goal": "制造信息缺口，用「只差一步」的答案换点击",
        "titles": [
            "{conflict}后，他们都跪着求我回去",
            "谁也没想到，{hero}的{twist}是这样来的",
            "她死了三次，才学会{conflict}",
        ],
        "cover": "留白构图 + 悬念要素；背影、剪影、关键道具（不露正脸）",
        "blurb": [
            "{conflict}那天，她收到了一条消息。",
            "发消息的人，三年前就已经死了。",
            "而她必须在明天之前，弄清楚这是谁。",
        ],
        "risk": "悬念必须有阶段性回收，否则成为「神秘欠账」低留存死因",
    },
    {
        "code": "E",
        "name": "情绪价值型",
        "goal": "直接给情绪承诺，锁定特定情绪需求的读者",
        "titles": [
            "这一世，我只想护住自己",
            "{hero}不想{conflict}，她只想活着",
            "重来一次，我先救我自己",
        ],
        "cover": "情绪化构图；暖色调或高对比；亲密关系/背影/眼神",
        "blurb": [
            "上一世，她为了别人，把命都给了出去。",
            "这一世，她只做一件事——",
            "把属于自己的，一样一样拿回来。",
        ],
        "risk": "情绪型标题点击率高但留存依赖前 3 章的情绪兑现速度",
    },
]

TAG_POOL = ["穿书", "系统", "重生", "退婚", "开局", "空间", "签到", "无敌",
            "从…开始", "谁懂啊", "我靠…", "她死后", "都跪了", "侯门", "宅斗", "搞钱"]


def fill(tpl, ctx):
    try:
        return tpl.format(**ctx)
    except (KeyError, IndexError):
        out = tpl
        for k, v in ctx.items():
            out = out.replace("{%s}" % k, str(v))
        return out


def build(args):
    tags = [t.strip() for t in (args.tag or "").split(",") if t.strip()]
    ctx = {
        "genre": args.genre or "网文",
        "hero": args.hero or "主角",
        "twist": args.twist or "金手指",
        "conflict": args.conflict or "被赶出门",
        "tag1": tags[0] if tags else (args.twist or "金手指"),
        "tag2": tags[1] if len(tags) > 1 else "",
    }
    groups = []
    for s in STRATEGIES:
        groups.append({
            "code": s["code"],
            "name": s["name"],
            "goal": s["goal"],
            "titles": [fill(t, ctx) for t in s["titles"]],
            "cover": s["cover"],
            "blurb": [fill(b, ctx) for b in s["blurb"]],
            "risk": s["risk"],
        })
    suggested_tags = tags or TAG_POOL[:3]
    return {"ctx": ctx, "groups": groups, "suggested_tags": suggested_tags,
            "tag_pool": TAG_POOL}


def md(rep, args, today):
    c = rep["ctx"]
    L = ["# 番茄殿堂作家 · 书测素材套餐（5 组）", "",
         "- 生成日期：%s" % today,
         "- 作品定位：%s / 主角：%s / 核心机制：%s / 核心冲突：%s"
         % (c["genre"], c["hero"], c["twist"], c["conflict"]),
         "- 建议标签池：%s" % "、".join(rep["suggested_tags"]),
         "- 当前字数：%s  → 书测轮次：%s"
         % (args.words or "待填", args.round or "第一轮（20—50 万字）"),
         "",
         "> **5 组素材不是 5 个随机名字，是 5 种不同的点击诱因。** 系统同时投放，7—10 天按点击率择优。",
         "", "---", ""]
    for g in rep["groups"]:
        L.append("## %s 组 · %s" % (g["code"], g["name"]))
        L.append("")
        L.append("- **策略目标**：%s" % g["goal"])
        L.append("- **候选书名**（任选 1 个，或多测 1 个）")
        for t in g["titles"]:
            L.append("  - 《%s》" % t)
        L.append("- **封面方向**：%s" % g["cover"])
        L.append("- **简介三句话骨架**")
        for i, b in enumerate(g["blurb"], 1):
            L.append("  %d. %s" % (i, b))
        L.append("- **风险提示**：%s" % g["risk"])
        L.append("")
    L += ["---", "", "## 自检清单", "",
          "- [ ] 5 组是否构成 5 种**不同**的点击诱因？（不是同义改写）",
          "- [ ] 是否有任一组使用了**与正文不符**的标签？（书名简介错配 = 低留存第 11 类死因）",
          "- [ ] 5 组是否都保留了作品的核心承诺？",
          "- [ ] 封面是否为缩略图可辨的主体构图？",
          "- [ ] 简介是否避免了「先讲世界观 / 只写履历 / 堆三个反问 / 提新人慢热」？",
          "", "---", "", "## 操作禁忌（必读）", "",
          "1. ⚠️ **测试中途主动关闭 → 直接消耗本次测试名额，无法再次开启**",
          "2. ⚠️ **测试周期内不能大幅修改正文内容**，仅允许调整封面、书名、简介",
          "3. ⚠️ **首秀期不做书测**（首秀期严禁改封面/书名/简介，会被判异常降权）",
          "4. ✅ 测试期同步动作：日更保持稳定（4000—6000 字），时段**避开 22:00—24:00**",
          "5. ✅ 测试结束立即**锁定数据最优素材并更换**",
          "", "---", "", "## 时间窗口建议", "",
          "| 情形 | 建议节点 |", "|---|---|",
          "| 首秀数据低迷 / 点击率长期低于同赛道均值 | **20 万字立即书测** |",
          "| 数据正常、想提升单价 | **45 万字再书测**（字数多单价高） |",
          "| 验证流量低迷但单价可以（男频 10000:100 正常） | 高于此比例即可尝试 |",
          "| 第二轮书测 | **100 万字以上**，微调封面与文案风格防审美疲劳 |",
          "", "## 可用标签池", "",
          "`" + "` `".join(rep["tag_pool"]) + "`", "",
          "> **免责**：素材效果受题材、封面设计与当期流量环境影响，本套餐为创作侧参考，",
          "> 最终以平台书测实际点击率数据为准。", ""]
    return "\n".join(L)


def print_report(rep):
    print("=" * 74)
    print("番茄殿堂作家 · 书测素材套餐（5 组）")
    print("=" * 74)
    for g in rep["groups"]:
        print("\n【%s 组 · %s】%s" % (g["code"], g["name"], g["goal"]))
        print("  候选书名：")
        for t in g["titles"]:
            print("    · 《%s》" % t)
        print("  封面方向：%s" % g["cover"])
        print("  简介骨架：")
        for i, b in enumerate(g["blurb"], 1):
            print("    %d. %s" % (i, b))
        print("  风险：%s" % g["risk"])
    print("\n" + "=" * 74)
    print("禁忌：中途关闭消耗名额｜测试期不得大改正文｜首秀期不做书测")
    print("=" * 74)


def main():
    ap = argparse.ArgumentParser(description="番茄殿堂作家 · 书测素材套餐生成器")
    ap.add_argument("--genre", help="题材/频道，如 古言 / 都市 / 玄幻")
    ap.add_argument("--hero", help="主角身份，如 商户女 / 外卖骑手")
    ap.add_argument("--twist", help="核心机制/反转，如 重生先知 / 能看见谎言")
    ap.add_argument("--conflict", help="核心冲突，如 退婚 / 被顶替")
    ap.add_argument("--tag", help="关键词池，逗号分隔，如 重生,退婚,空间")
    ap.add_argument("--words", help="当前字数")
    ap.add_argument("--round", help="书测轮次说明")
    ap.add_argument("--out", metavar="FILE", help="输出 Markdown 文件")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    rep = build(args)
    today = datetime.date.today().isoformat()

    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print_report(rep)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md(rep, args, today))
        print("\n[OK] 书测套餐已写入：%s" % args.out)


if __name__ == "__main__":
    main()
