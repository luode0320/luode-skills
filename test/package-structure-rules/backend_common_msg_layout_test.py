"""验证 common/msg 国际化消息目录的唯一落点与前后端目录树同步。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "package-structure-rules" / "scripts" / "placement_catalog.py"
CATALOG = ROOT / "package-structure-rules" / "references" / "placement-catalog.yaml"


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """调用本地 Catalog CLI。

    [参数] arguments：CLI 子命令及参数。
    [返回] subprocess.CompletedProcess[str]：本地命令结果。
    最近修改时间: 2026-08-13 10:04:25 新增 common/msg 行为测试入口。
    """
    # 1. 通过当前 Python 解释器运行 CLI，保持测试与实际入口一致。
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), *arguments],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def strict_backend(root: Path, language: str = "go") -> subprocess.CompletedProcess[str]:
    """执行独立后端 strict 检查。

    [参数] root：临时项目根；language：待检查的后端语言。
    [返回] subprocess.CompletedProcess[str]：strict 检查结果。
    最近修改时间: 2026-08-13 10:04:25 新增 common/msg 严格策略断言入口。
    """
    # 1. 固定项目类型与 strict 策略，只切换当前语言样本。
    return run_cli(
        "check", "--root", str(root), "--project-kind", "backend",
        "--language", language, "--policy", "strict",
    )


class BackendCommonMsgLayoutTests(unittest.TestCase):
    """覆盖 common/msg 的 Catalog 唯一性、strict 边界和目录树同步。"""

    def test_catalog_query_returns_one_common_msg_entry(self):
        """Catalog 与 query 对国际化消息目录给出唯一位置。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-13 10:04:25 覆盖 msg 条目唯一路径与查询入口。
        """
        # 1. 先核对机器目录事实，确认 msg 只有一个规范位置。
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        entries = [entry for entry in catalog["entries"] if entry.get("artifact_kind") == "msg"]
        self.assertEqual(1, len(entries))
        self.assertEqual("common/msg", entries[0]["canonical_path"])
        self.assertIn("msg", catalog["allowed_children"]["common"])

        # 2. 再核对查询入口返回同一路径，避免 Catalog 与 CLI 口径漂移。
        result = run_cli("query", "--artifact", "msg")
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertEqual("common/msg", json.loads(result.stdout)["entry"]["canonical_path"])

    def test_strict_accepts_common_msg_source_and_still_rejects_unknown_child(self):
        """strict 放行 common/msg 源码，同时保持 common 子目录白名单封闭。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-13 10:04:25 覆盖 msg 放行与非法子目录拒绝。
        """
        with tempfile.TemporaryDirectory() as directory:
            # 1. 正向样本确认 msg 已被 allowed_children 放行。
            root = Path(directory)
            (root / "Dockerfile").touch()
            message = root / "common/msg/message.go"
            message.parent.mkdir(parents=True)
            message.touch()
            accepted = strict_backend(root)
            self.assertEqual(0, accepted.returncode, accepted.stdout)

            # 2. 负向样本确认白名单没有被放宽成任意 common 子目录。
            unknown = root / "common/unknown/x.go"
            unknown.parent.mkdir()
            unknown.touch()
            rejected = strict_backend(root)
            self.assertEqual(2, rejected.returncode, rejected.stdout)
            self.assertIn("非法子目录", rejected.stdout)

    def test_render_synchronizes_msg_in_backend_and_frontend_trees(self):
        """后端与前端目录树同时表达 msg，且国际化数据目录保持不变。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-13 10:04:25 覆盖前后端 msg 目录树同步。
        """
        # 1. 后端树里 msg 位于根 common/ 下，文案数据仍在 resources/i18n/。
        backend = run_cli("render", "--project-kind", "backend")
        self.assertEqual(0, backend.returncode, backend.stderr)
        self.assertIn("│   ├── msg/", backend.stdout)
        self.assertIn("│   ├── i18n/", backend.stdout)

        # 2. 前端树里 msg 位于 src/common/ 下，词条数据仍在 src/locales/。
        frontend = run_cli("render", "--project-kind", "frontend")
        self.assertEqual(0, frontend.returncode, frontend.stderr)
        self.assertIn("│   │   ├── msg/", frontend.stdout)
        self.assertIn("│   ├── locales/", frontend.stdout)


if __name__ == "__main__":
    unittest.main()
