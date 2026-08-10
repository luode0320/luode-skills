---
schema_version: 1
doc_id: "BUGDOC-PMO-001"
doc_type: "bug"
source_ids:
  - "BUG-PLAN-OPTION-20260810-001"
  - "SRC-PMO-001"
status: "confirmed"
version: "v1.0"
current_slice: "RULE-PMO-001"
updated_at: "2026-08-10 23:45:00"
reader_level: "business_general"
writing_style: "plain_chinese"
appendix_policy: "preserve_existing_or_one_terminal_appendix"
unresolved_decisions: []
review_acceptance_gates:
  - stage: "review"
    applicability: "applicable"
    reason: "选择框载荷质量校验会同时影响规划 Owner 与 plan-output-gate，必须审查职责边界。"
    basis: "RULE-PMO-001..007"
    required_by_source: true
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: "实施后按 TASK-PMO-03 的当前改动审查入口复核。"
    pass_standard: "调用前校验、无效载荷重建、合法载荷才进入 WAITING_DECISION，且测试覆盖所有正负边界。"
  - stage: "acceptance"
    applicability: "limited"
    reason: "本 Bug 入口已由会话时间线确认；修复后的真实 Desktop 链路尚未执行。"
    basis: "SRC-PMO-001、AC-PMO-001..007"
    required_by_source: true
    required_now: true
    completed_validation: []
    substitute_validation: ["自动行为回归覆盖空标签、空描述、重复标签、占位标签和合法载荷。"]
    manual_follow_up: "修复后的 Plan Mode 环境中，选择框应始终展示有效内容，空白或无效选择框不再出现。"
    pass_standard: "自动回归全通过，且真实 Desktop 中每次选择框都展示有效选项。"
---

# Bug：Plan Mode 选择框空白与无效选项

结论：在 Plan Mode 使用 `request_user_input` 时，偶发出现选项框为空、占位内容、重复或无效选择的情况；影响：用户无法看到有效选项，计划推进受阻；范围：本记录确认 Plan Mode 选择框载荷质量的前置校验规则；非范围：Codex Desktop 宿主 UI 渲染问题、非 Plan Mode 行为、Goal 和任务投影；变化：修复后无效载荷在调用前被阻断，重建合法后才进入选择框；完成标准：每个选择框的选项都有实际可选的文字和决策差异，不再出现空白或占位选项；术语说明：载荷质量指选项的 label、description 非空、去重、拒绝占位标签；验证状态：已通过规则回放复现空选项和占位选项被当前验证器放行的漏洞。 图片资产决策：N/A + 原因 + 证据。本 Bug 只处理文本协议、状态逻辑和测试代码，无需位图。

## 文档信息

| 项目 | 内容 |
| --- | --- |
| 来源对象 | `BUG-PLAN-OPTION-20260810-001` |
| 实施总览 | [doc/3-实施/2026-08-10_233457_PlanMode选择框空白无效选项_实施总览.md](../../3-实施/2026-08-10_233457_PlanMode选择框空白无效选项_实施总览.md) |
| 实施周期 | [CYCLE-PMO-01](../../3-实施/2026-08-10_233457_PlanMode选择框空白无效选项_实施周期01_选择项载荷前置校验闭环.md) |
| 6-review | [6-review 记录](../../6-review/2026-08-10_233457_Bug-PlanMode选择框空白无效选项_6-review.md) |

## 问题现象

在 Plan Mode 需要用户选择时，偶发出现以下情况：

1. 两个选项都为空或只显示占位内容（如"选项1"、"选项2"）
2. 两个选项虽然都有文字，但实际相同或没有真实决策差异
3. 选项标签或描述为空，显示为空白选择框
4. 问题（question）字段为空，用户无法看到问题内容

## 根因分析

当前规则只约束"用户没有选择后的永久等待和重发"，没有在调用 `request_user_input` 前严格验证选择框载荷质量。

具体缺口：
- `plan-question-coverage.md` 只要求"2-4 个互斥选项"，没有定义 `question/header/id` 非空、`options[].label/description` 非空、去重和拒绝占位标签
- 当前 `validate_decision_call` 只检查 `autoResolutionMs` 不存在和 `questions` 非空
- 历史行为模型使用字符串数组构造选项，不是 `{label, description}` 结构

## 完成标准

| ID | 条件 | 证据 |
| --- | --- | --- |
| AC-PMO-001 | 合法中文载荷通过校验 | 测试用例 1 |
| AC-PMO-002 | 空问题字段被拒绝 | 测试用例 2 |
| AC-PMO-003 | 少于 2 个选项被拒绝 | 测试用例 3 |
| AC-PMO-004 | 多于 3 个选项被拒绝 | 测试用例 4 |
| AC-PMO-005 | 空标签被拒绝 | 测试用例 5 |
| AC-PMO-006 | 空描述被拒绝 | 测试用例 6 |
| AC-PMO-007 | 去重后重复标签被拒绝 | 测试用例 7 |
| AC-PMO-008 | 重复结果描述被拒绝 | 测试用例 8 |
| AC-PMO-009 | 占位标签被拒绝 | 测试用例 9 |
| AC-PMO-010 | 无效草稿不调用工具，重建合法后只调用一次 | 测试用例 10 |

## 修复方案

增加调用前载荷校验门禁：
1. 每次调用 `request_user_input` 前校验候选载荷
2. 首次无效时在内部重建（重写选项）
3. 仍无效时执行一次只读侦察并重新生成
4. 再次无法形成至少两个有效选项时，退出多选流程，提出一个具体开放式问题
5. 无效载荷不得调用工具，也不得进入 `WAITING_DECISION`
6. 合法载荷真实调用工具后，继续沿用既有永久等待和空答案重发规则
7. 若合法载荷仍被客户端渲染为空，归为宿主渲染问题，不用同一载荷无限重试

## 图片资产决策\n\nN/A + 原因 + 证据。本 Bug 只处理文本协议、状态逻辑和测试代码，流程关系使用 Mermaid 足以表达。证据：Mermaid 流程图可表达校验流程，无需位图。

## 决策维度覆盖表

| 维度 | 状态 | 结论 / 依据 |
| --- | --- | --- |
| 架构 | 已确定 | 在现有 `plan-question-coverage.md` 和 `validate_decision_call` 基础上增加前置校验层，不引入新架构 |
| 代码落点 | 已确定 | `implementation-planning-rules/references/plan-question-coverage.md` + `plan-output-gate.md` |
| 实现方式 | 已确定 | 增加 `validate_option_payload` 函数，按协议契约校验载荷 |
| 命名 | 已确定 | 沿用现有 `validate_decision_call` 命名风格 |
| 注释 | 已确定 | 中文注释，按仓库约定 |
| 错误处理 | 已确定 | 校验失败抛 `PayloadViolation`，内部重建失败转开放式问题 |
| 测试策略 | 已确定 | 新增 `test/implementation-planning-rules/plan_mode_option_payload_test.py`，10 项正负测试 |
| 依赖与库 | 已确定 | 纯 Python 标准库，不引入第三方 |
| 图片资产 | N/A | 本 Bug 不涉及位图 |
