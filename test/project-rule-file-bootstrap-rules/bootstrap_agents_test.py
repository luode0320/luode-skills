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


    def test_commit_implies_push_extra_is_scoped_to_owner_repo(self) -> None:
        """验证「提交即推送」项目专属补充不会被通用自举扩散到其他仓库。

        [参数] 无
        [返回] 无；断言失败时由 unittest 抛出异常。
        最近修改时间：2026-10-01 17:52:00；覆盖受管通用章节混入单仓库授权默认值的回归。
        """

        # 1. 归属仓库命中 slug 时必须注入项目专属补充。
        extra = "本项目（luode-skills）默认「提交即推送」"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "luode-skills"
            root.mkdir()
            subprocess.run(
                [BASH, git_bash_path(SCRIPT), "--repo", git_bash_path(root), "--target", "both"],
                capture_output=True,
                check=True,
                cwd=ROOT,
                text=True,
                encoding="utf-8",
                env=os.environ.copy(),
            )
            self.assertIn(extra, (root / "AGENTS.md").read_text(encoding="utf-8"))

        # 2. 其他仓库必须保持通用正文，不得继承该默认授权。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "some-other-project"
            root.mkdir()
            subprocess.run(
                [BASH, git_bash_path(SCRIPT), "--repo", git_bash_path(root), "--target", "both"],
                capture_output=True,
                check=True,
                cwd=ROOT,
                text=True,
                encoding="utf-8",
                env=os.environ.copy(),
            )
            agents = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertNotIn(extra, agents)
            self.assertIn("严禁自动提交 Git", agents)


if __name__ == "__main__":
    unittest.main()
