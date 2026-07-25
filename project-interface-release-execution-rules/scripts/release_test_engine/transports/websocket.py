"""原生 RFC 6455 WebSocket 真实客户端传输。"""

from __future__ import annotations

import json
from typing import Any, Mapping

from ..scenario_assertions import json_pointer
from .http import assert_local_config


class WebSocketRuntime:
    """管理单次场景内的 WebSocket 连接，禁止跨场景共享会话。"""

    def __init__(self) -> None:
        """初始化空连接注册表。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:43:47，新增场景级 WebSocket 生命周期容器。
        """

        # 1. 连接对象只保存在当前运行时内存，不进入步骤输出或持久化证据。
        self._connections: dict[str, Any] = {}

    def connect(self, config: Mapping[str, Any], environment: str) -> dict[str, Any]:
        """建立一个真实 WebSocket 连接。

        [参数] config: URL、请求头、子协议和会话标识；environment: 执行环境。
        [返回] 不含连接对象的握手结果。
        最近修改时间：2026-07-25 14:43:47，新增鉴权头、子协议和超时支持。
        """

        # 1. 联网前先校验 local 配置来源，并拒绝覆盖尚未关闭的同名会话。
        assert_local_config(config, environment)
        session = str(config.get("session", "default"))
        if session in self._connections:
            raise ValueError(f"WS_SESSION_ALREADY_CONNECTED:{session}")
        url = str(config.get("url", ""))
        if not url:
            raise ValueError("ws.connect url is required")

        # 2. 使用隔离工具环境中的正式 RFC 6455 客户端建立真实网络连接。
        try:
            from websockets.sync.client import connect
        except ImportError as exc:
            raise ImportError("websockets runtime is unavailable") from exc
        headers = {str(key): str(value) for key, value in dict(config.get("headers", {})).items()}
        subprotocols = [str(item) for item in config.get("subprotocols", [])]
        connection = connect(
            url,
            additional_headers=headers or None,
            subprotocols=subprotocols or None,
            open_timeout=float(config.get("timeout_seconds", 5)),
            close_timeout=float(config.get("close_timeout_seconds", 2)),
        )
        self._connections[session] = connection
        return {"connected": True, "session": session, "subprotocol": connection.subprotocol or ""}

    def send(self, config: Mapping[str, Any]) -> dict[str, Any]:
        """通过指定会话发送 JSON、文本或字节消息。

        [参数] config: 会话标识和唯一消息负载。
        [返回] 发送类型和字节长度摘要。
        最近修改时间：2026-07-25 14:43:47，将发送期真实关闭码归一化为场景失败。
        """

        # 1. 只允许一种消息负载，避免执行模型猜测序列化方式。
        connection = self._connection(config)
        kinds = [name for name in ("json", "text", "bytes") if name in config]
        if len(kinds) != 1:
            raise ValueError("ws.send requires exactly one message kind")
        kind = kinds[0]
        if kind == "json":
            # 1.1 JSON、文本和字节三种负载使用互斥编码分支。
            message: str | bytes = json.dumps(config["json"], ensure_ascii=False, separators=(",", ":"))
        elif kind == "text":
            message = str(config["text"])
        else:
            raw = config["bytes"]
            if not isinstance(raw, bytes):
                # 1.2 字节负载必须保持 bytes 类型，禁止隐式字符串编码。
                raise ValueError("ws.send bytes must be bytes")
            message = raw

        # 2. 发送失败由真实协议异常进入场景 FAIL，不生成虚假的发送成功结果。
        try:
            # 2.1 真实发送异常提取关闭码，交由场景层记录安全错误标识。
            connection.send(message)
        except Exception as exc:
            received = getattr(exc, "rcvd", None)
            code = getattr(received, "code", "unknown")
            raise ValueError(f"WS_CONNECTION_CLOSED_{code}") from exc
        length = len(message if isinstance(message, bytes) else message.encode("utf-8"))
        return {"sent": True, "session": str(config.get("session", "default")), "message_type": kind, "length": length}

    def expect(self, config: Mapping[str, Any]) -> dict[str, Any]:
        """按到达顺序接收指定数量的 WebSocket 消息。

        [参数] config: 会话、数量、超时和重复策略。
        [返回] 保持网络到达顺序的结构化消息列表。
        最近修改时间：2026-07-25 14:43:47，使用正式接收帧属性读取关闭码并识别重复事件。
        """

        connection = self._connection(config)
        count = int(config.get("count", 1))
        if count < 1:
            raise ValueError("ws.expect count must be positive")
        timeout = float(config.get("timeout_seconds", 3))
        messages: list[Any] = []

        # 1. 每条消息都使用同一确定超时读取，缺失消息不得被部分结果冒充成功。
        for _ in range(count):
            # 1.1 每次循环只读取一帧，并保持网络到达顺序。
            try:
                # 1.2 超时和连接关闭分别映射为稳定协议错误码。
                raw = connection.recv(timeout=timeout)
            except TimeoutError as exc:
                raise ValueError("WS_MESSAGE_TIMEOUT") from exc
            except Exception as exc:
                received = getattr(exc, "rcvd", None)
                code = getattr(received, "code", "unknown")
                raise ValueError(f"WS_CONNECTION_CLOSED_{code}") from exc
            if isinstance(raw, bytes):
                messages.append(raw)
                continue
            try:
                messages.append(json.loads(raw))
            except ValueError:
                messages.append(raw)

        # 2. 场景显式拒绝重复时，以结构化字段为唯一去重键，重复立即失败。
        if str(config.get("duplicate_policy", "allow")) == "reject":
            # 2.1 reject 策略必须给出结构化去重路径，并比较全部消息键。
            duplicate_path = str(config.get("duplicate_path", ""))
            if not duplicate_path:
                raise ValueError("ws.expect duplicate_path is required")
            keys = [json_pointer(message, duplicate_path) for message in messages]
            if len(set(str(item) for item in keys)) != len(keys):
                raise ValueError("WS_DUPLICATE_MESSAGE")
        return {"session": str(config.get("session", "default")), "messages": messages, "count": len(messages)}

    def close(self, config: Mapping[str, Any]) -> dict[str, Any]:
        """显式关闭并移除指定 WebSocket 会话。

        [参数] config: 会话标识和关闭码。
        [返回] 关闭结果。
        最近修改时间：2026-07-25 14:43:47，新增场景内关闭和同名重连边界。
        """

        # 1. 先从注册表移除再执行网络关闭，确保关闭异常也不会污染后续重连。
        session = str(config.get("session", "default"))
        connection = self._connections.pop(session, None)
        if connection is None:
            raise ValueError(f"WS_SESSION_NOT_CONNECTED:{session}")
        connection.close(code=int(config.get("code", 1000)), reason=str(config.get("reason", "")))
        return {"closed": True, "session": session, "code": int(config.get("code", 1000))}

    def close_all(self) -> None:
        """回收当前场景仍存活的全部 WebSocket 连接。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:43:47，保证失败场景也不残留连接。
        """

        # 1. 复制后清空注册表，逐连接尽力关闭且不覆盖原始场景失败原因。
        connections = list(self._connections.values())
        self._connections.clear()
        for connection in connections:
            try:
                connection.close()
            except Exception:
                continue

    def _connection(self, config: Mapping[str, Any]) -> Any:
        """读取一个已连接会话。

        [参数] config: 包含会话标识的动作配置。
        [返回] 仅供当前运行时使用的连接对象。
        最近修改时间：2026-07-25 14:43:47，统一未连接会话错误语义。
        """

        # 1. 所有收发动作都通过注册表取连接，禁止把连接对象嵌入场景配置。
        session = str(config.get("session", "default"))
        if session not in self._connections:
            raise ValueError(f"WS_SESSION_NOT_CONNECTED:{session}")
        return self._connections[session]
