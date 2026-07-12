"""协议发现与未知 runner 降级的 local fixture 测试。"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.discovery import discover_project
from release_test_engine.model import InterfaceIR
from release_test_engine.runner import execute


class ProtocolAdapterTests(unittest.TestCase):
    """验证各协议 fixture 发现及未知执行不可伪报。"""

    def test_declarations_are_discovered_without_markdown_false_positive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schema.graphql").write_text("type Query { user(id: ID!): User }", encoding="utf-8")
            (root / "service.proto").write_text("service UserService { rpc GetUser (GetUserRequest) returns (User); }", encoding="utf-8")
            (root / "socket.py").write_text('@app.websocket("/ws")\nws.on("user.updated", handler)', encoding="utf-8")
            (root / "service.wsdl").write_text('<definitions xmlns="urn"><portType name="P"><operation name="Get"/></portType></definitions>', encoding="utf-8")
            (root / "rpc.json").write_text('{"jsonrpc":"2.0","method":"user.get"}', encoding="utf-8")
            (root / "handlers.py").write_text('@KafkaListener(topics=["users"])\n@Scheduled(cron="0 * * * *")\n@event_handler("user.created")', encoding="utf-8")
            (root / "README.md").write_text("type Query { fake: String } kafka consumer", encoding="utf-8")
            result = discover_project(root)
            protocols = {item.protocol for item in result.interfaces}
            self.assertTrue({"graphql", "grpc", "websocket", "soap", "jsonrpc", "message", "scheduler", "event"} <= protocols)
            self.assertFalse(any(item.evidence[0].get("source") == "README.md" for item in result.interfaces))

    def test_unknown_execution_is_pending_and_fixture_is_deterministic(self) -> None:
        interface = InterfaceIR("fp", "svc", "socket", "websocket", {"path": "/ws"})
        pending = execute(interface, environment="local")
        self.assertEqual("PENDING", pending.status)
        self.assertEqual("UNSUPPORTED_ADAPTER", pending.failure_type)
        fixture = InterfaceIR("fp", "svc", "socket", "websocket", {"path": "/ws", "fixture_response": {"status": "PASS", "body": {"ok": True}}})
        passed = execute(fixture, environment="local")
        self.assertEqual("PASS", passed.status)
        self.assertEqual("fixture", passed.evidence["transport"])

    def test_non_local_is_blocked_before_fixture(self) -> None:
        interface = InterfaceIR("fp", "svc", "socket", "grpc", {"fixture_response": {"status": "PASS"}})
        result = execute(interface, environment="production")
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("environment.non_local", result.failure_type)

    def test_rpc_endpoint_provenance_is_local_only(self) -> None:
        interface = InterfaceIR("fp", "svc", "query", "graphql", {"endpoint_ref": "graphql_endpoint"})
        with patch("release_test_engine.runner.urllib.request.urlopen", side_effect=AssertionError("remote endpoint must not be contacted")) as urlopen:
            result = execute(interface, environment="local", env={"graphql_endpoint": "https://prod.example"})
        urlopen.assert_not_called()
        self.assertEqual("BLOCKED", result.status)
        self.assertEqual("LOCAL_CONFIG_PROVENANCE_INVALID", result.failure_type)


if __name__ == "__main__":
    unittest.main()
