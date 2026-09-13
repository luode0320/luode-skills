#!/usr/bin/env python3
"""
__pycache__ 自动清理脚本

递归删除 test/ 目录下所有 __pycache__/ 目录。
支持 --dry-run 模式预览。

用法:
    python test-strategy-rules/scripts/cleanup_pycache.py --root <repo_root> [--dry-run]
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def find_pycache_dirs(root: Path) -> list[Path]:
    """查找 test/ 下所有 __pycache__ 目录"""
    test_dir = root / "test"
    if not test_dir.exists():
        print(f"test/ 目录不存在: {test_dir}")
        return []

    pycache_dirs = []
    for entry in test_dir.rglob("__pycache__"):
        if entry.is_dir():
            pycache_dirs.append(entry)
    return sorted(pycache_dirs)


def get_size(path: Path) -> int:
    """递归计算目录大小"""
    total = 0
    for entry in path.rglob("*"):
        if entry.is_file():
            total += entry.stat().st_size
    return total


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / 1024 / 1024:.1f}MB"


def main():
    parser = argparse.ArgumentParser(description="清理 test/ 下 __pycache__ 目录")
    parser.add_argument("--root", required=True, help="仓库根目录")
    parser.add_argument("--dry-run", action="store_true", default=True, help="仅预览不执行（默认启用）")
    parser.add_argument("--no-dry-run", action="store_true", help="实际执行清理")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    dry_run = not args.no_dry_run

    pycache_dirs = find_pycache_dirs(root)

    if not pycache_dirs:
        print("未找到 __pycache__ 目录，无需清理。")
        return 0

    total_size = sum(get_size(d) for d in pycache_dirs)
    total_count = len(pycache_dirs)

    print(f"找到 {total_count} 个 __pycache__ 目录，共 {format_size(total_size)}")
    print()

    if dry_run:
        print("=== DRY RUN - 以下目录将被清理 ===")
        for d in pycache_dirs:
            size = get_size(d)
            rel = d.relative_to(root).as_posix()
            print(f"  {rel} ({format_size(size)})")
        print()
        print(f"总计: {total_count} 个目录, {format_size(total_size)} 空间可释放")
        print("使用 --no-dry-run 实际执行清理")
    else:
        print("正在清理...")
        freed = 0
        removed = 0
        for d in pycache_dirs:
            try:
                size = get_size(d)
                rel = d.relative_to(root).as_posix()
                shutil.rmtree(d)
                print(f"  ✓ {rel} ({format_size(size)})")
                freed += size
                removed += 1
            except Exception as e:
                rel = d.relative_to(root).as_posix()
                print(f"  ✗ {rel}: {e}")

        print()
        print(f"清理完成: 删除 {removed}/{total_count} 个目录, 释放 {format_size(freed)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
