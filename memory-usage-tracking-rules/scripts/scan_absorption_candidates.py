#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_absorption_candidates.py — 吸收候选扫描（只读）

读取三记忆文件的计数锚点，输出达到吸收阈值的候选清单，供收口闸门自动吸收使用。

用法：
  python scan_absorption_candidates.py \
      --project-root D:/谷歌云盘/luode-skills \
      --project-slug luode-skills

参数：
  --project-root   项目根目录（默认当前目录或环境变量 PROJECT_ROOT）
  --memory-file / --style-file / --history-file  三文件显式路径（缺省按固定名找）
  --project-slug   项目 slug（用于生成建议 skill 名，默认取项目根目录名）
  --min-usage      最小使用次数阈值（默认 3）
  --min-days       最小引用天数阈值（默认 2）
  --with-weak      同时输出 HISTORY 弱信号候选（默认不输出）

吸收阈值（全部满足才进入候选）：
  usage_count >= min_usage
  AND usage_days >= min_days          （引用分布在 >= min_days 个不同日期）
  AND absorbed_to 为空
  AND 生命周期状态为 active（MEMORY 缺省视为 active）

输出（stdout JSON）：
  {"candidates": [{"file", "anchor", "title", "usage_count", "usage_days",
                   "last_used_at", "status", "weak_signal",
                   "suggested_skill_name", "dedup_hint"}],
   "threshold": {...}, "existing_project_skills": [...], "generated_at": "..."}

existing_project_skills 列出项目根 skills/ 下 project-* 目录（luode-skills 仓库特例含仓库根；
另兼容扫描用户级 ~/.workbuddy/skills 与 ~/.claude/skills 防历史重复），供 AI 对照查重。
退出码：0 = 正常；1 = 参数/读取错误。只读脚本，不修改任何文件。
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from usage_ledger_validate import (  # noqa: E402
    HISTORY_NAME,
    MEMORY_NAME,
    STYLE_NAME,
    parse_anchor_section_anchors,
    parse_memory_anchors,
)


def locate_file(project_root, kind, explicit_path):
    if explicit_path:
        return explicit_path
    names = {MEMORY_NAME, STYLE_NAME, HISTORY_NAME}
    for name in names:
        if kind in name.lower():
            return os.path.join(project_root, name)
    raise ValueError(f"无法定位文件: {kind}")


def read_body(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def make_suggested_skill_name(slug, title):
    """从条目标题生成建议 skill 名：project-<slug>-<topic>-rules。

    优先提取英文/数字 token 用 '-' 连接；全中文时保留前 8 个中文字符。
    仅为建议，最终命名由 AI 按 project-skill-template.md 裁决。
    """
    tokens = re.findall(r"[a-zA-Z0-9]+", title)
    if tokens:
        topic = "-".join(tokens).lower()[:40]
    else:
        topic = re.sub(r"\s+", "", title)[:8]
    return f"project-{slug}-{topic}-rules"


def existing_project_skills(project_root):
    """列出已存在的 project-* skill 目录，供 AI 对照查重。

    主扫描：项目根 skills/（新落点）；luode-skills 仓库特例：仓库根即 skill 资产库，
    同时扫描项目根本身。兼容扫描：用户级 ~/.workbuddy/skills 与 ~/.claude/skills
    （历史 project-* 曾落用户级，查重防重复）。
    """
    roots = [
        os.path.join(project_root, "skills"),
        project_root,  # luode-skills 仓库特例：仓库根即 skill 资产库
    ]
    home = os.path.expanduser("~")
    roots += [
        os.path.join(home, ".workbuddy", "skills"),
        os.path.join(home, ".claude", "skills"),
    ]
    found = []
    for base in roots:
        if os.path.isdir(base):
            for d in sorted(os.listdir(base)):
                if d.startswith("project-") and d not in found:
                    found.append(d)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=os.environ.get("PROJECT_ROOT") or ".")
    parser.add_argument("--memory-file", default=None)
    parser.add_argument("--style-file", default=None)
    parser.add_argument("--history-file", default=None)
    parser.add_argument("--project-slug", default=None)
    parser.add_argument("--min-usage", type=int, default=3)
    parser.add_argument("--min-days", type=int, default=2)
    parser.add_argument("--with-weak", action="store_true")
    args = parser.parse_args()

    slug = args.project_slug or os.path.basename(os.path.abspath(args.project_root))

    try:
        paths = {
            "memory": locate_file(args.project_root, "memory", args.memory_file),
            "style": locate_file(args.project_root, "style", args.style_file),
            "history": locate_file(args.project_root, "history", args.history_file),
        }
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "error": f"定位文件失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        memory_ents = parse_memory_anchors(read_body(paths["memory"]))
        style_anchors = parse_anchor_section_anchors(read_body(paths["style"]))
        history_anchors = parse_anchor_section_anchors(read_body(paths["history"]))
    except OSError as e:
        print(json.dumps({"ok": False, "error": f"读取文件失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    candidates = []

    def consider(file_key, anchor, title, usage_count, usage_days, last_used_at, status, absorbed_to, weak=False):
        if not anchor:
            return
        if absorbed_to:  # 已吸收条目冻结，不再进候选
            return
        if usage_count is None or usage_count < args.min_usage:
            return
        if usage_days is None or usage_days < args.min_days:
            return
        if weak and not args.with_weak:
            return
        if hasattr(last_used_at, "strftime"):  # yaml 解析出的 date/datetime 转字符串
            last_used_at = last_used_at.strftime("%Y-%m-%d")
        candidates.append({
            "file": file_key,
            "anchor": anchor,
            "title": title or anchor,
            "usage_count": usage_count,
            "usage_days": usage_days,
            "last_used_at": last_used_at,
            "status": status or "active",
            "weak_signal": weak,
            "suggested_skill_name": make_suggested_skill_name(slug, title or anchor),
            "dedup_hint": "查重: ls <项目根>/skills/ | grep '^project-'（luode-skills 仓库: ls . | grep '^project-'）",
        })

    # MEMORY：entities[]（主候选）
    for eid, ent in memory_ents.items():
        status = (ent.get("status") or "active").lower()
        if status in ("deprecated", "stale", "retired", "conflicted"):
            continue
        consider(
            MEMORY_NAME, eid, ent.get("name") or eid,
            ent.get("usage_count"), ent.get("usage_days"),
            ent.get("last_used_at"), ent.get("status"), ent.get("absorbed_to"),
        )

    # STYLE：anchors[]（主候选）
    for a in style_anchors:
        consider(
            STYLE_NAME, a["title"], a["title"],
            a.get("usage_count"), a.get("usage_days"),
            a.get("last_used_at"), None, a.get("absorbed_to"),
        )

    # HISTORY：anchors[]（弱信号，默认不输出）
    for a in history_anchors:
        consider(
            HISTORY_NAME, a["title"], a["title"],
            a.get("usage_count"), a.get("usage_days"),
            a.get("last_used_at"), None, a.get("absorbed_to"), weak=True,
        )

    candidates.sort(key=lambda c: (-(c["usage_count"] or 0), -(c["usage_days"] or 0)))

    result = {
        "candidates": candidates,
        "threshold": {"min_usage": args.min_usage, "min_days": args.min_days},
        "existing_project_skills": existing_project_skills(args.project_root),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
