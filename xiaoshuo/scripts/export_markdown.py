#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄殿堂作家 · Markdown 导出与交付整理

用法：
    python export_markdown.py --input <产出目录> --out <交付目录> --title <作品名>
    python export_markdown.py --input ./chapters --out ./交付 --title 冒姓琅琊 --split
    python export_markdown.py --text "正文内容" --out ./交付 --title 冒姓琅琊 --kind 章节

功能：
    1. 合并产出目录下的 .md/.txt 为单一「整合稿」
    2. 可选保留分章稿（--split）
    3. 自动生成交付说明骨架（含算法对齐卡、质检入口、格式导出提示）
    4. 生成目录索引与统计信息

输出文件命名：{作品名}_{类型}_{YYYYMMDD}.md
所有内容均为 Markdown，可随时导出为 PDF / Word / HTML 等主流格式。

零第三方依赖，仅标准库。
"""

import argparse
import datetime
import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KIND_LABEL = {
    "chapter": "章节正文",
    "outline": "大纲架构",
    "brief": "立项方案",
    "report": "质检报告",
    "package": "整合稿",
}


def read_text(path):
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def natural_key(name):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def collect(src):
    if os.path.isfile(src):
        return [src]
    out = []
    for root, _dirs, names in os.walk(src):
        for n in sorted(names, key=natural_key):
            if n.lower().endswith((".md", ".txt")) and not n.startswith("."):
                out.append(os.path.join(root, n))
    return out


def cn_count(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text))


DELIVERY_TEMPLATE = """# {title} · 交付说明

> 本文件由「番茄殿堂作家」自动生成骨架，请在方括号位置填入实际内容。
> 全部内容为 Markdown，可随时导出为 PDF / Word / HTML 等主流格式。

## 一、本次交付物清单

{file_list}

## 二、赛道卡

- 频道：<男频/女频 - 具体分类>
- 供需判定：<过热 / 均衡 / 蓝海>，依据：<榜单席位 + 头部壁垒 + 均值在读走势>
- 目标读者：<年龄段 / 核心情绪需求>
- 核心爽点 Top3：<身份反转 / 生死博弈 / 信息差碾压 …>
- 差异化切口：<一句话能讲清>
- 对标样本：<2-3 本 + 在读量级>
- 情报日期：<本次引用的榜单日期>

## 三、作品立项卡

- 一句话卖点：<谁 + 在什么绝境 + 靠什么 + 达成什么>
- 核心设定与金手指：<含代价与限制>
- 主角人设与动机：<一句话>
- 关键配角：<3-5 名，各一句话>
- 长线悬念：<总纲层终局画面>
- 预计篇幅与分卷数：<X 万字 / X 卷>

## 四、黄金三章自检卡

- 第 1 章前 300 字钩子类型：<绝境/异象/身份反差/信息差/临终回望/规则宣告>
- 三章爽点类型：<…>
- 章末钩子类型与强度：<…>
- 金手指代价：<…>
- 受气→反击间隔：<≤3 章？>
- 禁用项命中：<开篇禁忌清单逐条核对结果>

## 五、殿堂体检（脚本报告）

- 执行命令：`python scripts/tomato_audit.py <稿件目录> --json`
- AI 味评分：<__ / 100>
- 高危句式命中：<__ 处>
- 计数一致性疑点：<__ 处>
- 已完成的改写动作：<…>
- 复跑结果：<达标 / 未达标>

## 六、算法对齐卡

- 作品名：{title}
- 当前字数：<X 万字>
- 所处流量池：<六层之一>
- 本阶段核心考核：<该池对应 1–2 个指标 + 达标线>
- 已完成动作：<…>
- 未来 7 天动作：<…>
- 风险提示：<是否触碰断流红线 / 是否接近 AI 低质判定>
- 知识截止：2026-09-11

## 七、本次关键假设清单

<按"假设 + 影响"逐条列出，用户可逐条指正，指正后秒级迭代>

## 八、下一步建议

1. <…>
2. <…>
3. <…>

## 九、格式导出提示

本次全部文字内容均为 Markdown 文件，可直接使用，也可随时导出为：
- **Word / PDF**：用任意 Markdown 编辑器或在线转换工具一键导出
- **HTML**：直接推送至公众号、文档平台或自建站点
- **纯文本 TXT**：番茄作家助手后台粘贴发布（推荐直接复制章节正文）

