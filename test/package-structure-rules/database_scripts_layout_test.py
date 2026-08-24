"""验证数据库执行脚本目录 database/scripts 的布局边界。"""

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
    最近修改时间: 2026-08-24 21:00:00 新增数据库脚本目录测试入口。
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
    最近修改时间: 2026-08-24 21:00:00 新增数据库脚本目录测试入口。
    """
    # 1. 固定项目类型与 strict 策略，只切换当前语言样本。
    return run_cli(
        "check", "--root", str(root), "--project-kind", "backend",
        "--language", language, "--policy", "strict",
    )


class DatabaseScriptsLayoutTests(unittest.TestCase):
    """覆盖 database/scripts 的合法路径、旧路径废弃与扩展名边界。"""

    def _project(self, files: list[str]) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        """构造带样本文件的临时后端项目根。

        [参数] files：项目相对路径清单。
        [返回] tuple[tempfile.TemporaryDirectory[str], Path]：临时目录句柄与项目根。
        最近修改时间: 2026-08-24 21:00:00 新增数据库脚本目录测试入口。
        """
        # 1. strict 要求项目根存在 Dockerfile；样本文件自动补父目录。
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "Dockerfile").touch()
        for relative in files:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        return tmp, root

    def test_catalog_declares_scripts_layout_and_forbids_old_sql_root(self):
        """Catalog 声明 database/scripts 三层结构与旧 database/sql 废弃。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-24 21:00:00 覆盖机器事实源一致性。
        """
        # 1. 核对 allowed_children 三层与 forbidden_paths 整根废弃。
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(
            ["sql", "js", "lua"], catalog["allowed_children"]["database/scripts"],
        )
        self.assertEqual(
            ["ddl", "index", "field"], catalog["allowed_children"]["database/scripts/sql"],
        )
        self.assertEqual(
            ["create", "update", "delete"],
            catalog["allowed_children"]["database/scripts/sql/field"],
        )
        self.assertIn("database/sql", catalog["forbidden_paths"])
        self.assertIn("database/scripts/sql/dml", catalog["forbidden_paths"])
        # 2. entries 同时存在 database_sql 与 database_script 两类脚本资产。
        kinds = {entry["artifact_kind"] for entry in catalog["entries"]}
        self.assertIn("database_sql", kinds)
        self.assertIn("database_script", kinds)

    def test_new_script_paths_pass_strict(self):
        """新结构合法脚本路径在 strict 下通过。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-24 21:00:00 覆盖 SQL 分类与 js/lua 正向样本。
        """
        # 1. 覆盖 SQL 五个叶子目录与 js/lua 两个脚本目录。
        files = [
            "database/scripts/sql/ddl/init.sql",
            "database/scripts/sql/index/user_idx.sql",
            "database/scripts/sql/field/create/add_age.sql",
            "database/scripts/sql/field/update/change_name.sql",
            "database/scripts/sql/field/delete/drop_age.sql",
            "database/scripts/js/reset_user.js",
            "database/scripts/lua/rate_limit.lua",
        ]
        tmp, root = self._project(files)
        try:
            result = strict_backend(root)
            self.assertEqual(0, result.returncode, result.stdout)
        finally:
            tmp.cleanup()

    def test_old_database_sql_root_is_forbidden(self):
        """旧 database/sql 整根命中禁止路径。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-24 21:00:00 覆盖旧路径废弃语义。
        """
        # 1. 旧路径与旧字段分类都应按禁止路径失败关闭。
        for relative in (
            "database/sql/ddl/init.sql",
            "database/sql/field/create/add_age.sql",
        ):
            with self.subTest(path=relative):
                tmp, root = self._project([relative])
                try:
                    result = strict_backend(root)
                    self.assertEqual(2, result.returncode, result.stdout)
                    self.assertIn("禁止路径", result.stdout)
                finally:
                    tmp.cleanup()

    def test_script_directories_reject_wrong_extensions(self):
        """脚本叶子目录只允许声明扩展名，拒绝其他扩展与子目录。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-24 21:00:00 覆盖扩展名与嵌套层级边界。
        """
        # 1. js/lua 目录拒绝 SQL，SQL 目录拒绝生产源码。
        samples = (
            ("database/scripts/js/x.sql", "只允许 .js 文件"),
            ("database/scripts/lua/x.js", "只允许 .lua 文件"),
            ("database/scripts/sql/ddl/x.go", "只允许 .sql 文件"),
            ("database/scripts/js/sub/x.js", "只允许直接存放声明扩展名文件"),
        )
        for relative, message in samples:
            with self.subTest(path=relative):
                tmp, root = self._project([relative])
                try:
                    result = strict_backend(root)
                    self.assertEqual(2, result.returncode, result.stdout)
                    self.assertIn(message, result.stdout)
                finally:
                    tmp.cleanup()

    def test_forbidden_sql_categories_and_invalid_children_are_rejected(self):
        """dml 等禁止分类与 scripts 非法子目录稳定失败。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-24 21:00:00 覆盖禁止分类与子目录边界。
        """
        # 1. database/scripts/sql/dml 是禁止分类；database/scripts/ddl 不是合法子目录。
        samples = (
            ("database/scripts/sql/dml/x.sql", "禁止路径"),
            ("database/scripts/ddl/x.sql", "非法子目录"),
        )
        for relative, message in samples:
            with self.subTest(path=relative):
                tmp, root = self._project([relative])
                try:
                    result = strict_backend(root)
                    self.assertEqual(2, result.returncode, result.stdout)
                    self.assertIn(message, result.stdout)
                finally:
                    tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
