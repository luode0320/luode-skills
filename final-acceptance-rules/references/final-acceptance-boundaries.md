# 最终验收边界说明

## 和相邻 skill 的边界

- 前置“做到什么算完成”：转 `acceptance-criteria-rules`。
- 实施步骤、周期和落点：转 `implementation-planning-rules`。
- 测试执行与验证证据：转 `functional-validation-rules`、`test-regression-rules` 等测试域 skill。
- 审核结论：转 `implementation-review-rules` 或 `project-change-review-rules`。

## 使用提醒

- 最终验收负责“是否放行”，不是“如何实现”。
- 测试和审核的适用性、受限状态和正式放行条件统一按 `review_acceptance_gates` 判断；不适用不阻断，受限可继续但不能正式放行，明确必需且无替代验证才阻断。
- 若来源对象变更影响验收标准、实施文档或测试结论，原最终验收必须失效并待重验。
