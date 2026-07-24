---
name: mcp-installation-rules
description: 当用户要求分析项目、检查当前项目是否需要安装 MCP、判断浏览器或 Godot 编辑器应优先由哪个工具接管，或任务即将涉及前端页面验证、浏览器联动、Godot 编辑器操控且需要先根据项目结构决定是否安装 Chrome DevTools MCP 或 Godot AI MCP 时自动触发。对“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”统一按官方当前名称 `Chrome DevTools MCP` 处理。负责识别前端项目与 Godot 项目标记，给出 MCP 安装结论、优先级、Codex 配置补齐规则和后续工具让路规则；浏览器工具必须按 `references/tool-priority.md` 路由：依赖用户真实 Chrome profile 时使用 Chrome Plugin，独立调试与验证优先使用 Chrome DevTools MCP，隔离 profile / session 等核心自动化需求使用 `browser-session-automation-rules`，HAR/route、视觉 diff、录制/trace、代理或多引擎等高级验证需求使用 `browser-advanced-testing-rules`；不得将 Chrome Plugin 与 Chrome DevTools MCP 视为同一能力，工具不可用且无等价安全能力时明确阻断。此外，任何代码仓库默认推荐 CodeGraph（代码探索默认入口）与 codebase-memory-mcp（架构分析补充）这组代码图谱 MCP，安装与配置以官方仓库为准。当用户提出接入“TAPD MCP / TAPD 技能 / TAPD OpenAPI / tapd-skills”时，按本 skill 的「TAPD 技能包（tapd-skills）安装规则」处理：归档直下安装（不用 git clone），环境变量按项目级配置补齐，`TAPD_TOKEN` / `TAPD_WORKSPACE_IDS` 由用户自行填写。MCP 检测与安装默认经 parallel-task-dispatch-rules 委派子代理执行（检测只读并行、写 config 的安装串行独占），细则见 parallel-task-dispatch-rules/references/provisioning-delegation.md。
---

# MCP 安装判定规则

只在“当前项目需不需要安装 MCP，以及后续浏览器 / Godot 编辑器由谁优先接管”这个问题上使用本 skill。
如果当前只是单纯做前端实现、浏览器自动化执行或 Godot 代码修改，不要让本 skill 代替对应主域 skill。

## Skill 作用与适用场景

- 在整项目分析、环境准备或工具选型阶段，先判断当前项目是否需要补装 MCP。
- 识别前端项目标记，并要求优先接入 Chrome DevTools MCP。
- 对“谷歌浏览器 MCP”“Google Chrome MCP”“Chrome MCP”“Chrome DevTools for agents”等浏览器 MCP 说法做统一收口，避免同一工具被误当成多个候选。
- 识别 Godot 项目标记，并要求优先接入 Godot AI MCP。
- 当一个项目同时包含前端与 Godot 子项目时，允许两个 MCP 同时成为推荐安装项。
- 覆盖 Codex 本地配置缺口：若项目级 `./codex/config.toml` 或 `./.codex/config.toml` 缺少目标 MCP 配置，默认补齐而不是只停留在口头建议。以上 `./codex/config.toml` / `./.codex/config.toml` 特指 Codex CLI 的项目级 MCP 配置文件；Claude Code 的项目级 MCP 配置机制另见下方"平台判定与 Claude Code MCP 配置分支"，两者不通用，不得混用同一份配置文件语义。
- 为后续浏览器控制和 Godot 编辑器控制建立清晰的优先级，避免同类工具抢主导权。
- 仅负责 provisioning：安装、注册、配置补齐和首次可用性检查。已配置 MCP 在任务执行期间发生的 timeout、EOF、断开、失活或宿主异常，统一转给 `agent-runtime-recovery-rules`，不在本 skill 内猜测 reload/restart 命令。
- 浏览器路由唯一以 `references/tool-priority.md` 为准：Chrome Plugin（用户真实 profile）与 Chrome DevTools MCP（独立调试 / 验证）是不同能力；`browser-session-automation-rules` 仅在矩阵命中隔离 profile / session 自动化能力时使用，或作为不依赖用户 profile 的条件后备；`browser-advanced-testing-rules` 仅在矩阵命中 HAR / 视觉 diff / trace / 代理 / 多引擎等高级验证能力时使用。

