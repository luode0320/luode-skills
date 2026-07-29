"""微业务脚手架 scaffold 子命令 crontask 目录改名回归测试。"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLI = ROOT / "micro-business-architecture-rules" / "scripts" / "micro_business.py"


def run(*args):
    """调用本地 CLI 并返回不抛异常的进程结果。

    [参数] args：传递给 CLI 的子命令参数。
    [返回] CompletedProcess：包含退出码、标准输出和标准错误。
    最近修改时间: 2026-07-29 16:20:54 新增 scaffold crontask 改名回归测试的本地调用入口。
    """
    return subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)


class ScaffoldCrontaskTests(unittest.TestCase):
    """验证 scaffold 创建的默认子目录已从 corntask 改名为 crontask。"""

    def test_scaffold_creates_crontask_not_corntask(self):
        """确认 scaffold 创建 crontask/ 子目录，且不再产生历史拼写 corntask/。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 16:20:54 新增 DEFAULT_SUBDIRS 改名后的正向断言。
        """
        # 1. 新建业务包骨架，确认真实创建的目录名已同步为 crontask。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run("scaffold", "orders", "--root", str(root), "--business-dir", "internal/business")
            self.assertEqual(0, result.returncode, result.stdout)
            business_pkg = root / "internal" / "business" / "orders"
            self.assertTrue((business_pkg / "crontask").is_dir())
            self.assertFalse((business_pkg / "corntask").exists())

    def test_scaffold_is_idempotent_for_crontask(self):
        """确认二次执行 scaffold 幂等，不重复创建、不报错。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 16:20:54 新增幂等性回归断言。
        """
        # 1. 连续执行两次 scaffold，确认第二次仍成功且不产生重复或异常。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = run("scaffold", "orders", "--root", str(root), "--business-dir", "internal/business")
            second = run("scaffold", "orders", "--root", str(root), "--business-dir", "internal/business")
            self.assertEqual(0, first.returncode, first.stdout)
            self.assertEqual(0, second.returncode, second.stdout)
            self.assertTrue((root / "internal" / "business" / "orders" / "crontask").is_dir())


if __name__ == "__main__":
    unittest.main()
