---
name: skill-hit-check-rules
description: 作为总控层的轮次命中检查入口 skill，在每轮用户提问开始时负责检查本轮是否命中任何 skill，防止漏触发或忘触发；若命中则必须在回复中明确告知命中 skill 列表，若未命中则明确告知未命中及原因。该 skill 应由 `team-development-rules` 或平台侧总控在每轮开局优先路由调用，而不是依赖自身先被业务命中。若本轮发生代码新增或修改，不仅在最终回复前收口必须命中 `comment-placement-granularity-rules`、`comment-completion-gate-rules` 与 `skill-compliance-gate-rules`，还必须在首次代码改动后的中间阶段立即补做一次注释相关命中检查；涉及代码改动收口时，需补做 `cleanup-format-review-rules` 与 `syntax-check-review-rules` 的命中检查，避免只做构建不做基础格式和语法收口；当用户请求“补充注释/只补注释/注释完善”时，必须同时命中 `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules`，并优先处理未提交且已有改动的代码位点。不要用它代替需求、Bug、编码、测试或交付等主域 skill 的实际执行。
---

# Skill 命中检查规则

本 skill 由总控层在每轮开局优先路由调用。
目标是确保“先检查 skill 命中，再进入主任务执行”，避免静默漏触发。

## Skill 作用与适用场景

- 在每轮用户提问后，先做一次 skill 命中检查。
- 明确给出本轮命中的 skill 列表，避免“命中了但没说”。
- 如果没有命中，明确说明未命中原因，避免“未命中但没解释”。
- 把 skill 检查作为前置动作，不代替后续主域执行。
- 当用户给出执行型 Git 短指令（如“提交git”“提交 git”“commit 一下”）时，必须优先命中 `git-collaboration-rules`，且其优先级高于 `autonomous-execution-rules`、`delivery-summary-rules` 和其他阶段判断，避免被误分流。

## 自动触发信号

- 用户发起任意新问题或新指令。
- 用户在同一任务中发起新一轮追问。
- 上下文压缩后进入新回合继续执行。
- 多步骤任务中出现阶段切换且存在可直接执行的下一步（非关键决策/高风险节点）。
- 本轮首次发生代码新增或修改（不等待最终收口）。
- 本轮发生代码新增或修改，且即将进入最终回复前收口。
- 本轮执行链路较长并出现中间阶段总结时（例如已经产生多条中间进度消息），需要在中段再次复检命中结果。

## 进入后先做什么

1. 先基于本轮用户输入，检查是否命中任何现有 skill。
2. 命中判断时，优先依据各 skill 的 `description` 触发条件。
3. 必须在回复最开始先输出命中检查结果，再进入主域执行。
4. 输出命中列表时，不把本 skill 自己计入“业务命中 skill 列表”。
5. 当请求包含“补充注释 / 只补注释 / 注释规范检查 / 注释完善”时，必须同时命中 `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules`，不得缺任一项。
6. 当本轮首次发生代码新增或修改时，即使用户未显式提“注释”，也必须在中间进度阶段立即补命中 `comment-placement-granularity-rules`、`comment-completion-gate-rules` 与 `skill-compliance-gate-rules`。
7. 当本轮发生代码新增或修改且进入最终回复前收口时，必须再次复核上述三个注释相关 skill 仍处于命中状态。
7.1 当本轮发生代码新增或修改且进入最终回复前收口时，必须补做 `cleanup-format-review-rules` 与 `syntax-check-review-rules` 命中检查；若未执行，不能给出“已完成”结论。
7.2 当本轮已命中任一业务 skill 时，默认同步补命中 `subagent-dispatch-rules`，先做“是否委派”判定再进入主执行；仅在用户明确禁止委派或环境不支持时回退本地执行。
8. 当多步骤任务存在可直接继续的下一步时，必须补做 `autonomous-execution-rules` 命中检查，并默认继续推进。
9. 当用户请求补注释时，先定位“未提交且已有改动”的代码范围，再执行注释补齐，不得优先处理未改动历史代码。
10. 当用户请求是“执行提交”而不是“审查提交”时，必须优先命中 `git-collaboration-rules`，不得先进入其他阶段 skill；若是“review commit/审核提交”，则命中 `code-review-automation-rules`。

