#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初始化小说 bible 目录骨架（单一事实源）。

用法:
  python build_bible.py --project ./my-novel

会在 <project>/bible/ 下生成 world-bible.md、characters/、timeline.md、plot-board.md，
内容来自技能 templates/ 目录。确定性、可复跑；已存在文件不覆盖。
"""
import argparse
import os
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "templates"))


def main():
    ap = argparse.ArgumentParser(description="初始化小说 bible 骨架")
    ap.add_argument("--project", required=True, help="项目根目录，将在其下创建 bible/")
    args = ap.parse_args()

    project = os.path.abspath(args.project)
    bible_dir = os.path.join(project, "bible")
    if not os.path.isdir(TEMPLATE_DIR):
        sys.stderr.write("ERROR: 模板目录不存在: %s\n" % TEMPLATE_DIR)
        return 2

    os.makedirs(bible_dir, exist_ok=True)
    os.makedirs(os.path.join(bible_dir, "characters"), exist_ok=True)

    copied = []
    skipped = []
    files = ["world-bible.md", "timeline.md", "plot-board.md"]
    for fn in files:
        src = os.path.join(TEMPLATE_DIR, fn)
        dst = os.path.join(bible_dir, fn)
        if os.path.exists(dst):
            skipped.append(fn)
        elif os.path.exists(src):
            shutil.copyfile(src, dst)
            copied.append(fn)
    # characters 下给一个示例人物卡
    sample = os.path.join(TEMPLATE_DIR, "character-card.md")
    sample_dst = os.path.join(bible_dir, "characters", "示例人物.md")
    if os.path.exists(sample) and not os.path.exists(sample_dst):
        shutil.copyfile(sample, sample_dst)
        copied.append("characters/示例人物.md")

    print("bible 目录: %s" % bible_dir)
    print("已复制: %s" % (", ".join(copied) if copied else "(无)"))
    print("已跳过(已存在): %s" % (", ".join(skipped) if skipped else "(无)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
