"""验证独立后端 common/util 与根 utils 的目录边界。"""

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
    最近修改时间: 2026-08-04 12:00:00 新增 common/util 行为测试入口。
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
    最近修改时间: 2026-08-04 12:00:00 新增多语言 common/util 断言入口。
    """
    # 1. 固定项目类型与 strict 策略，只切换当前语言样本。
    return run_cli(
        "check", "--root", str(root), "--project-kind", "backend",
        "--language", language, "--policy", "strict",
    )


class BackendCommonUtilLayoutTests(unittest.TestCase):
    """覆盖 common/util 的唯一落点、扁平文件和旧位置拒绝。"""

    def test_catalog_and_compatibility_query_use_one_common_util_entry(self):
        """Catalog 只保留 common/util，source-util 仅作为兼容查询别名。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-04 12:00:00 覆盖 Catalog 唯一路径与兼容查询。
        """
        # 1. 先核对机器目录事实，再核对两个查询入口的结果。
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        entries = [entry for entry in catalog["entries"] if entry.get("artifact_kind") == "common-util"]
        self.assertEqual(1, len(entries))
        self.assertEqual("common/util", entries[0]["canonical_path"])
        self.assertTrue(entries[0]["flat_files"])
        self.assertFalse(any(entry.get("artifact_kind") == "source-util" for entry in catalog["entries"]))

        for artifact, language in (("common-util", None), ("source-util", "go")):
            arguments = ["query", "--artifact", artifact]
            if language:
                arguments.extend(("--language", language))
            result = run_cli(*arguments)
            self.assertEqual(0, result.returncode, result.stdout)
            self.assertEqual("common/util", json.loads(result.stdout)["entry"]["canonical_path"])

    def test_init_and_render_express_common_util_without_creating_it_by_default(self):
        """默认 init 不创建条件目录，显式启用时只创建 common/util。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-04 12:00:00 覆盖 init 与 render 目录表达。
        """
        # 1. 对比默认初始化与显式启用后的目录集合。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialized = run_cli("init", "--project-kind", "backend", "--root", str(root))
            self.assertEqual(0, initialized.returncode, initialized.stdout)
            self.assertFalse((root / "common/util").exists())

            enabled = run_cli(
                "init", "--project-kind", "backend", "--root", str(root),
                "--enable", "backend.common.util",
            )
            self.assertEqual(0, enabled.returncode, enabled.stdout)
            self.assertTrue((root / "common/util").is_dir())

        rendered = run_cli("render", "--project-kind", "backend")
        self.assertEqual(0, rendered.returncode, rendered.stderr)
        self.assertIn("common/", rendered.stdout)
        self.assertIn("util/", rendered.stdout)
        self.assertNotIn("internal/", rendered.stdout)

    def test_common_util_accepts_flat_current_language_files_and_rejects_other_shapes(self):
        """common/util 允许当前语言直接文件，拒绝子目录、错误扩展和根 utils 文件。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-04 12:00:00 覆盖四语言扁平目录边界。
        """
        # 1. 为四种语言依次构造正向文件和三类负向路径。
        samples = {
            "go": ("helper.go", "helper.txt"),
            "java": ("Helper.java", "Helper.txt"),
            "node": ("helper.ts", "helper.py"),
            "python": ("helper.py", "helper.ts"),
        }
        for language, (valid_name, invalid_name) in samples.items():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "Dockerfile").touch()
                valid = root / "common/util" / valid_name
                valid.parent.mkdir(parents=True)
                valid.touch()
                accepted = strict_backend(root, language)
                self.assertEqual(0, accepted.returncode, accepted.stdout)

                invalid = root / "common/util" / invalid_name
                invalid.touch()
                rejected_extension = strict_backend(root, language)
                self.assertEqual(2, rejected_extension.returncode, rejected_extension.stdout)
                self.assertIn("common/util 仅允许", rejected_extension.stdout)

                invalid.unlink()
                nested = root / "common/util/nested" / valid_name
                nested.parent.mkdir()
                nested.touch()
                rejected_nested = strict_backend(root, language)
                self.assertEqual(2, rejected_nested.returncode, rejected_nested.stdout)
                self.assertIn("common/util 禁止子目录", rejected_nested.stdout)

                nested.unlink()
                nested.parent.rmdir()
                root_file = root / "utils" / valid_name
                root_file.parent.mkdir()
                root_file.touch()
                rejected_root_utils = strict_backend(root, language)
                self.assertEqual(2, rejected_root_utils.returncode, rejected_root_utils.stdout)
                self.assertIn("根 utils 禁止直接文件", rejected_root_utils.stdout)

    def test_old_source_util_and_non_backend_common_util_are_rejected(self):
        """新项目拒绝源码根 util，非独立后端也不能使用根 common/util。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-04 12:00:00 覆盖旧位置与项目类型边界。
        """
        # 1. 分别验证 backend 旧源码根和 frontend 根 common/util 的失败关闭。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Dockerfile").touch()
            old = root / "internal/util/helper.go"
            old.parent.mkdir(parents=True)
            old.touch()
            rejected = strict_backend(root)
            self.assertEqual(2, rejected.returncode, rejected.stdout)
            self.assertIn("源码根 util 已废弃", rejected.stdout)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Dockerfile").touch()
            frontend_util = root / "common/util/helper.js"
            frontend_util.parent.mkdir(parents=True)
            frontend_util.touch()
            rejected = run_cli(
                "check", "--root", str(root), "--project-kind", "frontend", "--policy", "strict",
            )
            self.assertEqual(2, rejected.returncode, rejected.stdout)
            self.assertIn("common/util 仅允许独立后端项目", rejected.stdout)

    def test_adoption_legacy_snapshot_can_maintain_old_source_util_without_migration(self):
        """旧源码根只有登记为 legacy 快照后才可继续维护，adoption 不自动搬移。

        [参数] self：测试实例。
        [返回] None：断言失败时由 unittest 报告。
        最近修改时间: 2026-08-04 12:00:00 覆盖 legacy 快照兼容边界。
        """
        # 1. 登记真实旧目录和文件快照，再执行 adoption 只读检查。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old_root = root / "internal/util"
            old_file = old_root / "helper.go"
            old_root.mkdir(parents=True)
            old_file.touch()
            manifest = root / "doc/1-架构/3-目录规则收敛清单.yaml"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({
                "version": 1,
                "project_kind": "backend",
                "language": "go",
                "adopted_paths": [],
                "legacy_source_roots": [{
                    "path": "internal/util",
                    "responsibility": "旧源码根工具快照",
                    "existing_directories": ["internal/util"],
                    "existing_files": ["internal/util/helper.go"],
                }],
            }, ensure_ascii=False), encoding="utf-8")
            accepted = run_cli(
                "check", "--root", str(root), "--project-kind", "backend", "--language", "go",
                "--policy", "adoption", "--adoption-manifest", "doc/1-架构/3-目录规则收敛清单.yaml",
            )
            self.assertEqual(0, accepted.returncode, accepted.stdout)


if __name__ == "__main__":
    unittest.main()
