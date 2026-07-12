"""C09-01 三方契约资产加载、来源校验和 strict 门禁测试。"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.cli import load_interface_contract_assets, run_pipeline


class ContractAssetSyncTests(unittest.TestCase):
    """所有 fixture 只位于 local 临时项目目录，不连接外部服务。"""

    def _write_complete_assets(self, root: Path) -> None:
        (root / "swag").mkdir(parents=True)
        (root / "doc" / "5-tests" / "基线").mkdir(parents=True)
        (root / "swag" / ".swag-manifest.yaml").write_text(
            yaml.safe_dump({"interfaces": [{"method": "GET", "path": "/health", "generated": True}]}, sort_keys=False),
            encoding="utf-8",
        )
        (root / "doc" / "5-tests" / "基线" / "interface-inventory.yaml").write_text(
            yaml.safe_dump([{"HTTP 方法": "GET", "接口路径": "/health"}], sort_keys=False),
            encoding="utf-8",
        )
        (root / "doc" / "5-tests" / "基线" / "reusable-params.yaml").write_text(
            yaml.safe_dump({"params": {}}, sort_keys=False),
            encoding="utf-8",
        )

    def test_complete_assets_have_provenance_and_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_complete_assets(root)
            result = load_interface_contract_assets(root)
            self.assertEqual("PASS", result["metadata"]["status"])
            self.assertFalse(result["metadata"]["requires_refresh"])
            self.assertEqual(["GET /health"], result["metadata"]["manifest_interfaces"])
            for name in ("manifest", "inventory", "reusable_params"):
                provenance = result[name]["provenance"]
                self.assertEqual("loaded", provenance["status"])
                self.assertEqual(64, len(provenance["sha256"]))
                self.assertEqual(name if name != "reusable_params" else "reusable_params", provenance["source_type"])

    def test_missing_and_invalid_assets_are_blocked_without_fabrication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = load_interface_contract_assets(root)
            self.assertEqual("BLOCKED", result["metadata"]["status"])
            self.assertTrue(result["metadata"]["requires_refresh"])
            self.assertIn("missing_manifest", result["metadata"]["failure_types"])
            self.assertIn("missing_inventory", result["metadata"]["failure_types"])
            (root / "swag").mkdir(parents=True)
            (root / "swag" / ".swag-manifest.yaml").write_text("interfaces: [", encoding="utf-8")
            invalid = load_interface_contract_assets(root)
            self.assertEqual("BASELINE_INVALID", invalid["manifest"]["failure_type"])
            self.assertEqual("blocked", invalid["manifest"]["provenance"]["status"])

    def test_non_local_asset_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            outside_manifest = Path(outside) / "manifest.yaml"
            outside_manifest.write_text(yaml.safe_dump({"interfaces": []}), encoding="utf-8")
            result = load_interface_contract_assets(root, manifest=outside_manifest)
            self.assertEqual("NON_LOCAL_ASSET", result["manifest"]["failure_type"])
            self.assertEqual("BLOCKED", result["metadata"]["status"])

    def test_strict_pipeline_passes_sync_metadata_to_report_and_blocks_missing_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "openapi.yaml").write_text(
                yaml.safe_dump({"openapi": "3.0.3", "info": {"title": "local", "version": "1"}, "paths": {"/health": {"get": {"operationId": "health", "responses": {"200": {"description": "ok"}}}}}}, sort_keys=False),
                encoding="utf-8",
            )
            output = root / "artifacts"
            result = run_pipeline(root, output_dir=output, environment="local", dry_run=True, strict_contracts=True)
            self.assertEqual("BLOCKED", result["status"])
            report = json.loads((output / "release-test-report.json").read_text(encoding="utf-8"))
            self.assertEqual("BLOCKED", report["sync_metadata"]["contract_status"])
            self.assertTrue(report["sync_metadata"]["requires_refresh"])


if __name__ == "__main__":
    unittest.main()
