from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "project-rule-file-bootstrap-rules" / "scripts" / "bootstrap_agents.sh"
BASH = next(
    (
        str(candidate)
        for candidate in (
            Path(r"C:\\Program Files\\Git\\bin\\bash.exe"),
            Path(r"C:\\Program Files\\Git\\usr\\bin\\bash.exe"),
        )
        if candidate.exists()
    ),
    shutil.which("bash") or "bash",
)
SKIP_MANAGED_SECTIONS_MARKER = "<!-- bootstrap-agents:skip-managed-sections -->"


def git_bash_path(path: Path) -> str:
    """把 Windows 路径转换成 Git Bash 可以执行的盘符路径。"""
    resolved = path.resolve()
    return f"/{resolved.drive[0].lower()}{resolved.as_posix()[2:]}"


class BootstrapAgentsTests(unittest.TestCase):
    def test_generated_rules_allow_persistence_and_forbid_output_echo(self) -> None:
        """Bootstrap 必须生成持久化允许与过程性输出脱敏的双边界。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "project.godot").write_text("[application]\nconfig/name=\"fixture\"\n", encoding="utf-8")
            result = subprocess.run(
                [BASH, git_bash_path(SCRIPT), "--repo", git_bash_path(root), "--target", "both"],
                capture_output=True,
                check=False,
                cwd=ROOT,
                text=True,
                encoding="utf-8",
                env=os.environ.copy(),
            )

            self.assertEqual(0, result.returncode, result.stderr)
            agents = (root / "AGENTS.md").read_text(encoding="utf-8")
            claude = (root / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertEqual(agents, claude)
            self.assertIn("有意持久化", agents)
            self.assertIn("过程性输出中回显", agents)
            self.assertNotIn("禁止将真实 API key、token、密码、私钥、连接串原值或其他敏感配置写入代码、文档、日志、输出或 Git 提交", agents)

    def test_subdirectory_skip_marker_keeps_isolated_rules_untouched(self) -> None:
        """子目录规则文件含跳过标记时逐文件打印跳过原因且字节不变，无标记子目录与根目录照常同步，重跑幂等。

        判据防止跳过标记失效后精简规则文件被补全成根规则副本、跳过时静默无输出，以及根目录误认标记而停止同步。
        副作用：只在临时目录内运行自举脚本，用例结束后目录自动删除。
        最近修改时间: 2026-10-08 11:19:43 新增, 覆盖子目录跳过标记的跳过提示、字节不变与幂等
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # 1. 构造带标记的根目录文件、带标记的隔离子目录文件（LF 与带首尾空白的 CRLF 各一份）和无标记的普通子目录文件
            (root / "isolated").mkdir()
            (root / "plain").mkdir()
            (root / "AGENTS.md").write_bytes(f"# 根规则\n{SKIP_MANAGED_SECTIONS_MARKER}\n".encode("utf-8"))
            (root / "plain" / "AGENTS.md").write_bytes("# 普通子目录规则\n".encode("utf-8"))
            skipped = {
                root / "isolated" / "AGENTS.md": f"# 隔离规则\n{SKIP_MANAGED_SECTIONS_MARKER}\n\n## 本文件的定位\n".encode("utf-8"),
                root / "isolated" / "CLAUDE.md": f"# 隔离规则\r\n  {SKIP_MANAGED_SECTIONS_MARKER}\t\r\n\r\n## 本文件的定位\r\n".encode("utf-8"),
            }
            for path, content in skipped.items():
                path.write_bytes(content)

            # 2. 连续运行两次自举脚本
            runs = []
            for _ in range(2):
                # 2.1 运行一次自举脚本
                result = subprocess.run(
                    [BASH, git_bash_path(SCRIPT), "--repo", git_bash_path(root), "--target", "both"],
                    capture_output=True,
                    check=False,
                    cwd=ROOT,
                    text=True,
                    encoding="utf-8",
                    env=os.environ.copy(),
                )
                # 2.2 记录本次运行后全部文件的字节快照
                runs.append((result, {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}))

            # 3. 每次运行都只对两份隔离文件逐个打印跳过原因，且两次快照一致
            for result, _ in runs:
                self.assertEqual(0, result.returncode, result.stderr)
                skip_lines = [line for line in result.stdout.splitlines() if line.startswith("[INFO] 已跳过: ")]
                self.assertEqual(len(skipped), len(skip_lines), result.stdout)
                for path in skipped:
                    self.assertTrue(any(f"/isolated/{path.name}（" in line for line in skip_lines), result.stdout)
            self.assertEqual(runs[0][1], runs[1][1])

            # 4. 隔离文件字节不变；普通子目录与根目录同步出相同的受管章节，根目录两份规则文件一致
            for path, content in skipped.items():
                self.assertEqual(content, path.read_bytes())
            headings = {
                path: [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("## ")]
                for path in (root / "AGENTS.md", root / "plain" / "AGENTS.md")
            }
            self.assertTrue(headings[root / "AGENTS.md"])
            self.assertEqual(headings[root / "AGENTS.md"], headings[root / "plain" / "AGENTS.md"])
            self.assertEqual((root / "AGENTS.md").read_bytes(), (root / "CLAUDE.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
