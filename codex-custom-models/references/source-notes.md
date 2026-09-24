# Source Notes - codex-custom-models

## 2026-09-21 内部调整与执行 Gap 回补（工具通道 aborted 修复）

- **来源通道**：内部更新通道 + 执行中 gap 回补通道
- **触发背景**：用户在 Codex Desktop 中使用自定义第三方模型（`deepseek-v4.1-flash`）运行 `/goal 找bug, 并修复` 时，所有工具调用 0 秒立刻被中止（aborted），模型死循环报错并提示「工具通道整体不可用，需要应用侧重启」。
- **根因分析**：
  1. `model-catalog.json` 中第三方模型继承了 GPT-5.6-luna 的 `"tool_mode": "code_mode_only"` 与 `"use_responses_lite": true`。Codex Desktop 强制进入 Code Mode 只开放 raw JS `custom_tool_call`（`exec`），而第三方模型输出标准 OpenAI `function_call`，触发 `Fatal error: tool exec invoked with incompatible payload` 导致命令被强制 abort。
  2. Codex 客户端自动升级后，`cua_node` 运行时目录哈希由 `ad3b5049246cde44` 变更为 `df473e5367fa2b42`，`config.toml` 中残留旧路径。
- **落点清单**：
  - `SKILL.md`：更新标准步骤 2（第三方模型工具模式要求）、已沉淀的坑第 11 条与第 12 条。
  - `scripts/generate_catalog.py` & `D:\谷歌云盘\workbuddy-model\gen_codex_catalog.py`：强制配置非 GPT 模型 `tool_mode = None`、`use_responses_lite = False`、`multi_agent_version = None`。
  - `references/troubleshooting-tool-channel.md`：创建工具通道排查诊断与彻底根治手册。
  - `~/.codex/config.toml`：校准 `notify` 与 `CODEX_CLI_PATH` 路径。
- **验证结论**：通过 `deepseek-v4.1-flash` 与 `glm-5.3-flash` 真实执行 `exec_command`，正常返回终端输出，无 abort，验证通过。
