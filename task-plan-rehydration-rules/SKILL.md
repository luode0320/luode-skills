---
name: task-plan-rehydration-rules
description: 当 Goal、普通会话或 Plan Mode 需要默认展示细粒度且用户可读的任务步骤，正式实施计划需要投影到宿主任务悬浮窗（跨宿主：Codex Desktop / WorkBuddy Desktop / 无任务 UI 宿主），明确实质任务需要在领域侦察、项目内容读取、CodeGraph 查询、命令、委派或修改之前创建并同步暂定启动投影，取得上下文并先写正式 L1 计划后需要细化/替换为正式投影，或任务步骤状态发生迁移时自动触发；还适用于 Goal 的 create/get/update 生命周期成功返回、Desktop 或宿主关闭后用户在同一任务首次发送任意“继续”或恢复意图、上下文压缩恢复时检测到 PROJECT_CURRENT 存在活动任务投影，或历史投影缺失但需要根据当前会话与项目文档补建悬浮任务列表。任意继续语义包括“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义表达，不要求出现“任务”或“计划”。作为任务投影唯一 Owner，负责 PROJECT_CURRENT 多会话 registry 托管区的 schema、指纹、原子写入、失活、细粒度 Goal 安全步骤、旧 Goal 清单兼容迁移、持久化后立即返回宿主任务列表 payload、十分钟未显示步骤异常补救、失败降级、校验、synthesize 补建和 update_plan payload；实际 Goal 工具与 UI 工具必须由主 Agent 调用，且进行中步骤先核验中断点。不要把 Goal 或 UI 重建当作执行授权或 L5 checkpoint resume，也不要重放未知幂等性的写操作。
---

# 任务计划断点恢复规则

## 目标

把 Goal、普通会话和 Plan Mode 的细粒度任务步骤默认展示出来；执行期将适用步骤投影到 `PROJECT_CURRENT.md`，并在宿主关闭（Codex Desktop / WorkBuddy Desktop / 无任务 UI 宿主）、会话中断或上下文恢复后的首次继续回合中重建悬浮任务列表。正式实施文档仍是真实计划源，本 Skill 只拥有运行时任务投影。本 Skill 的 UI 同步通道按宿主分级适配，不再以 Codex 专属协议作为所有宿主的硬闸门。

## 与持久层任务计划文档的关系（强制）

本 Skill 拥有的 registry 投影是紧凑运行时视图（任务 ID、悬浮窗文案、三态；不设任意小的步骤数量上限），不是全保真事实源；唯一物理上限是整个 `PROJECT_CURRENT.md` 的 UTF-8 大小 51,200 字节。全保真事实源是按执行顺序命名、落盘在项目 `doc/3-实施/` 的独立任务计划文档（契约唯一细则见 `../autonomous-execution-rules/references/state-persistence-and-task-granularity.md`，落点与命名见 `../artifact-storage-rules/references/path-map.yaml` 的 `implementation_task_plan_doc`）：

- 固定写入顺序：先落盘任务计划文档（L1 事实源），再原子更新 registry 投影（L2）；任何投影写入不得替代或推迟 L1 落盘。
- 恢复时以任务计划文档的状态字段和“下一动作”指针确认中断点；registry 只用于重建悬浮任务列表，不用于判定任务真实状态。
- registry 与任务计划文档不一致时，以任务计划文档为准，并在下一检查点把投影修正为与事实源一致。
- 所有模式默认展示足够细、可逐项检查的步骤：按最小独立可执行、可验证工作项拆分，覆盖适用的侦察、决策、实施、验证、回归和交付；不把列表压成“开始、执行、完成”，不为凑数量制造无意义微步骤。任务多时保留完整清单并由宿主滚动查看。
- Goal 与普通执行模式默认使用细粒度主清单；有正式计划时以其步骤为准。Plan Mode 使用原生计划流程展示同等颗粒度的计划步骤；若当前宿主同时提供 `update_plan`，可同步展示状态，但 Plan Mode 不写执行期 registry 投影。
- 投影或 UI 工具缺失、调用失败、或无法确认界面已显示时，只记录显示状态并继续领域任务；不得将显示故障设为 Goal 或普通任务的暂停条件。持久化、会话归属或执行状态的既有安全闸门仍按各自规则处理。
- 压缩后的会话层不可信；registry 恰好落盘了三态，因此跨会话再水化安全，但决策、偏差、证据只存在于任务计划文档，恢复细节必须回读 L1。

## 自动触发信号

