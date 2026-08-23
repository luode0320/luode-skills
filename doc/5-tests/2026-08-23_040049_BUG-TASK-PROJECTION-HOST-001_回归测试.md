# 测试主文档：任务投影跨宿主适配回归

- 来源对象：`BUG-TASK-PROJECTION-HOST-001`
- 关联实施：`doc/3-实施/2026-08-23_040049_BUG-TASK-PROJECTION-HOST-001_实施总览.md`、实施周期01
- 测试时间：2026-08-23
- 结论：**全部通过**（73/73 用例 0 失败；skill 校验通过；语义 Grep 无绝对化残留）

## 1. 测试目的

验证任务投影跨宿主适配改动不破坏既有契约，并确认新能力生效：

1. `ensure-start` 缺 `trigger` 默认补 `start`；显式 `timeout` 仍拒绝；`synthesize` 保持严格必填。
2. 会话解析支持 WorkBuddy 回退；多来源冲突拒绝；全缺失失败关闭。
3. 规则层与上层联动文档口径统一（分级阻断语义）。

## 2. 测试命令与结果

| 测试点 | 命令 | 结果 |
| --- | --- | --- |
| TEST-1/2/3 全量单元测试 | `python -X utf8 -B test/task-plan-rehydration-rules/task_plan_projection_test.py` | `Ran 73 tests in 5.271s` / `OK`，退出码 0 |
| TEST-4 skill 结构校验 | `python -B .system/skill-creator/scripts/quick_validate.py task-plan-rehydration-rules` | `Skill is valid!`，退出码 0 |
| TEST-4 语义 Grep | `Grep "禁止继续领域写入\|UI_SYNC_BLOCKED\|update_plan.*不可用\|update_plan.*失败" --glob "**/*.md"` | 规则文件全部为分级表述；AGENTS.md/CLAUDE.md 命中行为 Goal 降级语义（非绝对化）；历史文档（doc/4-bugs、doc/3-实施）为记录旧行为，不适用 |

## 3. 被测文件与样本

- 被测源码：`task-plan-rehydration-rules/scripts/task_plan_projection.py`（`_resolve_workbuddy_session_id`、`resolve_session_id`、`ensure_start_projection`）
- 测试代码：`test/task-plan-rehydration-rules/task_plan_projection_test.py`（新增 `test_ensure_start_context_defaults_trigger_to_start_but_timeout_rejected`、`test_session_resolution_falls_back_to_workbuddy_and_rejects_conflicts`）
- 样本：`_sample` fixture、mock 环境变量组合（缺 trigger 上下文 / timeout 上下文 / WorkBuddy 来源 / 冲突来源 / 全缺失）

## 4. 关键断言

- 缺 `trigger` 合成上下文经 `ensure-start` → `action=created` 且投影 `state=active`。
- `trigger=timeout` 经 `ensure-start` → `ProjectionContractError`。
- `synthesize_projection` 缺 `trigger` → `ProjectionContractError`（严格必填保留）。
- `WORKBUDDY_SESSION_ID` / `CODEBUDDY_MCP_CONFIG` 唯一 `X-WorkBuddy-Session-Id` → 回退成功。
- 显式值与 WorkBuddy 来源不一致 → `ProjectionContractError`。
- 全缺失且 `required=True` → 失败关闭；`required=False` → `None`。

## 5. 证据定位

- 单元测试输出：本表「测试命令与结果」。
- 文档校验：`doc/5-tests/2026-08-23_040049_BUG-TASK-PROJECTION-HOST-001_实施总览.validate.json`、`doc/5-tests/2026-08-23_040049_BUG-TASK-PROJECTION-HOST-001_实施周期01.validate.json`（均 `valid: true`）。
- 风格回归：`doc/6-review/2026-08-23_114924_BUG-TASK-PROJECTION-HOST-001_6-review.md`（`STYLE: PASS`）。

## 6. 追踪

- `SRC: BUG-TASK-PROJECTION-HOST-001` → `TEST-1/2/3/4` → 本文档。
