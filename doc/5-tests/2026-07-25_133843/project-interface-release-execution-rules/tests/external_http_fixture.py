"""C14 HTTP 与 SSE 真实回环测试服务。"""

from __future__ import annotations

import hashlib
import json
import threading
import time
import urllib.parse
from email.parser import BytesParser
from email.policy import default
from http.server import BaseHTTPRequestHandler
from typing import Any


DOWNLOAD_BYTES = b"external-scenario-download\x00\xff"


class UploadHandler(BaseHTTPRequestHandler):
    """提供 HTTP 负载、下载和 SSE 的本地闭环服务。"""

    records: dict[str, dict[str, Any]] = {}
    events: list[dict[str, Any]] = []
    event_condition = threading.Condition()
    last_event_ids: list[str] = []

    def _json(self, status: int, value: Any) -> None:
        """返回 JSON 响应。

        [参数] status: HTTP 状态码；value: 可序列化响应值。
        [返回] 无。
        最近修改时间：2026-07-25 14:23:51，新增本地 fixture 统一响应入口。
        """

        # 1. 固定 UTF-8 和长度，确保消费者断言不依赖连接关闭猜测边界。
        payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _read_body(self) -> bytes:
        """读取当前请求的完整内存负载。

        [参数] 无。
        [返回] 请求体字节。
        最近修改时间：2026-07-25 14:23:51，新增 fixture 请求体读取入口。
        """

        # 1. 测试请求均显式携带长度，不接受无限流式上传。
        return self.rfile.read(int(self.headers.get("Content-Length", "0")))

    def do_POST(self) -> None:  # noqa: N802
        """接收事件触发、form 或 multipart 并返回结构化结果。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:33:26，增加 SSE 的 HTTP 触发入口。
        """

        # 1. 事件触发先写入有序内存队列，再通知已经建立连接的 SSE 订阅者。
        media_type = self.headers.get_content_type()
        raw = self._read_body()
        if self.path == "/trigger" and media_type == "application/json":
            # 1.1 触发负载生成唯一事件和对应可读回对象。
            payload = json.loads(raw.decode("utf-8"))
            with self.event_condition:
                # 1.2 在同一条件锁内追加对象和事件，再通知已就绪订阅者。
                event = {"id": str(len(self.events) + 1), "event": "resource.changed", "data": dict(payload)}
                record_id = f"event-{event['id']}"
                event["data"]["object_id"] = record_id
                self.records[record_id] = {"correlation_id": payload["correlation_id"], "state": "visible", "value": payload.get("value")}
                self.events.append(event)
                self.event_condition.notify_all()
            self._json(202, {"id": event["id"], "object_id": record_id})
            return

        # 2. form 场景解析字段并生成可跨步骤读取的固定标识。
        if self.path == "/form" and media_type == "application/x-www-form-urlencoded":
            # 2.1 form 字段按标准解析后保存到固定临时对象。
            fields = urllib.parse.parse_qs(raw.decode("utf-8"))
            record_id = "form-1"
            self.records[record_id] = {"kind": "form", "fields": fields}
            self._json(201, {"id": record_id})
            return

        # 3. multipart 场景使用标准 MIME 解析器读取文件并只保存摘要。
        if self.path == "/multipart" and media_type == "multipart/form-data":
            # 3.1 multipart 仅解析内存负载，并把文件内容转换为长度和摘要。
            message = BytesParser(policy=default).parsebytes(
                f"Content-Type: {self.headers['Content-Type']}\r\nMIME-Version: 1.0\r\n\r\n".encode("ascii") + raw
            )
            file_part = next(part for part in message.iter_parts() if part.get_filename())
            content = file_part.get_payload(decode=True)
            record_id = "file-1"
            self.records[record_id] = {
                "kind": "multipart",
                "filename": file_part.get_filename(),
                "length": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
            self._json(201, {"id": record_id})
            return
        self._json(415, {"error": "unsupported media type"})

    def do_GET(self) -> None:  # noqa: N802
        """返回 SSE、下载内容或按标识返回服务端保存的摘要。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:33:26，增加可重连和可控断流的 SSE 响应。
        """

        # 1. 断流端点只发送半个事件后关闭，用于验证客户端不会把半包误报为成功。
        if self.path == "/events-disconnect":
            # 1.1 只发送未闭合事件后返回，稳定模拟半包断流。
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            self.wfile.write(b"id: partial\ndata: {\"correlation_id\":\"broken\"}")
            self.wfile.flush()
            return

        # 2. 正常 SSE 端点记录 Last-Event-ID，并等待 HTTP 触发产生游标之后的新事件。
        if self.path == "/events":
            # 2.1 先发送响应头建立订阅，再进入条件等待，保证触发动作不会先于订阅。
            last_event_id = self.headers.get("Last-Event-ID", "")
            self.last_event_ids.append(last_event_id)
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.flush()
            last_number = int(last_event_id or "0")
            deadline = time.monotonic() + 3
            with self.event_condition:
                while not any(int(item["id"]) > last_number for item in self.events) and time.monotonic() < deadline:
                    self.event_condition.wait(timeout=0.1)
                available = [item for item in self.events if int(item["id"]) > last_number]
            if available:
                event = available[0]
                payload = json.dumps(event["data"], ensure_ascii=False, separators=(",", ":"))
                self.wfile.write(f'id: {event["id"]}\nevent: {event["event"]}\ndata: {payload}\n\n'.encode("utf-8"))
                self.wfile.flush()
            return

        # 3. 下载响应固定提供文件名和长度，供消费者验证头部与实际字节一致。
        if self.path == "/download":
            # 3.1 下载端点同时固定媒体类型、文件名、长度和字节内容。
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition", 'attachment; filename="sample.bin"')
            self.send_header("Content-Length", str(len(DOWNLOAD_BYTES)))
            self.end_headers()
            self.wfile.write(DOWNLOAD_BYTES)
            return

        # 4. 读回不存在的对象时明确返回 404，避免空对象被误报为成功。
        record_id = self.path.removeprefix("/objects/")
        if self.path.startswith("/objects/") and record_id in self.records:
            self._json(200, self.records[record_id])
            return
        self._json(404, {"error": "not found"})

    def do_DELETE(self) -> None:  # noqa: N802
        """删除场景创建的临时记录。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:23:51，新增场景内清理动作的真实服务端入口。
        """

        # 1. 返回删除数量，供场景断言清理确实发生。
        record_id = self.path.removeprefix("/objects/")
        deleted = int(self.records.pop(record_id, None) is not None)
        self._json(200, {"deleted": deleted})

    def log_message(self, format: str, *args: object) -> None:
        """关闭 fixture 默认访问日志。

        [参数] format: 默认日志模板；args: 模板参数。
        [返回] 无。
        最近修改时间：2026-07-25 14:23:51，避免测试输出混入不可控访问日志。
        """

        return
