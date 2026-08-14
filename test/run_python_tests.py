"""递归执行根 test 目录中所有 *_test.py 测试。"""

from __future__ import annotations

from pathlib import Path
import importlib.util
import sys
import unittest


TEST_ROOT = Path(__file__).resolve().parent


def test_directories() -> list[Path]:
    """返回直接包含 *_test.py 的目录，避免测试发现依赖包目录。"""
    return sorted({path.parent for path in TEST_ROOT.rglob("*_test.py")})


def load_test_file(path: Path) -> None:
    """显式加载单个测试文件，不要求镜像目录可导入。"""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"unable to load test module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)


def main() -> int:
    """运行全部根测试并返回进程退出码。"""
    # 1. 显式加载每个 *_test.py，确保未添加 __init__.py 的镜像目录也能递归执行。
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for directory in test_directories():
        for path in sorted(directory.glob("*_test.py")):
            load_test_file(path)
            suite.addTests(loader.loadTestsFromModule(sys.modules[path.stem]))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return int(not result.wasSuccessful())


if __name__ == "__main__":
    sys.exit(main())
