"""Git 提交 pre gate 测试的共用夹具。"""

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


class GateTestCase(unittest.TestCase):
    """在隔离临时仓库中执行真实 gate 脚本的基类。"""

    # 宿主已有 ripgrep 时直接复用：通过 PATH 注入 shim 再经 shebang 调起原生解释器，
    # 会受 MSYS /tmp 与盘符路径转换影响而失败，仅在缺少宿主 rg 时才回退到内置 shim。
    HOST_RG = shutil.which("rg")

    def run_gate(
        self, *, title: str, files: dict[str, str], fake_node: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        """在临时 Git 仓库中 staged 指定文件并执行真实 gate 脚本。

        [参数] title: 提交标题；files: 临时仓库中的 staged 文件及内容；
               fake_node: 非空时在 PATH 前置同内容的 node 桩，用于模拟工具链异常。
        [返回] subprocess.CompletedProcess[str]：gate 执行结果。
        最近修改时间：2026-10-22 10:40:00；支持注入失效 node 桩验证工具链异常分支。
        """
        with tempfile.TemporaryDirectory(dir=self.temp_root()) as directory:
            root = Path(directory)

            # 1. 准备隔离的 Git 仓库、README 日志与 rg 依赖。
            shutil.copy2(GATE_SCRIPT, root / "pre_commit_gate.sh")
            if self.HOST_RG is None:
                self.write_rg_shim(root)
            if fake_node is not None:
                self.write_file(root, "fakebin/node", fake_node)
                (root / "fakebin" / "node").chmod(0o755)
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
                env=self.gate_env(root, fake_node=fake_node is not None),
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

    def gate_env(self, root: Path, *, fake_node: bool = False) -> dict[str, str]:
        """让临时仓库优先使用测试内置 rg shim，按需前置 node 桩。

        [参数] root: 临时仓库根目录；fake_node: 是否把同目录 node 桩放到 PATH 最前。
        [返回] dict[str, str]：注入 shim 路径后的环境变量。
        最近修改时间：2026-10-22 10:40:00；新增 node 桩注入以验证工具链异常分支。
        """
        # 1. 复制当前环境，避免测试修改宿主进程变量。
        env = os.environ.copy()

        # 2. 使用 Windows PATH 语法注入目录，由 Git Bash 负责转换路径。
        prefixes = [str(root)]
        if fake_node:
            prefixes.insert(0, str(root / "fakebin"))
        env["PATH"] = os.pathsep.join([*prefixes, env.get("PATH", "")])
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