- 正式实施周期首次进入执行，需要把最小任务同步到悬浮任务列表。
- 默认执行模式取得 `confirmed` 后，首次领域动作前必须先用 `ensure-start` 持久化当前会话投影；成功后立即使用返回 payload 调用 `update_plan`。
- 任一任务从 `pending` 迁移为 `in_progress`，或从 `in_progress` 迁移为 `completed`。
- 当前周期全部完成，需要把投影设为 `inactive`。
- Desktop 或宿主关闭后，用户在同一任务首次发送任意“继续”或恢复意图；至少包括“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义表达。
- 上下文压缩恢复、新会话恢复或项目状态重载时，`PROJECT_CURRENT.md` 存在有效活动投影。
- 历史投影缺失，但当前会话和项目文档需要补建正式悬浮任务列表。
- 投影持久化失败、会话归属冲突或执行状态不明时按各自边界处理：禁止破坏原文件、错投或重放未知写操作；但投影写入仅因全文超过 51,200 字节被拒绝时，不得暂停领域任务，必须先转给 `project-memory-rules` 压缩普通历史正文并重试。两轮安全压缩后仍因容量无法持久化时保留原文件、明确标记未落盘并继续领域任务；仅 UI 同步通道不可用（`update_plan` 缺失或调用失败，但磁盘投影已成功且会话归属明确）时按 `UI_SYNC_BLOCKED` 降级继续。
- 当前实施周期把最小任务委派给子智能体（`spawn_agent` / 多智能体并行 / delegation）执行，主智能体需要维持并持续更新面向用户的主计划投影。
- `create_goal` 成功后、默认执行回合检测到活动 Goal、`update_goal` 成功进入 `blocked` 或 `complete` 时，需要生成、恢复或迁移 Goal 专属投影。
- 默认执行回合不允许因任务简单而跳过首次投影；若扣除 Plan Mode、等待用户、`blocked` 和 `manual_handoff` 暂停后的主动执行时间严格超过 600 秒，且当前会话原生步骤清单尚未确认同步成功（没有活动 projection，或已有 projection 但 UI 同步失败/用户明确反馈未显示），必须在首个可执行检查点进入十分钟异常探测：无活动 projection 时按 Goal 优先路径补建；已有唯一活动 projection 时取回原 payload 并重试 UI，同一会话多条活动 projection 时按下方消歧规则处理。UI 显示失败不得暂停领域任务。

### 原生清单可见性的验收规则

- 用户明确把“当前会话的 Codex 原生步骤悬浮清单实际可见”列为完成条件时，必须把它作为独立验收项；该显示要求不暂停领域任务。
- `update_plan` 缺失、调用失败或无法确认原生清单已显示时，按本节前述 `UI_SYNC_BLOCKED` 规则处理。Desktop 重启后用户明确要求继续时，重新检查当前回合工具注册和当前会话投影；若 `update_plan` 已注册且投影校验通过，立即同步该会话清单。若此前 Goal 仅因 UI 同步失败被标为 `blocked`，不得把该显示状态当成领域任务阻断；按用户本轮继续意图恢复工作，不调用不支持的 Goal 状态恢复操作。
- Codex Desktop 未注册 `update_plan` 时，先检查用户级 `~/.codex/config.toml` 与当前项目 `.codex/config.toml` 中的 `[tools.update_plan].enabled`。官方 Codex CLI 0.152.0 起该工具默认关闭；若配置未显式启用，且用户目标要求恢复原生步骤清单，可在授权范围内设置为 `true`。配置文件更新本身不证明活动会话已重新注册该工具，仍须核对当前工具注册与原生 UI 实际显示；同步未恢复期间继续领域任务。
- 磁盘 projection、Markdown 清单、`open_in_codex` 文件面板或浏览器页面不能替代原生清单的可见性验收；没有当前线程原生 UI 的实际显示证据时，不得声称显示验收通过或报告该目标已完成。
- 本次规则调整依据与边界见[来源记录](references/source-notes.md)；同域整理与去重结果见[规则调整记录](workbuddy-absorption-map.md)；完整复盘见[重启后步骤悬浮清单恢复案例](references/case-task-plan-rehydration-rules-absorption.md)。

## 跨宿主适配（Codex / WorkBuddy / 无任务 UI 宿主）

UI 同步通道按宿主分级适配，磁盘投影（`PROJECT_CURRENT.md` registry）在所有宿主上语义一致；同一轮只走一条宿主路径，互斥不双写（参考 `thread-title-rules/references/workbuddy-host-contract.md` 的"同轮只走一条宿主路径"原则）：

| 宿主 | UI 通道 | 说明 |
| --- | --- | --- |
| Codex Desktop | `update_plan`（Codex 专属适配层） | 沿用 `CODEX_THREAD_ID + update_plan` 路径；按契约返回 payload 后同步悬浮任务列表 |
| WorkBuddy Desktop | 宿主任务列表工具（任务条目协议） | 任务列表经宿主任务列表工具更新；与 Codex `update_plan` 互斥，绝不双写 |
| 无任务 UI 宿主 | 无 UI 通道 | 只保留磁盘投影，不伪造 UI 同步成功 |

