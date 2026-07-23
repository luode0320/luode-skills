# 边界规则

## 与 `history-recall-rules` 的边界

- `recent-context-bootstrap-rules` 是新会话的轻量预热，或压缩恢复确认缺少近期事实后的条件补充。
- `history-recall-rules` 是用户明确要求回忆过去方案、修复或决策时的深度历史回溯。
- 如果已明确要查“以前怎么做过”，转交 `history-recall-rules`，不扩大近期预热范围。

## 与 `project-timeline-rules` 的边界

- 这里只看近 3 天和共享契约记录的缺失项，不做长期项目阶段演进报告。
- 用户要求完整历程或关键决策时间线时转交 `project-timeline-rules`。

## 与 `project-design-doc-rules` 的边界

- 根目录项目设计类文档最多是弱参考源，不能压过当前代码、工作区和最近变更。
- 不负责判断、同步、合并或补建项目设计文档；相关请求转交 `project-design-doc-rules`。

## 与主域 skill 的边界

- 不负责需求、Bug、编码、测试、审查、验收或交付本体。
- 预热完成后必须让路给真正主域，且不得恢复或扩大历史授权。
- 压缩恢复条件调用时只补 `context-recovery-contract` 已记录的缺失项，不重复完整恢复。

## 不应触发的场景

- 用户只是闲聊、问通用知识或任务与当前项目无关。
- 当前会话已有足够上下文。
- 压缩恢复状态为 `sufficient` 或 `uncertain`。
- 用户明确暂停、停止、终止或不要继续。
