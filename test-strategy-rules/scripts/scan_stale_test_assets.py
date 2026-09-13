#!/usr/bin/env python3
"""
测试过期资产扫描脚本

扫描 test/ 目录下的资产，按六类分类标记，识别遗留资产（无对应 skill 的目录）。
支持 --dry-run 模式。

用法:
    python test-strategy-rules/scripts/scan_stale_test_assets.py --root <repo_root> [--dry-run]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def collect_registered_skills(repo_root: Path) -> set[str]:
    """扫描仓库中所有 SKILL.md 的 name 字段，返回已注册 skill 名集合"""
    skills = set()
    for skill_md in repo_root.rglob("**/SKILL.md"):
        # 排除 node_modules 和 .git
        rel = skill_md.relative_to(repo_root).as_posix()
        if "node_modules" in rel or ".git" in rel:
            continue
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
        if m:
            skills.add(m.group(1).strip())
    return skills


def is_referenced_by_test(path: Path, repo_root: Path) -> bool:
    """检查文件是否被 test/ 下的测试文件引用"""
    name = path.name
    stem = path.stem  # 不带扩展名
    # 搜索 test/ 下所有测试文件是否包含该文件名
    test_dir = repo_root / "test"
    if not test_dir.exists():
        return False
    for test_file in test_dir.rglob("*_test.py"):
        try:
            content = test_file.read_text(encoding="utf-8", errors="replace")
            if name in content or stem in content:
                return True
        except Exception:
            continue
    return False


def classify_asset(path: Path, repo_root: Path, registered_skills: set[str]) -> dict:
    """对单个路径进行资产分类"""
    rel = path.relative_to(repo_root).as_posix()
    parts = rel.split("/")

    # 编译缓存
    if path.name == "__pycache__" or path.suffix == ".pyc":
        return {"path": rel, "category": "编译缓存", "action": "自动清理", "reason": "自动生成的字节码，可重建"}

    # 共享辅助代码
    if rel.startswith("test/shared/"):
        return {"path": rel, "category": "共享辅助代码", "action": "保留", "reason": "跨测试复用的 helper"}

    # 测试运行器
    if rel == "test/run_python_tests.py":
        return {"path": rel, "category": "共享辅助代码", "action": "保留", "reason": "测试运行器，持续使用"}

    # 正式测试代码
    if path.suffix == ".py" and path.name.endswith("_test.py"):
        return {"path": rel, "category": "正式测试代码", "action": "保留", "reason": "长期有效的测试文件"}
    if path.suffix == ".go" and path.name.endswith("_test.go"):
        return {"path": rel, "category": "正式测试代码", "action": "保留", "reason": "长期有效的测试文件"}

    # 遗留资产：对应 skill 已不存在的测试目录
    if len(parts) >= 2 and parts[0] == "test":
        skill_dir = parts[1]  # test/<skill-name>/...
        # 排除 shared 和 test-asset-governance 等特殊目录
        special_dirs = {"shared", "test-asset-governance", "run_python_tests.py"}
        if skill_dir not in special_dirs and not any(skill_dir == s.replace("-", "_") or skill_dir == s for s in registered_skills):
            # 检查是否可能在 registered_skills 中有匹配
            skill_match = False
            for s in registered_skills:
                # skill 名可能使用下划线或连字符，尝试模糊匹配
                if skill_dir.replace("_", "-") == s.replace("_", "-"):
                    skill_match = True
                    break
            if not skill_match:
                return {"path": rel, "category": "遗留资产", "action": "待确认清理", "reason": f"skill '{skill_dir}' 未在仓库中注册"}

    # 临时测试数据
    if "temp" in parts or "fixtures" in parts:
        # 检查是否被测试文件引用
        if is_referenced_by_test(path, repo_root):
            return {"path": rel, "category": "正式测试数据", "action": "保留", "reason": "fixture 数据，被测试文件引用"}
        return {"path": rel, "category": "临时测试数据", "action": "待确认清理", "reason": "测试生成的临时数据，未被测试文件引用"}

    # 一次性调试脚本
    if path.suffix in (".py", ".sh", ".bat") and not path.name.endswith("_test.py"):
        # 检查是否在 test/ 下但非测试文件
        if rel.startswith("test/") and not path.name.endswith("_test.go"):
            return {"path": rel, "category": "一次性调试脚本", "action": "待确认清理", "reason": "非标准测试命名，可能为一次性脚本"}

    # 默认：临时测试数据
    if rel.startswith("test/"):
        return {"path": rel, "category": "临时测试数据", "action": "待确认清理", "reason": "未分类的测试资产"}

    return {"path": rel, "category": "未知", "action": "需人工判断", "reason": "无法自动分类"}


def scan(repo_root: Path, dry_run: bool = True) -> list[dict]:
    """扫描 test/ 目录下的所有资产"""
    test_dir = repo_root / "test"
    if not test_dir.exists():
        print(f"test/ 目录不存在: {test_dir}")
        return []

    registered_skills = collect_registered_skills(repo_root)
    print(f"已注册 skill 数: {len(registered_skills)}")
    if dry_run:
        print(f"注册的 skill: {sorted(registered_skills)}")

    results = []
    # 遍历 test/ 下的所有文件和目录
    for entry in sorted(test_dir.rglob("*")):
        if entry.is_dir():
            continue
        # 排除 .gitkeep
        if entry.name == ".gitkeep":
            continue
        result = classify_asset(entry, repo_root, registered_skills)
        results.append(result)

    return results


def generate_report(results: list[dict], repo_root: Path) -> str:
    """生成清理报告"""
    lines = []
    lines.append("# 测试资产清理报告\n")
    lines.append(f"扫描时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append(f"仓库根目录: {repo_root}\n")

    # 按类别统计
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"count": 0, "paths": []}
        categories[cat]["count"] += 1
        categories[cat]["paths"].append(r)

    lines.append("## 统计\n")
    lines.append("| 类别 | 数量 | 建议操作 |")
    lines.append("|------|------|---------|")
    for cat, data in sorted(categories.items()):
        action = data["paths"][0]["action"] if data["paths"] else "未知"
        lines.append(f"| {cat} | {data['count']} | {action} |")
    lines.append("")

    # 待清理资产详情
    cleanup_categories = {"遗留资产", "临时测试数据", "一次性调试脚本"}
    has_cleanup = any(r["category"] in cleanup_categories and r["action"] != "保留" for r in results)
    if has_cleanup:
        lines.append("## 待清理资产\n")
        for r in results:
            if r["category"] in cleanup_categories and r["action"] != "保留":
                lines.append(f"- **{r['path']}**")
                lines.append(f"  - 类别: {r['category']}")
                lines.append(f"  - 建议操作: {r['action']}")
                lines.append(f"  - 理由: {r['reason']}")
                lines.append("")

    # 自动清理资产
    auto_cleanup = [r for r in results if r["action"] == "自动清理"]
    if auto_cleanup:
        lines.append("## 自动清理资产\n")
        lines.append("以下资产可自动清理，无需确认：\n")
        for r in auto_cleanup:
            lines.append(f"- {r['path']} ({r['reason']})")
        lines.append("")

    # 保留资产
    keep = [r for r in results if r["action"] == "保留"]
    if keep:
        lines.append("## 保留资产\n")
        lines.append("以下资产当前保留：\n")
        for r in keep:
            lines.append(f"- {r['path']} ({r['reason']})")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="扫描过期测试资产")
    parser.add_argument("--root", required=True, help="仓库根目录")
    parser.add_argument("--dry-run", action="store_true", default=True, help="仅输出不执行（默认启用）")
    parser.add_argument("--output", help="输出报告到文件")
    parser.add_argument("--no-dry-run", action="store_true", help="实际执行清理（需要用户确认）")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    dry_run = not args.no_dry_run

    print(f"扫描仓库: {repo_root}")
    print(f"模式: {'DRY RUN (仅扫描)' if dry_run else '实际执行'}")
    print()

    results = scan(repo_root, dry_run=dry_run)
    report = generate_report(results, repo_root)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"报告已写入: {output_path}")
    else:
        print(report)

    # 汇总
    cleanup_count = sum(1 for r in results if r["action"] in ("待确认清理", "自动清理"))
    print(f"\n总计: {len(results)} 个资产, {cleanup_count} 个需要清理")

    return 0


if __name__ == "__main__":
    sys.exit(main())
