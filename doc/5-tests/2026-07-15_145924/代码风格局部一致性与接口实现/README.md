---
schema_version: 1
doc_id: TEST-STYLE-FB-20260715-001
doc_type: test
source_ids:
  - SRC-STYLE-FB-04
status: confirmed
version: 1.0.0
current_slice: 周期02-新增规则行为演练
template_version: 1
updated_at: 2026-07-15
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: review
    applicability: not_applicable
    reason: 本 README 只记录测试任务，不替代实现审查。
    basis: 审查证据单独归档到 doc/6-审查/。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
  - stage: acceptance
    applicability: applicable
    reason: 本测试任务为新增验收场景提供真实证据。
    basis: 本轮新增局部风格、接口实现和写后闸门规则。
    required_by_source: true
    required_now: true
    completed_validation:
      - 本 README
      - 三份 ASCII 证据
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: 三项演练均 PASS。
  - stage: third_party
    applicability: not_applicable
    reason: 本地规则资产演练不调用第三方业务服务。
    basis: 测试只读取本地 Markdown 和内存样本。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---

# 测试任务：代码风格局部一致性与接口实现

结论：本轮规则行为演练已通过；影响：后续代码生成任务的局部风格延续和接口实现对照；范围：本地规则资产和受控样本；非范围：业务代码、外部环境和生产数据；变化：新增规则具备可复核的正反例证据；完成标准：所有演练结果通过且测试说明可交接；术语说明：无技术术语需要解释；验证状态：本地测试已完成并通过。

## 既有测试摘要

结论：三组新增规则演练均通过，可以继续进入字典、审查和最终验收收口；影响：后续代码生成任务会优先延续稳定局部写法，并在实现接口时留下既有实现对照；范围：本轮 `code-generation-style-rules` 规则资产及其可执行契约；非范围：不修改业务代码、不连接外部环境、不新增测试专用生产代码；变化：新增规则可识别同构局部模板、记录接口参考实现并驳回风格跳变和多余代码；完成标准：三项演练均通过且证据可追溯；术语说明：局部一致性指当前文件、同目录或同模块已经重复形成的稳定写法；验证状态：已使用本地 Python 对真实规则文件和受控样本完成演练，结果均为通过。

## 文档信息

- 测试类型：规则资产行为演练。
- 图片资产决策：N/A + 原因 + 证据。本轮没有 UI、截图、视觉对比或真实图片产物。

## 验收结论

三项新增规则演练均通过，证据已落盘并可回指需求、规则、验收和实施任务。

## 验证结论

本地 Python 断言、UTF-8 读取和测试证据归档均通过；详细命令和输出位于执行附录及 ASCII 证据文件。

## 完成标准

README 能说明测试对象、执行方式、环境边界、覆盖范围、真实证据入口和通过结论。

## 测试目的

验证本轮新增规则是否能把用户反馈转成可执行的写码前契约和写后闸门，重点覆盖：

- 高度统一的局部代码区段只做必要模板替换。
- 实现已有接口时记录既有实现的文件路径和符号。
- 没有参考实现时使用明确降级依据。
- 风格跳变、额外 helper、临时变量、循环、日志、校验和陌生抽象被驳回。
- 正确性、安全、兼容和接口契约要求的必要代码不会被“风格一致”规则误删。

## 执行方式

- 环境：Windows 本地工作区，Python `-X utf8`，不连接数据库、缓存、消息队列、HTTP/RPC 或外部业务服务。
- 生产代码：未修改；没有新增测试专用方法、字段、fixture 或运行时结构。
- 规则资产断言入口：

```text
python -X utf8 -c "读取 code-generation-style-rules 的 SKILL.md、references 和受控样本，执行 TEST-06 至 TEST-08 断言"
```

## 覆盖范围与结论

| 测试 | 覆盖内容 | 结果 | 证据 |
| --- | --- | --- | --- |
| TEST-06 | `xx.New().Start(true)` 同构注册区段的局部模板替换 | PASS | `code_generation_style/local_style_positive.md` |
| TEST-07 | 同文件、同目录/模块参考实现及无参考降级 | PASS | `code_generation_style/interface_style_reference.md` |
| TEST-08 | 风格跳变、多余代码负例驳回及必要硬性代码保留 | PASS | `code_generation_style/post_change_gate_negative.md` |

## 真实证据入口

详细证据位于同一时间戳根目录下的 ASCII 真实代码路径镜像目录：

- `doc/5-tests/2026-07-15_145924/code_generation_style/local_style_positive.md`
- `doc/5-tests/2026-07-15_145924/code_generation_style/interface_style_reference.md`
- `doc/5-tests/2026-07-15_145924/code_generation_style/post_change_gate_negative.md`

## 失败预期与清理

- 负例必须被写后闸门驳回；若负例通过，TEST-08 失败并回到 `TASK-02-05` 修复。
- 局部风格冲突或接口样例无法收敛时，必须记录 `GAP-STYLE-LOCAL-001` 或 `GAP-STYLE-INTERFACE-001` 并停止；本轮受控样本未触发该边界。
- 本轮只读规则文件和内存样本，没有写入外部数据；无运行时数据需要清理或回滚。

## 追踪附录

| 来源 | 规则/需求 | 验收 | 周期/任务 | 测试 | 证据 |
| --- | --- | --- | --- | --- | --- |
| `SRC-STYLE-FB-04` | `REQ-07` / `RULE-05` | `AC-06` | `CYCLE-02` / `TASK-02-03` | `TEST-06` | `EVD-02-03-LOCAL-STYLE` |
| `SRC-STYLE-FB-04` | `REQ-08` / `RULE-06` | `AC-07` | `CYCLE-02` / `TASK-02-04` | `TEST-07` | `EVD-02-04-INTERFACE-STYLE` |
| `SRC-STYLE-FB-04` | `REQ-07` / `REQ-08` / `RULE-05` / `RULE-06` | `AC-08` | `CYCLE-02` / `TASK-02-05` | `TEST-08` | `EVD-02-05-NEGATIVE-GATE` |
