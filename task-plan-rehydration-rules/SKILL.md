---
name: task-plan-rehydration-rules
description: 当正式实施计划需要投影到 Codex Desktop 任务悬浮窗、任务步骤状态发生 pending/in_progress/completed 迁移、Goal 的 create/get/update 生命周期成功返回、Desktop 或宿主关闭后用户在同一任务首次发送任意“继续”或恢复意图、上下文压缩恢复时检测到 PROJECT_CURRENT 存在活动任务投影，或历史投影缺失但需要根据当前会话与项目文档补建悬浮任务列表时自动触发。任意继续语义包括“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义表达，不要求出现“任务”或“计划”。作为任务投影唯一 Owner，负责 PROJECT_CURRENT 托管区的 schema、指纹、原子写入、失活、Goal 安全三步、校验、synthesize 补建和 update_plan payload；实际 UI 重建必须由 Agent 调用 update_plan，且进行中步骤先核验中断点。不要把 UI 重建当作执行授权或 L5 checkpoint resume，也不要重放未知幂等性的写操作。
---

# 任务计划断点恢复规则

## 目标

把当前实施周期的精简任务列表持久化到 `PROJECT_CURRENT.md`，在 Codex Desktop 关闭、宿主中断或上下文恢复后的首次继续回合中重建悬浮任务列表。正式实施文档仍是真实计划源，本 Skill 只拥有运行时任务投影。

## 自动触发信号

- 正式实施周期首次进入执行，需要把最小任务同步到悬浮任务列表。
- 任一任务从 `pending` 迁移为 `in_progress`，或从 `in_progress` 迁移为 `completed`。
- 当前周期全部完成，需要把投影设为 `inactive`。
- Desktop 或宿主关闭后，用户在同一任务首次发送任意“继续”或恢复意图；至少包括“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义表达。
- 上下文压缩恢复、新会话恢复或项目状态重载时，`PROJECT_CURRENT.md` 存在有效活动投影。
- 历史投影缺失，但当前会话和项目文档需要补建正式悬浮任务列表。
- `update_plan` 调用失败后需要保留磁盘状态，并在下一个可用回合重建 UI。
- 当前实施周期把最小任务委派给子智能体（`spawn_agent` / 多智能体并行 / delegation）执行，主智能体需要维持并持续更新面向用户的主计划投影。
- `create_goal` 成功后、默认执行回合检测到活动 Goal、`update_goal` 成功进入 `blocked` 或 `complete` 时，需要生成、恢复或迁移 Goal 专属投影。

## 唯一 Owner 边界

- 本 Skill 唯一负责：托管区标记、JSON schema、计划指纹、敏感字段拒绝、51,200 字节闸门、原子写入、失活和 payload 生成。
- `project-memory-rules` 只负责更新 `PROJECT_CURRENT.md` 的普通当前状态，并原样保留托管区。
- `project-rule-file-bootstrap-rules` 只在新建模板中提供失活槽位，不管理活动投影。
- `parallel-task-dispatch-rules` 只负责判断是否启动只读子代理收集补建证据，不接管最终归属裁决。
- `autonomous-execution-rules` 只决定是否允许继续执行；投影恢复不恢复执行许可。
- `context-compression-rules` 只在压缩恢复路径调用本 Skill；Desktop 重开但未压缩时由本 Skill 自身触发。
- `agent-runtime-recovery-rules` 只声明 UI 重建不是 L5 任务续接，不接管投影。

## 保存和状态迁移流程

1. 从当前正式实施周期提取最多 20 个最小任务，只保留任务 ID、悬浮窗文案和三态状态。
2. 使用 `scripts/task_plan_projection.py write` 校验并原子更新 `PROJECT_CURRENT.md`。
3. 确认命令成功后，使用脚本 `payload` 输出的数据真实调用 `update_plan`。
4. `update_plan` 成功后才能说明悬浮任务列表已刷新；工具不可用或调用失败时只说明磁盘投影已保存。
5. 当前周期全部完成后调用 `deactivate`；失活投影不得再次生成 payload。

