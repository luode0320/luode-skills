# 边界规则

## 与 `recent-context-bootstrap-rules` 的关系

- 本 skill 不直接替代最近上下文预热。
- 触发压缩时，必须先联动 `recent-context-bootstrap-rules`。
- 预热负责补上下文来源，本 skill 负责压缩和降噪。

## 与 `history-recall-rules` 的关系

- 当前需求是“压缩当前会话”时，优先本 skill。
- 当前需求是“回忆更久以前怎么做的”时，转交 `history-recall-rules`。

## 与 `project-timeline-rules` 的关系

- 本 skill 只处理当前执行上下文，不输出长期项目历程。
- 需要完整时间线时，转交 `project-timeline-rules`。

## 与主域 skill 的关系

- 本 skill 不执行需求、Bug、编码、测试或交付本体逻辑。
- 压缩完成后立即让路，由当前主域 skill 接管执行。
