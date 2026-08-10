---
schema_version: 1
doc_id: "TEST-PMO-20260810-001"
doc_type: "test"
source_ids:
  - "BUG-PLAN-OPTION-20260810-001"
  - "AC-PMO-001..010"
status: "confirmed"
version: "v1.0"
current_slice: "AC-PMO-001"
updated_at: "2026-08-10 23:55:00"
reader_level: "business_general"
writing_style: "plain_chinese"
appendix_policy: "preserve_existing_or_one_terminal_appendix"
---

# 测试说明：Plan Mode 选择框空白无效选项修复

结论：本测试说明确认选择框载荷质量前置校验的测试范围与结果。影响：Plan Mode 用户可见有效选择框。范围：新增测试文件覆盖 10 项验收标准。非范围：宿主 UI 渲染。变化：新增测试验证无效载荷被拒绝。完成标准：全部测试通过。术语说明：载荷质量指选项的非空、去重、拒绝占位。验证状态：已完成，测试全部通过。图片资产决策：N/A + 原因 + 证据。本测试说明只涉及文本协议和测试结果，无需位图。

## 文档信息

| 项目 | 内容 |
| --- | --- |
| 来源对象 | BUG-PLAN-OPTION-20260810-001 |
| 实施总览 | 实施总览 |
| 实施周期 | CYCLE-PMO-01 |
| 测试状态 | 已完成 |

## 完成标准

| 验收 ID | 条件 | 测试覆盖 | 状态 |
| --- | --- | --- | --- |
| AC-PMO-001 | 合法中文载荷通过校验 | test_valid_chinese_payload | PASS |
| AC-PMO-002 | 空问题字段被拒绝 | test_empty_question_field | PASS |
| AC-PMO-003 | 少于 2 个选项被拒绝 | test_less_than_two_options | PASS |
| AC-PMO-004 | 多于 3 个选项被拒绝 | test_more_than_three_options | PASS |
| AC-PMO-005 | 空标签被拒绝 | test_empty_label | PASS |
| AC-PMO-006 | 空描述被拒绝 | test_empty_description | PASS |
| AC-PMO-007 | 规范化后重复标签被拒绝 | test_duplicate_labels | PASS |
| AC-PMO-008 | 重复描述被拒绝 | test_duplicate_descriptions | PASS |
| AC-PMO-009 | 纯占位标签被拒绝 | test_placeholder_labels | PASS |
| AC-PMO-010 | 无效草稿不调用工具 | test_invalid_draft_no_tool_call | PASS |

## 测试文件

### 测试文件

- `test/implementation-planning-rules/plan_mode_option_payload_test.py`：选择框载荷质量前置校验测试

## 测试内容

10 项正负行为测试：

1. `test_valid_chinese_payload` - 合法中文载荷通过校验（AC-PMO-001）
2. `test_empty_question_field` - 空问题字段被拒绝（AC-PMO-002）
3. `test_less_than_two_options` - 少于 2 个选项被拒绝（AC-PMO-003）
4. `test_more_than_three_options` - 多于 3 个选项被拒绝（AC-PMO-004）
5. `test_empty_label` - 空标签被拒绝（AC-PMO-005）
6. `test_empty_description` - 空描述被拒绝（AC-PMO-006）
7. `test_duplicate_labels` - 规范化后重复标签被拒绝（AC-PMO-007）
8. `test_duplicate_descriptions` - 重复描述被拒绝（AC-PMO-008）
9. `test_placeholder_labels` - 纯占位标签被拒绝（AC-PMO-009）
10. `test_invalid_draft_no_tool_call` - 无效草稿不调用工具（AC-PMO-010）

## 执行命令

```powershell
python -X utf8 -B test/implementation-planning-rules/plan_mode_option_payload_test.py
```

## 测试结果

2026-08-10 执行结果：PASS (10 cases)

## 回归测试

```powershell
python -X utf8 -B test/implementation-planning-rules/plan_output_contract_test.py
python -X utf8 -B doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py
python -X utf8 -B .system/skill-creator/scripts/quick_validate.py implementation-planning-rules
git diff --check
```

## 回归结果

- plan-mode-option-payload: PASS (10 cases)
- plan_output_contract_test: OK (15 tests)
- plan-mode-wait-loop: PASS (10 cases)
- Skill 校验：PASS
- git diff --check：无错误
