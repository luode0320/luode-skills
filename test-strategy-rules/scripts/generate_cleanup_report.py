#!/usr/bin/env python3
"""
生成测试资产清理报告

扫描 test/ 目录，输出格式化的清理报告（Markdown / JSON）。
支持两种输出格式。

用法:
    python test-strategy-rules/scripts/generate_cleanup_report.py --root <repo_root> [--format markdown|json] [--output <file>]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# 复用 scan_stale_test_assets 的分类逻辑
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_stale_test_assets import scan, generate_report


def generate_json_report(results: list[dict], repo_root: Path) -> str:
    """生成 JSON 格式报告"""
    report = {
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo_root),
        "total_assets": len(results),
        "categories": {},
        "assets": results,
    }

    for r in results:
        cat = r["category"]
        if cat not in report["categories"]:
            report["categories"][cat] = {"count": 0, "action": r["action"]}
        report["categories"][cat]["count"] += 1

    return json.dumps(report, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="生成测试资产清理报告")
    parser.add_argument("--root", required=True, help="仓库根目录")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="输出格式")
    parser.add_argument("--output", help="输出文件路径（默认输出到 stdout）")
    parser.add_argument("--dry-run", action="store_true", default=True, help="仅扫描不执行清理（默认启用）")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()

    results = scan(repo_root, dry_run=True)

    if args.format == "json":
        output = generate_json_report(results, repo_root)
    else:
        output = generate_report(results, repo_root)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        print(f"报告已写入: {output_path}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
