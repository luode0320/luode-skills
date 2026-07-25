"""Socket.IO namespace、事件与 ack 真实客户端传输。"""

from __future__ import annotations

import queue
from typing import Any, Mapping

from .http import assert_local_config


class SocketIORuntime:
    """管理单次场景内的 Socket.IO 客户端和事件队列。"""

    def __init__(self) -> None:
        """初始化空 Socket.IO 会话注册表。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，新增场景级 Socket.IO 生命周期容器。
        """

        # 1. 客户端与事件队列只保存在当前运行时内存，不进入步骤证据。
        self._sessions: dict[str, dict[str, Any]] = {}

    def connect(self, config: Mapping[str, Any], environment: str) -> dict[str, Any]:
        """连接指定 Socket.IO namespace。

        [参数] config: URL、namespace、auth、请求头和会话标识；environment: 执行环境。
        [返回] 会话和 namespace 连接结果。
        最近修改时间：2026-07-25 14:50:26，新增真实 Socket.IO namespace 连接。
        """

        # 1. 联网前校验 local 来源，并拒绝覆盖仍在线的同名会话。
        assert_local_config(config, environment)
        session = str(config.get("session", "default"))
        if session in self._sessions:
            raise ValueError(f"SOCKETIO_SESSION_ALREADY_CONNECTED:{session}")
        url = str(config.get("url", ""))
        namespace = str(config.get("namespace", "/"))
        if not url:
            raise ValueError("socketio.connect url is required")
        try:
            import socketio
        except ImportError as exc:
            raise ImportError("python-socketio runtime is unavailable") from exc

        # 2. 在连接前注册 catch-all 处理器，避免 connect 与 emit 之间的早到事件丢失。
        events: queue.Queue[dict[str, Any]] = queue.Queue()
        client = socketio.Client(reconnection=False, logger=False, engineio_logger=False)

        def receive_event(event: str, data: Any = None) -> None:
            """把 namespace 内的网络事件放入场景队列。

            [参数] event: Socket.IO 事件名；data: 事件负载。
            [返回] 无。
            最近修改时间：2026-07-25 14:50:26，捕获早到事件供后续 expect 步骤读取。
            """

            # 1. 仅保存结构化事件名和负载，不保存底层连接或鉴权上下文。
            events.put({"event": event, "data": data})

        client.on("*", receive_event, namespace=namespace)
        try:
            # 2.1 连接参数只来自声明式 local 配置，并固定关闭自动重连。
            client.connect(
                url,
                headers={str(key): str(value) for key, value in dict(config.get("headers", {})).items()} or None,
                auth=config.get("auth"),
                namespaces=[namespace],
                transports=[str(item) for item in config.get("transports", ["polling"])],
                wait_timeout=float(config.get("timeout_seconds", 5)),
            )
        except Exception as exc:
            client.disconnect()
            raise ValueError("SOCKETIO_CONNECT_FAILED") from exc
        self._sessions[session] = {"client": client, "namespace": namespace, "events": events}
        return {"connected": True, "session": session, "namespace": namespace}

    def emit(self, config: Mapping[str, Any]) -> dict[str, Any]:
        """发送 Socket.IO 事件并可等待真实 ack。

        [参数] config: 会话、事件名、负载和 ack 超时。
        [返回] 事件名与 ack 结果。
        最近修改时间：2026-07-25 14:50:26，新增 Socket.IO event/ack 消费者动作。
        """

        # 1. 使用 call 等待服务端 ack，超时或断开必须进入场景 FAIL。
        state = self._session(config)
        event = str(config.get("event", ""))
        if not event:
            raise ValueError("socketio.emit event is required")
        try:
            # 1.1 根据显式 expect_ack 选择同步 call 或普通 emit，不能把缺失 ack 当成功。
            if config.get("expect_ack", True):
                ack = state["client"].call(event, config.get("data"), namespace=state["namespace"], timeout=float(config.get("timeout_seconds", 3)))
            else:
                state["client"].emit(event, config.get("data"), namespace=state["namespace"])
                ack = None
        except Exception as exc:
            raise ValueError("SOCKETIO_ACK_FAILED") from exc
        return {"session": str(config.get("session", "default")), "namespace": state["namespace"], "event": event, "ack": ack}

    def expect(self, config: Mapping[str, Any]) -> dict[str, Any]:
        """从指定 namespace 的网络事件队列读取事件。

        [参数] config: 会话、事件名、数量和超时。
        [返回] 保持到达顺序的事件列表。
        最近修改时间：2026-07-25 14:50:26，新增 Socket.IO 事件等待与名称过滤。
        """

        state = self._session(config)
        expected_event = str(config.get("event", ""))
        count = int(config.get("count", 1))
        timeout = float(config.get("timeout_seconds", 3))
        matched: list[dict[str, Any]] = []

        # 1. 只把名称匹配的真实事件计入数量，超时前未满足数量即稳定失败。
        while len(matched) < count:
            # 1.1 每轮从真实事件队列读取一条，直到名称匹配数量满足。
            try:
                # 1.2 队列超时稳定映射为协议错误码，供场景层安全记录。
                item = state["events"].get(timeout=timeout)
            except queue.Empty as exc:
                raise ValueError("SOCKETIO_EVENT_TIMEOUT") from exc
            if not expected_event or item["event"] == expected_event:
                matched.append(item)
        return {"session": str(config.get("session", "default")), "namespace": state["namespace"], "events": matched, "count": len(matched)}

    def disconnect(self, config: Mapping[str, Any]) -> dict[str, Any]:
        """断开并移除指定 Socket.IO 会话。

        [参数] config: 会话标识。
        [返回] 断开结果。
        最近修改时间：2026-07-25 14:50:26，新增显式 namespace 会话清理。
        """

        # 1. 先移除注册表再断开客户端，防止异常会话污染后续同名重连。
        session = str(config.get("session", "default"))
        state = self._sessions.pop(session, None)
        if state is None:
            raise ValueError(f"SOCKETIO_SESSION_NOT_CONNECTED:{session}")
        state["client"].disconnect()
        return {"disconnected": True, "session": session, "namespace": state["namespace"]}

    def close_all(self) -> None:
        """回收当前场景仍存活的全部 Socket.IO 会话。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，保证失败场景不残留 Engine.IO 轮询线程。
        """

        # 1. 清空注册表后逐客户端尽力断开，不覆盖原始场景失败原因。
        states = list(self._sessions.values())
        self._sessions.clear()
        for state in states:
            try:
                state["client"].disconnect()
            except Exception:
                continue

    def _session(self, config: Mapping[str, Any]) -> dict[str, Any]:
        """读取一个已连接 Socket.IO 会话。

        [参数] config: 包含会话标识的动作配置。
        [返回] 当前运行时内的客户端、namespace 和事件队列。
        最近修改时间：2026-07-25 14:50:26，统一未连接会话错误语义。
        """

        # 1. 底层客户端只能由运行时注册表提供，场景配置不能注入连接对象。
        session = str(config.get("session", "default"))
        if session not in self._sessions:
            raise ValueError(f"SOCKETIO_SESSION_NOT_CONNECTED:{session}")
        return self._sessions[session]
