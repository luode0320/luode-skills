## Chrome DevTools MCP 安装流程（本节专属 Codex CLI 环境）

当项目命中前端标记，且用户希望当前会话后续由浏览器侧 MCP 接管时，按下面流程执行：

1. 先统一名称为 `Chrome DevTools MCP`，不要把“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”拆成多个工具名。
2. 先检查项目级配置路径：
   - `./codex/config.toml`
   - `./.codex/config.toml`
3. 如果项目级配置不存在，默认创建 `./.codex/config.toml`。
4. 如果项目级配置中没有 `chrome-devtools` 对应项，默认补齐最小可用配置：
   - `command = "npx"`
   - `args = ["-y", "chrome-devtools-mcp@latest"]`
5. 如果当前运行环境是 Windows 且需要更稳的启动路径，优先使用官方仓库给出的 Windows 兜底参数，而不是自己臆造命令。
6. 执行安装命令：
   - `codex mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest`
7. 安装后立即做可用性检查：
   - `codex mcp list`
   - `codex mcp get chrome-devtools`
8. 如果工具已写入但会话里还看不到新 MCP，先重启 Codex 会话或刷新当前会话，再做页面验证。
9. 页面联调与验证按 `references/tool-priority.md` 的条件矩阵执行：用户真实 profile 走 Chrome Plugin，独立调试 / 验证优先 Chrome DevTools MCP，隔离核心自动化走 `browser-session-automation-rules`，高级验证与观测走 `browser-advanced-testing-rules`；不得用线性优先级替代场景判断。
