# Context Recovery Contract

**用途**

- 供 `context-compression-rules` 与 `recent-context-bootstrap-rules` 共享恢复顺序、事实充分性判定和停止边界。
- 压缩恢复是主入口；近期预热只是确认缺少近期事实后的条件补充，不是压缩后的无条件步骤。

**固定恢复顺序**

1. 重新读取当前平台规则文件：Codex 使用 `AGENTS.md`，Claude Code 使用 `CLAUDE.md`。
2. 读取 `PROJECT_CURRENT.md` 恢复当前目标、范围、状态、已完成、待办、阻断、验证和下一执行点。
3. 当前状态包含任务投影托管区时，调用 `task-plan-rehydration-rules` 校验；有效 `active` 投影真实调用 `update_plan`，`inactive`、`invalid`、`tool-unavailable` 分别记录，进行中步骤先核验中断点。
4. 读取 `PROJECT_MEMORY.md` 恢复稳定规则与关键决策；`PROJECT_HISTORY.md` 默认不读，只有明确历史追问或当前状态真实不足时才窄检索。
5. 对照当前用户消息、压缩摘要和工作区事实，恢复当前阶段、主域 Owner、必命中 Skill、写集和最大推进边界。
6. 恢复编码许可：仅有明确授权证据时为 `confirmed`；明确未授权为 `not-confirmed`；无法确认时为 `unknown`。任务投影的 UI 重建不改变该许可。
7. 判断近期事实状态，再决定是否调用 `recent-context-bootstrap-rules`。

**近期事实三态**

- `sufficient`：当前消息、压缩摘要、项目当前状态和工作区事实足以确定下一动作、目标文件、验证方式与停止边界；不得调用近期预热。
- `missing`：继续任务所必需的最近改动、最近结论、验证证据或下一执行点明确缺失；允许条件调用近期预热。
- `uncertain`：来源存在冲突或尚未完成核验；先核验现有来源，不得因为不确定就直接调用近期预热，也不得继续高风险动作。

**条件调用协议**

- 调用前记录 `recent_context_state=missing` 和缺失项。
- `recent-context-bootstrap-rules` 只补缺失项相关的近 3 天材料与最小 Skill 索引，不重新执行完整压缩恢复。
- 返回后记录来源、补齐项、仍缺项和主域交接点；未补齐时保持阻断，不以猜测填空。

**保护与停止语义**

- 当前代码和工作区事实优先于压缩摘要；当前用户消息优先于历史授权。
- 不删除或弱化用户习惯、安全、授权、local 环境、清理、回滚、输出和证据要求。
- 编码许可非 `confirmed` 时禁止开始或继续编码。
- 用户明确暂停、停止、终止或不要继续时，不得借恢复流程重启任务，只允许最小收口。
- 恢复完成后立即让路给当前主域 Skill，不在恢复层执行需求、Bug、编码、测试或交付本体。

**最小输出状态**

- `rules_reload:<complete/blocked>`
- `project_context:<complete/partial/blocked>`
- `task_projection:<rehydrated/inactive/invalid/tool-unavailable/absent>`
- `recent_context_state:<sufficient/missing/uncertain>`
- `recent_bootstrap:<invoked/not-invoked/blocked>`
- `implementation_permission:<confirmed/not-confirmed/unknown>`
- `handoff:<主域 Skill 或阻断原因>`
