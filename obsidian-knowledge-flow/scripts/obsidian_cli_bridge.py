#!/usr/bin/env python3
"""Bridge Obsidian CLI requests from Windows and WSL to the Windows adapter.

The bridge intentionally owns only host routing, request validation and project
identity normalization. The PowerShell adapter owns all real Obsidian CLI work.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping


ALLOWED_COMMANDS = frozenset({"doctor", "search", "search-context", "read", "create", "append", "open", "project-context"})
KNOWLEDGE_PREFIX = "知识库"
VAULT_ROOT = r"D:\obsidian_data"
WSL_UNC_PATTERN = re.compile(
    r"^(?:\\\\|//)wsl(?:\.localhost)?[\\/]+(?P<distro>[^\\/]+)[\\/]+(?P<path>.+)$",
    re.IGNORECASE,
)
WINDOWS_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:[\\/]")


class BridgeError(RuntimeError):
    """携带稳定错误码的 bridge 异常。"""

    def __init__(self, code: str, message: str) -> None:
        """初始化可安全返回给调用方的异常。

        [参数] code: 稳定错误码；message: 不包含正文的错误说明。
        [返回] 无。
        最近修改时间: 2026-07-13 新增跨宿主 bridge 的稳定错误边界。
        """
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class HostContext:
    """bridge 所在宿主和可用 Windows transport 的最小描述。"""

    host: str
    transport: str


def detect_host(
    *,
    platform_name: str | None = None,
    environ: Mapping[str, str] | None = None,
    proc_version: str | None = None,
) -> str:
    """识别 bridge 运行在 Windows 还是 WSL。

    [参数] platform_name: 可注入的平台名；environ: 可注入的环境变量；proc_version: 可注入的 Linux 版本文本。
    [返回] ``windows`` 或 ``wsl``。
    最近修改时间: 2026-07-13 为 Windows/WSL transport 路由新增可测试 host 检测。
    """
    # 1. Windows 直接使用本机 PowerShell，不把它误判为 WSL。
    name = (platform_name or os.name).casefold()
    if name in {"nt", "windows"}:
        return "windows"

    # 2. WSL 需要同时接受环境标记和 /proc 版本标记，便于不同发行版稳定识别。
    environment = environ or os.environ
    version = proc_version
    if version is None:
        try:
            version = Path("/proc/version").read_text(encoding="utf-8", errors="replace")
        except OSError:
            version = ""
    if name in {"posix", "linux"} and (
        environment.get("WSL_INTEROP")
        or environment.get("WSL_DISTRO_NAME")
        or "microsoft" in version.casefold()
    ):
        return "wsl"
    raise BridgeError("UNSUPPORTED_HOST", "bridge only supports Windows and WSL hosts")


def discover_windows_transport(
    host: str,
    which: Callable[[str], str | None] = shutil.which,
) -> str:
    """发现 Windows PowerShell transport，优先 PowerShell 7。

    [参数] host: 已识别的宿主；which: 可注入的可执行文件定位函数。
    [返回] PowerShell 可执行文件路径或名称。
    最近修改时间: 2026-07-13 新增 Windows/WSL 的统一 PowerShell 发现顺序。
    """
    candidates = (
        ("pwsh.exe", "pwsh", "powershell.exe", "powershell")
        if host == "windows"
        else ("pwsh.exe", "powershell.exe")
    )
    for candidate in candidates:
        found = which(candidate)
        if found:
            return found
    code = "WSL_INTEROP_UNAVAILABLE" if host == "wsl" else "POWERSHELL_UNAVAILABLE"
    raise BridgeError(code, "Windows PowerShell transport is unavailable")


def build_host_context(
    *,
    platform_name: str | None = None,
    environ: Mapping[str, str] | None = None,
    proc_version: str | None = None,
    which: Callable[[str], str | None] = shutil.which,
) -> HostContext:
    """构建执行 adapter 所需的宿主上下文。

    [参数] platform_name: 可注入的平台名；environ: 可注入环境变量；proc_version: 可注入版本文本；which: 可执行文件定位函数。
    [返回] 已包含 transport 的宿主上下文。
    最近修改时间: 2026-07-13 集中 host 与 transport 校验，避免调用方重复分支。
    """
    host = detect_host(platform_name=platform_name, environ=environ, proc_version=proc_version)
    return HostContext(host=host, transport=discover_windows_transport(host, which))


def windows_path_to_wsl(
    value: str,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> str:
    """通过 WSL 的 ``wslpath`` 把 Windows 路径转换为 Linux 路径。

    [参数] value: Windows 原生路径；runner: 可注入的进程执行器。
    [返回] 归一后的 WSL Linux 路径。
    最近修改时间: 2026-07-13 使用 wslpath 保持跨盘符转换与 WSL 实际配置一致。
    """
    if not WINDOWS_DRIVE_PATTERN.match(value):
        raise BridgeError("INVALID_WINDOWS_PATH", "expected an absolute Windows drive path")
    completed = runner(
        ["wslpath", "-u", value],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    converted = completed.stdout.strip() if completed.returncode == 0 else ""
    if not converted.startswith("/"):
        raise BridgeError("WSLPATH_CONVERSION_FAILED", "wslpath could not convert the Windows path")
    return converted


def wsl_path_to_windows(
    value: Path,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> str:
    """将 WSL 路径转为 Windows PowerShell 可访问的 UNC 路径。

    [参数] value: WSL 中的 adapter 或临时 JSON 路径；runner: 可注入的进程执行器。
    [返回] Windows 侧可访问的路径文本。
    最近修改时间: 2026-07-13 修复 WSL 不能直接把 Linux 路径传给 Windows PowerShell 的 P0 问题。
    """
    # 1. Windows PowerShell 需要 UNC/盘符路径，不能直接消费 WSL 的 /tmp 或 /mnt 路径。
    completed = runner(
        ["wslpath", "-w", str(value).replace("\\", "/")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    converted = completed.stdout.strip() if completed.returncode == 0 else ""
    if not converted or not (WINDOWS_DRIVE_PATTERN.match(converted) or converted.startswith("\\\\")):
        raise BridgeError("WSLPATH_CONVERSION_FAILED", "wslpath could not create a Windows path")
    return converted


def canonical_project_identity(path: str, distro: str | None = None) -> str:
    """将 Windows、WSL native 和 WSL UNC 路径归一为稳定项目身份。

    [参数] path: 项目绝对路径；distro: WSL native 路径对应的发行版名。
    [返回] ``windows://`` 或 ``wsl://`` 开头的 canonical project ID。
    最近修改时间: 2026-07-13 消除 WSL native、UNC 与 Git Bash 表示造成的重复实体。
    """
    raw = path.strip()
    if not raw:
        raise BridgeError("INVALID_PROJECT_PATH", "project path is required")

    # 1. UNC 与 Git Bash 的 //wsl.localhost 表示都指向同一个 WSL 身份。
    normalized_unc = raw.replace("\\", "/")
    match = WSL_UNC_PATTERN.match(normalized_unc)
    if match:
        remainder = "/" + match.group("path").strip("/")
        return f"wsl://{match.group('distro').casefold()}{remainder}"

    # 2. Linux native 路径必须带发行版来源，避免与不同 WSL 发行版混淆。
    if raw.startswith("/"):
        if not distro:
            raise BridgeError("WSL_DISTRO_REQUIRED", "WSL project paths require a distro name")
        return f"wsl://{distro.casefold()}/{raw.lstrip('/')}"

    # 3. Windows 项目仅折叠盘符大小写和分隔符，保留路径语义。
    if WINDOWS_DRIVE_PATTERN.match(raw):
        drive = raw[0].casefold()
        remainder = raw[2:].replace("\\", "/").strip("/")
        return f"windows://{drive}/{remainder}"
    raise BridgeError("INVALID_PROJECT_PATH", "project path is not Windows, WSL, or WSL UNC")


def validate_knowledge_path(path: str) -> str:
    """校验所有 vault 操作只落在固定知识路径前缀内。

    [参数] path: 调用方提供的 vault 内相对路径。
    [返回] 使用正斜杠的安全相对路径。
    最近修改时间: 2026-07-13 14:59:17 保留原始空白字符，避免路径校验静默改写调用方输入。
    """
    if not isinstance(path, str) or not path.strip():
        raise BridgeError("PATH_OUTSIDE_KNOWLEDGE", "knowledge path is required")
    # 1. 仅允许空白用于空值判断；路径本身不能被静默 trim 后继续执行。
    if path != path.strip():
        raise BridgeError("PATH_OUTSIDE_KNOWLEDGE", "path must remain below 知识库/ without leading or trailing whitespace")
    normalized = path.replace("\\", "/")
    parts = normalized.split("/")
    if (
        normalized.startswith("/")
        or WINDOWS_DRIVE_PATTERN.match(normalized)
        or any(
            part in {"", ".", ".."}
            or any(ord(char) < 32 or char in '<>:"|?*' for char in part)
            or part.endswith((" ", "."))
            for part in parts
        )
        or parts[0] != KNOWLEDGE_PREFIX
    ):
        raise BridgeError("PATH_OUTSIDE_KNOWLEDGE", "path must remain below 知识库/")
    return "/".join(parts)


def build_request(command: str, **values: Any) -> dict[str, Any]:
    """构造经过 allowlist 和路径校验的 adapter 请求。

    [参数] command: bridge 支持的操作；values: 操作参数。
    [返回] 只包含允许字段的 UTF-8 JSON 可序列化请求对象。
    最近修改时间: 2026-07-13 在跨进程前冻结命令 allowlist 和输入边界。
    """
    if command not in ALLOWED_COMMANDS:
        raise BridgeError("INVALID_ARGUMENT", f"command is not allowed: {command}")

    request: dict[str, Any] = {
        "schema_version": 1,
        "operation": command.replace("-", "_"),
        "vault_root": VAULT_ROOT,
        "knowledge_prefix": f"{KNOWLEDGE_PREFIX}/",
        "timeout_seconds": 30,
        "auto_start": True,
        "startup_wait_seconds": 15,
        "verify_readback": True,
        "chunk_chars": 1800,
    }
    # 1. 检索只按 query；只有路径型操作才校验固定知识目录。
    if command in {"read", "create", "append", "open"}:
        request["path"] = validate_knowledge_path(values.get("path", ""))
    if command in {"create", "append"}:
        content = values.get("content")
        if not isinstance(content, str):
            raise BridgeError("INVALID_ARGUMENT", "create and append require string content")
        request["content"] = content
    if command in {"search", "search-context"}:
        query = values.get("query")
        if not isinstance(query, str) or not query.strip():
            raise BridgeError("INVALID_ARGUMENT", "search requires a non-empty query")
        request["query"] = query
        limit = values.get("limit", 10)
        if not isinstance(limit, int) or not 1 <= limit <= 100:
            raise BridgeError("INVALID_ARGUMENT", "limit must be an integer between 1 and 100")
        request["limit"] = limit
    if project_path := values.get("project_path"):
        if not isinstance(project_path, str):
            raise BridgeError("INVALID_ARGUMENT", "project_path must be a string")
        request["project_id"] = canonical_project_identity(
            project_path,
            values.get("distro"),
        )
    if command == "project-context" and "project_id" not in request:
        raise BridgeError("INVALID_PROJECT_PATH", "project-context requires project_path")
    return request


def invoke_windows_adapter(
    context: HostContext,
    request: Mapping[str, Any],
    adapter_path: Path,
    *,
    timeout: int | None = None,
    temp_root: Path | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    """以 UTF-8 临时 JSON 文件调用 Windows PowerShell adapter。

    [参数] context: 已校验 host/transport；request: 已校验请求；adapter_path: PowerShell adapter 路径；timeout: 可选总超时秒数；temp_root: 可注入临时目录；runner: 可注入进程执行器。
    [返回] adapter 返回的 JSON 对象。
    最近修改时间: 2026-07-13 14:59:17 外层超时覆盖 CLI 和一次应用启动恢复的完整预算。
    """
    with tempfile.TemporaryDirectory(prefix="obsidian-bridge-", dir=temp_root) as temp_dir:
        request_path = Path(temp_dir) / "request.json"
        response_path = Path(temp_dir) / "response.json"
        # 1. 请求和响应仅在私有临时目录存在，退出作用域即删除。
        request_path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
        adapter_argument = str(adapter_path)
        request_argument = str(request_path)
        response_argument = str(response_path)
        if context.host == "wsl":
            adapter_argument = wsl_path_to_windows(adapter_path, runner)
            request_argument = wsl_path_to_windows(request_path, runner)
            response_argument = wsl_path_to_windows(response_path, runner)
        # 2. bridge 不能比 adapter 的单次 CLI 超时和一次启动等待更早终止恢复流程。
        adapter_timeout = timeout
        if adapter_timeout is None:
            adapter_timeout = int(request.get("timeout_seconds", 30)) + int(request.get("startup_wait_seconds", 15)) + 5
        try:
            completed = runner(
                [
                    context.transport,
                    "-NoProfile",
                    "-File",
                    adapter_argument,
                    "-RequestPath",
                    request_argument,
                    "-ResponsePath",
                    response_argument,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=adapter_timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise BridgeError("CLI_TIMEOUT", "Windows adapter timed out") from exc
        # 2. adapter 会在失败时写入 JSON 后再以对应退出码退出，不能先丢弃该响应。
        try:
            response = json.loads(response_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise BridgeError("CLI_FAILED", "Windows adapter did not return JSON") from exc
        if not isinstance(response, dict):
            raise BridgeError("CLI_FAILED", "Windows adapter response must be an object")
        if completed.returncode != 0 and response.get("ok", False):
            raise BridgeError("CLI_FAILED", "Windows adapter returned success JSON with a non-zero exit code")
        if completed.returncode != 0 and not response.get("ok", False):
            return response
        return response


def normalize_adapter_response(context: HostContext, response: Mapping[str, Any]) -> dict[str, Any]:
    """将 adapter 响应归一为调用 bridge 的宿主语义。

    [参数] context: bridge 所在宿主；response: adapter 已解析的结构化响应。
    [返回] 带 v1 envelope 和调用方 host/transport 的响应对象。
    最近修改时间: 2026-07-13 14:59:17 修复 WSL 调用被错误标记为 Windows direct transport。
    """
    # 1. transport 由 bridge 宿主决定，adapter 仅描述其内部 Windows 执行环境。
    normalized = dict(response)
    normalized["schema_version"] = 1
    normalized["host"] = context.host
    normalized["transport"] = "wsl-powershell-interop" if context.host == "wsl" else "windows-direct"
    return normalized


def parse_args() -> argparse.Namespace:
    """解析 bridge 的最小命令行输入。

    [参数] 无。
    [返回] 解析后的命令行参数。
    最近修改时间: 2026-07-13 新增 bridge CLI 入口，保持参数面最小。
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=sorted(ALLOWED_COMMANDS))
    parser.add_argument("--path")
    parser.add_argument("--content-file", type=Path)
    parser.add_argument("--query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--project-path")
    parser.add_argument("--root", dest="project_path")
    parser.add_argument("--distro")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def exit_code_for(code: str) -> int:
    """将稳定错误码映射为公开进程退出码。

    [参数] code: bridge 或 adapter 返回的稳定错误码。
    [返回] 契约定义的 2 至 7 错误退出码，未知错误为 6。
    最近修改时间: 2026-07-13 补齐调用方可判定的错误退出语义。
    """
    # 1. 参数、宿主、应用、vault、CLI 与读回失败必须保持可区分。
    if code in {"INVALID_ARGUMENT", "PATH_OUTSIDE_KNOWLEDGE", "LEGACY_NESTED_VAULT_MODEL"}:
        return 2
    if code in {"UNSUPPORTED_HOST", "WSL_INTEROP_UNAVAILABLE", "POWERSHELL_UNAVAILABLE", "WSLPATH_CONVERSION_FAILED"}:
        return 3
    if code in {"CLI_NOT_FOUND", "OBSIDIAN_APP_UNAVAILABLE"}:
        return 4
    if code in {"VAULT_NOT_REGISTERED", "VAULT_ROOT_AMBIGUOUS"}:
        return 5
    if code == "READBACK_MISMATCH":
        return 7
    return 6


