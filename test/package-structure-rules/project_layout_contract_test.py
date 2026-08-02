"""验证三类项目研发文档目录与前端根静态数据边界。"""

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
LAYOUT = ROOT / "package-structure-rules" / "references" / "project-layout-v2.md"


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """调用本地 Catalog CLI。"""
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(CLI), *arguments],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


class ProjectLayoutContractTests(unittest.TestCase):
    """覆盖 fullstack、backend、frontend 的活动 doc 骨架。"""

    def test_catalog_query_defines_one_root_test_entry_per_project_kind(self):
        """确认三类项目均只有一个由测试策略 Skill 负责的根 test 条目。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-02 补充三类项目根 test Catalog 查询契约。
        """
        # 1. 校验三类项目的唯一条目、Owner、规范路径和 query 输出。
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        entries = [entry for entry in catalog["entries"] if entry.get("artifact_kind") == "test"]
        self.assertEqual(3, len(entries))
        self.assertEqual({"fullstack", "backend", "frontend"}, {entry["project_kind"] for entry in entries})
        self.assertTrue(all(entry["canonical_path"] == "test" for entry in entries))
        self.assertTrue(all(entry["owner_skill"] == "test-strategy-rules" for entry in entries))
        for project_kind in ("fullstack", "backend", "frontend"):
            with self.subTest(project_kind=project_kind):
                result = run_cli("query", "--project-kind", project_kind, "--artifact", "test")
                self.assertEqual(0, result.returncode, result.stdout)
                self.assertEqual("test", json.loads(result.stdout)["entry"]["canonical_path"])

    def test_render_and_init_use_root_test_without_competing_subroots(self):
        """确认 render 与 init 均表达根 test，且不生成 backend/test 或 frontend/test。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-02 补充根 test 的 render 与 init 契约。
        """
        # 1. 逐类确认目录渲染、初始化和竞争测试根边界。
        for project_kind in ("fullstack", "backend", "frontend"):
            with self.subTest(project_kind=project_kind), tempfile.TemporaryDirectory() as directory:
                rendered = run_cli("render", "--project-kind", project_kind)
                self.assertEqual(0, rendered.returncode, rendered.stderr)
                self.assertIn("test/", rendered.stdout)
                initialized = run_cli("init", "--project-kind", project_kind, "--root", directory)
                self.assertEqual(0, initialized.returncode, initialized.stdout)
                self.assertTrue((Path(directory) / "test").is_dir())
                self.assertFalse((Path(directory) / "backend/test").exists())
                self.assertFalse((Path(directory) / "frontend/test").exists())

    def test_catalog_and_layout_define_same_active_doc_tree(self):
        """确认 Catalog skeleton 与人工目录树均只保留活动目录。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-02 将根 test 纳入三类 skeleton 对账。
        """
        # 1. 对账活动 doc 目录、根 test 和历史目录排除项。
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        active = [
            "doc/1-架构",
            "doc/2-需求",
            "doc/3-实施",
            "doc/4-bugs",
            "doc/5-tests",
            "doc/6-review",
            "doc/data/images",
        ]
        for project_kind in ("fullstack", "backend", "frontend"):
            skeleton = catalog["skeletons"][project_kind]
            self.assertIn("test", skeleton, (project_kind, "test"))
            for path in active:
                self.assertIn(path, skeleton, (project_kind, path))
            self.assertNotIn("doc/6-审查", skeleton)
            self.assertNotIn("doc/7-验收", skeleton)
        layout = LAYOUT.read_text(encoding="utf-8")
        self.assertNotIn("├── 6-审查", layout)
        self.assertNotIn("├── 7-验收", layout)
        self.assertNotIn("├── data/                                    # [条件·提交] 原始静态数据", layout)

    def test_init_creates_doc_tree_for_all_project_kinds(self):
        """确认三类初始化均创建完整活动 doc 树且不创建旧目录。

        [参数] self：unittest 测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-02 将根 test 纳入 init 骨架断言。
        """
        # 1. 验证三类 init 创建根 test 和活动 doc 树，并排除历史目录。
        expected = {
            "test",
            "doc/1-架构",
            "doc/2-需求",
            "doc/3-实施",
            "doc/4-bugs",
            "doc/5-tests",
            "doc/6-review",
            "doc/data/images",
        }
        for project_kind in ("fullstack", "backend", "frontend"):
            with self.subTest(project_kind=project_kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                result = run_cli("init", "--project-kind", project_kind, "--root", str(root))
                self.assertEqual(0, result.returncode, result.stdout)
                for relative in expected:
                    self.assertTrue((root / relative).is_dir(), (project_kind, relative))
                self.assertFalse((root / "doc/6-审查").exists())
                self.assertFalse((root / "doc/7-验收").exists())
                if project_kind == "frontend":
                    self.assertFalse((root / "data/business").exists())
                    self.assertFalse((root / "data/project").exists())


if __name__ == "__main__":
    unittest.main()
