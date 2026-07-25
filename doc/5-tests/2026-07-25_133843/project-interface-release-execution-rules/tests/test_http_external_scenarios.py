"""C14 HTTP 常用负载消费者场景真实测试。"""

from __future__ import annotations

import hashlib
import sys
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

from external_http_fixture import DOWNLOAD_BYTES, UploadHandler
from release_test_engine.scenario_loader import load_scenario_catalog, promote_to_verified, source_fingerprint
from release_test_engine.scenario_runner import run_scenario
from scenario_verification_fixture import load_verified_catalog, promote_fixture_scenario, verification_evidence, verification_project_root


def scenario_document(scenario_id: str, steps: list[dict[str, Any]], cleanup: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """构造来源指纹正确的已验证场景目录。

    [参数] scenario_id: 场景标识；steps: 待执行步骤；cleanup: 主流程结束后必须执行的声明式清理。
    [返回] external-scenario/1.0 文档。
    最近修改时间：2026-07-26 00:30:00，HTTP 场景晋级绑定结构化验证摘要。
    """

    # 1. 测试场景使用固定来源证据，确保失败来自运行行为而非指纹漂移。
    evidence = [{"source": "test-openapi", "operation_id": scenario_id}]
    document = {
        "schema_version": "external-scenario/1.0",
        "scenarios": {
            scenario_id: {
                "scenario_id": scenario_id,
                "risk": "P0",
                "consumers": ["frontend.upload"],
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


def http_step(step_id: str, method: str, url: str, **config: Any) -> dict[str, Any]:
    """构造带 local 来源和成功断言的 HTTP 步骤。

    [参数] step_id: 步骤标识；method: HTTP 方法；url: 目标地址；config: 额外负载配置。
    [返回] 可直接加载的场景步骤。
    最近修改时间：2026-07-25 14:23:51，减少 C14 场景样本的非行为重复。
    """

    # 1. 每个步骤固定断言成功状态，负向样本通过服务端错误稳定触发失败。
    return {
        "step_id": step_id,
        "action": "http.request",
        "config": {"method": method, "url": url, "config_environment": "local", **config},
        "captures": {"object_id": "/body/id"} if method == "POST" else {},
        "assertions": [{"path": "/status", "op": "equal", "expected": 201 if method == "POST" else 200}],
        "parallel_group": "",
    }


class HttpExternalScenarioTest(unittest.TestCase):
    """验证 C14-01 的 form、multipart、读回和清理闭环。"""

    @classmethod
    def setUpClass(cls) -> None:
        """启动随机回环端口 HTTP 服务。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:23:51，建立 C14 真实网络测试环境。
        """

        # 1. fixture 只监听回环地址，后台线程在类级清理中强制回收。
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), UploadHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls) -> None:
        """关闭服务并等待线程退出。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:23:51，确保测试不残留端口或后台线程。
        """

        # 1. 先停止接收请求再关闭套接字，最后确认服务线程退出。
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def setUp(self) -> None:
        """清空上一测试可能留下的内存记录。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:33:26，隔离每个场景的本地对象与事件状态。
        """

        # 1. fixture 数据只存在当前进程内存，不接触项目数据库。
        UploadHandler.records.clear()
        UploadHandler.events.clear()
        UploadHandler.last_event_ids.clear()

    def _run(self, scenario_id: str, steps: list[dict[str, Any]], cleanup: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        """加载并执行一个已验证场景。

        [参数] scenario_id: 场景标识；steps: 串行步骤；cleanup: 无论主流程结果如何都执行的清理步骤。
        [返回] 场景执行结果。
        最近修改时间：2026-07-25 20:20:00，使测试资产通过正式顶层清理契约进入 runner。
        """

        # 1. 所有样本都经过正式 loader 和 runner，不绕过运行契约。
        catalog = load_verified_catalog(scenario_document(scenario_id, steps, cleanup))
        return run_scenario(catalog.scenarios[scenario_id])

    def test_form_submit_readback_and_cleanup(self) -> None:
        """验证 form 提交、读回和删除清理。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:23:51，覆盖 form 消费者闭环。
        """

        # 1. 创建后捕获对象标识，用于后续读回和清理步骤。
        steps = [http_step("create", "POST", f"{self.base_url}/form", form={"name": "alpha", "tags": ["a", "b"]})]
        steps.append(http_step("read", "GET", f"{self.base_url}/objects/${{capture.object_id}}"))
        steps[-1]["assertions"].append({"path": "/body/fields/name/0", "op": "equal", "expected": "alpha"})
        cleanup = [http_step("cleanup", "DELETE", f"{self.base_url}/objects/${{capture.object_id}}")]
        cleanup[0]["assertions"].append({"path": "/body/deleted", "op": "equal", "expected": 1})

        # 2. 两个主步骤和独立清理都必须通过，服务端状态最终为空。
        result = self._run("form-lifecycle", steps, cleanup)
        self.assertEqual("PASS", result["status"])
        self.assertEqual(2, len(result["steps"]))
        self.assertEqual("PASS", result["cleanup"][0]["status"])
        self.assertEqual({}, UploadHandler.records)

    def test_multipart_upload_readback_digest_and_cleanup(self) -> None:
        """验证 multipart 上传、摘要读回和删除清理。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:23:51，覆盖文件上传消费者闭环。
        """

        content = b"external-scenario-upload"
        digest = hashlib.sha256(content).hexdigest()

        # 1. 上传内容仅在请求内存中存在，服务端只保留长度和摘要。
        steps = [
            http_step(
                "upload",
                "POST",
                f"{self.base_url}/multipart",
                multipart={
                    "fields": {"purpose": "digest-check"},
                    "files": {"file": {"filename": "sample.bin", "content_type": "application/octet-stream", "content": content}},
                },
            )
        ]
        steps.append(http_step("read", "GET", f"{self.base_url}/objects/${{capture.object_id}}"))
        steps[-1]["assertions"].extend(
            [
                {"path": "/body/filename", "op": "equal", "expected": "sample.bin"},
                {"path": "/body/length", "op": "equal", "expected": len(content)},
                {"path": "/body/sha256", "op": "equal", "expected": digest},
            ]
        )
        cleanup = [http_step("cleanup", "DELETE", f"{self.base_url}/objects/${{capture.object_id}}")]
        cleanup[0]["assertions"].append({"path": "/body/deleted", "op": "equal", "expected": 1})

        # 2. 上传、读回和独立清理必须全部通过，场景结束后不得残留对象。
        result = self._run("multipart-lifecycle", steps, cleanup)
        self.assertEqual("PASS", result["status"])
        self.assertEqual({}, UploadHandler.records)

    def test_wrong_media_type_fails_deterministically(self) -> None:
        """验证错误媒体类型不会被误报为通过。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:23:51，增加 C14-01 必测失败样本。
        """

        # 1. 向 multipart 路由发送 form，服务端返回 415，步骤成功断言必须失败。
        steps = [http_step("upload", "POST", f"{self.base_url}/multipart", form={"name": "wrong-kind"})]
        cleanup = [http_step("cleanup-guard", "DELETE", f"{self.base_url}/objects/wrong-media-type")]
        cleanup[0]["assertions"].append({"path": "/body/deleted", "op": "equal", "expected": 0})
        result = self._run("wrong-media-type", steps, cleanup)
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("SCENARIO_ASSERTION_FAILED", result["failure_type"])
        self.assertEqual("PASS", result["cleanup"][0]["status"])

    def test_download_headers_length_and_digest(self) -> None:
        """验证下载头、字节长度和内容摘要。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:30:03，覆盖 C14-02 下载消费者正向闭环。
        """

        # 1. 下载断言同时约束协议头和实际响应体，避免只校验状态码。
        step = http_step("download", "GET", f"{self.base_url}/download")
        step["assertions"].extend(
            [
                {"path": "/headers/Content-Disposition", "op": "equal", "expected": 'attachment; filename="sample.bin"'},
                {"path": "/headers/Content-Length", "op": "equal", "expected": str(len(DOWNLOAD_BYTES))},
                {"path": "/body_length", "op": "equal", "expected": len(DOWNLOAD_BYTES)},
                {"path": "/body_sha256", "op": "equal", "expected": hashlib.sha256(DOWNLOAD_BYTES).hexdigest()},
            ]
        )
        result = self._run("download-binary", [step])
        self.assertEqual("PASS", result["status"])
        self.assertEqual(len(DOWNLOAD_BYTES), result["steps"][0]["output"]["body_bytes"]["length"])

    def test_wrong_download_digest_fails_deterministically(self) -> None:
        """验证错误下载摘要稳定失败。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:30:03，增加 C14-02 必测摘要错误样本。
        """

        # 1. 即使 HTTP 状态为 200，摘要不一致仍必须判定整个场景失败。
        step = http_step("download", "GET", f"{self.base_url}/download")
        step["assertions"].append({"path": "/body_sha256", "op": "equal", "expected": "0" * 64})
        result = self._run("download-wrong-digest", [step])
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("SCENARIO_ASSERTION_FAILED", result["failure_type"])

    def test_sse_subscribe_trigger_correlation_and_reconnect(self) -> None:
        """验证先订阅、HTTP 触发、事件关联和游标重连。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:33:26，覆盖 C14-03 SSE 正向消费者闭环。
        """

        # 1. 第一并行组必须先建立 SSE 订阅，再通过 HTTP 产生首个关联事件。
        first_sse = {
            "step_id": "expect-first",
            "action": "sse.expect",
            "config": {"url": f"{self.base_url}/events", "count": 1, "timeout_seconds": 3, "config_environment": "local"},
            "captures": {"last_event_id": "/events/0/id"},
            "assertions": [
                {"path": "/events/0/event", "op": "equal", "expected": "resource.changed"},
                {"path": "/events/0/data/correlation_id", "op": "equal", "expected": "corr-1"},
            ],
            "parallel_group": "first-event",
        }
        first_trigger = http_step("trigger-first", "POST", f"{self.base_url}/trigger", json={"correlation_id": "corr-1", "value": 1})
        first_trigger["assertions"][0]["expected"] = 202
        first_trigger["captures"] = {"first_object_id": "/body/object_id"}
        first_trigger["parallel_group"] = "first-event"

        # 2. 第二并行组携带首个事件游标，只接受游标之后的关联事件。
        second_sse = {
            "step_id": "expect-second",
            "action": "sse.expect",
            "config": {
                "url": f"{self.base_url}/events",
                "count": 1,
                "last_event_id": "${capture.last_event_id}",
                "timeout_seconds": 3,
                "config_environment": "local",
            },
            "captures": {},
            "assertions": [
                {"path": "/events/0/id", "op": "equal", "expected": "2"},
                {"path": "/events/0/data/correlation_id", "op": "equal", "expected": "corr-2"},
            ],
            "parallel_group": "second-event",
        }
        second_trigger = http_step("trigger-second", "POST", f"{self.base_url}/trigger", json={"correlation_id": "corr-2", "value": 2})
        second_trigger["assertions"][0]["expected"] = 202
        second_trigger["captures"] = {"second_object_id": "/body/object_id"}
        second_trigger["parallel_group"] = "second-event"

        # 3. 两次订阅均通过后，使用两个触发响应捕获的对象标识执行独立清理。
        cleanup = [
            http_step("cleanup-first", "DELETE", f"{self.base_url}/objects/${{capture.first_object_id}}"),
            http_step("cleanup-second", "DELETE", f"{self.base_url}/objects/${{capture.second_object_id}}"),
        ]
        for cleanup_step in cleanup:
            cleanup_step["assertions"].append({"path": "/body/deleted", "op": "equal", "expected": 1})
        result = self._run("sse-reconnect", [first_sse, first_trigger, second_sse, second_trigger], cleanup)
        self.assertEqual("PASS", result["status"])
        self.assertEqual(["", "1"], UploadHandler.last_event_ids)
        self.assertEqual(["sse.expect", "http.request", "sse.expect", "http.request"], [item["action"] for item in result["steps"]])
        self.assertEqual({}, UploadHandler.records)

    def test_sse_interrupted_stream_fails_deterministically(self) -> None:
        """验证半包断流稳定失败。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:33:26，增加 C14-03 必测断流样本。
        """

        # 1. 服务端未发送事件结束空行，客户端必须判定断流而不是接收成功。
        step = {
            "step_id": "expect",
            "action": "sse.expect",
            "config": {"url": f"{self.base_url}/events-disconnect", "count": 1, "timeout_seconds": 1, "config_environment": "local"},
            "captures": {},
            "assertions": [],
            "parallel_group": "",
        }
        result = self._run("sse-interrupted", [step])
        self.assertEqual("FAIL", result["status"])
        self.assertIn("SSE_STREAM_INTERRUPTED", result["reason"])

    def test_sse_wrong_correlation_fails_deterministically(self) -> None:
        """验证事件关联值不一致稳定失败。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:33:26，增加 C14-03 必测错误关联样本。
        """

        # 1. 真实事件到达但关联 ID 与消费者预期不同，场景级结果必须失败。
        expect_step = {
            "step_id": "expect",
            "action": "sse.expect",
            "config": {"url": f"{self.base_url}/events", "count": 1, "timeout_seconds": 3, "config_environment": "local"},
            "captures": {},
            "assertions": [{"path": "/events/0/data/correlation_id", "op": "equal", "expected": "corr-expected"}],
            "parallel_group": "wrong-correlation",
        }
        trigger_step = http_step("trigger", "POST", f"{self.base_url}/trigger", json={"correlation_id": "corr-actual"})
        trigger_step["assertions"][0]["expected"] = 202
        trigger_step["captures"] = {"object_id": "/body/object_id"}
        trigger_step["parallel_group"] = "wrong-correlation"
        cleanup = [http_step("cleanup", "DELETE", f"{self.base_url}/objects/event-1")]
        cleanup[0]["assertions"].append({"path": "/body/deleted", "op": "equal", "expected": 1})
        result = self._run("sse-wrong-correlation", [expect_step, trigger_step], cleanup)
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("SCENARIO_ASSERTION_FAILED", result["failure_type"])
        self.assertEqual({}, UploadHandler.records)


if __name__ == "__main__":
    unittest.main()