- Codex 专属路径 `CODEX_THREAD_ID + update_plan` 保留为适配层之一，不再是所有宿主的硬闸门。
- 无论走哪条通道，都保持"先持久化、后同步 UI"的固定顺序；UI 同步失败不改变磁盘投影的有效性。
- WorkBuddy 宿主只走宿主任务列表工具；Codex 宿主只走 `update_plan`；两者互斥，禁止同轮双写。无任务 UI 宿主不做任何 UI 声称。

## 唯一 Owner 边界

- 本 Skill 唯一负责：托管区标记、v5 registry JSON schema、会话投影归属、计划指纹、敏感字段拒绝、51,200 字节闸门、原子写入、失活和 payload 生成。
- `project-memory-rules` 只负责更新 `PROJECT_CURRENT.md` 的普通当前状态，并原样保留 registry 托管区。
- `project-rule-file-bootstrap-rules` 只在新建模板中提供空 registry，不管理活动投影。
- `parallel-task-dispatch-rules` 只负责判断是否启动只读子代理收集补建证据，不接管最终归属裁决。
- `autonomous-execution-rules` 只决定是否允许继续执行；投影恢复不恢复执行许可。
- `context-compression-rules` 只在压缩恢复路径调用本 Skill；Desktop 重开但未压缩时由本 Skill 自身触发。
- `agent-runtime-recovery-rules` 只声明 UI 重建不是 L5 任务续接，不接管投影。

## 保存和状态迁移流程

1. 从正式计划提取所有适用的最小可执行、可验证任务，只保留任务 ID、用户可见步骤文案和三态状态；不设置小数量上限，不删减来缩短滚动列表。Goal 清单、普通会话投影和 Plan Mode 原生计划中的每条步骤，都必须让不了解内部编号的用户单独阅读也能说出“要做什么、处理什么对象、要得到或确认什么结果”；优先使用具体中文动词 + 当前任务对象 + 可辨认的结果/检查点。`TASK-001`、`GOAL-02` 等编号只作辅助索引，不能代替任务含义；必须保留编号时，将清楚的动作说明放在编号之后。缩写或内部术语首次出现时要有上下文解释，避免把多个无法理解的编号串成句子。唯一硬限制为整个 `PROJECT_CURRENT.md` 不超过 51,200 UTF-8 字节；超限时不得截断或改成三步占位，按容量恢复规则处理。
2. 非 Plan Mode 的实质任务在取得 `confirmed` 后，先按当前模式校验是否已有同一 `session_id` 的有效投影。为定位或安全更新 registry，只允许最小读取 `PROJECT_CURRENT.md`；不得读取其它项目文档/源码或执行侦察。只有当该投影能由当前回合证据确认属于同一已确认任务来源对象时，才可复用并立即同步；同一会话内的新任务、来源不匹配、多个候选或归属不确定都不得复用旧投影，也不得覆盖其它任务/会话记录。新任务必须根据当前用户请求直接构造任务专属暂定投影，明确写出当前任务对象、要完成的动作和可核验结果，并在 `ensure-start` 输入中明确唯一 `plan_key`；不得把固定 `RECOVERY-*` 流程清单当作新任务说明。`ensure-start` 已支持直接接收投影对象；新任务不得为方便而走会丢失任务对象的通用恢复合成路径。脚本返回后只同步该当前任务的 payload，不得按更新时间或数组顺序选计划，不得失活其它任务的 registry 记录，也不得声称一个原生清单同时展示了多个计划。若脚本因歧义拒绝写入，按投影安全规则处理，不猜测或覆盖。暂定启动投影不是正式 L2 计划，不替代正式 L1；它必须早于领域侦察、其他项目文档/源码读取、CodeGraph 查询、命令执行、委派和修改。持久化成功后下一动作立即调用当前宿主任务列表工具。取得上下文后，先落正式 L1 计划，再将暂定投影细化/替换为正式 L2 投影；明确选中并失活暂定投影，避免同一会话留下多个活动列表。不得以“计划还不够精确”为由延后初始显示。
3. 确认命令成功后，必须把同一结果中的 `payload` 作为下一动作调用当前宿主任务列表工具（Codex 为 `update_plan`）；中间不得执行其它领域写操作。宿主工具缺失或同步失败时，如实记录 UI 未同步并继续原任务；不得因显示故障暂停执行，也不得声称悬浮列表已显示。
4. UI 同步成功后才能说明悬浮任务列表已刷新；同步失败时按本节前述 `UI_SYNC_BLOCKED` 规则处理。
5. 当前会话的当前周期全部完成后调用 `deactivate`；成功落盘后可使用一次性完成收口 payload 刷新 UI，随后该会话的失活投影不得再次生成活动 payload，也不得影响其它会话投影。