## 默认执行流程

1. 默认先读 `references/hit-checklist.md`，按固定步骤做命中判定。
2. 再读 `references/output-format.md`，按固定格式输出检查结果。
3. 若命中一个或多个 skill，先输出命中列表，再转交对应 skill 继续执行。
4. 本轮对用户可见的**首条中间进度消息**必须以命中检查区块开头，不能等到最终回复才给出。
5. 最终回复也必须再次以命中检查区块开头，确保收口时可复核。
6. 若未命中任何 skill，输出未命中原因后，按通用能力继续处理当前问题。
7. 若本轮首次发生代码改动，立刻在下一条中间进度消息补做注释相关命中检查，不得拖延到最终回复。
8. 若本轮执行链路较长，在中间阶段总结前再次复检命中结果，避免“前面改了代码、后面才补命中”。
9. 若本轮是多步骤任务且当前阶段完成后可继续，先命中 `autonomous-execution-rules` 并直接推进下一步，不在中段停顿征求确认。
9.1 若本轮已命中业务 skill，默认先补命中 `subagent-dispatch-rules`，完成委派判定后再继续后续技能执行；若用户明确禁止委派，则保留命中但回退本地执行。
10. 若本轮存在代码改动且准备最终回复，强制补命中 `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`cleanup-format-review-rules`、`syntax-check-review-rules` 与 `skill-compliance-gate-rules` 后再收口。
10.1 当命中 `comment-completion-gate-rules` 且本轮存在函数/方法改动时，最终回复必须包含“函数注释核对清单”；若无函数/方法改动，必须声明“函数位点 0 个”。
10.2 当本轮在原有方法中存在补丁位点时，最终回复必须包含“补丁注释核对清单”；若无补丁位点，必须声明“补丁位点 0 个”。
11. 若本轮是补注释请求，强制校验是否已命中 `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules`，并确认注释范围优先覆盖未提交改动代码。
12. 若用户输入“提交git / 提交 git / commit一下 / 帮我提交”这类执行型短指令，必须先命中 `git-collaboration-rules` 再进入其他域判断，不得等待“测试已完成”等附加描述才触发，也不得先命中 `autonomous-execution-rules` 或 `delivery-summary-rules`。

## 输出要求

每轮必须在**回复开头第一段**先输出命中检查区块，并给出每个命中 skill 的简短说明，建议格式如下：

```text
Skill 命中检查：
- 命中 skill：
`skill-a`: 简短说明
`skill-b`: 简短说明
```

并且必须满足以下时机要求：
- 本轮首条中间进度消息（思考过程开始时）必须先输出该区块。
- 本轮首次代码改动后的下一条中间进度消息必须再次输出该区块。
- 本轮长链路执行的中间阶段总结消息必须再次输出该区块。
- 本轮最终回复也必须先输出该区块。
- 禁止仅在最终回复输出，导致执行过程不可见。

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

- 通过：首条中间消息、首次代码改动后的中间消息、以及最终回复都给出命中检查结果，且命中 skill 列表与本轮任务一致；涉及函数/方法改动时最终回复包含函数注释核对清单（或明确函数位点 0 个）；涉及补丁位点时最终回复包含补丁注释核对清单（或明确补丁位点 0 个）。
- 驳回：用户提问后未执行命中检查，或命中了 skill 但未告知清单，或已改代码但拖到最终回复才补注释相关命中，或“提交git”类执行指令未命中 `git-collaboration-rules`，或函数/方法改动场景未输出函数注释核对清单，或补丁位点场景未输出补丁注释核对清单。

## references 读取规则

- 默认先读 `references/hit-checklist.md`。
- 只有在需要组织输出时，再读 `references/output-format.md`。
