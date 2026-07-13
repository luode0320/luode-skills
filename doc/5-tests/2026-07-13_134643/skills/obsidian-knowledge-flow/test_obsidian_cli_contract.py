"""契约测试：Windows adapter 仅通过 fake CLI 验证公开 JSON 协议。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
ADAPTER_PATH = REPOSITORY_ROOT / "obsidian-knowledge-flow/scripts/obsidian_cli_windows.ps1"
FAKE_CLI_PATH = Path(__file__).with_name("fixtures") / "fake_obsidian_cli.py"
POWERSHELL = "powershell.exe"
VAULT_ROOT = r"D:\obsidian_data"
KNOWLEDGE_PREFIX = "\u77e5\u8bc6\u5e93/"


def build_request(operation: str, **values: object) -> dict[str, object]:
    """构造 adapter v1 请求，并只覆盖当前测试所需字段。

    [参数] operation: 本次测试的公开操作；values: 操作定制字段。
    [返回] 可直接按 UTF-8 写入请求文件的 JSON 对象。
    最近修改时间: 2026-07-13 为 TASK-OBS-03 固化统一 request 默认值。
    """
    # 1. 默认值必须和 bridge 输出保持一致，避免测试绕过正式契约。
    request: dict[str, object] = {
        "schema_version": 1,
        "operation": operation,
        "vault_root": VAULT_ROOT,
        "knowledge_prefix": KNOWLEDGE_PREFIX,
        "timeout_seconds": 30,
        "auto_start": True,
        "startup_wait_seconds": 1,
        "verify_readback": True,
        "chunk_chars": 1800,
    }
    request.update(values)
    return request


class ObsidianCliAdapterContractTest(unittest.TestCase):
    """用本地 fake CLI 覆盖 adapter 的稳定行为和错误映射。"""

    def run_adapter(self, request: dict[str, object], **environment: str) -> tuple[int, dict[str, object]]:
        """执行 PowerShell adapter 并读取它唯一允许的 response JSON。

        [参数] request: 已冻结的 bridge request；environment: fake CLI 的本地测试状态。
        [返回] adapter 进程退出码与结构化 JSON response。
        最近修改时间: 2026-07-13 通过临时 JSON 与环境 seam 避免调用真实 Obsidian。
        """
        # 1. fake CLI 和状态文件都位于临时目录，不读写真实 vault。
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request_path = root / "request.json"
            response_path = root / "response.json"
            state_path = root / "fake-state.md"
            request_path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
            env = os.environ.copy()
            env.update(
                {
                    "OBSIDIAN_CLI_PATH": str(FAKE_CLI_PATH),
                    "OBSIDIAN_APP_PATH": str(FAKE_CLI_PATH),
                    "FAKE_OBSIDIAN_STATE": str(state_path),
                    "OBSIDIAN_TEST_PYTHON": sys.executable,
                    "PYTHONUTF8": "1",
                }
            )
            env.update(environment)
            completed = subprocess.run(
                [
                    POWERSHELL,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(ADAPTER_PATH),
                    "-RequestPath",
                    str(request_path),
                    "-ResponsePath",
                    str(response_path),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                env=env,
                timeout=180,
            )
            self.assertTrue(response_path.exists(), completed.stderr)
            return completed.returncode, json.loads(response_path.read_text(encoding="utf-8"))

    def test_doctor_returns_the_unique_fixed_vault_selector(self) -> None:
        """验证 doctor 先探活再按固定 root 唯一解析 selector。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖成功路径与固定 vault 根。
        """
        code, response = self.run_adapter(build_request("doctor"))
        self.assertEqual(0, code, response)
        self.assertTrue(response["ok"])
        self.assertEqual("OK", response["code"])
        self.assertEqual("main", response["vault_selector"])
        self.assertTrue(response["verified"])

    def test_auto_starts_once_when_the_application_is_unavailable(self) -> None:
        """验证应用不可达时仅隐藏启动一次并在等待窗口内恢复。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖一次启动与轮询恢复契约。
        """
        with tempfile.TemporaryDirectory() as directory:
            ready_path = Path(directory) / "ready.txt"
            code, response = self.run_adapter(
                build_request("doctor"),
                FAKE_OBSIDIAN_MODE="app_unavailable",
                FAKE_OBSIDIAN_READY=str(ready_path),
            )
        self.assertEqual(0, code)
        self.assertTrue(response["started_app"])
        self.assertGreaterEqual(response["attempts"], 2)

    def test_zero_and_multiple_matching_vaults_are_stable_errors(self) -> None:
        """验证没有匹配根或有多个 selector 时都不会执行 vault 操作。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖零匹配、多匹配的 vault 锁定错误。
        """
        cases = (
            ("other|D:\\other", "VAULT_NOT_REGISTERED"),
            ("one|D:\\obsidian_data;two|D:\\obsidian_data", "VAULT_ROOT_AMBIGUOUS"),
        )
        for vaults, expected in cases:
            with self.subTest(expected=expected):
                code, response = self.run_adapter(build_request("doctor"), FAKE_OBSIDIAN_VAULTS=vaults)
                self.assertEqual(5, code)
                self.assertFalse(response["ok"])
                self.assertEqual(expected, response["code"])

    def test_vault_listing_semantic_error_with_zero_exit_is_rejected(self) -> None:
        """验证无 selector/root 结构的 Error 文本映射为 CLI_FAILED。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 15:59:48 区分无效 vault 列表与合法 Error: selector。
        """
        # 1. 只有缺少 vault 记录结构的 Error: 才是 CLI 失败，不能误伤用户命名的 selector。
        code, response = self.run_adapter(build_request("doctor"), FAKE_OBSIDIAN_MODE="vaults_semantic_error")
        self.assertEqual(6, code)
        self.assertEqual("CLI_FAILED", response["code"])

    def test_cli_nonzero_and_timeout_map_without_content_leakage(self) -> None:
        """验证 CLI 非零和超时均产生稳定错误，不把请求正文写进错误响应。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖进程失败、超时与正文脱敏边界。
        """
        for mode, expected in (("cli_failed", "CLI_FAILED"), ("timeout", "CLI_TIMEOUT")):
            with self.subTest(mode=mode):
                code, response = self.run_adapter(build_request("doctor", timeout_seconds=1), FAKE_OBSIDIAN_MODE=mode)
                self.assertEqual(6, code)
                self.assertEqual(expected, response["code"])
                self.assertNotIn("secret-content", json.dumps(response, ensure_ascii=False))

    def test_cli_semantic_error_with_zero_exit_is_rejected(self) -> None:
        """验证预检 CLI 的 Error 文本不会因零退出码被误判为成功。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 15:52:23 仅对无用户正文的 version 预检保留语义失败防线。
        """
        code, response = self.run_adapter(build_request("doctor"), FAKE_OBSIDIAN_MODE="semantic_error")
        self.assertEqual(6, code)
        self.assertEqual("CLI_FAILED", response["code"])

    def test_read_preserves_error_prefix_as_valid_note_content(self) -> None:
        """验证合法笔记正文以 Error: 开头时不会被 adapter 误拒绝。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 15:52:23 覆盖正文与预检语义错误的边界。
        """
        # 1. read 的 stdout 是用户 Markdown，不能用 Error: 前缀猜测 CLI 失败。
        code, response = self.run_adapter(
            build_request("read", path=KNOWLEDGE_PREFIX + "contract.md"),
            FAKE_OBSIDIAN_MODE="error_like_content",
        )
        self.assertEqual(0, code, response)
        self.assertTrue(response["ok"])
        self.assertEqual("Error: saved user content", response["data"]["output"])

    def test_write_semantic_error_with_zero_exit_is_rejected(self) -> None:
        """验证写命令的 Error 文本不会在跳过读回时误报成功。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 15:52:23 覆盖 create/append 无用户正文的语义失败边界。
        """
        # 1. create/append 没有合法正文输出，Error: 必须直接映射为 CLI_FAILED。
        code, response = self.run_adapter(
            build_request(
                "create",
                path=KNOWLEDGE_PREFIX + "contract.md",
                content="fixture",
                verify_readback=False,
            ),
            FAKE_OBSIDIAN_MODE="write_semantic_error",
        )
        self.assertEqual(6, code)
        self.assertEqual("CLI_FAILED", response["code"])

    def test_search_preserves_query_and_limit_as_single_cli_arguments(self) -> None:
        """验证 search 的 query/limit 不会在 PowerShell 参数数组中拆分。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 15:52:23 要求 fake 验证完整 query= 与 limit= argv。
        """
        # 1. fake 会在任一 key=value 参数被 PowerShell 拆分时以非零退出码失败。
        code, response = self.run_adapter(
            build_request("search", query="Windows WSL bridge", limit=5),
            FAKE_OBSIDIAN_EXPECT_QUERY="Windows WSL bridge",
            FAKE_OBSIDIAN_EXPECT_LIMIT="5",
        )
        self.assertEqual(0, code, response)
        self.assertTrue(response["ok"])
        self.assertEqual("fake search result", response["data"]["output"])

    def test_rejects_direct_invalid_search_limit(self) -> None:
        """验证绕过 bridge 的 search 请求仍受整数范围限制。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 15:52:23 对齐 bridge 的 limit 1..100 输入契约。
        """
        # 1. adapter 是第二道输入防线，不能信任调用方已经通过 bridge 校验。
        for limit in ("5", 0, -1, 101):
            with self.subTest(limit=limit):
                code, response = self.run_adapter(build_request("search", query="bridge", limit=limit))
                self.assertEqual(2, code)
                self.assertEqual("INVALID_ARGUMENT", response["code"])

    def test_create_chunks_and_verifies_unicode_readback(self) -> None:
        """验证超过 1800 字符的 Unicode 正文按分块写入后通过 readback。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖长正文、UTF-8 传递和 create 读回断言。
        """
        # 1. 2048 rows exceed both the 10 KB contract threshold and the default 1800-char chunk boundary.
        content = "\u4e2d\u6587\u884c\n" * 2048
        code, response = self.run_adapter(
            build_request("create", path=KNOWLEDGE_PREFIX + "contract.md", content=content)
        )
        self.assertEqual(0, code, response)
        self.assertTrue(response["ok"])
        self.assertTrue(response["verified"])

    def test_append_and_readback_mismatch_have_distinct_results(self) -> None:
        """验证 append 读回成功与 create 读回不一致使用不同稳定结果。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 append 断言与 READBACK_MISMATCH。
        """
        append_code, append_response = self.run_adapter(
            build_request("append", path=KNOWLEDGE_PREFIX + "contract.md", content="append")
        )
        self.assertEqual(0, append_code)
        self.assertTrue(append_response["verified"])

        mismatch_code, mismatch_response = self.run_adapter(
            build_request("create", path=KNOWLEDGE_PREFIX + "contract.md", content="content"),
            FAKE_OBSIDIAN_MODE="readback_mismatch",
        )
        self.assertEqual(7, mismatch_code)
        self.assertEqual("READBACK_MISMATCH", mismatch_response["code"])

    def test_rejects_operations_outside_the_adapter_allowlist(self) -> None:
        """验证 adapter 自身再次限制 operation，不信任 bridge 以外的调用者。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 adapter allowlist 的输入防线。
        """
        code, response = self.run_adapter(build_request("delete"))
        self.assertEqual(2, code)
        self.assertEqual("INVALID_ARGUMENT", response["code"])

    def test_rejects_direct_path_traversal_before_invoking_the_cli(self) -> None:
        """验证绕过 bridge 的 adapter 调用也不能利用 traversal 离开知识目录。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 adapter 自身的 canonical 路径防线。
        """
        code, response = self.run_adapter(
            build_request("read", path=KNOWLEDGE_PREFIX + "../outside.md")
        )
        self.assertEqual(2, code)
        self.assertEqual("PATH_OUTSIDE_KNOWLEDGE", response["code"])

    def test_rejects_direct_prefix_override_and_nested_vault_root(self) -> None:
        """验证 adapter 不能接受调用方自定义的知识前缀或旧嵌套 vault 根。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 14:59:17 覆盖绕过 bridge 时的固定路径边界。
        """
        prefix_code, prefix_response = self.run_adapter(
            build_request("read", knowledge_prefix="other/", path="other/../outside.md")
        )
        self.assertEqual(2, prefix_code)
        self.assertEqual("PATH_OUTSIDE_KNOWLEDGE", prefix_response["code"])

        legacy_code, legacy_response = self.run_adapter(
            build_request("doctor", vault_root=r"D:\obsidian_data\知识库")
        )
        self.assertEqual(2, legacy_code)
        self.assertEqual("LEGACY_NESTED_VAULT_MODEL", legacy_response["code"])

    def test_rejects_duplicate_matching_vault_records(self) -> None:
        """验证相同 selector 的重复注册记录仍视为 vault 根歧义。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 14:59:17 覆盖不能被 selector 去重掩盖的唯一性要求。
        """
        code, response = self.run_adapter(
            build_request("doctor"),
            FAKE_OBSIDIAN_VAULTS=r"main|D:\obsidian_data;main|D:\obsidian_data",
        )
        self.assertEqual(5, code)
        self.assertEqual("VAULT_ROOT_AMBIGUOUS", response["code"])

    def test_reads_large_cli_output_without_pipe_deadlock(self) -> None:
        """验证超过 Windows 管道缓冲区的 read 输出会完整返回而不是卡死。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 stdout 异步 drain 的 10KB 回归场景。
        """
        code, response = self.run_adapter(
            build_request("read", path=KNOWLEDGE_PREFIX + "large.md"),
            FAKE_OBSIDIAN_READ_BYTES="12000",
        )
        self.assertEqual(0, code, response)
        self.assertEqual(12000, len(response["data"]["output"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
