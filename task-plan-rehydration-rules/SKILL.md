---
name: task-plan-rehydration-rules
description: 当正式实施计划需要投影到 Codex Desktop 任务悬浮窗、默认执行回合中的未完成任务没有活动悬浮窗且主动执行时间严格超过 10 分钟、任务步骤状态发生 pending/in_progress/completed 迁移、Goal 的 create/get/update 生命周期成功返回、Desktop 或宿主关闭后用户在同一任务首次发送任意“继续”或恢复意图、上下文压缩恢复时检测到 PROJECT_CURRENT 存在活动任务投影，或历史投影缺失但需要根据当前会话与项目文档补建悬浮任务列表时自动触发。任意继续语义包括“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义表达，不要求出现“任务”或“计划”。作为任务投影唯一 Owner，负责 PROJECT_CURRENT 多会话 registry 托管区的 schema、指纹、原子写入、失活、Goal 安全三步、10 分钟 Goal 优先升级、失败降级、校验、synthesize 补建和 update_plan payload；实际 Goal 工具与 UI 工具必须由主 Agent 调用，且进行中步骤先核验中断点。不要把 Goal 或 UI 重建当作执行授权或 L5 checkpoint resume，也不要重放未知幂等性的写操作。
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
- 默认执行回合开始时允许简单任务暂不创建悬浮窗；若任务仍未完成、当前会话没有活动或阻断 projection，且扣除 Plan Mode、等待用户、`blocked` 和 `manual_handoff` 暂停后的主动执行时间严格超过 600 秒，必须先探测并优先自动创建或复用 Goal，失败时降级普通悬浮窗。

## 唯一 Owner 边界

- 本 Skill 唯一负责：托管区标记、v4 registry JSON schema、会话投影归属、计划指纹、敏感字段拒绝、51,200 字节闸门、原子写入、失活和 payload 生成。
- `project-memory-rules` 只负责更新 `PROJECT_CURRENT.md` 的普通当前状态，并原样保留 registry 托管区。
- `project-rule-file-bootstrap-rules` 只在新建模板中提供空 registry，不管理活动投影。
- `parallel-task-dispatch-rules` 只负责判断是否启动只读子代理收集补建证据，不接管最终归属裁决。
- `autonomous-execution-rules` 只决定是否允许继续执行；投影恢复不恢复执行许可。
- `context-compression-rules` 只在压缩恢复路径调用本 Skill；Desktop 重开但未压缩时由本 Skill 自身触发。
- `agent-runtime-recovery-rules` 只声明 UI 重建不是 L5 任务续接，不接管投影。

## 保存和状态迁移流程

1. 从当前正式实施周期提取最多 20 个最小任务，只保留任务 ID、悬浮窗文案和三态状态。
2. 使用 `scripts/task_plan_projection.py write` 校验并原子更新 `PROJECT_CURRENT.md`。
3. 确认命令成功后，使用脚本 `payload` 输出的数据真实调用 `update_plan`。
4. `update_plan` 成功后才能说明悬浮任务列表已刷新；工具不可用或调用失败时只说明磁盘投影已保存。
5. 当前会话的当前周期全部完成后调用 `deactivate`；该会话的失活投影不得再次生成 payload，也不得影响其它会话投影。

固定顺序是“先持久化，再调用工具”。不得先刷新 UI 再补写磁盘状态。

## 无悬浮窗任务的 10 分钟 Goal 优先升级