### 任务说明与恢复兜底

- 启动清单必须从当前用户请求提炼具体任务对象与预期结果；不得仅用“核对目标”“确认来源”“更新进度”等通用恢复动作代表当前任务。
- 恢复合成时，只要能从当前用户请求、已确认的项目目标或来源文档中识别任务，就必须提供经过脱敏的一行 `task_summary`（最多 96 字符）；不得因为字段可选而省略已知任务。来源必须是可确认的当前任务目标；不得直接复制原始 prompt、Goal 原文、凭据或业务数据。`synthesize` 进入 fallback 时，应把该摘要带入每条恢复步骤，使用户从任一可见步骤都能辨认正在恢复什么任务。
- 若没有可信、可安全展示的任务摘要，fallback 必须明确写明“尚未识别具体任务”，并把清单标为核验会话目标与来源的临时步骤；不得把通用恢复流程伪装成当前任务的具体说明。
- 通用恢复步骤只能在 exact 来源无法安全确认时作为过程框架；新任务开始时必须使用调用方按当前请求构造的具体投影。

固定顺序是“先持久化，再调用工具”。不得先刷新 UI 再补写磁盘状态。

## 未显示步骤任务的 10 分钟异常修复

1. 只在默认执行回合取得 `confirmed` 执行许可并进入第一个真实执行动作时开始计时；需求澄清、Plan Mode 计划编写和尚未取得执行许可的阶段不开始计时。
2. Agent 只在当前执行上下文维护开始时间和累计暂停秒数。等待用户、真实 `blocked` 与 `manual_handoff` 期间暂停累计；这些计时事实不写入 projection、步骤文案、`PROJECT_CURRENT.md` 普通正文或其它长期状态。
3. 每次工具返回后、阶段进度更新前和准备结束当前回合前检查一次。任务已完成、当前处于 Plan Mode、执行许可不是 `confirmed` 或计时上下文丢失时，不调用超时探测、不创建 Goal、不刷新 UI；计时丢失后从下一次真实执行动作重新计时，禁止根据墙钟或历史消息猜测。首次观察到主动执行时间已严格超过 600 秒且当前会话的原生步骤清单尚未确认同步成功时，必须把补救作为该检查点的首项立即执行，不得等到下一个阶段或回合结束。
4. 主动执行时间 `observed_at - started_at - paused_seconds` 严格大于 600 秒才有资格升级；恰好 600 秒和不足 600 秒均不升级。时间必须是 UTC ISO-8601，暂停秒数必须非负且不得超过总墙钟时长。
5. 到期检查点先调用带当前 `session_id` 的只读 `probe-timeout`。`not_due` 不做任何动作；`goal_check_required` 才进入宿主 Goal 编排；`blocked_goal_preserved` 保持阻断观察状态，不恢复执行。`already_active` 只证明磁盘有活动投影，不等于 UI 已显示：若当前同步状态为 `UI_SYNC_BLOCKED` 或用户明确反馈未显示，立即调用 `ensure-timeout` 取回同一会话唯一活动投影的现有 payload，并由主 Agent 重试 `update_plan`；这条重同步路径不得创建 Goal 或改写/替换现有任务。多个活动计划、会话归属不明、投影损坏或读写错误时禁止猜测和错投。`ensure-timeout` 仅在当前会话恰有一条活动 projection 时返回其 payload；若当前会话有多条活动 projection 且本回合已凭正式计划或首次同步返回值确认目标身份，可用只读 `payload --project-current PROJECT_CURRENT.md --session-id <session-id> --plan-key <plan-key>`（或 `--projection-id <projection-id>`）读取并同步该条；身份未确认或选择结果不唯一时不得刷新 UI，继续领域任务并说明未能安全判定要显示哪条。
6. `goal_check_required` 后只允许当前主会话主 Agent 先调用一次 `get_goal`。子 Agent 不得调用 `get_goal`、`create_goal`、`update_goal` 或主悬浮窗 `update_plan`。
7. `get_goal` 返回的活动 Goal 与当前已确认任务来源和目标明确匹配时复用，不调用 `create_goal`；没有活动 Goal 时，主 Agent 使用脱敏任务摘要调用一次 `create_goal`；活动 Goal 不匹配或无法可靠确认匹配时，不覆盖、不创建第二个 Goal，直接进入普通投影降级。
8. `create_goal` 结果不明确时，只允许再调用一次 `get_goal` 确认，禁止无变化重试 `create_goal`。确认存在匹配活动 Goal 后，执行带当前 `session_id` 的 `goal --event create` 原子同步细化安全步骤；脚本成功后才使用 payload 调用 `update_plan`。
9. Goal 工具不可用、创建失败、复核仍不明确、活动 Goal 不匹配，或 Goal 已成功但安全投影写入失败时，调用原 `ensure-timeout` 生成当前会话 `exact/fallback` 普通投影。Goal 已成功后不得再次创建；`ensure-timeout` 只作为失败降级入口，不再是到期后的首选入口。
10. Goal 投影成功但 UI 同步通道不可用时按本节前述 `UI_SYNC_BLOCKED` 规则处理；后续检查点只恢复 UI，不重新创建 Goal。只要仍未确认 UI 同步成功，超过 600 秒后的每个可执行检查点优先重试当前会话清单同步。Goal 完成和阻断继续遵守既有真实完成条件与连续三次相同阻断门槛。

