# 分类与路由

本文件只定义“如何找到 owner”和“执行前检查什么”，不保存具体错误正文。具体案例由 owner skill 的 `references/*casebook*.md` 保存。

## 失败分类

先用可观察证据分类，再决定恢复动作：

| 类别 | 典型信号 | 首要检查 |
| --- | --- | --- |
| `input-contract` | 参数缺失、格式不符、非法组合 | 当前 skill/官方契约与实际参数 |
| `environment` | 依赖、路径、shell、编码、权限或版本不匹配 | local 配置、运行时版本、文件存在性 |
| `auth` | 401/403、凭据来源错误或过期 | 允许的凭据优先级；不得记录凭据值 |
| `transport` | DNS、超时、限流、连接断开 | local 网络与重试边界；区分一次性抖动 |
| `tool-contract` | MCP/CLI/API 响应结构、退出码或 flag 语义变化 | 当前工具版本与真实返回 |
| `artifact` | 退出码成功但文件缺失、损坏或不满足约束 | 产物存在性、格式和用户成功标准 |
| `workflow` | 步骤顺序、状态、上下文或路由错误 | 调用链与前置步骤 |
| `unknown` | 证据不足或多类同时成立 | 先收集证据，不得写案例 |

## 高风险域预检注册表

调用以下域的工具前自动进入 `prevent`。新增域必须先确定唯一 owner 和成功标准；不要对所有普通函数调用做全局预检。

| 域/触发 | owner skill | 预检重点 |
| --- | --- | --- |
| 位图生成、编辑、真实图像 API | `imagegen` | 通道、模型能力、参数与输出校验 |
| Windows/WSL shell、跨平台执行 | `windows-wsl-execution-rules` | shell、路径、编码、WSL/Windows 边界 |
| Windows PowerShell command-not-found、缺失 Windows CLI、PowerShell 版本/包管理器失败 | `windows-powershell-environment-rules` | `references/failure-casebook.md`、精确 manifest/package 映射、SessionEnsure/RecoverCommand 状态 |
| 浏览器自动化、隔离 profile、会话 | `agent-browser` | profile、认证上下文、页面状态 |
| URL、认证 URL、网页读取 | `authenticated-url-routing-rules` | URL 路由、登录态、来源与页面可达性 |
| MCP 安装/注册/连接 | `mcp-installation-rules` | 版本、配置来源、连接和回退 |
| Codex/AI 插件安装或启用 | `plugin-installation-rules` | 官方来源、版本、启用状态 |
| Obsidian CLI/vault 知识流 | `obsidian-knowledge-flow` | CLI-only、vault 根目录、路径与超时 |
| CodeGraph 索引、图分析 | `codegraph-analysis-rules` | 安装、索引新鲜度和项目范围 |
| Git 状态、提交、推送或恢复 | `git-collaboration-rules` | 当前轮授权、工作树与远端边界 |
| 功能/回归/策略验证 | `functional-validation-rules` | local 环境、样本、成功标准与副作用 |

未列入注册表的领域先按 `recover` 分类；如果相同缺口重复出现，转 `skill-evolution-rules` 评估是否加入注册表或补现有 skill。

Windows PowerShell 的 `CommandNotFoundException`、`command-not-found`、`not recognized` 和缺失 manifest 命令归上述 owner；Linux/WSL 原生 shell 的 `127`、`command -v` 缺失和 `/mnt/*.exe` 误用仍归 `windows-wsl-execution-rules`。两类证据不得混写到同一 failure case。

## 唯一 owner 规则

1. 先按实际失败阶段确定 owner，不按“最先被调用的工具”确定。
2. 一个案例只能有一个 canonical owner；其他 skill 只能引用案例 ID 和 owner 路径。
3. 如果两个 owner 都合理，标记 `conflicted` 并暂停自动复用，交给 `skill-evolution-rules` 或人工裁决。
4. owner 没有 casebook 时，输出结构化 candidate 交接并触发 `skill-evolution-rules`；不得在无归属目录下临时新建全局 casebook。

## 最小预检清单

- 当前调用是否命中高风险域及其 owner？
- 是否存在匹配的 `active` 案例，且环境、工具/模型版本、输入特征和适用边界均满足？
- 案例的预防动作是否与当前用户目标和当前轮授权一致？不确定时不要套用。
- local 配置是否明确？如果只能使用 test/prod 信息，立即阻断并报告环境边界。
- 预检改变参数或路径后，是否仍能用原成功标准验证？