固定顺序是“先持久化，再调用工具”。不得先刷新 UI 再补写磁盘状态。


## Goal 生命周期投影流程

1. `create_goal` 成功后，只在默认执行回合执行 `goal --event create`。若已有活动正式投影，脚本返回 `preserved_formal`，不得覆盖正式最小任务；否则原子写入不含 Goal 原文的固定三步。
2. Desktop 或会话重开后，先通过 `get_goal` 确认仍有活动 Goal；随后执行 `goal --event restore`。活动 Goal 安全投影返回可恢复 payload；此前已保留的正式计划返回 `preserved_formal` 且不重写、不刷新，仍由其自身的正式计划恢复路径负责。阻断、失活、来源不匹配、损坏或 Plan Mode 一律明确退出。
3. `update_goal` 成功进入 `blocked` 时，执行 `goal --event blocked`：若当前是 Goal 安全投影，先持久化“无进行中步骤”的观察投影，再使用返回 payload 调用 `update_plan`；若 `create` 已返回 `preserved_formal`，则返回同名无副作用结果，保持正式计划独立且不得调用 `update_plan`。此 UI 仅观察进度，绝不恢复执行授权。
4. `update_goal` 成功进入 `complete` 时，执行 `goal --event complete`：Goal 安全投影须先持久化三步完成、投影失活且 `payload: null`；`preserved_formal` 同样返回无副作用结果，不得失活真实正式计划，也不得调用 `update_plan` 重放已完成 Goal。
5. Goal 运行中出现正式实施最小任务时，仍用既有 `write` 写入正式投影，唯一托管区会替换安全三步。投影不得保存 Goal 原文、Goal ID、线程 ID、原始用户输入、prompt、response、业务数据或凭据。
6. 每个脚本事件成功后才读取返回 payload 并由当前主会话调用 `update_plan`；工具不可用或调用失败时仅说明投影已保存。Plan Mode 不调用 Goal CLI，也不调用 `update_plan`。


**主智能体投影责任（多智能体委派场景）**

- 只有当前主会话的主智能体调用 `update_plan` 才会驱动 Codex Desktop 主悬浮窗；子智能体在自身作用域内调用 `update_plan` 不会顶到主悬浮窗。
- 主智能体把最小任务委派给子智能体（`spawn_agent` / 并行 / delegation）时，必须在主会话保留并持续更新一份映射整体进度的主计划；每当子智能体返回阶段结果，主智能体要把对应步骤迁移为 `completed` 并把下一步置 `in_progress`，避免主智能体长时间只 `wait_agent` 导致主悬浮窗“空窗”。
- 本投影的 `update_plan` 必须在 default 执行模式回合内调用；Plan Mode 只产出 `<proposed_plan>` 计划文档卡片、不驱动步骤悬浮窗，不得用 Plan Mode 的计划卡片替代主计划投影。
- fork 会话打开时，父会话的历史 `update_plan` 只是静态回放上下文，不会自动重建 live 主悬浮窗；需要悬浮窗时由当前主会话主智能体依据 `PROJECT_CURRENT` 重新调用 `update_plan`。

## 首次继续回合恢复流程

当前回合处于 Plan Mode 时，本 Skill 只保留候选命中，不读取投影、不调用 `update_plan`，也不创建任务悬浮窗。Plan Mode 是形成、修改或确认正式执行计划的阶段；用户选择、受限计划和正式计划均由 `implementation-planning-rules` 处理。只有 Plan Mode 已结束且当前开始执行已确认计划时，才允许进入以下恢复流程。

