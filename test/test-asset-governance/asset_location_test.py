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
    validate_simulation_file_location,
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

    def test_mock_stub_and_fake_mirror_source_path(self) -> None:
        """mock、stub、fake 必须与被测源码共享同一镜像目录。

        [参数] self：测试实例。
        [返回] 无。
        最近修改时间：2026-08-02 23:33:30；改动原因：覆盖三类模拟程序的源码路径镜像契约。
        """
        # 1. 固定被测源码，确保三类模拟程序使用同一相对路径。
        source = Path("src/order/service.py")
        # 2. 逐类验证合法镜像路径不产生错误。
        for kind in ("mock", "stub", "fake"):
            with self.subTest(kind=kind):
                self.assertEqual(
                    validate_simulation_file_location(
                        ROOT,
                        source,
                        Path(f"test/src/order/service_{kind}.py"),
                        kind,
                    ),
                    [],
                )

    def test_simulation_outside_source_mirror_is_rejected(self) -> None:
        """模拟程序放在错误目录或文档目录时必须失败。

        [参数] self：测试实例。
        [返回] 无。
        最近修改时间：2026-08-02 23:33:30；改动原因：覆盖错误目录和证据目录越界防护。
        """
        # 1. 固定源码并准备不符合镜像契约的候选路径。
        source = Path("src/order/service.py")
        wrong_paths = (
            Path("test/order/service_mock.py"),
            Path("doc/5-tests/service_mock.py"),
        )
        # 2. 逐个确认越界路径被拒绝并给出合法目标。
        for wrong_path in wrong_paths:
            with self.subTest(path=wrong_path):
                errors = validate_simulation_file_location(ROOT, source, wrong_path)
                self.assertEqual(len(errors), 1)
                self.assertIn("test/src/order/service_mock.py", errors[0])

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

    def test_mock_policy_is_explicit_and_interface_rule_has_no_old_conflict(self) -> None:
        """相关 Skill 必须显式覆盖 mock，专项接口规则不得恢复旧落点。

        [参数] self：测试实例。
        [返回] 无。
        最近修改时间：2026-08-02 23:33:30；改动原因：锁定多 Skill 规则的一致性和旧口径清除。
        """
        # 1. 收集所有必须声明模拟程序根目录的规则入口。
        documents = (
            ROOT / "artifact-storage-rules" / "SKILL.md",
            ROOT / "test-strategy-rules" / "SKILL.md",
            ROOT / "test-program-rules" / "SKILL.md",
            ROOT / "functional-validation-rules" / "SKILL.md",
            ROOT / "test-regression-rules" / "SKILL.md",
            ROOT / "project-interface-release-execution-rules" / "SKILL.md",
        )
        # 2. 确认每个入口都声明 mock 和根 test 镜像边界。
        for document in documents:
            content = document.read_text(encoding="utf-8")
            with self.subTest(document=document.relative_to(ROOT).as_posix()):
                self.assertIn("mock", content.lower())
                self.assertIn("根 `test/`", content)
        # 3. 确认上线接口专项未恢复历史文档目录落点。
        interface_content = (
            ROOT / "project-interface-release-execution-rules" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("所有测试资产强制落地到 `doc/5-tests/`", interface_content)

    def test_path_map_declares_mock_mirror_policy(self) -> None:
        """中央路径映射必须声明模拟程序根目录、镜像和文档非可执行策略。

        [参数] self：测试实例。
        [返回] 无。
        最近修改时间：2026-08-02 23:33:30；改动原因：把中央路径策略键纳入机器契约。
        """
        # 1. 读取中央路径映射，避免测试复制规则文本。
        path_map = (ROOT / "artifact-storage-rules" / "references" / "path-map.yaml").read_text(
            encoding="utf-8"
        )
        # 2. 验证模拟程序根目录、源码镜像和证据目录策略键齐全。
        self.assertIn("test_mock_stub_fake_under_test_root: true", path_map)
        self.assertIn("test_mock_stub_fake_mirror_source_paths: true", path_map)
        self.assertIn("doc5_tests_non_executable_only: true", path_map)


    def test_runtime_mock_is_not_treated_as_scattered_test_asset(self) -> None:
        """根 mock/ 下的运行时 Mock 不被误判为散落测试资产。

        [参数] self：测试实例。
        [返回] 无。
        最近修改时间：2026-08-08；改动原因：运行时 Mock 与测试 Mock 分离，根 mock/ 是运行时 Mock 唯一合法目录。
        """
        # 1. 在隔离仓库中构造根 mock/ 运行时 Mock，确认根 test/ 布局校验不报错。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "test").mkdir()
            mock_file = root / "mock" / "internal" / "business" / "scalp" / "api" / "gateway.go"
            mock_file.parent.mkdir(parents=True)
            mock_file.write_text("//go:build mock\n\npackage mock_api\n", encoding="utf-8")
            errors = validate_root_test_layout(root)
            self.assertEqual(errors, [])

    def test_runtime_mock_policy_is_explicit_in_rules(self) -> None:
        """相关 Skill 必须显式声明根 mock/ 运行时 Mock 落点。

        [参数] self：测试实例。
        [返回] 无。
        最近修改时间：2026-08-08；改动原因：固化运行时 Mock 目录规则跨 Skill 一致性。
        """
        # 所有相关 Skill 必须包含 `mock/` 引用
        mock_docs = (
            ROOT / "artifact-storage-rules" / "SKILL.md",
            ROOT / "test-strategy-rules" / "SKILL.md",
            ROOT / "test-program-rules" / "SKILL.md",
            ROOT / "package-structure-rules" / "SKILL.md",
            ROOT / "AGENTS.md",
            ROOT / "CLAUDE.md",
        )
        for document in mock_docs:
            content = document.read_text(encoding="utf-8")
            with self.subTest(document=document.relative_to(ROOT).as_posix()):
                self.assertIn("mock/", content)
        # 定义构建标签的 Skill 必须额外包含 //go:build mock
        tag_docs = (
            ROOT / "test-program-rules" / "SKILL.md",
            ROOT / "package-structure-rules" / "SKILL.md",
            ROOT / "AGENTS.md",
            ROOT / "CLAUDE.md",
        )
        for document in tag_docs:
            content = document.read_text(encoding="utf-8")
            with self.subTest(document=document.relative_to(ROOT).as_posix()):
                self.assertIn("//go:build mock", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
