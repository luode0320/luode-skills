"""根 test 目录、镜像路径和历史测试资产的契约测试。"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml


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
PATH_MAP = ROOT / "artifact-storage-rules" / "references" / "path-map.yaml"
BUG_DOMAIN_SKILLS = (
    "bug-intake-rules",
    "bug-fix-proposal-rules",
    "bug-reproduction-rules",
    "bug-root-cause-rules",
    "bug-validation-rules",
)
TEST_DOMAIN_SKILLS = (
    "test-strategy-rules",
    "test-program-rules",
    "test-regression-rules",
    "functional-validation-rules",
)
# 历史归档只读，规则文本允许提到旧目录形态；这一行是唯一豁免。
TEST_DOMAIN_LEGACY_ALLOWLIST = frozenset({
    "test-strategy-rules/references/test-asset-governance.md:25",
})


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

    def test_path_map_declares_flat_bug_and_test_docs(self) -> None:
        """路径真相源必须声明扁平 md，并移除全部任务子目录键位。"""
        # 1. 单一真相源必须可解析，否则下游 skill 无法引用统一模板。
        path_map = yaml.safe_load(PATH_MAP.read_text(encoding="utf-8"))
        entry_files = path_map["entry_files"]
        directories = path_map["directories"]
        policies = path_map["policies"]

        # 2. 旧的任务子目录与 README 入口键位必须彻底消失，避免新旧两套模板并存。
        for removed in ("bug_root_readme", "test_task_readme", "test_task_readme_note"):
            self.assertNotIn(removed, entry_files)
        for removed in ("bug_root", "test_task_root", "test_task_evidence_dir", "test_task_artifacts_dir"):
            self.assertNotIn(removed, directories)

        # 3. 新的扁平模板、豁免目录和策略开关必须同时到位。
        self.assertEqual(entry_files["bug_doc"], "{datetime}_{bug_cn_title}.md")
        self.assertEqual(entry_files["test_doc"], "{datetime}_{test_cn_title}.md")
        self.assertEqual(directories["test_baseline_dir"], "doc/5-tests/基线")
        self.assertEqual(directories["release_test_artifacts_root"], "test/release-artifacts")
        for policy in (
            "bug_and_test_docs_are_flat_files",
            "historical_subdirectory_artifacts_read_only",
            "test_baseline_dir_exempt_from_flattening",
            "release_test_machine_artifacts_outside_doc",
            "same_bug_updates_same_doc",
            "same_test_round_updates_same_doc",
            "new_independent_test_round_creates_new_doc",
        ):
            self.assertTrue(policies[policy], policy)
        for removed in (
            "same_bug_updates_same_root",
            "same_test_round_updates_same_root",
            "new_independent_test_round_creates_new_root",
            "test_task_readme_is_evidence_only",
        ):
            self.assertNotIn(removed, policies)

    def test_bug_domain_rules_drop_subdirectory_terminology(self) -> None:
        """Bug 域规则必须统一到扁平主文档口径，不残留根目录与 README 入口。"""
        # 1. 逐个 skill 扫描，命中即报出精确文件行，便于定位漏改。
        offenders: list[str] = []
        for skill in BUG_DOMAIN_SKILLS:
            for path in sorted((ROOT / skill).rglob("*")):
                if not path.is_file() or path.suffix not in {".md", ".yaml"}:
                    continue
                relative = path.relative_to(ROOT).as_posix()
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    if "Bug 根目录" in line or "doc/4-bugs/` 根目录" in line:
                        offenders.append(f"{relative}:{number}")
        self.assertEqual(offenders, [])

    def test_test_domain_rules_drop_subdirectory_terminology(self) -> None:
        """测试域规则必须统一到扁平测试主文档，不残留任务子目录与证据子目录。"""
        # 1. 同时拦截旧路径模板与 evidence/artifacts 子目录表述。
        forbidden = ("doc/5-tests/<时间戳>", "/README.md", "`evidence/`", "`artifacts/`", "时间戳目录")
        offenders: list[str] = []
        for skill in TEST_DOMAIN_SKILLS:
            for path in sorted((ROOT / skill).rglob("*")):
                if not path.is_file() or path.suffix not in {".md", ".yaml"}:
                    continue
                relative = path.relative_to(ROOT).as_posix()
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    anchor = f"{relative}:{number}"
                    if anchor in TEST_DOMAIN_LEGACY_ALLOWLIST:
                        continue
                    if any(token in line for token in forbidden):
                        offenders.append(anchor)
        self.assertEqual(offenders, [])

    def test_test_naming_template_is_flat_markdown(self) -> None:
        """测试命名模板必须是扁平 md，并保留基线目录豁免。"""
        naming = (ROOT / "artifact-storage-rules" / "references" / "naming-templates.md").read_text(encoding="utf-8")
        self.assertIn("doc/5-tests/YYYY-MM-DD_HHmmss_<测试任务中文主题>.md", naming)
        self.assertNotIn("doc/5-tests/YYYY-MM-DD_HHmmss/README.md", naming)
        self.assertIn("doc/5-tests/基线/", naming)

    def test_bug_naming_template_is_flat_markdown(self) -> None:
        """Bug 命名模板必须是扁平 md，且不再声明 README 主入口。"""
        naming = (ROOT / "artifact-storage-rules" / "references" / "naming-templates.md").read_text(encoding="utf-8")
        self.assertIn("doc/4-bugs/YYYY-MM-DD_HHmmss_问题中文简介.md", naming)
        self.assertNotIn("doc/4-bugs/YYYY-MM-DD_HHmmss_问题中文简介/", naming)


if __name__ == "__main__":
    unittest.main(verbosity=2)
