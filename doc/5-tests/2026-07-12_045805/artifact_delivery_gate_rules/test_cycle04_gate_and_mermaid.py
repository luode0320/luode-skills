#!/usr/bin/env python3
"""周期 04 的严格追踪、文档 profile 和 Mermaid 真解析集成测试。"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = ROOT / "artifact-delivery-gate-rules" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import validate_engineering_docs as validator  # noqa: E402


DOCS = [
    ROOT / "doc/2-需求/2026-07-12_033322_需求与实施文档极致完备化.md",
    ROOT / "doc/7-验收/2026-07-12_033322_需求与实施文档极致完备化_验收标准.md",
    ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施总览.md",
    ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施周期01_契约与基线.md",
    ROOT / "doc/3-实施/2026-07-12_042832_需求与实施文档极致完备化_实施周期02_需求入口与验收契约.md",
    ROOT / "doc/3-实施/2026-07-12_033322_需求与实施文档极致完备化_实施周期03_执行卡与输出门禁.md",
]


class Cycle04GateAndMermaidTests(unittest.TestCase):
    def test_strict_fixture_positive_and_negative(self) -> None:
        fixture_root = Path(__file__).parent / "fixtures"
        errors: list[str] = []
        validator.check_strict_trace(fixture_root / "complete", errors)
        self.assertEqual(errors, [])

        errors = []
        validator.check_strict_trace(fixture_root / "orphan", errors)
        self.assertTrue(any("missing evidence category REVIEW" in error for error in errors))

    def test_all_current_profiles_pass(self) -> None:
        profiles = validator.load_profiles(
            ROOT / "artifact-delivery-gate-rules/references/document-quality-profiles.yaml"
        )["profiles"]
        targets = (
            ("requirement", DOCS[0]),
            ("acceptance", DOCS[1]),
            ("implementation_overview", DOCS[2]),
            ("implementation_cycle", DOCS[3]),
            ("implementation_cycle", DOCS[4]),
            ("implementation_cycle", DOCS[5]),
        )
        for profile_name, document in targets:
            result = validator.validate_document(document, profile_name, profiles[profile_name], validator.load_profiles(ROOT / "artifact-delivery-gate-rules/references/document-quality-profiles.yaml"), ROOT)
            self.assertTrue(result["valid"], f"{document}: {result['errors']}")

    def test_mermaid_cli_renders_current_documents(self) -> None:
        npx = shutil.which("npx") or shutil.which("npx.cmd")
        self.assertIsNotNone(npx, "npx is required for Mermaid true parsing")
        with tempfile.TemporaryDirectory(prefix="codex-mermaid-c04-") as directory:
            output_root = Path(directory)
            rendered = 0
            for index, document in enumerate(DOCS):
                output = output_root / f"document-{index}.md"
                command = [npx, "--offline", "--yes", "@mermaid-js/mermaid-cli", "-i", str(document), "-o", str(output), "-q"]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
                svgs = list(output_root.glob(f"document-{index}*.svg"))
                self.assertTrue(svgs, f"no SVG generated for {document}")
                self.assertTrue(all(path.stat().st_size > 0 for path in svgs))
                rendered += len(svgs)
            self.assertGreaterEqual(rendered, 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
