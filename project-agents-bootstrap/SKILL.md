---
name: project-agents-bootstrap
description: 若当前 AI 为 Claude Code，目标规则文件为 `CLAUDE.md`；若为 Codex，目标规则文件为 `AGENTS.md`；新会话第一轮默认自动触发（不依赖用户意图）；也可被”创建、补齐或更新 AGENTS.md / CLAUDE.md / 补充仓库级规则”等显式请求触发。负责在项目根目录强制检测 AGENTS.md / CLAUDE.md：不存在则必须创建最小可用模板，存在则对受管章节执行增量补齐与幂等 upsert，既保留用户已有规则，也持续同步最新仓库规则；同时确保包含注释类任务流程、跨平台 UTF-8 文件写入约束、按平台能力矩阵执行的会话动态重命名规则，以及”上下文压缩后必须重新读取项目根目录规则文件再继续主任务”的硬规则。若仓库命中 Godot 项目标记，还必须额外补齐 Godot 工具接管与图像生成配置模板，并明确规则文件里不能存真实密钥；图像生成配置必须同步主通道与回退规则，且回退规则必须写成 `回退规则：回退配置` 的层级结构，并在其下声明 `api` / `baseurl`；若仓库需要长期记忆与长期风格，两者都要同步引入 `project-memory-rules` 和 `project-style-rules`，并确保其最低命中要求写入仓库级规则。当用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 更新这几个 md”等聚合指令时，本 skill 作为统一入口，一次性编排项目根目录 `AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md` 四个核心 md 的“检测→缺失则创建→已存在则增量补齐”；其中 `PROJECT_MEMORY.md` 必须继续保持为唯一长期记忆主文件，但内部补齐为“人类阅读区 + 底部机器索引区”的单文件双区结构，且不得新增 `PROJECT_MEMORY_INDEX.yaml`。
---

# 项目 AGENTS.md 自举与补齐 Skill

## AI 环境检测与规则文件约定

本 skill 统一用"规则文件"指代与当前 AI 对应的仓库级配置文件：

- **Codex 环境**：规则文件 = `AGENTS.md`
- **Claude Code 环境**：规则文件 = `CLAUDE.md`

检测方式（按优先级）：

1. 若仓库根目录已存在 `AGENTS.md` 或 `CLAUDE.md` 其中一个，使用已存在的那个
2. 若两者都不存在，根据当前运行 AI 创建对应文件（Claude → `CLAUDE.md`，Codex → `AGENTS.md`）
3. 若两者都存在，使用与当前 AI 对应的文件，并在输出中标注另一个文件的存在

## 目标

- 让仓库在新会话中也能稳定执行项目规则。
- 把“会话记忆”转成“仓库常驻约束”。
- 把 `Plan Mode` 的默认计划外壳沉到仓库级规则里，保证所有计划型提问都会先触发 `implementation-planning-rules` 再回流前置域。
- 若仓库是 Godot 项目，自动补齐 Godot 工具接管和图像生成配置模板，并把图像通道的主配置与回退规则一起写全。

## 仓库级总控规则

