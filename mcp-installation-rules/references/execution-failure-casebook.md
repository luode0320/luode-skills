# MCP 安装执行失败案例库

本文件只记录 MCP 安装、配置、可用性检查和工具接管失败的脱敏经验，归属 `mcp-installation-rules`。

## 统一维护规则

- 状态使用 `candidate`、`active`、`stale`、`superseded`、`rejected`。
- 先按 AI 平台、MCP 名称、配置文件和验证命令匹配 active；官方命令或版本变化后重新验证。
- 未确认的 Claude Code 配置方式不得从 Codex TOML 命令猜测；失败案例不得写入凭据或完整配置值。

## MCP-001

- 状态：`active`
- 类型：配置不可见
- 错误特征：配置已写入但当前会话工具列表仍不可见
- 根因：MCP 配置刷新需要重启 Codex 会话或刷新工具列表
- 解决方案：先执行 `codex mcp list` / `codex mcp get <name>`，确认配置后重启或刷新当前会话，再验证工具
- 验证：工具出现在当前会话并能完成最小安全调用
- 来源：`mcp-installation-rules/SKILL.md` Chrome DevTools MCP 流程
- 最后验证：2026-07-12

## MCP-002

- 状态：`active`
- 类型：平台命令不兼容
- 错误特征：在 Claude Code 环境执行 Codex 专用 `codex mcp ...` 命令失败
- 根因：不同 AI 平台的 MCP 配置机制和 schema 不同
- 解决方案：先确认当前平台和官方配置机制；未确认前停止配置补齐并报告阻断
- 验证：使用当前平台官方等价机制完成配置和可用性检查
- 来源：`mcp-installation-rules/SKILL.md` 平台判定分支
- 最后验证：2026-07-12

## MCP-003

- 状态：`active`
- 类型：provisioning/runtime owner 分流
- 错误特征：MCP 已完成配置并在任务执行期间出现 timeout、EOF、连接断开或暂时不可用
- 根因：运行期传输或宿主生命周期故障，不是安装、注册或首次连接问题
- 解决方案：保留当前 MCP 名称、平台、配置来源和最小脱敏失败证据，转交 `agent-runtime-recovery-rules` 的 `mcp_runtime_transport`；由 adapter 能力协商决定 reconnect/reload/restart/resume。不得回到安装流程，也不得猜测平台命令或进程名
- 验证：运行期 owner 以原成功标准完成健康探针和恢复后验证；无 adapter 能力时明确 `manual_handoff`/`blocked`
- 禁止动作：将运行期断连写入本安装 casebook 的恢复方案；把会话刷新或任意重启宣称为通用 MCP reload/restart
- 来源：`execution-failure-learning-rules/references/classification-and-routing.md` provisioning/runtime 分流
- 最后验证：2026-07-12
