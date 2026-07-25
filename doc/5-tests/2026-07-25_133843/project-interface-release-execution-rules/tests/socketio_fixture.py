"""C15 Socket.IO aiohttp 真实回环测试服务。"""

from __future__ import annotations

import asyncio
import threading
from typing import Any


class SocketIOFixture:
    """在独立事件循环中托管随机端口 Socket.IO 服务。"""

    def __init__(self) -> None:
        """初始化未启动的 fixture 状态。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，新增 Socket.IO 服务生命周期容器。
        """

        # 1. 服务端口只在启动后发布，避免测试提前连接未就绪地址。
        self.ready = threading.Event()
        self.loop: asyncio.AbstractEventLoop | None = None
        self.runner: Any = None
        self.server: Any = None
        self.port = 0
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        """启动随机回环端口 Socket.IO 服务。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，建立 namespace/event/ack 真实 fixture。
        """

        # 1. 后台线程拥有独立 asyncio 循环，主测试线程等待端口真实可用。
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        if not self.ready.wait(5):
            raise RuntimeError("Socket.IO fixture did not start")

    def stop(self) -> None:
        """停止服务并回收事件循环线程。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，等待 Engine.IO 后台任务关闭后再停止循环。
        """

        # 1. 先在线程所属循环关闭 Engine.IO 后台任务，再触发 aiohttp 最终清理。
        if self.loop is not None and self.server is not None:
            future = asyncio.run_coroutine_threadsafe(self._shutdown_server(), self.loop)
            future.result(timeout=5)
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread is not None:
            self.thread.join(timeout=5)

    async def _shutdown_server(self) -> None:
        """断开现存 Engine.IO socket 并停止后台服务任务。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，等待缩短后的 ping task 自然退出再关闭事件循环。
        """

        # 1. 每个底层 sid 都先完成协议断开，确保其 ping task 收到关闭信号。
        for sid in list(self.server.eio.sockets):
            await self.server.eio.disconnect(sid)
        # 2. 所有连接清空后再停止 Engine.IO 全局 service task。
        await self.server.shutdown()
        await asyncio.sleep(0.1)

    def _run(self) -> None:
        """创建并运行 aiohttp Socket.IO 应用。

        [参数] 无。
        [返回] 无。
        最近修改时间：2026-07-25 14:50:26，提供真实 namespace、事件推送和 ack 行为。
        """

        # 1. 服务端只接受 /chat namespace 和 local token，错误鉴权拒绝连接。
        import socketio
        from aiohttp import web

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        server = socketio.AsyncServer(
            async_mode="aiohttp",
            logger=False,
            engineio_logger=False,
            ping_interval=0.05,
            ping_timeout=1,
        )
        self.server = server
        app = web.Application()
        server.attach(app)

        @server.event(namespace="/chat")
        async def connect(sid: str, environ: dict[str, Any], auth: Any) -> bool:
            """校验 /chat namespace 的 local 鉴权。

            [参数] sid: 客户端标识；environ: 握手环境；auth: 客户端鉴权负载。
            [返回] 是否接受连接。
            最近修改时间：2026-07-25 14:50:26，新增 namespace 鉴权 fixture。
            """

            # 1. 只有显式 local token 可以建立 namespace 会话。
            return isinstance(auth, dict) and auth.get("token") == "local-token"

        @server.on("publish", namespace="/chat")
        async def publish(sid: str, data: dict[str, Any]) -> dict[str, Any]:
            """推送 published 事件并返回 ack。

            [参数] sid: 客户端标识；data: publish 事件负载。
            [返回] 服务端 ack 文档。
            最近修改时间：2026-07-25 14:50:26，提供 event 与 ack 正反例。
            """

            # 1. 事件先通过真实 namespace 发出，随后按 mode 返回可断言 ack。
            await server.emit("published", {"correlation_id": data["correlation_id"], "state": "visible"}, to=sid, namespace="/chat")
            return {"accepted": data.get("mode") != "bad-ack", "correlation_id": data["correlation_id"]}

        # 2. 绑定随机回环端口并在事件循环停止后清理应用资源。
        self.runner = web.AppRunner(app)
        self.loop.run_until_complete(self.runner.setup())
        site = web.TCPSite(self.runner, "127.0.0.1", 0)
        self.loop.run_until_complete(site.start())
        self.port = site._server.sockets[0].getsockname()[1]
        self.ready.set()
        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.runner.cleanup())
            self.loop.close()
