"""C13 外部场景契约、HTTP JSON 和生命周期真实测试。"""

from __future__ import annotations

import json
import sys
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
ENGINE_ROOT = ROOT / "project-interface-release-execution-rules" / "scripts"
TEST_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_ROOT))
sys.path.insert(0, str(TEST_ROOT))

from release_test_engine.scenario_generation import generate_candidates
from release_test_engine.scenario_loader import can_promote_to_verified, load_scenario_catalog, promote_to_verified, source_fingerprint
from release_test_engine.scenario_model import ScenarioValidationError
from release_test_engine.scenario_runner import run_scenario
from scenario_verification_fixture import load_verified_catalog, promote_fixture_scenario, verification_evidence, verification_project_root


class JsonHandler(BaseHTTPRequestHandler):
    """返回可跨步骤捕获的固定 JSON。"""

    def do_GET(self) -> None:  # noqa: N802
        """返回包含敏感字段和业务数据的确定性 JSON。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，增加真实 HTTP 超时负向响应路径。
        """

        # 1. slow 路径保持连接无响应直到客户端超时，用于验证网络异常不能逃逸 runner。
        if self.path == "/slow":
            time.sleep(0.2)
            return
        # 2. 敏感字段用于验证正式结果脱敏，业务字段用于跨步骤捕获。
        payload = json.dumps({"access_token": "runtime-secret-token", "data": {"id": "item-42", "state": "ready"}}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        """关闭 fixture 默认访问日志。

        [参数] format: 默认日志格式；args: 日志参数。
        [返回] 无。
        最近修改时间：2026-07-25 21:10:00，避免测试输出混入不可控访问日志。
        """

        return


def scenario_document(url: str) -> dict[str, object]:
    """构造来源指纹正确的场景目录。

    [参数] url: local HTTP 地址。
    [返回] external-scenario/1.0 场景文档。
    最近修改时间：2026-07-25 23:50:00，fixture 只构造 candidate 并禁止手写 verified。
    """

    # 1. 来源证据与指纹使用同一结构，确保失败只来自被测契约。
    evidence = [{"source": "test-openapi", "operation_id": "read-item"}]
    # 2. 场景身份、来源、步骤、清理和五项验证门槛按公共契约完整输出。
    return {
        "schema_version": "external-scenario/1.0",
        "scenarios": {
            "read-item": {
                "scenario_id": "read-item",
                "risk": "P0",
                "consumers": ["frontend.item-detail"],
                "source_evidence": evidence,
                "source_fingerprint": source_fingerprint(evidence),
                "lifecycle": "candidate",
                "preconditions": [{"environment": "local"}],
                "steps": [
                    {
                        "step_id": "read",
                        "action": "http.request",
                        "config": {"method": "GET", "url": url, "config_environment": "local"},
                        "captures": {"item_id": "/body/data/id"},
                        "assertions": [
                            {"path": "/status", "op": "equal", "expected": 200},
                            {"path": "/body/data/state", "op": "enum", "values": ["ready"]},
                        ],
                        "parallel_group": "",
                    }
                ],
                "assertions": [{"path": "/captures/item_id", "op": "equal", "expected": "item-42"}],
                "cleanup": [],
                "verification": {},
            }
        },
    }


def verified_document(url: str) -> dict[str, object]:
    """通过唯一晋级入口生成 verified 场景文档。

    [参数] url: local HTTP 地址。
    [返回] 带 external-verify/1.0 晋级证明的场景文档。
    最近修改时间：2026-07-26 00:30:00，测试用结构化运行摘要生成 verified。
    """

    # 1. 先加载 candidate，再由 promote_to_verified 生成可被 loader 重算的证明。
    candidate = load_scenario_catalog(scenario_document(url)).scenarios["read-item"]
    verified = promote_fixture_scenario(candidate)
    return {"schema_version": "external-scenario/1.0", "scenarios": {verified.scenario_id: verified.to_dict()}}


class ScenarioContractTest(unittest.TestCase):
    """验证 C13-01/02 的最小消费者闭环。"""

    @classmethod
    def setUpClass(cls) -> None:
        """启动随机回环端口 HTTP 服务。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:10:00，补齐 C13 真实网络测试环境说明。
        """

        # 1. 使用随机回环端口启动真实 HTTP 服务。
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), JsonHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_address[1]}/items/42"

    @classmethod
    def tearDownClass(cls) -> None:
        """关闭服务并等待线程退出。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:10:00，确保 C13 测试不残留端口或线程。
        """

        # 1. 关闭服务并等待线程退出，确保测试不残留端口。
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def test_verified_http_json_scenario_runs_over_network(self) -> None:
        """验证 verified HTTP JSON 场景通过真实网络并脱敏。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:50:00，正向场景改由唯一晋级入口生成 verified。
        """

        # 1. 场景必须经过 loader 和 runner，结果同时验证捕获、状态和脱敏。
        catalog = load_verified_catalog(verified_document(self.url))
        result = run_scenario(catalog.scenarios["read-item"])
        self.assertEqual("PASS", result["status"])
        self.assertEqual("item-42", result["captures"]["item_id"])
        self.assertEqual("PASS", result["steps"][0]["status"])
        self.assertNotIn("runtime-secret-token", json.dumps(result, ensure_ascii=False))
        self.assertEqual("***", result["steps"][0]["output"]["body"]["access_token"])

    def test_candidate_cannot_enter_release_runtime(self) -> None:
        """验证 candidate 不能伪装成正式发布运行。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:50:00，候选 fixture 与晋级证明测试保持分离。
        """

        # 1. candidate 可以加载和验证，但 runner 必须返回 PENDING。
        catalog = load_scenario_catalog(scenario_document(self.url))
        result = run_scenario(catalog.scenarios["read-item"])
        self.assertEqual("PENDING", result["status"])
        self.assertEqual("SCENARIO_NOT_VERIFIED", result["failure_type"])

    def test_http_timeout_returns_structured_transport_failure(self) -> None:
        """验证真实 HTTP 超时返回结构化 FAIL 而不是抛出异常。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，覆盖复审发现的 TimeoutError 逃逸边界。
        """

        # 1. 通过随机回环 HTTP 服务制造确定性超时，并仍走正式 verified 场景入口。
        timeout_url = self.url.split("/items/", 1)[0] + "/slow"
        document = scenario_document(timeout_url)
        document["scenarios"]["read-item"]["steps"][0]["config"]["timeout_seconds"] = 0.02
        candidate = load_scenario_catalog(document).scenarios["read-item"]
        result = run_scenario(promote_fixture_scenario(candidate))
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("SCENARIO_TRANSPORT_FAILED", result["failure_type"])
        self.assertEqual("deterministic scenario assertion or transport failed", result["reason"])

    def test_source_drift_and_unknown_action_are_rejected(self) -> None:
        """验证来源漂移和任意代码动作在加载阶段被拒绝。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:10:00，补齐来源与动作白名单负向契约。
        """

        # 1. 先验证来源指纹漂移，再验证未知动作不能进入 runtime。
        drifted = scenario_document(self.url)
        drifted["scenarios"]["read-item"]["source_fingerprint"] = "0" * 64
        with self.assertRaisesRegex(ScenarioValidationError, "source_fingerprint drifted"):
            load_scenario_catalog(drifted)
        invalid_action = scenario_document(self.url)
        invalid_action["scenarios"]["read-item"]["steps"][0]["action"] = "python.eval"
        with self.assertRaisesRegex(ScenarioValidationError, "action is not allowed"):
            load_scenario_catalog(invalid_action)

    def test_fault_injection_is_detected(self) -> None:
        """验证错误断言会失败且敏感样式的实际值不会进入失败原因。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-26 00:30:00，故障样本晋级绑定结构化正负运行摘要。
        """

        # 1. 即使期望值伪装成协议错误码前缀，断言异常也只能输出通用失败摘要。
        secret_expected = "WS_PRIVATE_TOKEN_VALUE"
        document = scenario_document(self.url)
        document["scenarios"]["read-item"]["steps"][0]["assertions"][0]["expected"] = secret_expected
        candidate = load_scenario_catalog(document).scenarios["read-item"]
        result = run_scenario(promote_fixture_scenario(candidate))
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("SCENARIO_ASSERTION_FAILED", result["failure_type"])
        self.assertNotIn(secret_expected, json.dumps(result, ensure_ascii=False))
        self.assertEqual("deterministic scenario assertion or transport failed", result["reason"])

    def test_verified_asset_cannot_bypass_verification_preconditions_or_cleanup(self) -> None:
        """验证手写 verified、非 local 前置条件和写场景空清理均被 loader 拒绝。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-26 00:30:00，增加五布尔直接晋级和缺运行证据阻断。
        """

        # 1. lifecycle 文本和五项布尔值不能替代 promote_to_verified 生成的晋级证明。
        invalid_verification = scenario_document(self.url)
        invalid_verification["scenarios"]["read-item"]["lifecycle"] = "verified"
        invalid_verification["scenarios"]["read-item"]["verification"] = {"contract_valid": True, "positive_passed": True, "fault_detected": True, "cleanup_passed": True, "source_current": True}
        with self.assertRaisesRegex(ScenarioValidationError, "structured runtime verification evidence"):
            load_scenario_catalog(invalid_verification)
        # 2. 已晋级文档的步骤被篡改后，候选指纹必须立即失效。
        tampered = verified_document(self.url)
        tampered["scenarios"]["read-item"]["steps"][0]["assertions"][0]["expected"] = 201
        with self.assertRaisesRegex(ScenarioValidationError, "structured runtime verification evidence"):
            load_verified_catalog(tampered)
        # 3. 缺 artifact root 或文件字节被篡改时，结构化摘要也不能自证晋级有效。
        artifact_tampered = verified_document(self.url)
        with self.assertRaisesRegex(ScenarioValidationError, "structured runtime verification evidence"):
            load_scenario_catalog(artifact_tampered)
        verification = artifact_tampered["scenarios"]["read-item"]["verification"]
        artifact_path = verification_project_root() / verification["artifact_path"]
        artifact_path.write_text(artifact_path.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(ScenarioValidationError, "structured runtime verification evidence"):
            load_verified_catalog(artifact_tampered)
        # 4. 前置条件必须匹配 local，HTTP 写入则必须声明清理。
        invalid_precondition = scenario_document(self.url)
        invalid_precondition["scenarios"]["read-item"]["preconditions"] = [{"environment": "production"}]
        with self.assertRaisesRegex(ScenarioValidationError, "environment: local"):
            load_scenario_catalog(invalid_precondition)
        missing_cleanup = scenario_document(self.url)
        missing_cleanup["scenarios"]["read-item"]["steps"][0]["config"]["method"] = "POST"
        candidate = load_scenario_catalog(missing_cleanup).scenarios["read-item"]
        with self.assertRaisesRegex(ScenarioValidationError, "write scenario requires cleanup"):
            promote_fixture_scenario(candidate)

    def test_generation_and_promotion_require_all_verification_gates(self) -> None:
        """验证生成结果固定为 candidate 且晋级要求五项全真。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-26 00:30:00，校验结构化运行摘要与五布尔负向样本。
        """

        # 1. 真实生成候选后分别验证不完整门槛、完整门槛和错误晋级。
        generated = generate_candidates(
            [{"protocol": "http", "operation_id": "read-item", "risk": "P1", "adapter": "openapi", "entrypoint": {"method": "GET", "path": "/items/{id}"}}],
            consumer="frontend.item-detail",
            source_name="openapi.yaml",
        )
        scenario = load_scenario_catalog(generated).scenarios["read-item"]
        self.assertEqual("candidate", scenario.lifecycle)
        self.assertFalse(can_promote_to_verified(scenario, {"contract_valid": True}, project_root=verification_project_root()))
        boolean_only = {"contract_valid": True, "positive_passed": True, "fault_detected": True, "cleanup_passed": True, "source_current": True}
        self.assertFalse(can_promote_to_verified(scenario, boolean_only, project_root=verification_project_root()))
        with self.assertRaisesRegex(ScenarioValidationError, "cannot be promoted"):
            promote_to_verified(scenario, boolean_only, project_root=verification_project_root())
        verification = verification_evidence(scenario)
        self.assertTrue(can_promote_to_verified(scenario, verification, project_root=verification_project_root()))
        verified = promote_to_verified(scenario, verification, project_root=verification_project_root())
        self.assertEqual("verified", verified.lifecycle)
        self.assertEqual("external-verify/1.0", verified.verification["method"])
        self.assertEqual(64, len(verified.verification["candidate_fingerprint"]))
        self.assertEqual(64, len(verified.verification["verification_digest"]))
        with self.assertRaisesRegex(ScenarioValidationError, "cannot be promoted"):
            promote_to_verified(scenario, {"contract_valid": True}, project_root=verification_project_root())


if __name__ == "__main__":
    unittest.main()