- 处理本仓库任务时，必须先命中并加载至少五个基础 skill。
- 最低要求：至少命中 `skill-hit-check-rules`、`parallel-task-dispatch-rules`、`reasoning-summary-structure-rules`、`project-memory-rules`、`project-style-rules`。
- 若本轮涉及创建、补齐或更新仓库级规则文件（`AGENTS.md` 对应 Codex，`CLAUDE.md` 对应 Claude Code），默认额外启用 `project-agents-bootstrap` 进行自举补齐；该规则同样适用于其他项目仓库。对已经存在的规则文件，也必须继续做增量同步与受管章节 upsert，而不是只初始化一次。
- 首轮规则文件、`.gitattributes`、`.editorconfig` 自举是硬闸门：若其中任一缺失、未创建、未补齐或未完成受管章节同步，判定为阻断，禁止进入任何项目分析、读码、需求、Bug、编码、测试或交付主任务，必须先更新补充完成后再继续。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若命中 `parallel-task-dispatch-rules`，中间进度必须额外输出当前并行技能列表；若最终未并行，明确写 `并行技能:无`。
- 本仓库默认处于 subagent 完全授权模式：用户已明确允许 agent 在任务可切分、写集不冲突、风险可控且环境支持时自动启动 subagent / delegation / parallel agent work；该项目级 standing authorization 视为满足工具显式授权条件。
- 进入分析、侦察、需求、Bug、审查、测试、文档或编码等实质执行前，主 agent 必须自主判断是否存在可由 subagent 并行推进的独立问题、证据来源、文件集、模块边界或职责边界；不得只依赖固定 skill 映射表。
- 只要判定为可并行或条件并行，且当前环境支持 subagent / multi-agent / thread 能力、当前轮授权或项目级完全授权成立、无明确禁止或写集冲突，必须优先真实启动子 agent 并行执行；不能只输出线程分配或并行建议。
- 项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，即使没有固定并行 skill，也应优先尝试拆出只读 sidecar 子任务交给 subagent；主 agent 保留最终判断、归纳和冲突裁决职责。
- 单一根因、需求边界、接口契约、schema 或架构方向等需要统一裁决的主路径必须串行；其旁路证据收集、影响面盘点和资料检索可在边界清晰时条件并行。
- 若计划并行但真实子 agent 启动失败、环境不支持或被阻断，必须说明计划线程数、实际启动数、关闭/回收数和回退原因，不得把计划并行伪装成已并行。
- 需求阶段只允许围绕真实缺口一次推进一个关键问题；禁止把 agent 猜测写成待确认答案，禁止“先做了再补需求”，正式需求主文档未真实落盘前禁止进入实施规划与正式编码。
- 用户若在当前轮显式提出计划型问题（如“怎么做”“先给计划”“先出方案和步骤”“这个怎么改”），必须先命中计划规则；即使前置条件尚未齐备，也要输出受限计划 / 阻断计划，而不是表现成计划规则未触发。
- 当前上下文处于 `Plan Mode` 时，必须把 `implementation-planning-rules` 作为第一层计划外壳先命中，再按需回流需求侦察、需求接入、缺口、边界、拆分或其他域；这条路由优先级高于普通计划型提问。
- 当前运行环境若要求用 `<proposed_plan>` 或其他专用计划包裹输出，包裹层不改变项目内计划格式；计划正文仍必须遵守 `implementation-planning-rules` 与 `plan-structure-template.md` 的结构、字段和约束，不得退化成通用摘要式计划。
- Plan Mode 硬闸门：若计划正文以 `Summary`、`Key Changes`、`Public Interfaces`、`Test Plan`、`Assumptions` 等通用工程计划小节作为主结构，或缺少“当前计划最终方案的简要说明、agent 理解的问题 / 目标、本轮范围、非范围、当前优先闭环、关键假设 / 待确认点、实施周期、阶段计划、最小任务、真实测试、任务完成条件、任务停止 / 结束条件、最大推进边界”任一核心字段，直接判定为无效计划，必须立即按 `plan-structure-template.md` 重写；不得解释为“简化版计划”或继续进入实施。
- 用户使用“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现 / 按建议执行 / 按方案执行 / 就按你刚才说的做”等开工类指令时，不得视为无边界长文本执行授权；必须先确认已有执行计划，或当场给出本轮执行计划、任务完成条件、任务停止 / 结束条件和最大推进边界。缺少这些边界时，禁止直接进入实现 / 执行。
- 受限计划不得作为实施授权；用户即使明确采纳，agent 也只能先补齐缺失前置条件并将其升级为正式执行计划，未升级前禁止进入编码、改码、重构、测试实施或其他执行动作。
- 若当前轮只是采纳 agent 上一轮或更早轮次给出的建议、方案、修复路线或实施思路，也必须先把该建议收口成正式执行计划，才允许继续实现 / 执行；不得把聊天建议直接当成可执行计划。
- 实施规划阶段默认采用只读计划模式：禁止写代码、禁止边计划边试做；只允许读仓库、定依赖、列风险、拆任务、写实施文档。实施计划正文开头必须先写“当前计划最终方案的简要说明”，用 1-3 句先交代推荐方案、主落点和为什么这么做；随后再写 agent 对当前问题的理解，至少交代问题 / 目标、本轮范围、非范围、当前优先闭环和关键假设 / 待确认点，再进入“依赖图 + 垂直切片”的最小闭环任务拆分；避免按前端 / 后端 / 数据库水平分层堆计划。单任务默认尽量控制在约 5 个文件以内，且每个最小任务都必须先完成自己的真实测试、审查、验收闭环后，才允许推进下一个任务。涉及代码生成、修改或重构的计划，必须显式写出真实测试入口、依赖环境、样本 / 数据来源和通过标准；`build`、`lint`、静态检查或人工阅读不算真实测试，免测只能写在纯文档、纯注释、纯排版、纯静态资源改名 / 搬运或不会影响运行结果的场景里；若计划涉及代码生成、修改或重构，“现状与落点”必须给出代码落点目录树，不能只写文件名或普通条目。
- 若连 `skill-hit-check-rules` 或 `parallel-task-dispatch-rules` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 `skill-audit-rules` 进行只读审计。
- 自动审查白名单只保留 `implementation-review-rules` 与最终收口前的 `project-change-review-rules`。
- `project-change-review-rules` 同时支持两类触发：用户明确要求审查当前改动，或本轮存在代码改动且准备最终收口。
- `code-review-automation-rules` 仅用于当前分支提交级审查，不纳入默认自动审查链。
- 任何 agent 收到用户明确结束指令（如“结束”“停止”“到此为止”“不要继续”“不要下一步建议”“不要扩散”）时，必须立即停止自动继续和扩散性输出，只允许给出必要的最小收口结论。
- 若命中 `autonomous-execution-rules`，自动继续只允许用于“完成原始用户目标仍必需的动作”；不得把“进一步优化 / 可继续整理 / 总结里的下一步建议 / 未来迭代建议”自动升级成新的执行目标。
- 当原始用户目标已经完成或用户已给出明确结束指令，且不存在完成原始目标仍必需的动作时，必须停止连续执行并直接结束；不得输出“下一步状态”“下一步建议”“等待用户新指令”“无需继续动作”等任何可能触发循环 loop 的占位区块或扩散性文案，除非用户明确要求后续建议。
- 若当前运行环境存在 goal / plan / task 等显式状态收口机制，且原始用户目标已经完成或已满足该机制的阻断条件，必须在最终收口前真实执行对应收口动作；只写完成文案不算真正结束运行时状态。Codex goal 仅是其中一种特例。
- 若当前会话刚发生”压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 `context-compression-rules`，并在继续主任务前重新读取当前项目根目录规则文件。
- 当当前会话进入明确需求、Bug、实施、审查、测试、提交或其他可命名任务，且标题为空泛、过时或不匹配当前任务时，必须自动命中 `thread-title-rules`，生成中文简要并按平台能力矩阵调用真实线程重命名工具更新当前会话标题；Codex 优先使用 `set_thread_title`，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认显式跳过；任务主题尚未稳定、标题已准确、工具不可用或用户明确禁止时记录跳过。

## 触发条件

- 默认自动触发（强制）：
  - 新会话第一轮必须执行本 skill（不依赖用户意图是否为项目分析）。
  - 首轮执行时必须先做一次根目录规则文件（`AGENTS.md` / `CLAUDE.md`）检测。
  - 首轮执行时必须同时检查 `.gitattributes`、`.editorconfig` 是否存在且满足最小可用约束。
  - 在规则文件（`AGENTS.md` / `CLAUDE.md`）、`.gitattributes`、`.editorconfig` 三者全部完成自举前，禁止进入项目分析、架构梳理、代码阅读、需求、Bug、编码、测试与交付主任务。
  - 若当前上下文处于 `Plan Mode`，首轮自举期间还必须先把 `implementation-planning-rules` 的默认外壳路由同步进仓库级规则，再继续其他主任务；不得只补规则文件却遗漏计划路由。
  - 遇到创建、补齐或更新仓库级规则文件（`AGENTS.md` / `CLAUDE.md`）的请求时必须执行。
- 用户显式要求（仍然支持）：
  - 创建 `AGENTS.md` 或 `CLAUDE.md`
  - 自动检查并补齐 `AGENTS.md` 或 `CLAUDE.md`
  - 补充仓库级执行规则
  - 解决”新会话规则遗漏”
- 统一 md 聚合指令（强制）：
  - 用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 更新这几个 md / 补充更新 md”等聚合表达（含语义等价）时，必须进入“统一 md 补齐编排”，对 `AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md` 全部走一遍“检测→缺失则创建→已存在则补齐”，不得只更新其中一两个就收口。
- 兜底触发：
  - 任意阶段检测到仓库根目录缺失规则文件（`AGENTS.md` / `CLAUDE.md`），必须立即补齐后再继续主任务。

## 会话动态重命名规则

- 当当前 Codex / Claude / agent 会话进入明确需求、Bug、实施、审查、测试、提交或其他可命名任务，且会话标题为空泛、过时、泛称或不匹配当前任务时，必须自动命中 `thread-title-rules`。
- `thread-title-rules` 负责生成 8-24 字中文简要标题，并按平台能力矩阵调用当前环境真实线程重命名工具更新当前会话标题；Codex 环境优先使用真实 `set_thread_title` 工具，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认视为无真实自动改名工具并显式跳过。
- 会话重命名不等待用户显式要求；但任务主题尚未稳定、标题已准确、工具不可用、无法可靠确定当前会话 ID 或用户明确禁止时必须跳过，并说明原因。
- `CLAUDE.md` 仅用于 Claude Code 仓库规则自举，不等同于 Claude Desktop 已具备自动会话改名能力。
- 标题采用“任务对象 + 动作 / 症状 / 阶段”的中文简要写法，避免只写“提交 git”“开始实施”“继续做”“修复 bug”“更新文档”等泛化动作标题。
- 禁止用正文伪造工具调用、raw directive 或猜测结果来宣称已经改名；所有标题变更必须来自真实工具返回。

