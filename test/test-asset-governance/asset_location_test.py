"""根 test 目录、镜像路径和历史测试资产的契约测试。"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


SHARED_DIR = Path(__file__).resolve().parents[1] / "shared"
sys.path.insert(0, str(SHARED_DIR))

from layout_policy import (  # noqa: E402
    legacy_manifest,
    validate_legacy_manifest,
    validate_root_test_layout,
    validate_test_file_location,
)


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "test" / "shared" / "legacy_doc5_tests_manifest.json"


class TestAssetLocation(unittest.TestCase):
    """验证测试代码根、镜像命名和历史包只读边界。"""

    def test_repository_layout_matches_root_test_contract(self) -> None:
        """活动测试必须全部归位到根 test 目录。"""
        self.assertEqual(validate_root_test_layout(ROOT), [])

    def test_single_file_test_mirrors_source_path(self) -> None:
        """单文件测试路径必须镜像被测源码目录。"""
        self.assertEqual(
            validate_test_file_location(
                ROOT,
                Path("src/order/service.py"),
                Path("test/src/order/service_test.py"),
            ),
            [],
        )

    def test_wrong_test_directory_is_rejected(self) -> None:
        """不镜像被测源码的测试目录必须失败。"""
        errors = validate_test_file_location(
            ROOT,
            Path("src/order/service.py"),
            Path("test/order/service_test.py"),
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("test/src/order/service_test.py", errors[0])

    def test_legacy_python_name_and_source_go_test_are_rejected(self) -> None:
        """旧 Python 命名和源码目录 Go 测试都必须被拒绝。"""
        # 1. 在隔离仓库中构造两个违规文件，避免改变真实工作树。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "test" / "src").mkdir(parents=True)
            (root / "test" / "src" / "test_service.py").write_text("pass\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "service_test.go").write_text("package src\n", encoding="utf-8")
            errors = validate_root_test_layout(root)
        self.assertTrue(any("*_test.py" in error for error in errors))
        self.assertTrue(any("*_test.go" in error for error in errors))

    def test_legacy_manifest_rejects_changed_or_new_executables(self) -> None:
        """历史文档目录的可执行资产不得被新增或篡改。"""
        # 1. 先固化临时历史包基线，再分别验证修改和新增都会触发同一边界。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "doc" / "5-tests" / "legacy" / "fixture.py"
            asset.parent.mkdir(parents=True)
            asset.write_text("VALUE = 1\n", encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps(legacy_manifest(root)), encoding="utf-8")
            asset.write_text("VALUE = 2\n", encoding="utf-8")
            self.assertEqual(len(validate_legacy_manifest(root, manifest)), 1)
            (asset.parent / "new_fixture.py").write_text("VALUE = 3\n", encoding="utf-8")
            self.assertEqual(len(validate_legacy_manifest(root, manifest)), 1)

    def test_repository_legacy_manifest_matches_current_history(self) -> None:
        """当前历史测试包必须与首次迁移时的指纹基线一致。"""
        self.assertEqual(validate_legacy_manifest(ROOT, MANIFEST), [])

    def test_active_rules_keep_test_code_and_evidence_separate(self) -> None:
        """活动规则必须共同声明测试代码根与证据根。"""
        documents = (
            ROOT / "artifact-storage-rules" / "SKILL.md",
            ROOT / "test-strategy-rules" / "SKILL.md",
            ROOT / "test-program-rules" / "SKILL.md",
            ROOT / "code-change-finalization-gate-rules" / "SKILL.md",
        )
        for document in documents:
            content = document.read_text(encoding="utf-8")
            with self.subTest(document=document.relative_to(ROOT).as_posix()):
                self.assertIn("根 `test/`", content)
                self.assertIn("`doc/5-tests/`", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
