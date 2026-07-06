---
name: godot-project-bootstrap-rules
description: 当仓库命中 `project.godot`、`.gd`、`.tscn`、`addons/`、`export_presets.cfg` 等 Godot 项目标记，且需要自动补齐项目级规则文件（`AGENTS.md` / `CLAUDE.md`）、Godot AI MCP 配置、图像生成配置模板或检查 Godot 开发环境是否可直接进入执行时强制自动触发。负责把 Godot 项目的环境准备、自举补齐、图像通道模板和只差人工配置的缺口一次性收口。
---

# Godot 项目自举规则

## 目标

- 识别当前仓库是否为真实 Godot 项目。
- 自动补齐仓库级规则文件（`AGENTS.md` / `CLAUDE.md`）中的 Godot 开发约定与图像生成配置模板。
- 自动补齐项目级 Codex MCP 配置中的 `Godot AI MCP`。
- 明确哪些部分已经自动就绪，哪些部分仍需要项目维护者手工补配置。

## 自动触发信号

- 命中 `project.godot`
- 命中 `.gd`、`.tscn`、`.scn`、`.tres`、`.res`
- 命中 `addons/`、`export_presets.cfg`
- 用户明确说“这是 Godot 游戏项目”“帮我把 Godot 项目的环境和图像生成配置补齐”“检查 Godot MCP / gpt-image 配置”

## 进入后先做什么

1. 先按 `mcp-installation-rules` 的项目识别规则确认是否为 Godot 项目。
2. 强制联动 `project-agents-bootstrap`，确保仓库根目录规则文件（`AGENTS.md` / `CLAUDE.md`）存在。
3. 检查规则文件（`AGENTS.md` / `CLAUDE.md`）是否已包含：
   - `## Godot 项目工具配置`
   - `## 图像生成配置`
4. 若项目级 `./codex/config.toml` 或 `./.codex/config.toml` 缺少 `Godot AI MCP`，按 `mcp-installation-rules` 默认补齐（Codex 环境；Claude Code 按 `mcp-installation-rules` 的"平台判定与 Claude Code MCP 配置分支"处理）。

## 默认执行流程

1. 识别 Godot 项目标记。
2. 补齐仓库级规则文件（`AGENTS.md` / `CLAUDE.md`）。
3. 若为 Godot 项目，强制补齐：
   - Godot 工具接管约定
   - 图像生成配置模板
4. 检查并补齐项目级 Codex MCP 配置（Codex 环境；Claude Code 按 `mcp-installation-rules` 的"平台判定与 Claude Code MCP 配置分支"处理）。
5. 输出环境就绪结论，区分：
   - 已自动补齐
   - 已存在可直接复用
   - 仍需人工配置

## 图像配置硬规则

- 规则文件（`AGENTS.md` / `CLAUDE.md`）里只允许写图像通道的读取约定、`baseurl`、模型名、优先级和回退规则。
- 规则文件（`AGENTS.md` / `CLAUDE.md`）里不得明文写真实 `OPENAI_API_KEY`。
- 真实密钥必须来自：
  - 当前进程环境变量
  - `~/.codex/auth.json`（仅 Codex 环境存在该机制）
  - `~/.codex/config.toml`（仅 Codex 环境存在该机制）
  - 项目已经接好的运行时环境变量或运行时配置
  - Claude Code 环境：当前没有已确认的等价全局密钥文件机制（不假设存在 `~/.claude/auth.json` 等路径）；必须回退到"当前进程环境变量"或"项目已经接好的运行时环境变量或运行时配置"，若都不可用则明确提示用户在项目规则文件（`CLAUDE.md`）或本机环境变量中补充声明
- 项目如需专用图像通道，优先让项目维护者在本机环境里配置真实密钥，再在规则文件（`AGENTS.md` / `CLAUDE.md`）中声明读取位置，例如 `env:PROJECT_IMAGE_OPENAI_API_KEY`。
- 图像生成配置必须同时声明主通道与回退规则。
- 主通道优先使用 `baseurl=https://api.openai.com/v1` 和最新可用的 `gpt-image` 模型，例如 `gpt-image-1`。
- 若主通道无法使用最新 `gpt-image` 模型，必须回退到项目规则文件（`AGENTS.md` / `CLAUDE.md`）中声明的回退配置。
- 回退规则必须写成 `回退规则：回退配置` 的层级结构，并至少包含：
  - `api: ''`
  - `baseurl: ''`
- 若主通道和项目回退配置都不可用，必须明确标记为缺失配置，不得伪造生成结果或静默切换到未声明的服务商。

## 输出要求

最终必须明确写出：

- 是否命中 Godot 项目标记
- 规则文件（`AGENTS.md` / `CLAUDE.md`）是否已补齐 Godot 与图像配置模板
- `Godot AI MCP` 是否已补齐到项目级 Codex 配置
- 当前图像生成模板是否只剩人工填写
- 剩余人工步骤是什么

## 与相邻 skill 的边界

- 不替代 `mcp-installation-rules` 做 MCP 安装来源分析；这里只负责把 Godot 项目的完整准备流串起来。
- 不替代 `imagegen` 做实际图片生成；这里只保证项目的图像配置入口存在且格式可读。
- 不替代 `project-agents-bootstrap` 做通用仓库规则补齐；这里只追加 Godot 项目的专项模板。

## 通过标准

- Godot 项目已被识别。
- 规则文件（`AGENTS.md` / `CLAUDE.md`）中已有 Godot 项目工具配置与图像生成配置模板。
- 项目级 Codex 配置中已有 `Godot AI MCP`，或已明确记录无法安全补齐的原因。
- 最终输出中已明确区分自动完成项与人工待办项。
