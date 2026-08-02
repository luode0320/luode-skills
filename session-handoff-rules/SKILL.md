---
name: session-handoff-rules
description: 当用户表达“开新会话继续”“新会话中继续”“新会话继续”“会话太长”“归档旧会话”“迁移任务”“接续任务”“提取会话压缩信息”“唤起另一个会话”等，或要求把当前 Codex 任务交给新的本地任务时触发。提取当前目标、范围、已完成项、进行中、下一步、阻断、验证和关键决策，生成脱敏交接包，并在同一保存项目的 local 环境创建新任务继续；默认只提示人工归档旧任务，不自动归档。
---

# 会话交接规则

## 目标

把当前会话压缩为一个可验证、可脱敏、可交接的最小任务包，然后在同一保存项目的 `local` 环境唤起新的 Codex 任务。新任务必须重新建立自己的上下文和任务投影，不把旧会话的 UI 状态、执行授权或未验证假设直接当成事实。

## 触发与边界

- 触发词包括：`开新会话继续`、`新会话中继续`、`新会话继续`、`会话太长`、`归档旧会话`、`迁移任务`、`接续任务`、`提取会话压缩信息`、`唤起另一个会话`，以及语义等价的“把当前任务交给新会话继续”。
- 交接前先命中 `skill-hit-check-rules`；新任务首轮再命中一次，并按 `task-plan-rehydration-rules`、`project-memory-rules` 读取当前项目上下文。
- 只提取当前会话和当前项目实际可核验的信息；不把模型猜测、旧摘要或未验证的“下一步”伪装成完成事实。
- 交接包不得包含 API key、token、密码、私钥、Cookie、完整连接串、原始鉴权头、绝对本机路径、原始 prompt、完整日志、`session_id` 或 `thread_id`。
- v1 的归档策略固定为 `manual_only`：新任务成功创建后只提示用户在 UI 中人工归档旧任务，不自动调用 `codex_app__set_thread_archived`。只有用户在后续独立回合明确授权实际归档时，才进入归档工具路由。
- 不因交接自动提交、推送、切分支、重放非幂等写操作或切换到 test、staging、pre、release、prod 环境。

## 标准流程

1. **冻结当前状态**：读取当前项目父目录平台规则，以及项目根目录 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`；需要历史时再窄读 `PROJECT_HISTORY.md`。检查当前 `session_id` 的 projection，确认进行中步骤和是否存在 `UI_SYNC_BLOCKED`。交接不替代原任务的执行授权。
2. **抽取任务事实**：按 [handoff-packet-contract.md](references/handoff-packet-contract.md) 填写目标、范围、已完成、进行中、下一步、阻断、验证、稳定决策和新任务启动说明。每个进行中项必须注明当前已知中断点；未知的非幂等动作改写为“查询后暂停”。
3. **本地校验与脱敏**：先用 `scripts/validate_handoff_packet.py` 校验 JSON、字段白名单、大小、列表上限、时间格式和敏感信息。校验失败时不创建新任务，修正来源事实后只允许重新生成一次；仍失败则输出阻断事实。
4. **定位保存项目**：调用 `codex_app__list_projects`，用当前工作目录对应的保存项目做精确匹配。没有匹配、匹配多个或项目身份无法确认时停止，不凭项目名相似度猜测。读取 `isGitRepository` 仅用于记录事实；用户本流程要求同项目 `local`，因此创建时明确使用 `environment: { type: "local" }`。
5. **创建新任务**：调用 `codex_app__create_thread`，传入匹配的 `projectId`、`target.type: "project"`、`target.environment.type: "local"` 和脱敏交接包。启动提示必须要求新任务先做命中检查、读取四件套、校验交接包、核验进行中断点，再按 `next_steps` 逐项执行。
6. **等待创建结果**：创建结果包含可用 `threadId` 和 `hostId` 时，调用 `codex_app__wait_threads` 等待新任务首次完成或需要关注；只返回 `clientThreadId` 表示仍在设置中，禁止把它传给需要真实 `threadId` 的工具，也不得宣称新任务已经可执行。具体路由见 [codex-thread-routing.md](references/codex-thread-routing.md)。
7. **交接收口**：报告交接包校验结果、项目匹配结果、创建结果和等待结果。新任务 ready 后提示人工归档旧任务；创建失败、项目未匹配、交接包不安全或等待状态不明确时，保留旧任务，不做归档，不声称迁移完成。

## 新任务启动契约

新任务收到交接包后必须按以下顺序执行：

1. 输出本轮 `skill-hit-check-rules` 固定字段，并声明 `Obsidian` 判断和并行判断。
2. 读取父目录规则、`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`；按当前新 `session_id` 精确校验 projection，不跨会话复制或覆盖旧 projection。
3. 用标准库脚本再次校验交接包，核对项目实际文件、测试证据和进行中断点；与交接包冲突时以当前代码和当前项目文档为准，并报告冲突。
4. 建立或恢复当前新任务自己的 projection，成功持久化后立即调用 `update_plan`；UI 同步失败时进入 `UI_SYNC_BLOCKED`，禁止继续领域写入。
5. 只执行交接包 `next_steps` 中仍然必要的动作。已完成项不得重做；非幂等或状态未知的动作先只读查询并暂停等待人工确认。

## 停止条件

- 交接包包含敏感字段、缺少 `next_steps`、超过大小限制、来源事实不可核验或 JSON 校验失败。
- `list_projects` 无法证明当前工作目录对应唯一保存项目，或 `create_thread` 返回错误 / 结果不明确。
- 新任务仍处于 setup pending，或 `wait_threads` 返回错误；此时只能报告状态，不得伪报已接续。
- 当前存在未决的 Plan Mode 选择、真实阻断、`UI_SYNC_BLOCKED` 或未知非幂等操作；交接包必须保留这些状态，不能用“继续”覆盖。
- 用户明确要求停止时，立即停止自动继续和扩散性输出；不得顺手归档、提交或生成额外任务。

## 资源

- [handoff-packet-contract.md](references/handoff-packet-contract.md)：交接包字段、脱敏和校验契约。
- [codex-thread-routing.md](references/codex-thread-routing.md)：Codex App 项目匹配、local 创建、等待和新任务启动路由。
- `scripts/validate_handoff_packet.py`：只读校验交接包，不写项目文件。
