"""HTTP JSON、表单、文件上传和下载传输。"""

from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Mapping


def assert_local_config(config: Mapping[str, Any], environment: str) -> None:
    """校验运行环境和配置来源均属于 local。

    [参数] config: 当前步骤配置；environment: 执行环境名称。
    [返回] 无。
    最近修改时间：2026-07-25 14:23:51，新增统一 local 来源门禁供协议传输复用。
    """

    # 1. 同时校验运行环境和配置归属，避免仅凭地址判断环境安全性。
    provenance = str(config.get("config_environment", environment)).lower()
    if environment != "local" or provenance not in {"local", "local-dev", "development"}:
        raise PermissionError("LOCAL_CONFIG_PROVENANCE_INVALID")


def _body_bytes(value: Any) -> bytes:
    """把声明式上传内容转换为内存字节。

    [参数] value: 场景中声明的文本或字节内容。
    [返回] 仅在当前请求生命周期使用的字节。
    最近修改时间：2026-07-25 14:23:51，新增 multipart 内存编码并拒绝隐式文件读取。
    """

    # 1. 只接受显式内存内容，禁止传输层根据字符串猜测本地文件路径。
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    raise ValueError("multipart file content must be string or bytes")


def _encode_multipart(value: Mapping[str, Any]) -> tuple[bytes, str]:
    """按 RFC 7578 编码声明式 multipart 请求体。

    [参数] value: 包含 fields 和 files 的 multipart 配置。
    [返回] 请求体字节与 Content-Type。
    最近修改时间：2026-07-25 14:23:51，新增文件上传消费者场景支持。
    """

    boundary = f"external-scenario-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    # 1. 普通字段只做 UTF-8 文本编码，不把值写入任何持久化证据。
    fields = value.get("fields", {})
    if not isinstance(fields, Mapping):
        raise ValueError("multipart fields must be an object")
    for name, field_value in fields.items():
        # 1.1 每个普通字段独立写入边界、声明和值。
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                str(field_value).encode("utf-8"),
                b"\r\n",
            ]
        )

    # 2. 文件必须显式给出文件名和内容，避免任意路径读取进入测试引擎。
    files = value.get("files", {})
    if not isinstance(files, Mapping):
        raise ValueError("multipart files must be an object")
    for name, file_value in files.items():
        # 2.1 每个文件只接受内存内容映射，禁止从路径读取原始文件。
        if not isinstance(file_value, Mapping):
            # 2.2 非映射文件配置立即失败，不能猜测文件名或内容来源。
            raise ValueError("multipart file must be an object")
        filename = str(file_value.get("filename", "upload.bin"))
        content_type = str(file_value.get("content_type", "application/octet-stream"))
        content = _body_bytes(file_value.get("content", b""))
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode("utf-8"),
                f"Content-Type: {content_type}\r\n\r\n".encode("ascii"),
                content,
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode("ascii"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def _request_body(config: Mapping[str, Any], headers: dict[str, str]) -> bytes | None:
    """根据唯一负载字段构造 HTTP 请求体。

    [参数] config: HTTP 步骤配置；headers: 待补默认媒体类型的请求头。
    [返回] 编码后的请求体，无负载时返回 None。
    最近修改时间：2026-07-25 14:23:51，统一 JSON、form 和 multipart 互斥选择。
    """

    # 1. 同一请求只允许一种负载，避免 Content-Type 与实际内容不确定。
    body_kinds = [name for name in ("json", "form", "multipart") if name in config]
    if len(body_kinds) > 1:
        raise ValueError("http.request accepts only one body kind")
    if not body_kinds:
        return None

    # 2. 每种负载使用确定性编码，并允许场景显式覆盖请求头做负向测试。
    kind = body_kinds[0]
    if kind == "json":
        headers.setdefault("Content-Type", "application/json")
        return json.dumps(config["json"], ensure_ascii=False).encode("utf-8")
    if kind == "form":
        if not isinstance(config["form"], Mapping):
            raise ValueError("http form must be an object")
        headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
        return urllib.parse.urlencode(config["form"], doseq=True).encode("utf-8")
    body, content_type = _encode_multipart(config["multipart"])
    headers.setdefault("Content-Type", content_type)
    return body


def _response_document(status: int, headers: Any, raw: bytes) -> dict[str, Any]:
    """把真实 HTTP 响应转换为可断言的结构化文档。

    [参数] status: HTTP 状态码；headers: 响应头；raw: 完整响应体字节。
    [返回] 不丢失摘要信息的响应文档。
    最近修改时间：2026-07-25 14:23:51，统一成功和错误响应的解析口径。
    """

    # 1. JSON 响应保持结构，其余响应只提供文本视图和内存字节供摘要断言。
    media_type = headers.get_content_type()
    try:
        body: Any = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError):
        body = raw.decode("utf-8", errors="replace")
    return {
        "status": status,
        "headers": dict(headers.items()),
        "media_type": media_type,
        "body": body,
        "body_bytes": raw,
        "body_length": len(raw),
        "body_sha256": hashlib.sha256(raw).hexdigest(),
    }


def execute_http_request(config: Mapping[str, Any], environment: str) -> dict[str, Any]:
    """执行一次声明式真实 HTTP 请求。

    [参数] config: 方法、URL、请求头和负载配置；environment: 执行环境名称。
    [返回] 可供 JSON Pointer 捕获和断言的响应文档。
    最近修改时间：2026-07-25 14:23:51，新增 form 与 multipart 并保留 JSON 兼容行为。
    """

    # 1. 在解析和联网前先执行 local 配置来源门禁。
    assert_local_config(config, environment)
    method = str(config.get("method", "GET")).upper()
    url = str(config.get("url", ""))
    if not url:
        raise ValueError("http.request url is required")
    query = config.get("query", {})
    if isinstance(query, Mapping) and query:
        separator = "&" if "?" in url else "?"
        url += separator + urllib.parse.urlencode(query, doseq=True)

    # 2. 构造互斥负载并执行真实网络请求，错误响应仍进入确定性断言。
    headers = {str(key): str(value) for key, value in dict(config.get("headers", {})).items()}
    data = _request_body(config, headers)
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=float(config.get("timeout_seconds", 10))) as response:
            return _response_document(response.status, response.headers, response.read())
    except urllib.error.HTTPError as exc:
        # 3. 错误响应同样读取后显式关闭，避免批量场景运行累积文件描述符。
        try:
            return _response_document(exc.code, exc.headers, exc.read())
        finally:
            exc.close()
