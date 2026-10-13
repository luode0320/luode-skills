---
name: skill-hit-check-rules
description: 【强制总控】每轮用户新消息（含新会话第一条）都必须先做命中检查并在首条中间进度输出。凡涉及 Git 协作动作（含显式关键词与隐式语义，如“提交git/帮我提交/commit一下/推送代码/看下状态”），必须联动命中 git-collaboration-rules。凡处理本仓库任务，最低还必须联动命中 `parallel-task-dispatch-rules`，并在非 Plan Mode 的实质任务轮按 `references/deferred-gate-registry.md` 用 `闸门预告` 字段登记本轮所有延迟触发 gate（含 `reasoning-summary-structure-rules`）；同时执行知识库知识流选择性默认判断，输出 `知识库:检索/沉淀/不适用/阻断`；当判断为 `检索` 或 `沉淀` 时必须同时命中 `knowledge-flow`。继续类消息命中恢复 Owner 后，必须按当前 `session_id` 从 PROJECT_CURRENT v5 registry（兼容读取 v4） 精确恢复对应 projection；无匹配时还要支持“先持久化并显示当前会话暂定恢复清单，再由只读子代理收集证据，最后补建 exact 或 fallback 正式悬浮任务列表”的执行前路由。非 Plan Mode 的明确实质任务在完成最低必要规则命中并取得 `confirmed` 后，必须先允许任务 Owner 最小读取 `PROJECT_CURRENT.md` 以安全定位当前会话 registry，再在其他领域侦察、项目内容读取、CodeGraph 查询、命令、委派或修改之前，为当前会话生成并持久化可读的初始步骤，随即调用宿主任务列表工具；Plan Mode 必须先以原生计划输出展示细化步骤，再开始计划侦察。首条中间进度最小必填包含 `命中检查`、`命中技能`，若本轮命中 `parallel-task-dispatch-rules` 还必须追加 `并行技能`；非 Plan Mode 的仓库实质任务还必须追加 `闸门预告`（按延迟触发 gate 注册表登记本轮将适用的延迟 gate）。
---

# Skill 命中检查规则（最小闭环版）

## -1.4 极简硬闸门（强制）

- 本 skill 是每轮用户新消息的唯一首入口，必须先完成命中检查，再执行任何领域动作。
- 首条中间进度固定包含：
  - `命中检查:<通过/阻断>; Git规则:<通过/不适用/阻断>`
  - `命中技能:<skill1,skill2,...>`
  - 仓库任务追加 `知识库:<检索/沉淀/不适用/阻断>`
  - 命中 `parallel-task-dispatch-rules` 时追加 `并行技能:<skill.../无>`
  - 非 Plan Mode 的仓库实质任务追加 `闸门预告:<checkpoint→gate;... / 无 / 不适用(Plan Mode)>`（按 `references/deferred-gate-registry.md` 登记本轮延迟 gate）
