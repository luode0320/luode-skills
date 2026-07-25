"""Server-Sent Events 真实订阅、解析和重连传输。"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from typing import Any, Mapping

from .http import assert_local_config


def _event_document(fields: Mapping[str, Any]) -> dict[str, Any]:
    """把一个完整 SSE 字段集合转换为结构化事件。

    [参数] fields: 当前事件的 id、event 和 data 字段。
    [返回] 可使用 JSON Pointer 断言的事件文档。
    最近修改时间：2026-07-25 14:33:26，新增 SSE 文本与 JSON 数据统一解析。
    """

    # 1. JSON 数据保持结构，普通文本保持原值，避免测试侧自行猜测编码。
    data_text = "\n".join(fields.get("data", []))
    try:
        data: Any = json.loads(data_text)
    except (TypeError, ValueError):
        data = data_text
    return {"id": str(fields.get("id", "")), "event": str(fields.get("event", "message")), "data": data}


def expect_sse(config: Mapping[str, Any], environment: str, *, ready_event: threading.Event | None = None) -> dict[str, Any]:
    """订阅 SSE 并读取指定数量的完整事件。

    [参数] config: URL、请求头、重连游标和期望数量；environment: 执行环境；ready_event: 订阅就绪信号。
    [返回] 状态码、响应头和保持到达顺序的事件列表。
    最近修改时间：2026-07-25 14:33:26，新增先订阅后触发、断流识别和 Last-Event-ID 重连。
    """

    # 1. 联网前校验 local 来源，并明确声明事件流媒体类型和可选重连游标。
    assert_local_config(config, environment)
    url = str(config.get("url", ""))
    if not url:
        raise ValueError("sse.expect url is required")
    headers = {str(key): str(value) for key, value in dict(config.get("headers", {})).items()}
    headers.setdefault("Accept", "text/event-stream")
    if "last_event_id" in config:
        headers["Last-Event-ID"] = str(config["last_event_id"])
    request = urllib.request.Request(url, headers=headers, method="GET")
    expected_count = int(config.get("count", 1))
    if expected_count < 1:
        raise ValueError("sse.expect count must be positive")

    # 2. 响应头通过后立即发出就绪信号，同组 HTTP 动作只能在此后触发事件。
    try:
        # 2.1 只在响应头成功后进入流处理，HTTP 错误先转换为稳定协议错误码。
        response = urllib.request.urlopen(request, timeout=float(config.get("timeout_seconds", 5)))
    except urllib.error.HTTPError as exc:
        try:
            raise ValueError(f"SSE_HTTP_STATUS_{exc.code}") from exc
        finally:
            exc.close()
    with response:
        if response.headers.get_content_type() != "text/event-stream":
            raise ValueError("SSE_MEDIA_TYPE_INVALID")
        if ready_event is not None:
            ready_event.set()

        # 3. 只有空行结束的事件才进入结果；半包后断流必须失败而非误报事件到达。
        events: list[dict[str, Any]] = []
        fields: dict[str, Any] = {"data": []}
        while len(events) < expected_count:
            # 3.1 每次读取都区分超时、完整断开和事件结束空行，避免半包进入结果。
            try:
                raw_line = response.readline()
            except (OSError, TimeoutError) as exc:
                raise ValueError("SSE_EVENT_TIMEOUT") from exc
            if raw_line == b"":
                failure = "SSE_STREAM_INTERRUPTED" if fields.get("data") or fields.get("id") else "SSE_EVENT_MISSING"
                raise ValueError(failure)
            line = raw_line.rstrip(b"\r\n")
            if not line:
                if fields.get("data"):
                    events.append(_event_document(fields))
                fields = {"data": []}
                continue
            if line.startswith(b":"):
                continue
            raw_field, separator, raw_value = line.partition(b":")
            field = raw_field.decode("utf-8", errors="strict")
            value = raw_value[1:] if separator and raw_value.startswith(b" ") else raw_value
            text_value = value.decode("utf-8", errors="strict")
            if field == "data":
                fields["data"].append(text_value)
            elif field in {"id", "event"}:
                fields[field] = text_value
        return {"status": response.status, "headers": dict(response.headers.items()), "events": events}