## 统一 md 补齐编排（根据 skill 补充更新 md）

当用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 更新这几个 md / 补充更新 md”等聚合指令（含语义等价）时，本 skill 作为统一入口，对项目根目录四个核心 md 逐个执行“检测 → 缺失则创建 → 已存在则增量补齐”：

| 目标文件 | 负责 skill | 缺失时动作 | 已存在时动作 |
|---------|-----------|-----------|-------------|
| `AGENTS.md`（Codex）/ `CLAUDE.md`（Claude Code） | `project-agents-bootstrap`（本 skill） | 按最小模板创建对应规则文件 | 受管章节增量同步与幂等 upsert |
| `PROJECT_MEMORY.md` | `project-memory-rules` + `project-agents-bootstrap` | 按双区主文档模板创建，至少补齐人类阅读区与底部机器索引区骨架 | `project-agents-bootstrap` 只负责检测 / 创建 / 补齐双区骨架；事实抽取、实体关系更新仍由 `project-memory-rules` 负责 |
| `PROJECT_STYLE.md` | `project-style-rules` | 按风格主文档模板创建 | 按风格合并规则增量回写 |

编排要求：

1. 四个文件都必须走一遍“检测 → 创建或补齐”，不得只更新其中一两个就收口。
2. `AGENTS.md` / `CLAUDE.md` 按本 skill 受管章节规则处理；`PROJECT_MEMORY.md` 必须联动 `project-memory-rules`，并继续保持“单文件双区”结构；`PROJECT_STYLE.md` 必须联动 `project-style-rules`，由各自 skill 决定具体写入与合并细节。
3. 当前 AI 为 Claude Code 时规则文件取 `CLAUDE.md`，为 Codex 时取 `AGENTS.md`；两者都已存在时按本 skill 既有规则同步全部已存在规则文件。
4. 四个 md 可按文件边界并行补齐（联动 `parallel-task-dispatch-rules`），但必须等全部落盘后统一核对，缺任一文件不得宣称完成。
5. 最终回复必须逐文件给出结果：新建 / 更新 / 跳过原因，禁止只给整体一句“已更新”。
6. `PROJECT_MEMORY.md` 缺失时创建双区骨架；已存在但缺少 `## 机器索引区` 时只补底部受管区；已存在且双区完整时只做最小同步，不重写已有正文区。
7. `project-agents-bootstrap` 不负责从代码或对话抽取事实，不负责重建全部正文词条；它只负责双区骨架的检测、创建与幂等补齐。

## 执行步骤

1. 优先执行脚本：`scripts/bootstrap_agents.sh`（默认当前目录，可通过 `--repo` 指定仓库）。
2. 只要进入本 skill，就不能停留在“已读取规则但未落盘”的状态；必须真的执行脚本，而不是只阅读 `SKILL.md` 或口头说明。
3. 若仓库内已存在多个规则文件（例如根目录与 `game/AGENTS.md` 或 `game/CLAUDE.md`），必须同步所有已存在规则文件的受管章节，不能只更新根目录后静默忽略子工程规则文件。
4. 定位项目根目录（通常为当前工作目录）。
5. 检查根目录是否存在规则文件（`AGENTS.md` 或 `CLAUDE.md`）。
6. 若不存在：必须创建最小可用规则文件（`AGENTS.md` 或 `CLAUDE.md`）（禁止跳过）。
7. 若存在：对受管章节做增量同步，缺失则追加，已存在则更新为最新规则，非受管内容保持不动；不能退化为”只初始化一次、后续不再同步”。
8. 若仓库根目录缺失 `.gitattributes` 或 `.editorconfig`，必须一并补齐最小可用版本，用于固定 `LF`、`UTF-8`、末尾换行和基础编辑器行为。
9. 若仓库根目录缺失 `PROJECT_MEMORY.md`，或该文件缺少 `## 机器索引区`，必须通过脚本补齐最小双区骨架；不得改为创建 `PROJECT_MEMORY_INDEX.yaml`。
10. 若首轮尚未完成规则文件（`AGENTS.md` / `CLAUDE.md`）、`.gitattributes`、`.editorconfig` 或 `PROJECT_MEMORY.md` 双区骨架中任一项的创建、补齐或受管章节同步，必须立即停止后续主任务；此时唯一允许继续的工作是完成这些仓库级文件更新，不得先做项目分析再回补。
11. 执行脚本后必须立刻核对结果，至少包含：

- 受管章节是否真的写入最新内容
- 是否同步到了所有已存在的规则文件（`AGENTS.md` / `CLAUDE.md`）
- `PROJECT_MEMORY.md` 是否存在且具备 `## 机器索引区`
- `git diff -- AGENTS.md CLAUDE.md .gitattributes .editorconfig */AGENTS.md` 或等价检查中是否只出现预期改动

12. 若脚本未执行、执行失败、只同步了部分规则文件、未补齐 `PROJECT_MEMORY.md` 双区骨架、或执行后未核对结果，判定为阻断，禁止宣称已完成自举。
13. 必须确保文档包含以下最低规则：

