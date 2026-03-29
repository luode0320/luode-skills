# 冲突裁决样例

## 用途

用于处理多 skill 同时触发、重复命中、顺序错位或规则冲突的场景。

## 裁决优先级

1. 阶段优先
2. 位点次之
3. 类型兜底

## 样例

### 样例 1：需求未澄清就要求直接写代码

- 当前信号：用户提出新接口，但字段、鉴权和返回结构都不完整，同时要求直接开始实现。
- 应命中：`team-development-rules` + 需求域 skill。
- 裁决：先进入 `requirement-gap-rules` 和 `requirement-boundary-rules`，不允许直接进入编码。
- 原因：阶段优先，需求前置条件未满足。

### 样例 2：新增接口同时命中多个位点 skill

- 当前信号：新增接口，同时涉及请求参数、响应结构、认证头、日志和异常映射。
- 应命中：`api-endpoint-rules`、`api-request-rules`、`api-response-rules`、`request-header-rules`、`logging-trace-rules`、`error-handling-rules`。
- 裁决：总控层只确认主位点是接口主干，小 skill 并行生效；总控层随后退出。
- 原因：不存在阶段争议，也不存在互斥冲突。

### 样例 3：代码已写完但用户要求跳过编码审查直接测

- 当前信号：实现已完成，但还没有做语法检查、清理未使用引用和调试残留。
- 应命中：`team-development-rules` + 编码审查域。
- 裁决：阻断进入测试域，先进入 `implementation-review-rules`、`syntax-check-review-rules`、`cleanup-format-review-rules`。
- 原因：编码审查阶段未完成，不能跳测试前自审。

### 样例 4：验收不通过，但原因可能是需求理解偏差也可能是代码缺陷

- 当前信号：结果不符合预期，但尚不确定是需求理解偏差还是实现错误。
- 应命中：`team-development-rules`。
- 裁决：先做归因判定；如果是理解偏差，回需求域；如果是实现错误，转 Bug 域。
- 原因：需求域与 Bug 域边界不清，需要总控层先分流。

### 样例 5：前端页面任务同时像视觉设计又像组件拆分

- 当前信号：用户要做一个新页面，同时既强调首屏视觉表达，又要求把组件拆干净、状态边界清晰。
- 应命中：`frontend-ui-visual-rules` + `frontend-component-rules`。
- 裁决：如果当前先解决的是页面视觉方向、信息层级和构图节奏，先由 `frontend-ui-visual-rules` 主导；一旦进入组件拆分、props 设计、状态归属和复用边界，再由 `frontend-component-rules` 接手工程细节。
- 原因：两者可以串行配合，但不能互相替代；页面视觉规则不应抢组件工程规则的职责。

### 样例 6：运行时诊断同时命中 debug 日志和断言诊断

- 当前信号：静态定位已经卡住，团队同时想加 debug 日志、加断言、打断点。
- 应命中：`bug-runtime-debug-rules` + `bug-debug-log-rules` / `bug-assertion-diagnostic-rules`。
- 裁决：先由 `bug-runtime-debug-rules` 判断本轮诊断目标和最小手段；只有在“日志是最小证据路径”时再进入 `bug-debug-log-rules`，只有在“需要快速暴露不变量破坏”时再进入 `bug-assertion-diagnostic-rules`。
- 原因：`bug-runtime-debug-rules` 是诊断入口裁决层；日志和断言是子手段，不应一上来并行乱用。

### 样例 7：测试阶段同时命中策略、功能验证和回归验证

- 当前信号：代码审查刚通过，团队既想先验证当前功能，又担心共享逻辑被带坏，还没决定先测什么。
- 应命中：`test-strategy-rules`、`functional-validation-rules`、`test-regression-rules`。
- 裁决：先进入 `test-strategy-rules` 确定优先级；当前变更正确性由 `functional-validation-rules` 先收口；确认当前功能没问题后，再由 `test-regression-rules` 处理旧能力兼容性。
- 原因：先定策略，再验当前功能，最后做回归；否则容易把三层职责混成一轮模糊测试。

### 样例 8：用户一边提新需求，一边问“之前是不是做过类似功能”

- 当前信号：用户提出一个新需求，同时要求先回忆以前有没有做过类似页面、接口或流程。
- 应命中：`history-recall-rules` + 需求域 skill。
- 裁决：先由 `history-recall-rules` 补回历史方案和历史结论；历史补齐后回到 `requirement-intake-rules` / `requirement-gap-rules` 继续做当前需求澄清。
- 原因：历史回忆只是辅助信息，不代替当前需求分析；先补上下文，再继续需求主流程。

### 样例 9：用户要求“写项目历程报告”，但当前也需要交付说明

- 当前信号：用户既想看整个项目演进历史，又想知道这次交付做了什么。
- 应命中：`project-timeline-rules` + `delivery-summary-rules`。
- 裁决：如果问题重点是长期历史、关键决策、阶段演进，先由 `project-timeline-rules` 主导；如果问题重点是当前这一轮改动、验证和风险，再由 `delivery-summary-rules` 输出本次交付摘要。
- 原因：时间尺度不同；项目时间线报告不应替代当前交付说明，当前交付说明也不能冒充完整项目史。

### 样例 10：需求已稳定，但用户要求直接开写复杂功能

- 当前信号：需求文档、边界结论和验收标准都已经基本齐，但当前功能仍涉及多个模块、多个文件和多步验证，用户想直接开始编码。
- 应命中：`implementation-plan-rules`。
- 裁决：先进入 `implementation-plan-rules`，把当前优先闭环的文件落点、任务顺序和验证点拆清后，再进入编码基线域和代码位点域。
- 原因：阶段上仍处于“编码前计划”而不是“直接实现”；此时缺的是实施计划，不是需求拆分或测试执行。

### 样例 11：需求拆分与实施计划同时被提起

- 当前信号：一个大需求既包含多个独立子系统，又要求顺便把开发步骤一起列出来。
- 应命中：`requirement-splitting-rules` + `implementation-plan-rules`。
- 裁决：先由 `requirement-splitting-rules` 拆出子系统 / 子项边界，只保留当前优先闭环；边界稳定后，再由 `implementation-plan-rules` 继续细化该优先子项的文件落点和执行步骤。
- 原因：拆分先回答“先做哪一块”；实施计划再回答“这块具体怎么落地”，两者不能倒置。

### 样例 12：当前功能验证需要真实浏览器操作

- 当前信号：用户要求验证一个前端页面是否能正常打开、点击、输入、提交并截图留证。
- 应命中：`functional-validation-rules` + `agent-browser`。
- 裁决：由 `agent-browser` 负责真实浏览器执行、页面交互和截图取证；由 `functional-validation-rules` 负责判断当前需求是否通过、结论如何归档。
- 原因：一个负责执行手段，一个负责验证结论，二者并行配合但不能互相替代。