1. 在任何领域写操作前读取 `PROJECT_CURRENT.md`。
2. 若唯一托管区存在，则先用 `validate` 校验来源文档、计划指纹、状态约束和文件大小；有效 `active` 投影直接使用 `payload` 重建。
3. 若唯一托管区缺失，则先由主代理派只读子代理收集候选来源文档、完成步骤提示、当前步骤提示和冲突信息；子代理不得决定最终归属、不得写回文件、不得直接调用 `update_plan`。
4. 主代理把当前会话摘要、`PROJECT_CURRENT` 普通正文、子代理证据和候选来源文档传给 `synthesize`。唯一来源且存在明确状态提示时生成 `exact` 正式补建；否则生成固定三步 `fallback` 安全恢复列表。
5. `exact` 或 `fallback` 结果都必须先原子写回托管区，再生成 `payload`；`inactive`、过期、损坏或来源不匹配时不调用工具。
6. 真实调用 `update_plan` 后固定说明：历史投影命中时写“悬浮任务列表已从 PROJECT_CURRENT 重建”；`exact` 补建写“悬浮任务列表已根据当前会话与项目文档正式补建”；`fallback` 写“悬浮任务列表已根据当前会话与项目文档生成安全恢复列表”。三种路径都必须追加“进行中步骤必须先核验中断点”。
7. 对 `in_progress` 步骤核验当前磁盘、测试和外部状态；未知或非幂等写操作只允许查询状态并暂停，不得自动重放。
8. 再把执行权交还 `autonomous-execution-rules` 判断是否继续。

“同一任务”必须有当前回合可核验的来源证据（当前对话明确承接该实施周期、来源文档或计划标识）。仅因工作目录相同、用户说了“继续”或项目存在活动投影，不足以把投影错投到其它会话；来源无法确认时必须明确说明“未重建：当前会话与活动投影来源无法确认”，保留磁盘状态并暂停 UI 重建，不得使用选择弹窗确认归属。

## 数据与安全约束

- 托管区契约、字段白名单和状态规则见 [task-plan-projection-contract.md](references/task-plan-projection-contract.md)。
- 投影不得保存 prompt、响应、凭据、token、线程 ID、业务数据或原始用户输入。
- 最多一个 `in_progress`；允许因阻断暂时没有 `in_progress`。
- 指纹只根据有序任务 ID 和文案计算，状态与更新时间不参与。
- 读取兼容 `version: 1/2`；任何成功写入统一为 `version: 3`。v3 允许 `projection_origin=goal` 和 `synthesis_mode=goal_default|goal_blocked`，Goal 固定 `plan_key=GOAL/ACTIVE`、空 `source_document` 与安全三步；`blocked` 仅允许 Goal 且没有 `in_progress`。
- 文件必须是严格 UTF-8，最终全文不得超过 51,200 字节。
- 缺半边标记、重复区块、损坏 JSON、未知字段或敏感字段时必须拒绝，原文件保持不变。

## 工具不可用和停止条件

- `update_plan` 不可用：保留活动投影，不得声称 UI 已恢复。
- 投影来源、指纹或正式计划无法确认：不重建 UI，不继续未知写操作。
- 原子替换失败或候选全文超限：原文件必须保持不变。
- 用户明确结束：只允许把投影失活并完成必要状态收口，不得扩展新任务。

## 通过标准

- 合法活动投影可跨进程稳定读取并生成精确 `update_plan` payload。
- 状态迁移先落盘，崩溃发生在工具调用前时仍能恢复最新状态。
- 完成、损坏、过期和来源不匹配投影不会重放。
- 非托管正文逐字保留，非法输入不破坏原文件。
- UI 重建、执行授权和 L5 任务续接三者没有混淆。

## 执行入口

- 脚本：`scripts/task_plan_projection.py`
- 校验：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py validate --project-current PROJECT_CURRENT.md`
- 生成 payload：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py payload --project-current PROJECT_CURRENT.md`
- 创建 Goal 投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event create`
- 恢复 Goal 投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event restore`
- 迁移 Goal 终态：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event blocked|complete`
- 补建投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json`
- Python 入口按当前环境选择可用的 Python 3 命令；CLI 参数固定使用 `--project-current`，不得写成不存在的 `--file`。
- 单元测试：`python -B task-plan-rehydration-rules/tests/test_task_plan_projection.py`
- Skill 校验：`python -B .system/skill-creator/scripts/quick_validate.py task-plan-rehydration-rules`
