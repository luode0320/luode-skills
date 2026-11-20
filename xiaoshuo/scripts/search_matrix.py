#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄殿堂作家 · 增强联网检索矩阵生成器

把 references/web-search-protocol.md 的三波次检索协议变成可执行的关键词矩阵。
用于：① 每次交付前的三波次联网增强；② 月度自动进化的 21 组关键词。

用法：
    python search_matrix.py                                  # 生成当前月份的完整矩阵
    python search_matrix.py --wave 1                          # 只要波次一（动笔前）
    python search_matrix.py --genres 都市脑洞,悬疑脑洞         # 追加指定赛道词
    python search_matrix.py --out 检索清单.md                  # 落盘 Markdown
    python search_matrix.py --today 2026-10-01                # 指定日期（测试用）
    python search_matrix.py --json                            # JSON 输出

零第三方依赖，仅标准库。
"""

import argparse
import datetime
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── 词库（对齐 web-search-protocol.md 第三节）────────────────────
SUBJECTS = ["番茄小说", "番茄作家", "免费阅读平台", "网文平台", "红果短剧", "七猫", "起点"]
INTENTS = ["规则", "福利", "征文", "公告", "榜单", "趋势", "达标线", "及格线",
           "数据", "治理", "判定", "技巧", "方法", "拆解", "复盘"]
METRICS = ["完读率", "追更率", "书架比", "点击率", "在读人数", "评分", "听读收益"]
STAGES = ["签约", "验证期", "首秀", "书测", "上架", "完本", "断流"]
AUDIENCE = ["新人", "全职", "腰部作者", "中老年读者", "下沉市场"]
FORMS = ["长篇小说", "短故事", "漫剧", "短剧", "有声书"]
DEFAULT_GENRES = ["都市高武", "都市脑洞", "悬疑脑洞", "玄幻脑洞", "年代",
                  "豪门总裁", "快穿", "规则怪谈", "短剧改编"]

WAVES = {
    1: {"name": "波次一 · 动笔前（赛道与规则核验）",
        "desc": "核验近 30 天榜单趋势、当期征文活动、福利规则变更、读者结构",
        "templates": [
            ("当期征文活动", "{ym} 番茄小说 征文活动 公告 奖励"),
            ("当期征文活动", "{ym} 番茄小说 收稿 扶持 专项"),
            ("福利规则变更", "{ym} 番茄小说 作家福利 最新规则 档位"),
            ("福利规则变更", "{ym} 番茄小说 全勤 星火 完本 门槛 变化"),
            ("榜单趋势", "{ym} 番茄小说 榜单 热门题材 趋势"),
            ("榜单趋势", "{ym} 番茄小说 标签流量 排行 男频 女频"),
            ("赛道热度", "{ym} 番茄小说 {genre} 在读量 数据 热度"),
            ("读者画像", "{y} 番茄小说 用户画像 读者结构 年龄 地域"),
            ("短剧IP变现", "{ym} 番茄小说 短剧改编 版权 政策 分成"),
        ]},
    2: {"name": "波次二 · 写作中（写法与竞品核验）",
        "desc": "核验开篇方法、去 AI 味技巧、同类爆款当前写法、平台机制阈值",
        "templates": [
            ("开篇方法", "{y} 网文 开篇 留存率 技巧 前三章"),
            ("开篇方法", "{y} 网文 300字 生死线 3秒停留率 实战"),
            ("去AI味", "{y} 网文 去AI味 写作技巧 AI腔 改稿"),
            ("同类爆款写法", "{ym} {genre} 爆款 写法 拆解 复盘"),
            ("平台机制细节", "{ym} 番茄小说 首秀 验证期 及格线 书架比"),
            ("平台机制细节", "{ym} 番茄小说 书测 封面 书名 测试 规则"),
            ("节奏与钩子", "{y} 网文 章末钩子 爽点密度 追读率 提升"),
            ("人物与对话", "{y} 网文 人设 反差 对话 潜台词 技巧"),
        ]},
    3: {"name": "波次三 · 交付前（红线与治理核验）",
        "desc": "核验 AI 内容治理口径、敏感题材红线、版权与改编规则、政策法规",
        "templates": [
            ("AI治理口径", "{ym} 番茄小说 AI生成内容 治理 判定 违规 处罚"),
            ("AI治理口径", "{ym} 网文平台 AI检测 红线 拒稿 标准"),
            ("敏感题材", "{y} 网文 题材 红线 违规 下架 规避"),
            ("版权与改编", "{ym} 短剧改编 版权 授权 边界 纠纷"),
            ("政策法规", "{y} 网络文学 出版 管理 规定 政策"),
            ("低质治理数据", "{ym} 番茄小说 拒签 低质 清理 数据"),
        ]},
}


def build(ym, y, genres):
    out = []
    for wi in (1, 2, 3):
        w = WAVES[wi]
        rows = []
        seen = set()
        for topic, tpl in w["templates"]:
            if "{genre}" in tpl:
                for g in genres:
                    q = tpl.format(ym=ym, y=y, genre=g)
                    if q not in seen:
                        seen.add(q)
                        rows.append({"topic": topic, "query": q})
            else:
                q = tpl.format(ym=ym, y=y)
                if q not in seen:
                    seen.add(q)
                    rows.append({"topic": topic, "query": q})
        out.append({"wave": wi, "name": w["name"], "desc": w["desc"], "rows": rows})
    return out


def md(plan, ym):
    L = ["# 番茄殿堂作家 · 增强联网检索清单", "",
         "- 生成日期：%s" % datetime.date.today().isoformat(),
         "- 检索周期标识：%s" % ym,
         "- 规范来源：`references/web-search-protocol.md`", "",
         "> **立场**：联网不是装饰，是防过期的免疫系统。",
         "> 所有判断必须带来源与日期；禁止把历史榜单说成实时数据。", "",
         "---", ""]
    total = 0
    for w in plan:
        L.append("## %s" % w["name"])
        L.append("")
        L.append("%s" % w["desc"])
        L.append("")
        L.append("| # | 检索主题 | 检索关键词 | 核验结论 | 是否变更 |")
        L.append("|---|---|---|---|---|")
        for r in w["rows"]:
            total += 1
            L.append("| %d | %s | %s | | □ 变更 □ 不变 |" % (total, r["topic"], r["query"]))
        L.append("")
    L += ["---", "", "## 信源分级（每条结论必须标）", "",
          "| 等级 | 定义 | 使用方式 |", "|---|---|---|",
          "| **A【官方】** | 平台官方公告、作家专区、官方公众号 | 直接采信，作为硬规则 |",
          "| **B【实操】** | 作者社群、资深作者教程、有实测数据的经验帖 | 采信但标注「实操共识」 |",
          "| **C【分歧】** | 多来源口径不一致 | 并列保留，说明保守取法 |",
          "| **D【推断】** | 基于公开数据的合理推断 | 明确标注「推断」 |", "",
          "---", "", "## 时效标注规范", "",
          "| 场景 | 正确表述 | 错误表述 |", "|---|---|---|",
          "| 引用榜单 | 「截至 YYYY 年 M 月公开数据」 | 「目前榜单第一是……」 |",
          "| 引用规则 | 「据 YYYY-MM-DD 平台公告」 | 「平台规定……」 |",
          "| 引用经验 | 「据 YYYY 年作者社群实操共识」 | 「大家都这么做」 |",
          "| 联网失败 | 「基于 2026-09 资源库，未联网校验」 | 省略不提 |",
          "| 数据存疑 | 「两种口径并存，本方案取严」 | 只挑有利口径 |", "",
          "---", "", "## 冲突处理规则", "",
          "```",
          "资源库 vs 联网冲突 → 以联网最新为准",
          "  1. 交付物标注变更点：「资源库记 X，最新核验为 Y，本次采用 Y」",
          "  2. 把变更回流到对应 references 文件（带来源与日期）",
          "  3. 在 changelog.md 追加一条记录（只增不改）",
          "",
          "联网来源之间冲突 → 按信源分级排序（官方 > 实操 > 推断）",
          "  同级冲突 → 保留双方口径，施工取「更严」的一方",
          "```", "",
          "---", "", "## 检索质量自检", "",
          "- [ ] 是否至少跑了 6 组关键词？",
          "- [ ] 是否每组结论都标注了来源与日期？",
          "- [ ] 是否至少命中 1 条【官方】级信息？",
          "- [ ] 是否存在与资源库冲突的内容，且已按冲突规则处理？",
          "- [ ] 是否有任何把历史数据说成实时数据的表述？",
          "- [ ] 是否有任何编造的字段或数字？（**零容忍**）",
          "- [ ] 联网失败时是否已显式标注降级状态？",
          "", "**本清单共 %d 组关键词。**" % total, ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="番茄殿堂作家 · 增强联网检索矩阵生成器")
    ap.add_argument("--wave", type=int, choices=[1, 2, 3], help="只生成指定波次")
    ap.add_argument("--genres", help="追加赛道词，逗号分隔（默认 9 个主流赛道）")
    ap.add_argument("--out", metavar="FILE", help="输出 Markdown 文件")
    ap.add_argument("--today", help="指定日期 YYYY-MM-DD（测试用）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    if args.today:
        try:
            d = datetime.date.fromisoformat(args.today)
        except ValueError:
            print("[X] --today 格式应为 YYYY-MM-DD")
            sys.exit(1)
    else:
        d = datetime.date.today()

    ym = "%d年%d月" % (d.year, d.month)
    y = str(d.year)
    genres = [g.strip() for g in args.genres.split(",")] if args.genres else DEFAULT_GENRES

    plan = build(ym, y, genres)
    if args.wave:
        plan = [w for w in plan if w["wave"] == args.wave]

    if args.json:
        print(json.dumps({"period": ym, "waves": plan}, ensure_ascii=False, indent=2))
        return

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md(plan, ym))
        print("[OK] 检索清单已写入：%s" % args.out)
        return

    print("=" * 74)
    print("番茄殿堂作家 · 增强联网检索清单（%s）" % ym)
    print("=" * 74)
    total = 0
    for w in plan:
        print("\n【%s】" % w["name"])
        print("%s\n" % w["desc"])
        for r in w["rows"]:
            total += 1
            print("  %2d. [%s] %s" % (total, r["topic"], r["query"]))
    print("\n" + "=" * 74)
    print("共 %d 组关键词。信源分级与时效标注规范见 references/web-search-protocol.md" % total)
    print("=" * 74)


if __name__ == "__main__":
    main()