1. 只在默认执行回合取得 `confirmed` 执行许可并进入第一个真实执行动作时开始计时；需求澄清、Plan Mode 计划编写和尚未取得执行许可的阶段不开始计时。
2. Agent 只在当前执行上下文维护开始时间和累计暂停秒数。等待用户、真实 `blocked` 与 `manual_handoff` 期间暂停累计；这些计时事实不写入 projection、步骤文案、`PROJECT_CURRENT.md` 普通正文或其它长期状态。
3. 每次工具返回、阶段进度更新和准备结束当前回合前检查一次。任务已经完成、当前处于 Plan Mode、执行许可不是 `confirmed` 或计时上下文丢失时，不调用超时探测、不创建 Goal、不刷新 UI；计时丢失后从下一次真实执行动作重新计时，禁止根据墙钟或历史消息猜测。
4. 主动执行时间 `observed_at - started_at - paused_seconds` 严格大于 600 秒才有资格升级；恰好 600 秒和不足 600 秒均不升级。时间必须是 UTC ISO-8601，暂停秒数必须非负且不得超过总墙钟时长。
5. 检查点先调用带当前 `session_id` 的只读 `probe-timeout`。`not_due` 不做任何动作；`already_active` 保持现有活动投影；`blocked_goal_preserved` 只保留观察状态；契约或 I/O 错误立即停止 Goal 路由，禁止猜测。只有 `goal_check_required` 才进入宿主 Goal 编排。
6. `goal_check_required` 后只允许当前主会话主 Agent 先调用一次 `get_goal`。子 Agent 不得调用 `get_goal`、`create_goal`、`update_goal` 或主悬浮窗 `update_plan`。
7. `get_goal` 返回的活动 Goal 与当前已确认任务来源和目标明确匹配时复用，不调用 `create_goal`；没有活动 Goal 时，主 Agent 使用脱敏任务摘要调用一次 `create_goal`；活动 Goal 不匹配或无法可靠确认匹配时，不覆盖、不创建第二个 Goal，直接进入普通投影降级。
8. `create_goal` 结果不明确时，只允许再调用一次 `get_goal` 确认，禁止无变化重试 `create_goal`。确认存在匹配活动 Goal 后，执行带当前 `session_id` 的 `goal --event create` 原子同步固定安全三步；脚本成功后才使用 payload 调用 `update_plan`。
9. Goal 工具不可用、创建失败、复核仍不明确、活动 Goal 不匹配，或 Goal 已成功但安全投影写入失败时，调用原 `ensure-timeout` 生成当前会话 `exact/fallback` 普通投影。Goal 已成功后不得再次创建；`ensure-timeout` 只作为失败降级入口，不再是到期后的首选入口。
10. 投影成功但 `update_plan` 失败时保留磁盘投影，不声称 UI 已刷新；后续检查点只恢复 UI，不重新创建 Goal。Goal 完成和阻断继续遵守既有真实完成条件与连续三次相同阻断门槛。

**Goal 目标摘要契约**

- 来源优先级固定为：已确认实施计划的最终方案摘要 -> 当前已确认用户目标 -> 固定兜底文案。
- 摘要必须是单行中文，最多 80 个 Unicode 字符；禁止包含密钥、token、密码、连接串、完整路径、session ID、原始 prompt、原始日志或大段用户输入。
- 无法可靠脱敏时固定使用“完成当前已确认的长任务并完成验证收口”。摘要只传给 `create_goal`，不得写入 `PROJECT_CURRENT.md`、测试 fixture、工程文档、项目记忆或 Obsidian。
- Goal 匹配只在宿主返回的活动状态和目标语义足以证明与当前确认来源一致时成立；不得依据标题、时间、路径、会话 ID 或相似关键词猜测。

本规则不是后台定时器：Agent 只能在可执行的进度检查点完成超时判断，不能承诺工具调用运行中或没有新回合时在第 601 秒精确唤醒。

## Goal 生命周期投影流程

1. `create_goal` 成功后，只在默认执行回合执行带当前 `session_id` 的 `goal --event create`。若该会话已有活动正式投影，脚本返回 `preserved_formal`，不得覆盖正式最小任务；否则原子写入不含 Goal 原文的固定三步，且不得影响其它会话投影。
2. Desktop 或会话重开后，先通过 `get_goal` 确认仍有活动 Goal；随后执行带同一 `session_id` 的 `goal --event restore`。活动 Goal 安全投影返回可恢复 payload；此前已保留的正式计划返回 `preserved_formal` 且不重写、不刷新，仍由其自身的正式计划恢复路径负责。阻断、失活、来源不匹配、损坏或 Plan Mode 一律明确退出。
3. `update_goal` 成功进入 `blocked` 时，执行 `goal --event blocked`：若当前是 Goal 安全投影，先持久化“无进行中步骤”的观察投影，再使用返回 payload 调用 `update_plan`；若 `create` 已返回 `preserved_formal`，则返回同名无副作用结果，保持正式计划独立且不得调用 `update_plan`。此 UI 仅观察进度，绝不恢复执行授权。
4. `update_goal` 成功进入 `complete` 时，执行 `goal --event complete`：Goal 安全投影须先持久化三步完成、投影失活且 `payload: null`；`preserved_formal` 同样返回无副作用结果，不得失活真实正式计划，也不得调用 `update_plan` 重放已完成 Goal。
5. Goal 运行中出现正式实施最小任务时，仍用带当前 `session_id` 的 `write` 写入正式投影；仅替换当前会话投影中的安全三步，其它会话投影保持不变。投影不得保存 Goal 原文、Goal ID、线程 ID、原始用户输入、prompt、response、业务数据或凭据。
6. 每个脚本事件成功后才读取返回 payload 并由当前主会话调用 `update_plan`；工具不可用或调用失败时仅说明投影已保存。Plan Mode 不调用 Goal CLI，也不调用 `update_plan`。


