"""CLI init 与只读 check 真实行为测试。"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CLI = ROOT / "package-structure-rules" / "scripts" / "placement_catalog.py"
BOOTSTRAP = ROOT / "project-rule-file-bootstrap-rules" / "scripts" / "bootstrap_agents.sh"
GIT_BASH = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "bin" / "bash.exe"


def run(*args):
    """调用本地 CLI 并返回不抛异常的进程结果。

    [参数] args：传递给 CLI 的子命令参数。
    [返回] CompletedProcess：包含退出码、标准输出和标准错误。
    最近修改时间: 2026-07-28 22:40:00 明确初始化和检查测试共享的本地执行入口。
    """
    return subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)


def git_bash_path(path):
    """将 Windows 绝对路径转换为 Git Bash 可识别的挂载路径。

    [参数] path：待传给 Git Bash 的本地路径。
    [返回] str：Git Bash 使用的盘符挂载绝对路径。
    最近修改时间: 2026-07-29 23:59:00 补齐双平台 bootstrap 测试辅助函数的注释契约。
    """
    # 1. 先解析真实绝对路径，再转换盘符和分隔符以保持 Git Bash 调用一致。
    resolved = path.resolve()
    return f"/{resolved.drive[0].lower()}{resolved.as_posix()[2:]}"


class InitCheckTests(unittest.TestCase):
    def test_init_creates_required_and_explicit_enabled_paths_only(self):
        """确认 init 只创建必需目录和显式启用的根 utils 工具包。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 23:45:00 增加必需双平台规则文件的初始化断言。
        """
        # 1. 启用单个服务发现包，确认 init 不批量创建其他条件目录。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run("init", "--project-kind", "backend", "--root", str(root), "--enable", "backend.utils.discovery.polaris")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((root / "config" / "yaml").is_dir())
            for filename in ("AGENTS.md", "CLAUDE.md", "PROJECT_CURRENT.md", "PROJECT_MEMORY.md", "PROJECT_HISTORY.md"):
                self.assertTrue((root / filename).is_file())
            self.assertEqual((root / "AGENTS.md").read_bytes(), (root / "CLAUDE.md").read_bytes())
            self.assertFalse((root / "PROJECT_STYLE.md").exists())
            self.assertTrue((root / "utils" / "discovery" / "polaris").is_dir())
            self.assertFalse((root / "utils" / "discovery" / "nacos").exists())

    def test_init_creates_project_style_only_when_explicitly_enabled(self):
        """确认条件 PROJECT_STYLE 文件不会随必需根文件被批量创建。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 23:00:00 新增条件根治理文件初始化断言。
        """
        # 1. 仅显式启用长期风格文件，确保 init 不把其他条件目录一并创建。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run("init", "--project-kind", "backend", "--root", str(root), "--enable", "backend.root.project-style")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((root / "PROJECT_STYLE.md").is_file())
            self.assertFalse((root / "utils").exists())

    def test_init_creates_matched_rule_files_for_all_project_kinds(self):
        """确认三类项目初始化都会创建同内容的双平台规则文件。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 23:45:00 新增 fullstack、backend、frontend 根文件初始化断言。
        """
        # 1. 对三种项目骨架逐一初始化，确认目录规则只创建位置且双文件字节相同。
        for project_kind in ("fullstack", "backend", "frontend"):
            with self.subTest(project_kind=project_kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                result = run("init", "--project-kind", project_kind, "--root", str(root))
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertTrue((root / "AGENTS.md").is_file())
                self.assertTrue((root / "CLAUDE.md").is_file())
                self.assertEqual((root / "AGENTS.md").read_bytes(), (root / "CLAUDE.md").read_bytes())

    def test_bootstrap_both_uses_agents_as_claude_source(self):
        """确认双平台自举始终以 AGENTS.md 覆盖同步 CLAUDE.md。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 23:55:00 新增双平台规则文件同步与幂等行为断言。
        """
        # 1. 构造两份不同的规则正文，验证显式 both 模式仅以 AGENTS.md 为唯一正文源。
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(GIT_BASH.is_file(), "缺少 Git for Windows Bash，无法验证 bootstrap 脚本")
            root = Path(directory)
            agents = root / "AGENTS.md"
            claude = root / "CLAUDE.md"
            agents.write_text("# Codex 规则\n", encoding="utf-8")
            claude.write_text("# Claude 漂移规则\n", encoding="utf-8")
            result = subprocess.run(
                [str(GIT_BASH), git_bash_path(BOOTSTRAP), "--repo", git_bash_path(root), "--target", "both"],
                cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(agents.read_bytes(), claude.read_bytes())

            # 2. 重复执行不得重新制造正文差异或改变已同步的规则文件。
            before = agents.read_bytes()
            retry = subprocess.run(
                [str(GIT_BASH), git_bash_path(BOOTSTRAP), "--repo", git_bash_path(root), "--target", "both"],
                cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False,
            )
            self.assertEqual(0, retry.returncode, retry.stderr)
            self.assertEqual(before, agents.read_bytes())
            self.assertEqual(agents.read_bytes(), claude.read_bytes())

    def test_init_creates_explicit_ip_package_only(self):
        """确认 init 只在显式启用时创建 IP 技术工具包。

        [参数] self 为 unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 00:00:00 新增 IP 工具包初始化正反向断言。
        """
        # 1. 启用 IP 工具包，确认 init 不顺带创建其他条件工具目录。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run("init", "--project-kind", "backend", "--root", str(root), "--enable", "backend.utils.ip")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((root / "utils" / "ip").is_dir())
            self.assertFalse((root / "utils" / "time").exists())

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

    def test_strict_rejects_mismatched_rule_files_without_writing(self):
        """确认 strict 只读拒绝同根双平台规则文件正文漂移。

        [参数] self：unittest 测试实例。
        [返回] 无。
        最近修改时间: 2026-07-29 23:45:00 新增 AGENTS.md 与 CLAUDE.md 内容一致性断言。
        """
        # 1. 先构造不一致正文并比较检查前后哈希，确认 strict 不会自动覆盖用户规则。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("# 共同规则\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("# 漂移规则\n", encoding="utf-8")
            before = json.loads(run("hash", "--root", str(root)).stdout)["sha256"]
            rejected = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "strict")
            after = json.loads(run("hash", "--root", str(root)).stdout)["sha256"]
            self.assertEqual(2, rejected.returncode)
            self.assertEqual(before, after)
            self.assertIn("CLAUDE.md 必须与 AGENTS.md 一致", rejected.stdout)

            # 2. 用户自行统一正文后，检查必须放行而不要求额外目录或迁移操作。
            (root / "CLAUDE.md").write_text("# 共同规则\n", encoding="utf-8")
            accepted = run("check", "--root", str(root), "--project-kind", "backend", "--language", "go", "--policy", "strict")
            self.assertEqual(0, accepted.returncode, accepted.stdout)

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
        最近修改时间: 2026-07-29 00:00:00 将 IP 技术工具包纳入根 utils 正向边界断言。
        """
        # 1. 根 utils 只包含工具包子目录及其代码文件，不能触发根目录文件或非法服务发现子目录错误。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for package, filename in (
                ("utils/time", "format.go"),
                ("utils/cron", "scheduler.go"),
                ("utils/ip", "address.go"),
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
