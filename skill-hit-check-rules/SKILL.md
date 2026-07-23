---
name: skill-hit-check-rules
description: 【强制总控】每轮用户新消息（含新会话第一条）都必须先做命中检查并在首条中间进度输出。凡涉及 Git 协作动作（含显式关键词与隐式语义，如“提交git/帮我提交/commit一下/推送代码/看下状态”），必须联动命中 git-collaboration-rules。凡处理本仓库任务，最低还必须联动命中 `parallel-task-dispatch-rules`，并执行 Obsidian 知识流选择性默认判断，输出 `Obsidian:检索/沉淀/不适用/阻断`；当判断为 `检索` 或 `沉淀` 时必须同时命中 `obsidian-knowledge-flow`。首条中间进度最小必填包含 `命中检查`、`命中技能`，若本轮命中 `parallel-task-dispatch-rules` 还必须追加 `并行技能`。
---

# Skill 命中检查规则（最小闭环版）

## -1.4 极简硬闸门（强制）

- 本 skill 是每轮用户新消息的唯一首入口，必须先完成命中检查，再执行任何领域动作。
- 首条中间进度固定包含：
  - `命中检查:<通过/阻断>; Git规则:<通过/不适用/阻断>`
  - `命中技能:<skill1,skill2,...>`
  - 仓库任务追加 `Obsidian:<检索/沉淀/不适用/阻断>`
  - 命中 `parallel-task-dispatch-rules` 时追加 `并行技能:<skill.../无>`
- 固定字段的 Markdown 形态以 `references/output-format.md` 为准；缺少必填字段即阻断领域执行。

## -1.5 违规处理（强制）

- 若发生“先执行命令、后做命中检查”，立即停止后续命令，补齐固定字段后重走命中流程。
- 不得用额外恢复文案替代固定字段，也不得把迟到的命中声明伪装成首条合规。

## -1. 触发确认（强制）

- 每轮都命中本 skill；自动触发不依赖用户点名，也不因任务简单而跳过。
- 仓库任务联动 `parallel-task-dispatch-rules` 并执行 Obsidian 选择性判断。
- 当前轮存在 Git 意图时联动 `git-collaboration-rules`；只识别当前轮，不继承历史授权。
- 修改 Skill 资产时联动 `skill-execution-compliance-gate-rules`，并按职责边界追加 `skill-evolution-rules`、`skill-audit-rules`。
- 联动条件、用户习惯、负向边界和漏触发防护统一见 `references/hit-checklist.md`；本入口不复制各 Owner 的执行细则。

## -1.0 新会话首轮保障（强制）

- 新会话第一条与普通轮次同等处理，必须先输出命中检查。
- 新会话的规则文件和项目上下文准备交给对应自举或恢复 Skill；本 skill 只负责确认已正确联动，不代替其执行。
- 新会话、上下文恢复或用户发送“继续”“继续任务”“按计划继续”等继续类消息时，首条命中列表必须先把 `task-plan-rehydration-rules` 列为候选 Owner；输出固定命中字段后、任何领域动作前读取并校验 `PROJECT_CURRENT.md`。只有当前回合能证明与活动投影属于同一来源对象时，才真实调用 `update_plan`；失活、损坏、过期、来源不匹配或归属不确定则由该 Owner 明确退出，禁止静默跳过或错投到其它任务。

## -1.1 Git 意图识别（强制）

- Git 关键词、中文动作词、口语表达和语义等价表达的识别清单见 `references/hit-checklist.md`。
- 一旦当前轮命中 Git 意图，必须联动 `git-collaboration-rules`；具体盘点、提交、推送、证据和回退步骤只由该 Skill 定义。

## -1.1.1 Git 仅限当前轮次（新增，强制）

- Git 意图和写历史授权只基于当前轮用户消息。
- 当前轮未出现 Git 意图时，不得沿用先前轮次的提交、推送、合并或同步授权。

## -1.2 Git 判定优先级（强制）

- 同一消息同时命中 Git 与其他领域时，先确认 Git 联动，再进入其他领域判断。
- 本优先级只保证不漏触发，不授权越过 `git-collaboration-rules` 的安全和提交边界。

## -1.3 新会话首轮联动（强制）

- 新会话按当前平台联动规则文件与项目上下文自举；缺失或损坏时由对应 Owner 修复。
- 自举未完成时禁止进入主任务；详细文件范围、幂等和用户内容保护不在本 skill 重复定义。

## 0. 首条消息格式（强制）

- 使用 `templates/hit-check-template.md`，并遵守 `references/output-format.md`。
- 标题、字段、Git、Obsidian 与并行行必须使用普通 Markdown，不得放进代码围栏、缩进代码块或 HTML。

## 1. 最小流程

1. 基于当前轮请求匹配所有可用 Skill 的 `description` 与条件路由。
2. 输出固定首条字段。
3. 执行 Git、并行、Obsidian、Skill 资产及新会话自举的联动摘要判断。
4. 将执行权交给对应 Owner Skill；本入口不复制领域流程。

## 1.1 首条闸门（强制阻断）

- 未完成固定首条字段时，不得执行对应领域命令。
- Git 场景的盘点例外与后续许可边界以 `git-collaboration-rules` 为准。

## 1.2 执行期失败联动（强制）

- 非预期失败或“退出码成功但产物不达标”时，联动 `execution-failure-learning-rules`，不得无变化重试。
- 失败分类、active 案例、恢复和沉淀全部由该 Skill 定义，本入口只负责不漏触发。

## 2. Git 联动闸门（强制）

- 本 skill 只校验当前轮是否正确联动 `git-collaboration-rules`。
- Git 操作、脚本、证据、提交标题和回退检查以 `git-collaboration-rules` 为唯一事实 Owner。

## 2.3 Skill 资产改动联动闸门（强制）

- 本 skill 只输出联动摘要：是否命中执行合规、演进和多 Skill 审计。
- PASS / FAIL、保护语义、迁移证据和字典刷新要求以 `skill-execution-compliance-gate-rules`、`skill-evolution-rules`、`skill-audit-rules` 为准。

## 3. 通过标准

- 每轮先完成固定命中字段，且真实执行所有已命中 Skill 的必要步骤。
- Git、并行、Obsidian、Skill 资产和失败恢复均已正确联动，没有在本入口复制 Owner 细则。
- 最终回复保留 `命中检查:通过`；仓库任务保留 Obsidian 状态；Git 场景保留 `Git规则:通过`。

## 4. 执行文件

- `templates/hit-check-template.md`
- `references/output-format.md`
- `references/hit-checklist.md`
