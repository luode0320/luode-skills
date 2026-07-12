"""v1 到 v2 基线 CLI 迁移回归。"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[5] / "project-release-test-rules" / "scripts" / "generate_release_test_plan.py"
if str(SCRIPT_PATH.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_PATH.parent))


def load_cli():
    spec = importlib.util.spec_from_file_location("migration_cli_contract", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class MigrationCliTests(unittest.TestCase):
    def test_valid_v1_migration_writes_v2_evidence(self) -> None:
        cli = load_cli()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "v1.yaml"
            output = root / "v2.json"
            source.write_text("schema_version: '1'\ninterfaces: []\n", encoding="utf-8")
            args = cli.build_parser().parse_args(["migrate-baseline", "--input", str(source), "--output", str(output), "--project-fingerprint", "fp", "--source-revision", "r1"])
            with contextlib.redirect_stdout(io.StringIO()):
                args.func(args)
            migrated = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("2.0", migrated["schema_version"])
            self.assertEqual("legacy-v1", migrated["adapter"]["name"])

    def test_invalid_migration_is_blocked_and_source_hash_is_unchanged(self) -> None:
        cli = load_cli()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "invalid.yaml"
            output = root / "v2.json"
            source.write_text("- invalid\n", encoding="utf-8")
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            args = cli.build_parser().parse_args(["migrate-baseline", "--input", str(source), "--output", str(output), "--project-fingerprint", "fp"])
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                args.func(args)
            self.assertEqual(before, hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertIn('"status": "BLOCKED"', captured.getvalue())
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
