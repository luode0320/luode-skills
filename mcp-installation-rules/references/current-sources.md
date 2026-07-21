# 当前推荐来源

以下来源用于“确认当前该装什么、去哪里看最新安装说明”，不是要把某一条命令硬编码到所有环境里。

## Chrome DevTools MCP

- 官方当前产品名会同时出现 `Chrome DevTools MCP` 与 `Chrome DevTools for agents`；本仓库在规则判定里统一记作 `Chrome DevTools MCP`。
- Chrome 官方说明：
  - `https://developer.chrome.com/docs/devtools/agents`
  - `https://developer.chrome.com/docs/devtools/agents/get-started`
- 官方仓库：
  - `https://github.com/ChromeDevTools/chrome-devtools-mcp`

使用原则：

- 默认以 Chrome 官方文档和官方仓库的最新安装说明为准。
- 若用户说“谷歌浏览器 MCP”或“Google Chrome MCP”，回答时先做一次名称归一，再引用官方来源。
- 后续浏览器控制优先让位给该 MCP，而不是继续默认使用其他浏览器工具。

## Godot AI MCP

- Godot Asset Library 中的 `Godot AI` 条目：
  - `https://godotengine.org/asset-library/asset/5050`
- 活跃项目主页：
  - `https://github.com/hi-godot/godot-ai`

使用原则：

- Godot 生态变化较快，默认以项目主页或资产库中的当前安装说明为准。
- 后续只要任务涉及 Godot 编辑器操控，就优先让位给该 MCP。

## TAPD 技能包（tapd-skills）

- 官方技能仓库：
  - `https://cnb.cool/tapd.cn/skills/tapd-skills`
- 归档直下地址（默认安装方式，不用 git clone）：
  - `https://cnb.cool/tapd.cn/skills/tapd-skills/-/git/archive/main.tar.gz`
- Token 获取入口（TAPD 开放平台，登录后获取个人 API Token）：
  - `https://www.tapd.cn/open_platform/open_api_redirect`

使用原则：

- 用户口中的“TAPD MCP”默认按 `tapd-skills` 技能包处理（含 `tapd-openapi` / `tapd-cli` / `tapd-addcomment` 三个 skill），通过环境变量 + TAPD OpenAPI 直连工作，不需要常驻 MCP server 进程。
- 默认安装方式是下载归档解包，不用 `git clone` 拉取仓库历史。
- `TAPD_TOKEN`、`TAPD_WORKSPACE_IDS` 属于用户私密配置，由用户自行填写，不得代填、不得写入示例真值。
