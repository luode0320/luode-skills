---
schema_version: 1
doc_id: TESTDOC-PMW-001
doc_type: test
source_ids:
  - BUG-PLAN-WAIT-20260726-001
  - CYCLE-PMW-01
  - TASK-PMW-03
  - TASK-PMW-04
  - TEST-PMW-001
  - TEST-PMW-002
  - TEST-PMW-003
  - TEST-PMW-004
  - TEST-PMW-005
  - TEST-PMW-006
  - TEST-PMW-007
  - TEST-PMW-008
  - TEST-PMW-009
  - TEST-PMW-010
  - TEST-PMW-011
  - TEST-PMW-012
  - TEST-PMW-013
status: in_progress
version: v1.0
current_slice: TEST-PMW-001..013
updated_at: 2026-07-26 04:52:00
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: functional_validation
    applicability: limited
    reason: 本地状态模型和规则文本已验证，真实 Desktop 选择框链路仍待执行。
    basis: AC-PMW-005、TEST-PMW-013。
    required_by_source: true
    required_now: true
    completed_validation:
      - 本地 Python 标准库行为回归 10/10
      - 规则、AST、YAML、UTF-8 和文档 profile 检查
    substitute_validation:
      - 状态机和总结消费方行为模型
    manual_follow_up: 真实宿主跨越两个以上空答案周期后，在当前活动选择框提交完整选择。
    pass_standard: 每次空答案立即重发同一选择框，等待期间无总结，最终选择后才恢复计划。
  - stage: review
    applicability: applicable
    reason: 本测试资产刚完成缺口修正，需要实现审查和当前改动总审查记录。
    basis: REVIEW-PMW-001、REVIEW-PMW-002。
    required_by_source: true
    required_now: true
    completed_validation:
      - REVIEW-PMW-001
      - REVIEW-PMW-002
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: 无 P0/P1，测试模型不允许错误实现假通过。
  - stage: browser_integration
    applicability: limited
    reason: 测试目标包含用户可见选择框，但当前没有真实 Desktop 回放证据。
    basis: TEST-PMW-013。
    required_by_source: true
    required_now: true
    completed_validation: []
    substitute_validation:
      - 本地行为状态机回归
    manual_follow_up: 更新后的 Plan Mode 宿主中执行两个以上空答案周期和最终选择恢复。
    pass_standard: 无并存选择框、无提前总结、用户选择后计划恢复。
  - stage: third_party
    applicability: not_applicable
    reason: 测试只使用本地 Python 标准库和仓库 fixture。
    basis: 本轮不连接数据库、缓存、消息队列、HTTP/RPC 上游或第三方接口。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---

# Plan Mode 选择框永久等待回归

结论：本地回归已覆盖永久等待、空返回重发、部分答案、停止终态和总结消费闸门；影响：规则层错误实现会在测试中被拒绝；范围：Plan Mode 决策与总结消费的本地行为模型；非范围：Desktop 产品源码、数据库和外部服务；变化：新增 null/缺失答案、单活动框、推荐标记、陈旧终态和历史回放断言；完成标准：脚本十项用例全部通过且测试资产可追溯；术语说明：空返回是宿主没有交付用户选择，不代表取消或授权；验证状态：本地自动回归通过，真实 Desktop 待人工确认。本测试任务验证 `BUG-PLAN-WAIT-20260726-001` 的行为闭环：用户未选择时保持 `WAITING_DECISION`；宿主返回空答案时立即重发同一选择框；连续重发没有次数或时间上限；只有完整选择、明确代选、明确停止或不可恢复工具故障才离开等待状态。测试同时验证最终消费方拒绝冻结集合内的 `commentary`、`limited_plan`、`pending_summary`、`proposed_plan`、`final`、`summary`、`final_answer`、`task_complete`、`result_and_conclusion` 及中文“结果与结论”。

## 文档信息