**Goal 目标摘要契约**

- 来源优先级固定为：已确认实施计划的最终方案摘要 -> 当前已确认用户目标 -> 固定兜底文案。
- 摘要必须是单行中文，最多 80 个 Unicode 字符；禁止包含密钥、token、密码、连接串、完整路径、session ID、原始 prompt、原始日志或大段用户输入。
- 无法可靠脱敏时固定使用“完成当前已确认的长任务并完成验证收口”。摘要只传给 `create_goal`，不得写入 `PROJECT_CURRENT.md`、测试 fixture、工程文档、项目记忆或知识库。
- Goal 匹配只在宿主返回的活动状态和目标语义足以证明与当前确认来源一致时成立；不得依据标题、时间、路径、会话 ID 或相似关键词猜测。

本规则不是后台定时器：Agent 不能在工具调用仍运行或没有新回合时于第 601 秒自行唤醒；但只要长调用返回或出现其它可执行检查点，若主动执行时间已超过 600 秒且步骤尚未确认显示，就必须立即执行上述补建或 UI 重同步，不得再等下一次阶段更新或回合结束。

## Goal 生命周期投影流程

1. `create_goal` 成功后，只在默认执行回合执行带当前 `session_id` 的 `goal --event create`。若该会话已有活动正式投影，脚本返回 `preserved_formal`，不得覆盖正式最小任务；若存在多条活动正式投影，返回空 projection/payload，不得按注册表顺序选择；否则原子写入不含 Goal 原文的细化安全步骤，且不得影响其它计划或会话投影。
2. Desktop 或会话重开后，先通过 `get_goal` 确认仍有活动 Goal；随后执行带同一 `session_id` 的 `goal --event restore`。活动 Goal 安全投影返回可恢复 payload；此前已保留的正式计划返回 `preserved_formal` 且不重写、不刷新，仍由其自身的正式计划恢复路径负责。阻断、失活、来源不匹配、损坏或 Plan Mode 一律明确退出。
3. `update_goal` 成功进入 `blocked` 时，执行 `goal --event blocked`：若当前是 Goal 安全投影，先持久化“无进行中步骤”的观察投影，再使用返回 payload 调用 `update_plan`；若 `create` 已返回 `preserved_formal`，则返回同名无副作用结果，保持正式计划独立且不得调用 `update_plan`。此 UI 仅观察进度，绝不恢复执行授权。
4. `update_goal` 成功进入 `complete` 时，执行 `goal --event complete`：Goal 安全投影须先生成一次性全完成收口 payload，再持久化全部默认步骤为完成并失活；失活后不得重放，`preserved_formal` 同样返回无副作用结果，不得失活真实正式计划。
5. Goal 运行中出现正式实施最小任务时，仍用带当前 `session_id` 的 `write` 写入正式投影；仅移除该会话的 Goal 默认步骤并写入正式计划，其它正式计划及其它会话投影保持不变。投影不得保存 Goal 原文、Goal ID、线程 ID、原始用户输入、prompt、response、业务数据或凭据。
6. 每个脚本事件成功后才读取返回 payload 并由当前主会话同步 UI；同步失败时按本节前述 `UI_SYNC_BLOCKED` 规则处理。Plan Mode 不调用 Goal CLI；若当前会话提供 `update_plan`，可同步细化计划步骤。


**主智能体投影责任（多智能体委派场景）**

