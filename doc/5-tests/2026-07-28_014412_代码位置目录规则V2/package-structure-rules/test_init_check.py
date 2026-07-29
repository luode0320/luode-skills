"""CLI init 与只读 check 真实行为测试。"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLI = ROOT / "package-structure-rules" / "scripts" / "placement_catalog.py"


def run(*args):
    """调用本地 CLI 并返回不抛异常的进程结果。

    [参数] args：传递给 CLI 的子命令参数。
    [返回] CompletedProcess：包含退出码、标准输出和标准错误。
    最近修改时间: 2026-07-28 22:40:00 明确初始化和检查测试共享的本地执行入口。
    """
    return subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)


class InitCheckTests(unittest.TestCase):
    def test_init_creates_required_and_explicit_enabled_paths_only(self):
        """确认 init 只创建必需目录和显式启用的根 utils 工具包。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 更新服务发现启用 ID 与根目录断言。
        """
        # 1. 启用单个服务发现包，确认 init 不批量创建其他条件目录。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run("init", "--project-kind", "backend", "--root", str(root), "--enable", "backend.utils.discovery.polaris")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((root / "config" / "yaml").is_dir())
            self.assertTrue((root / "utils" / "discovery" / "polaris").is_dir())
            self.assertFalse((root / "utils" / "discovery" / "nacos").exists())

    def test_strict_rejects_mixed_content_without_writing(self):
        """确认 strict 拒绝根 utils 文件、旧根 util 与源码根 util 子目录。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 补齐 utils 与源码根 util 的负向 fixture。
        """
        # 1. 构造工具、源码根、迁移和 SQL 的正负混合样本。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "utils" / "time").mkdir(parents=True)
            (root / "utils" / "time" / "format.go").write_text("package time", encoding="utf-8")
            (root / "utils" / "direct.go").write_text("package utils", encoding="utf-8")
            (root / "util").mkdir()
            (root / "util" / "legacy.go").write_text("package util", encoding="utf-8")
            (root / "internal" / "util").mkdir(parents=True)
            (root / "internal" / "util" / "request_context.go").write_text("package util", encoding="utf-8")
            (root / "internal" / "util" / "nested").mkdir()
            (root / "internal" / "util" / "nested" / "bad.go").write_text("package util", encoding="utf-8")
            (root / "database" / "migration" / "field" / "create").mkdir(parents=True)
            (root / "database" / "migration" / "field" / "create" / "bad.sql").write_text("select 1;", encoding="utf-8")
            (root / "database" / "sql" / "ddl").mkdir(parents=True)
            (root / "database" / "sql" / "ddl" / "bad.go").write_text("package ddl", encoding="utf-8")
            # 2. 比较检查前后哈希，证明 strict 只报告而不写入 fixture。
            before = json.loads(run("hash", "--root", str(root)).stdout)["sha256"]
            result = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "strict")
            after = json.loads(run("hash", "--root", str(root)).stdout)["sha256"]
            self.assertEqual(2, result.returncode)
            self.assertEqual(before, after)
            errors = "\n".join(json.loads(result.stdout)["errors"])
            self.assertIn("根 utils 禁止直接文件", errors)
            self.assertIn("源码根 util 禁止子目录", errors)
            self.assertIn("禁止路径", errors)
            self.assertIn("自动迁移目录禁止 SQL 文件", errors)
            self.assertIn("独立 SQL 目录禁止生产源码", errors)

    def test_strict_accepts_four_language_source_util_files(self):
        """确认四种后端语言的源码根 util 允许直接存放本语言代码文件。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 新增四语言正向 source-util fixture。
        """
        # 1. 为每种语言创建只包含直接代码文件的源码根 util 样本。
        cases = (
            ("go", "internal/util", "helper.go"),
            ("java", "src/main/java/com/example/util", "Helper.java"),
            ("node", "src/util", "helper.ts"),
            ("python", "src/app/util", "helper.py"),
        )
        for language, directory_name, filename in cases:
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source_util = root / directory_name
                source_util.mkdir(parents=True)
                (source_util / filename).write_text("source", encoding="utf-8")
                result = run("check", "--root", str(root), "--project-kind", "backend", "--language", language, "--policy", "strict")
                self.assertEqual(0, result.returncode, result.stdout)

    def test_strict_accepts_utils_subpackages(self):
        """确认根 utils 的合法工具包子目录可通过严格检查。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 23:20:00 补齐根 utils 正向工具包边界断言。
        """
        # 1. 根 utils 只包含工具包子目录及其代码文件，不能触发根目录文件或非法服务发现子目录错误。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for package, filename in (
                ("utils/time", "format.go"),
                ("utils/cron", "scheduler.go"),
                ("utils/json", "codec.go"),
                ("utils/log", "logger.go"),
                ("utils/discovery/polaris", "register.go"),
                ("utils/discovery/nacos", "register.go"),
            ):
                package_root = root / package
                package_root.mkdir(parents=True)
                (package_root / filename).write_text("package utils", encoding="utf-8")
            result = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "strict")
            self.assertEqual(0, result.returncode, result.stdout)

    def test_init_creates_explicit_business_rpc_only(self):
        """确认业务域 RPC 只有显式域名与语言上下文时才会创建。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 23:55:00 新增按域初始化 RPC 的正反向断言。
        """
        # 1. 合法请求只能创建 Go users 域的 rpc，不得创建字面量占位目录或其他业务域。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run(
                "init", "--project-kind", "backend", "--root", str(root), "--enable", "backend.business-rpc",
                "--domain", "users", "--language", "go",
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((root / "internal" / "business" / "users" / "rpc").is_dir())
            self.assertFalse((root / "internal" / "business" / "<domain>").exists())

            invalid = run("init", "--project-kind", "backend", "--root", str(root), "--enable", "backend.business-rpc")
            self.assertEqual(2, invalid.returncode)
            self.assertIn("--domain", invalid.stdout)

    def test_strict_accepts_flat_business_rpc_files(self):
        """确认业务域 RPC 允许直接代码文件并拒绝继续建立子目录。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 23:55:00 新增扁平 JSON RPC 入口边界断言。
        """
        # 1. 先验证直接公开函数文件可通过，再验证私自分层会被 strict 拒绝。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rpc_root = root / "internal" / "business" / "users" / "rpc"
            rpc_root.mkdir(parents=True)
            (rpc_root / "get_profile.go").write_text("package rpc", encoding="utf-8")
            accepted = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "strict")
            self.assertEqual(0, accepted.returncode, accepted.stdout)

            nested = rpc_root / "private"
            nested.mkdir()
            (nested / "bad.go").write_text("package private", encoding="utf-8")
            rejected = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "strict")
            self.assertEqual(2, rejected.returncode)
            self.assertIn("业务域 rpc 禁止子目录", rejected.stdout)

    def test_strict_requires_backend_language_context(self):
        """确认后端 strict 必须明确语言，避免错误识别源码根 util。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 新增 strict 语言上下文缺失断言。
        """
        # 1. 不传语言执行后端 strict，确认 CLI 失败关闭而不猜测源码根。
        with tempfile.TemporaryDirectory() as directory:
            result = run("check", "--root", directory, "--project-kind", "backend", "--policy", "strict")
            self.assertEqual(2, result.returncode)
            self.assertIn("--language", result.stdout)

    def test_legacy_warns_without_failing(self):
        """确认 legacy 对旧根 util 仅告警且不产生 strict 错误。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-28 21:45:00 将兼容样本更新为旧根 util。
        """
        # 1. 旧根 util 在 legacy 下只能产生警告且不改写目录。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "util").mkdir()
            result = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "legacy")
            self.assertEqual(0, result.returncode)
            payload = json.loads(result.stdout)
            self.assertEqual([], payload["errors"])
            self.assertTrue(payload["warnings"])


if __name__ == "__main__":
    unittest.main()
