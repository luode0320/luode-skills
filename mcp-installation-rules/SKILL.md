---
name: mcp-installation-rules
description: 当用户要求分析项目、检查当前项目是否需要安装 MCP、判断浏览器或 Godot 编辑器应优先由哪个工具接管，或任务即将涉及前端页面验证、浏览器联动、Godot 编辑器操控且需要先根据项目结构决定是否安装 Chrome DevTools MCP 或 Godot AI MCP 时自动触发。对“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”统一按官方当前名称 `Chrome DevTools MCP` 处理。负责识别前端项目与 Godot 项目标记，给出 MCP 安装结论、优先级、Codex 配置补齐规则和后续工具让路规则；浏览器工具必须按 `references/tool-priority.md` 路由：依赖用户真实 Chrome profile 时使用 Chrome Plugin，独立调试与验证优先使用 Chrome DevTools MCP，隔离 session、HAR/route、视觉 diff、录制/trace、代理或多引擎需求使用 `agent-browser`；不得将 Chrome Plugin 与 Chrome DevTools MCP 视为同一能力，工具不可用且无等价安全能力时明确阻断。此外，任何代码仓库默认推荐 CodeGraph（代码探索默认入口）与 codebase-memory-mcp（架构分析补充）这组代码图谱 MCP，安装与配置以官方仓库为准。
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
- 浏览器路由唯一以 `references/tool-priority.md` 为准：Chrome Plugin（用户真实 profile）与 Chrome DevTools MCP（独立调试 / 验证）是不同能力；`agent-browser` 仅在矩阵命中隔离或高级自动化能力时使用，或作为不依赖用户 profile 的条件后备。

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
   - 后续浏览器工具选择按 `references/tool-priority.md` 的矩阵执行：用户已有标签、登录态、Cookie 或扩展由 Chrome Plugin 接管；独立页面调试与验证优先 Chrome DevTools MCP；隔离 profile / session、HAR / route、视觉 diff、录制 / trace、代理或多引擎需求使用 `agent-browser`
   - 若仅需不依赖用户 profile 的基础自动化，且 Chrome DevTools MCP 不可用，可按矩阵条件后备到 `agent-browser`；不满足能力或安全边界时明确阻断
3. 若命中 Godot 标记：
   - 结论写为“需要安装 Godot AI MCP”
   - 检查项目级 `./codex/config.toml` 与 `./.codex/config.toml`；若目标配置不存在，则默认补齐对应 MCP 配置
   - 后续 Godot 编辑器控制优先级写为“Godot AI MCP > 其他本地兜底方式”
   - 若同时命中场景编辑、节点调整、运行项目、抓取编辑器状态场景，要求优先让位给 Godot AI MCP
4. 若两类标记都命中：
   - 结论写为“两类 MCP 都需要安装”
   - 浏览器相关工作按 `references/tool-priority.md` 的 Chrome Plugin / Chrome DevTools MCP / `agent-browser` 条件矩阵执行
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

## 代码图谱 MCP（CodeGraph + codebase-memory-mcp）

适用于任何需要长期理解和维护的代码仓库（不限前端 / Godot）。这是一组配合使用的代码图谱 MCP：

| 工具 | 仓库 | 定位 |
|------|------|------|
| CodeGraph | `colbymchenry/codegraph` | **默认入口**：日常理解代码、查调用链、分析改动影响 |
| codebase-memory-mcp | `DeusData/codebase-memory-mcp` | **架构分析补充**：项目架构关系、跨模块依赖、函数调用频率、Route/Service/Controller 关系、ADR 记录 |

**配合规则：**

- CodeGraph 作默认入口，codebase-memory-mcp 作高级图分析工具；不要用 memory-mcp 替代日常的 CodeGraph 探索。
- 仅在架构层任务（架构梳理、跨模块依赖、调用频率统计、ADR）才补充使用 codebase-memory-mcp。
- 两个工具的结果与当前代码不一致时，以当前代码为准，并重新同步对应索引。

**安装与配置：**

- CodeGraph 的强制安装与 `codegraph init` 初始化由 `project-agents-bootstrap` 的 CodeGraph 准备规则负责。
- codebase-memory-mcp 按官方仓库 `https://github.com/DeusData/codebase-memory-mcp` 的当前说明安装并建立索引；**不要沿用第三方博客转述里的旧命名、旧参数或旧安装路径**，一切以官方仓库 README 为准。
- 两者均为 stdio 类 MCP，需要时把对应 server 配置补齐到项目级 MCP / Codex 配置（与本 skill 其他 MCP 的配置补齐策略一致）。
- 安装或建立索引失败时，回退到 CodeGraph，再回退到本地搜索与文件读取，不阻塞主任务。

## 平台判定与 Claude Code MCP 配置分支（新增）

以上"覆盖 Codex 本地配置缺口"及下方"Chrome DevTools MCP 安装流程"中出现的 `./codex/config.toml` / `./.codex/config.toml` 特指 Codex CLI 的项目级 MCP 配置文件；Claude Code 的项目级 MCP 配置机制另见本节，两者不通用，不得混用同一份配置文件语义。

执行本 skill 任何配置补齐动作前，先判断当前运行环境是 Codex 还是 Claude Code：

