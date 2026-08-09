---
schema_version: 1
doc_id: "TEST-PLAN-DETAIL-20260809"
doc_type: "test"
source_ids: ["REQ-PLAN-DETAIL-COMPLETE-002", "CYCLE-PD-02"]
status: "accepted"
version: "v1.0"
current_slice: "计划输出契约回归"
updated_at: "2026-08-09 19:02:00"
reader_level: "business_general"
writing_style: "plain_chinese"
appendix_policy: "preserve_existing_or_one_terminal_appendix"
---

# 计划输出契约真实测试

结论：本轮验证计划输出契约在模板、闸门、跨会话清单与外部引用 `EXT-*` 上的完整约束，活动测试入口 15 项全部通过。影响：正式计划将完整承载思考细节并支持新会话独立执行。范围：`implementation-planning-rules` 模板与契约、`test/implementation-planning-rules/` 测试资产。非范围：业务正确性、真实业务项目源码、外部服务和发布放行。变化：测试从历史位置迁至根 `test/`，并从 12 项扩展为 15 项。完成标准：15 项契约测试与 10 项等待模型回归全部通过。术语说明：`EXT-*` 是外部项目代码引用标识。验证状态：已通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联任务 | `TASK-PLAN-DETAIL-08` 至 `TASK-PLAN-DETAIL-10` |
| 测试环境 | local 工作树、Windows Python、临时目录 |
| 可执行测试 | `test/implementation-planning-rules/plan_output_contract_test.py` |
| 证据边界 | 仅记录脱敏命令和结果，不记录任何秘密原值 |

## 测试矩阵

| TEST | 入口 | 断言 | 失败预期 |
|---|---|---|---|
| `TEST-PD-09-01` | `plan_output_contract_test.py` | 15 项全 PASS | 任一断言失败 |
| `TEST-PD-09-02` | 测试内子进程等待模型 | `plan-mode-wait-loop: PASS (10 cases)` | 子进程退出码非 0 |
| `TEST-PD-10-01` | `validate_engineering_docs.py` 五档 | `valid: true` | 任一 profile 失败 |
| `TEST-PD-10-02` | `validate_engineering_docs.py --strict` 四档 | 全 PASS | 任一 profile 失败 |
| `TEST-PD-10-03` | 字典生成与 `git diff --check` | 退出码 0 | 任一步骤失败 |
| `TEST-PD-10-04` | 临时文件检查 | `.codex-plan-projection-input.json` 不存在 | 临时文件残留 |

## 任务证据台账

| 任务 | IMPL | TEST | STYLE |
|---|---|---|---|
| `TASK-PLAN-DETAIL-08` | `EVD-TASK-PLAN-DETAIL-08-IMPL-01` | `EVD-TASK-PLAN-DETAIL-08-TEST-01` | `EVD-TASK-PLAN-DETAIL-08-STYLE-01` |
| `TASK-PLAN-DETAIL-09` | `EVD-TASK-PLAN-DETAIL-09-IMPL-01` | `EVD-TASK-PLAN-DETAIL-09-TEST-01`、`EVD-TASK-PLAN-DETAIL-09-TEST-02` | `EVD-TASK-PLAN-DETAIL-09-STYLE-01` |
| `TASK-PLAN-DETAIL-10` | `EVD-TASK-PLAN-DETAIL-10-IMPL-01` | `EVD-TASK-PLAN-DETAIL-10-TEST-01`、`EVD-TASK-PLAN-DETAIL-10-TEST-02`、`EVD-TASK-PLAN-DETAIL-10-TEST-03`、`EVD-TASK-PLAN-DETAIL-10-TEST-04` | `EVD-TASK-PLAN-DETAIL-10-STYLE-01` |

## 真实测试命令

```powershell
python -X utf8 -B test/implementation-planning-rules/plan_output_contract_test.py
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile requirement --doc doc/2-需求/2026-08-09_190217_REQ-PLAN-DETAIL-COMPLETE-002_计划输出完整性与跨会话独立执行.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_overview --doc doc/3-实施/2026-08-09_190217_REQ-PLAN-DETAIL-COMPLETE-002_实施总览.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc doc/3-实施/2026-08-09_190217_REQ-PLAN-DETAIL-COMPLETE-002_实施周期01_模板闸门测试与收口.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile style_regression --doc doc/6-review/2026-08-09_190217_REQ-PLAN-DETAIL-COMPLETE-002_6-review.md --root F:\luode-skills --strict
python -X utf8 -B skill-dictionary/generate_dictionary.py
git diff --check
```

## 本轮实测结果

| TEST | 状态 | 证据 |
|---|---|---|
| `TEST-PD-09-01` | 15/15 通过 | `EVD-TASK-PLAN-DETAIL-09-TEST-01` |
| `TEST-PD-09-02` | 10 项回归通过 | `EVD-TASK-PLAN-DETAIL-09-TEST-02` |
| `TEST-PD-10-01` | 五档 profile 通过 | `EVD-TASK-PLAN-DETAIL-10-TEST-01` |
| `TEST-PD-10-02` | 四档 strict profile 通过 | `EVD-TASK-PLAN-DETAIL-10-TEST-02` |
| `TEST-PD-10-03` | 字典与 diff check 通过 | `EVD-TASK-PLAN-DETAIL-10-TEST-03` |
| `TEST-PD-10-04` | 临时文件已清理 | `EVD-TASK-PLAN-DETAIL-10-TEST-04` |

## 验证结论

六项测试均达到完成标准；历史可执行资产已按根 `test/` 规则迁出，历史目录只保留 README 与证据。所有样本为脱敏数据，不包含凭证、token、连接串或用户私密数据。

## 测试边界

- 本轮只使用 local 工作树和临时目录，不连接数据库、缓存、消息队列、HTTP/RPC 上游或 test/prod 环境。
- 图片资产决策：`N/A + 原因`：本任务只验证文本规则与测试资产，无界面或视觉产物 `+ 证据`：测试矩阵。

## 追踪附录

| 规则变化 | TEST | 风格证据 |
|---|---|---|
| 跨会话契约与模板同步 | `TEST-PD-09-01` | `EVD-TASK-PLAN-DETAIL-08-IMPL-01`、`EVD-TASK-PLAN-DETAIL-08-TEST-01`、`EVD-TASK-PLAN-DETAIL-08-STYLE-01` |
| 测试迁移与扩展 | `TEST-PD-09-01/02` | `EVD-TASK-PLAN-DETAIL-09-IMPL-01`、`EVD-TASK-PLAN-DETAIL-09-TEST-01/02`、`EVD-TASK-PLAN-DETAIL-09-STYLE-01` |
| 文档与记忆收口 | `TEST-PD-10-01..04` | `EVD-TASK-PLAN-DETAIL-10-IMPL-01`、`EVD-TASK-PLAN-DETAIL-10-TEST-01..04`、`EVD-TASK-PLAN-DETAIL-10-STYLE-01` |
