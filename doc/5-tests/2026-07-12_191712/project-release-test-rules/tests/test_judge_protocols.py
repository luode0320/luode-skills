"""协议错误和响应 schema 判定真值表。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).parents[5] / "project-release-test-rules" / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from release_test_engine.judge import judge
from release_test_engine.model import InterfaceIR


class ProtocolJudgeTests(unittest.TestCase):
    def _result(self, protocol: str, body: object) -> dict[str, object]:
        return {"operation_id": "op", "status": "PASS", "request": {}, "response": {"status": 200, "body": body}, "evidence": {}}

    def test_graphql_jsonrpc_and_soap_errors_are_fail(self) -> None:
        cases = (
            ("graphql", {"errors": [{"message": "bad"}]}),
            ("jsonrpc", {"error": {"code": -1}}),
            ("soap", "<soap:Fault>bad</soap:Fault>"),
        )
        for protocol, body in cases:
            interface = InterfaceIR("fp", "svc", "op", protocol, {})
            self.assertEqual("FAIL", judge(self._result(protocol, body), interface)["status"])

    def test_required_response_field_missing_is_fail(self) -> None:
        interface = InterfaceIR("fp", "svc", "op", "http", {}, response_schema={"required_fields": ["data.id"]})
        judged = judge(self._result("http", {"data": {"name": "Ada"}}), interface)
        self.assertEqual("FAIL", judged["status"])
        self.assertIn("data.id", judged["reason"])


if __name__ == "__main__":
    unittest.main()
