---
name: plugin-installation-rules
description: 当用户要求分析项目、检查是否需要安装某个 AI 编码插件 / agent 增强插件，或提到具体插件名（如 Ponytail）需要安装、启用、配置时自动触发。负责通用的"插件检测 → 安装 → 验证 → 使用 → 回退"流程，适用于 Claude Code、Codex 等多种 AI 环境；安装命令与配置一律以官方仓库为准，拒绝沿用第三方博客/公众号转述的旧命名、旧参数或臆造命令。具体插件条目（含 Ponytail）见 references/plugin-catalog.md，未来新增插件只追加条目、不改框架；其中标记为【必装】的插件（当前为 Ponytail）在会话 / 项目准备时默认强制安装与启用。不要用它代替 mcp-installation-rules 的 MCP server 判定，也不代替具体编码 / 测试 / 审查 skill。插件检测与安装默认经 parallel-task-dispatch-rules 委派子代理执行（检测只读并行、写 config 的安装串行独占），细则见 parallel-task-dispatch-rules/references/provisioning-delegation.md。
---

# 插件检测安装使用规则

只在"当前是否需要安装 / 启用某个 AI 编码插件，以及装好后怎么用"这个问题上使用本 skill。
与 `mcp-installation-rules`（负责 MCP server 判定与配置）并列：本 skill 负责"AI 编码插件 / agent 增强"这一类工具。

## Skill 作用与适用场景

- 判断当前项目 / 会话是否需要某个插件。
- 给出以官方仓库为准的安装命令、配置补齐、可用性验证。
- 明确装好后的使用方式、强度 / 参数和回退策略。
- 通用支持多 AI 环境（Claude Code、Codex 等），不绑定单一 AI。
- 作为可扩展框架：每个插件一个条目，未来加插件只追加条目、不改框架。
- 仅负责 provisioning：插件检测、安装、启用、配置和首次可用性验证。已启用插件在任务执行期间失活、崩溃、超时或无响应，统一转给 `agent-runtime-recovery-rules`，不在本 skill 内臆造 reload/restart 命令。

## 自动触发信号

- 用户提到具体插件名（如 `Ponytail`），希望安装、启用或配置。
- 用户问"这个插件能不能用""帮我装上这个插件""怎么启用 XXX 插件"。
- 用户分享某插件的文章 / 链接，希望吸收成可安装、可用的能力。
- 当前任务即将用到某插件提供的能力，但会话尚未安装 / 启用它。

## 进入后先做什么

1. 先确认插件名称，并归一到官方名称（避免第三方转述的别名、错名）。
2. 读 `references/plugin-catalog.md`，确认该插件是否已有条目。
3. 若有条目：按条目里以官方为准的安装命令、配置、使用方式执行。
4. 若无条目：先查证官方仓库 README 拿到准确信息，再按统一格式补一个新条目，再安装。
5. 确认当前 AI 环境（Claude Code / Codex / 其他），选对应平台的安装方式。

## 默认执行流程

1. 名称归一（统一到官方名）。
2. 查条目 / 查官方仓库，确认它是什么、支持哪些平台。
3. 按当前 AI 平台选择并执行官方安装命令。
4. 配置补齐（如该插件需要配置文件或环境变量）。
5. 可用性验证（按插件官方说明确认已生效）。
6. 说明使用方式、强度 / 参数。
7. 安装或启用失败时（仍属于 provisioning 阶段），回退到不依赖该插件的常规流程并记录。
8. 已启用插件在任务期间失活、崩溃、超时或无响应时，记录插件标识和最小脱敏证据，转交 `agent-runtime-recovery-rules` 的 `plugin_runtime_unhealthy` owner；由运行期 adapter 决定是否支持 reload/restart/resume。

## 必装插件（默认强制）

`references/plugin-catalog.md` 中标记为【必装】的插件，按与 CodeGraph 同等强度处理：

- 新会话 / 项目自举准备时，默认检测是否已安装；未安装则按当前 AI 环境的官方方式安装，不需要用户额外确认。
- 安装命令能由 agent 直接执行的（如 Codex 的 `codex plugin marketplace add ...`），直接执行。
- 安装需交互式命令、agent 无法直接触发的（如 Claude Code 的 `/plugin ...` 斜杠命令），必须提示用户执行对应命令并等待其确认，不要假装已安装。
- 安装或启用失败时，记录不可用并回退到常规流程，不阻塞主任务。

**当前必装清单：**

- Ponytail（详见 `references/plugin-catalog.md` 条目）：默认启用，强度 `full`。

## 关键原则

- **以官方仓库为准**：安装命令、参数、配置一律以插件官方仓库 README 为准；**严禁沿用第三方博客 / 公众号转述里的旧命名、旧参数或臆造命令**——这些经常与官方不符（例如 Ponytail，第三方文章给的 `npx ponytail init` 与官方 `/plugin marketplace add` 完全不同）。
- **通用多 AI**：同一插件常有 Claude Code / Codex / Cursor 等多种接入方式，按当前 AI 环境选对应方式，不要把某一种当成唯一。
- **安全边界**：减码 / 优化类插件不得削弱数据校验、访问控制、输入验证等安全代码。
- **失败回退**：安装或启用失败时，明确记录不可用，回退到常规流程，不阻塞主任务。

## 子代理委派（provisioning）

- 本 skill 的插件检测与安装默认经 `parallel-task-dispatch-rules` 委派子代理执行，细则以 `../parallel-task-dispatch-rules/references/provisioning-delegation.md` 为唯一事实来源，本节只引用、不复制策略正文。
- 检测（插件是否已安装 / 启用、依赖是否就绪、项目结构标记）默认派只读检测子 agent，多插件可并行扇出，检测子 agent 禁止任何写动作。
- 涉及写 config 的安装 / 注册默认集中到单一“安装子 agent”串行独占对应 config 文件；插件官方以平台命令安装时，命令级安装可独立执行，但任何 config 文件写不得并发。
- 主 agent 负责冻结写集、汇总检测、裁决冲突、收口校验，并输出计划线程数 / 实际启动数 / 完成数 / 关闭数 / 回退原因。
- 系统规则、平台工具元数据、用户当前轮禁止仍高于该默认；无真实子代理工具或用户当轮禁止时回退主 agent 本地串行，并如实说明。

## 与相邻 skill 的边界

插件安装、启用或首次可用性验证失败时，先触发 `execution-failure-learning-rules` 的 `recover`，查阅 [references/execution-failure-casebook.md](references/execution-failure-casebook.md)，保留官方来源、平台和版本边界；恢复成功后自动写 candidate，active 仍需授权。已启用插件的运行期失活不归本 casebook，统一路由到 `agent-runtime-recovery-rules` 的 `plugin_runtime_unhealthy`。

- 不代替 `mcp-installation-rules`：那个负责 MCP server 的判定与配置；本 skill 负责 AI 编码插件 / agent 增强。
- 不代替具体的编码、测试、审查 skill 的领域工作。
- 不代替 `find-skills` 的开放生态技能搜索。

## 执行通过 / 驳回标准

- 通过：能明确插件名称、当前 AI 平台对应的官方安装命令、配置、验证方式、使用方式与回退策略；信息以官方仓库为准。
- 驳回：只泛泛说"装个插件试试"，没有官方来源、没有平台区分、没有验证与回退；或直接照搬第三方博客的旧 / 错命令。

## references 读取规则

- 默认读 `references/plugin-catalog.md` 确认插件条目。
- 新增插件时，按该文件的条目格式追加，并标注官方仓库来源。
