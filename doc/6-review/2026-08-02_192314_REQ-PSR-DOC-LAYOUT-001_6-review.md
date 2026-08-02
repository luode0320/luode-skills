---
schema_version: 1
template_version: 1
doc_id: "STYLE-PSR-DOC-LAYOUT-20260802-01"
doc_type: style_regression
source_ids: ["REQ-PSR-DOC-LAYOUT-001", "CYCLE-PSR-DOC-LAYOUT-16-001"]
status: accepted
version: "v1.0"
current_slice: "TASK-PSR-DOC-16-04"
updated_at: "2026-08-02 19:23:14"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：三类项目 doc 目录收敛

结论：真实测试通过后，规则、Catalog、测试和研发文档的格式、目录归位、中文注释和证据引用一致，结论为 `STYLE: PASS`。影响：活动研发产物统一落在新的 `doc/6-review` 入口，审查结论可按任务追踪。范围：规则目录树、Catalog、根 `test/` 专项测试、测试证据、需求/实施文档和项目记忆的风格与位置。非范围：目录业务正确性、真实项目迁移、历史目录清理、外部服务和 Git 历史写入。变化：新活动记录使用 `doc/6-review`，旧 `doc/6-审查/` 与 `doc/7-验收/` 仅只读保留。完成标准：清单全部 `PASS`，没有未修复 `STYLE: FIX_REQUIRED`。术语说明：`6-review` 指测试后的代码习惯风格回归。验证状态：入口回归、目录专项测试、文档 profile 和差异检查均已执行或记录。本文只检查风格与位置，不替代目录契约测试或需求验收。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联任务 | `TASK-PSR-DOC-16-01` 至 `TASK-PSR-DOC-16-04` |
| 关联测试 | `TEST-PSR-DOC-LAYOUT-001`、`TEST-PSR-BINARY-BASELINE-001` |
| 检查时点 | 专项测试、入口回归和文档 profile 之后 |
| 范围 | `package-structure-rules` 目录树、Catalog、根 `test/` 专项测试、`doc/5-tests` README、需求/实施文档和项目记忆。 |

## 检查范围

- 检查 UTF-8、Markdown 层级、中文目录注释、`doc/6-review` 归位、根测试可执行资产位置、临时文件和追踪引用。
- 不判断目录业务规则是否正确；该结论由 `TEST-PSR-DOC-LAYOUT-001` 负责。

## 范围外说明

- 不迁移真实项目，不清理历史 `doc/6-审查/` 与 `doc/7-验收/`，不执行 Git 历史写入。
- 不读取或写入 Obsidian vault。

## 真实测试前置证据

- `TEST-PSR-BINARY-BASELINE-001`：`python -X utf8 -B test/package-structure-rules/entrypoint_layout_test.py` 返回 `5/5 OK`。
- `TEST-PSR-DOC-LAYOUT-001`：`python -X utf8 -B test/package-structure-rules/project_layout_contract_test.py` 返回 `2/2 OK`。
- `TEST-PSR-DOC-ROOT-001`：根目录 Python 测试、文档 profile 和 `git diff --check` 均通过。

## 6-review 结论

- STYLE: PASS

## 检查清单

| 检查项 | 结果 | 证据 |
|---|---|---|
| UTF-8、Markdown 结构、尾随空白 | PASS | `EVD-PSR-DOC-16-04-STYLE-01` |
| 三类目录树与 Catalog 注释归位 | PASS | `EVD-PSR-DOC-16-04-STYLE-02` |
| 可执行测试只位于根 `test/` | PASS | `EVD-PSR-DOC-16-04-STYLE-03` |
| `doc/5-tests` 仅保存 README/证据 | PASS | `EVD-PSR-DOC-16-04-STYLE-04` |
| 项目记忆与活动 doc 目录语义一致 | PASS | `EVD-PSR-DOC-16-04-STYLE-05` |

## 问题与修复

N/A + 原因 + 证据：没有未修复的 `STYLE: FIX_REQUIRED` 项；CYCLE-15 的同仓入口误判已在基线阶段以最小分支修复，并由入口回归测试确认。

图片资产决策：N/A + 原因 + 证据：本次只检查文本规则、测试入口和文档位置，没有视觉资产。

## 执行附录

检查均使用本地 Python、临时目录和仓库文件；未连接数据库、缓存、消息队列、第三方 API、test/prod 环境或 Obsidian vault。

## 追踪附录

`TASK-PSR-DOC-16-01..04` -> `TEST-PSR-DOC-LAYOUT-001`/`TEST-PSR-BINARY-BASELINE-001` -> `EVD-PSR-DOC-16-04-STYLE-01..05` -> `STYLE: PASS`。
