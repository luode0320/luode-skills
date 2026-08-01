---
schema_version: 1
template_version: 1
doc_id: "STYLE-<主题>-<日期>"
doc_type: "style_regression"
source_ids: ["SRC-<来源>"]
status: "accepted"
version: "v1.0"
current_slice: "TASK-<任务>"
updated_at: "YYYY-MM-DD HH:mm:ss"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：<主题>

结论：本次仅核对代码写法和归位结果；影响：不代替功能测试或发布判断；范围：本次改动涉及的代码与测试资产；非范围：业务正确性、需求覆盖和发布放行；变化：记录风格检查结论；完成标准：`STYLE` 为 `PASS` 或已按 `FIX_REQUIRED` 修复并复查；术语说明：风格回归是对代码写法和位置的检查；验证状态：真实测试证据已关联。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | `TASK-<任务>` |
| 关联真实测试 | `TEST-<测试>` / `EVD-<任务>-TEST-01` |
| 检查时点 | 真实测试通过后 |

## 检查范围

- 检查格式、换行、UTF-8、尾随空白、命名、局部写法、目录位置、依赖方向、测试资产归位、注释、日志、可读性与公共工具复用。
- 范围外：不判断业务正确性、需求覆盖、测试覆盖率或发布放行。

## 真实测试前置证据

- `TEST-<测试>`：关联实施计划中的完成条件；证据为 `EVD-<任务>-TEST-01`。

## 6-review 结论

- STYLE: PASS

## 检查清单

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| 格式、编码与尾随空白 | PASS | `EVD-<任务>-STYLE-01` |
| 命名、写法与目录归位 | PASS | `EVD-<任务>-STYLE-02` |
| 注释、日志、可读性与复用 | PASS | `EVD-<任务>-STYLE-03` |

## 问题与修复

N/A + 原因 + 证据：本模板未发现具体问题；实际出现 `STYLE: FIX_REQUIRED` 时，逐项写明修复位置和复查证据。

图片资产决策：N/A + 原因 + 证据：本风格回归记录不需要图片资产。

## 执行附录

记录本次格式检查、局部规则核对命令和复查步骤。

## 追踪附录

关联 `SRC-*`、`TASK-*`、`TEST-*`、`EVD-*-TEST-*` 与 `EVD-*-STYLE-*` 证据；历史 `REVIEW/ACCEPT` 只用于归档资料，不进入本模板。
