"""Browser Use Cloud 预检的 local mock 回归。"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "browser-use-cloud-rules"
    / "scripts"
    / "browser_use_cloud_preflight.py"
)
SPEC = importlib.util.spec_from_file_location("browser_use_cloud_preflight", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("无法加载预检脚本")
PREFLIGHT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PREFLIGHT
SPEC.loader.exec_module(PREFLIGHT)
SENTINEL_KEY = "bu_test_secret_must_never_appear"


class _BillingServer:
    """为单个测试提供可关闭的 loopback Billing mock。"""

    def __init__(self, status: int, payload: Any, expected_key: str = SENTINEL_KEY):
        """初始化单次测试使用的本机账单服务。
        [参数] status: HTTP 状态码；payload: 响应体；expected_key: 预期哨兵 key
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐 local mock 初始化的注释契约
        """

        # 1. 保存测试输入与可观测状态，不记录真实凭据
        self.status = status
        self.payload = payload
        self.expected_key = expected_key
        self.seen_key: str | None = None
        owner = self

        # 2. 定义只服务当前测试实例的标准库请求处理器
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 - 标准库回调名固定
                """返回冻结的 Billing mock 响应。
                [参数] 无
                [返回] 无
                最近修改时间: 2026-07-26 13:56:24，补齐 mock GET 回调的注释契约
                """

                # 1. 记录收到的哨兵 key，仅供当前进程断言 header 是否正确
                owner.seen_key = self.headers.get(PREFLIGHT.API_KEY_HEADER)

                # 2. 把测试 payload 编码为 UTF-8 JSON 或直接使用损坏字节样本
                body = (
                    owner.payload
                    if isinstance(owner.payload, bytes)
                    else json.dumps(owner.payload).encode("utf-8")
                )

                # 3. 返回带完整长度的响应，确保客户端不会因传输不完整误判
                self.send_response(owner.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: object) -> None:
                """关闭标准库 HTTP 访问日志，避免测试输出携带 header。
                [参数] format: 标准库日志模板；args: 模板参数
                [返回] 无
                最近修改时间: 2026-07-26 13:56:24，补齐 mock 日志脱敏的注释契约
                """

                # 1. 明确丢弃本机 mock 访问日志，避免凭据进入 stderr
                return

        # 3. 只监听 loopback 随机端口，并准备可回收的后台线程
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        """返回当前 mock 的 loopback Billing URL。
        [参数] 无
        [返回] 包含随机端口的本机 URL
        最近修改时间: 2026-07-26 13:56:24，补齐 mock URL 的注释契约
        """

        # 1. 只构造 loopback 地址，不暴露外部网络入口
        return f"http://127.0.0.1:{self.server.server_port}/billing/account"

    def __enter__(self) -> "_BillingServer":
        """启动当前测试的 mock 服务。
        [参数] 无
        [返回] 已启动的当前 mock 实例
        最近修改时间: 2026-07-26 13:56:24，补齐 mock 启动的注释契约
        """

        # 1. 启动后台线程并把服务交给 with 作用域
        self.thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        """停止 mock 服务并回收后台线程。
        [参数] args: with 退出协议参数
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐 mock 清理的注释契约
        """

        # 1. 先停止请求循环并关闭监听端口
        self.server.shutdown()
        self.server.server_close()

        # 2. 等待后台线程退出，防止测试残留资源
        self.thread.join(timeout=2)


class BrowserUseCloudPreflightTests(unittest.TestCase):
    """覆盖 key、账单、余额、schema、URL 和脱敏契约。"""

    def setUp(self) -> None:
        """构造每个用例独立使用的账单样本。
        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐账单测试样本的注释契约
        """

        # 1. 同时放入允许字段与必须被剔除的身份字段
        self.billing = {
            "totalCreditsBalanceUsd": 12.5,
            "monthlyCreditsBalanceUsd": 10,
            "additionalCreditsBalanceUsd": 2.5,
            "rateLimit": 3,
            "planInfo": {
                "planName": "Free",
                "subscriptionId": "subscription-private",
            },
            "projectId": "project-private",
            "name": "person-private",
            "isFreeTier": True,
        }

    def _schema_file(self, payload: Any) -> tempfile.NamedTemporaryFile:
        """创建自动清理的 UTF-8 schema 临时文件。
        [参数] payload: 待写入的 schema 对象
        [返回] 已关闭但仍可读取的临时文件句柄
        最近修改时间: 2026-07-26 13:56:24，补齐 schema fixture 的注释契约
        """

        # 1. 以 UTF-8 写入独立 JSON 文件，避免依赖 shell 默认编码
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".json", delete=False
        )
        json.dump(payload, handle)
        handle.close()

        # 2. 注册无条件清理，测试完成后不留下 schema 文件
        self.addCleanup(Path(handle.name).unlink, missing_ok=True)
        return handle

    def _run(
        self,
        server: _BillingServer,
        schema: Any,
        action: str = "run_session",
    ) -> dict[str, Any]:
        """使用哨兵 key 运行一次预检。
        [参数] server: 当前 local mock；schema: 当前动作工具 schema；action: 收费动作
        [返回] 预检返回的脱敏结果
        最近修改时间: 2026-07-26 14:03:00，支持 run_session 与 send_task 独立预检
        """

        # 1. 创建 schema fixture，并只向显式 environ 注入哨兵 key
        schema_file = self._schema_file(schema)
        return PREFLIGHT.run_preflight(
            billing_url=server.url,
            schema_file=schema_file.name,
            timeout_seconds=2,
            action=action,
            environ={PREFLIGHT.API_KEY_ENV: SENTINEL_KEY},
        )

    def assert_secret_free(self, result: dict[str, Any]) -> None:
        """断言结果不含哨兵 key 和私有身份字段。
        [参数] result: 预检输出对象
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐无泄密断言的注释契约
        """

        # 1. 序列化完整结果后逐项检查所有禁止值
        rendered = json.dumps(result, ensure_ascii=False)
        for forbidden in (
            SENTINEL_KEY,
            "person-private",
            "project-private",
            "subscription-private",
        ):
            self.assertNotIn(forbidden, rendered)

    def test_missing_key_blocks_without_network(self) -> None:
        """验证缺 key 时在网络调用前返回固定提醒。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐缺 key 回归用例的注释契约
        """

        # 1. 指向不可用端口，以证明缺 key 分支不会发起网络请求
        result = PREFLIGHT.run_preflight(
            billing_url="http://127.0.0.1:1/not-called",
            schema_file=None,
            timeout_seconds=0.1,
            environ={},
        )

        # 2. 校验固定阻断状态与用户提醒
        self.assertEqual("blocked_key_missing", result["status"])
        self.assertEqual(PREFLIGHT.MISSING_KEY_REMINDER, result["reminder"])

    def test_401_and_403_block_auth(self) -> None:
        """验证 401 和 403 均归类为认证阻断。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐认证失败回归用例的注释契约
        """

        # 1. 分别模拟两种认证错误，并复核输出不泄密
        for status in (401, 403):
            with self.subTest(status=status), _BillingServer(status, {"detail": "denied"}) as server:
                result = self._run(server, {"properties": {"maxCostUsd": {"type": "number"}}})
                self.assertEqual("blocked_auth", result["status"])
                self.assert_secret_free(result)

    def test_billing_errors_fail_closed(self) -> None:
        """验证账户不存在、损坏 JSON 和字段缺失均失败关闭。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐 Billing 异常回归用例的注释契约
        """

        # 1. 覆盖 HTTP、解析和契约三类账单错误
        cases = (
            (404, {"detail": "Account not found"}),
            (200, b"not-json"),
            (200, {"totalCreditsBalanceUsd": 1}),
        )

        # 2. 每个错误都必须返回统一 Billing 阻断且不泄密
        for status, payload in cases:
            with self.subTest(status=status, payload=payload), _BillingServer(status, payload) as server:
                result = self._run(server, {"properties": {"maxCostUsd": {"type": "number"}}})
                self.assertEqual("blocked_billing", result["status"])
                self.assert_secret_free(result)

    def test_zero_credit_blocks(self) -> None:
        """验证零余额账户不能进入费用确认。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐零余额回归用例的注释契约
        """

        # 1. 把总余额归零后运行具有硬上限的正常 schema
        self.billing["totalCreditsBalanceUsd"] = 0
        with _BillingServer(200, self.billing) as server:
            result = self._run(server, {"properties": {"maxCostUsd": {"type": "number"}}})

        # 2. 余额阻断优先于费用确认，并保持输出脱敏
        self.assertEqual("blocked_no_credit", result["status"])
        self.assert_secret_free(result)

    def test_missing_hard_cap_blocks(self) -> None:
        """验证 schema 无硬费用上限时默认停止。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐无硬上限回归用例的注释契约
        """

        # 1. 使用只有保活字段的 schema，确保相似配置不会误判为费用上限
        with _BillingServer(200, self.billing) as server:
            result = self._run(server, {"properties": {"keep_alive": {"type": "boolean"}}})

        # 2. 校验专用阻断状态和硬上限可用性标记
        self.assertEqual("blocked_hard_cap_unavailable", result["status"])
        self.assertFalse(result["hard_cap_available"])

    def test_supported_hard_cap_is_ready(self) -> None:
        """验证 `maxCostUsd` 通过预检且 key 仅进入请求 header。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐标准硬上限回归用例的注释契约
        """

        # 1. 使用嵌套 schema 运行预检，并确认服务端收到哨兵 header
        with _BillingServer(200, self.billing) as server:
            result = self._run(
                server,
                {"inputSchema": {"properties": {"maxCostUsd": {"type": "number"}}}},
            )
            self.assertEqual(SENTINEL_KEY, server.seen_key)

        # 2. 校验可确认状态、实际命中字段、免费层和无泄密契约
        self.assertEqual("ready_for_confirmation", result["status"])
        self.assertEqual("maxCostUsd", result["hard_cap_field"])
        self.assertTrue(result["is_free_tier"])
        self.assert_secret_free(result)

    def test_output_schema_and_aliases_do_not_enable_hard_cap(self) -> None:
        """验证输出字段、描述和推测别名不能误放行硬上限。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 14:03:00，增加工具 schema 误判负向回归
        """

        # 1. 逐一覆盖 output schema、说明文本和推测别名
        cases = (
            {"outputSchema": {"properties": {"maxCostUsd": {"type": "number"}}}},
            {"description": "accepts maxCostUsd", "properties": {}},
            {"properties": {"max_cost_usd": {"type": "number"}}},
            {"properties": {"maxCostUsd": {"type": "string"}}},
            {"properties": {"maxCostUsd": {"type": "number", "readOnly": True}}},
        )

        # 2. 每种不可写 schema 都必须保持硬上限阻断
        for schema in cases:
            with self.subTest(schema=schema), _BillingServer(200, self.billing) as server:
                result = self._run(server, schema)
                self.assertEqual("blocked_hard_cap_unavailable", result["status"])

    def test_send_task_requires_its_own_writable_hard_cap(self) -> None:
        """验证 send_task 使用自身 schema 独立通过费用预检。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 14:03:00，增加 send_task 逐次预算回归
        """

        # 1. 使用 send_task 的可写 input schema 运行独立预检
        schema = {"inputSchema": {"properties": {"maxCostUsd": {"type": "number"}}}}
        with _BillingServer(200, self.billing) as server:
            result = self._run(server, schema, action="send_task")

        # 2. 校验动作回显和可确认状态，防止复用 run_session 授权
        self.assertEqual("send_task", result["action"])
        self.assertEqual("ready_for_confirmation", result["status"])

    def test_session_cleanup_uses_session_strategy_for_all_outcomes(self) -> None:
        """验证成功、失败和取消路径都要求销毁整个 session。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 14:03:00，增加三类任务结果的 session 清理回归
        """

        # 1. 用三种活跃状态代表成功收尾前、失败后和取消后的遗留 session
        cases = (("success", "idle"), ("failure", "running"), ("cancel", "created"))

        # 2. 每条路径都必须生成 strategy=session，禁止只停止当前 task
        for outcome, status in cases:
            with self.subTest(outcome=outcome, status=status):
                instruction = PREFLIGHT.build_session_cleanup_instruction({"status": status})
                self.assertTrue(instruction["stop_required"])
                self.assertEqual("session", instruction["stop_strategy"])

    def test_stopped_session_reports_valid_actual_costs(self) -> None:
        """验证最终 stopped 状态回读总费用和可用拆分费用。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 14:03:00，增加实际费用回读正向回归
        """

        # 1. 构造带完整实际费用字段的 stopped session
        instruction = PREFLIGHT.build_session_cleanup_instruction(
            {
                "status": "stopped",
                "totalCostUsd": 1.25,
                "llmCostUsd": 1,
                "proxyCostUsd": 0.2,
                "browserCostUsd": 0.05,
            }
        )

        # 2. 校验无需再次停止且费用保持服务端返回的精确十进制值
        self.assertFalse(instruction["stop_required"])
        self.assertEqual("1.25", instruction["actual_costs"]["totalCostUsd"])
        self.assertEqual("0.05", instruction["actual_costs"]["browserCostUsd"])

    def test_session_finalization_fails_closed_on_unknown_state_or_cost(self) -> None:
        """验证未知状态、未停止状态和异常费用不能伪装为清理完成。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 14:03:00，增加 session 收口失败关闭回归
        """

        # 1. 未知状态必须拒绝，仍活跃状态只能返回停止指令
        with self.assertRaises(ValueError):
            PREFLIGHT.build_session_cleanup_instruction({"status": "paused"})
        active = PREFLIGHT.build_session_cleanup_instruction({"status": "running"})
        self.assertTrue(active["stop_required"])

        # 2. stopped 状态缺总费用、费用为负或非有限时必须拒绝
        invalid_payloads = (
            {"status": "stopped"},
            {"status": "stopped", "totalCostUsd": -1},
            {"status": "stopped", "totalCostUsd": "NaN"},
            {"status": "stopped", "totalCostUsd": 1, "proxyCostUsd": -0.1},
        )
        for payload in invalid_payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                PREFLIGHT.build_session_cleanup_instruction(payload)

    def test_non_loopback_mock_url_is_blocked(self) -> None:
        """验证非官方且非 loopback 的 Billing URL 被拒绝。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐 URL 白名单回归用例的注释契约
        """

        # 1. 外部域名即使使用 HTTPS 也不能作为测试 Billing endpoint
        with self.assertRaises(ValueError):
            PREFLIGHT._validate_billing_url("https://example.com/billing")

    def test_cli_output_and_error_stream_never_include_secret(self) -> None:
        """验证 CLI stdout 和 stderr 均不出现凭据或身份字段。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 13:56:24，补齐 CLI 无泄密回归用例的注释契约
        """

        # 1. 准备有效 schema、local mock 与隔离的输出缓冲区
        schema_file = self._schema_file({"properties": {"maxCostUsd": {"type": "number"}}})
        with _BillingServer(200, self.billing) as server:
            original = dict(PREFLIGHT.os.environ)
            PREFLIGHT.os.environ[PREFLIGHT.API_KEY_ENV] = SENTINEL_KEY
            stdout = io.StringIO()
            stderr = io.StringIO()

            # 2. 临时替换当前模块环境变量，并在执行后无条件恢复
            try:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    exit_code = PREFLIGHT.main(
                        ["--billing-url", server.url, "--schema-file", schema_file.name]
                    )
            finally:
                PREFLIGHT.os.environ.clear()
                PREFLIGHT.os.environ.update(original)

        # 3. 校验退出码、双流脱敏和最终状态
        self.assertEqual(0, exit_code)
        output = stdout.getvalue() + stderr.getvalue()
        self.assertNotIn(SENTINEL_KEY, output)
        self.assertNotIn("person-private", output)
        self.assertEqual("ready_for_confirmation", json.loads(stdout.getvalue())["status"])

    def test_cli_missing_key_returns_exit_code_two(self) -> None:
        """验证缺 key 的 CLI 阻断状态固定返回退出码 2。

        [参数] 无
        [返回] 无
        最近修改时间: 2026-07-26 14:03:00，增加缺 key 退出码回归
        """

        # 1. 清空模块环境并捕获 stdout/stderr，避免真实进程环境影响用例
        original = dict(PREFLIGHT.os.environ)
        PREFLIGHT.os.environ.pop(PREFLIGHT.API_KEY_ENV, None)
        stdout = io.StringIO()
        stderr = io.StringIO()
        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = PREFLIGHT.main([])
        finally:
            PREFLIGHT.os.environ.clear()
            PREFLIGHT.os.environ.update(original)

        # 2. 校验退出码、固定状态和双流无泄密
        self.assertEqual(2, exit_code)
        self.assertEqual("blocked_key_missing", json.loads(stdout.getvalue())["status"])
        self.assertNotIn(SENTINEL_KEY, stdout.getvalue() + stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
