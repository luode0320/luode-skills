"""C15 原生 WebSocket 与 Socket.IO 外部消费者真实测试。"""

from __future__ import annotations

import json
import socket
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

from external_http_fixture import UploadHandler
from socketio_fixture import SocketIOFixture
from release_test_engine.scenario_loader import load_scenario_catalog, promote_to_verified, source_fingerprint
from release_test_engine.scenario_runner import run_scenario
from scenario_verification_fixture import load_verified_catalog, promote_fixture_scenario, verification_evidence, verification_project_root


def scenario_document(scenario_id: str, steps: list[dict[str, Any]], cleanup: list[dict[str, Any]] | None = None, assertions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """构造一个来源指纹正确的实时场景目录。

    [参数] scenario_id: 场景标识；steps: 实时动作步骤；cleanup: 声明式清理；assertions: 场景级断言。
    [返回] external-scenario/1.0 文档。
    最近修改时间：2026-07-26 00:30:00，实时场景晋级绑定结构化验证摘要。
    """

    # 1. 所有测试都经过正式 loader 和 verified 运行入口，不注入 fixture PASS。
    evidence = [{"source": "test-asyncapi", "operation_id": scenario_id}]
    document = {
        "schema_version": "external-scenario/1.0",
        "scenarios": {
            scenario_id: {
                "scenario_id": scenario_id,
                "risk": "P0",
                "consumers": ["frontend.realtime"],
                "source_evidence": evidence,
                "source_fingerprint": source_fingerprint(evidence),
                "lifecycle": "candidate",
                "preconditions": [{"environment": "local"}],
                "steps": steps,
                "assertions": assertions or [],
                "cleanup": cleanup or [],
                "verification": {},
            }
        },
    }
    candidate = load_scenario_catalog(document).scenarios[scenario_id]
    verified = promote_fixture_scenario(candidate)
    return {"schema_version": "external-scenario/1.0", "scenarios": {scenario_id: verified.to_dict()}}


def ws_step(step_id: str, action: str, **config: Any) -> dict[str, Any]:
    """构造一个原生 WebSocket 步骤。

    [参数] step_id: 步骤标识；action: WebSocket 动作；config: 动作配置。
    [返回] 无并行组的可加载步骤。
    最近修改时间：2026-07-25 14:43:47，减少 C15-01 样本中的契约重复。
    """

    # 1. WebSocket 动作默认串行，保证握手、收发和关闭顺序与消费者一致。
    return {"step_id": step_id, "action": action, "config": config, "captures": {}, "assertions": [], "parallel_group": ""}


class WebSocketExternalScenarioTest(unittest.TestCase):
    """验证 C15-01 原生 RFC 6455 消费者闭环。"""

    @classmethod
    def setUpClass(cls) -> None:
        """启动随机回环端口 WebSocket 服务。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:43:47，建立原生 WebSocket 真实网络 fixture。
        """

        # 1. 官方同步服务运行在独立线程，并在类级清理中关闭监听端口。
        from websockets.sync.server import serve

        cls.server = serve(cls._handler, "127.0.0.1", 0)
        cls.port = cls.server.socket.getsockname()[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"ws://127.0.0.1:{cls.port}/events"

    @classmethod
    def tearDownClass(cls) -> None:
        """关闭 WebSocket 服务并等待线程退出。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:43:47，确保测试不残留实时服务端口。
        """

        # 1. 先关闭服务再等待线程，服务端会同步回收仍存活的连接处理器。
        cls.server.shutdown()
        cls.thread.join(timeout=3)

    @staticmethod
    def _handler(connection: Any) -> None:
        """按请求模式返回正常、乱序、重复或缺失消息。

        [参数] connection: websockets 服务端真实连接。
        [返回] 无。
        最近修改时间：2026-07-25 14:43:47，提供 C15-01 正反例协议行为。
        """

        # 1. 缺失 local 鉴权头时使用策略关闭码拒绝后续消费者动作。
        if connection.request.headers.get("Authorization") != "Bearer local-token":
            connection.close(code=1008, reason="auth required")
            return

        # 2. 每条客户端命令决定响应模式，服务端实际发送网络帧而非静态测试结果。
        for raw in connection:
            # 2.1 每条客户端命令生成两条带顺序和关联标识的事件。
            command = json.loads(raw)
            correlation_id = command["correlation_id"]
            mode = command.get("mode", "normal")
            first = {"event_id": f"{correlation_id}-1", "sequence": 1, "correlation_id": correlation_id}
            second = {"event_id": f"{correlation_id}-2", "sequence": 2, "correlation_id": correlation_id}
            messages = [first, second]
            if mode == "bad-order":
                # 2.2 乱序、重复和缺失模式只改变真实发送帧序列。
                messages = [second, first]
            elif mode == "duplicate":
                messages = [first, first]
            elif mode == "missing":
                messages = [first]
            for message in messages:
                connection.send(json.dumps(message, separators=(",", ":")))

    def _run(self, scenario_id: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
        """加载并执行一个原生 WebSocket 场景。

        [参数] scenario_id: 场景标识；steps: 场景步骤。
        [返回] 场景执行结果。
        最近修改时间：2026-07-25 14:43:47，统一 C15-01 正反例正式运行入口。
        """

        # 1. 运行结果必须来自真实场景 runner，不允许测试直接调用 transport 冒充门禁结果。
        catalog = load_verified_catalog(scenario_document(scenario_id, steps))
        return run_scenario(catalog.scenarios[scenario_id])

    def _conversation(self, mode: str = "normal", *, token: str = "local-token", session: str = "primary") -> list[dict[str, Any]]:
        """构造一次握手、发送、接收和关闭会话。

        [参数] mode: 服务端响应模式；token: 鉴权值；session: 会话标识。
        [返回] 原生 WebSocket 串行步骤。
        最近修改时间：2026-07-25 14:43:47，冻结 C15-01 消费者会话动作顺序。
        """

        # 1. 接收步骤同时验证顺序、关联值和重复策略，关闭步骤证明正常生命周期完成。
        correlation_id = f"corr-{mode}-{session}"
        connect_step = ws_step(
            "connect",
            "ws.connect",
            url=self.url,
            session=session,
            headers={"Authorization": f"Bearer {token}"},
            config_environment="local",
        )
        send_step = ws_step("send", "ws.send", session=session, json={"correlation_id": correlation_id, "mode": mode})
        expect_step = ws_step("expect", "ws.expect", session=session, count=2, timeout_seconds=0.3, duplicate_policy="reject", duplicate_path="/event_id")
        expect_step["assertions"] = [
            {"path": "/messages/0/sequence", "op": "equal", "expected": 1},
            {"path": "/messages/1/sequence", "op": "equal", "expected": 2},
            {"path": "/messages/1/correlation_id", "op": "equal", "expected": correlation_id},
            {"path": "/messages", "op": "ordered", "field": "/sequence", "direction": "asc"},
            {"path": "/messages", "op": "unique", "field": "/event_id"},
        ]
        close_step = ws_step("close", "ws.close", session=session, code=1000)
        return [connect_step, send_step, expect_step, close_step]

    def test_websocket_auth_send_order_close_and_reconnect(self) -> None:
        """验证鉴权、收发、顺序、关闭和同场景重连。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:43:47，覆盖 C15-01 完整正向闭环。
        """

        # 1. 两段同名会话串行执行，首次关闭后必须能够真实重新握手并再次收发。
        first = self._conversation(session="reconnect")
        second = self._conversation(session="reconnect")
        for index, step in enumerate(second):
            step["step_id"] = f"reconnect-{index + 1}"
        result = self._run("ws-reconnect", first + second)
        self.assertEqual("PASS", result["status"], result)
        self.assertEqual(8, len(result["steps"]))

    def test_websocket_auth_failure_is_detected(self) -> None:
        """验证鉴权失败不会被握手表象掩盖。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:43:47，增加 C15-01 鉴权负向样本。
        """

        # 1. 服务端以 1008 关闭未授权连接，后续动作必须使场景稳定失败。
        result = self._run("ws-auth-failure", self._conversation(token="wrong"))
        self.assertEqual("FAIL", result["status"])
        self.assertIn("WS_CONNECTION_CLOSED_1008", result["reason"])

    def test_websocket_refused_connection_returns_structured_failure(self) -> None:
        """验证关闭端口的 WebSocket 握手返回结构化 FAIL。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 21:59:37，覆盖 ConnectionRefusedError 逃逸边界。
        """

        # 1. 先由系统分配随机回环端口再关闭监听，真实握手必须稳定进入传输失败分支。
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe.bind(("127.0.0.1", 0))
        closed_port = probe.getsockname()[1]
        probe.close()
        step = ws_step("connect-refused", "ws.connect", url=f"ws://127.0.0.1:{closed_port}/events", timeout_seconds=0.2, config_environment="local")
        result = self._run("ws-connect-refused", [step])
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("SCENARIO_TRANSPORT_FAILED", result["failure_type"])
        self.assertEqual("deterministic scenario assertion or transport failed", result["reason"])

    def test_websocket_missing_out_of_order_and_duplicate_fail(self) -> None:
        """验证消息丢失、乱序和重复均稳定失败。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:43:47，覆盖 C15-01 三类必测事件故障。
        """

        # 1. 每类故障使用独立真实连接，避免一个关闭状态影响后续故障判定。
        results = {mode: self._run(f"ws-{mode}", self._conversation(mode=mode)) for mode in ("missing", "bad-order", "duplicate")}
        self.assertEqual("FAIL", results["missing"]["status"])
        self.assertIn("WS_MESSAGE_TIMEOUT", results["missing"]["reason"])
        self.assertEqual("FAIL", results["bad-order"]["status"])
        self.assertEqual("FAIL", results["duplicate"]["status"])
        self.assertIn("WS_DUPLICATE_MESSAGE", results["duplicate"]["reason"])


class SocketIOExternalScenarioTest(unittest.TestCase):
    """验证 C15-02 Socket.IO namespace/event/ack 消费者闭环。"""

    @classmethod
    def setUpClass(cls) -> None:
        """启动随机回环端口 Socket.IO 服务。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，建立 C15-02 真实协议 fixture。
        """

        # 1. 独立 fixture 使用 aiohttp Engine.IO 服务，不复用原生 WebSocket 模拟器。
        cls.fixture = SocketIOFixture()
        cls.fixture.start()
        cls.url = f"http://127.0.0.1:{cls.fixture.port}"

    @classmethod
    def tearDownClass(cls) -> None:
        """停止 Socket.IO 服务并回收线程。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，确保 Engine.IO 轮询和端口全部回收。
        """

        # 1. fixture 负责清理 aiohttp runner、事件循环和后台线程。
        cls.fixture.stop()

    def _run(self, scenario_id: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
        """加载并执行一个 Socket.IO 场景。

        [参数] scenario_id: 场景标识；steps: Socket.IO 步骤。
        [返回] 场景执行结果。
        最近修改时间：2026-07-25 14:50:26，统一 C15-02 正反例正式运行入口。
        """

        # 1. 所有结果都经过正式 runner，不直接调用客户端或服务端对象。
        catalog = load_verified_catalog(scenario_document(scenario_id, steps))
        return run_scenario(catalog.scenarios[scenario_id])

    def _steps(self, *, token: str = "local-token", mode: str = "normal") -> list[dict[str, Any]]:
        """构造 namespace 连接、emit/ack、expect 和 disconnect 步骤。

        [参数] token: namespace 鉴权值；mode: ack 响应模式。
        [返回] Socket.IO 串行消费者步骤。
        最近修改时间：2026-07-25 14:50:26，使用 Socket.IO 的 WebSocket transport 缩短发布测试清理时间。
        """

        correlation_id = f"socketio-{mode}"
        # 1. emit 断言真实 ack，expect 断言服务端通过 namespace 推送的关联事件。
        connect_step = {"step_id": "connect", "action": "socketio.connect", "config": {"url": self.url, "namespace": "/chat", "auth": {"token": token}, "transports": ["websocket"], "config_environment": "local"}, "captures": {}, "assertions": [], "parallel_group": ""}
        emit_step = {"step_id": "emit", "action": "socketio.emit", "config": {"event": "publish", "data": {"correlation_id": correlation_id, "mode": mode}, "timeout_seconds": 2}, "captures": {}, "assertions": [{"path": "/ack/accepted", "op": "equal", "expected": True}], "parallel_group": ""}
        expect_step = {"step_id": "expect", "action": "socketio.expect", "config": {"event": "published", "count": 1, "timeout_seconds": 2}, "captures": {}, "assertions": [{"path": "/events/0/data/correlation_id", "op": "equal", "expected": correlation_id}, {"path": "/events/0/data/state", "op": "equal", "expected": "visible"}], "parallel_group": ""}
        disconnect_step = {"step_id": "disconnect", "action": "socketio.disconnect", "config": {}, "captures": {}, "assertions": [], "parallel_group": ""}
        return [connect_step, emit_step, expect_step, disconnect_step]

    def test_socketio_namespace_event_and_ack(self) -> None:
        """验证 namespace、事件推送、ack 和断开。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，覆盖 C15-02 正向消费者闭环。
        """

        # 1. 四个真实动作必须全部 PASS，且最终显式断开 namespace 会话。
        result = self._run("socketio-publish", self._steps())
        self.assertEqual("PASS", result["status"])
        self.assertEqual(4, len(result["steps"]))

    def test_socketio_auth_and_ack_failures_are_detected(self) -> None:
        """验证 namespace 鉴权和 ack 错误稳定失败。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，增加 C15-02 必测负向样本。
        """

        # 1. 鉴权拒绝和错误 ack 使用独立真实客户端，任一均不得进入 PASS。
        auth_result = self._run("socketio-auth-failure", self._steps(token="wrong"))
        ack_result = self._run("socketio-ack-failure", self._steps(mode="bad-ack"))
        self.assertEqual("FAIL", auth_result["status"])
        self.assertIn("SOCKETIO_CONNECT_FAILED", auth_result["reason"])
        self.assertEqual("FAIL", ack_result["status"])


class CrossProtocolExternalScenarioTest(unittest.TestCase):
    """验证 C15-03 HTTP、SSE 和 HTTP 读回的消费者链。"""

    @classmethod
    def setUpClass(cls) -> None:
        """启动 HTTP/SSE 随机回环端口服务。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，建立跨协议真实闭环 fixture。
        """

        # 1. 使用与 C14 相同的真实 HTTP/SSE 服务语义，但独立监听端口和线程。
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), UploadHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls) -> None:
        """关闭跨协议服务并等待线程回收。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，确保跨协议测试无端口残留。
        """

        # 1. 关闭服务并等待处理线程退出，避免读回请求在测试结束后仍运行。
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def test_http_trigger_sse_event_and_http_readback(self) -> None:
        """验证 HTTP 写入、SSE 通知和 HTTP 最终读回一致。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 23:50:00，跨协议断言在 candidate 阶段写入后再晋级。
        """

        # 1. 先订阅 SSE，再由 HTTP 创建对象；事件捕获对象 ID 后通过 HTTP 读回最终状态。
        correlation_id = "cross-corr-1"
        sse_step = {
            "step_id": "expect-event",
            "action": "sse.expect",
            "config": {"url": f"{self.base_url}/events", "count": 1, "timeout_seconds": 3, "config_environment": "local"},
            "captures": {"object_id": "/events/0/data/object_id", "event_correlation": "/events/0/data/correlation_id"},
            "assertions": [{"path": "/events/0/data/correlation_id", "op": "equal", "expected": correlation_id}],
            "parallel_group": "cross-write",
        }
        trigger_step = {
            "step_id": "trigger-http",
            "action": "http.request",
            "config": {"method": "POST", "url": f"{self.base_url}/trigger", "json": {"correlation_id": correlation_id, "value": 7}, "config_environment": "local"},
            "captures": {},
            "assertions": [{"path": "/status", "op": "equal", "expected": 202}],
            "parallel_group": "cross-write",
        }
        readback_step = {
            "step_id": "readback-http",
            "action": "http.request",
            "config": {"method": "GET", "url": f"{self.base_url}/objects/${{capture.object_id}}", "config_environment": "local"},
            "captures": {"read_correlation": "/body/correlation_id"},
            "assertions": [
                {"path": "/status", "op": "equal", "expected": 200},
                {"path": "/body/correlation_id", "op": "equal", "expected": correlation_id},
                {"path": "/body/state", "op": "equal", "expected": "visible"},
                {"path": "/body/value", "op": "equal", "expected": 7},
            ],
            "parallel_group": "",
        }
        cleanup_step = {
            "step_id": "cleanup-http",
            "action": "http.request",
            "config": {"method": "DELETE", "url": f"{self.base_url}/objects/${{capture.object_id}}", "config_environment": "local"},
            "captures": {},
            "assertions": [{"path": "/status", "op": "equal", "expected": 200}, {"path": "/body/deleted", "op": "equal", "expected": 1}],
            "parallel_group": "",
        }
        document = scenario_document(
            "http-sse-http",
            [sse_step, trigger_step, readback_step],
            [cleanup_step],
            [{"path": "/captures/event_correlation", "op": "equal_path", "other_path": "/captures/read_correlation"}],
        )
        result = run_scenario(load_verified_catalog(document).scenarios["http-sse-http"])
        self.assertEqual("PASS", result["status"], result)
        self.assertEqual({}, UploadHandler.records)


if __name__ == "__main__":
    unittest.main()
