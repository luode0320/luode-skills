# 组件工程自审清单

- 组件职责是否单一
- 当前拆分是否过粗或过细
- 状态是否放在最小合理归属层
- props 是否语义清楚且没有爆炸式增长
- events / emits 是否表达事实而不是命令
- 是否存在明显的 props 透传链
- hooks / composables 是否真的稳定复用
- 是否把强业务逻辑伪装成通用组件
- effect / watch / lifecycle 是否依赖清楚、清理完整
- 列表 key、条件渲染和状态切换是否稳定
- 是否和 `frontend-ui-visual-rules` 的职责边界保持清楚，没有把视觉问题和组件工程问题混在一起
