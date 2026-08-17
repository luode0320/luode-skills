"""生产代码测试污染扫描脚本的判定回归。"""

from __future__ import annotations

from pathlib import Path
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "test-strategy-rules" / "scripts" / "scan_test_pollution.py"


def load_scanner():
    """按文件路径加载扫描脚本，不要求镜像目录可导入。

    [参数] 无。
    [返回] module：已加载的 scan_test_pollution 模块。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描回归。
    """
    spec = importlib.util.spec_from_file_location("scan_test_pollution", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"unable to load scanner: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    # dataclass 装饰器会回查 sys.modules，动态加载必须先注册再执行。
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_project(root: Path, *, with_prod_caller: bool, allowlist: str | None = None) -> None:
    """构造最小 Go 项目样本，覆盖污染与正常两种引用面。

    [参数] root：临时项目根目录；with_prod_caller：生产侧是否存在调用方；allowlist：豁免登记内容。
    [返回] None。
    最近修改时间: 2026-08-17 新增生产代码测试污染扫描回归。
    """
    # 1. 生产文件：EnsureSeed 与 seedAddressBlacklist 复刻真实污染形态。
    (root / "repository").mkdir(parents=True)
    (root / "test" / "repository").mkdir(parents=True)
    (root / "repository" / "repo.go").write_text(
        "package repository\n"
        "\n"
        "var seedAddressBlacklist = []string{\"0xaaa\"}\n"
        "\n"
        "func EnsureSeed() []string {\n"
        "    return seedAddressBlacklist\n"
        "}\n"
        "\n"
        "func ListBlacklist() []string {\n"
        "    return nil\n"
        "}\n",
        encoding="utf-8",
    )

    # 2. 测试文件：只有测试调用 EnsureSeed 与 seedAddressBlacklist。
    (root / "test" / "repository" / "repo_test.go").write_text(
        "package repository_test\n"
        "\n"
        "import \"example.com/scan/repository\"\n"
        "\n"
        "func probe() {\n"
        "    _ = repository.EnsureSeed()\n"
        "    _ = repository.ListBlacklist()\n"
        "}\n",
        encoding="utf-8",
    )

    # 3. 生产入口始终存在：ListBlacklist 作为正常对照组，恒有生产调用方；
    #    with_prod_caller 只决定生产侧是否也调用 EnsureSeed。
    seed_call = "    _ = repository.EnsureSeed()\n" if with_prod_caller else ""
    (root / "service").mkdir()
    (root / "service" / "service.go").write_text(
        "package service\n"
        "\n"
        "import \"example.com/scan/repository\"\n"
        "\n"
        "func Boot() {\n"
        f"{seed_call}"
        "    _ = repository.ListBlacklist()\n"
        "}\n",
        encoding="utf-8",
    )

    if allowlist is not None:
        (root / ".test-pollution-allowlist").write_text(allowlist, encoding="utf-8")


class ScanTestPollutionTests(unittest.TestCase):
    """验证引用面判据、豁免登记与仅测试可达分支的判定结果。"""

    @classmethod
    def setUpClass(cls) -> None:
        """加载被测脚本并确认 rg 可用。"""
        if shutil.which("rg") is None:
            raise unittest.SkipTest("未找到 rg，无法统计符号引用面")
        cls.scanner = load_scanner()

    def verdicts_of(self, root: Path) -> dict[str, str]:
        """执行扫描并返回符号到判定的映射。

        [参数] root：临时项目根目录。
        [返回] dict[str, str]：符号名到判定结论的映射。
        最近修改时间: 2026-08-17 新增生产代码测试污染扫描回归。
        """
        result = self.scanner.scan(root)
        return {item.symbol: item.verdict for item in result.findings}

    def test_symbol_only_referenced_by_test_is_pollution(self) -> None:
        """生产符号只被 test/ 引用时判定为 POLLUTION，有生产调用方的对照组不受影响。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_project(root, with_prod_caller=False)
            verdicts = self.verdicts_of(root)
            result = self.scanner.scan(root)

        self.assertEqual(verdicts.get("EnsureSeed"), "POLLUTION")
        self.assertNotIn("ListBlacklist", verdicts)
        self.assertTrue(result.blocking())

    def test_data_referenced_only_by_polluted_symbol_cascades(self) -> None:
        """只被污染函数引用的静态数据按级联污染判定，复刻 seedAddressBlacklist 形态。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_project(root, with_prod_caller=False)
            result = self.scanner.scan(root)

        cascaded = [item for item in result.blocking() if item.symbol == "seedAddressBlacklist"]
        self.assertEqual(len(cascaded), 1, [vars(item) for item in result.findings])
        self.assertIn("级联污染", cascaded[0].reason)

    def test_symbol_with_production_caller_passes(self) -> None:
        """生产侧存在调用方时不判污染，扫描通过。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_project(root, with_prod_caller=True)
            result = self.scanner.scan(root)

        self.assertEqual(result.blocking(), [])

    def test_allowlist_downgrades_pollution_to_exempted(self) -> None:
        """已登记豁免的符号降级为 EXEMPTED 且不再阻断。"""
        allowlist = (
            "repository/repo.go::EnsureSeed  # 反射调用，无静态调用点\n"
            "repository/repo.go::seedAddressBlacklist  # REQ-DEMO-001 待接线\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_project(root, with_prod_caller=False, allowlist=allowlist)
            verdicts = self.verdicts_of(root)
            result = self.scanner.scan(root)

        self.assertEqual(verdicts.get("EnsureSeed"), "EXEMPTED")
        self.assertEqual(verdicts.get("seedAddressBlacklist"), "EXEMPTED")
        self.assertEqual(result.blocking(), [])

    def test_runtime_test_branch_is_pollution(self) -> None:
        """生产文件中的仅测试可达分支判定为 POLLUTION。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_project(root, with_prod_caller=True)
            (root / "service" / "gate.go").write_text(
                "package service\n"
                "\n"
                "func Gate(env string) bool {\n"
                "    if env == \"test\" {\n"
                "        return true\n"
                "    }\n"
                "    return false\n"
                "}\n",
                encoding="utf-8",
            )
            result = self.scanner.scan(root)

        reasons = [item.reason for item in result.blocking()]
        self.assertTrue(any("P4" in reason for reason in reasons), reasons)

    def test_diff_only_covers_untracked_new_directory(self) -> None:
        """--diff-only 必须展开未跟踪新目录，否则新增生产文件会被漏扫。"""
        git = shutil.which("git")
        if git is None:
            self.skipTest("未找到 git，无法验证增量扫描范围")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_project(root, with_prod_caller=False)
            # 1. 建库但不 add，repository/ 与 service/ 都处于未跟踪新目录状态。
            for command in (["init"], ["config", "user.email", "t@example.com"], ["config", "user.name", "t"]):
                subprocess.run([git, *command], cwd=root, capture_output=True, check=True, text=True)
            result = self.scanner.scan(root, diff_only=True)

        symbols = {item.symbol for item in result.blocking()}
        self.assertIn("EnsureSeed", symbols)

    def test_main_returns_nonzero_on_pollution(self) -> None:
        """命令行入口在存在阻断级污染时返回退出码 1。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_project(root, with_prod_caller=False)
            code = self.scanner.main(["--root", str(root)])

        self.assertEqual(code, 1)

    def test_main_returns_zero_when_clean(self) -> None:
        """命令行入口在无污染时返回退出码 0。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_project(root, with_prod_caller=True)
            code = self.scanner.main(["--root", str(root)])

        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
