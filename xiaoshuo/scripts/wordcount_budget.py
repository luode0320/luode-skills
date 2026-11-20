#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""百万字长篇字数预算分配（确定性）。

用法:
  python wordcount_budget.py --total 1000000 --volumes 5 --chapters-per-volume 60
  python wordcount_budget.py --total 1200000 --weights 1,1.2,1.5,1.2,0.8 --chapters-per-volume 60

输出每卷字数上限与每章建议字数。纯算术，可复跑一致。
"""
import argparse
import sys


def parse_weights(s):
    return [float(x) for x in s.split(",") if x.strip() != ""]


def main():
    ap = argparse.ArgumentParser(description="长篇字数预算分配")
    ap.add_argument("--total", type=int, required=True, help="全书目标字数，如 1000000")
    ap.add_argument("--volumes", type=int, default=0, help="卷数（与 --weights 二选一）")
    ap.add_argument("--weights", type=str, default="", help="各卷权重，逗号分隔，如 1,1.2,1.5,1.2,0.8")
    ap.add_argument("--chapters-per-volume", type=int, default=60, help="每卷章数（用于章均分）")
    ap.add_argument("--midpoint-boost", type=float, default=1.0, help="中点卷加权系数，默认 1.0")
    args = ap.parse_args()

    if args.weights:
        weights = parse_weights(args.weights)
        if not weights:
            sys.stderr.write("ERROR: --weights 解析为空\n")
            return 2
        n = len(weights)
    elif args.volumes > 0:
        n = args.volumes
        base = [1.0] * n
        mid = n // 2
        base[mid] = args.midpoint_boost if args.midpoint_boost > 0 else 1.0
        weights = base
    else:
        sys.stderr.write("ERROR: 需提供 --volumes 或 --weights\n")
        return 2

    total_w = sum(weights)
    print("全书目标: %d 字 | 卷数: %d | 每卷章数: %d" % (args.total, n, args.chapters_per_volume))
    print("%-6s %-10s %-12s %s" % ("卷", "权重", "卷字数", "章均字数"))
    grand = 0
    for i, w in enumerate(weights, 1):
        vol_words = int(round(args.total * w / total_w))
        per_ch = int(round(vol_words / args.chapters_per_volume))
        grand += vol_words
        print("卷%-3d %-10.2f %-12d %d" % (i, w, vol_words, per_ch))
    print("合计: %d 字 (目标 %d，误差 %+d)" % (grand, args.total, grand - args.total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
