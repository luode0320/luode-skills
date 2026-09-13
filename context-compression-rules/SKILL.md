---
name: context-compression-rules
description: 基于“上下文压缩是有损的、必然丢失细节”这一前提工作：当当前会话已发生“压缩上下文 / 自动压缩上下文 / 上下文太多”后的压缩重组，或继续执行前刚得到压缩摘要时自动触发。负责按共享 context-recovery-contract 重新读取当前平台规则文件与项目当前上下文，恢复目标、阶段、约束、必命中 skill 和“是否允许开始/继续实现代码”的许可状态；恢复只认磁盘事实源（按执行顺序命名的任务计划文档、doc/ 工程文档、项目记忆四件套、知识库），压缩摘要只作线索不作细节来源；只有确认缺少继续任务所需的近期项目事实时，才条件联动 recent-context-bootstrap-rules 补载近 3 天上下文与 skill 索引。不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线分析或当前主域执行。
---

# 上下文压缩规则

只在上下文压缩已经发生后使用这个 skill；尚未压缩时不得提前触发。

## 有损前提与落盘纪律（最高优先级）

本 skill 的全部设计基于一个不可协商的前提：

- **上下文压缩是有损的，必然丢失细节**；压缩发生时机不可精确预测，任何未落盘的内容——计划、任务状态、决策、偏差、证据——在压缩后都必须视为已经丢失。
- 推论一（磁盘是唯一可靠记忆）：唯一可靠的记忆载体是磁盘文件（项目 `doc/` 下按执行顺序命名的任务计划文档与工程文档、项目记忆四件套、知识库）；会话上下文、聊天输出、思考过程、宿主 UI 任务列表和临时文件都不是事实源。
- 推论二（写入纪律先于恢复纪律）：不要指望“压缩后还能恢复”，而要在压缩发生前的每个状态变更点先把状态写盘（write-through，检查点节奏见 `../autonomous-execution-rules/references/state-persistence-and-task-granularity.md`）；压缩恢复只是最后防线，不是常态手段。
- 推论三（恢复只认磁盘）：压缩后重建上下文时，摘要只作线索；任何细节（数值、路径、命令、结论、状态）必须回读对应磁盘文件确认后才可引用，禁止把压缩摘要中残存的细节直接当作已确认事实。
- 压缩恢复后的第一件事，是读取当前任务的持久化任务计划文档，按其状态字段与“下一动作”指针确定恢复偏移，而不是依赖对话记忆续做。

## Skill 作用与适用场景

- 按共享恢复契约重建继续当前任务所需的最小上下文。
- 强制重新读取当前平台规则文件和项目当前上下文，恢复仓库级硬规则与主线状态。
- 判断近期事实是 `sufficient`、`missing` 还是 `uncertain`；不得把“发生压缩”直接等同于“必须预热最近 3 天”。
- 只有确认状态为 `missing` 时，才条件联动 `recent-context-bootstrap-rules`。
- 恢复编码许可状态 `confirmed` / `not-confirmed` / `unknown`；未确认默认 `unknown`，不得直接编码。
- 输出可立即交还主域的最小上下文包，不代替主域执行。

## 自动触发信号

- 刚完成“压缩上下文 / 自动压缩上下文 / 上下文太多”后的摘要重组。
- 系统自动压缩后准备继续执行当前任务。
- 用户明确表示“已经压缩完了，继续”或“按压缩结果继续执行”。
- 压缩后存在规则、Skill、范围、许可或下一执行点丢失风险。
- 压缩恢复后需要确定当前任务的恢复偏移（回读任务计划文档状态字段与下一动作指针）。

## 进入后先做什么