- 只有当前主会话的主智能体调用 `update_plan` 才会驱动 Codex Desktop 主悬浮窗；子智能体在自身作用域内调用 `update_plan` 不会顶到主悬浮窗。
- 主智能体把最小任务委派给子智能体（`spawn_agent` / 并行 / delegation）时，必须在主会话保留并持续更新一份映射整体进度的主计划；每当子智能体返回阶段结果，主智能体要把对应步骤迁移为 `completed` 并把下一步置 `in_progress`，避免主智能体长时间只 `wait_agent` 导致主悬浮窗“空窗”。
- 默认使用步骤清单覆盖 Goal、普通会话和 Plan Mode。Goal/普通执行模式在持久化当前计划后调用可用的原生任务列表工具；Plan Mode 通过原生计划输出展示同等细粒度步骤，并在当前工具可用时同步 `update_plan`。Plan Mode 不写入执行期 registry，不能因 UI 同步故障暂停计划形成或任务。
- fork 会话打开时，父会话的历史 `update_plan` 只是静态回放上下文，不会自动重建 live 主悬浮窗；需要悬浮窗时由当前主会话主智能体依据 `PROJECT_CURRENT` 重新调用 `update_plan`。

## 首次继续回合恢复流程

当前回合处于 Plan Mode 时，本 Skill 只负责投影与 UI 适配路由：不读取、写入或恢复执行期 registry；默认由 `implementation-planning-rules` 通过原生计划流程展示细化步骤，若 `update_plan` 在当前会话可用则可同步显示。UI 不可用不暂停计划形成。Plan Mode 结束并开始执行后，才进入以下执行期 registry 恢复流程。

1. 在任何领域写操作前读取 `PROJECT_CURRENT.md`。
2. 若 registry 托管区存在，先对完整托管区及全部 projection 执行严格校验，再使用当前 `session_id` 定位唯一 projection，并校验来源文档、计划指纹、状态约束和文件大小；有效 `active` projection 直接使用 `payload` 重建。任一条目、标记、JSON 结构或身份校验失败时，立即保留整个 `PROJECT_CURRENT.md` 原文并退出 registry UI 恢复；不得继续 `ensure-start`、`synthesize`、委派来源侦察或写入 fallback。完整校验通过但当前会话无匹配时，才进入下一步。无匹配、多匹配、来源不一致或归属不确定时不得读取其它会话 projection。
3. 仅当 registry 托管区缺失，或完整校验通过且当前 `session_id` 无匹配 projection 时，才可先仅根据当前用户请求构造任务专属、脱敏的暂定步骤；若当前请求也不足以辨认任务，则明确写“尚未识别具体任务”。将该临时清单绑定当前 `session_id`，以唯一临时 `plan_key` 通过 `ensure-start` 持久化，并立即同步当前会话 UI；不得借用同项目其它会话的投影、来源文档或步骤作为本会话投影。完成这一步后，主代理才可派只读子代理收集候选来源文档、完成步骤提示、当前步骤提示和冲突信息。子代理不得决定最终归属、不得写回文件、不得直接调用 `update_plan`。
4. 主代理把当前会话摘要、`PROJECT_CURRENT` 普通正文、子代理证据和候选来源文档传给 `synthesize`，并绑定当前 `session_id`。唯一来源且存在明确状态提示时生成 `exact` 正式补建；否则生成细化 `fallback` 安全恢复列表。正式来源必须先由主代理核验，不能因为同一项目中另一个会话引用了某份计划就认定当前会话属于该计划。
5. 正式计划补建必须先写入 L1 事实源，再原子写入 L2 投影和 payload。若已有暂定恢复投影，正式 projection 通过后按明确的 `plan_key` 或 `projection_id` 失活暂定项，再用正式 payload 同步 UI。`inactive`、过期或来源不匹配时不得恢复未知正式步骤；仅在完整 registry 仍通过校验且当前会话身份明确时，才可保留并继续显示已绑定本会话的暂定清单。registry 损坏时不得创建、更新或显示任何恢复清单，不得错投其它会话。
6. 真实调用 `update_plan` 后固定说明：历史投影命中时写“悬浮任务列表已从 PROJECT_CURRENT 重建”；`exact` 补建写“悬浮任务列表已根据当前会话与项目文档正式补建”；`fallback` 写“悬浮任务列表已根据当前会话与项目文档生成安全恢复列表”。三种路径都必须追加“进行中步骤必须先核验中断点”。
7. 对 `in_progress` 步骤核验当前磁盘、测试和外部状态；未知或非幂等写操作只允许查询状态并暂停，不得自动重放。
8. 再把执行权交还 `autonomous-execution-rules` 判断是否继续。

当恢复源是真实 `blocked` / `manual_handoff` 的 `BLK-*` 记录时，恢复提示必须包含“用户授权操作”：请直接回复：`同意授权` 或 请直接回复：`暂不授权`，并注明授权边界（仅最近一条、唯一有效、仍未解除的 `BLK-*` 记录列明的恢复动作；授权后必须执行原恢复步骤并通过原验证入口，验证失败保持阻断；授权不构成跨任务、跨会话或未来写入的通用许可）。