- 固定字段的 Markdown 形态以 `references/output-format.md` 为准；缺少必填字段即阻断领域执行。
- 全程中文自检（硬闸，不可跳过）：本轮全程，含**每一次**工具前导语 / 中间叙述发送前，先自检草稿是否为简体中文；发现成段非中文（英文 / 日文等）自然语言必须改回简体中文再发送，代码符号、命令、路径、原始字段名、报错原文等技术片段除外。思考 / 推理通道同口径尽力而为。最终总结阶段的中文自检以 `reasoning-summary-structure-rules` 为准，本条负责过程叙述的全程覆盖，二者互补不重复。
- 非 Plan Mode 的明确实质任务在完成最低必要规则命中并取得 `confirmed` 后，必须立即由 `task-plan-rehydration-rules` 为当前 `session_id` 持久化 `active` projection；允许该 Owner 为安全定位当前会话 registry 最小读取 `PROJECT_CURRENT.md`，除此之外必须早于领域侦察、其它项目文档/源码读取、CodeGraph 查询、命令执行、委派和修改。初始步骤可标为暂定，但必须直接根据当前请求写出具体任务对象、动作和可核验结果；禁止用通用 RECOVERY 清单代替任务说明。取得项目上下文后先建立正式 L1，再细化/替换为正式 L2。持久化成功后的下一动作只能是立即调用宿主任务列表工具（Codex 为 `update_plan`），不得插入其它领域动作。仅纯问答、用户尚未确认执行的澄清、或明确处于 Plan Mode 的计划形成不走此执行期入口。
- 继续恢复时，若当前请求、已确认项目目标或来源文档足以辨认正在恢复的具体任务，必须把该任务提炼为脱敏 `task_summary` 传给恢复 Owner；只有来源证据不足以安全确认任务时，才允许显示明确标注“尚未识别具体任务”的通用恢复步骤。
- 非 Plan Mode 的仓库实质任务轮，首条命中列表必须按 `references/deferred-gate-registry.md` + 当前任务类型，用 `闸门预告` 字段登记本轮将适用的延迟触发 gate（`reasoning-summary-structure-rules` 恒为成员），并把强制项列入 `命中技能`；`闸门预告` 是预测，中段按真实改动对账修正，收口按其逐项复核声明与执行是否一致，不得只在回合末端凭自觉临时补触发。
- 当前处于 Plan Mode 时，命中列表不得包含 `reasoning-summary-structure-rules`，`闸门预告` 置 `不适用(Plan Mode)`；该 Skill 明确判定 `NOT_APPLICABLE`，计划出口只交给 `implementation-planning-rules`。计划型请求必须先用原生计划出口展示可读的细化步骤，再读取项目源码、运行命令或派发子任务；当前宿主提供 `update_plan` 时可同步，但同步失败不得暂停计划形成。
- 仅当投影持久化失败、会话归属冲突/不确定或执行状态不明时按各自安全规则处理；`update_plan` 成功后才可声称 UI 已同步，单纯 UI 同步通道不可用（缺失或调用失败，磁盘投影已成功且归属明确）时进入 `UI_SYNC_BLOCKED` 降级继续：保留磁盘 projection + 继续领域执行，下一检查点优先重试 UI，不得声称 UI 已恢复。Goal、普通会话和 Plan Mode 默认展示细粒度任务步骤；Plan Mode 不持久化执行期 projection，默认使用原生计划流程，当前会话若提供 `update_plan` 也可同步显示；`inactive` projection 不创建活动悬浮任务列表，禁止跨 session 读取、刷新或覆盖。
- 十分钟只作未显示步骤的异常补救闸门：主动执行时间扣除暂停后严格超过 600 秒，且当前会话尚未确认原生步骤清单同步成功时，在首个可执行检查点先执行只读 `probe-timeout`；缺少活动 projection 则补建，已有 projection 但 UI 未同步则取回当前唯一 payload 并重试 `update_plan`，不创建 Goal、不覆盖投影；UI 失败仍继续领域任务。
- 当前会话首次投影或正式计划写入若只因 `PROJECT_CURRENT.md` 全文超过 51,200 字节被拒绝，先命中 `project-memory-rules`，在共享锁内压缩普通正文的旧已完成历史条目，再由投影 Owner 重读并重试。最多两轮；仍超限时保持原文件不变、如实标记投影未持久化并继续领域任务，容量问题不得阻断执行。registry、隔离项、最近会话快照和活动状态不得作为释放空间的内容。

## -1.5 违规处理（强制）

- 若发生“先执行命令、后做命中检查”，立即停止后续命令，补齐固定字段后重走命中流程。
- 不得用额外恢复文案替代固定字段，也不得把迟到的命中声明伪装成首条合规。

## -1. 触发确认（强制）

- 每轮都命中本 skill；自动触发不依赖用户点名，也不因任务简单而跳过。
- 仓库任务联动 `parallel-task-dispatch-rules` 并执行知识库选择性判断；非 Plan Mode 的实质任务轮按 `references/deferred-gate-registry.md` 用 `闸门预告` 登记本轮延迟触发 gate（`reasoning-summary-structure-rules` 恒为成员）。
- 当前轮存在 Git 意图时联动 `git-collaboration-rules`；只识别当前轮，不继承历史授权。
- 修改 Skill 资产时联动 `skill-execution-compliance-gate-rules`，并按职责边界追加 `skill-absorption-rules`、`skill-audit-rules`。
- 联动条件、用户习惯、负向边界和漏触发防护统一见 `references/hit-checklist.md`；本入口不复制各 Owner 的执行细则。

## -1.0 新会话首轮保障（强制）

- 新会话第一条与普通轮次同等处理，必须先输出命中检查。
- 新会话的规则文件和项目上下文准备交给对应自举或恢复 Skill；本 skill 只负责确认已正确联动，不代替其执行。
- 新会话、上下文恢复或用户消息包含任意“继续”语义时，首条命中列表必须先把 `task-plan-rehydration-rules` 列为候选 Owner；“继续”语义包括但不限于“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义自然语言表达。当前回合处于 Plan Mode 时，Owner 不读写执行期 `PROJECT_CURRENT.md` registry；默认由 `implementation-planning-rules` 原生计划流程展示细化步骤，若当前会话提供 `update_plan` 可同步显示。执行期恢复先严格校验整个 registry，再按当前宿主提供的 `session_id` 精确定位；托管标记、JSON、顶层契约或 v5 活跃项损坏时立即保留原文并退出全部 UI 恢复；v4 单条坏项按 Owner 规则隔离，只有身份唯一且不与隔离项冲突时才继续恢复，身份未知的隔离项阻止所有会话恢复。仅 registry 缺失或完整校验通过但当前会话无匹配时，才根据当前请求创建并同步仅绑定当前会话的任务专属暂定步骤，然后派只读子代理收集来源证据并决定 `exact/fallback`。任何阶段都不得读取、复制或刷新同项目其它会话的投影。精确匹配 legacy ID 的历史记录仍有效，不自动修复身份。与 UI 恢复无关且已明确授权的领域工作按各自执行规则处理。

