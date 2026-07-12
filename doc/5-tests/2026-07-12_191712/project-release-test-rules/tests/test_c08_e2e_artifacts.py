"""C08-03 local pipeline 产物、基线投影与证据互链回归。"""

from __future__ import annotations

import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.cli import run_pipeline
from release_test_engine.storage import BaselineStore


class _C08Handler(BaseHTTPRequestHandler):
    """提供只监听回环地址的可重复 HTTP fixture。"""

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler protocol name
        payload = json.dumps({"code": 0, "message": "ok", "data": {"service": "c08-local"}}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, _format: str, *_args: object) -> None:
        return


class C08E2EArtifactTests(unittest.TestCase):
    """验证 C08 交付物是真实执行结果，而不是仅由返回值拼出的占位文件。"""

    def test_local_pipeline_artifacts_and_baseline_projection_are_replayable(self) -> None:
        """[参数] 无；[返回] 无；最近修改时间: 2026-07-12 22:05:00 验证响应预览和 baseline 投影证据可回放。"""

        # 1. 启动仅监听回环地址的 local fixture，并执行完整 pipeline。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = {
                "openapi": "3.0.3",
                "info": {"title": "c08 local fixture", "version": "1.0.0"},
                "paths": {"/health": {"get": {"operationId": "health", "responses": {"200": {"description": "ok"}}}}},
            }
            (root / "openapi.yaml").write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            server = ThreadingHTTPServer(("127.0.0.1", 0), _C08Handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                output_dir = root / "artifacts"
                baseline_path = root / "baseline.yaml"
                result = run_pipeline(
                    root,
                    output_dir=output_dir,
                    baseline_path=baseline_path,
                    environment="local",
                    env={"local_config": f"http://127.0.0.1:{server.server_port}"},
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)

            self.assertEqual("PASS", result["status"])
            report_path = output_dir / "release-test-report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual("2.0", report["schema_version"])
            self.assertEqual(result["run_id"], report["run_id"])
            self.assertEqual("PASS", report["gate"]["gate"])
            self.assertEqual(["health"], [item["operation_id"] for item in report["results"]])
            for item in report["results"]:
                self.assertIsInstance(item["request"], str)
                self.assertIsInstance(item["response"], str)
                json.loads(item["request"])
                response_preview = json.loads(item["response"])
                self.assertIn("dataPreview", response_preview)
                self.assertEqual("c08-local", response_preview["dataPreview"]["service"])
            self.assertIn(report["sync_metadata"]["status"], {"not_configured", "PENDING", "PASS"})
            self.assertEqual(1, report["sync_metadata"]["code_count"])

            expected_files = (
                "interface-test-results.md",
                "responses.json",
                "dependency-graph.json",
                "scenario-results.json",
                "interface-sync-report.yaml",
                "inventory-reconcile.yaml",
                "release-test-plan.yaml",
                "artifacts/dependency-trace/health.json",
                "artifacts/raw-request/health.json",
                "artifacts/raw-response/health.json",
                "artifacts/masked-response/health.json",
                "artifacts/resolved-params/health.json",
                "artifacts/baseline-update-summary.yaml",
                "artifacts/logs/execute.log",
            )
            for relative_path in expected_files:
                self.assertTrue((output_dir / relative_path).is_file(), relative_path)

            details = (output_dir / "interface-test-results.md").read_text(encoding="utf-8")
            self.assertIn("【接口 1】", details)
            self.assertIn("简要响应", details)
            self.assertNotIn("| 接口", details)
            dependency_trace = json.loads((output_dir / "artifacts/dependency-trace/health.json").read_text(encoding="utf-8"))
            self.assertIsInstance(dependency_trace, list)
            graph = json.loads((output_dir / "dependency-graph.json").read_text(encoding="utf-8"))
            self.assertEqual(["health"], graph["order"])

            baseline = yaml.safe_load(baseline_path.read_text(encoding="utf-8"))
            self.assertEqual("2.0", baseline["schema_version"])
            self.assertEqual("PASS", baseline["latest_gate"]["gate"])
            self.assertEqual(["health"], [item["operation_id"] for item in baseline["interface_inventory"]])
            self.assertEqual(["health"], [item["operation_id"] for item in baseline["scenarios"]])
            self.assertEqual(result["run_id"], baseline["events"][0]["run_id"])
            event_result = baseline["events"][0]["payload"]["results"][0]
            self.assertIsInstance(event_result["response"], str)
            self.assertIn("dataPreview", json.loads(event_result["response"]))
            event_lines = baseline_path.with_suffix(".events.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(1, len(event_lines))
            self.assertEqual(result["run_id"], json.loads(event_lines[0])["run_id"])

            replayed = BaselineStore(baseline_path).project()
            self.assertEqual(baseline["events"], replayed["events"])
            summary = yaml.safe_load((output_dir / "artifacts" / "baseline-update-summary.yaml").read_text(encoding="utf-8"))
            self.assertTrue(summary["updated"])
            self.assertEqual("PASS", summary["projection_status"])
            self.assertEqual(1, summary["event_count"])

            evidence_root = Path(__file__).parents[1] / "evidence"
            for evidence_name in (
                "EVD-TASK-RT-C08-03-IMPL.md",
                "EVD-TASK-RT-C08-03-TEST.md",
                "EVD-TASK-RT-C08-03-REVIEW.md",
                "EVD-TASK-RT-C08-03-ACCEPT.md",
            ):
                evidence = (evidence_root / evidence_name).read_text(encoding="utf-8")
                self.assertIn("EVD-TASK-RT-C08-03", evidence)


if __name__ == "__main__":
    unittest.main()
