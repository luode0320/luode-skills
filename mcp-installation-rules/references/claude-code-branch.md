## 平台判定与 Claude Code MCP 配置分支（新增）

以上"覆盖 Codex 本地配置缺口"及下方"Chrome DevTools MCP 安装流程"中出现的 `./codex/config.toml` / `./.codex/config.toml` 特指 Codex CLI 的项目级 MCP 配置文件；Claude Code 的项目级 MCP 配置机制另见本节，两者不通用，不得混用同一份配置文件语义。

执行本 skill 任何配置补齐动作前，先判断当前运行环境是 Codex 还是 Claude Code：

- **Codex 分支**：完全复用下方"Chrome DevTools MCP 安装流程"小节（该小节专属 Codex CLI 环境），逐字不变。
- **Claude Code 分支（待确认）**：当前尚未实测确认 Claude Code 的项目级 MCP 配置具体机制（可能是项目根目录 `.mcp.json` 文件，也可能存在 `claude mcp add` 等命令，需在实际 Claude Code 版本中核实）。在核实之前，遇到 Claude Code 环境下的 MCP 安装/配置需求时：
  - 不得照搬 Codex 分支的 `codex mcp add/list/get` 命令，这些命令在 Claude Code 环境不存在，执行会直接失败（`command not found`）；
  - 应先向用户确认当前 Claude Code 版本支持的 MCP 配置方式（可查阅当前会话可用的官方文档/帮助，或询问用户），确认后再执行配置补齐动作；
  - 若确认存在等价的项目级配置文件（如 `.mcp.json`），比照 Codex 分支的"检测缺失 → 默认补齐最小可用配置"思路执行，但具体 key/value schema 需以确认结果为准，不得照抄 Codex 的 TOML `command`/`args` 字段名假设它们同样适用于 Claude Code 的 JSON schema；
  - 配置补齐后的可用性检查同理，需要用当前确认的 Claude Code 等价命令/机制替代 `codex mcp list` / `codex mcp get`，若没有等价查询手段，则通过让用户在下一次会话中确认新 MCP 是否出现在可用工具列表来间接验证。