**主智能体投影责任（多智能体委派场景）**

- 只有当前主会话的主智能体调用 `update_plan` 才会驱动 Codex Desktop 主悬浮窗；子智能体在自身作用域内调用 `update_plan` 不会顶到主悬浮窗。
- 主智能体把最小任务委派给子智能体（`spawn_agent` / 并行 / delegation）时，必须在主会话保留并持续更新一份映射整体进度的主计划；每当子智能体返回阶段结果，主智能体要把对应步骤迁移为 `completed` 并把下一步置 `in_progress`，避免主智能体长时间只 `wait_agent` 导致主悬浮窗“空窗”。
- 本投影的 `update_plan` 必须在 default 执行模式回合内调用；Plan Mode 只产出 `<proposed_plan>` 计划文档卡片、不驱动步骤悬浮窗，不得用 Plan Mode 的计划卡片替代主计划投影。
- fork 会话打开时，父会话的历史 `update_plan` 只是静态回放上下文，不会自动重建 live 主悬浮窗；需要悬浮窗时由当前主会话主智能体依据 `PROJECT_CURRENT` 重新调用 `update_plan`。

## 首次继续回合恢复流程

当前回合处于 Plan Mode 时，本 Skill 只保留候选命中，不读取投影、不调用 `update_plan`，也不创建任务悬浮窗。Plan Mode 是形成、修改或确认正式执行计划的阶段；用户选择、受限计划和正式计划均由 `implementation-planning-rules` 处理。只有 Plan Mode 已结束且当前开始执行已确认计划时，才允许进入以下恢复流程。

1. 在任何领域写操作前读取 `PROJECT_CURRENT.md`。
2. 若 registry 托管区存在，则必须使用当前 `session_id` 定位唯一 projection，再用 `validate` 校验来源文档、计划指纹、状态约束和文件大小；有效 `active` projection 直接使用 `payload` 重建。无匹配、多匹配、来源不一致或归属不确定时不得读取其它会话 projection。
3. 若 registry 托管区缺失，或当前 `session_id` 无匹配 projection，则先由主代理派只读子代理收集候选来源文档、完成步骤提示、当前步骤提示和冲突信息；子代理不得决定最终归属、不得写回文件、不得直接调用 `update_plan`。
4. 主代理把当前会话摘要、`PROJECT_CURRENT` 普通正文、子代理证据和候选来源文档传给 `synthesize`，并绑定当前 `session_id`。唯一来源且存在明确状态提示时生成 `exact` 正式补建；否则生成固定三步 `fallback` 安全恢复列表。
5. `exact` 或 `fallback` 结果都必须先原子写回托管区，再生成 `payload`；`inactive`、过期、损坏或来源不匹配时不调用工具。
6. 真实调用 `update_plan` 后固定说明：历史投影命中时写“悬浮任务列表已从 PROJECT_CURRENT 重建”；`exact` 补建写“悬浮任务列表已根据当前会话与项目文档正式补建”；`fallback` 写“悬浮任务列表已根据当前会话与项目文档生成安全恢复列表”。三种路径都必须追加“进行中步骤必须先核验中断点”。
7. 对 `in_progress` 步骤核验当前磁盘、测试和外部状态；未知或非幂等写操作只允许查询状态并暂停，不得自动重放。
8. 再把执行权交还 `autonomous-execution-rules` 判断是否继续。

“同一任务”必须有当前回合可核验的来源证据（当前对话明确承接该实施周期、来源文档或计划标识）并与当前 `session_id` 匹配。仅因工作目录相同、用户说了“继续”或项目存在其它会话的活动 projection，不足以把投影错投到当前会话；来源无法确认时必须明确说明“未重建：当前会话与活动投影来源无法确认”，保留 registry 磁盘状态并暂停 UI 重建，不得使用选择弹窗确认归属。

## 数据与安全约束