- **Codex 分支**：完全复用下方"Chrome DevTools MCP 安装流程"小节（该小节专属 Codex CLI 环境），逐字不变。
- **Claude Code 分支（待确认）**：当前尚未实测确认 Claude Code 的项目级 MCP 配置具体机制（可能是项目根目录 `.mcp.json` 文件，也可能存在 `claude mcp add` 等命令，需在实际 Claude Code 版本中核实）。在核实之前，遇到 Claude Code 环境下的 MCP 安装/配置需求时：
  - 不得照搬 Codex 分支的 `codex mcp add/list/get` 命令，这些命令在 Claude Code 环境不存在，执行会直接失败（`command not found`）；
  - 应先向用户确认当前 Claude Code 版本支持的 MCP 配置方式（可查阅当前会话可用的官方文档/帮助，或询问用户），确认后再执行配置补齐动作；
  - 若确认存在等价的项目级配置文件（如 `.mcp.json`），比照 Codex 分支的"检测缺失 → 默认补齐最小可用配置"思路执行，但具体 key/value schema 需以确认结果为准，不得照抄 Codex 的 TOML `command`/`args` 字段名假设它们同样适用于 Claude Code 的 JSON schema；
  - 配置补齐后的可用性检查同理，需要用当前确认的 Claude Code 等价命令/机制替代 `codex mcp list` / `codex mcp get`，若没有等价查询手段，则通过让用户在下一次会话中确认新 MCP 是否出现在可用工具列表来间接验证。

## Chrome DevTools MCP 安装流程（本节专属 Codex CLI 环境）

当项目命中前端标记，且用户希望当前会话后续由浏览器侧 MCP 接管时，按下面流程执行：

1. 先统一名称为 `Chrome DevTools MCP`，不要把“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”拆成多个工具名。
2. 先检查项目级配置路径：
   - `./codex/config.toml`
   - `./.codex/config.toml`
3. 如果项目级配置不存在，默认创建 `./.codex/config.toml`。
4. 如果项目级配置中没有 `chrome-devtools` 对应项，默认补齐最小可用配置：
   - `command = "npx"`
   - `args = ["-y", "chrome-devtools-mcp@latest"]`
5. 如果当前运行环境是 Windows 且需要更稳的启动路径，优先使用官方仓库给出的 Windows 兜底参数，而不是自己臆造命令。
6. 执行安装命令：
   - `codex mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest`
7. 安装后立即做可用性检查：
   - `codex mcp list`
   - `codex mcp get chrome-devtools`
8. 如果工具已写入但会话里还看不到新 MCP，先重启 Codex 会话或刷新当前会话，再做页面验证。
9. 页面联调与验证按 `references/tool-priority.md` 的条件矩阵执行：用户真实 profile 走 Chrome Plugin，独立调试 / 验证优先 Chrome DevTools MCP，隔离或高级自动化走 `agent-browser`；不得用线性优先级替代场景判断。

## 适用安装结论模板

Codex 环境：

- `需要安装 Chrome DevTools MCP`
- `项目级 ./.codex/config.toml 已默认补齐`
- `后续浏览器工具路由：Chrome Plugin（用户真实 profile）/ Chrome DevTools MCP（独立调试验证）/ agent-browser（隔离或高级自动化条件后备），详见 references/tool-priority.md`
- `如当前会话未刷新到新 MCP，先重启 Codex 再验证`

Claude Code 结论模板（待确认阶段使用，新增）：

- `需要接入 Chrome DevTools MCP`
- `当前 Claude Code 版本的具体 MCP 配置机制尚未核实，已提示用户确认`
- `后续浏览器工具路由：Chrome Plugin（用户真实 profile）/ Chrome DevTools MCP（独立调试验证）/ agent-browser（隔离或高级自动化条件后备），详见 references/tool-priority.md`（该路由平台无关，可直接复用）

## 默认优先级

- 浏览器控制：按 `references/tool-priority.md` 条件路由：
  - `Chrome Plugin`：依赖用户已有标签、登录态、Cookie、扩展或真实 profile
  - `Chrome DevTools MCP`：独立 profile 的 DOM、控制台、Network、Performance 与页面行为验证
  - `agent-browser`：隔离 session、多 session、HAR / route、视觉 diff、录制 / trace、代理、多引擎；在不依赖用户 profile 的基础自动化中可作为条件后备
- Godot 编辑器控制：
  - `Godot AI MCP`
  - 其他 Godot 本地兜底方式（如仅运行命令、静态读文件、人工编辑）

MCP 安装、配置、注册或首次连接失败时，先触发 `execution-failure-learning-rules` 的 `recover`，查阅 [references/execution-failure-casebook.md](references/execution-failure-casebook.md)，按当前 AI 平台和官方版本复验；未验证或无法脱敏的经验不得写入 active。已配置 MCP 的运行期故障不归本 casebook，统一路由到 `agent-runtime-recovery-rules` 的 `mcp_runtime_transport`。

## 与相邻 skill 的边界

- 不代替 `project-design-doc-rules` 做整项目总览同步。
- 不代替 `godot-project-bootstrap-rules` 做 Godot 项目的规则文件（`AGENTS.md` / `CLAUDE.md`）模板补齐、图像配置模板补齐或环境就绪收口；本 skill 只负责 MCP 判定与项目级 Codex 配置补齐。
- 不代替 `agent-browser` 做实际浏览器自动化执行；浏览器工具按 `references/tool-priority.md` 的能力矩阵选择，不能用 Chrome DevTools MCP 绕过用户真实 profile，也不能用 `agent-browser` 替代需要 Chrome Plugin 登录态的任务。
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