## -1.1 Git 意图识别（强制）

- Git 关键词、中文动作词、口语表达和语义等价表达的识别清单见 `references/hit-checklist.md`。
- 一旦当前轮命中 Git 意图，必须联动 `git-collaboration-rules`；具体盘点、提交、推送、证据和回退步骤只由该 Skill 定义。

## -1.1.1 Git 仅限当前轮次（新增，强制）

- Git 意图和写历史授权只基于当前轮用户消息。
- 当前轮未出现 Git 意图时，不得沿用先前轮次的提交、推送、合并或同步授权。

## -1.1.2 阻断授权意图识别（新增，强制）

- 用户当前轮回复“同意授权”时，识别为对最近一条、唯一有效、仍未解除的 `BLK-*` 记录列明恢复动作的授权意图，必须联动 `task-plan-rehydration-rules` 恢复流程与 `reasoning-summary-structure-rules` 阻断渲染。
- 用户当前轮回复“暂不授权”时，识别为保持阻断意图，不执行任何恢复动作，继续输出阻断收口。
- 存在多条有效 `BLK-*` 记录、记录已解除/过期或无法唯一确定时，不自动采纳授权，必须提示用户确认。
- 授权只作用于该条 `BLK-*` 记录，不构成跨任务、跨会话或未来任意写入的通用许可。

## -1.2 Git 判定优先级（强制）

- 同一消息同时命中 Git 与其他领域时，先确认 Git 联动，再进入其他领域判断。
- 本优先级只保证不漏触发，不授权越过 `git-collaboration-rules` 的安全和提交边界。

## -1.3 新会话首轮联动（强制）

- 新会话按当前平台联动规则文件与项目上下文自举；缺失或损坏时由对应 Owner 修复。
- 自举未完成时禁止进入主任务；详细文件范围、幂等和用户内容保护不在本 skill 重复定义。

## 0. 首条消息格式（强制）

- 使用 `templates/hit-check-template.md`，并遵守 `references/output-format.md`。
- 标题、字段、Git、知识库与并行行必须使用普通 Markdown，不得放进代码围栏、缩进代码块或 HTML。

## 1. 最小流程

1. 基于当前轮请求匹配所有可用 Skill 的 `description` 与条件路由。
2. 输出固定首条字段。
3. 执行 Git、并行、知识库、Skill 资产及新会话自举的联动摘要判断。
4. 将执行权交给对应 Owner Skill；本入口不复制领域流程。

## 1.1 首条闸门（强制阻断）

- 未完成固定首条字段时，不得执行对应领域命令。
- Git 场景的盘点例外与后续许可边界以 `git-collaboration-rules` 为准。

## 1.2 执行期失败联动（强制）

- 非预期失败或“退出码成功但产物不达标”时，联动 `execution-failure-learning-rules`，不得无变化重试。
- 失败分类、active 案例、恢复和沉淀全部由该 Skill 定义，本入口只负责不漏触发。

## 2. Git 联动闸门（强制）

- 本 skill 只校验当前轮是否正确联动 `git-collaboration-rules`。
- Git 操作、脚本、证据、提交标题和回退检查以 `git-collaboration-rules` 为唯一事实 Owner。

## 2.3 Skill 资产改动联动闸门（强制）

- 本 skill 只输出联动摘要：是否命中执行合规、演进和多 Skill 审计。
- PASS / FAIL、保护语义、迁移证据和字典刷新要求以 `skill-execution-compliance-gate-rules`、`skill-absorption-rules`、`skill-audit-rules` 为准。

## 3. 通过标准

- 每轮先完成固定命中字段，且真实执行所有已命中 Skill 的必要步骤。
- Git、并行、知识库、Skill 资产和失败恢复均已正确联动，没有在本入口复制 Owner 细则。
- 最终回复保留 `命中检查:通过`；仓库任务保留知识库状态；Git 场景保留 `Git规则:通过`。

## 4. 执行文件

- `templates/hit-check-template.md`
- `references/output-format.md`
- `references/hit-checklist.md`
