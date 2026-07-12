"""C09-02 三方契约集合、schema hash 和 reusable stale 对账测试。"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.cli import sync_interface_contract_assets


def _stable_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class ContractReconcileTests(unittest.TestCase):
    """对账测试只使用 local 临时目录，不调用任何外部服务。"""

    def _fixture(self, root: Path, *, inventory_extra: list[dict] | None = None, manifest_extra: list[dict] | None = None, drift: bool = False) -> tuple[Path, Path, Path]:
        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}}
        root.joinpath("swag").mkdir(parents=True)
        root.joinpath("doc", "5-tests", "基线").mkdir(parents=True)
        root.joinpath("openapi.yaml").write_text(
            yaml.safe_dump({"openapi": "3.0.3", "info": {"title": "local", "version": "1"}, "paths": {"/health": {"get": {"operationId": "health", "responses": {"200": {"description": "ok", "content": {"application/json": {"schema": schema}}}}}}}}, sort_keys=False),
            encoding="utf-8",
        )
        response_hash = _stable_hash({"type": "object", "properties": {"ok": {"type": "boolean"}}})
        manifest_items = [{"method": "GET", "path": "/health", "operationId": "health", "request_schema_hash": "", "response_schema_hash": response_hash}]
        if manifest_extra:
            manifest_items.extend(manifest_extra)
        inventory_items = [{"接口标识": "health", "HTTP 方法": "GET", "接口路径": "/health", "request_schema_hash": "", "response_schema_hash": "different" if drift else response_hash, "可复用参数影响字段": ["user_id"] if drift else []}]
        if inventory_extra:
            inventory_items.extend(inventory_extra)
        manifest_path = root / "swag" / ".swag-manifest.yaml"
        inventory_path = root / "doc" / "5-tests" / "基线" / "interface-inventory.yaml"
        reusable_path = root / "doc" / "5-tests" / "基线" / "reusable-params.yaml"
        manifest_path.write_text(yaml.safe_dump({"interfaces": manifest_items, "updated_at": "2026-07-13T00:00:00Z"}, sort_keys=False), encoding="utf-8")
        inventory_path.write_text(yaml.safe_dump(inventory_items, sort_keys=False), encoding="utf-8")
        reusable_path.write_text(yaml.safe_dump({"params": {"user_id": [{"status": "reusable", "value_masked": "***", "value_ref": "local.fixture.user_id", "last_verified_at": "2026-07-12T00:00:00Z"}]}}, sort_keys=False), encoding="utf-8")
        return manifest_path, inventory_path, reusable_path

    def test_three_sources_are_synced_and_report_is_written_without_mutating_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, inventory, reusable = self._fixture(root)
            before = {path: path.read_bytes() for path in (manifest, inventory, reusable)}
            output = root / "report.yaml"
            result = sync_interface_contract_assets(root, manifest=manifest, inventory=inventory, reusable_params=reusable, output=output)
            self.assertEqual("PASS", result["metadata"]["status"])
            self.assertTrue(result["reconciliation"]["synced"])
            self.assertEqual([], result["reconciliation"]["drift"])
            self.assertTrue(output.is_file())
            self.assertEqual(before, {path: path.read_bytes() for path in (manifest, inventory, reusable)})

    def test_single_side_missing_is_blocked_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, inventory, reusable = self._fixture(root, manifest_extra=[{"method": "POST", "path": "/submit", "operationId": "submit"}])
            result = sync_interface_contract_assets(root, manifest=manifest, inventory=inventory, reusable_params=reusable)
            self.assertEqual("BLOCKED", result["metadata"]["status"])
            self.assertTrue(any(item["type"] == "missing_in_code" for item in result["reconciliation"]["drift"]))
            self.assertTrue(result["metadata"]["requires_refresh"])

    def test_schema_drift_marks_reusable_sample_stale_in_projection_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, inventory, reusable = self._fixture(root, drift=True)
            before = reusable.read_bytes()
            result = sync_interface_contract_assets(root, manifest=manifest, inventory=inventory, reusable_params=reusable)
            self.assertEqual("BLOCKED", result["metadata"]["status"])
            self.assertTrue(any(item["type"] == "schema_changed" for item in result["reconciliation"]["drift"]))
            self.assertEqual(1, result["reconciliation"]["stale_param_count"])
            sample = result["reconciliation"]["reusable_params_projection"]["params"]["user_id"][0]
            self.assertEqual("stale", sample["status"])
            self.assertEqual("schema_changed", sample["failure_type"])
            self.assertEqual(before, reusable.read_bytes())

    def test_duplicate_interface_id_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, inventory, reusable = self._fixture(root, inventory_extra=[{"接口标识": "health", "HTTP 方法": "POST", "接口路径": "/health-copy"}])
            result = sync_interface_contract_assets(root, manifest=manifest, inventory=inventory, reusable_params=reusable)
            self.assertEqual("BLOCKED", result["metadata"]["status"])
            self.assertIn("health", result["reconciliation"]["duplicate_interface_ids"])

    def test_missing_assets_never_become_synced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = sync_interface_contract_assets(root)
            self.assertNotEqual("PASS", result["metadata"]["status"])
            self.assertTrue(result["metadata"]["requires_refresh"])

    def test_compat_cli_routes_to_read_only_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, inventory, reusable = self._fixture(root)
            before = {path: path.read_bytes() for path in (manifest, inventory, reusable)}
            output = root / "cli-report.yaml"
            script = SCRIPT_ROOT / "generate_release_test_plan.py"
            completed = subprocess.run(
                [sys.executable, str(script), "sync-interface-contract-assets", "--project-root", str(root), "--manifest", str(manifest), "--inventory", str(inventory), "--reusable-params", str(reusable), "--output", str(output)],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            payload = json.loads(completed.stdout)
            self.assertEqual("PASS", payload["metadata"]["status"])
            self.assertTrue(output.is_file())
            self.assertEqual(before, {path: path.read_bytes() for path in (manifest, inventory, reusable)})


if __name__ == "__main__":
    unittest.main()
