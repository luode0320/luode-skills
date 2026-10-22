---
name: tapd-cli
description: 凭据默认来源为项目代码/项目配置/普通维护文档，环境变量仅作运行时覆盖；禁止在过程性输出中回显凭据原值。TAPD OpenAPI 命令行工具。将 TAPD 平台的 OpenAPI 封装为 tapd-cli 命令，是 TAPD 查询与操作的首选通道，适用于单条查询、批量操作、终端脚本、自动化管线和 AI Agent 调用。出现 TAPD URL 或操作请求时，先检查本工具是否支持所需操作；仅 CLI 不支持或无法满足所需数据时才转用 `tapd-openapi` 的直接 API 能力，API 也无法覆盖时才按 `authenticated-url-routing-rules` 考虑浏览器。执行前遵守 `tapd-openapi` 的环境预检，`TAPD_TOKEN` 未配置时阻断并按 `tapd-env-bootstrap` 的本机真源核对环境。
allowed-tools: Bash,Read,Glob,Grep
---

# tapd-cli Skill

TAPD OpenAPI 命令行工具，无需手动拼接 curl，直接用 `tapd-cli <entity> <subcommand> [key=value]` 调用。

## TAPD 操作默认路由

- 用户要求查询或操作 TAPD 时，先用 `tapd-cli` 检查并执行所需操作；单条查询与批量操作都遵循此优先级。
- CLI 明确不支持该实体、字段或操作，或无法返回完成请求所需的数据时，才回退到 `tapd-openapi` 的直接 API 能力；不要因为网页读取失败、浏览器已有登录态或页面已打开而跳过 CLI/API。
- 只有 CLI 与直接 API 都无法满足请求中的页面专属需求（例如页面截图、富文本实际渲染或必须人工完成的页面操作）时，才按 `authenticated-url-routing-rules` 使用浏览器。凭据缺失或鉴权失败按 TAPD 环境规则处理，不得静默改用浏览器绕过。
- 用户明确要求直接操作 TAPD 页面时，按其明确指令使用浏览器；仍遵守页面安全、登录与授权边界。

## 安装

CLI 组件不在官方聚合包（`tapd-skills`）内，需从独立仓库获取预构建产物：

```bash
# 方式一：构建 cjs bundle（需 Node 18+，产出 skills/tapd-cli/scripts/tapd-cli.cjs）
git clone https://cnb.cool/tapd.cn/skills/tapd-cli /tmp/tapd-cli-src
cd /tmp/tapd-cli-src && npm install && npm run build:bundle
cp skills/tapd-cli/scripts/tapd-cli.cjs <你的skills根目录>/tapd-cli/scripts/

# 方式二：release 编译二进制（无需 Node）
# Windows: install.ps1 | macOS/Linux: install.sh，见仓库 README
```

安装后目录结构：
```
<skills根目录>/tapd-cli/
├── SKILL.md                            # 本文件
└── scripts/tapd-cli.cjs                # 预构建产物（直接运行）
```

> 注意：官方聚合包 `cnb.cool/tapd.cn/skills/tapd-skills` 内 `skills/tapd-cli/` 仅含 SKILL.md，无脚本——这是官方打包现状，不是安装损坏；脚本需按上述方式补装。

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `TAPD_API_ENDPOINT` | 是 | API 端点，如 `https://api.tapd.cn` |
| `TAPD_TOKEN` | 是 | Bearer Token（从 TAPD 开放平台获取） |
| `TAPD_WORKSPACE_IDS` | 建议 | 项目 ID，逗号分隔多个，第一个为默认值 |
| `TAPD_NPC_ROLE` | 否 | NPC 登录名，作为默认 creator |
| `TAPD_CLI_LOG` | 否 | 日志模式：`1=text`（文本）/ `json` / `silent`（默认） |

> 环境变量注入机制（Windows 用户级环境变量 / WSL `~/.bashrc` source / 真源 `~/.tapd/env.sh`）以 `tapd-env-bootstrap` 记录的本机事实为准；`TAPD_TOKEN` 缺失时先按该 skill 核对环境，再考虑重新获取 Token。

## 运行方式

需要 Node.js 18+。先从当前已加载的 `tapd-cli` 技能目录定位 `scripts/tapd-cli.cjs`，并用 `node` 直接运行该文件。若技能文件位于 Windows 盘且当前 agent 在 WSL，先用 `wslpath -u` 将该文件的 Windows 路径转换为 WSL 路径，再在 WSL 中执行：

```bash
node "<当前技能目录>/scripts/tapd-cli.cjs" --help
```

确认脚本可运行后，可按实际路径设置 shell alias，并按需将其加入当前 shell 的启动配置：

```bash
alias tapd-cli='node "<当前技能目录>/scripts/tapd-cli.cjs"'
```

设置 alias 后即可直接执行：

```bash
tapd-cli <entity> <subcommand> [key=value ...]
```

## 功能覆盖