- 严禁脑补工具调用与结果（最高优先级）：任何文件/命令/搜索/网络的读取与执行必须经真实工具调用完成，严禁在正文编写 `<invoke>`/`<result>`/伪 function_calls 假装调用或凭记忆想象文件内容当结果；引用代码/行号/函数名前必须来自本轮真实工具返回；发现大段重复行、错乱行号、源码异常以代码块结束符收尾等迹象立即停止并重发真实工具调用、用 `md5sum`/`wc -c` 交叉校验。
- Skill 命中强制规则：
  - 处理本仓库任务时，必须先命中并加载至少五个基础 skill。
  - 最低要求：至少命中 `skill-hit-check-rules`、`parallel-task-dispatch-rules`、`reasoning-summary-structure-rules`、`project-memory-rules`、`project-style-rules`。
  - 若本轮涉及创建、补齐或更新仓库级规则文件（`AGENTS.md` / `CLAUDE.md`），默认额外启用 `project-agents-bootstrap` 进行自举补齐；该规则同样适用于其他项目仓库。
  - 必须在首条中间进度明确输出当前命中的 skill 列表。
  - 若命中 `parallel-task-dispatch-rules`，中间进度必须额外输出当前并行技能列表；若最终未并行，明确写 `并行技能:无`。
  - 本仓库默认处于 subagent 完全授权模式：用户已明确允许 agent 在任务可切分、写集不冲突、风险可控且环境支持时自动启动 subagent / delegation / parallel agent work；该项目级 standing authorization 视为满足工具显式授权条件。
  - 进入分析、侦察、需求、Bug、审查、测试、文档或编码等实质执行前，主 agent 必须自主判断是否存在可由 subagent 并行推进的独立问题、证据来源、文件集、模块边界或职责边界；不得只依赖固定 skill 映射表。
  - 只要判定为可并行或条件并行，且当前环境支持 subagent / multi-agent / thread 能力、当前轮授权或项目级完全授权成立、无明确禁止或写集冲突，必须优先真实启动子 agent 并行执行；不能只输出线程分配或并行建议。
  - 项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，即使没有固定并行 skill，也应优先尝试拆出只读 sidecar 子任务交给 subagent；主 agent 保留最终判断、归纳和冲突裁决职责。
  - 单一根因、需求边界、接口契约、schema 或架构方向等需要统一裁决的主路径必须串行；其旁路证据收集、影响面盘点和资料检索可在边界清晰时条件并行。
  - 若计划并行但真实子 agent 启动失败、环境不支持或被阻断，必须说明计划线程数、实际启动数、关闭/回收数和回退原因，不得把计划并行伪装成已并行。
  - 需求阶段只允许围绕真实缺口一次推进一个关键问题；禁止把 agent 猜测写成待确认答案，禁止“先做了再补需求”，正式需求主文档未真实落盘前禁止进入实施规划与正式编码。
  - Plan Mode 硬闸门：若计划正文以 `Summary`、`Key Changes`、`Public Interfaces`、`Test Plan`、`Assumptions` 等通用工程计划小节作为主结构，或缺少“当前计划最终方案的简要说明、agent 理解的问题 / 目标、本轮范围、非范围、当前优先闭环、关键假设 / 待确认点、实施周期、阶段计划、最小任务、真实测试、任务完成条件、任务停止 / 结束条件、最大推进边界”任一核心字段，直接判定为无效计划，必须立即按 `plan-structure-template.md` 重写；不得解释为“简化版计划”或继续进入实施。
  - 用户使用“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现 / 按建议执行 / 按方案执行 / 就按你刚才说的做”等开工类指令时，不得视为无边界长文本执行授权；必须先确认已有执行计划，或当场给出本轮执行计划、任务完成条件、任务停止 / 结束条件和最大推进边界。缺少这些边界时，禁止直接进入实现 / 执行。
  - 若当前轮只是采纳 agent 上一轮或更早轮次给出的建议、方案、修复路线或实施思路，也必须先把该建议收口成正式执行计划，才允许继续实现 / 执行；不得把聊天建议直接当成可执行计划。
  - 实施规划阶段默认采用只读计划模式：禁止写代码、禁止边计划边试做；只允许读仓库、定依赖、列风险、拆任务、写实施文档。实施计划正文开头必须先写“当前计划最终方案的简要说明”，用 1-3 句先交代推荐方案、主落点和为什么这么做；随后再写 agent 对当前问题的理解，至少交代问题 / 目标、本轮范围、非范围、当前优先闭环和关键假设 / 待确认点，再进入“依赖图 + 垂直切片”的最小闭环任务拆分；避免按前端 / 后端 / 数据库水平分层堆计划。单任务默认尽量控制在约 5 个文件以内，且每个最小任务都必须先完成自己的真实测试、审查、验收闭环后，才允许推进下一个任务。涉及代码生成、修改或重构的计划，必须显式写出真实测试入口、依赖环境、样本 / 数据来源和通过标准；`build`、`lint`、静态检查或人工阅读不算真实测试，免测只能写在纯文档、纯注释、纯排版、纯静态资源改名 / 搬运或不会影响运行结果的场景里；若计划涉及代码生成、修改或重构，“现状与落点”必须给出代码落点目录树，不能只写文件名或普通条目。
  - 若连 `skill-hit-check-rules` 或 `parallel-task-dispatch-rules` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
  - 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 `skill-audit-rules` 进行只读审计。
  - 自动审查白名单只保留 `implementation-review-rules` 与最终收口前的 `project-change-review-rules`。
  - `project-change-review-rules` 同时支持两类触发：用户明确要求审查当前改动，或本轮存在代码改动且准备最终收口。
  - `code-review-automation-rules` 仅用于当前分支提交级审查，不纳入默认自动审查链。
- 注释任务强制流程：
  - 先声明命中的注释类 skill。
  - 读取对应 `SKILL.md` 后再改代码。
  - 最终回复给执行证据（改动点、UTF-8、格式化/编译/测试结果）。
- 文件编码与写入规则：注释默认中文；所有代码、文档、配置、脚本、测试资产和生成类文本文件新增或修改时默认使用 UTF-8；禁止 GBK、ANSI、系统默认编码或编辑器默认编码落盘；命令行写文件必须显式指定 UTF-8，写后回读并检查 `git diff`。
- 图像生成强制规则：
  - 只要当前用户请求属于生图、改图、参考图出新图、sprite、动作帧、概念图、UI 位图、贴图、透明底抠图、2D 游戏素材预览或其他位图资产任务，必须自动命中 `imagegen`，不得等用户额外明确说“使用 imagegen”。
  - 命中 2D 游戏素材相关任务时，若涉及设计图、预览图、原始素材图、动作关键帧或 sprite 方向图，除命中领域 skill 外，还必须联动命中 `imagegen`。
  - 对于生图任务，允许的“原始图产生方式”只有真实图像生成/编辑链路：内置 `image_gen`，或经验证可用的 `imagegen` CLI/API 图像通道。
  - 严禁把 Pillow、SVG、HTML/CSS/canvas、脚本拼接、程序绘制、几何组合、占位图、自动排版图、后处理脚本输出伪装成“已完成生图结果”或“最终素材”。
  - CLI fallback 仅表示“改走 imagegen 的脚本入口去调用真实图像生成/编辑 API”，不表示允许退化成脚本合成图片；凡是不经过真实图像模型生成的结果，一律不得作为生图成品交付。
  - 如果内置 `image_gen` 不可用，必须先验证 `imagegen` CLI/API 链路；若也不可用，则明确阻断并只允许交付 prompt、brief、参考候选、动作规划等中间信息，不得交付脚本生成图冒充成品。
  - 后处理脚本只允许在“真实生成出的原始图”基础上做去背、切帧、对齐、拼表、预览整理；不得替代 imagegen 负责原始创作出图。
