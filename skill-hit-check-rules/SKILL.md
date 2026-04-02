---
name: skill-hit-check-rules
description: 当用户每次提问进入新回合时自动触发。负责在执行主任务前先检查本轮是否命中任何 skill，防止漏触发或忘触发；若命中则必须在回复中明确告知命中 skill 列表，若未命中则明确告知未命中及原因。若本轮发生代码新增或修改且进入最终回复前收口，必须同时命中 `code-comment-rules` 与 `skill-compliance-gate-rules`。不要用它代替需求、Bug、编码、测试或交付等主域 skill 的实际执行。
---

# Skill 命中检查规则

每次用户提问都先触发本 skill。
目标是确保“先检查 skill 命中，再进入主任务执行”，避免静默漏触发。

## Skill 作用与适用场景

- 在每轮用户提问后，先做一次 skill 命中检查。
- 明确给出本轮命中的 skill 列表，避免“命中了但没说”。
- 如果没有命中，明确说明未命中原因，避免“未命中但没解释”。
- 把 skill 检查作为前置动作，不代替后续主域执行。

## 自动触发信号

- 用户发起任意新问题或新指令。
- 用户在同一任务中发起新一轮追问。
- 上下文压缩后进入新回合继续执行。
- 本轮发生代码新增或修改，且即将进入最终回复前收口。

## 进入后先做什么

1. 先基于本轮用户输入，检查是否命中任何现有 skill。
2. 命中判断时，优先依据各 skill 的 `description` 触发条件。
3. 先输出命中检查结果，再进入主域执行。
4. 输出命中列表时，不把本 skill 自己计入“业务命中 skill 列表”。
5. 当请求包含“补充注释 / 只补注释 / 注释规范检查”时，除 `code-comment-rules` 外，必须同时命中 `skill-compliance-gate-rules` 作为收口闸门。
6. 当本轮发生代码新增或修改且进入最终回复前收口时，即使用户未显式提“注释”，也必须同时命中 `code-comment-rules` 与 `skill-compliance-gate-rules`。

## 默认执行流程

1. 默认先读 `references/hit-checklist.md`，按固定步骤做命中判定。
2. 再读 `references/output-format.md`，按固定格式输出检查结果。
3. 若命中一个或多个 skill，先输出命中列表，再转交对应 skill 继续执行。
4. 若未命中任何 skill，输出未命中原因后，按通用能力继续处理当前问题。
5. 若本轮存在代码改动且准备最终回复，强制补命中 `code-comment-rules` 与 `skill-compliance-gate-rules` 后再收口。

## 输出要求

每轮必须先输出一个命中检查区块，建议格式如下：

```text
Skill 命中检查：
- 命中 skill：`skill-a`、`skill-b`
```

未命中时：

```text
Skill 命中检查：
- 命中 skill：无
- 原因：当前请求不满足任何已定义 skill 的触发条件
```

## 权责边界与不负责事项

- 只负责“检查并告知命中结果”，不代替主域 skill 的具体规则执行。
- 不伪造命中结果，不把未命中写成命中。
- 不因为做了命中检查而跳过主任务。

## 执行通过 / 驳回标准

- 通过：每轮都先给出命中检查结果，且命中 skill 列表与本轮任务一致。
- 驳回：用户提问后未执行命中检查，或命中了 skill 但未告知清单。

## references 读取规则

- 默认先读 `references/hit-checklist.md`。
- 只有在需要组织输出时，再读 `references/output-format.md`。
