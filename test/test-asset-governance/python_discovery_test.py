"""根 test 目录的 Python 测试发现行为回归。"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class PythonDiscoveryTests(unittest.TestCase):
    """验证统一入口只发现 *_test.py。"""

    def test_unittest_discovers_suffix_named_tests_only(self) -> None:
        """unittest 入口必须发现 *_test.py 并忽略旧 test_*.py。"""
        # 1. 在临时目录放入一正一负两个命名样本，再走真实 unittest 发现命令。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "alpha_test.py").write_text(
                "import unittest\nclass Alpha(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(True)\n",
                encoding="utf-8",
            )
            (root / "test_legacy.py").write_text("raise RuntimeError('must not be imported')\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(root), "-p", "*_test.py", "-v"],
                capture_output=True,
                check=False,
                text=True,
                encoding="utf-8",
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("test_ok", result.stderr)
        self.assertNotIn("must not be imported", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
