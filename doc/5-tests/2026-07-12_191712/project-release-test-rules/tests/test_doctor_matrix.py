"""doctor 发现能力与执行能力矩阵回归。"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.cli import run_doctor


class DoctorMatrixTests(unittest.TestCase):
    def test_discovery_ready_but_execution_pending_is_not_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schema.graphql").write_text("type Query { user: String }", encoding="utf-8")
            result = run_doctor(root)
            self.assertIn(result["status"], {"PENDING", "PARTIAL"})
            self.assertEqual("pending", result["adapter_matrix"]["graphql"]["execution_status"])

    def test_http_discovery_and_execution_ready_can_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "openapi.yaml").write_text("openapi: '3.0.0'\ninfo: {title: fixture, version: '1'}\npaths: {}\n", encoding="utf-8")
            result = run_doctor(root)
            self.assertIn(result["status"], {"PENDING", "PASS"})


if __name__ == "__main__":
    unittest.main()
