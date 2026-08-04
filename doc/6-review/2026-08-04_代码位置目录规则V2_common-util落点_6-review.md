---
schema_version: 1
template_version: 1
doc_id: STYLE-PSR-COMMON-UTIL-001
doc_type: style_regression
source_ids: [SRC-PSR-COMMON-UTIL-001]
status: accepted
version: v1.0
current_slice: CYCLE-PSR-22-001
updated_at: 2026-08-04
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：独立后端 common/util 落点

结论：本次规则、CLI、测试和文档改动的格式、命名、目录归位、注释和可读性符合现有风格；影响：`common/util` 新落点在活动资产中保持一致；范围：本周期涉及的规则、测试、文档和项目记忆；非范围：业务正确性、需求覆盖、发布放行和真实项目迁移；变化：源码根 `util/` 旧口径改为废弃，新增 `common/util` 唯一落点；完成标准：STYLE 结果为 PASS 且测试前置证据可核验；术语说明：common/util 表示独立后端项目关联工具的扁平目录，风格回归表示只检查写法与位置；验证状态：专项测试 `5/5`、package-structure-rules 四个活动测试文件共 `22/22`、需求/实施/测试/风格 profile 均通过。

## 文档信息

关联任务：`T22-01`、`T22-02`、`T22-03`；证据：`EVD-T22-01-TEST`、`EVD-T22-02-TEST`、`EVD-T22-03-DOC`。

## 检查范围

- 检查规则文档、Catalog、Schema、CLI、活动测试和四件套的格式、UTF-8、目录归位、注释、命名与引用一致性。
- 检查 `common/util` 与根 `utils/<package>/` 的职责描述是否与测试和目录树一致。
- 不判断业务逻辑正确性、需求覆盖、测试充分性或发布放行。

## 真实测试前置证据

`backend_common_util_layout_test.py` 真实运行 `5/5`；`package-structure-rules` 四个活动文件真实运行 `22/22`；需求、实施周期、测试和风格 profile 返回 `valid: true`。

## 6-review 结论

STYLE: PASS

## 检查清单

| 检查项 | 结果 | 依据 |
|---|---|---|
| UTF-8、换行、尾随空白 | PASS | 本轮编码与 `git diff --check` 检查 |
| 规则资产与测试目录归位 | PASS | `package-structure-rules` 与根 `test/` 约定 |
| Python 命名、注释和局部结构 | PASS | 现有 CLI 与测试风格 |
| 文档中文表达、追踪 ID 和 Mermaid | PASS | requirement/implementation_cycle profile |
| 根 `utils` 与 `common/util` 职责描述 | PASS | backend-util-layout 与专项断言 |

## 问题与修复

N/A + 原因 + 证据：本轮未发现需要风格修复的问题；全仓测试中的历史文档 fixture 路径失败不属于风格问题，已记录在 `doc/5-tests/2026-08-04_common-util/run-report.md`。

图片资产决策：N/A + 原因 + 证据：本轮不涉及图片或视觉对象。

## 追踪结论

`T22-01/T22-02/T22-03` -> `EVD-T22-01-TEST/EVD-T22-02-TEST/EVD-T22-03-DOC` -> `STYLE: PASS`。

兼容追踪：`TASK-PSR-COMMON-UTIL-01`、`TEST-PSR-COMMON-UTIL-01`、`EVIDENCE-PSR-COMMON-UTIL-01`。
