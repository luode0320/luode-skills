# 需求域路由与合并判断

## 对外心智模型

对外统一使用“单一需求入口 + 条件路由 + 下游移交”：

- 需求域主流程：`Idea -> requirement-intake-rules`。
- 条件路由：`initial-discovery`、`gap-routing`、`boundary`、`splitting`、`change`。
- 下游移交：`Acceptance Criteria -> Implementation -> Test -> Review -> Final Acceptance`。

其中：

- `requirement-intake-rules` 是唯一自动触发入口和唯一需求主文档 owner。
- `initial-discovery` 只在粗略 idea、资料不足但可主动查证时进入，负责侦察和找资料。
- `gap-routing` 只处理主动侦察后仍无法补齐、且会影响实现方向的关键缺口。
- `boundary`、`splitting`、`change` 继续由各自专门 Skill 承接。
- 条件路由按触发条件插入，不是每次都默认走完整长链路。

## 内部默认顺序

需求域内部只承接到“需求稳定前”为止：

1. `requirement-intake-rules`：接收新需求、整理资料并维护唯一主需求文档。
2. `initial-discovery`：遇到老板式 idea、资料不全或用户补充侦察入口时，在同一 owner 内主动侦察。
3. `gap-routing`：只处理侦察后仍缺失且会阻断实现方向的内容。
4. `requirement-boundary-rules`：范围、兼容、历史问题归属不清时裁决影响范围。
5. `requirement-splitting-rules`：需求体量过大或跨多个子系统时拆出可独立闭环的子项。
6. `requirement-change-rules`：已澄清或已实现需求发生新增条件、优先级或交付物变化时重算影响。
7. 条件路由收敛后，需求域结束并向下游移交。

## 下游移交顺序

1. `acceptance-criteria-rules`：把稳定后的需求目标转成可验证、可测试、可复核的前置验收标准。
2. `implementation-planning-rules`：把当前优先闭环转成编码前实施总览、实施周期、文件落点和验证点。
3. 需求主文档、前置验收标准和实施规划都真实落盘，且用户再次明确开工、执行计划、完成定义、停止条件和最大推进边界齐备后，才允许正式编码。
4. 测试域按实施周期执行功能、回归和测试收口。
5. 审查域按实施周期完成实现审查和当前改动审查。
6. `final-acceptance-rules` 在测试和审查完成后做最终放行。

## 合并判断

本周期采用“单主入口 + 条件路由”，而不是保留多个同生命周期竞争入口：

- `initial-discovery` 的深度侦察职责已迁入 `requirement-intake-rules` 的条件路由，不再单独占用自动触发入口。
- `gap-routing` 保留为后续条件路由，不覆盖可通过侦察解决的问题。
- `boundary` 是范围裁决，不能被接入或缺口规则顺手处理。
- `splitting` 是体量和闭环拆分，不是需求补全。
- `change` 是已进入流程后的变更重算，不是初始 idea 接入。
- 验收、实施和最终验收是下游产物，不能提前吃掉前置不确定性。

## 允许吸收的重叠

- 主入口保留轻量项目上下文确认；深度侦察只在 `initial-discovery` 路由中执行。
- `gap-routing` 只处理侦察后仍无法补齐的关键内容；能主动查到的缺口必须先回到 `initial-discovery`。
- `requirement-change-rules` 只处理已存在需求的变更；新增内容若本质上是新 idea，回到 `initial-discovery`。

## 跳转规则

- 用户只给 idea：命中 `requirement-intake-rules` 后进入 `initial-discovery`。
- 用户给完整资料包：可直接进入主入口；资料互相矛盾或需要补查时进入 `initial-discovery`。
- 用户给额外项目路径、URL、数据库、GitHub、第三方服务或 API 文档入口：进入 `initial-discovery` 扩展侦察。
- `initial-discovery` 输出后立即创建或更新同一份需求主文档，再按需进入 `gap-routing`、`boundary`、`splitting` 或 `change`。
- 侦察后仍缺关键业务取舍：一次只推进一个真实关键缺口问题，不预填业务答案。
- 主入口文档中仍有关键事实缺失：先判断能否进入 `initial-discovery`，不能再进入 `gap-routing`。
- 任一关键条件路由未收敛时，阻断进入 `acceptance-criteria-rules` 与 `implementation-planning-rules`。
- 正式需求主文档未真实落盘前，不得进入实施规划或正式编码；实施计划确认后仍需用户明确开工指令。
- 实施规划保持只读，按“依赖图 + 垂直切片”拆最小闭环任务，单任务默认尽量控制在约 5 个文件以内。
- 用户已明确开工且计划边界齐备后，按“最小任务实现 -> 测试 -> 审查 -> 验收 -> 下一任务 -> 周期收口”的顺序自动推进。
