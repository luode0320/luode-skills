---
name: tapd-cli
description: 凭据默认来源为项目代码/项目配置/普通维护文档，环境变量仅作运行时覆盖；禁止在过程性输出中回显凭据原值。TAPD OpenAPI 命令行工具。将 TAPD 平台的全量 OpenAPI 封装为 tapd-cli 命令，适用于终端脚本、自动化管线和 AI Agent调用（批量/脚本化操作走本工具，单次交互查询走 tapd-openapi）。当用户给出 `tapd.cn` 链接且需要批量 / 终端化操作时随 `tapd-openapi` 自动联动触发；执行前遵守 `tapd-openapi` 的环境预检，`TAPD_TOKEN` 未配置时阻断并按 `tapd-env-bootstrap` 的本机真源核对环境。
allowed-tools: Bash,Read,Glob,Grep
---

# tapd-cli Skill

TAPD OpenAPI 命令行工具，无需手动拼接 curl，直接用 `tapd-cli <entity> <subcommand> [key=value]` 调用。

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

安装后目录结构（本机 WorkBuddy 已补装）：
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

需要 Node.js 18+。本机（WorkBuddy）脚本位于 `~/.workbuddy/skills/tapd-cli/scripts/tapd-cli.cjs`，添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
alias tapd-cli="node ~/.workbuddy/skills/tapd-cli/scripts/tapd-cli.cjs"
# 其他宿主按实际 skills 根目录调整；找不到时先执行 `tapd-cli --help` 探测
```

之后即可直接执行：

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

| 现象 | 排查路径 |
|------|---------|
| `command not found: tapd-cli` | alias 未配置或 shell 未重载；先用 `node <skills根目录>/tapd-cli/scripts/tapd-cli.cjs --help` 直连验证脚本存在 |
| 鉴权失败 / 401 | 按 `tapd-env-bootstrap` 验证 `TAPD_TOKEN` 已注入且非空（只判断有无，不回显明文），必要时重新获取 Token |
| 网络超时 / 连接失败 | 检查 `TAPD_API_ENDPOINT` 是否可达：`curl -s -m 15 -H "Authorization: Bearer $TAPD_TOKEN" "$TAPD_API_ENDPOINT/users/info"` |
| 参数报错 | 用 `tapd-cli <entity> <subcommand> --help` 查看该子命令参数；`-` 与 `_` 分隔符等价 |

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
