# 分类与路由

本文件只定义“如何找到 owner”和“执行前检查什么”，不保存具体错误正文。具体案例由 owner skill 的 `references/*casebook*.md` 保存。

MCP/插件相关动作必须先区分 provisioning（安装、注册、启用、首次可用性检查）与 runtime（已配置组件在任务执行期间的超时、断开、失活或宿主异常）。前者仍由安装类 skill 负责；后者统一由 `agent-runtime-recovery-rules` 负责恢复能力协商、重载/重启和任务续接。没有真实 adapter 能力时不得猜测平台命令。

## 失败分类

先用可观察证据分类，再决定恢复动作：

| 类别 | 典型信号 | 首要检查 |
| --- | --- | --- |
| `input-contract` | 参数缺失、格式不符、非法组合 | 当前 skill/官方契约与实际参数 |
| `environment` | 依赖、路径、shell、编码、权限或版本不匹配 | local 配置、运行时版本、文件存在性 |
| `auth` | 401/403、凭据来源错误或过期 | 允许的凭据优先级；不得记录凭据值 |
| `transport` | DNS、超时、限流、连接断开 | local 网络与重试边界；区分一次性抖动；已配置 MCP 的运行期故障转 `mcp_runtime_transport` |
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
| Windows PowerShell command-not-found、缺失 Windows CLI、PowerShell 版本/包管理器失败、已确认 Git Bash 中 Windows CLI 不可见 | `windows-powershell-environment-rules` | `references/failure-casebook.md`、精确的每源 manifest/package 映射、SessionEnsure/RecoverCommand JSON 状态；未确认 Git Bash、`wsl.exe`、Linux 127 或 `/mnt/*.exe` 不走此 owner |
| 浏览器核心自动化、隔离 profile、会话 | `browser-session-automation-rules` | profile、认证上下文、页面状态 |
| 浏览器高级验证、HAR/网络记录、视觉 diff、trace/代理/多引擎 | `browser-advanced-testing-rules` | 网络记录、视觉基线、trace/性能样本、代理配置 |
| URL、认证 URL、网页读取 | `authenticated-url-routing-rules` | URL 路由、登录态、来源与页面可达性 |
| MCP 安装/注册/首次连接 | `mcp-installation-rules` | 版本、配置来源、初次连接和回退；仅限 provisioning 阶段 |
| Codex/AI 插件安装或启用 | `plugin-installation-rules` | 官方来源、版本、启用状态；仅限 provisioning 阶段 |
| 已配置 MCP 的运行期超时、EOF、断开或不可用 | `agent-runtime-recovery-rules` | `mcp_runtime_transport`；能力探测、单飞锁、预算、重连/重载/重启和恢复后健康验证 |
| 已启用插件运行期失活、崩溃或无响应 | `agent-runtime-recovery-rules` | `plugin_runtime_unhealthy`；仅按 adapter 声明的 reload/restart 能力执行 |
| 智能体宿主进程异常、重启或任务续接 | `agent-runtime-recovery-rules` | `agent_host_unhealthy`；检查点、宿主生命周期能力和恢复后续接验证 |
| Obsidian CLI/vault 知识流 | `obsidian-knowledge-flow` | CLI-only、vault 根目录、路径与超时 |
| CodeGraph 索引、图分析 | `codegraph-analysis-rules` | 安装、索引新鲜度和项目范围 |
| Git 状态、提交、推送或恢复 | `git-collaboration-rules` | 当前轮授权、工作树与远端边界 |
| 功能/回归/策略验证 | `functional-validation-rules` | local 环境、样本、成功标准与副作用 |

未列入注册表的领域先按 `recover` 分类；如果相同缺口重复出现，转 `skill-evolution-rules` 评估是否加入注册表或补现有 skill。`agent-runtime-recovery-rules` 尚未提供真实 adapter 的平台只能降级为观测/人工交接，不得把安装命令、进程名或 UI 操作当作通用恢复接口。

Windows PowerShell 的 `CommandNotFoundException`、`command-not-found`、`not recognized` 和缺失 manifest 命令归上述 owner。Git Bash 只有在 `git.exe` 根目录下的 `bin\\bash.exe` 经 `uname -s` 确认是 `MINGW` 或 `MSYS` 后，才可作为该 owner 的 Windows CLI 可见性证据。Linux/WSL 原生 shell 的 `127`、`command -v` 缺失、`wsl.exe` 路由和 `/mnt/*.exe` 误用仍归 `windows-wsl-execution-rules`。两类证据不得混写到同一 failure case。

### Provisioning/runtime 分流

- 配置文件缺失、安装命令失败、注册失败、版本不兼容或首次连接未建立：归安装类 skill；可以查阅其 casebook，并保留现有官方命令事实。
- 已成功配置并曾经可用的组件在任务期间出现 timeout、EOF、连接断开、插件失活或宿主异常：归 `agent-runtime-recovery-rules`；安装类 skill 只提供组件标识和 provisioning 证据，不执行恢复动作。
- 只有在 runtime adapter 明确声明且真实验证 `reconnect`、`reload`、`restart` 或 `resume` 能力时，agent 才能执行对应动作；否则转 `manual_handoff`/`blocked`。

## 唯一 owner 规则

1. 先按实际失败阶段确定 owner，不按“最先被调用的工具”确定。
2. 一个案例只能有一个 canonical owner；其他 skill 只能引用案例 ID 和 owner 路径。
3. 如果两个 owner 都合理，标记 `conflicted` 并暂停自动复用，交给 `skill-evolution-rules` 或人工裁决。
4. owner 没有 casebook 时，输出结构化 candidate 交接并触发 `skill-evolution-rules`；不得在无归属目录下临时新建全局 casebook。
5. provisioning 与 runtime 证据不得合并成一个案例；同一组件从“未安装”到“已配置后断连”必须分别记录在安装类 casebook 与运行期 owner casebook。

## 最小预检清单

- 当前调用是否命中高风险域及其 owner？
- 当前失败发生在 provisioning 还是 runtime？如果组件已配置并进入任务执行，不能继续沿用安装类 owner。
- 是否存在匹配的 `active` 案例，且环境、工具/模型版本、输入特征和适用边界均满足？
- 案例的预防动作是否与当前用户目标和当前轮授权一致？不确定时不要套用。
- local 配置是否明确？如果只能使用 test/prod 信息，立即阻断并报告环境边界。
- 预检改变参数或路径后，是否仍能用原成功标准验证？