- 只要本轮实际发生了 imagegen 生图或改图，最终回复必须向用户明确汇报本次生图路径与本次实际使用的模型名；例如 `生图路径: CLI fallback` 与 `生图模型: gpt-image-2`。若走 built-in 且拿不到精确模型名，也必须明确写成 `生图模型: built-in image_gen（底层精确模型名当前环境未暴露）`，不得省略。
- 最小改动原则：注释补充不改变业务逻辑。
- 本地连接调试测试红线：需求侦察、Bug 复现 / 定位 / 运行时调试、功能验证、回归测试、上线接口测试、浏览器联调、启动前后端服务或执行任何测试脚本时，所有数据库、缓存、消息队列、HTTP/RPC 上游、前端 / 后端服务连接都只能使用 `local` 本地环境；`test`、`prod`、`production`、`staging`、`pre`、`release` 等非 local 环境一律禁止连接；即使用户提供连接串或临时授权，也必须记录为环境阻断并要求改用 local。
- 依赖与工具复用优先规则：编写代码前先检索项目工具类 / npm / GitHub 开源库，优先复用，禁止重复造轮子；引入新依赖须确认许可证兼容与维护活跃；确需自行实现须在注释或 PR 说明中写明原因。
- Windows / WSL 执行规则（代码在 WSL 文件系统内 `/home/<user>/<project>`）：
  - 只有执行类动作才优先进入 WSL：编译、运行、启动程序、测试、调试，以及会真实启动运行时的依赖安装
  - **agent 在 WSL（推荐）**：直接 `cd /home/<user>/<project>` 执行执行类命令；普通命令也可直接在当前 shell 完成，无需包裹
  - **agent 在 Windows（如 Claude Desktop GUI）**：普通仓库命令优先使用 Git Bash / bash；PowerShell 只用于 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求的场景
  - 看代码、改代码、搜索、规则检查、普通 git 经 `\\wsl.localhost\<distro>\home\<user>\<project>` 或 Git Bash / bash 可访问的等价路径访问
  - 执行类动作通过 `wsl.exe --cd /home/<user>/<project> <command>` 进 WSL 执行
  - 为什么只有执行类动作在 WSL：只有 WSL 进程能正常联网，且运行产物面向 Linux；普通读写、搜索、规则检查不依赖 WSL 运行时
  - 命令格式：执行类命令用 `wsl.exe --cd /home/<user>/<project> <command>`（默认发行版；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`）
  - 用户可访问文件引用：回复用户时，凡引用项目内文件都按用户当前环境可打开的路径输出；项目在 WSL 且用户从 Windows 桌面访问时，Markdown 链接、普通文本路径、审查证据路径、截图说明和最终总结中的项目内文件路径都使用 `\\wsl.localhost\<distro>\home\<user>\<project>\...`；只有命令参数、WSL shell 上下文和日志原文保留 `/home/<user>/<project>`
  - 不再使用 `/mnt/<drive>`——代码已在 WSL，用 `/home/<user>/...` 与 `\\wsl.localhost\...`；纯 Windows 项目或本轮不执行程序时不要误切 WSL
  - 编码约束：仓库提交 `.gitattributes` 与 `.editorconfig`，固定 UTF-8；`.gitattributes` 默认 `* text=auto`，`*.sh`/`*.yaml` 显式 `eol=lf`
- CodeGraph 强制准备规则：未安装 `codegraph` 时，必须从 `colbymchenry/codegraph` 强制下载安装到当前服务器 / 电脑；安装后必须为当前项目初始化 CodeGraph；全程不需要用户确认。
- 代码图谱 MCP 配套：架构层分析可补充安装 codebase-memory-mcp（`DeusData/codebase-memory-mcp`，按官方说明安装，非强制、失败不阻塞）；安装判定与配合规则详见 `mcp-installation-rules`。
- 插件检测安装：涉及 AI 编码插件（如 Ponytail）的安装、启用、配置时，联动 `plugin-installation-rules`，以官方仓库为准、claude/codex 通用。Ponytail 为默认必装插件，会话/项目准备时默认安装并启用。
- 若仓库命中 Godot 项目标记，还必须补齐：
  - `## Godot 项目工具配置`
  - `## 图像生成配置`
  - 其中 `图像配置:` 块只能声明读取位置、`baseurl`、模型名、优先级和回退规则，不能写真实 `OPENAI_API_KEY`
  - 图像配置应同时包含：
    - 主通道：优先 `baseurl=https://api.openai.com/v1`，模型优先写最新可用的 `gpt-image` 系列，例如 `gpt-image-1`
    - 回退规则：回退配置
      - `api: ''`
      - `baseurl: ''`
  - 回退规则：如果用户项目规则文件已声明回退配置里的 `api` / `baseurl`，则在当前进程环境变量之后优先使用该回退配置作为项目图像通道；若未声明回退配置或回退配置不可用，再继续使用项目主配置与 `~/.codex/auth.json`、`~/.codex/config.toml` 的默认配置；若这些也都不可用，则允许降级到人工补图或占位图，不得伪造已生成结果

9. 若当前服务器 / 电脑未安装 `codegraph` CLI，或当前仓库尚未初始化 CodeGraph：
   - 未安装时必须先从 `https://github.com/colbymchenry/codegraph` 强制下载并安装 `codegraph`
   - 安装入口优先使用官方仓库提供的安装方式：Windows PowerShell 使用 `$PSDefaultParameterValues['Invoke-WebRequest:UseBasicParsing']=$true; $PSDefaultParameterValues['Invoke-RestMethod:UseBasicParsing']=$true; irm -UseBasicParsing https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex`，macOS / Linux 使用 `curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh`，已有 npm 环境时也可使用 `npm i -g @colbymchenry/codegraph`
   - 安装完成后必须在当前项目根目录执行 `codegraph init`，生成 `.codegraph/` 并建立索引
   - 不需要、也不得等待用户确认
   - 初始化成功后再按对应 skill 使用
   - 下载、安装或初始化失败则直接回退，不阻塞主任务
   - 若在 Windows PowerShell 5.1 下执行远端安装脚本、下载资源或请求 GitHub API，必须显式使用 `-UseBasicParsing`，或预先设置 `Invoke-WebRequest` / `Invoke-RestMethod` 的默认 `UseBasicParsing`，避免弹出人工确认框
10. 输出结果时给出：

- 规则文件（`AGENTS.md` / `CLAUDE.md`）是否新建/更新。
- 受影响的规则文件列表，明确哪些被同步。
- `.gitattributes` / `.editorconfig` 是否新建/更新。
- 更新了哪些规则段落。
- 是否执行了格式检查（如仅文档变更可不跑编译）。

## 脚本用法

- 默认当前目录：`scripts/bootstrap_agents.sh`
- 指定仓库：`scripts/bootstrap_agents.sh --repo /path/to/repo`
- 幂等执行：可重复运行，已有章节不会重复追加。

## 最小模板（缺失时使用）

以下模板适用于 `AGENTS.md`（Codex）和 `CLAUDE.md`（Claude Code），文件名按当前 AI 环境选择，内容结构相同。

````md
# AGENTS.md / CLAUDE.md

> Codex 使用 `AGENTS.md`，Claude Code 使用 `CLAUDE.md`，内容规则相同。

## 适用范围

- 本文件适用于本仓库下所有代码与文档变更。

## Skill 强制自动触发规则（最高优先级）

- **所有 skill 的触发不依赖用户主动通知**，AI 必须基于任务内容、工作目录、用户意图主动检测并触发
- 每轮处理用户消息时，必须主动扫描所有可用 skill 的触发条件，符合条件的 skill 必须被调用
- `skill-hit-check-rules` 每轮必须作为第一个 tool call 被调用，无例外
- 禁止以下理由跳过应触发的 skill：
  - “用户没有明确说需要这个 skill”
  - “任务看起来简单，不需要 skill”
  - “我已经知道怎么做了”
  - “这不是核心 skill”
