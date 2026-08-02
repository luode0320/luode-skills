---
schema_version: 1
doc_id: "STYLE-PSR-TEST-ROOT-001"
doc_type: style_regression
source_ids: ["REQ-PSR-TEST-ROOT-001", "CYCLE-PSR-18-001"]
status: accepted
version: "v1.0"
current_slice: "TASK-18-03..04"
updated_at: "2026-08-02 23:50:00"
template_version: "style-regression-v1"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：三类项目根 test 目录统一

结论：本轮目录 reference、Catalog、根测试和研发文档均沿用现有写法并正确归位。影响：本记录只确认格式、命名、注释、可读性、测试资产路径和文档位置，不替代根目录契约测试或规则验收；范围：本周期的规则、目录事实、测试和证据文件；非范围：真实项目迁移、外部服务、业务正确性和 Git 历史；变化：三类项目统一表达根 `test/`，测试说明与活动测试继续分离；完成标准：风格回归通过；术语说明：根 `test/` 是活动测试代码根，`doc/5-tests/` 是测试说明和证据根；验证状态：根目录专项 `4/4`、入口回归 `5/5`、配置回归 `7/7`、根 Python 测试 `212/212` 和适用文档 profile 均通过。

## 图片资产决策

图片资产决策：N/A + 原因：本轮只检查文本规则、目录结构、测试代码归位和 Markdown 证据，不包含 UI、截图或视觉产物；证据：测试矩阵与风格清单均为文本/路径断言。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联任务 | `TASK-18-03..04` |
| 关联真实测试 | `TEST-PSR-TEST-ROOT-001..006` |
| 实现证据 | `EVD-TASK-18-03-IMPL`、`EVD-TASK-18-04-IMPL` |
| 测试证据 | `EVD-TASK-18-03-TEST`、`EVD-TASK-18-04-TEST` |
| 风格证据 | `EVD-TASK-18-03-STYLE`、`EVD-TASK-18-04-STYLE` |
| 检查时点 | 根目录专项、既有回归、全量根测试和测试 README profile 通过后 |

## 检查范围

- `package-structure-rules/references/project-layout-v2.md`、`placement-catalog.yaml` 与目录引用契约的根 `test/` 表达。
- `test/package-structure-rules/project_layout_contract_test.py` 的测试路径、临时目录清理、断言粒度和中文注释。
- `doc/2-需求/`、`doc/3-实施/`、`doc/5-tests/` 和本记录的 front matter、白话首段、Markdown 层级、证据 ID 与目录归位。
- 项目四件套中 CYCLE-18 的当前状态、稳定规则和历史事件职责分离。
- 范围外：不重新判断目录规则业务覆盖、不替代 CLI 行为测试、不判断真实业务项目构建或发布放行。

## 真实测试前置证据

- `TEST-PSR-TEST-ROOT-001..004`：根目录契约测试 `4/4` 通过，覆盖三类 Catalog、人工目录树、query、render 和 init。
- `TEST-PSR-TEST-ROOT-005`：入口回归 `5/5`、配置回归 `7/7` 通过。
- `TEST-PSR-TEST-ROOT-006`：根 Python 入口 `212/212` 通过，活动测试仍由根 `test/` 发现。
- 测试 README `test` profile、`package-structure-rules` Skill 校验和相关文档 profile 均返回通过。

## 6-review 结论

- STYLE: PASS

## 检查清单

| 检查项 | 结果 | 证据 |
|---|---|---|
| UTF-8、Markdown 结构、标题和尾随空白 | PASS | `git diff --check`、测试 README profile |
| 命名、证据 ID 和 CYCLE-18 术语一致 | PASS | CYCLE-18、测试 README、V2 总览 |
| 活动测试归位根 `test/`，测试说明归位 `doc/5-tests/` | PASS | `project_layout_contract_test.py`、`TEST-PSR-TEST-ROOT-006` |
| 中文注释、断言可读性和临时目录清理 | PASS | `project_layout_contract_test.py`、根 Python 测试 |
| 目录文档与活动 `doc/6-review/` 归位 | PASS | 本记录、适用文档 profile |

## 问题与修复

N/A + 原因 + 证据：本轮没有未修复的 `STYLE: FIX_REQUIRED` 项；测试说明首次 profile 缺少独立“完成标准”章节的问题已补齐，补齐后 profile 返回 `valid: true`，未扩大目录规则范围。

## 执行附录

本轮只使用 local 工作树、UTF-8 Python、临时目录和文档校验器；不连接数据库、缓存、消息队列、HTTP/RPC 上游或非 local 环境，不移动历史测试资产，不执行 Git 历史写入。

## 追踪附录

`TASK-18-03..04` -> `EVD-TASK-18-03-IMPL/TEST/STYLE`、`EVD-TASK-18-04-IMPL/TEST/STYLE` -> `STYLE-PSR-TEST-ROOT-001` -> `STYLE: PASS`。
