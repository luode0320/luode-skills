---
name: final-acceptance-rules
description: 当测试与审核均已完成、任务准备最终放行时触发。负责基于来源对象文档（需求或 Bug）、验收标准、实施总览/实施周期、测试结果和审核结果做后置最终验收，并将结论单独保存到 `artifact-storage-rules` 约定的最终验收文档中；不要用它代替前置验收标准、功能验证、回归验证或实现审查。
---

# 最终验收放行规则

只在当前任务准备做最终放行结论时使用这个 skill。测试和审核是否必须完成，先按共享条件化门禁契约判断；不适用项不阻断，受限项允许继续准备但不能正式放行，明确必需且没有替代验证的项才阻断正式放行。

Git 提交例外：仅为 `git commit` 准备提交时，只执行 `git-collaboration-rules` 对当前 staged 改动要求的基础审查、验收步骤和证据输出；不得因此自动触发本 skill、执行正式最终验收或创建/更新 `doc/7-验收/` 文档。用户明确要求最终验收，或在非 Git 提交场景准备正式放行时，仍完整执行本 skill 的原有验收和归档规则。

## Skill 作用与适用场景

- 基于前置验收标准逐条判断当前来源对象（需求或 Bug）是否真正通过。
- 强制检查最终验收输入是否齐备：来源对象文档、验收标准、实施总览/实施周期、测试结果、审核结果。
- 强制检查实施范围内的周期与最小任务闭环状态：所有纳入本轮验收的实施周期必须已按顺序收口，且每个最小任务都有实现、真实测试、审查、验收证据。
- 将最终放行结论单独沉淀到 `doc/7-验收/` 下的最终验收文档中，不与需求、Bug、实施、测试或审核文档混写。
- 根据 `review_acceptance_gates` 区分“可继续推进”“受限交接”和“正式放行”，不把不适用项误判为阻断。
- 当来源对象变更已经影响范围、默认值、交互、修复口径或交付物时，识别原最终验收是否失效并要求重验。

## 自动触发信号

- 测试已完成，审核已完成，团队准备确认“是否可以正式验收通过”。
- 用户明确要求“做最终验收”“给最终放行结论”“按验收标准逐条确认是否通过”。
- 当前来源对象已经有验收标准和实施文档，但还缺最终收口判断。
- 仅准备 Git 提交、且未提出正式最终验收或非 Git 正式放行时，不属于本 skill 的自动触发信号；该场景仅按 `git-collaboration-rules` 完成 staged 改动相关的基础核查与证据。

## 进入后先做什么

1. 先确认来源对象文档、验收标准文档、实施总览/实施周期文档都已经存在，且实施文档记录了周期顺序、期次定位、周期内最小任务顺序和闭环状态。
2. 再确认测试结果（包含功能验证、回归验证、项目级上线接口测试门禁结论）与审核结果已经形成可引用的正式记录。
3. 再确认本轮验收范围内的全部实施周期都已收口；只对门禁中标记为当前必须完成的验证检查实现、真实测试、审查和验收闭环。
4. 按验收标准逐条对照当前结果，标记通过 / 不通过 / 阻断。
5. 找到当前来源对象对应的最终验收文档；如果还没有，就按 `artifact-storage-rules` 的命名模板初始化单独文档。
6. 若发现明确必需、当前必须完成且没有替代验证的门禁未完成，输出“未满足正式放行条件”；若只是受限，输出“可继续但待补验”，不得写成正式通过。

## 默认执行流程

1. 默认先读 `references/final-acceptance-checklist.md`，确认最终验收前置条件是否满足。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认最终验收文档路径、命名模板和同文档更新策略。
3. 再读 `references/final-acceptance-template.md`，按统一结构生成或更新最终验收文档。
4. 如需判断与相邻 skill 的边界，再读 `references/final-acceptance-boundaries.md`。
5. 输出最终验收结论、逐条判定、阻断项和待重验项，并更新到当前来源对象对应的最终验收文档；结论为“不通过/待重验”且确实无法正式放行时，按 `../artifact-delivery-gate-rules/references/task-blocker-closure-contract.md` 创建或引用去重的 `BLK-*`，给出补测/补审/回改后的重验入口。
6. 如果还没有最终验收文档，则按 `artifact-storage-rules` 约定的命名规则创建；如同一天存在多个近似标题，在不改变中文语义前提下补充更具体描述以避免重名。
7. `not_applicable` 不要求不存在的证据；`limited` 必须记录替代验证、人工补验方式和通过标准，并只能输出受限交接结论。
8. 只有来源明确要求、当前必须完成且没有验证或替代验证时，最终验收文档才输出阻断；文档完整性、追踪和失效链接等硬门禁仍按原规则阻断。
9. 若来源对象变更已推翻原验收标准、实施文档或测试结论，必须先回开相邻文档并使当前最终验收状态失效待重验。

## 权责边界与不负责事项

- 只负责后置最终放行，不代替 `acceptance-criteria-rules` 编写前置验收标准。
- 不代替 `functional-validation-rules` 或 `test-regression-rules` 执行测试。
- 不代替 `implementation-review-rules` 或 `project-change-review-rules` 执行审核。
- 不把最终验收结论回写成需求、Bug、实施、测试或审核域的平行口径。

## 需要暂停并确认的条件

- 当前无法证明测试是否已经完成。
- 当前无法证明审核是否已经完成。
- 验收标准与实施结果之间存在明显口径冲突。
- 来源对象已发生变更，但验收标准、实施文档或测试结果尚未同步更新。

## 执行通过 / 驳回标准

- 通过：能够基于来源对象文档、验收标准、实施文档、测试结果和审核结果形成最终放行结论；实施范围内周期已按顺序收口，每个最小任务都有实现、真实测试、审查、验收证据，并逐条说明通过 / 不通过 / 阻断状态。
- 驳回：测试或审核未完成就提前放行，或实施周期未按顺序收口，或任一纳入验收范围的最小任务缺少实现、真实测试、审查、验收证据，或没有对照验收标准逐条判定，或把最终验收结论散落在其他文档中。

## 执行结果归档要求

- 将最终放行结论记录到 `artifact-storage-rules` 约定的最终验收文档中。
- 文档文件名、根目录和同文档更新策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 同一个来源对象只保留一份最终验收文档；若发生重验，应在同一份文档中更新最新结论并保留失效原因。
- 归档内容至少包含输入材料清单、实施周期收口状态、最小任务闭环证据清单、逐条验收判定、阻断项、遗留项和最终放行结论。
- 最终结论为“不通过/待重验”且属于真实阻断时，文档必须包含共享契约的完整“任务阻断收口”；同根因已有 `BLK-*` 时引用该记录。`limited` 只能保留替代验证与人工补验交接，`not_applicable` 和非阻断遗留项不得创建阻断记录。

## references 读取规则

- 默认先读 `references/final-acceptance-checklist.md`。
- 必须读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，按结构化门禁判断正式放行，不使用“测试或审核未完成即一律阻断”的旧口径。
- 在决定最终验收文档的根目录、命名模板和同文档更新策略时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在输出或更新结构化最终验收文档时，再读 `references/final-acceptance-template.md`。
- 只有在判断与相邻 skill 的边界时，再读 `references/final-acceptance-boundaries.md`。
- 输出最终验收文档前，必须读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`。正文先说明放行结论及验收适用性；不适用项必须有原因和依据，不得无故阻断。
- 最终结论为“不通过/待重验”且属于真实阻断时，必须读取 `../artifact-delivery-gate-rules/references/task-blocker-closure-contract.md`；`limited` 与 `not_applicable` 不适用该契约。

