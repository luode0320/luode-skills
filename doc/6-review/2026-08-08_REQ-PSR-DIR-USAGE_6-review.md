---
schema_version: 1
template_version: 1
doc_id: "STYLE-PSR-DIR-USAGE-20260808"
doc_type: style_regression
source_ids: ["REQ-PSR-DIR-USAGE-001", "TEST-PSR-DIR-USAGE-20260809"]
status: accepted
version: "v1.1"
current_slice: "completed"
updated_at: "2026-08-09"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 目录用法入口升级（含 Decimal 收录）6-review

结论：本轮已完成目录用法入口升级与 Decimal 收录改动的格式、编码、命名、目录归位、注释和可读性回归。影响：Catalog、目录树、recipe 和索引中的 Decimal 事实表达一致。范围：reference、Catalog、SKILL 示例、活动测试和测试证据。非范围：业务正确性、真实项目源码、外部服务和发布放行。变化：新增 Decimal 目录规则和 4 个专项测试。完成标准：真实测试先通过且本记录为 `STYLE: PASS`。术语说明：STYLE 只表示格式、位置、写法和可读性回归结果。验证状态：已通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联测试 | `TEST-PSR-DIR-USAGE-01..09` |
| 风格结果 | `STYLE: PASS` |
| 检查对象 | 规则正文、Catalog、Markdown recipe/索引、Python 契约测试与测试证据 |

## 检查范围

- UTF-8、换行、尾随空白、JSON Catalog 可解析性和 Python 测试命名保持现有仓库口径。
- Decimal 条目位于 `package-structure-rules/references/`，活动测试位于根 `test/package-structure-rules/`，测试证据位于 `doc/5-tests/`。
- `usage-recipes-go.md` 的 decimal 小节与 Catalog 的 `package_alias`、`related_skills`、`usage_recipes` 字段保持一致。
- 本轮新增 4 个测试方法均具备 docstring 注释，符合仓库注释口径。
- N/A + 原因 + 证据：不判断业务逻辑、需求覆盖、接口运行或发布放行；真实测试证据见 `TEST-PSR-DIR-USAGE-20260809`。

## 真实测试前置证据

| 测试 | 证据 |
|---|---|
| `TEST-PSR-DIR-USAGE-01` | `EVD-TASK-04-02-TEST-01`：guide Decimal 查询返回 decimalUtil |
| `TEST-PSR-DIR-USAGE-02` | `EVD-TASK-04-02-TEST-02`：目录树包含 decimal 节点 |
| `TEST-PSR-DIR-USAGE-03` | `EVD-TASK-04-03-TEST-01`：recipe 文档包含 decimal 小节 |
| `TEST-PSR-DIR-USAGE-04` | `EVD-TASK-04-03-TEST-02`：索引文档包含 utils/decimal |
| `TEST-PSR-DIR-USAGE-05` | `EVD-TASK-04-03-TEST-03`：专项测试 9/9 |
| `TEST-PSR-DIR-USAGE-06` | `EVD-TASK-04-04-TEST-01`：py_compile 与 git diff --check |
| `TEST-PSR-DIR-USAGE-07` | `EVD-TASK-04-01-TEST-01`：需求/实施总览/周期文档门禁 |

## 任务风格证据

| 任务 | IMPL | TEST | STYLE |
|---|---|---|---|
| `T04-01` | `EVD-TASK-04-01-IMPL-01` | `EVD-TASK-04-01-TEST-01` | `EVD-TASK-04-01-STYLE-01` |
| `T04-02` | `EVD-TASK-04-02-IMPL-01` | `EVD-TASK-04-02-TEST-01` | `EVD-TASK-04-02-STYLE-01` |
| `T04-03` | `EVD-TASK-04-03-IMPL-01` | `EVD-TASK-04-03-TEST-01` | `EVD-TASK-04-03-STYLE-01` |
| `T04-04` | `EVD-TASK-04-04-IMPL-01` | `EVD-TASK-04-04-TEST-01` | `EVD-TASK-04-04-STYLE-01` |
| `T04-05` | `EVD-TASK-04-05-IMPL-01` | `EVD-TASK-04-05-TEST-01` | `EVD-TASK-04-05-STYLE-01` |

## 6-review 结论

STYLE: PASS

## 检查清单

| 检查项 | 结果 | 证据 |
|---|---|---|
| 格式、编码、换行和尾随空白 | PASS | `EVD-TASK-04-04-TEST-01` |
| 命名、写法、路径和目录归位 | PASS | `EVD-TASK-04-02-TEST-01` |
| 注释、可读性和规则术语一致性 | PASS | `EVD-TASK-04-03-TEST-01` |
| 测试资产未进入 `doc/5-tests/` 活动代码区 | PASS | `EVD-TASK-04-04-TEST-01` |

## 问题与修复

- 已修复：`project-layout-v2.md` 插入 decimal 行时缺换行，导致目录树行与后续 http 行粘连；已补换行并新增目录树断言测试。
- 已修复：`backend-util-layout.md` 插入 Decimal 行后遗留尾随空白，`git diff --check` 报错；已清理并复验。
- 已修复：`PROJECT_MEMORY.md` 首次插入 Decimal 小节时产生空标题重复，已清理重复空节。
- 已修复：需求、实施总览和周期文档首版未满足文档门禁结构；已按 profile 重写并逐份 PASS。
- 未发现需要新增生产逻辑、真实项目源码或测试专用生产字段的问题。
- 若后续真实业务项目 Decimal 行为与本规则不一致，应在业务项目按 local 配置验证，不得使用本记录替代运行验证。

图片资产决策：N/A + 原因：本风格回归只检查文本规则、目录和测试资产，不存在界面或视觉产物 + 证据：检查清单与 `EVD-TASK-04-01..05`。

## 追踪附录

| 来源/规则 | 测试 | 风格证据 |
|---|---|---|
| `REQ-PSR-DIR-USAGE-001` 目录用法入口升级 | `TEST-PSR-DIR-USAGE-01..05` | `EVD-TASK-04-01..05-STYLE-01` |
| Decimal 目录规则收录 | `TEST-PSR-DIR-USAGE-01..04` | `EVD-TASK-04-02/03-STYLE-01` |
