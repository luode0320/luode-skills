# 需求接入边界与样例

## 应继续留在需求接入的情况

- 只是入口信息零散，需要先整理目标、输入输出和背景。
- 任务刚进入研发，还没开始讨论实现边界和验收标准。

## 应转交相邻 skill 的情况

- 信息不全且缺字段、缺流程、缺规则：转 `requirement-gap-rules`。
- 范围、兼容性、旧逻辑影响不清：转 `requirement-boundary-rules`。
- 需求过大、跨多个模块或多个实施阶段：转 `requirement-splitting-rules`。
- 编码中出现新条件或优先级变化：转 `requirement-change-rules`。
- 需要把“做到什么算完成”写成可验证标准：转 `acceptance-criteria-rules`。
- 如果本质是历史行为错误或故障：转 Bug 域。
