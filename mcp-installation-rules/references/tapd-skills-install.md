## TAPD 技能包（tapd-skills）安装规则

当用户提出“下载安装 TAPD MCP / 接入 TAPD / TAPD 技能 / TAPD OpenAPI”时，按本节处理。TAPD 官方当前提供的是技能包（skills）形态：`tapd-openapi`（OpenAPI 全量调用）、`tapd-cli`（命令行封装）、`tapd-addcomment`（写评论脚本），通过环境变量 + TAPD OpenAPI 直连工作，不需要常驻 MCP server 进程；名称收口后仍统称“TAPD 技能包”。

**安装方式（归档直下，不用 git clone）：**

1. 从官方仓库归档地址下载：`https://cnb.cool/tapd.cn/skills/tapd-skills/-/git/archive/main.tar.gz`。
2. 解包后将 `skills/` 下的 `tapd-openapi`、`tapd-cli`、`tapd-addcomment` 复制到当前技能根目录（本仓库即 `D:\luode\luode-skills`，Codex Desktop 侧经 `C:\Users\luode\.codex\skills` 符号链接自动可见）。
3. 已存在同名 skill 目录时不得覆盖，先对比差异再决定是否更新。
4. 下载或解包失败时，退回官方仓库页面 `https://cnb.cool/tapd.cn/skills/tapd-skills` 按当前说明处理，不得沿用第三方转述。

**环境变量配置（项目级 Codex 配置补齐）：**

按 `references/config-bootstrap.md` 的检查顺序（`./codex/config.toml` -> `./.codex/config.toml`，都缺失时创建后者），在项目级配置中补齐 TAPD 环境变量。Codex 项目级配置没有独立 env 段时，写入 `[shell_environment_policy.set]`；若用户在其他宿主（如 Claude Code）使用 JSON `env` 段，保持同一组 key：

```toml
[shell_environment_policy.set]
TAPD_API_ENDPOINT = "https://api.tapd.cn"
TAPD_TOKEN = ""
TAPD_WORKSPACE_IDS = ""
TAPD_SITE_URL = "https://www.tapd.cn"
```

- `TAPD_API_ENDPOINT`、`TAPD_SITE_URL` 使用上述默认值即可。
- `TAPD_TOKEN`、`TAPD_WORKSPACE_IDS` 属于用户私密配置，**必须留空并提示用户自行填写**；agent 不得代填、不得把任何真值写进仓库或示例。
- Token 获取入口：TAPD 开放平台 `https://www.tapd.cn/open_platform/open_api_redirect`（登录后获取个人 API Token）；`TAPD_WORKSPACE_IDS` 为项目 ID 列表，逗号分隔，取自 TAPD 项目 URL。
- 配置写入后必须回读确认 UTF-8 未乱码；`TAPD_TOKEN` 仍为空时视为“已安装未激活”，提示用户填写后重启会话生效，不得阻断其他任务。

**使用路由：**

- TAPD 需求 / 缺陷 / 任务 / 迭代 / Wiki / 评论 / 工时等操作，优先由 `tapd-openapi` skill 接管；写评论场景可直接用 `tapd-addcomment`；终端批量脚本场景用 `tapd-cli`（需 Node.js 18+）。
- 用户消息出现 `https://www.tapd.cn` 或任意 `tapd.cn` 链接时，自动触发 `tapd-openapi`（按需联动 `tapd-addcomment` / `tapd-cli`），优先走 OpenAPI 而不是浏览器打开页面；执行前必须按 `tapd-openapi` 的「环境预检」检查 env，`TAPD_TOKEN` 未配置时阻断 TAPD 任务并输出配置指引。
- `TAPD_TOKEN` 泄露防护：任何输出、日志、提交中不得回显 Token 明文。