- 违反本规则视为流程违规，必须立即停止当前执行，回到命中检查重走

### 项目长期上下文文档自动加载（强制）

- 会话开始（含新会话首轮、上下文压缩续做后）必须检测项目根目录四个长期上下文文档：`AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md`。
- 存在即读取并加载为当前上下文；缺失即按各自主文档模板创建；其后随对话与代码变化持续维护，不是只建一次。
- `PROJECT_MEMORY.md` 记忆对象：指标、参数、表字段、缓存键、变量、公式、方法映射、别名等反复出现且需长期复用的事实（联动 `project-memory-rules`）。
- `PROJECT_STYLE.md` 记忆对象：方法、注释、错误处理、日志、接口等代码写法样例（联动 `project-style-rules`）。
- 来源优先级：当前项目代码 > 最近对话 > 已有文档 > 旧记忆 / 旧风格；来源冲突时以高优先级为准。
- 缺失则按各自 `references` 主文档模板创建；只写明确事实，合并去重，刷新「更新时间」，并在「变更记录」补写变更原因。
- 单一主文档原则：每类长期上下文只维护一份根目录主文档，不产生衍生文件。

## 严禁脑补工具调用与结果（最高优先级，强制）

- 任何对文件、命令、搜索、网络的读取与执行，必须通过真实工具调用（独立 tool call）完成；严禁在回复正文里编写 `<invoke>` / `<result>` / 伪 function_calls 文本假装调用工具，也禁止凭记忆“想象”文件内容当作已读取结果。
- 引用任何文件内容、行号、函数名、配置值前，必须来自本轮真实工具返回；未真实读取不得断言具体代码或数据。
- 若发现输出出现大段重复行、错乱或重复行号、源码文件莫名以 Markdown 代码块结束符收尾、import 与实际用法矛盾等异常，立即判定为生成异常：停止后重新发起真实工具调用，并用 `md5sum` / `wc -c` 等独立命令交叉校验再继续。
- 关键文件读取建议附带指纹校验（`md5sum` + `wc -c`），确保所读即磁盘真实内容。
- 违反本条视为最高级别流程违规。

## 严禁自动提交 Git（最高优先级，强制）

- 绝对禁止在用户未于「当前这轮消息」显式提出提交的前提下，执行任何写入仓库历史的 Git 动作（`git commit`、`git commit --amend`、`git push`、`git rebase`、`git merge --no-ff` 等）。
- 「显式提出提交」指用户在当前这轮消息里明确表达提交/推送意图，例如：`提交git`、`提交代码`、`commit一下`、`帮我提交`、`推送`、`push`、`同步到远端`。
- 仅完成代码改动、任务收尾、或上一轮提交过，都不构成本轮提交授权；缺少当轮显式授权时，必须停在「已改动未提交」状态并提示用户。
- 任何情况下都不得以「我以为你想提交」「按惯例提交」「顺手提交」为由自动提交。
- 只读盘点命令（`git status`、`git diff`、`git log`）不受限制；写入历史的动作严格受限。
- 本条与全局技能 `git-collaboration-rules` 的「1.-2」一致，为项目级重申，确保重启会话 / 无全局上下文时本规则仍在项目内生效。
- 违反本条视为最高级别流程违规。

## Skill 命中强制规则

- 处理本仓库任务时，必须先命中并加载至少五个基础 skill。
- 最低要求：至少命中 `skill-hit-check-rules`、`parallel-task-dispatch-rules`、`reasoning-summary-structure-rules`、`project-memory-rules`、`project-style-rules`。
- 若本轮涉及创建、补齐或更新仓库级规则文件，默认额外启用 `project-agents-bootstrap` 进行自举补齐；该规则同样适用于其他项目仓库。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若命中 `parallel-task-dispatch-rules`，中间进度必须额外输出当前并行技能列表；若最终未并行，明确写 `并行技能:无`。
- 本仓库默认处于 subagent 完全授权模式：用户已明确允许 agent 在任务可切分、写集不冲突、风险可控且环境支持时自动启动 subagent / delegation / parallel agent work；该项目级 standing authorization 视为满足工具显式授权条件。
- 进入分析、侦察、需求、Bug、审查、测试、文档或编码等实质执行前，主 agent 必须自主判断是否存在可由 subagent 并行推进的独立问题、证据来源、文件集、模块边界或职责边界；不得只依赖固定 skill 映射表。
- 只要判定为可并行或条件并行，且当前环境支持 subagent / multi-agent / thread 能力、当前轮授权或项目级完全授权成立、无明确禁止或写集冲突，必须优先真实启动子 agent 并行执行；不能只输出线程分配或并行建议。
- 项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，即使没有固定并行 skill，也应优先尝试拆出只读 sidecar 子任务交给 subagent；主 agent 保留最终判断、归纳和冲突裁决职责。
- 单一根因、需求边界、接口契约、schema 或架构方向等需要统一裁决的主路径必须串行；其旁路证据收集、影响面盘点和资料检索可在边界清晰时条件并行。
- 若计划并行但真实子 agent 启动失败、环境不支持或被阻断，必须说明计划线程数、实际启动数、关闭/回收数和回退原因，不得把计划并行伪装成已并行。
- 用户使用“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现”等开工类指令时，不得视为无边界长文本执行授权；必须先确认已有执行计划，或当场给出本轮执行计划、任务完成条件、任务停止 / 结束条件和最大推进边界。缺少这些边界时，禁止直接进入实现 / 执行。
- 任何 agent 收到用户明确结束指令（如“结束”“停止”“到此为止”“不要继续”“不要下一步建议”“不要扩散”）时，必须立即停止自动继续和扩散性输出，只允许给出必要的最小收口结论。
- 若命中 `autonomous-execution-rules`，自动继续只允许用于“完成原始用户目标仍必需的动作”；不得把“进一步优化 / 可继续整理 / 总结里的下一步建议 / 未来迭代建议”自动升级成新的执行目标。
- 当原始用户目标已经完成或用户已给出明确结束指令，且不存在完成原始目标仍必需的动作时，必须停止连续执行并直接结束；不得输出“下一步状态”“下一步建议”“等待用户新指令”“无需继续动作”等任何可能触发循环 loop 的占位区块或扩散性文案，除非用户明确要求后续建议。
- 若当前运行环境存在 goal / plan / task 等显式状态收口机制，且原始用户目标已经完成或已满足该机制的阻断条件，必须在最终收口前真实执行对应收口动作；只写完成文案不算真正结束运行时状态。Codex goal 仅是其中一种特例。
- 若连 `skill-hit-check-rules` 或 `parallel-task-dispatch-rules` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 `skill-audit-rules` 进行只读审计。
- 自动审查白名单只保留 `implementation-review-rules` 与最终收口前的 `project-change-review-rules`。
- `project-change-review-rules` 同时支持两类触发：用户明确要求审查当前改动，或本轮存在代码改动且准备最终收口。
- `code-review-automation-rules` 仅用于当前分支提交级审查，不纳入默认自动审查链。
- 若本轮新增或修改任意 skill 资产（`SKILL.md`、`references`、`scripts`、`agents` 等），必须命中 `skill-compliance-gate-rules` 并在收口前给出 PASS / FAIL 结论；改动 `description` 或触发条件追加 `skill-evolution-rules`，涉及多 skill / 职责边界 / 规则收口风险追加 `skill-audit-rules`；改动 `description` 或新增 / 修改 `##` 级标题后，收口前必须重跑 skill 字典生成脚本刷新 `data.js` 与 `字典.md`；上述联动未走完不得收口。
- 上下文压缩续做规则：
  - 若当前会话刚发生”压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 `context-compression-rules`。
  - 压缩后继续执行前，必须重新读取当前项目根目录规则文件（`AGENTS.md` / `CLAUDE.md`），恢复仓库级硬规则、必命中 skill 和阻断条件。
  - 若压缩后未重新读取规则文件，禁止直接进入任何需求、Bug、编码、测试或交付主任务。
  - 若压缩后发现规则文件缺失、损坏或规则不完整，必须先触发 `project-agents-bootstrap` 补齐，再继续主任务。