> 平台规则提示：番茄小说平台规则高频变动，本文档引用的平台情报知识截止 **2026-09-11**，
> 超过 30 天建议运行 `python scripts/search_matrix.py --wave 1` 生成当期检索清单，
> 按 `references/platform/web-search-protocol.md` 复核后再做重要决策。
"""


def build_filelist(items):
    if not items:
        return "- <无>"
    lines = []
    for i, (name, chars) in enumerate(items, 1):
        lines.append("%d. `%s` —— %d 字" % (i, name, chars))
    total = sum(c for _n, c in items)
    lines.append("")
    lines.append("**合计：%d 个文件，%d 字**" % (len(items), total))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="番茄殿堂作家 · Markdown 导出与交付整理")
    ap.add_argument("--input", help="产出目录或文件")
    ap.add_argument("--text", help="直接落盘的正文内容（与 --input 二选一）")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--title", default="未命名作品", help="作品名")
    ap.add_argument("--kind", default="package", choices=list(KIND_LABEL.keys()), help="产出类型")
    ap.add_argument("--split", action="store_true", help="同时保留分章稿")
    ap.add_argument("--no-delivery", action="store_true", help="不生成交付说明文件")
    args = ap.parse_args()

    today = datetime.date.today().strftime("%Y%m%d")
    os.makedirs(args.out, exist_ok=True)

    entries = []

    if args.text:
        name = "%s_%s_%s.md" % (args.title, KIND_LABEL[args.kind], today)
        dst = os.path.join(args.out, name)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(args.text.strip() + "\n")
        entries.append((name, cn_count(args.text)))
        print("[OK] 已落盘：%s（%d 字）" % (dst, cn_count(args.text)))
    elif args.input:
        files = collect(args.input)
        if not files:
            print("[X] 未找到 .md/.txt 文件：%s" % args.input)
            sys.exit(2)

        # 分章稿复制
        if args.split:
            keep_dir = os.path.join(args.out, "分章稿")
            os.makedirs(keep_dir, exist_ok=True)
            for fp in files:
                shutil.copy2(fp, os.path.join(keep_dir, os.path.basename(fp)))
            print("[OK] 分章稿已保留：%s（%d 个）" % (keep_dir, len(files)))

        # 合并
        parts, idx_lines, total = [], [], 0
        for i, fp in enumerate(files, 1):
            t = read_text(fp).strip()
            if not t:
                continue
            c = cn_count(t)
            total += c
            idx_lines.append("%d. %s —— %d 字" % (i, os.path.basename(fp), c))
            parts.append("<!-- ===== %s ===== -->\n\n%s" % (os.path.basename(fp), t))
        merged = "\n\n\n".join(parts)

        merged_name = "%s_整合稿_%s.md" % (args.title, today)
        with open(os.path.join(args.out, merged_name), "w", encoding="utf-8") as f:
            f.write("# %s（整合稿）\n\n> 生成时间：%s\n> 合计：%d 个文件 · %d 字\n\n---\n\n%s\n"
                    % (args.title, datetime.date.today().isoformat(), len(files), total, merged))
        entries.append((merged_name, total))
        print("[OK] 整合稿已生成：%s（%d 字）" % (merged_name, total))

        idx_name = "%s_目录索引_%s.md" % (args.title, today)
        with open(os.path.join(args.out, idx_name), "w", encoding="utf-8") as f:
            f.write("# %s · 目录索引\n\n生成时间：%s\n\n%s\n"
                    % (args.title, datetime.date.today().isoformat(), "\n".join(idx_lines)))
        entries.append((idx_name, 0))
    else:
        print("[X] 请提供 --input 或 --text")
        sys.exit(1)

    if not args.no_delivery:
        del_name = "%s_交付说明_%s.md" % (args.title, today)
        content = DELIVERY_TEMPLATE.format(title=args.title, file_list=build_filelist(entries))
        with open(os.path.join(args.out, del_name), "w", encoding="utf-8") as f:
            f.write(content)
        print("[OK] 交付说明骨架已生成：%s（按方括号填写内容）" % del_name)

    print("\n输出目录：%s" % os.path.abspath(args.out))
    print("全部内容为 Markdown，可随时导出为 PDF / Word / HTML 等主流格式。")


if __name__ == "__main__":
    main()
