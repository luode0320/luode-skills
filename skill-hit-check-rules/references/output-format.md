# 输出格式

每轮首条中间进度先给出命中检查。区块使用普通 Markdown，不得放入代码围栏、缩进代码块或 HTML。

**Skill 命中检查**

`命中检查:通过; Git规则:不适用`

`命中技能:skill-hit-check-rules,parallel-task-dispatch-rules`

`并行技能:无`

`Obsidian:不适用`

`闸门预告:收口前→reasoning-summary-structure-rules`

格式要求：

- `命中检查`、`Git规则`、`命中技能` 为固定字段。
- 仓库任务必须追加 `Obsidian`；命中并行规则时必须追加 `并行技能`。
- 非 Plan Mode 的仓库实质任务必须追加 `闸门预告`，按 `deferred-gate-registry.md` + 当前任务类型登记本轮延迟 gate（格式 `checkpoint→gate;...`，无适用项写 `无`），并把其中强制项（含 `reasoning-summary-structure-rules`）列入 `命中技能`；Plan Mode 下 `闸门预告` 置 `不适用(Plan Mode)` 且 `命中技能` 不含 `reasoning-summary-structure-rules`。
- 当前轮存在 Git 意图时，`Git规则` 必须为 `通过` 或 `阻断`，不得写 `不适用`。
- 命中技能使用真实 Skill 名称，按总控入口、强制联动、主域和辅助域排序。
- 若除总控与仓库基础联动外无其他领域 Skill，如实列出，不虚构业务命中。
- 首条字段只报告路由结果，不替代各 Owner Skill 的真实执行证据。
