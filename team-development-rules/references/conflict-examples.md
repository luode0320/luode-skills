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