- 托管区契约、字段白名单和状态规则见 [task-plan-projection-contract.md](references/task-plan-projection-contract.md)。
- 投影不得保存 prompt、响应、凭据、token、线程 ID、业务数据或原始用户输入；原始宿主会话 / 线程标识只允许出现在受控字段 `session_id`，不得出现在其它字段或步骤文案中。
- 最多一个 `in_progress`；允许因阻断暂时没有 `in_progress`。
- 指纹只根据有序任务 ID 和文案计算，状态与更新时间不参与。
- 读取兼容 `version: 1/2/3`；任何成功写入统一为 `version: 4` registry。registry 的 `projections[]` 按 `session_id + projection_id` 隔离多个会话；v4 保留 `projection_origin=goal` 和 `synthesis_mode=goal_default|goal_blocked`，Goal 固定 `plan_key=GOAL/ACTIVE`、空 `source_document` 与安全三步；`blocked` 仅允许 Goal 且没有 `in_progress`。v1-v3 单投影只作读取 / migrate 兼容，不能覆盖其它会话 projection。
- 文件必须是严格 UTF-8，最终全文不得超过 51,200 字节。
- 缺半边标记、重复区块、损坏 JSON、未知字段或敏感字段时必须拒绝，原文件保持不变。

## 工具不可用和停止条件

- `update_plan` 不可用：保留当前会话活动 projection，不得声称 UI 已恢复。
- 超时计时缺失、时间不是 UTC、暂停秒数非法或主动执行时长无法可靠计算：不创建 projection，不得用墙钟猜测补齐。
- 投影来源、指纹或正式计划无法确认：不重建 UI，不继续未知写操作。
- 原子替换失败或候选全文超限：原文件必须保持不变。
- 用户明确结束：只允许把投影失活并完成必要状态收口，不得扩展新任务。

## 通过标准

- 合法 registry 可跨进程稳定读取；多个会话 projection 可并存、交错写入互不覆盖，并按 `session_id` 生成精确 `update_plan` payload。
- 无活动 projection 的未完成任务在主动执行时间严格超过 600 秒后，先由只读 `probe-timeout` 返回 `goal_check_required`，再由主 Agent 优先创建或复用 Goal；只有 Goal 不匹配、不可用、失败或结果不明确时才通过 `ensure-timeout` 原子降级普通投影。未到阈值、已有活动 projection、已有 `blocked` Goal 观察投影和非法计时输入均不产生重复或错误写入。
- 状态迁移先落盘，崩溃发生在工具调用前时仍能恢复最新状态。
- 完成、损坏、过期和来源不匹配投影不会重放。
- 非托管正文逐字保留，非法输入不破坏原文件。
- UI 重建、执行授权和 L5 任务续接三者没有混淆。

## 执行入口

- 脚本：`scripts/task_plan_projection.py`
- 校验：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py validate --project-current PROJECT_CURRENT.md`
- 生成当前会话 payload：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py payload --project-current PROJECT_CURRENT.md --session-id <session-id>`
- 创建 Goal 投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event create --session-id <session-id>`
- 恢复 Goal 投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event restore --session-id <session-id>`
- 迁移 Goal 终态：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py goal --project-current PROJECT_CURRENT.md --event blocked|complete --session-id <session-id>`
- 补建当前会话投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json --session-id <session-id>`
- 只读探测超时资格：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py probe-timeout --project-current PROJECT_CURRENT.md --started-at <UTC-ISO-8601> --observed-at <UTC-ISO-8601> --paused-seconds <seconds> --session-id <session-id>`
- 超时升级当前会话投影：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py ensure-timeout --project-current PROJECT_CURRENT.md --started-at <UTC-ISO-8601> --observed-at <UTC-ISO-8601> --paused-seconds <seconds> --input synthesis_context.json --session-id <session-id>`
- 迁移旧单投影 registry：`python3 -X utf8 -B task-plan-rehydration-rules/scripts/task_plan_projection.py migrate --project-current PROJECT_CURRENT.md --session-id <session-id>`
- Python 入口按当前环境选择可用的 Python 3 命令；CLI 参数固定使用 `--project-current`，不得写成不存在的 `--file`。
- 单元测试：`python -B task-plan-rehydration-rules/tests/test_task_plan_projection.py`
- Skill 校验：`python -B .system/skill-creator/scripts/quick_validate.py task-plan-rehydration-rules`
