"""上线接口测试引擎的双落点布局契约测试。"""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "project-interface-release-execution-rules" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from generate_release_test_plan import ensure_release_task_root  # noqa: E402
from release_test_engine.report import write_report  # noqa: E402


STAMP = "2026-08-11_101500"


class TestReleaseArtifactLayout(unittest.TestCase):
    """验证中文主报告落在扁平 doc md，机器产物落在根 test。"""

    def _paths(self, root: Path) -> tuple[Path, Path]:
        """构造本轮的中文主报告与机器产物根路径。

        [参数] root：临时项目根目录。
        [返回] tuple：(中文主报告 md 路径, 机器产物根目录)。
        最近修改时间：2026-08-11；改动原因：新增双落点布局的活动测试。
        """
        doc_path = root / "doc" / "5-tests" / f"{STAMP}_上线前项目接口测试.md"
        artifacts_root = root / "test" / "release-artifacts" / f"{STAMP}_release-interface-test"
        return doc_path, artifacts_root

    def test_task_skeleton_keeps_doc_flat_and_artifacts_outside_doc(self) -> None:
        """骨架初始化后 doc/5-tests 下只有扁平 md，机器产物全在根 test。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            doc_path, artifacts_root = self._paths(root)
            result = ensure_release_task_root(artifacts_root, doc_path)

            # 1. doc/5-tests 下只允许出现本轮那一份扁平 md，不得再出现任何子目录。
            doc_root = root / "doc" / "5-tests"
            self.assertEqual([item.name for item in doc_root.iterdir()], [doc_path.name])
            self.assertTrue(doc_path.is_file())

            # 2. 机器产物必须全部落在根 test/release-artifacts/ 内，不得回流 doc/。
            for key in ("plan", "sync_report", "reconcile", "results", "logs_dir"):
                produced = Path(result[key])
                self.assertTrue(produced.exists(), key)
                self.assertTrue(produced.is_relative_to(artifacts_root), f"{key} -> {produced}")

            # 3. 旧布局的中间层与 README 入口都不得再生成。
            self.assertFalse((artifacts_root / "ascii-artifacts").exists())
            self.assertFalse((artifacts_root / "上线前项目接口测试").exists())
            self.assertNotIn("readme", result)
            self.assertNotIn("task_root", result)

    def test_write_report_splits_doc_report_from_machine_artifacts(self) -> None:
        """报告生成同样遵守双落点：中文主报告进 doc，机器产物留在产物根。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            doc_path, artifacts_root = self._paths(root)
            results = [{"operation_id": "GET /health", "status": "PASS", "request": {}, "response": {"code": 0}}]
            gate = {"gate": "PASS", "allow_release": True, "passed": 1, "failed": 0, "pending": 0}

            write_report(artifacts_root, results, gate, run_id="run-1", doc_report_path=doc_path)

            # 1. 中文主报告只落在 doc 的扁平 md，产物根内不得再留一份 README.md。
            self.assertTrue(doc_path.is_file())
            self.assertFalse((artifacts_root / "README.md").exists())
            self.assertEqual([item.name for item in (root / "doc" / "5-tests").iterdir()], [doc_path.name])

            # 2. 正文指引必须换算成从 doc 主报告出发的相对路径，而不是旧的 ascii-artifacts。
            content = doc_path.read_text(encoding="utf-8")
            self.assertIn("interface-sync-report.yaml", content)
            self.assertNotIn("ascii-artifacts/", content)

    def test_write_report_without_doc_path_keeps_legacy_single_root(self) -> None:
        """未指定 doc 落点的旧调用方仍在产物根内直接得到 README.md。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output_dir = root / "custom-output"
            results = [{"operation_id": "GET /health", "status": "PASS", "request": {}, "response": {"code": 0}}]
            gate = {"gate": "PASS", "allow_release": True, "passed": 1, "failed": 0, "pending": 0}

            write_report(output_dir, results, gate, run_id="run-2")

            self.assertTrue((output_dir / "README.md").is_file())
            self.assertFalse((output_dir / "ascii-artifacts").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
