# 当前会话重命名工具契约

本契约约束 `thread-title-rules` 的统一 MCP 工具。它只解决“把当前 Codex App 任务改成给定标题”，不负责判断何时改名，也不允许选择其他任务。

## 工具接口

```text
rename_current_thread({
  title: string
}) -> {
  ok: boolean,
  code: "RENAMED"
      | "INVALID_TITLE"
      | "THREAD_CONTEXT_MISSING"
      | "APP_SERVER_UNAVAILABLE"
      | "APP_SERVER_REJECTED"
      | "TIMEOUT",
  title?: string
}
```

- 输入 schema 只允许 `title`，不暴露 `threadId`。
- `title` 去除首尾空白后必须包含 1-24 个 Unicode 字符；推荐的 8-18 字中文简要由 Skill 负责。
- 成功结果只返回经过校验的标题，不返回完整本机路径、命令行、App Server 原始响应或其他线程信息。

## 当前任务身份

按以下顺序解析可信元数据：

1. MCP 调用 `_meta.threadId`。
2. `_meta["x-codex-turn-metadata"].thread_id`。
多个非空来源不一致时返回 `THREAD_CONTEXT_MISSING`。不得读取 `list_threads`，也不得用 `cwd`、最近更新时间、preview 或标题相似度猜测当前任务。

这里的“可信”是宿主适配器边界，不是 MCP 协议本身提供的鉴权能力：第一版只信任 Codex App 在当前工具调用中注入的 `_meta`。任意本机外部 MCP 客户端都可以自行构造 `_meta`，因此不属于本工具的安全边界；本 Server 不得作为网络服务或多用户授权组件暴露。其他宿主若复用该工具契约，必须提供能够绑定“当前任务”的真实适配器，不能把客户端自报的线程 ID 当作通用授权凭据。

## 本机安装与注册

- 在 Skill 目录执行 `npm ci --omit=dev --prefix thread-title-rules/mcp` 安装锁定依赖；`node_modules` 只作为本机运行依赖，不进入 Git。
- 在 `~/.codex/config.toml` 注册 `mcp_servers.thread_session`，命令指向 Node.js 20+，参数指向 `thread-title-rules/mcp/index.mjs`。
- MCP 配置在新任务或宿主重载后生效；旧任务没有重新加载工具列表时，不得声称工具已经暴露。

## App Server 调用

- 启动本机 `codex app-server --stdio`，先完成 `initialize`，再发送 `thread/name/set`。
- Windows 通过 `cmd.exe /d /s /c codex.cmd app-server --stdio` 启动；其他平台使用 `codex app-server --stdio`。
- 请求参数固定为 `{threadId, name}`，其中 `threadId` 来自可信 MCP 元数据，`name` 来自校验后的标题。
- 收到对应请求 ID 的成功响应才返回 `RENAMED`；通知、日志或进程退出码不能单独作为成功证据。
- 无论成功、失败或超时，都必须关闭 stdin 并回收子进程；超时后允许强制终止该次启动的 App Server 子进程。

## 返回码与 Skill 路由

| 返回码 | 含义 | Skill 动作 |
| --- | --- | --- |
| `RENAMED` | App Server 已接受改名 | 输出成功证据并停止，不调用原生工具 |
| `INVALID_TITLE` | 标题为空或超过 24 字 | 首次出现时修正后最多重试 MCP 一次；第二次调用仍失败则直接跳过，不再回退原生工具 |
| `THREAD_CONTEXT_MISSING` | 当前任务元数据缺失或冲突 | 禁止猜测；存在直接当前线程原生工具时回退，否则跳过 |
| `APP_SERVER_UNAVAILABLE` | Codex CLI/App Server 无法启动或异常退出 | 原生工具存在时回退一次，否则跳过 |
| `APP_SERVER_REJECTED` | App Server 返回协议错误或拒绝请求 | 原生工具存在时回退一次，否则跳过 |
| `TIMEOUT` | 初始化或改名请求超时 | 不做同输入 MCP 重试；原生工具存在时回退一次 |

未知返回码、缺失字段或格式错误结果不得写成成功，统一按 MCP 失败处理。

## 安全与兼容边界

- 工具只能改名调用它的当前任务，不能接收或选择任意线程 ID。
- 当前任务身份依赖 Codex App 宿主注入元数据；能够直接启动本机 MCP 客户端或 App Server 的同一操作系统用户不在该身份边界内。本工具不提供跨用户隔离，也不声称可以防止本机同权限客户端伪造 `_meta`。
- 不直接修改 SQLite、rollout 文件或其他内部存储。
- 不使用 UI 自动点击模拟改名。
- 第一版只声明支持 Codex App 的持久化任务；`codex exec --ephemeral` 创建的临时线程不保证可被 App Server 改名。其他宿主必须提供经过真实验证的适配器。
- 模型无关只表示支持工具调用的模型共用同一 MCP 工具；完全不支持工具调用的模型仍必须显式跳过。
