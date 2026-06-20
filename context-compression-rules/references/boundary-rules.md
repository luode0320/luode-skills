# 边界规则

## 与 `recent-context-bootstrap-rules` 的关系

- 本 skill 不直接替代最近上下文预热。
- 触发压缩时，必须先联动 `recent-context-bootstrap-rules`。
- 预热负责补上下文来源，本 skill 负责压缩和降噪。

## 与项目 `AGENTS.md` / `project-agents-bootstrap` 的关系

- 压缩后恢复最近上下文不等于恢复仓库级硬规则。
- 触发压缩时，必须重新读取当前项目根目录 `AGENTS.md`，再继续主任务。
- 若项目根目录缺失 `AGENTS.md`，或读取后发现规则不完整，应转交 `project-agents-bootstrap` 补齐后再继续。
- 仓库级 `AGENTS.md` 规则优先级高于压缩摘要中的口头记忆，冲突时以重新读取后的 `AGENTS.md` 为准。

## 与 `history-recall-rules` 的关系

- 当前需求是“压缩当前会话”时，优先本 skill。
- 当前需求是“回忆更久以前怎么做的”时，转交 `history-recall-rules`。

## 与 `project-timeline-rules` 的关系

- 本 skill 只处理当前执行上下文，不输出长期项目历程。
- 需要完整时间线时，转交 `project-timeline-rules`。

## 与主域 skill 的关系

- 本 skill 不执行需求、Bug、编码、测试或交付本体逻辑。
- 压缩完成后立即让路，由当前主域 skill 接管执行。
