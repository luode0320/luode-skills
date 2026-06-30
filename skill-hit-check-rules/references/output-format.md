# 输出格式

每轮输出前先给出命中检查。命中检查区块使用普通 Markdown 输出，不得放入代码围栏（三反引号 / 三波浪线）或缩进代码块；标题独立一行，字段行整行使用单反引号包裹，避免渲染成横向滚动代码块。

**Skill 命中检查**

`命中检查:通过; Git规则:不适用`

`命中技能:skill-a,skill-b`

`并行技能:无`

如果除总控外未命中其他领域 skill：

**Skill 命中检查**

`命中检查:通过; Git规则:不适用`

`命中技能:skill-hit-check-rules`

`并行技能:无`

格式要求：

- 命中技能必须使用真实 skill 名称。
- 若命中多个，按相关度从高到低列出。
- 命中检查区块必须出现在本轮回复开头。
- 命中检查区块不得使用代码围栏、缩进代码块或 HTML；长列表自然换行即可。

代码改动收口示例：

**Skill 命中检查**

`命中检查:通过; Git规则:不适用`

`命中技能:skill-hit-check-rules,comment-placement-granularity-rules,comment-completion-gate-rules,skill-compliance-gate-rules`

`并行技能:无`