## 自动触发信号

- 用户明确说“检查项目是否需要安装 MCP”“看下这个项目要不要装 MCP”“帮我判断该装哪个 MCP”。
- 用户明确提到“谷歌浏览器 MCP”“Google Chrome MCP”“Chrome MCP”“Chrome DevTools for agents”“浏览器 MCP”之类说法，希望接入或统一浏览器侧 MCP 规则。
- 用户要求先分析项目，再决定浏览器、前端验证或 Godot 编辑器要由什么工具接管。
- 当前任务即将涉及前端页面验证、浏览器联动测试、真实页面交互，但仓库中尚未明确 MCP 接管策略。
- 当前任务即将涉及 Godot 编辑器联动、场景编辑、运行项目、抓取编辑器状态，但仓库中尚未明确 MCP 接管策略。

## 进入后先做什么

1. 先读 `references/project-signals.md`，按项目结构判断是否存在前端或 Godot 标记。
2. 再读 `references/tool-priority.md`，确认“需要安装什么”与“浏览器 / Godot 后续谁优先执行”的条件路由关系；不得把 Chrome Plugin 与 Chrome DevTools MCP 合并成同一工具。
3. 再读 `references/config-bootstrap.md`，确认 `./codex/config.toml` / `./.codex/config.toml` 的检查顺序与默认补齐动作。
4. 只有在需要给出当前可参考安装来源时，再读 `references/current-sources.md`。
5. 输出结论时必须明确三件事：
   - 是否命中前端项目标记
   - 是否命中 Godot 项目标记
   - 对应 MCP 的安装建议、配置补齐结论、别名归一结果与后续执行优先级

## 默认执行流程

1. 扫描仓库根目录和常见子目录，识别前端标记与 Godot 标记。
2. 若命中前端标记：
   - 若用户使用了“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”等叫法，先统一解释为官方当前名称 `Chrome DevTools MCP`
   - 结论写为“需要安装 Chrome DevTools MCP”
   - 检查项目级 `./codex/config.toml` 与 `./.codex/config.toml`；若目标配置不存在，则默认补齐对应 MCP 配置
   - 后续浏览器工具选择按 `references/tool-priority.md` 的矩阵执行：用户已有标签、登录态、Cookie 或扩展由 Chrome Plugin 接管；独立页面调试与验证优先 Chrome DevTools MCP；隔离 profile / session 等核心自动化需求使用 `browser-session-automation-rules`；HAR / route、视觉 diff、录制 / trace、代理或多引擎需求使用 `browser-advanced-testing-rules`
   - 若仅需不依赖用户 profile 的基础自动化，且 Chrome DevTools MCP 不可用，可按矩阵条件后备到 `browser-session-automation-rules`；不满足能力或安全边界时明确阻断
3. 若命中 Godot 标记：
   - 结论写为“需要安装 Godot AI MCP”
   - 检查项目级 `./codex/config.toml` 与 `./.codex/config.toml`；若目标配置不存在，则默认补齐对应 MCP 配置
   - 后续 Godot 编辑器控制优先级写为“Godot AI MCP > 其他本地兜底方式”
   - 若同时命中场景编辑、节点调整、运行项目、抓取编辑器状态场景，要求优先让位给 Godot AI MCP
4. 若两类标记都命中：
   - 结论写为“两类 MCP 都需要安装”
   - 浏览器相关工作按 `references/tool-priority.md` 的 Chrome Plugin / Chrome DevTools MCP / `browser-session-automation-rules` / `browser-advanced-testing-rules` 条件矩阵执行
   - Godot 编辑器相关工作由 Godot AI MCP 主导
   - 若项目级 Codex 配置缺失任一 MCP，对缺失项默认补齐
5. 若两类标记都未命中：
   - 明确写“当前没有足够证据要求安装这两个 MCP”
   - 不得机械推荐安装
6. 若已确认需要某个 MCP 且项目级 Codex 配置缺失：
   - 默认补齐 `./codex/config.toml` 或 `./.codex/config.toml` 中对应 MCP 配置；两者都不存在时按 `references/config-bootstrap.md` 约定创建项目级配置文件
   - 不需要、也不得等待用户额外确认