1. 确认压缩已经完成；未完成则不触发。
2. 读取 `references/context-recovery-contract.md`，按固定顺序恢复规则、项目状态、目标、范围、验证和许可。
3. 重新读取当前平台规则文件；项目存在 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md` 时按契约读取，不把 `PROJECT_HISTORY.md` 当作默认来源。
4. `PROJECT_CURRENT.md` 存在任务投影托管区时，先由 `task-plan-rehydration-rules` 按当前 `session_id` 校验有效 `active`/`blocked` projection，并立即真实调用 `update_plan` 重建悬浮任务列表；失活、损坏、过期、工具不可用分别记录状态，不伪报恢复。仅投影持久化失败、会话归属冲突/不确定或执行状态不明时硬阻断领域动作；单纯 UI 同步通道不可用（磁盘投影已成功且归属明确）时保留磁盘投影并继续领域执行，下一检查点重试 UI，不得声称 UI 已恢复。
   - 若压缩恢复后许可已为 `confirmed` 但当前 session 没有活动 projection，必须先持久化 `active` 或 `blocked` projection，再立即调用 `update_plan`；投影持久化失败、会话归属冲突/不确定或执行状态不明时硬阻断，仅 UI 同步失败时进入 `UI_SYNC_BLOCKED` 降级继续：保留磁盘 projection + 继续领域执行，下一检查点重试 UI，不得声称 UI 已恢复。
   - 压缩恢复后必须先核对任务状态（联动 `reasoning-summary-structure-rules` 的 `SUMMARY-GATE-PMW-002`）：读取宿主任务列表 pending/in_progress 任务与投影 registry 未完成 step；存在未完成必需项时，恢复后必须继续执行，或输出显式中断点（已完成清单 + 剩余任务清单 + 下一动作 + 重入入口/投影 ID），禁止“压缩后误判已完成”式收口。
5. 评估近期事实状态：只有明确缺少继续任务所需的最近改动、证据或执行点时才标记 `missing`；同时读取当前任务的持久化任务计划文档，按其状态字段与“下一动作”指针确定恢复偏移；文档缺失时先按 `../autonomous-execution-rules/references/state-persistence-and-task-granularity.md` 补建落盘再继续，不得凭对话记忆续做。
6. 状态为 `missing` 时条件联动 `recent-context-bootstrap-rules`；`sufficient` 时直接继续，`uncertain` 时先核验现有来源，不得无条件预热。
7. 输出最小上下文包并交还当前主域。

## 默认执行流程

1. 读 `references/trigger-signals.md` 确认压缩后触发。
2. 读 `references/context-recovery-contract.md` 执行共享恢复顺序和近期事实判定。
3. 读 `references/compression-playbook.md` 生成保留、折叠和剔除结果。
4. 读 `references/boundary-rules.md` 确认与近期预热、历史回忆和主域的边界。
5. 读取当前状态后按 `task-plan-rehydration-rules` 输出 `task_projection` 恢复状态；进行中步骤只恢复 UI，不直接继续未知写操作。`Plan Mode` 不写入活动 projection，也不调用 `update_plan`；十分钟仅用于发现缺失 projection 后的只读异常修复，不作为正常任务首次显示悬浮窗的入口。
   - `Plan Mode` 压缩恢复期间禁止生成总结型 `final_answer`、`# 📋 本轮总结` 或其它用户可见总结；恢复后继续由 `implementation-planning-rules` 生成原计划。
6. 仅当 `recent_context_state=missing` 时调用 `recent-context-bootstrap-rules`；否则记录未调用原因。
7. 输出当前目标、已确认事实、约束、关键路径、待确认项、下一动作、编码许可、规则重载状态、任务投影和近期事实路由状态。
8. 立即退出并交还主执行权。

## 权责边界与不负责事项

- 不代替需求、Bug、编码、测试、审查、验收或交付。
- 不代替 `history-recall-rules` 的明确历史回溯，也不输出长期时间线。
- 不把压缩摘要、旧记忆或近期材料伪装成当前已确认事实。
- 不因压缩而删除仍影响决策的用户习惯、安全、授权、停止、回滚和范围边界。
- `Plan Mode` 不持久化活动 projection、不调用 `update_plan`；默认执行恢复只允许同步当前 session，禁止跨 session 读取、刷新或覆盖。
- 不得在规则未恢复或编码许可不是 `confirmed` 时继续编码。
- 用户明确停止、终止或不要继续时，恢复动作只允许形成最小收口，不得重启原任务。

## 需要暂停并确认的条件

- 当前平台规则文件缺失、损坏或无法读取。
- 现有摘要、项目状态与当前工作区事实冲突，无法确定有效来源。
- 编码许可为 `not-confirmed` 或 `unknown`，但下一步要求修改代码。
- 近期事实状态持续为 `uncertain`，且继续会引入错误决策。
- 用户明确停止、终止或撤销继续执行授权。

## 执行通过 / 驳回标准

- 通过：规则与项目状态已恢复，近期事实完成三态判定，只有 `missing` 才调用近期预热，编码许可和下一动作明确；恢复偏移已按磁盘任务计划文档确认。
- 驳回：压缩后无条件调用 `recent-context-bootstrap-rules`、跳过规则重载、把不确定内容写成事实，或未确认许可就继续编码；或压缩恢复后凭对话记忆续做而不回读任务计划文档。

## 执行结果归档要求

- 本 skill 自身默认不新建持久化文档；但恢复过程中确认的、影响后续执行的事实（决策、偏差、新约束、状态修正）必须由当前主域写回对应持久化载体（任务计划文档 / `PROJECT_CURRENT.md` / 知识库），不得只留在会话上下文——写入纪律见“有损前提与落盘纪律”一节。
- 若主域要求更新当前任务状态，由对应项目记忆或文档 Owner 执行，本 skill 不越权写入。
- 最小证据包括规则重载状态、项目状态来源、近期事实三态、是否调用近期预热及原因、编码许可、恢复偏移来源文件和下一执行点。

## references 读取规则

- 触发判断：`references/trigger-signals.md`
- 共享恢复契约：`references/context-recovery-contract.md`
- 压缩模板：`references/compression-playbook.md`
- 边界与让路：`references/boundary-rules.md`
- 落盘持久化与任务拆分契约（有损前提的执行细则）：`../autonomous-execution-rules/references/state-persistence-and-task-granularity.md`
