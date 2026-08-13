#!/usr/bin/env python3
"""long-run-loop-rules: check_completion_marker.py

检测 worker 输出中是否包含完成标记。

用法:
    python check_completion_marker.py --text <worker_output_text> --marker <marker_string>
    python check_completion_marker.py --file <output_file_path> --marker <marker_string>
    python check_completion_marker.py --text <text> --marker <marker> --mode regex

输出: {"found": true/false, "marker": "...", "position": N, "evidence": "..."}
"""

import argparse
import json
import re
import sys


def check_exact(text, marker):
    """精确匹配"""
    pos = text.find(marker)
    if pos >= 0:
        # 提取上下文
        start = max(0, pos - 40)
        end = min(len(text), pos + len(marker) + 40)
        evidence = text[start:end]
        return {"found": True, "marker": marker, "position": pos, "evidence": evidence.strip()}
    return {"found": False, "marker": marker, "position": -1, "evidence": ""}


def check_regex(text, marker):
    """正则匹配"""
    try:
        pattern = re.compile(marker, re.DOTALL)
        match = pattern.search(text)
        if match:
            start = max(0, match.start() - 40)
            end = min(len(text), match.end() + 40)
            evidence = text[start:end]
            return {"found": True, "marker": marker, "position": match.start(), "evidence": evidence.strip()}
        return {"found": False, "marker": marker, "position": -1, "evidence": ""}
    except re.error as e:
        return {"found": False, "marker": marker, "position": -1, "evidence": "", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="long-run-loop-rules: completion marker checker")
    parser.add_argument("--text", default=None, help="worker output text (inline)")
    parser.add_argument("--file", default=None, help="path to worker output file")
    parser.add_argument("--marker", required=True, help="completion marker to search for")
    parser.add_argument("--mode", default="exact", choices=["exact", "regex"], help="match mode (default: exact)")
    args = parser.parse_args()

    text = args.text
    if args.file:
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

    if not text:
        print(json.dumps({"found": False, "marker": args.marker, "position": -1, "evidence": "", "error": "no input text"}))
        sys.exit(0)

    if args.mode == "regex":
        result = check_regex(text, args.marker)
    else:
        result = check_exact(text, args.marker)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
