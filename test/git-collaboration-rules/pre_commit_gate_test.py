"""Git 提交 pre gate 回归测试。"""

from __future__ import annotations

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
GATE_SCRIPT = REPO_ROOT / "git-collaboration-rules" / "scripts" / "pre_commit_gate.sh"
BASH_EXECUTABLE = next(
    (
        str(candidate)
        for candidate in (
            Path(r"C:\Program Files\Git\bin\bash.exe"),
            Path(r"C:\Program Files\Git\usr\bin\bash.exe"),
        )
        if candidate.exists()
    ),
    shutil.which("bash") or "bash",
)


class PreCommitGateTests(unittest.TestCase):
    """验证按业务合并提交的 pre gate 边界。"""

    # 宿主已有 ripgrep 时直接复用：通过 PATH 注入 shim 再经 shebang 调起原生解释器，
    # 会受 MSYS /tmp 与盘符路径转换影响而失败，仅在缺少宿主 rg 时才回退到内置 shim。
    HOST_RG = shutil.which("rg")

    def test_business_scope_can_commit_together(self) -> None:
        """验证同一业务目标的实现、测试、文档与状态文件可同笔提交。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-10 17:20:00；覆盖按业务合并提交正例。
        """
        # 1. 构造同一业务目标的实现、可执行测试、流程文档与项目状态同步文件。
        result = self.run_gate(
            title="feat: [订单创建规则] 新增订单创建能力并同步流程文档",
            files={
                "src/order/create_order.py": "def create_order():\n    return True\n",
                "test/order/create_order_test.py": "import unittest\n",
                "doc/2-需求/2026-08-02_订单创建规则.md": "需求",
                "doc/3-实施/2026-08-02_订单创建规则_实施总览.md": "实施",
                "doc/5-tests/2026-08-02_订单创建规则/README.md": "测试说明",
                "doc/6-review/2026-08-02_订单创建规则_6-review.md": "STYLE: PASS",
                "PROJECT_CURRENT.md": "# 项目当前状态\n",
                "PROJECT_MEMORY.md": "# 项目长期记忆\n",
                "字典.md": "# 字典\n",
                "skill-dictionary/data.js": "export default {};\n",
            },
        )

        # 2. 按业务合并提交必须通过门禁，不再因跨域混提阻断。
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: pre-commit gate", result.stdout + result.stderr)

    def test_docs_and_executable_test_no_longer_blocked(self) -> None:
        """验证文档与可执行测试同笔提交不再被提交域门禁阻断。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-10 17:20:00；覆盖原提交域阻断规则被移除后的行为。
        """
        # 1. 构造流程文档和根 test 目录中的可执行测试。
        result = self.run_gate(
            title="docs: [订单创建规则] 更新需求实施记录并补充回归用例",
            files={
                "doc/2-需求/2026-08-02_订单创建规则.md": "需求",
                "test/order/create_order_test.py": "import unittest\n",
            },
        )

        # 2. 同一业务目标的文档与测试合并提交必须通过，且不再出现提交域阻断文案。
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("commit domains", result.stdout + result.stderr)

    def test_persisted_sentinel_does_not_block_or_echo(self) -> None:
        """代码、配置和普通文档中的 sentinel 不得被门禁阻断或回显。"""
        sentinel = "fixture-secret"
        result = self.run_gate(
            title="feat: [凭据边界] 更新持久化规则",
            files={
                "config/local.yaml": f"token: {sentinel}\\n",
                "src/config.py": f"TOKEN = '{sentinel}'\\n",
                "docs/config.md": f"token: {sentinel}\\n",
            },
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(sentinel, result.stdout + result.stderr)

    def test_go_test_outside_root_test_still_blocked(self) -> None:
        """验证 Go 测试落点约束未因合并提交而放宽。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-10 17:20:00；覆盖 Go 测试落点阻断仍生效。
        """
        # 1. 构造根 test/ 之外的新增 Go 测试文件。
        result = self.run_gate(
            title="feat: [订单创建] 新增订单创建能力",
            files={
                "internal/order/create_order_test.go": "package order\n",
            },
        )

        # 2. 落点违规必须继续阻断，退出码与原文案保持不变。
        self.assertEqual(result.returncode, 15, result.stdout + result.stderr)
        self.assertIn("BLOCK: staged *_test.go must be under root test/", result.stderr)

    def test_service_layer_root_file_still_blocked(self) -> None:
        """验证服务层根目录直落约束未因合并提交而放宽。

        [参数] 无。
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-09-10 17:20:00；覆盖服务层落点阻断仍生效。
        """
        # 1. 构造 internal/service 根目录直落的实现文件。
        result = self.run_gate(
            title="feat: [订单创建] 新增订单创建能力",
            files={
                "internal/service/create_order.go": "package service\n",
            },
        )

        # 2. 落点违规必须继续阻断，退出码与原文案保持不变。
        self.assertEqual(result.returncode, 16, result.stdout + result.stderr)
        self.assertIn("BLOCK: staged file in internal/service/*.go root", result.stderr)

    def run_gate(self, *, title: str, files: dict[str, str]) -> subprocess.CompletedProcess[str]:
        """在临时 Git 仓库中 staged 指定文件并执行真实 gate 脚本。

        [参数] title: 提交标题；files: 临时仓库中的 staged 文件及内容。
        [返回] subprocess.CompletedProcess[str]：gate 执行结果。
        最近修改时间：2026-08-02 17:18:00；固定 Git Bash 来源并补齐临时工具路径。
        """
        with tempfile.TemporaryDirectory(dir=self.temp_root()) as directory:
            root = Path(directory)

            # 1. 准备隔离的 Git 仓库、README 日志与 rg 依赖。
            shutil.copy2(GATE_SCRIPT, root / "pre_commit_gate.sh")
            if self.HOST_RG is None:
                self.write_rg_shim(root)
            self._run_command(["git", "init"], root)
            self._run_command(["git", "config", "user.email", "test@example.invalid"], root)
            self._run_command(["git", "config", "user.name", "Pre Commit Gate Test"], root)
            self.write_file(root, "README.md", f"# fixture\n\n## 改动日志\n2026-08-02 16:35:00 {title}\n")
            for relative_path, content in files.items():
                self.write_file(root, relative_path, content)
            self._run_command(["git", "add", "--", "README.md", *files], root)

            # 2. 使用当前临时仓库环境执行真实 Shell gate。
            return subprocess.run(
                [BASH_EXECUTABLE, "pre_commit_gate.sh", title],
                cwd=root,
                capture_output=True,
                check=False,
                text=True,
                encoding="utf-8",
                env=self.gate_env(root),
            )

    def _run_command(self, command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        """执行命令并在失败时保留 stdout/stderr 便于定位。

        [参数] command: 待执行命令；cwd: 命令工作目录。
        [返回] subprocess.CompletedProcess[str]：命令执行结果。
        最近修改时间：2026-08-02 17:14:57；明确临时仓库命令的失败证据。
        """
        # 1. 失败命令直接抛出，保留捕获输出供 unittest 定位。
        return subprocess.run(command, cwd=cwd, capture_output=True, check=True, text=True, encoding="utf-8")

    def write_file(self, root: Path, relative_path: str, content: str) -> None:
        """按 UTF-8 写入临时仓库文件。

        [参数] root: 临时仓库根目录；relative_path: 相对路径；content: 文件内容。
        [返回] 无。
        最近修改时间：2026-08-02 17:14:57；保持测试夹具使用显式 UTF-8。
        """
        # 1. 先创建文件父目录，再以 UTF-8 写入夹具内容。
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def write_rg_shim(self, root: Path) -> None:
        """提供 gate 脚本所需的最小 rg 行过滤能力。

        [参数] root: 临时仓库根目录。
        [返回] 无。
        最近修改时间：2026-08-02 17:14:57；隔离测试对 ripgrep 的最小依赖。
        """
        # 1. 写入只覆盖当前 gate 用到的正则过滤参数。
        shim = root / "rg"
        shim.write_text(
            "#!/usr/bin/env python\n"
            "import re, sys\n"
            "args = sys.argv[1:]\n"
            "invert = False\n"
            "while args and args[0].startswith('-'):\n"
            "    if args[0] == '-P':\n"
            "        args.pop(0)\n"
            "    elif args[0] == '-v':\n"
            "        invert = True\n"
            "        args.pop(0)\n"
            "    else:\n"
            "        break\n"
            "pattern = args[0] if args else ''\n"
            "regex = re.compile(pattern)\n"
            "status = 1\n"
            "for raw_line in sys.stdin:\n"
            "    line = raw_line.rstrip('\\n')\n"
            "    matched = bool(regex.search(line))\n"
            "    if invert:\n"
            "        matched = not matched\n"
            "    if matched:\n"
            "        print(line)\n"
            "        status = 0\n"
            "sys.exit(status)\n",
            encoding="utf-8",
            newline="\n",
        )

        # 2. 设置 Git Bash 可执行权限，保证临时 PATH 能调用 shim。
        shim.chmod(0o755)

    def gate_env(self, root: Path) -> dict[str, str]:
        """让临时仓库优先使用测试内置 rg shim。

        [参数] root: 临时仓库根目录。
        [返回] dict[str, str]：注入 shim 路径后的环境变量。
        最近修改时间：2026-08-02 17:18:00；修正 Windows PATH 到 Git Bash 的映射。
        """
        # 1. 复制当前环境，避免测试修改宿主进程变量。
        env = os.environ.copy()

        # 2. 使用 Windows PATH 语法注入目录，由 Git Bash 负责转换路径。
        env["PATH"] = os.pathsep.join([str(root), env.get("PATH", "")])
        return env

    @staticmethod
    def temp_root() -> str:
        """返回 Git Bash 能正确映射的临时目录根。

        [参数] 无。
        [返回] str：可直接传给 `tempfile.TemporaryDirectory(dir=...)` 的目录。
        最近修改时间：2026-09-10 17:35:00；规避宿主 TMP=/tmp 被解析成 C:\\tmp 后脱离 Git Bash 路径映射的问题。
        """
        # 1. 宿主把 TEMP/TMP 设为 POSIX 风格路径（如 /tmp）时，Git Bash 会把该值
        #    解析成 C:\tmp，而 MSYS 启动原生 python.exe 时又会把 TEMP 转成用户临时目录；
        #    两边对 /tmp 的理解不一致，导致 shim 被解释器按不存在的路径打开。
        # 2. 这里不依赖环境变量，直接固定到用户临时目录，使宿主与 Git Bash 路径语义一致。
        if os.name == "nt":
            candidate = Path.home() / "AppData" / "Local" / "Temp"
            if candidate.is_dir():
                return str(candidate)
        return tempfile.gettempdir()


if __name__ == "__main__":
    unittest.main(verbosity=2)
