# 当前推荐入口

以下入口用于“确认当前浏览器或 Godot 任务应走哪条本地工具链”，不是要把旧 MCP 路线重新设回默认值。

## 浏览器 CLI

- 本仓库统一浏览器控制入口：`agent-browser`
- 参考入口：
  - `../../agent-browser/SKILL.md`
  - `../../agent-browser/references/commands.md`

使用原则：

- 默认以后两份本地 skill 文档为准。
- 若当前环境未全局安装 `agent-browser`，优先使用 `npx -y agent-browser ...` 方式运行。
- 若用户说“谷歌浏览器 MCP”或“Chrome DevTools for agents”，回答时先说明这属于历史命名，再收口到 `agent-browser`。
- 不再默认推荐重新引入浏览器 MCP。

## Godot CLI

- 本地可执行入口优先级：
  - `godot4`
  - `godot`
  - 项目自带启动脚本或封装命令

建议检查方式：

- `godot4 --version`
- `godot --version`
- 项目已有脚本时，优先读取项目内约定

使用原则：

- 只要任务涉及 Godot 编辑器操控、运行验证、截图或读取运行态，优先走本地 Godot CLI / 编辑器命令行。
- 不再默认推荐重新引入旧 Godot MCP 路线。