7. 若已确认需要某个 MCP 但当前环境尚未安装或配置补齐后仍不可用（仍属于 provisioning 阶段）：
   - 先阻断对应工具类执行
   - 提醒先按该 MCP 的当前官方或项目主页说明完成安装，不要沿用过期博客或第三方转述里的旧命名、旧参数
   - 安装完成后再回到对应主域 skill
8. 若 MCP 已完成配置并在任务期间出现 timeout、EOF、连接断开或不可用：
   - 记录组件标识、失败分类和最小脱敏证据后，转交 `agent-runtime-recovery-rules` 的 `mcp_runtime_transport` owner
   - 由运行期 adapter 自行探测 `reconnect`/`reload`/`restart`/`resume` 能力；本 skill 不执行安装流程来代替运行期恢复

> MCP 分支安装细节已下沉到 references，按需读取：
>
> - 代码图谱 MCP（CodeGraph + codebase-memory-mcp）的配合规则、安装与配置详见 `references/codegraph-mcp.md`。
> - TAPD 技能包（tapd-skills）安装方式、环境变量配置与使用路由详见 `references/tapd-skills-install.md`；强约束：`TAPD_TOKEN` / `TAPD_WORKSPACE_IDS` 必须留空由用户自行填写，agent 不得代填，任何输出 / 日志 / 提交不得回显 Token 明文，TAPD 相关技能名称统一归一为“TAPD 技能包”。
> - 平台判定与 Claude Code MCP 配置分支详见 `references/claude-code-branch.md`；强约束：`./codex/config.toml` / `./.codex/config.toml` 仅指 Codex CLI 项目级配置，Claude Code 不通用，不得混用同一份配置文件语义。
> - Chrome DevTools MCP 安装流程详见 `references/chrome-devtools-codex.md`；强约束：该流程专属 Codex CLI 环境，`codex mcp add / list / get` 在 Claude Code 环境不存在，不得照搬。

## 适用安装结论模板

Codex 环境：

- `需要安装 Chrome DevTools MCP`
- `项目级 ./.codex/config.toml 已默认补齐`
- `后续浏览器工具路由：Chrome Plugin（用户真实 profile）/ Chrome DevTools MCP（独立调试验证）/ browser-session-automation-rules（隔离核心自动化条件后备）/ browser-advanced-testing-rules（高级验证条件后备），详见 references/tool-priority.md`
- `如当前会话未刷新到新 MCP，先重启 Codex 再验证`

Claude Code 结论模板（待确认阶段使用，新增）：

- `需要接入 Chrome DevTools MCP`
- `当前 Claude Code 版本的具体 MCP 配置机制尚未核实，已提示用户确认`
- `后续浏览器工具路由：Chrome Plugin（用户真实 profile）/ Chrome DevTools MCP（独立调试验证）/ browser-session-automation-rules（隔离核心自动化条件后备）/ browser-advanced-testing-rules（高级验证条件后备），详见 references/tool-priority.md`（该路由平台无关，可直接复用）

## 默认优先级

- 浏览器控制：按 `references/tool-priority.md` 条件路由：
  - `Chrome Plugin`：依赖用户已有标签、登录态、Cookie、扩展或真实 profile
  - `Chrome DevTools MCP`：独立 profile 的 DOM、控制台、Network、Performance 与页面行为验证
  - `browser-session-automation-rules`：隔离 profile、具名 session、认证登录、表单交互、批量执行；在不依赖用户 profile 的基础自动化中可作为条件后备
  - `browser-advanced-testing-rules`：HAR / route、视觉 diff、录制 / trace、代理、多引擎、多 session 观测面板
- Godot 编辑器控制：
  - `Godot AI MCP`
  - 其他 Godot 本地兜底方式（如仅运行命令、静态读文件、人工编辑）

MCP 安装、配置、注册或首次连接失败时，先触发 `execution-failure-learning-rules` 的 `recover`，查阅 [references/execution-failure-casebook.md](references/execution-failure-casebook.md)，按当前 AI 平台和官方版本复验；未验证或无法脱敏的经验不得写入 active。已配置 MCP 的运行期故障不归本 casebook，统一路由到 `agent-runtime-recovery-rules` 的 `mcp_runtime_transport`。