## 会话动态重命名规则

- 当当前 Codex / Claude / agent 会话进入明确需求、Bug、实施、审查、测试、提交或其他可命名任务，且会话标题为空泛、过时、泛称或不匹配当前任务时，必须自动命中 `thread-title-rules`。
- `thread-title-rules` 负责生成 8-24 字中文简要标题，并按平台能力矩阵调用当前环境真实线程重命名工具更新当前会话标题；Codex 环境优先使用真实 `set_thread_title` 工具，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认视为无真实自动改名工具并显式跳过。
- 会话重命名不等待用户显式要求；但任务主题尚未稳定、标题已准确、工具不可用、无法可靠确定当前会话 ID 或用户明确禁止时必须跳过，并说明原因。
- `CLAUDE.md` 仅用于 Claude Code 仓库规则自举，不等同于 Claude Desktop 已具备自动会话改名能力。
- 标题采用“任务对象 + 动作 / 症状 / 阶段”的中文简要写法，避免只写“提交 git”“开始实施”“继续做”“修复 bug”“更新文档”等泛化动作标题。
- 禁止用正文伪造工具调用、raw directive 或猜测结果来宣称已经改名；所有标题变更必须来自真实工具返回。

## 注释任务强制流程

- 触发词：补充注释 / 注意中文编码 / 只补注释 / 注释完善 / 加注释。
- 第一步：先声明命中的注释类 skill。
- 第二步：读取对应 `SKILL.md` 后再改代码。
- 第三步：最终回复给执行证据：改动点、UTF-8、格式化/编译/测试结果。

## 上下文压缩续做规则

- 若当前会话刚发生”压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 `context-compression-rules`。
- 压缩后继续执行前，必须重新读取当前项目根目录规则文件（`AGENTS.md` / `CLAUDE.md`），恢复仓库级硬规则、必命中 skill 和阻断条件。
- 若压缩后未重新读取规则文件，禁止直接进入任何需求、Bug、编码、测试或交付主任务。
- 若压缩后发现规则文件缺失、损坏或规则不完整，必须先触发 `project-agents-bootstrap` 补齐，再继续主任务。

## 文件编码与写入规则

- 新增或修改注释默认使用中文。
- 所有代码、文档、配置、脚本、测试资产和生成类文本文件，新增或修改时默认使用 UTF-8 编码；禁止使用 GBK、ANSI、系统默认编码或编辑器默认编码落盘。
- 在 Windows、Linux、WSL、容器和远程服务器上写文件时都必须保持 UTF-8 口径一致；不得因为当前终端、区域设置或系统语言不同而切换编码。
- 通过命令行写文件时必须显式指定 UTF-8：PowerShell 使用 `Set-Content -Encoding UTF8`、`Add-Content -Encoding UTF8`、`Out-File -Encoding utf8`，Python / Node / Go 等脚本必须显式声明 UTF-8 读写参数或确保运行时强制 UTF-8。
- 禁止用未确认编码的 `>`、`>>`、默认 `Out-File`、默认 `Set-Content` 或其他依赖 shell 默认编码的方式写入中文、代码、Markdown、JSON、YAML、脚本和规则文件。
- 写入后必须回读关键文件并检查 `git diff`，确认中文未乱码、编码未漂移、换行未被意外批量转换。
- 仓库应提交 `.editorconfig` 与 `.gitattributes` 固定 `charset = utf-8`、基础换行和二进制文件规则；若发现文件被 GBK / ANSI 写入，必须先转回 UTF-8 再继续后续改动。

## 变更最小化

- 注释补充不改变业务逻辑。

## 本地连接调试测试红线（最高优先级，强制）

- 需求侦察、Bug 复现 / 定位 / 运行时调试、功能验证、回归测试、上线接口测试、浏览器联调、启动前后端服务或执行任何测试脚本时，所有数据库、缓存、消息队列、HTTP/RPC 上游、前端 / 后端服务连接都只能使用 `local` 本地环境。
- 本地环境只允许来自 `config_local*`、`.env.local`、`.env.development`、本机开发容器、`localhost` / `127.0.0.1` / 本机端口等本地开发配置；`test`、`prod`、`production`、`staging`、`pre`、`release` 等非 local 环境一律禁止连接。
- 即使用户提供了 test / prod 连接串、账号、接口地址或临时授权，也不得由 agent 直接连接或调用；必须记录为环境阻断，并要求改用 local 本地数据库和本地服务。
- 若 local 配置缺失、local 数据不足或本地服务未启动，只能初始化 / 启动 / 查询 local 环境；不得回退到 test / prod 数据库、缓存、消息队列、外部服务或线上接口补证据。
- 需要写入数据时仅允许写入 local 环境，并且必须有清理或回滚方案；Bug 侦察类只读链路仍保持只读，禁止自行增删改数据。

## 依赖与工具复用优先规则

- 编写代码前，必须先检索是否已有可复用的开源库、npm 包或项目内工具类，优先复用而非从零实现。
- 优先级：项目内已有工具类 / 公共方法 > 成熟开源库（npm / GitHub）> 自行实现。
- 禁止在已有成熟第三方库覆盖该能力时重复造轮子；引入新依赖前须确认许可证兼容、维护活跃且无已知安全问题。
- 若确实需要自行实现，必须在代码注释或 PR 说明中写明为何不使用现有库 / 工具类。
- 检索范围应覆盖项目 `utils`、`common`、`helpers` 等公共目录，以及 `package.json` / `go.mod` 等依赖声明文件。

## 输出格式规则

