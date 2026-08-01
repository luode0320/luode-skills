"""递归执行根 test 目录中所有 *_test.py 测试。"""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


TEST_ROOT = Path(__file__).resolve().parent


def test_directories() -> list[Path]:
    """返回直接包含 *_test.py 的目录，避免测试发现依赖包目录。"""
    return sorted({path.parent for path in TEST_ROOT.rglob("*_test.py")})


def main() -> int:
    """运行全部根测试并返回进程退出码。"""
    # 1. 按目录发现测试，确保未添加 __init__.py 的镜像目录也能递归执行。
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for directory in test_directories():
        suite.addTests(loader.discover(str(directory), pattern="*_test.py"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return int(not result.wasSuccessful())


if __name__ == "__main__":
    sys.exit(main())
