---
name: apifox
description: Apifox CLI 全功能入口。覆盖登录/项目管理、API 设计、环境/Mock、分支协作、测试用例、测试场景、自动化测试/CI、导入导出、API 生命周期工作流及问题排查。按需加载命令模块。
metadata:
  requires:
    bins: ["apifox"]
  cliHelp: "apifox --help"
agent_created: true
---

# Apifox CLI

用 Apifox CLI 完成用户请求。不要凭记忆拼 payload，优先让 `--help`、`cli-schema`、`agentHints.nextSteps` 驱动下一步。

## 安装（强制，最高优先级）

> **apifox CLI 是本 skill 的硬依赖**：做任何 apifox 操作（查询/写入/测试）前，必须先确认 `apifox` 命令可用。**未安装时必须立即安装，不得跳过、不得以"CLI 未安装"为由放弃任务、不得仅提示用户自行安装后继续**——安装是任务的前置步骤，属于本 skill 职责，不是用户的事。

### 前置检查（每个 apifox 任务的第一步）

```bash
apifox --version   # 或 which apifox
```

- 命令可用 → 继续任务
- **命令不可用 → 进入强制安装流程（下方），安装成功并验证后再继续原任务**

### 强制安装流程

1. **安装**（npm 全局）：

   ```bash
   npm install -g apifox-cli@latest
   ```

2. **下载慢/安装异常时切换国内镜像重试**：

   ```bash
   npm install -g apifox-cli@latest --registry=https://registry.npmmirror.com/
   ```

3. **验证安装**（必须）：

   ```bash
   apifox --version
   ```

   输出版本号 → 安装成功，继续；仍失败 → 报告安装失败的完整命令与错误输出，**阻断**并请用户协助（网络/权限/npm 环境），不要绕过。

4. **确认登录**：`apifox whoami`；未登录则要求用户提供 API 访问令牌执行 `apifox login --with-token <TOKEN>`（令牌在 Apifox 客户端「用户头像 → 账号设置 → API 访问令牌」创建）。凭证存 `~/.apifox/config.toml`，不要把 token 打印到日志或聊天摘要。

5. **恢复原任务**：安装 + 登录完成后，从任务断点继续，不要重新问用户"还要不要做"。

### 升级策略（区别于安装）

- 安装是**强制**的（无 CLI 必须装）；升级是**按需**的——只有命令返回版本过低/unknown command/参数缺失疑似旧版导致，或用户任务依赖新能力时，才升级
- 已装可用版本时不默认升级

### 遥测与弹窗问题（Windows）

apifox-cli 每次命令结束会异步 spawn `--telemetry-flush-worker` 子进程上报遥测数据（写入 `~/.apifox/telemetry/events.jsonl`）。在 Windows GUI 宿主（WorkBuddy / IDE / 桌面工具）中运行时，该子进程可能**弹出黑色命令窗口闪一下即关闭**，且随每次 apifox 命令反复出现。

**禁用遥测可彻底消除**（apifox-cli 内置开关，源码逻辑为 `"0"===process.env.APIFOX_CLI_TELEMETRY`）：

```bash
# Windows 用户级持久化（推荐）
[Environment]::SetEnvironmentVariable('APIFOX_CLI_TELEMETRY','0','User')

# 或临时（当前命令会话）
APIFOX_CLI_TELEMETRY=0 apifox <command>
```

要点：

- 兼容变量：`APIFOX_CLI_TELEMETRY=0` / `APIDOG_CLI_TELEMETRY=0` / `<APP>_CLI_TELEMETRY=0`，任一为 `0` 即禁用
- 设置后需**重启 GUI 宿主进程**（如 WorkBuddy）让用户环境变量全局生效；生效前跑命令显式带变量
- 已存在的 telemetry worker 残留进程（命令行形如 `win32-x64.exe C:\Users\<user>\.apifox\telemetry\flush.lock`）无害、不再弹新窗，宿主重启后消失
- 定位手段：`Get-WmiObject Win32_Process -Filter "Name='win32-x64.exe'" | Select ProcessId,CommandLine`，看 CommandLine 是否指向 `flush.lock`

## 模块按需加载

本 skill 按命令类别拆分为以下模块。**读到本文件后，根据用户任务匹配模块，立即读取对应 `modules/<name>.md`：**

