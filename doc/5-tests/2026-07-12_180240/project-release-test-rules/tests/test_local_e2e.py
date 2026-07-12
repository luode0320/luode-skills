"""local 环境上线测试引擎的独立端到端 fixture。

测试项目在临时目录中生成，HTTP 服务只监听回环地址，确保不会读取或连接
test/prod/staging 配置。每个测试都验证可观察产物，而不是只断言函数返回值。
"""

from __future__ import annotations

import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import yaml

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.cli import run_pipeline
from release_test_engine.discovery import discover_project
from release_test_engine.graph import build_dependency_graph, topological_order
from release_test_engine.judge import aggregate, judge
from release_test_engine.model import InterfaceIR, ParameterIR
from release_test_engine.resolver import resolve_parameters
from release_test_engine.runner import execute


class _LocalHandler(BaseHTTPRequestHandler):
    """提供无外部依赖的 provider/consumer HTTP 响应。"""

    def _write(self, status: int, payload: dict[str, object]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler protocol name
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._write(200, {"code": 0, "data": {"service": "fixture"}})
            return
        if parsed.path == "/lookup":
            self._write(200, {"code": 0, "data": {"user_id": "u-local-1"}})
            return
        self._write(404, {"code": 404, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler protocol name
        parsed = urlparse(self.path)
        if parsed.path != "/orders":
            self._write(404, {"code": 404, "error": "not found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b"{}"
        try:
            params = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            params = {}
        if not params:
            from urllib.parse import parse_qs
            params = {key: values[0] for key, values in parse_qs(parsed.query).items() if values}
        self._write(200, {"code": 0, "data": {"user_id": params.get("user_id", "")}})

    def log_message(self, _format: str, *_args: object) -> None:
        return


class LocalE2ETests(unittest.TestCase):
    """验证 local HTTP 运行链路和不可伪报的阻断状态。"""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _LocalHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        self.temp_dir.cleanup()

    def _write_openapi_project(self) -> None:
        document = {
            "openapi": "3.0.3",
            "info": {"title": "local fixture", "version": "1.0.0"},
            "paths": {
                "/health": {
                    "get": {"operationId": "health", "responses": {"200": {"description": "ok"}}}
                },
                "/lookup": {
                    "get": {"operationId": "lookup_user", "responses": {"200": {"description": "ok"}}}
                },
                "/orders": {
                    "post": {
                        "operationId": "create_order",
                        "parameters": [{"name": "user_id", "in": "query", "required": True, "schema": {"type": "string"}}],
                        "responses": {"200": {"description": "created"}},
                    }
                },
            },
        }
        (self.root / "openapi.yaml").write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    def test_pipeline_discovers_executes_reports_and_projects_baseline(self) -> None:
        self._write_openapi_project()
        output_dir = self.root / "artifacts"
        baseline_path = self.root / "baseline.yaml"
        result = run_pipeline(
            self.root,
            output_dir=output_dir,
            baseline_path=baseline_path,
            reusable={"params": {"user_id": [{"status": "reusable", "value": "u-local-1"}]}},
            environment="local",
            env={"local_config": self.base_url},
        )

        self.assertEqual("PASS", result["status"])
        self.assertEqual(3, len(result["interfaces"]))
        self.assertEqual(3, result["gate"]["passed"])
        self.assertTrue((output_dir / "interface-test-results.md").is_file())
        self.assertTrue((output_dir / "release-test-report.json").is_file())
        report = json.loads((output_dir / "release-test-report.json").read_text(encoding="utf-8"))
        self.assertEqual("PASS", report["gate"]["gate"])
        self.assertTrue(all(isinstance(item["reason"], str) for item in report["results"]))
        self.assertTrue(all(isinstance(item.get("request"), str) for item in report["results"]))
        self.assertTrue(all(isinstance(item.get("response"), str) for item in report["results"]))
        for item in report["results"]:
            json.loads(item["request"])
            json.loads(item["response"])
        baseline = yaml.safe_load(baseline_path.read_text(encoding="utf-8"))
        self.assertEqual("2.0", baseline["schema_version"])
        self.assertEqual("execution.completed", baseline["events"][0]["event_type"])
        self.assertEqual(1, len(baseline["events"]))
        events = baseline_path.with_suffix(".events.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(1, len(events))
        self.assertEqual(result["run_id"], json.loads(events[0])["run_id"])

    def test_discovery_parameter_resolution_and_dependency_order_are_deterministic(self) -> None:
        self._write_openapi_project()
        discovery = discover_project(self.root)
        self.assertEqual({"health", "lookup_user", "create_order"}, {item.operation_id for item in discovery.interfaces})

        provider = InterfaceIR(
            project_fingerprint="fixture",
            service_id="api",
            operation_id="lookup_user",
            protocol="http",
            entrypoint={"method": "GET", "path": "/lookup", "base_url_ref": "local_config"},
        )
        consumer = InterfaceIR(
            project_fingerprint="fixture",
            service_id="api",
            operation_id="create_order",
            protocol="http",
            entrypoint={"method": "POST", "path": "/orders", "base_url_ref": "local_config"},
            parameters=(ParameterIR(name="user_id", location="query", required=True, source={"interface": "lookup_user", "response_path": "$.data.user_id"}),),
        )
        graph = build_dependency_graph([consumer, provider])
        self.assertEqual(["lookup_user", "create_order"], graph["order"])
        self.assertEqual(["lookup_user", "create_order"], topological_order(graph["nodes"], graph["edges"]))
        resolved = resolve_parameters(consumer, sources={"user_id": [{"type": "upstream_api", "value": "u-local-1", "value_ref": "lookup_user$.data.user_id"}]})
        self.assertEqual({"user_id": "u-local-1"}, resolved["resolved"])
        self.assertFalse(resolved["unresolved"])
        self.assertEqual("upstream_api", resolved["dependency_trace"][0]["source_type"])

    def test_http_judge_and_non_local_safety_block(self) -> None:
        interface = InterfaceIR(
            project_fingerprint="fixture",
            service_id="api",
            operation_id="health",
            protocol="http",
            entrypoint={"method": "GET", "path": "/health", "base_url_ref": "local_config"},
            response_schema={"code_path": "$.body.code", "success_values": [0]},
        )
        executed = execute(interface, environment="local", env={"local_config": self.base_url})
        self.assertEqual("PASS", executed.status)
        judged = judge(executed.to_dict(), interface)
        self.assertEqual("PASS", judged["status"])
        self.assertEqual("PASS", aggregate([judged], [interface])["gate"])

        provider = InterfaceIR(
            project_fingerprint="fixture",
            service_id="api",
            operation_id="lookup_user",
            protocol="http",
            entrypoint={"method": "GET", "path": "/lookup", "base_url_ref": "local_config"},
        )
        consumer = InterfaceIR(
            project_fingerprint="fixture",
            service_id="api",
            operation_id="create_order",
            protocol="http",
            entrypoint={"method": "POST", "path": "/orders", "base_url_ref": "local_config"},
            parameters=(ParameterIR(name="user_id", location="body", required=True),),
            response_schema={"code_path": "$.body.code", "success_values": [0]},
        )
        provider_result = execute(provider, environment="local", env={"local_config": self.base_url})
        self.assertEqual("PASS", provider_result.status)
        user_id = provider_result.response["body"]["data"]["user_id"]
        consumer_result = execute(consumer, {"user_id": user_id}, environment="local", env={"local_config": self.base_url})
        self.assertEqual("PASS", consumer_result.status)
        self.assertEqual(user_id, consumer_result.response["body"]["data"]["user_id"])

        blocked = execute(interface, environment="production")
        self.assertEqual("BLOCKED", blocked.status)
        self.assertEqual("environment.non_local", blocked.failure_type)
        provenance_blocked = execute(interface, environment="local", env={"base_url": "https://prod.example"})
        self.assertEqual("BLOCKED", provenance_blocked.status)
        self.assertEqual("LOCAL_CONFIG_PROVENANCE_INVALID", provenance_blocked.failure_type)
        dangerous = InterfaceIR(
            project_fingerprint="fixture",
            service_id="admin",
            operation_id="drop_schema",
            protocol="cli",
            entrypoint={"command": "DROP TABLE accounts"},
        )
        safety_blocked = execute(dangerous, environment="local")
        self.assertEqual("BLOCKED", safety_blocked.status)
        self.assertEqual("sql.drop", safety_blocked.failure_type)


if __name__ == "__main__":
    unittest.main()