- 来源 Bug：`BUG-PLAN-WAIT-20260726-001`
- 测试轮次：`2026-07-26_040607`
- 图片资产决策：`N/A`；原因：测试只交付文本、fixture 和脚本；证据：本 README 无图片引用。
- 测试状态：自动回归已完成；真实 Desktop 仍是单独人工验证入口。

## 测试资产

- 真实测试程序：`doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py`
- 脱敏历史轨迹：`doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/fixtures/historical_empty_then_summary.json`
- 说明文件：本 `README.md`
- 路径约束：程序与 fixture 均位于 ASCII 目录；不写入生产代码，不连接数据库、缓存、消息队列或外部服务。

## 执行命令

```powershell
python -B doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py
```

## 覆盖与断言

| 用例 | 关键断言 |
| --- | --- |
| `autoResolutionMs` 负例 | 决策载荷完全省略该字段；`60000`、`null`、`0` 均拒绝 |
| 空答案循环 | 连续 2、10、100 次空答案都立即重发并保持 `WAITING_DECISION`；`null`、空对象和缺失 `answers` 同样重发 |
| 载荷冻结 | 重发保留问题 ID、选项、推荐标记、文案和顺序 |
| 部分答案 | 已答项保留，只重发剩余问题 |
| 延迟选择 | 经过 100 次空答案后完整选择才进入 `DECISION_RESOLVED` |
| 明确授权/停止 | 仅明确“按推荐”可代选；明确停止后不再重发 |
| 工具故障 | 进入 `HOST_BLOCKED`，不得输出总结 |
| 总结闸门 | 未决状态拒绝 `commentary`、`limited_plan`、`pending_summary`、`proposed_plan`、`final`、`summary`、`final_answer`、`task_complete`、`result_and_conclusion` 及中文“结果与结论”，且不写入可见输出 |
| 历史违规轨迹 | 回放“空答案 -> 结果与结论”时消费方明确返回拒绝 |
| 规则文本 | Owner、总结消费方和 Agent 提示共同包含稳定契约 ID |

## 环境与结论口径

- 环境：纯本地 Python 标准库；数据库和远程服务未连接（原因：本测试只验证本地状态模型；证据：执行命令未包含外部服务配置）。
- 通过标准：脚本所有用例输出 `PASS`，最终输出 `plan-mode-wait-loop: PASS`。
- 失败标准：任意空答案不重发、重发丢失问题、等待状态允许总结、负例未拒绝或规则文本缺少契约 ID。
- 本地回归通过不等于真实 Desktop 视觉验证通过；本线程的 `computer-use` 安全规则禁止自动化 Codex Desktop/扩展，无法代替用户完成 `TEST-PMW-013`，因此按 `LIMITED/HOST_BLOCKED` 保留人工重验入口。

## 完成标准

自动测试完成标准为十项用例全部输出 `PASS`，覆盖 2、10、100 次空答案、null/缺失答案、部分答案、延迟选择、授权、停止、故障、总结闸门和历史负例；真实交互完成标准为跨越两个以上宿主空答案周期后用户选择仍能恢复计划。

## 验收结论

本地测试资产验收通过；真实 Desktop 验收受限，未取得宿主回放证据前不升级为整体修复通过。

## 验证结论

本轮执行结果：`plan-mode-wait-loop: PASS (10 cases)`；两个相关 Skill quick_validate、八份关联文档/审查/验收 profile、AST、YAML、UTF-8 和 `git diff --check` 均通过。WSL Python 缺 PyYAML，仅影响 Skill 校验入口，已用本机 Windows Python 复验；未连接任何服务。

## 追踪附录

`BUG-PLAN-WAIT-20260726-001` → `CYCLE-PMW-01` → `TASK-PMW-03/04` → `TEST-PMW-001..013` → 本 README 与 `test_plan_mode_wait_loop.py`；真实宿主证据由 `TEST-PMW-013` 承接。
