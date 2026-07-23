---
name: task-plan-rehydration-rules
description: 当正式实施计划需要投影到 Codex Desktop 任务悬浮窗、任务步骤状态发生 pending/in_progress/completed 迁移、Desktop 或宿主关闭后用户在同一任务首次发送任意“继续”或恢复意图、上下文压缩恢复时检测到 PROJECT_CURRENT 存在活动任务投影，或计划完成需要停止后续重放时自动触发。任意继续语义包括“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义表达，不要求出现“任务”或“计划”。作为任务投影唯一 Owner，负责 PROJECT_CURRENT 托管区的 schema、指纹、原子写入、失活、校验和 update_plan payload；实际 UI 重建必须由 Agent 调用 update_plan，且进行中步骤先核验中断点。不要把 UI 重建当作执行授权或 L5 checkpoint resume，也不要重放未知幂等性的写操作。
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
- `update_plan` 调用失败后需要保留磁盘状态，并在下一个可用回合重建 UI。

## 唯一 Owner 边界

- 本 Skill 唯一负责：托管区标记、JSON schema、计划指纹、敏感字段拒绝、51,200 字节闸门、原子写入、失活和 payload 生成。
- `project-memory-rules` 只负责更新 `PROJECT_CURRENT.md` 的普通当前状态，并原样保留托管区。
- `project-rule-file-bootstrap-rules` 只在新建模板中提供失活槽位，不管理活动投影。
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

## 首次继续回合恢复流程

当前回合处于 Plan Mode 时，本 Skill 只保留候选命中，不读取投影、不调用 `update_plan`，也不创建任务悬浮窗。Plan Mode 是形成、修改或确认正式执行计划的阶段；用户选择、受限计划和正式计划均由 `implementation-planning-rules` 处理。只有 Plan Mode 已结束且当前开始执行已确认计划时，才允许进入以下恢复流程。

1. 在任何领域写操作前读取 `PROJECT_CURRENT.md`。
2. 使用 `validate` 校验唯一托管区、来源文档、计划指纹、状态约束和文件大小。
3. 有效 `active` 投影使用 `payload` 生成原步骤和状态；`inactive`、过期、损坏或来源不匹配时不调用工具。
4. 真实调用 `update_plan` 后固定说明：“悬浮任务列表已从 PROJECT_CURRENT 重建；进行中步骤必须先核验中断点”。
5. 对 `in_progress` 步骤核验当前磁盘、测试和外部状态；未知或非幂等写操作只允许查询状态并暂停，不得自动重放。
6. 再把执行权交还 `autonomous-execution-rules` 判断是否继续。

“同一任务”必须有当前回合可核验的来源证据（当前对话明确承接该实施周期、来源文档或计划标识）。仅因工作目录相同、用户说了“继续”或项目存在活动投影，不足以把投影错投到其它会话；来源无法确认时必须明确说明“未重建：当前会话与活动投影来源无法确认”，保留磁盘状态并暂停 UI 重建，不得使用选择弹窗确认归属。

## 数据与安全约束

- 托管区契约、字段白名单和状态规则见 [task-plan-projection-contract.md](references/task-plan-projection-contract.md)。
- 投影不得保存 prompt、响应、凭据、token、线程 ID、业务数据或原始用户输入。
- 最多一个 `in_progress`；允许因阻断暂时没有 `in_progress`。
- 指纹只根据有序任务 ID 和文案计算，状态与更新时间不参与。
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
- Python 入口按当前环境选择可用的 Python 3 命令；CLI 参数固定使用 `--project-current`，不得写成不存在的 `--file`。
- 单元测试：`python -B task-plan-rehydration-rules/tests/test_task_plan_projection.py`
- Skill 校验：`python -B .system/skill-creator/scripts/quick_validate.py task-plan-rehydration-rules`