- AI 输出统一使用 markdown，不依赖 HTML 渲染：HTML 标签在 Claude Desktop、纯 CLI、Codex 等大量 agent 环境不渲染，会退化成原文噪声，并破坏对输出的机器解析。
- 视觉层级与区分靠 markdown 语义结构（`#` / `##` 标题、`---` 分隔线、表格、`>` 引用块、徽章 emoji），不靠绝对字号。
- 字号由各 agent 渲染端（客户端主题 / 字体 / 缩放）决定，内容层不强行控制；需要更大字号时调客户端，不在输出里塞 HTML。
- 普通说明、方案、流程、总结、审查报告、线程拆分和状态回报必须使用普通 Markdown 段落、列表、表格或引用块；不得用 ` ```text `、无语言代码围栏、缩进代码块或 HTML 包裹整段自然语言输出。
- 代码围栏只用于真实代码、命令、配置片段、日志片段、JSON/YAML 等需要等宽保真的内容；若只是为了展示可读结构，应改用 Markdown 列表或表格。

## Windows / WSL 执行规则

> 详细规则与命令模板见 `windows-wsl-execution-rules` 与 `windows-encoding-rules` skill。本节为写入规则文件的最小约束摘要。Windows 下普通仓库命令优先使用 Git Bash / bash；PowerShell 不作为普通仓库命令入口，只在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。代码位于 WSL 文件系统内且当前动作属于编译、运行、启动程序、测试、调试等执行类命令时，才优先进入 WSL；普通搜索、读写文件、规则检查、普通 git 盘点默认留在 Git Bash / bash。

**先看 agent 在哪运行：**

- **agent 在 WSL（推荐）**：直接 `cd /home/<user>/<project>` 执行执行类命令，普通命令也可直接在当前 shell 完成，无需任何包裹。
- **agent 在 Windows（如 Claude Desktop GUI）**：
  - 普通仓库命令优先使用 Git Bash / bash；PowerShell 只用于 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求的场景
  - 看代码、改代码、搜索、规则检查、普通 git：经 `\\wsl.localhost\<distro>\home\<user>\<project>` 或 Git Bash / bash 可访问的等价路径访问 WSL 文件
  - 编译、运行、启动程序、测试、调试，以及会真实启动运行时的依赖安装：`wsl.exe --cd /home/<user>/<project> <command>`

**为什么只有执行类动作在 WSL：** 只有 WSL 进程能正常联网，且运行产物面向 Linux；普通读写、搜索、规则检查不依赖 WSL 运行时，强行切换反而容易引入路径或权限问题。

**命令格式：** 执行类命令用 `wsl.exe --cd /home/<user>/<project> <command>`（默认发行版省略 `-d`；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`）。普通命令不要为了统一口径强制套这层。代码在 WSL 时不再使用 `/mnt/<drive>`；纯 Windows 项目或本轮不执行程序时，不要误触发本规则。

**用户可访问文件引用：** 回复用户时，凡引用项目内文件都按用户当前环境可打开的路径输出。项目在 WSL 且用户从 Windows 桌面访问时，Markdown 链接、普通文本路径、审查证据路径、截图说明和最终总结中的项目内文件路径都使用 `\\wsl.localhost\<distro>\home\<user>\<project>\...`；只有命令参数、WSL shell 上下文和日志原文保留 `/home/<user>/<project>`。

**编码约束：**

- 仓库提交 `.gitattributes` 与 `.editorconfig`，固定 UTF-8 和换行策略；任何读写文件操作都继续遵守“文件编码与写入规则”
- `.gitattributes` 默认 `* text=auto`，`*.sh`/`*.yaml` 显式 `eol=lf`
- 不对 `*.go`、`*.vue`、`*.md` 等全量强制 `eol=lf`
- Windows 下出现大量无关改动优先检查 `core.autocrlf`

## CodeGraph 强制准备规则

- 若当前服务器 / 电脑未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载并安装，不需要用户确认。
- 若在 Windows PowerShell 5.1 下执行安装，必须默认启用 `Invoke-WebRequest` / `Invoke-RestMethod` 的 `UseBasicParsing`，不得把人工点击确认当作标准流程。
- 安装完成后必须为当前项目执行 `codegraph init`，生成 `.codegraph/` 并建立索引。
- 若下载、安装或初始化失败，明确记录不可用并回退到本地搜索与文件读取。
- 架构层分析可配套 codebase-memory-mcp（`DeusData/codebase-memory-mcp`，按官方说明安装，非强制）作为 CodeGraph 的补充。

## 代码库探索规则

1. 日常理解代码、定位实现、追踪调用链、分析改动影响时，优先使用 CodeGraph。
2. 修改代码前，先用 CodeGraph 获取相关源码和影响范围。
3. 不要在 CodeGraph 已经返回足够上下文时重复全仓库 grep。
4. 项目架构分析、跨模块依赖、函数调用频率、ADR 记录等架构层任务，用 codebase-memory-mcp 作补充。
5. CodeGraph 作默认入口，codebase-memory-mcp 作高级图分析工具；两者结果与当前代码不一致时，以当前代码为准并重新同步索引。

## 插件检测安装规则

- 涉及 AI 编码插件（如 Ponytail）的安装、启用、配置时，联动 `plugin-installation-rules`。
- Ponytail 为默认必装插件：会话 / 项目准备时默认安装并启用（详见 `plugin-installation-rules`）。
- 安装命令与配置一律以插件官方仓库为准，不沿用第三方博客 / 公众号转述的旧命名、旧参数。
- 通用支持 Claude Code / Codex 等环境，按当前 AI 选对应安装方式；安装或启用失败时回退到常规流程。

```

## 边界

- 只负责仓库级规则落地，不替代具体业务开发。
- 不随意重写用户已有规则文件（`AGENTS.md` / `CLAUDE.md`），只做必要补充。
- 若用户明确给了规则文件（`AGENTS.md` / `CLAUDE.md`）模板，优先使用用户模板。
- 若根目录缺失规则文件（`AGENTS.md` / `CLAUDE.md`），本 skill 不允许降级为”仅提醒不处理”，必须完成补齐。
- 若规则文件（`AGENTS.md` / `CLAUDE.md`）已存在但其中受管章节落后于最新规则，本 skill 仍必须更新这些章节，不能只做一次性初始化。
- 若仓库内存在多个规则文件（`AGENTS.md` / `CLAUDE.md`），本 skill 不允许只同步根目录后结束；必须同步所有已存在规则文件的受管章节，除非用户明确要求排除某些子工程。
- 若首轮发现 `.gitattributes` 或 `.editorconfig` 缺失，也不允许降级为”先分析项目后补文件”；必须先补齐这两个文件，再继续主任务。
- 若 CodeGraph 下载、安装或初始化失败，不应阻塞规则文件（`AGENTS.md` / `CLAUDE.md`）自举流程；按当前环境继续执行即可。
- 若仓库位于 Windows 环境，默认应把“普通仓库命令优先 Git Bash / bash，PowerShell 仅用于 Windows 专项场景，执行类命令再进 WSL”的边界一并补入仓库规则，而不是只在单次会话里临时提醒。
- 若仓库位于 WSL 文件系统且用户从 Windows 桌面访问，默认应把“命令用 `/home/...`、面向用户的项目内文件引用用 `\\wsl.localhost\...`”的边界一并补入仓库规则，避免输出用户无法打开的项目文件路径。
```
````