| 用户任务关键词 | 加载模块 | 覆盖命令 |
|---|---|---|
| 安装、登录、项目、初次使用、help | `modules/quick-start.md` | login, project, 基础用法 |
| AI 团队、项目定位、projectId、默认项目登记、首轮未指明阻断、持久化到 PROJECT_TEST.md、新项目接入自动生成测试文档 | `modules/ai-team-project.md` | project, settings（AI 团队项目解析）；标准模板见 `references/project-test-md-template.md` |
| 接口新增/更新同步 apifox、代码→swag→import、契约校验、接口落地 | `modules/api-sync-to-apifox.md` | import, endpoint 校验, test-case 落地（与 swag 联动） |
| 接口、endpoint、Schema、目录/文件夹、安全方案 | `modules/api-design.md` | endpoint, schema, response-component, security-scheme, folder |
| 环境、变量、Mock、数据库连接、开发环境环境变量（鉴权签名/登录账号/token） | `modules/environment.md` | environment, variables, mock, database-connection |
| 分支、合并、merge request、AI 分支、pick-to | `modules/branch.md` | branch, merge-request |
| 测试用例创建/更新/运行、测试数据、处理器/断言字段（CLI 操作层） | `modules/test-case.md` | test-case, test-data |
| 鉴权自动化、token/JWT 获取与续期、401/403/签名错误、管理员账号、前置脚本自动重登 | `modules/test-auth.md` | 登录用例 extractor + preProcessor 续期 + 脚本构造 token + 全局认证 |
| 生成/补全测试用例、测试设计、测试点分析、覆盖度铁律（正/负/边界）、POST 必有完整用例（设计方法论层） | `modules/test-case-generation.md` | OpenAPI→用例生成方法论；规则同步进项目 `PROJECT_TEST.md` |
| 从 PRD/需求文档/用户故事/验收标准/功能拆分生成用例、需求追溯矩阵、五维预检、按风险选方法 | `modules/test-case-from-requirement.md` | 需求文档→用例 + RTM |
| 陷阱检查、测试失败排查、接口异常但"看起来正常" | `modules/testing-pitfalls.md` | 180 陷阱知识库（apifox 场景版） |
| 测试范围、优先级、哪些接口必测/可跳过、上线前测试 | `modules/test-selection-policy.md` | P0/P1/P2 风险分级 |
| 测试数据构造、真实数据来源、响应判定、伪通过检查 | `modules/test-data-and-judgement.md` | 参数来源优先级 + 响应判定 |
| 测试场景、多步骤、场景编排 | `modules/test-scenario.md` | test-scenario |
| 测试套件、定时任务、runner、CI、报告 | `modules/test-automation.md` | test-suite, scheduled-task, runner, run, test-report |
| 契约测试、Schema 验证、防接口漂移、结构断言 | `modules/test-contract.md` | 契约方法论 + apifox 落地 |
| 性能测试、负载、压力、并发、P95/P99 指标 | `modules/test-performance.md` | 性能方法论 + apifox 落地 |
| YAML 测试定义、批量测试、无代码测试套件设计 | `modules/test-yaml-definition.md` | YAML 设计层 → apifox 映射 |
| 健康评分、健康报告、API 健康度、上线健康评估 | `modules/test-health-score.md` | 五层健康评分方法论 |
| 导入、导出、OpenAPI、Postman、质量门禁 | `modules/import-export.md` | import, export |
| 创建一组接口、全流程、API 生命周期 | `modules/workflow.md` | 端到端工作流 |
| 命令成功但页面没有、404、找不到资源、版本问题 | `modules/troubleshooting.md` | 排查与版本确认 |

> 用户任务可能匹配多个模块（如"创建接口并写测试用例"→ 先读 api-design.md，再读 test-case.md）。按需依次加载。

## 核心共享规则

以下规则适用于**所有模块**，模块文件中不再重复。

### 基础用法

```bash
apifox --help
apifox <command> --help
apifox <command> <subcommand> --help
```

全局参数：

```text
--project <projectId>     项目 ID
--branch <branchName>     分支名；纯数字值兼容旧 branchId
--access-token <token>    覆盖当前登录 token
--api-base-url <url>      私有部署地址
```

### 登录与项目

