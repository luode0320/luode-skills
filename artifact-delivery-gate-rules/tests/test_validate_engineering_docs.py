#!/usr/bin/env python3
"""验证工程文档质量校验器的正例、负例和 N/A 处理。"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_engineering_docs as validator  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
PROFILE_FILE = ROOT / "artifact-delivery-gate-rules" / "references" / "document-quality-profiles.yaml"


class EngineeringDocumentValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = validator.load_profiles(PROFILE_FILE)

    def test_requirement_fixture_passes(self) -> None:
        document = ROOT / "doc" / "2-需求" / "2026-07-12_033322_需求与实施文档极致完备化.md"
        profile = self.payload["profiles"]["requirement"]
        result = validator.validate_document(document, "requirement", profile, self.payload, ROOT)
        self.assertTrue(result["valid"], result["errors"])

    def test_missing_section_is_rejected(self) -> None:
        source = ROOT / "doc" / "7-验收" / "2026-07-12_033322_需求与实施文档极致完备化_验收标准.md"
        text = source.read_text(encoding="utf-8").replace("## 4. 验收场景", "## 4. 删除的验收场景", 1)
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "negative.md"
            document.write_text(text, encoding="utf-8")
            profile = self.payload["profiles"]["acceptance"]
            result = validator.validate_document(document, "acceptance", profile, self.payload, Path(directory))
        self.assertFalse(result["valid"])
        self.assertTrue(any("验收场景" in error for error in result["errors"]))

    def test_na_with_reason_is_allowed(self) -> None:
        errors: list[str] = []
        validator.check_na_reasons("字段：`N/A`；原因与证据：本任务不涉及数据库。", errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
