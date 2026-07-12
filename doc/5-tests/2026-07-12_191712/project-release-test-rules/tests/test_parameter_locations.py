"""HTTP 参数位置和 local provider 语义回归。"""

from __future__ import annotations

import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.model import InterfaceIR, ParameterIR
from release_test_engine.resolver import resolve_parameters
from release_test_engine.runner import execute


class _CaptureHandler(BaseHTTPRequestHandler):
    request_snapshot: dict[str, object] = {}

    def do_POST(self) -> None:  # noqa: N802 - HTTP protocol callback
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8") if length else ""
        _CaptureHandler.request_snapshot = {
            "path": urlparse(self.path).path,
            "query": parse_qs(urlparse(self.path).query),
            "header": self.headers.get("X-Trace"),
            "cookie": self.headers.get("Cookie"),
            "body": body,
        }
        payload = b'{"code":0,"data":{"ok":true}}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, _format: str, *_args: object) -> None:
        return


class ParameterLocationTests(unittest.TestCase):
    def test_parameter_namespace_isolated_and_required_value_unresolved(self) -> None:
        interface = InterfaceIR(
            "fp", "svc", "op", "http", {"method": "POST", "path": "/users/{id}", "base_url_ref": "local_config"},
            parameters=(
                ParameterIR("id", "path", required=True),
                ParameterIR("id", "query"),
                ParameterIR("trace", "header"),
            ),
        )
        result = resolve_parameters(interface, sources={"id": [{"type": "fixture", "value": "wrong-namespace"}]})
        self.assertEqual("wrong-namespace", result["resolved"]["id"])
        self.assertFalse(result["unresolved"])
        self.assertEqual("fixture", result["dependency_trace"][0]["source_type"])

    def test_http_binds_path_query_header_cookie_and_body_to_distinct_locations(self) -> None:
        with tempfile.TemporaryDirectory():
            server = ThreadingHTTPServer(("127.0.0.1", 0), _CaptureHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                interface = InterfaceIR(
                    "fp", "svc", "op", "http", {"method": "POST", "path": "/users/{path_id}", "base_url_ref": "local_config"},
                    parameters=(
                        ParameterIR("path_id", "path"), ParameterIR("filter", "query"),
                        ParameterIR("X-Trace", "header"), ParameterIR("session", "cookie"), ParameterIR("name", "body"),
                    ),
                )
                result = execute(interface, {"path_id": "u/1", "filter": "active", "X-Trace": "t-1", "session": "s-1", "name": "Ada"}, environment="local", env={"local_config": f"http://127.0.0.1:{server.server_port}"})
                self.assertEqual("PASS", result.status)
                snapshot = _CaptureHandler.request_snapshot
                self.assertEqual("/users/u/1", snapshot["path"])
                self.assertEqual(["active"], snapshot["query"]["filter"])
                self.assertEqual("t-1", snapshot["header"])
                self.assertEqual("session=s-1", snapshot["cookie"])
                self.assertEqual('{"name": "Ada"}', snapshot["body"])
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