def main() -> int:
    """验证参数并把请求转交给 Windows adapter。

    [参数] 无。
    [返回] 成功为 0，失败为 2。
    最近修改时间: 2026-07-13 14:59:17 补齐 project-context v1 envelope 与跨宿主响应归一。
    """
    args = parse_args()
    try:
        # 1. 先在 Python 侧阻断非法输入，再创建任何 adapter 临时请求。
        content = None
        if args.content_file is not None:
            try:
                content = args.content_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise BridgeError("INVALID_ARGUMENT", "content_file is not readable") from exc
        request = build_request(
            args.command,
            path=args.path,
            content=content,
            query=args.query,
            limit=args.limit,
            project_path=args.project_path,
            distro=args.distro or os.environ.get("WSL_DISTRO_NAME"),
        )
        if args.command == "project-context":
            context = build_host_context()
            response = {
                "schema_version": 1,
                "ok": True,
                "code": "OK",
                "operation": "project_context",
                "host": context.host,
                "transport": "wsl-powershell-interop" if context.host == "wsl" else "windows-direct",
                "verified": True,
                "data": {
                    "project_id": request["project_id"],
                    "project_root": args.project_path,
                    "wsl_distro": args.distro or os.environ.get("WSL_DISTRO_NAME"),
                },
            }
        else:
            context = build_host_context()
            response = normalize_adapter_response(
                context,
                invoke_windows_adapter(
                    context,
                    request,
                    Path(__file__).with_name("obsidian_cli_windows.ps1"),
                ),
            )
    except BridgeError as exc:
        response = {"ok": False, "code": exc.code, "message": str(exc)}
        print(json.dumps(response, ensure_ascii=False))
        return exit_code_for(exc.code)
    if not response.get("ok", False):
        print(json.dumps(response, ensure_ascii=False))
        return exit_code_for(str(response.get("code", "CLI_FAILED")))
    print(json.dumps(response, ensure_ascii=False) if args.json else response.get("message", "ok"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