- 未登录时让用户提供 API 访问令牌：`apifox login --with-token <TOKEN>`
- 凭证存在 `~/.apifox/config.toml`；不要把 token 打印到日志、提交到仓库或写进普通聊天摘要
- 项目未指定时，**先读项目根目录下 `PROJECT_TEST.md`**（测试域单一事实源；或用户约定的其他测试文档），命中则直接取登记的 projectId
- 项目 ID 可从「项目设置 - 基本设置 - 项目 ID」获取，或 `apifox project list`
- **首轮必须指明**：本项目此前未登记过 Apifox 项目时，必须先让用户指明 [AI] 团队下对应的项目，否则**阻断会话**（不得猜测、不得"先试试别的"）
- **指明后必须持久化**：用户指明后写入项目根目录 `PROJECT_TEST.md`（团队/项目名/projectId/默认分支/登记时间），后续会话自动复用；`AGENTS.md` / `CLAUDE.md` 只放一行指针，不重复写 projectId（避免多工具口径漂移）
- 写入本地配置文件（`PROJECT_TEST.md` 或 `.apifox/settings.json`）前先询问用户
- 「AI 团队」对应项目的 projectId 解析、登记细节与阻断话术模板，见 `modules/ai-team-project.md`

### 写入标准流程

执行 `create` 或 `update` 前必须：

1. `apifox cli-schema get <schemaKey>` — 获取 JSON schema
2. 生成资源的 JSON 数据文件
3. `apifox cli-schema validate <schemaKey> --file <path>` — 校验
4. 只有 `validate` 无误后才执行 `create` 或 `update`
5. 命令完成后读取 `agentHints.nextSteps` 继续执行或恢复

### CLI 事实优先

- 具体命令、参数、schema key 以当前 CLI 输出为准
- 如本 skill 与当前 CLI 输出不一致，以 CLI 输出执行，并同步修正本 skill

### AI 写入权限

- 写入被 AI 权限限制时，不要替用户选择，优先询问：开启目标分支直接编辑权限，或在 AI 分支上编辑
- 直接编辑主分支/迭代分支/通用分支 → 需在 Apifox 客户端 2.8.32+ 「项目设置 - 功能设置 - AI 功能设置 - 外部 AI 编辑权限」开启
- 选择 AI 分支流程：创建 AI 分支 → pick-to 导入资源 → 编辑 → 完成后提醒用户合并
- 目标主分支受保护时（isProtected），优先 `merge-request`，不要直接 `merge`

### AI 分支说明

- AI 分支是给 AI/自动化修改项目资源的隔离分支
- 24 小时内与来源分支无差异将自动归档
- AI 分支初始为空，修改源分支已有资源前必须先 `pick-to`
- AI 分支新建资源无需先导入
- AI 分支修改不会自动写回源分支；完成后必须让用户确认是否合并
- 接口新增/更新同步 apifox 默认走 AI 分支，流程见 `modules/api-sync-to-apifox.md`

### 门控与确认清单（强制）

> 合并原「必须询问用户」事项级确认与「三重门控」阶段级确认（吸收自 API 测试自动化专家版 Inversion 门控），避免概念层叠。执行前逐项核对，匹配任一即先确认再继续；门控通过不代表可以绕过"写入标准流程"与"分支参数规则"。

**事项级确认（具体操作前）**：

- 登录 token、本地配置写入、私有部署地址
- 创建/切换 AI 分支、导入源分支资源到 AI 分支
- 删除、归档、覆盖导入、批量更新等破坏性操作
- AI 分支改动 merge / merge-request 回源分支
- 是否升级 CLI

**阶段级门控（多步骤测试任务的节点处）**：

| 阶段 | 门控问题 | 触发条件 |
|------|----------|----------|
| 设计 | "测试范围是[X]，是否继续？" | 确定用例范围后、执行前 |
| 执行 | "已失败[阈值]次，是否中止并诊断？" | 失败次数达到阈值（默认 3 次） |
| 报告 | "生成[格式]报告，输出路径[path]？" | 生成报告前确认输出位置 |

- 分工：事项级在具体操作前触发；阶段级在批量测试的设计/执行/报告三个节点触发
- 执行阶段门控避免"失败硬跑"；报告阶段门控避免输出路径漂移

### 分支参数规则（全局）

- 优先使用分支名：`--branch <branchName>`
- 同一任务内查询、创建、更新、运行测试必须带同一个分支上下文
- 不要在分支任务中省略 `--branch`

### 命令输出处理

- 命令输出结果后，优先读取 JSON 里的 `agentHints.nextSteps`
- `success=false` 时以真实 `success` 字段和退出码为准，不要相信 summary 里的成功语义