“同一任务”必须有当前回合可核验的来源证据（当前对话明确承接该实施周期、来源文档或计划标识）并与当前 `session_id` 匹配。仅因工作目录相同、用户说了“继续”或项目存在其它会话的活动 projection，不足以把投影错投到当前会话；来源无法确认时必须明确说明“未重建：当前会话与活动投影来源无法确认”，保留 registry 磁盘状态并暂停 UI 重建，不得使用选择弹窗确认归属。

## 数据与安全约束

- 托管区契约、字段白名单和状态规则见 [task-plan-projection-contract.md](references/task-plan-projection-contract.md)。
- 多会话身份与共享文件并发边界：每条投影只按当前宿主提供的 `session_id` 及该条自身的计划身份选择；同项目、相同 `plan_key`、相同工作目录或最近更新时间都不能证明会话归属。当前 canonical `projection_id` 按 `session_id`、`plan_key`、`source_document`、`projection_origin` 的规范 JSON 计算；历史 ID 若只在加入 `synthesis_mode` 的 legacy 算法下匹配，仍是有效兼容 ID，不能仅因它与 canonical 算法结果不同就报损坏。校验只接受精确匹配的 canonical 或 legacy ID；两者都不匹配时保留原文件并退出该投影的 UI 恢复，禁止自动修复 ID 或从其它会话补拷身份。
- 所有会改写 `PROJECT_CURRENT.md` 的入口必须共用 `.PROJECT_CURRENT.md.lock`：持锁后重读最新全文，只改自己拥有的区段或当前 `session_id + 计划身份` 对应项，原样保留其他会话/计划投影及非托管正文，再按 UTF-8 大小限制和原子替换规则写回。原子替换本身不提供并发读改写保护；不能取得共享锁或不能在锁内重读时，保持原文件不变并报告写入失败。绝不使用数组顺序、更新时间或“项目内唯一活动项”选择要同步的会话清单。
- registry 的顶层结构、托管标记、JSON、版本和共享文件边界仍整体严格校验；v4 registry 中单条投影损坏或投影 ID / 业务身份重复时，读取器可将所有冲突候选转换为 v5 `quarantined_projections`，保存原始 JSON 与安全诊断字段，并继续处理身份唯一且不与隔离项冲突的计划。隔离项与当前会话计划可能重叠、隔离记录无法确认所属会话、身份不足以排除冲突，或 v5 活动投影自身损坏时，针对该计划失败关闭；所属会话未知的隔离项会阻止所有会话继续恢复或写入。待隔离原文含凭据、prompt、token 等敏感字段时拒绝转换，保留原文件不变。不得仅凭 `session_id` 去重：同一会话允许并存不同 `plan_key`。除显式 `migrate` 或正常成功写入外，读取不得改写文件；转换失败时保留原文。
- 投影不得保存 prompt、响应、凭据、token、线程 ID、业务数据或原始用户输入；原始宿主会话 / 线程标识只允许出现在受控字段 `session_id`，不得出现在其它字段或步骤文案中。
- 所有 CLI/Python 状态入口按显式 `session_id` 优先、`CODEX_THREAD_ID` 回退、WorkBuddy 宿主元数据（`CODEBUDDY_MCP_CONFIG` 的 `mcpServers.*.headers["X-WorkBuddy-Session-Id"]` 唯一值或 `WORKBUDDY_SESSION_ID` 环境变量）兜底解析；多来源不一致时拒绝，全缺失时失败关闭，禁止猜测 `legacy/default` 或其它会话；解析时禁止打印 `CODEBUDDY_MCP_CONFIG` 全文或 token。
- 最多一个 `in_progress`；允许因阻断暂时没有 `in_progress`。
- 指纹只根据有序任务 ID 和文案计算，状态与更新时间不参与。
- 读取兼容 `version: 1/2/3` 单投影与 v4 registry；任何成功写入统一为 `version: 5` registry。`projections[]` 按 `session_id + projection_id` 隔离计划，同一会话可并存多个不同计划身份；单投影读取 / 失活遇到多个候选时必须显式选择 `plan_key` 或 `projection_id`，否则失败关闭。v5 保留 `projection_origin=goal` 与 `synthesis_mode=goal_default|goal_blocked`，Goal 固定 `plan_key=GOAL/ACTIVE`、空 `source_document` 与不含 Goal 原文的细化默认清单；`blocked` 仅允许 Goal 且没有 `in_progress`。v1-v3 单投影只作读取 / migrate 兼容，不能覆盖其它投影。
- 文件必须是严格 UTF-8，最终全文不得超过 51,200 字节。
- 缺半边标记、重复区块、损坏 JSON、未知字段或敏感字段时必须拒绝，原文件保持不变。