## 子代理委派（provisioning）

- 本 skill 的 MCP 检测与安装默认经 `parallel-task-dispatch-rules` 委派子代理执行，细则以 `../parallel-task-dispatch-rules/references/provisioning-delegation.md` 为唯一事实来源，本节只引用、不复制策略正文。
- 检测（依赖是否安装、目标 config 是否已含对应 `[mcp_servers.*]`、工具是否已暴露、项目结构标记）默认派只读检测子 agent，多工具可并行扇出，检测子 agent 禁止任何写动作。
- 写 config 的安装 / 注册默认集中到单一“安装子 agent”串行独占对应 config 文件（本 skill 写项目级 `./.codex/config.toml`）；同一时刻至多一个安装子 agent 活跃，绝不并行两个 config 写入者。
- 主 agent 负责冻结写集、汇总检测、裁决冲突、收口校验，并输出计划线程数 / 实际启动数 / 完成数 / 关闭数 / 回退原因。
- 系统规则、平台工具元数据、用户当前轮禁止仍高于该默认；无真实子代理工具或用户当轮禁止时回退主 agent 本地串行，并如实说明。

## 与相邻 skill 的边界

- 不代替 `project-design-doc-rules` 做整项目总览同步。
- 不代替 `godot-project-bootstrap-rules` 做 Godot 项目的规则文件（`AGENTS.md` / `CLAUDE.md`）模板补齐、图像配置模板补齐或环境就绪收口；本 skill 只负责 MCP 判定与项目级 Codex 配置补齐。
- 不代替 `browser-session-automation-rules` 或 `browser-advanced-testing-rules` 做实际浏览器自动化执行；浏览器工具按 `references/tool-priority.md` 的能力矩阵选择，不能用 Chrome DevTools MCP 绕过用户真实 profile，也不能用 `browser-session-automation-rules`/`browser-advanced-testing-rules` 替代需要 Chrome Plugin 登录态的任务。
- 不代替 `find-skills` 做开放生态技能搜索；这里只判断当前项目应安装什么 MCP。
- 不代替具体的前端 skill 或 Godot 项目实现规则。
- 本 skill 的 Claude Code MCP 配置分支目前仅完成判定与提示义务，具体命令细节以实际核实结果为准，不作为最终结论。

## 需要暂停并确认的条件

- 仓库同时存在大量混合技术栈，但无法判断前端或 Godot 是否为真实主项目。
- 用户明确要求不要安装任何外部 MCP。
- 当前只能发现可疑文件名，缺少足够项目结构证据支撑安装结论。

## 执行通过 / 驳回标准

- 通过：能明确指出项目是否命中前端 / Godot 标记、需要安装哪个 MCP，以及后续浏览器 / Godot 编辑器该由谁优先接管。
- 通过：能明确指出项目是否命中前端 / Godot 标记、需要安装哪个 MCP、项目级 Codex 配置是否已补齐，以及后续浏览器 / Godot 编辑器该由谁优先接管。
- 驳回：只泛泛建议“可以考虑装 MCP”，却没有项目证据、没有优先级、没有回退策略。

## references 读取规则

- 默认先读 `references/project-signals.md`。
- 只有在判断优先级和回退关系时，再读 `references/tool-priority.md`。
- 只有在判断 `./codex/config.toml` / `./.codex/config.toml` 是否缺失、该补齐哪类 MCP 配置以及如何落盘时，再读 `references/config-bootstrap.md`。
- 只有在需要给出当前推荐来源或安装入口时，再读 `references/current-sources.md`。
- 只有在需要 CodeGraph 与 codebase-memory-mcp 的配合、安装与配置细节时，再读 `references/codegraph-mcp.md`。
- 只有在处理 TAPD 技能包安装、环境变量配置或使用路由时，再读 `references/tapd-skills-install.md`。
- 只有在需要区分 Codex 与 Claude Code 平台、判断 MCP 配置分支时，再读 `references/claude-code-branch.md`。
- 只有在 Codex CLI 环境执行 Chrome DevTools MCP 安装流程时，再读 `references/chrome-devtools-codex.md`。
