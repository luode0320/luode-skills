# Browser Use Cloud 路由与安全契约

## 路由判定

只有以下条件之一明确成立时才进入 Cloud：

- 云端自主长链，需要托管 Agent 持续执行多步骤网页任务。
- 需要服务商托管并发、地域出口、住宅/托管代理或隐身浏览环境。
- 需要服务商明确提供且目标站点允许的合规验证码处理能力。
- 用户明确要求 Browser Use Cloud，并接受本 Skill 的全部安全与费用闸门。

以下场景必须让给现有 Owner：

| 场景 | Owner | Cloud 结论 |
|---|---|---|
| 已有专用 API、Connector 或 CLI | 专用语义接口 | 不使用 |
| 公开网页只读检索 | `web` 或 HTTP 来源 | 不使用 |
| 用户真实标签页、Cookie、扩展、登录态 | Chrome Plugin | 禁止替代 |
| 普通打开、点击、填写、本地页面交互 | 应用内 Browser | 通常不使用 |
| DOM、Console、Network、Performance | Chrome DevTools MCP | 不使用 |
| 隔离 profile、表单、批量确定性操作 | `browser-session-automation-rules` | 不使用 |
| HAR、视觉 diff、trace、调试代理、多引擎 | `browser-advanced-testing-rules` | 不使用 |

## MCP 配置模板

配置只引用环境变量，不保存 key 原值：

```toml
[mcp_servers.browser_use_cloud]
url = "https://api.browser-use.com/v3/mcp"
env_http_headers = { "x-browser-use-api-key" = "BROWSER_USE_API_KEY" }
enabled_tools = [
  "run_session",
  "get_session",
  "send_task",
  "stop_session",
  "get_session_messages",
  "list_sessions",
  "list_browser_profiles",
]

[mcp_servers.browser_use_cloud.tools.run_session]
approval_mode = "prompt"

[mcp_servers.browser_use_cloud.tools.send_task]
approval_mode = "prompt"
```

配置后必须重启 Codex，让 MCP 重新读取用户环境变量。不要在聊天、仓库配置、fixture 或项目记忆中粘贴 key。

## 费用与 schema

- Browser Use REST Session API 文档定义了 `maxCostUsd`，但 Cloud MCP 文档的工具能力清单未明确列出该参数。
- 每次实际使用前以当前收费动作的可写 input schema 为准：`run_session` 检查 `run_session.inputSchema.properties.maxCostUsd`，`send_task` 独立检查 `send_task.inputSchema.properties.maxCostUsd`。不得扫描 output schema、描述、示例或推测别名。
- Billing 使用官方账户 endpoint，只读取免费层、余额和速率限制；`name`、`projectId`、`subscriptionId` 及完整响应不得进入输出。
- Billing 不明确时失败关闭；免费层也必须逐次确认。

## 默认运行参数

| 参数 | 默认值 | 变更条件 |
|---|---|---|
| model | 服务商默认模型 | 用户当次确认具体模型 |
| profile | 不使用 | 本 Skill 默认禁止上传或选择 Cloud profile |
| recording | `false` | 只有用户为本次任务明确授权并确认隐私影响 |
| keep alive | `false` | 只有需要后续任务且用户当次明确授权 |
| scheduled tasks | `false` | 需要另行创建持久任务授权，本 Skill 的费用确认不包含 |
| temporary email | `false` | 需要另行业务副作用授权 |
| proxy/region | 服务商默认或用户选择 | 必须在费用确认中展示 |

## 确认与清理

- 无硬费用上限风险接受与本次 Cloud 运行确认是两个不同决定；缺少任一个都不能继续。
- `send_task` 是新的收费动作，每次重新执行 Billing、schema 与人工确认，不能复用首次任务预算。
- 任务结束后读取 session；活跃状态固定调用 `stop_session(strategy="session")` 销毁 sandbox，再有限次回读。
- 只有最终 `status="stopped"` 且 `totalCostUsd` 为非负有限数字才算生命周期收口；费用报告使用服务端返回的实际字段，不根据时长或 token 自行推算。

## 官方来源

- Cloud MCP：<https://docs.browser-use.com/cloud/guides/mcp-server>
- v3 Create Session：<https://docs.browser-use.com/cloud/api-v3/sessions/create-session>
- v3 Get Session：<https://docs.browser-use.com/cloud/api-v3/sessions/get-session>
- Billing：<https://docs.browser-use.com/cloud/api-v2/billing/get-account-billing>