## 工具不可用和停止条件

- UI 同步通道不可用：按本节前述 `UI_SYNC_BLOCKED` 规则降级继续；投影持久化失败、会话归属冲突/不确定或执行状态不明按各自安全边界处理。全文字节上限是持久化失败的专用例外：先压缩普通历史正文，压缩两轮后仍超限则保留原文件并继续领域任务，不阻断执行。
- 超时计时缺失、时间不是 UTC、暂停秒数非法或主动执行时长无法可靠计算：不创建 projection，不得用墙钟猜测补齐。
- 投影来源、指纹或正式计划无法确认：不重建 UI，不继续未知写操作。
- 原子替换失败：原文件必须保持不变，并按失败原因处理。候选全文仅因超过 51,200 字节被拒绝：先调用 `project-memory-rules` 在共享锁内压缩普通历史正文、验证托管区逐字节不变并重试，最多两轮；仍超限则保留原文件，不持久化该 projection，但继续领域任务，不把容量限制升级为任务阻断。
- 用户明确结束：只允许把投影失活并完成必要状态收口，不得扩展新任务。

## 通过标准

- 合法 registry 可跨进程稳定读取；多个会话及同一会话的多个计划可并存、交错写入互不覆盖，并按 `session_id + plan_key/projection_id` 生成精确 UI 同步 payload（Codex 宿主为 `update_plan` payload）。
- 首次 `ensure-start` 或 `write` 成功后直接返回同一当前会话 payload；主 Agent 下一动作必须同步 UI（Codex 宿主为 `update_plan`），不得先执行其它领域写操作。
- 状态入口统一按显式 `--session-id` 优先、`CODEX_THREAD_ID` 回退、WorkBuddy 宿主元数据兜底解析；多来源不一致、全缺失或非法时失败关闭且不写文件。
- 无活动 projection 的未完成任务在主动执行时间严格超过 600 秒后，先由只读 `probe-timeout` 返回 `goal_check_required`，再由主 Agent 优先创建或复用 Goal；只有 Goal 不匹配、不可用、失败或结果不明确时才通过 `ensure-timeout` 原子降级普通投影。未到阈值、已有活动 projection、已有 `blocked` Goal 观察投影和非法计时输入均不产生重复或错误写入。
- 状态迁移先落盘，崩溃发生在工具调用前时仍能恢复最新状态。
- 完成、损坏、过期和来源不匹配投影不会重放。
- 非托管正文逐字保留，非法输入不破坏原文件。
- UI 重建、执行授权和 L5 任务续接三者没有混淆。

## 执行入口

- 脚本：`scripts/task_plan_projection.py`
- 校验：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py validate --project-current PROJECT_CURRENT.md`
- 首次持久化并返回 payload：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py ensure-start --project-current PROJECT_CURRENT.md --input projection_or_synthesis_context.json --session-id <session-id>`（`--session-id` 可由 `CODEX_THREAD_ID` 回退）
- 写入正式投影并返回 payload：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py write --project-current PROJECT_CURRENT.md --input projection.json --session-id <session-id>`
- 生成当前会话 payload：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py payload --project-current PROJECT_CURRENT.md --session-id <session-id>`
- 创建 Goal 投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event create --session-id <session-id>`
- 恢复 Goal 投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event restore --session-id <session-id>`
- 迁移 Goal 终态：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event blocked|complete --session-id <session-id>`
- 补建当前会话投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json --session-id <session-id>`
- 只读探测超时资格：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py probe-timeout --project-current PROJECT_CURRENT.md --started-at <UTC-ISO-8601> --observed-at <UTC-ISO-8601> --paused-seconds <seconds> --session-id <session-id>`
- 超时升级当前会话投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py ensure-timeout --project-current PROJECT_CURRENT.md --started-at <UTC-ISO-8601> --observed-at <UTC-ISO-8601> --paused-seconds <seconds> --input synthesis_context.json --session-id <session-id>`
- 迁移旧单投影 registry：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py migrate --project-current PROJECT_CURRENT.md --session-id <session-id>`
- Python 入口按当前环境选择可用的 Python 3 命令；CLI 参数固定使用 `--project-current`，不得写成不存在的 `--file`。
- 单元测试：`python -X utf8 -B test/task-plan-rehydration-rules/task_plan_projection_test.py`
- Skill 校验：`python -B .system/skill-creator/scripts/quick_validate.py task-plan-rehydration-rules`
