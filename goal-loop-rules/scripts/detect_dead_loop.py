#!/usr/bin/env python3
"""long-run-loop-rules: detect_dead_loop.py

检测 worker 循环是否陷入死循环。对比最近 N 轮的产出变化，判断是否无实质进展。

用法:
    python detect_dead_loop.py --summaries <json_array_of_summaries> [--window 5] [--threshold 0.95]
    python detect_dead_loop.py --file <state_file_path> [--window 5] [--threshold 0.95]

输出: {"dead_loop": true/false, "reason": "...", "similarity": 0.xx, "diff_stats": {...}}
"""

import argparse
import json
import os
import sys
import re


def _extract_change_count(summary):
    """从 worker 摘要中提取文件变更数。"""
    # 匹配 "changed N files" / "N files changed" / "文件变更数: N"
    patterns = [
        r"(\d+)\s+files?\s+changed",
        r"changed\s+(\d+)\s+files?",
        r"文件变更[数了共]?\s*[:：]?\s*(\d+)",
        r"(\d+)\s+个文件",
        r"diff\s+lines?\s*[:：]?\s*(\d+)",
        r"(\d+)\s+lines?\s+of\s+diff",
    ]
    for p in patterns:
        m = re.search(p, summary, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return 0


def _extract_diff_lines(summary):
    """从 worker 摘要中提取 diff 行数。"""
    patterns = [
        r"diff\s+lines?\s*[:：]?\s*(\d+)",
        r"(\d+)\s+lines?\s+of\s+diff",
        r"diff[线行]数[:：]?\s*(\d+)",
        r"新增[了]?\s*(\d+)\s*[行条]",
        r"删除[了]?\s*(\d+)\s*[行条]",
    ]
    for p in patterns:
        m = re.search(p, summary, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return 0


def _text_similarity(texts, window):
    """计算最近 N 轮文本之间的平均相似度（基于字符 n-gram 的 Jaccard 相似度）。"""
    if len(texts) < 2:
        return 0.0

    recent = texts[-window:] if len(texts) >= window else texts
    total_sim = 0.0
    pairs = 0

    for i in range(len(recent) - 1):
        for j in range(i + 1, len(recent)):
            s1 = recent[i][:500]  # 取前 500 字符
            s2 = recent[j][:500]
            if not s1 or not s2:
                continue

            # 字符 3-gram 的 Jaccard 相似度
            set1 = {s1[k:k+3] for k in range(len(s1) - 2)}
            set2 = {s2[k:k+3] for k in range(len(s2) - 2)}
            if not set1 or not set2:
                continue
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            if union == 0:
                continue
            total_sim += intersection / union
            pairs += 1

    return total_sim / pairs if pairs > 0 else 0.0


def detect_dead_loop(summaries, window=5, threshold=0.95):
    """检测死循环。

    Args:
        summaries: worker 摘要列表
        window: 检测窗口大小
        threshold: 相似度阈值

    Returns:
        dict with dead_loop, reason, similarity, diff_stats
    """
    if len(summaries) < window:
        return {"dead_loop": False, "reason": "insufficient data", "similarity": 0.0, "diff_stats": {}}

    recent = summaries[-window:]

    # 统计文件变更数和 diff 行数
    change_counts = [_extract_change_count(s) for s in recent]
    diff_lines = [_extract_diff_lines(s) for s in recent]

    # 计算文本相似度
    similarity = _text_similarity(recent, window)

    total_changes = sum(change_counts)
    total_diff = sum(diff_lines)

    stats = {
        "window": window,
        "change_counts": change_counts,
        "total_changes": total_changes,
        "diff_lines": diff_lines,
        "total_diff_lines": total_diff,
        "text_similarity": round(similarity, 4),
    }

    # 判定条件
    # 注意：worker 摘要可能只报告文件变更数而不报告 diff 行数，
    # 此时 diff_lines 全为 0 属于"信息缺失"，不能单独作为死循环证据；
    # 只有两路进展信号（文件变更数、diff 行数）都缺失/为零时才判定无进展。
    reasons = []
    file_change_signal = any(c > 0 for c in change_counts)
    diff_signal = any(d > 0 for d in diff_lines)

    if not file_change_signal and not diff_signal:
        # 两路信号均无进展，才使用无进展类判定
        if total_changes < 2:
            reasons.append(f"最近 {window} 轮文件变更数与 diff 行数均为 0")
        if similarity > threshold:
            reasons.append(f"文本相似度 {similarity:.4f} 超过阈值 {threshold}")
    else:
        # 已有 diff 行数进展时，文件变更数缺失不作为死循环证据
        if not file_change_signal and total_changes < 2:
            reasons.append(f"最近 {window} 轮文件变更数为 0")

    if reasons:
        return {
            "dead_loop": True,
            "reason": "; ".join(reasons),
            "similarity": round(similarity, 4),
            "diff_stats": stats,
        }

    return {
        "dead_loop": False,
        "reason": "no dead loop detected",
        "similarity": round(similarity, 4),
        "diff_stats": stats,
    }


def main():
    parser = argparse.ArgumentParser(description="long-run-loop-rules: dead loop detector")
    parser.add_argument("--summaries", default=None, help="JSON array of worker summary strings")
    parser.add_argument("--file", default=None, help="path to loop state file (reads worker_summaries)")
    parser.add_argument("--window", type=int, default=5, help="detection window size (default: 5)")
    parser.add_argument("--threshold", type=float, default=0.95, help="similarity threshold (default: 0.95)")
    args = parser.parse_args()

    summaries = []
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            state = json.load(f)
        summaries = state.get("worker_summaries", [])
    elif args.summaries:
        summaries = json.loads(args.summaries)
    else:
        print(json.dumps({"error": "provide --summaries or --file"}))
        sys.exit(1)

    result = detect_dead_loop(summaries, window=args.window, threshold=args.threshold)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