详见仓库 [README](https://cnb.cool/tapd.cn/skills/tapd-cli)，以最新版本为准：

| 实体 | 支持操作 |
|------|---------|
| `story` | add / list / update / count / fields / custom-fields / categories / category-count / related-bugs / changes / changes-count / link / get-tcase / add-tcase / copy / link-bug / unlink-bug / all-links / batch-update |
| `bug` | add / list / update / count / fields / custom-fields / changes / changes-count / related-stories / link-tcase / copy / link-bug / unlink-bug / all-links / batch-update |
| `task` | add / list / update / count |
| `tcase` | add / batch-add / list / update / count / fields / categories / add-category / execute / assign / result / link-plan / remove-from-plan / unlink-story / count-by-category / category-count / custom-fields / story-by-tcase / import-xmind |
| `testplan` | add / list / update / count / details / progress / tcases / bugs / stories / link-story / unlink-story / by-iteration / fields / tcase-relation |
| `comment` | add / list / count |
| `iteration` | list |
| `wiki` | add / list / update / count |
| `timesheet` | add / list / update / count |
| `attachment` | list / by-entity / download / upload / upload-image / upload-image-base64 / get-image |
| `document` | download |
| `user` | info / workspaces |

## 使用示例

```bash
# 查询需求列表
tapd-cli story list workspaceid=12345678 limit=10

# 创建缺陷
tapd-cli bug add workspaceid=12345678 title="登录崩溃" severity=serious current_owner=user1

# 获取需求关联的测试用例
tapd-cli story get-tcase workspaceid=12345678 story-id=1112345678001000001

# 获取需求变更历史
tapd-cli story changes workspaceid=12345678 story-id=1112345678001000001

# 执行测试用例
tapd-cli tcase execute workspaceid=12345678 test-plan-id=456 tcase-id=789 result-status=pass last-executor=user1

# 从 xmind 导入测试用例
tapd-cli tcase import-xmind workspaceid=12345678 file=./test.xmind creator=user1
```

## 参数格式

- 所有参数使用 `key=value` 格式
- `workspaceid` 可省略（自动读取 `TAPD_WORKSPACE_IDS` 第一个值）
- 支持 `-` 和 `_` 两种分隔符：`story-id` 等价于 `story_id`

## 查看帮助

```bash
tapd-cli --help              # 所有实体
tapd-cli story --help        # 某实体子命令
tapd-cli story add --help    # 子命令详细参数
```

## 排障

已完成修复的实体选择、状态和工时语义统一见 [修复补录与工时登记](../tapd-openapi/references/completed-fix-and-timesheet.md)，本 CLI 只承接命令执行。

| 现象 | 排查路径 |
|------|---------|
| `command not found: tapd-cli` | alias 未配置或 shell 未重载；先用 `node <skills根目录>/tapd-cli/scripts/tapd-cli.cjs --help` 直连验证脚本存在 |
| 鉴权失败 / 401 | 按 `tapd-env-bootstrap` 验证 `TAPD_TOKEN` 已注入且非空（只判断有无，不回显明文），必要时重新获取 Token |
| 网络超时 / 连接失败 | 检查 `TAPD_API_ENDPOINT` 是否可达：`curl -s -m 15 -H "Authorization: Bearer $TAPD_TOKEN" "$TAPD_API_ENDPOINT/users/info"` |
| 参数报错 | 用 `tapd-cli <entity> <subcommand> --help` 查看该子命令参数；`-` 与 `_` 分隔符等价 |

### Windows agent 通过 WSL 调用 TAPD CLI

优先直接把 CLI 和业务参数作为进程参数传给 `wsl.exe`，不要把多层命令拼成一个 PowerShell 字符串。WSL 中必须显式 source 本机真源 `~/.tapd/env.sh`；不要假设 Windows 用户环境变量已传入 WSL，也不要把 `env.sh` 复制到临时目录或脚本中。

```powershell
# 先确认当前技能目录中的 bundle 在 WSL 确实可见。
$cliWindowsPath = '<当前技能目录>\scripts\tapd-cli.cjs'
$cliWslPath = (wsl.exe --exec wslpath -u $cliWindowsPath).Trim()
wsl.exe --exec test -f "$cliWslPath"
if ($LASTEXITCODE -ne 0) { throw 'WSL 无法访问 CLI bundle；按下方不可达路径处理，不要继续试写' }

# bash -c 后的参数由 "$@" 原样转发；凭据仅在 WSL 中加载。
wsl.exe --exec bash -c 'source "$HOME/.tapd/env.sh" >/dev/null 2>&1 && [ -n "${TAPD_TOKEN:-}" ] && exec "$@"' tapd-cli node "$cliWslPath" task list workspaceid=12345678 limit=10
```

执行前分别确认 CLI bundle 可读、Node.js 可运行、`~/.tapd/env.sh` 可加载且 `TAPD_TOKEN` 非空；只报告凭据有无，不输出原值。使用能传递参数数组的进程调用接口时，`bash -c` 脚本必须是一个独立参数，CLI 命令与每个 `key=value` 必须是后续独立参数；禁止再套 `bash -lc`、`cmd /c`、多层引号或用 `echo` 拼接 runner。这样可以避免登录 shell 提前返回、引号错配和 Windows CRLF 被当成 Bash 参数。

若 `wslpath` 转出的 CLI 路径不存在或无法读取，CLI 通道应明确标记为环境不可达；不要复制凭据，也不要循环重试同一路径。先按 `tapd-env-bootstrap` 核对 WSL 环境，再将**仅 CLI bundle**安装到稳定且当前 agent 可访问的位置，或在 CLI 确实不支持该操作时回退到 `tapd-openapi`。只有直接 API 也不能满足页面专属需求时才考虑浏览器。写入结果超时或不明确时，保留已取得的实体 ID，并先查询确认是否已写入，再决定是否重试。

如确需执行复杂多行脚本，脚本文件必须使用 UTF-8 无 BOM 和 LF 换行；先检查脚本与解释器可用，再显式 source WSL 凭据真源。脚本只存业务数据和命令，不含凭据值。操作结束后先回读 TAPD 实体与工时，再清理确认属于本轮的单个临时脚本。
## 开发

如需修改源码后重新构建：

```bash
git clone https://cnb.cool/tapd.cn/skills/tapd-cli /tmp/tapd-cli-src
cd /tmp/tapd-cli-src
npm install
npm run build:bundle
# 产出：skills/tapd-cli/scripts/tapd-cli.cjs，复制回 <skills根目录>/tapd-cli/scripts/
```

## 仓库地址

https://cnb.cool/tapd.cn/skills/tapd-cli
