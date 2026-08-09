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


if __name__ == "__main__":
    unittest.main()
