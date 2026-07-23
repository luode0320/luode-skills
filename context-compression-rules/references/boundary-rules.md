# 边界规则

## 与 `recent-context-bootstrap-rules` 的关系

- `context-compression-rules` 负责压缩后的规则、项目状态、目标、范围和许可恢复。
- `recent-context-bootstrap-rules` 负责新会话预热，或在共享契约确认 `recent_context_state=missing` 后补充近 3 天事实。
- 发生压缩不再构成无条件调用近期预热的理由。
- 状态为 `sufficient` 时不得调用；状态为 `uncertain` 时先核验现有来源；只有 `missing` 才条件调用。

## 与项目 `AGENTS.md` / `project-rule-file-bootstrap-rules` 的关系

- 恢复最近上下文不等于恢复仓库级硬规则；压缩后必须重新读取当前平台规则文件。
- 规则文件缺失或损坏时转交 `project-rule-file-bootstrap-rules`，完成前禁止继续主任务。
- 重新读取的仓库规则与当前代码事实优先于压缩摘要中的旧口径。

## 与 `history-recall-rules` 的关系

- 恢复当前压缩会话时使用本 skill。
- 用户明确追问“以前、上次、当时怎么做”且当前项目状态不足时，转交 `history-recall-rules` 做窄范围历史回溯。
- 不得用近期预热代替深度历史回忆。

## 与 `project-timeline-rules` 的关系

- 本 skill 只恢复当前执行上下文，不输出长期项目历程。
- 需要完整时间线时转交 `project-timeline-rules`。

## 与主域 skill 的关系

- 本 skill 不执行需求、Bug、编码、测试、审查、验收或交付本体逻辑。
- 恢复完成后立即让路；编码许可非 `confirmed` 时只能交接阻断，不能继续编码。
- 用户明确停止或终止时，不得因恢复完成而自动重启任务。
