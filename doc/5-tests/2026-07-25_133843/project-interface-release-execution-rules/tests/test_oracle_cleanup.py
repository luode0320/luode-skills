"""C16 探针、外部结果优先和清理阻断真实测试。"""

from __future__ import annotations

import json
import socket
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
ENGINE_ROOT = ROOT / "project-interface-release-execution-rules" / "scripts"
TEST_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_ROOT))
sys.path.insert(0, str(TEST_ROOT))

from external_http_fixture import UploadHandler
from release_test_engine.local_probe import LocalProbeRegistry
from release_test_engine.report import write_report
from release_test_engine.scenario_assertions import ScenarioAssertionError, assert_document
from release_test_engine.scenario_loader import load_scenario_catalog, promote_to_verified, source_fingerprint
from release_test_engine.scenario_runner import run_scenario
from scenario_verification_fixture import load_verified_catalog, promote_fixture_scenario, verification_evidence, verification_project_root


def scenario_document(scenario_id: str, steps: list[dict[str, Any]], cleanup: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """构造包含探针或清理声明的 verified 场景。

    [参数] scenario_id: 场景标识；steps: 主流程步骤；cleanup: 声明式清理步骤。
    [返回] external-scenario/1.0 文档。
    最近修改时间：2026-07-26 00:30:00，探针和清理样本绑定结构化验证摘要。
    """

    # 1. 测试资产只包含动作、结构化参数和断言，不嵌入执行代码或原始 SQL。
    evidence = [{"source": "test-openapi", "operation_id": scenario_id}]
    document = {
        "schema_version": "external-scenario/1.0",
        "scenarios": {
            scenario_id: {
                "scenario_id": scenario_id,
                "risk": "P0",
                "consumers": ["frontend.lifecycle"],
                "source_evidence": evidence,
                "source_fingerprint": source_fingerprint(evidence),
                "lifecycle": "candidate",
                "preconditions": [{"environment": "local"}],
                "steps": steps,
                "assertions": [],
                "cleanup": cleanup or [],
                "verification": {},
            }
        },
    }
    candidate = load_scenario_catalog(document).scenarios[scenario_id]
    verified = promote_fixture_scenario(candidate)
    return {"schema_version": "external-scenario/1.0", "scenarios": {scenario_id: verified.to_dict()}}


class OracleCleanupTest(unittest.TestCase):
    """验证 C16-01/02 的受控探针和清理边界。"""

    @classmethod
    def setUpClass(cls) -> None:
        """启动随机回环 HTTP fixture。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，建立 local 探针和清理真实环境。
        """

        # 1. 只监听回环地址，fixture 数据全部保存在当前测试进程内存。
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), UploadHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls) -> None:
        """关闭 HTTP fixture 并回收端口线程。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，保证 C16 测试没有服务残留。
        """

        # 1. 停止服务、关闭套接字并等待线程退出。
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def setUp(self) -> None:
        """清理 fixture 内存状态。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，隔离每个探针和清理样本。
        """

        # 1. 不连接数据库、不读外部服务，只清空本地 fixture 状态。
        UploadHandler.records.clear()
        UploadHandler.events.clear()

    def test_allowlisted_probe_supplements_external_result(self) -> None:
        """验证 allowlist 只读探针补充外部 HTTP 结果。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，覆盖 C16-01 正向闭环。
        """

        # 1. 外部 HTTP 先读回成功，allowlist 探针再读取同一结构化对象状态。
        steps = [
            {"step_id": "create", "action": "http.request", "config": {"method": "POST", "url": f"{self.base_url}/form", "form": {"name": "probe"}, "config_environment": "local"}, "captures": {"object_id": "/body/id"}, "assertions": [{"path": "/status", "op": "equal", "expected": 201}], "parallel_group": ""},
            {"step_id": "probe", "action": "state.probe", "config": {"name": "record_state", "args": {"object_id": "${capture.object_id}"}, "config_environment": "local"}, "captures": {}, "assertions": [{"path": "/value/state", "op": "equal", "expected": "visible"}], "parallel_group": ""},
        ]
        cleanup = [{"step_id": "delete", "action": "http.request", "config": {"method": "DELETE", "url": f"{self.base_url}/objects/${{capture.object_id}}", "config_environment": "local"}, "assertions": [{"path": "/body/deleted", "op": "equal", "expected": 1}]}]
        registry = LocalProbeRegistry()
        registry.register_readonly("record_state", lambda args: {"state": "visible", "object_id": args["object_id"]})
        scenario = load_verified_catalog(scenario_document("probe-positive", steps, cleanup)).scenarios["probe-positive"]
        result = run_scenario(scenario, probe_registry=registry)
        self.assertEqual("PASS", result["status"])
        self.assertEqual("PASS", result["cleanup"][0]["status"])
        self.assertEqual({}, UploadHandler.records)

    def test_external_failure_stops_before_probe(self) -> None:
        """验证外部结果失败时探针不能伪造整体通过。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 20:25:00，为失败主流程补充可独立执行的清理证据。
        """

        # 1. 首个 HTTP 状态断言故意错误，探针 reader 不应被调用或改变主结论。
        calls: list[dict[str, Any]] = []
        steps = [{"step_id": "wrong", "action": "http.request", "config": {"method": "POST", "url": f"{self.base_url}/form", "form": {"name": "wrong"}, "config_environment": "local"}, "captures": {}, "assertions": [{"path": "/status", "op": "equal", "expected": 200}], "parallel_group": ""}, {"step_id": "probe", "action": "state.probe", "config": {"name": "should-not-run", "config_environment": "local"}, "captures": {}, "assertions": [], "parallel_group": ""}]
        cleanup = [{"step_id": "delete", "action": "http.request", "config": {"method": "DELETE", "url": f"{self.base_url}/objects/form-1", "config_environment": "local"}, "assertions": [{"path": "/body/deleted", "op": "equal", "expected": 1}]}]
        registry = LocalProbeRegistry()
        registry.register_readonly("should-not-run", lambda args: calls.append(args) or {"state": "visible"})
        scenario = load_verified_catalog(scenario_document("external-priority", steps, cleanup)).scenarios["external-priority"]
        result = run_scenario(scenario, probe_registry=registry)
        self.assertEqual("FAIL", result["status"])
        self.assertEqual([], calls)
        self.assertEqual("PASS", result["cleanup"][0]["status"])
        self.assertEqual({}, UploadHandler.records)

    def test_probe_security_boundaries_are_blocked(self) -> None:
        """验证非 local、非 allowlist 和原始 SQL 探针均阻断。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，覆盖 C16-01 安全边界失败样本。
        """

        # 1. 三类越权配置分别运行，均必须返回 BLOCKED 而非 PENDING 或 PASS。
        registry = LocalProbeRegistry()
        registry.register_readonly("allowed", lambda args: {"ok": True})
        samples = [{"name": "missing", "config_environment": "local"}, {"name": "allowed", "config_environment": "staging"}, {"name": "allowed", "sql": "select 1", "config_environment": "local"}]
        for index, config in enumerate(samples):
            step = {"step_id": f"probe-{index}", "action": "state.probe", "config": config, "captures": {}, "assertions": [], "parallel_group": ""}
            scenario = load_verified_catalog(scenario_document(f"probe-block-{index}", [step])).scenarios[f"probe-block-{index}"]
            result = run_scenario(scenario, probe_registry=registry)
            self.assertEqual("BLOCKED", result["status"])

    def test_cleanup_failure_blocks_even_after_main_pass(self) -> None:
        """验证清理失败升级 BLOCKED 并保留清理报告。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，覆盖 C16-02 清理阻断样本。
        """

        # 1. 主流程创建成功，但清理使用不存在对象并要求 deleted=1，必须阻断最终结果。
        self.addCleanup(UploadHandler.records.clear)
        steps = [{"step_id": "create", "action": "http.request", "config": {"method": "POST", "url": f"{self.base_url}/form", "form": {"name": "leak"}, "config_environment": "local"}, "captures": {}, "assertions": [{"path": "/status", "op": "equal", "expected": 201}], "parallel_group": ""}]
        cleanup = [{"step_id": "bad-delete", "action": "http.request", "config": {"method": "DELETE", "url": f"{self.base_url}/objects/missing", "config_environment": "local"}, "assertions": [{"path": "/body/deleted", "op": "equal", "expected": 1}]}]
        scenario = load_verified_catalog(scenario_document("cleanup-block", steps, cleanup)).scenarios["cleanup-block"]
        result = run_scenario(scenario)
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("CLEANUP_FAILED", result["failure_type"])
        self.assertEqual(1, len(result["cleanup"]))

    def test_cleanup_failure_reason_redacts_sensitive_assertion_value(self) -> None:
        """验证清理断言失败不会持久化敏感 expected 值。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-26 00:35:00，直接回读 cleanup-report.json 验证落盘脱敏。
        """

        # 1. expected 故意使用敏感样式值，正式结果只能保留通用失败摘要。
        secret = "token-sensitive-cleanup-value"
        self.addCleanup(UploadHandler.records.clear)
        steps = [{"step_id": "create", "action": "http.request", "config": {"method": "POST", "url": f"{self.base_url}/form", "form": {"name": "redact"}, "config_environment": "local"}, "captures": {}, "assertions": [{"path": "/status", "op": "equal", "expected": 201}], "parallel_group": ""}]
        cleanup = [{"step_id": "bad-delete", "action": "http.request", "config": {"method": "DELETE", "url": f"{self.base_url}/objects/missing", "config_environment": "local"}, "assertions": [{"path": "/body/deleted", "op": "equal", "expected": secret}]}]
        scenario = load_verified_catalog(scenario_document("cleanup-redaction", steps, cleanup)).scenarios["cleanup-redaction"]
        result = run_scenario(scenario)
        serialized = str(result)
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("CLEANUP_FAILED", result["failure_type"])
        self.assertNotIn(secret, serialized)
        self.assertEqual("deterministic scenario assertion or transport failed", result["cleanup"][0]["reason"])
        # 2. 正式 cleanup-report.json 回读后同样不得出现 expected 敏感值。
        with tempfile.TemporaryDirectory() as directory:
            write_report(Path(directory), [], {"gate": "BLOCKED", "allow_release": False}, run_id="cleanup-redaction-run", environment="local", scenario_results=[result])
            cleanup_report = json.loads((Path(directory) / "cleanup-report.json").read_text(encoding="utf-8"))
        self.assertNotIn(secret, json.dumps(cleanup_report, ensure_ascii=False))
        self.assertEqual("deterministic scenario assertion or transport failed", cleanup_report["scenarios"][0]["steps"][0]["reason"])

    def test_cleanup_transport_failure_returns_blocked_result(self) -> None:
        """验证清理阶段拒绝连接返回结构化 BLOCKED 而不是抛出异常。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，覆盖清理动作的 OSError 归一化边界。
        """

        # 1. 主流程真实写入 local fixture，清理使用系统分配后关闭的随机回环端口。
        self.addCleanup(UploadHandler.records.clear)
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe.bind(("127.0.0.1", 0))
        closed_port = probe.getsockname()[1]
        probe.close()
        steps = [{"step_id": "create", "action": "http.request", "config": {"method": "POST", "url": f"{self.base_url}/form", "form": {"name": "cleanup-transport"}, "config_environment": "local"}, "captures": {}, "assertions": [{"path": "/status", "op": "equal", "expected": 201}], "parallel_group": ""}]
        cleanup = [{"step_id": "closed-port", "action": "http.request", "config": {"method": "DELETE", "url": f"http://127.0.0.1:{closed_port}/objects/form-1", "timeout_seconds": 0.2, "config_environment": "local"}, "assertions": []}]
        scenario = load_verified_catalog(scenario_document("cleanup-transport-block", steps, cleanup)).scenarios["cleanup-transport-block"]
        result = run_scenario(scenario)
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("CLEANUP_FAILED", result["failure_type"])
        self.assertEqual("declared cleanup did not complete", result["reason"])

    def test_cross_protocol_value_mismatch_fails_deterministically(self) -> None:
        """验证跨协议捕获值不一致稳定失败。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 15:00:00，覆盖 C16-03 equal_path 负向 oracle。
        """

        # 1. 同一场景文档中的事件值和读回值不同，必须抛出确定性断言错误。
        document = {"captures": {"event_correlation": "corr-event", "read_correlation": "corr-read"}}
        with self.assertRaisesRegex(ScenarioAssertionError, "cross-path values differ"):
            assert_document(document, [{"path": "/captures/event_correlation", "op": "equal_path", "other_path": "/captures/read_correlation"}])
