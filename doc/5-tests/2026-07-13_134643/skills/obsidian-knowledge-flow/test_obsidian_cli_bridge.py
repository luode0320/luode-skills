"""Offline contract tests for the Python Obsidian host bridge."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path
from types import SimpleNamespace


REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
BRIDGE_PATH = REPOSITORY_ROOT / "obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py"
SPEC = importlib.util.spec_from_file_location("obsidian_cli_bridge", BRIDGE_PATH)
assert SPEC and SPEC.loader
bridge = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bridge
SPEC.loader.exec_module(bridge)


class ObsidianCliBridgeTest(unittest.TestCase):
    """验证 bridge 的纯标准库输入边界与跨宿主归一逻辑。"""

    def test_detect_host_supports_windows_and_wsl(self) -> None:
        """验证 Windows 与 WSL 检测不会依赖真实宿主。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖双宿主 host detection 契约。
        """
        self.assertEqual("windows", bridge.detect_host(platform_name="nt"))
        self.assertEqual(
            "wsl",
            bridge.detect_host(platform_name="posix", environ={}, proc_version="Linux microsoft"),
        )

    def test_rejects_non_wsl_linux(self) -> None:
        """验证普通 Linux 不会被错误降级为原生 Obsidian transport。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖非 WSL Linux 的稳定阻断错误码。
        """
        with self.assertRaisesRegex(bridge.BridgeError, "Windows and WSL") as raised:
            bridge.detect_host(platform_name="posix", environ={}, proc_version="Linux")
        self.assertEqual("UNSUPPORTED_HOST", raised.exception.code)

    def test_canonical_identity_unifies_wsl_native_unc_and_git_bash(self) -> None:
        """验证同一 WSL 项目不会因路径别名产生重复实体。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 native、UNC 与 Git Bash WSL 路径等价性。
        """
        expected = "wsl://ubuntu-24.04/home/luode/code/project"
        self.assertEqual(expected, bridge.canonical_project_identity("/home/luode/code/project", "Ubuntu-24.04"))
        self.assertEqual(expected, bridge.canonical_project_identity(r"\\wsl.localhost\Ubuntu-24.04\home\luode\code\project"))
        self.assertEqual(expected, bridge.canonical_project_identity("//wsl.localhost/Ubuntu-24.04/home/luode/code/project"))

    def test_canonical_identity_supports_windows_drive_paths(self) -> None:
        """验证 Windows 盘符路径使用独立 canonical scheme。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 Windows 原生项目身份归一。
        """
        self.assertEqual("windows://d/luode/project", bridge.canonical_project_identity(r"D:\luode\project"))

    def test_wslpath_conversion_uses_utf8_output(self) -> None:
        """验证盘符转换只接受 wslpath 返回的绝对 Linux 路径。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 Windows 路径到 WSL 路径转换。
        """
        def runner(*_args: object, **_kwargs: object) -> SimpleNamespace:
            return SimpleNamespace(returncode=0, stdout="/mnt/d/luode/project\n")

        self.assertEqual("/mnt/d/luode/project", bridge.windows_path_to_wsl(r"D:\luode\project", runner))

    def test_path_allowlist_rejects_traversal_absolute_and_wrong_prefix(self) -> None:
        """验证知识路径不能离开固定 知识库/ 前缀。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 traversal、absolute 和错误前缀输入。
        """
        self.assertEqual("知识库/10-Projects/demo.md", bridge.validate_knowledge_path(r"知识库\10-Projects\demo.md"))
        for value in ("../secret.md", "/知识库/demo.md", "D:/secret.md", "其他库/demo.md", "知识库/../secret.md", "知识库/a:b.md", "知识库/a\x00b.md", "知识库/a\x01b.md", "知识库/name. ", "知识库/name ", " 知识库/name.md"):
            with self.subTest(value=value), self.assertRaisesRegex(bridge.BridgeError, "知识库") as raised:
                bridge.validate_knowledge_path(value)
            self.assertEqual("PATH_OUTSIDE_KNOWLEDGE", raised.exception.code)

    def test_build_request_enforces_command_and_content_contract(self) -> None:
        """验证 allowlist 和写操作正文类型在启动 adapter 前完成校验。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖非法命令和写入请求边界。
        """
        with self.assertRaisesRegex(bridge.BridgeError, "not allowed"):
            bridge.build_request("delete", path="知识库/demo.md")
        with self.assertRaisesRegex(bridge.BridgeError, "string content"):
            bridge.build_request("create", path="知识库/demo.md", content=None)

        # 1. search 的公开契约只要求 query，不能误要求不存在的 path。
        search = bridge.build_request("search", query="跨宿主 bridge")
        self.assertEqual(1, search["schema_version"])
        self.assertEqual("search", search["operation"])
        self.assertEqual("跨宿主 bridge", search["query"])
        self.assertEqual(10, search["limit"])
        self.assertNotIn("path", search)
        self.assertEqual("search_context", bridge.build_request("search-context", query="跨宿主 bridge")["operation"])
        self.assertEqual("知识库/demo.md", bridge.build_request("open", path="知识库/demo.md")["path"])
        self.assertEqual(
            "wsl://ubuntu-24.04/home/luode/code/project",
            bridge.build_request(
                "project-context",
                project_path="/home/luode/code/project",
                distro="Ubuntu-24.04",
            )["project_id"],
        )

    def test_wsl_paths_convert_to_windows_unc(self) -> None:
        """验证 WSL adapter 路径可转换为 Windows UNC。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 WSL 到 Windows PowerShell 的路径转换。
        """
        def runner(command: list[str], **_kwargs: object) -> SimpleNamespace:
            self.assertEqual(["wslpath", "-w", "/mnt/d/adapter.ps1"], command)
            return SimpleNamespace(returncode=0, stdout="\\\\wsl.localhost\\Ubuntu\\mnt\\d\\adapter.ps1\n")

        self.assertEqual(
            r"\\wsl.localhost\Ubuntu\mnt\d\adapter.ps1",
            bridge.wsl_path_to_windows(Path("/mnt/d/adapter.ps1"), runner),
        )

    def test_wsl_adapter_invocation_converts_all_three_paths(self) -> None:
        """验证 WSL transport 会转换 adapter、request 与 response 三个路径。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 WSL 调用 Windows adapter 的三路径契约。
        """
        converted: list[Path] = []

        def convert(path: Path, _runner: object) -> str:
            converted.append(path)
            return f"WIN:{path}"

        def runner(command: list[str], **_kwargs: object) -> SimpleNamespace:
            response_argument = command[command.index("-ResponsePath") + 1]
            response_path = Path(response_argument.removeprefix("WIN:"))
            response_path.write_text('{"ok": true}', encoding="utf-8")
            return SimpleNamespace(returncode=0)

        with tempfile.TemporaryDirectory() as temp_dir, mock.patch.object(bridge, "wsl_path_to_windows", side_effect=convert):
            response = bridge.invoke_windows_adapter(
                bridge.HostContext(host="wsl", transport="powershell.exe"),
                {"operation": "doctor"},
                Path("/mnt/d/adapter.ps1"),
                temp_root=Path(temp_dir),
                runner=runner,
            )
        self.assertTrue(response["ok"])
        self.assertEqual(3, len(converted))

    def test_adapter_failure_response_preserves_stable_error_code(self) -> None:
        """验证 adapter 非零退出时仍优先保留结构化失败响应。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 14:59:17 覆盖 vault 错误码不能被 bridge 泛化为 CLI_FAILED。
        """
        def runner(command: list[str], **_kwargs: object) -> SimpleNamespace:
            response_path = Path(command[command.index("-ResponsePath") + 1])
            response_path.write_text('{"ok": false, "code": "VAULT_ROOT_AMBIGUOUS"}', encoding="utf-8")
            return SimpleNamespace(returncode=5)

        response = bridge.invoke_windows_adapter(
            bridge.HostContext(host="windows", transport="powershell.exe"),
            {"operation": "doctor"},
            Path("adapter.ps1"),
            runner=runner,
        )
        self.assertFalse(response["ok"])
        self.assertEqual("VAULT_ROOT_AMBIGUOUS", response["code"])

    def test_adapter_success_response_with_nonzero_exit_is_rejected(self) -> None:
        """验证进程码和成功响应冲突时不会被误判为成功。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 14:59:17 覆盖 adapter protocol 冲突的稳定阻断。
        """
        def runner(command: list[str], **_kwargs: object) -> SimpleNamespace:
            response_path = Path(command[command.index("-ResponsePath") + 1])
            response_path.write_text('{"ok": true, "code": "OK"}', encoding="utf-8")
            return SimpleNamespace(returncode=1)

        with self.assertRaisesRegex(bridge.BridgeError, "non-zero") as raised:
            bridge.invoke_windows_adapter(
                bridge.HostContext(host="windows", transport="powershell.exe"),
                {"operation": "doctor"},
                Path("adapter.ps1"),
                runner=runner,
            )
        self.assertEqual("CLI_FAILED", raised.exception.code)

    def test_normalize_adapter_response_marks_wsl_interop(self) -> None:
        """验证 bridge 按调用方宿主而不是 adapter 宿主标记 transport。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 14:59:17 覆盖 WSL response v1 envelope。
        """
        response = bridge.normalize_adapter_response(
            bridge.HostContext(host="wsl", transport="powershell.exe"),
            {"ok": True, "code": "OK", "host": "windows", "transport": "windows-direct"},
        )
        self.assertEqual(1, response["schema_version"])
        self.assertEqual("wsl", response["host"])
        self.assertEqual("wsl-powershell-interop", response["transport"])

    def test_transport_discovery_prefers_pwsh_and_reports_missing_wsl_interop(self) -> None:
        """验证 PowerShell 7 优先且 WSL 缺少 interop 有稳定错误码。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 transport 优先级和 WSL 缺失场景。
        """
        self.assertEqual("C:/Program Files/PowerShell/7/pwsh.exe", bridge.discover_windows_transport("windows", lambda name: "C:/Program Files/PowerShell/7/pwsh.exe" if name == "pwsh.exe" else None))
        with self.assertRaises(bridge.BridgeError) as raised:
            bridge.discover_windows_transport("wsl", lambda _name: None)
        self.assertEqual("WSL_INTEROP_UNAVAILABLE", raised.exception.code)

    def test_adapter_uses_utf8_json_and_cleans_temporary_files(self) -> None:
        """验证 Unicode 请求通过 JSON 传输且临时 request/response 会被删除。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 UTF-8 JSON 生命周期，不调用真实 Obsidian。
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            observed: dict[str, object] = {}

            def runner(command: list[str], **_kwargs: object) -> SimpleNamespace:
                request_path = Path(command[command.index("-RequestPath") + 1])
                response_path = Path(command[command.index("-ResponsePath") + 1])
                observed["request_path"] = request_path
                observed["response_path"] = response_path
                observed["request"] = json.loads(request_path.read_text(encoding="utf-8"))
                response_path.write_text(json.dumps({"ok": True, "verified": True}), encoding="utf-8")
                return SimpleNamespace(returncode=0)

            response = bridge.invoke_windows_adapter(
                bridge.HostContext(host="windows", transport="pwsh.exe"),
                bridge.build_request("create", path="知识库/测试.md", content="中文\n第二行"),
                Path("adapter.ps1"),
                temp_root=root,
                runner=runner,
            )
            self.assertEqual({"ok": True, "verified": True}, response)
            self.assertEqual("中文\n第二行", observed["request"]["content"])
            self.assertFalse(Path(observed["request_path"]).exists())
            self.assertFalse(Path(observed["response_path"]).exists())
            self.assertEqual([], list(root.iterdir()))

    def test_adapter_timeout_and_invalid_response_have_stable_codes(self) -> None:
        """验证 transport 异常不返回正文、只映射为稳定错误码。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖 timeout 与无响应文件失败映射。
        """
        context = bridge.HostContext(host="windows", transport="pwsh.exe")

        def timeout_runner(*_args: object, **_kwargs: object) -> SimpleNamespace:
            raise subprocess.TimeoutExpired("pwsh.exe", 1)

        with self.assertRaises(bridge.BridgeError) as raised:
            bridge.invoke_windows_adapter(context, {"command": "doctor"}, Path("adapter.ps1"), runner=timeout_runner)
        self.assertEqual("CLI_TIMEOUT", raised.exception.code)

        def incomplete_runner(*_args: object, **_kwargs: object) -> SimpleNamespace:
            return SimpleNamespace(returncode=0)

        with self.assertRaises(bridge.BridgeError) as raised:
            bridge.invoke_windows_adapter(context, {"command": "doctor"}, Path("adapter.ps1"), runner=incomplete_runner)
        self.assertEqual("CLI_FAILED", raised.exception.code)

    def test_exit_code_mapping_preserves_contract_categories(self) -> None:
        """验证调用方可用退出码区分输入、宿主、应用、vault、CLI 和读回失败。

        [参数] 无。
        [返回] 无。
        最近修改时间: 2026-07-13 覆盖公开错误退出码契约。
        """
        self.assertEqual(2, bridge.exit_code_for("PATH_OUTSIDE_KNOWLEDGE"))
        self.assertEqual(3, bridge.exit_code_for("WSL_INTEROP_UNAVAILABLE"))
        self.assertEqual(4, bridge.exit_code_for("OBSIDIAN_APP_UNAVAILABLE"))
        self.assertEqual(5, bridge.exit_code_for("VAULT_ROOT_AMBIGUOUS"))
        self.assertEqual(6, bridge.exit_code_for("CLI_FAILED"))
        self.assertEqual(7, bridge.exit_code_for("READBACK_MISMATCH"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
