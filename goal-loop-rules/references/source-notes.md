# 来源记录（source-notes）

> 本文件登记 long-run-loop-rules 各次调整的来源与落点，保证可追溯。

## 2026-10-13 内部调整：Goal 计划文档缺项自修复并持续执行

- **来源**：用户裁决（2026-10-13）——Goal 执行过程中发现计划文档不完善，应主动完善并持续执行 Goal，不要因计划文档问题阻断停止。
- **通道**：Goal Owner 规则补充；Goal 已确认目标级许可，计划文档缺陷属于执行期可修复事项。
- **落点**：`SKILL.md` 增加缺项自修复规则；`references/safety-mechanisms.md` 补 Owner 引用；同步 `autonomous-execution-rules/SKILL.md`、`references/execution-authorization-and-plan-boundary.md`、`references/continuation-and-pause.md` 及 agent 默认提示。
- **边界**：仅用户显式开启或确认且仍 active 的 Goal 适用；普通模式和 Plan Mode 的正式计划门禁不变。计划缺项本身不生成 `BLK-*`；强制审批、高风险、不可逆、越界、用户撤销或无法安全推进的动作仍按真实阻断契约处理。

## 2026-09-24 内部调整：Goal 模式免确认推进与临时产物清理

- **来源**：用户指令（2026-09-24）——“只要我们开启 goal 模式，说明我们计划已经完成，只要实现就好了；如果执行过程有分歧，一律按照 agent 推荐的方案推进执行，不要求用户确认；临时生成的文件和脚本记得执行后删除，不要污染项目目录。”
- **通道**：内部更新通道（自有 skill 现状 + 用户调整诉求）。
- **落点**：
  - `SKILL.md`（新增「Goal 模式免确认推进（分歧按推荐方案执行）」章节 + description 补口径）
  - `references/safety-mechanisms.md`（新增「Goal 模式免确认推进」章节，只补与安全熔断的衔接，规则本体引用 SKILL.md）
- **联动落点**（同域，由对应 Owner 承载，不重复定义）：
  - `autonomous-execution-rules/SKILL.md`（description 放开口径 + 「必须暂停确认的关键节点」补 Goal 模式例外）
  - `autonomous-execution-rules/references/continuation-and-pause.md`（新增「Goal 模式免确认推进」小节 + 必须暂停项收缩）
  - `AGENTS.md` / `CLAUDE.md`（新增「Goal 模式免确认推进与临时产物清理」仓库级章节）
  - 复用既有红线 Owner：`runtime-process-cleanup-rules`（临时产物清理）、`git-collaboration-rules`（提交授权）、`local` 连接红线、跨项目 `WRT-*`
- **裁决详情**：见 `workbuddy-absorption-map.md`

## 2026-08-23 外部吸收：loop-engineering

- **来源**：`loop-engineering`（skillhub 市场安装源，本地目录 `~/.workbuddy/skills/loop-engineering__skillhub/`）
- **内容**：Loop Engineering AI 编程范式指南（SKILL.md + references/{patterns,config-examples,anti-patterns,integration}.md）
- **落点**：
  - `references/loop-patterns-library.md`（新增，8 模式压缩 + 选择指南，对应外部 patterns.md）
  - `references/safety-mechanisms.md`（补 4/5/6 节，对应外部 anti-patterns.md 反模式 3/5/6）
  - `references/completion-marker-pattern.md`（补独立验证节）
  - `references/loop-config-schema.md`（补 Automation 触发参数心智，对应外部 config-examples.md）
  - `SKILL.md`（范式定位 / /loop 映射 / 模式选择 3 节）
- **裁决详情**：见 `workbuddy-absorption-map.md`
- **已删除源**：吸收完成后已删除本地安装源 `~/.workbuddy/skills/loop-engineering__skillhub/`
