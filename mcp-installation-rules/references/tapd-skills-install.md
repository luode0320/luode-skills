## TAPD 技能包（tapd-skills）安装规则

当用户提出“下载安装 TAPD MCP / 接入 TAPD / TAPD 技能 / TAPD OpenAPI”时，按本节处理。TAPD 官方当前提供的是技能包（skills）形态：`tapd-openapi`（OpenAPI 全量调用）、`tapd-cli`（命令行封装）、`tapd-addcomment`（写评论脚本），通过环境变量 + TAPD OpenAPI 直连工作，不需要常驻 MCP server 进程；名称收口后仍统称“TAPD 技能包”。

**安装方式（归档直下，不用 git clone）：**

1. 从官方仓库归档地址下载：`https://cnb.cool/tapd.cn/skills/tapd-skills/-/git/archive/main.tar.gz`。
2. 解包后将 `skills/` 下的 `tapd-openapi`、`tapd-cli`、`tapd-addcomment` 复制到当前技能根目录（本仓库即 `C:\Users\luode\.workbuddy\skills`，符号链接指向 `D:\谷歌云盘\luode-skills`；宿主迁移时以宿主 skills 根目录为准）。
3. 已存在同名 skill 目录时不得覆盖，先对比差异再决定是否更新。
4. 下载或解包失败时，退回官方仓库页面 `https://cnb.cool/tapd.cn/skills/tapd-skills` 按当前说明处理，不得沿用第三方转述。

**凭据来源配置（项目代码/配置默认，环境变量仅作运行时覆盖）：**

按 `references/config-bootstrap.md` 的检查顺序（`./codex/config.toml` -> `./.codex/config.toml`，都缺失时创建后者），在项目级配置中补齐 TAPD 环境变量。Codex 项目级配置没有独立 env 段时，写入 `[shell_environment_policy.set]`；若用户在其他宿主（如 Claude Code）使用 JSON `env` 段，保持同一组 key：

```toml
[shell_environment_policy.set]
TAPD_API_ENDPOINT = "https://api.tapd.cn"
TAPD_TOKEN = ""
TAPD_WORKSPACE_IDS = ""
TAPD_SITE_URL = "https://www.tapd.cn"
```

- `TAPD_API_ENDPOINT`、`TAPD_SITE_URL` 使用上述默认值即可。
- `TAPD_TOKEN`、`TAPD_WORKSPACE_IDS` 允许写入项目代码/项目配置/普通维护文档并随 Git 提交；默认来源为项目代码/项目配置，环境变量可作为运行时覆盖。agent 不得代填，任何输出 / 日志 / 提交不得回显 Token 明文。
- Token 获取入口：TAPD 开放平台 `https://www.tapd.cn/open_platform/open_api_redirect`（登录后获取个人 API Token）；`TAPD_WORKSPACE_IDS` 为项目 ID 列表，逗号分隔，取自 TAPD 项目 URL。
- 配置写入后必须回读确认 UTF-8 未乱码；`TAPD_TOKEN` 仍为空时视为“已安装未激活”，提示用户填写后重启会话生效，不得阻断其他任务。

**安装后完整性校验（强制）：**

解包复制完成后，逐个 skill 目录做完整性核对，缺失即告警并补装，不得静默接受空壳 skill：

| skill | 必须存在的资源 | 缺失时处理 |
| --- | --- | --- |
| tapd-openapi | `SKILL.md` + `references/` + `scripts/` + `hooks/hooks.json` | 重新解包复制该目录 |
| tapd-addcomment | `SKILL.md` + `scripts/add_comment.py` | 同上 |
| tapd-cli | `SKILL.md`（聚合包内仅此一份，脚本见下） | 聚合包内 tapd-cli 无脚本属官方现状，不算安装损坏 |

校验命令示例（bash，`$SKILLS_ROOT` 为技能根目录）：

```bash
for d in tapd-openapi tapd-addcomment tapd-cli; do
  [ -f "$SKILLS_ROOT/$d/SKILL.md" ] || echo "[FAIL] $d 缺 SKILL.md"
done
[ -d "$SKILLS_ROOT/tapd-openapi/references" ] || echo "[FAIL] tapd-openapi 缺 references/"
[ -f "$SKILLS_ROOT/tapd-openapi/scripts/tapd_client_stdlib.py" ] || echo "[FAIL] tapd-openapi 缺 scripts/"
[ -f "$SKILLS_ROOT/tapd-addcomment/scripts/add_comment.py" ] || echo "[FAIL] tapd-addcomment 缺 scripts/"
[ -f "$SKILLS_ROOT/tapd-cli/scripts/tapd-cli.cjs" ] || echo "[INFO] tapd-cli 未补装 CLI 组件（官方聚合包如此，见下）"
```

**已知缺口（2026-08-28 实测）：官方聚合包 `skills/tapd-cli/` 仅含 SKILL.md，CLI 组件需二次安装：**

- tapd-cli 真实实现位于独立仓库 `https://cnb.cool/tapd.cn/skills/tapd-cli`（TypeScript 源码，不在聚合包内）。
- 预构建产物 `skills/tapd-cli/scripts/tapd-cli.cjs` 需 `npm run build:bundle`（esbuild 打包 src/index.ts）生成；或从 releases 下载编译二进制（install.sh / install.ps1，Windows 为 `tapd-cli-windows-x64.exe`）。
- 补装命令（Windows，Node 18+ 已就绪时）：

```bash
# 方式一：npm 构建 cjs（产出 skills/tapd-cli/scripts/tapd-cli.cjs）
git clone https://cnb.cool/tapd.cn/skills/tapd-cli /tmp/tapd-cli-src
cd /tmp/tapd-cli-src && npm install && npm run build:bundle
cp skills/tapd-cli/scripts/tapd-cli.cjs "$SKILLS_ROOT/tapd-cli/scripts/"

# 方式二：release 二进制（无需 Node）
# https://cnb.cool/tapd.cn/skills/tapd-cli/-/releases/download/latest/tapd-cli-windows-x64.exe
```

- 终端批量脚本场景优先用已补装的 cjs；未补装时降级由 `tapd-openapi` 直连 OpenAPI 完成，不要因此阻断 TAPD 任务。
- 聚合包 SKILL.md 内"git clone 到 ~/.codebuddy/skills"的安装指引已过时，以本文件为准。

**使用路由：**

- TAPD 需求 / 缺陷 / 任务 / 迭代 / Wiki / 评论 / 工时等操作，优先由 `tapd-openapi` skill 接管；写评论场景可直接用 `tapd-addcomment`；终端批量脚本场景用 `tapd-cli`（需 Node.js 18+，cjs 脚本未补装时由 `tapd-openapi` 降级，见上文「已知缺口」）。
- 用户消息出现 `https://www.tapd.cn` 或任意 `tapd.cn` 链接时，自动触发 `tapd-openapi`（按需联动 `tapd-addcomment` / `tapd-cli`），优先走 OpenAPI 而不是浏览器打开页面；执行前必须按 `tapd-openapi` 的「凭据预检」检查项目代码/配置或环境变量，`TAPD_TOKEN` 未配置时阻断 TAPD 任务并输出配置指引。
- `TAPD_TOKEN` 泄露防护：任何输出、日志、提交中不得回显 Token 明文。
