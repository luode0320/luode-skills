---
name: final-acceptance-rules
description: 当测试与审核均已完成、任务准备最终放行时触发。负责基于需求主文档、验收标准、实施总览/实施周期、测试结果和审核结果做后置最终验收，并将结论单独保存到 `artifact-storage-rules` 约定的最终验收文档中；不要用它代替前置验收标准、功能验证、回归验证或实现审查。
---

# 最终验收放行规则

只在测试和审核都已经完成、当前任务准备做最终放行结论时使用这个 skill。
如果当前问题还是需求未稳定、实施未完成、测试未完成或审核未完成，请先回到相邻域补齐前置条件。

## Skill 作用与适用场景

- 基于前置验收标准逐条判断当前需求是否真正通过。
- 强制检查最终验收输入是否齐备：需求主文档、验收标准、实施总览/实施周期、测试结果、审核结果。
- 将最终放行结论单独沉淀到 `doc/验收/` 下的最终验收文档中，不与需求、实施、测试或审核文档混写。
- 当测试或审核任一未完成时，明确阻断最终验收，不允许口头放行。
- 当需求变更已经影响范围、默认值、交互或交付物时，识别原最终验收是否失效并要求重验。

## 自动触发信号

- 测试已完成，审核已完成，团队准备确认“是否可以正式验收通过”。
- 用户明确要求“做最终验收”“给最终放行结论”“按验收标准逐条确认是否通过”。
- 当前需求已经有验收标准和实施文档，但还缺最终收口判断。

## 进入后先做什么

1. 先确认需求主文档、验收标准文档、实施总览/实施周期文档都已经存在。
2. 再确认测试结果与审核结果已经形成可引用的正式记录。
3. 按验收标准逐条对照当前结果，标记通过 / 不通过 / 阻断。
4. 找到当前需求对应的最终验收文档；如果还没有，就按 `artifact-storage-rules` 的命名模板初始化单独文档。
5. 若发现测试或审核未完成，直接输出“未满足最终验收前置条件”，不要继续伪装放行。

## 默认执行流程

1. 默认先读 `references/final-acceptance-checklist.md`，确认最终验收前置条件是否满足。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认最终验收文档路径、命名模板和同文档更新策略。
3. 再读 `references/final-acceptance-template.md`，按统一结构生成或更新最终验收文档。
4. 如需判断与相邻 skill 的边界，再读 `references/final-acceptance-boundaries.md`。
5. 输出最终验收结论、逐条判定、阻断项和待重验项，并更新到当前需求对应的最终验收文档。
6. 如果还没有最终验收文档，则按 `artifact-storage-rules` 约定的命名规则创建；如同一天存在多个近似标题，在不改变中文语义前提下补充更具体描述以避免重名。
7. 若测试或审核任一未完成，最终验收文档中只能输出“未满足最终验收前置条件”，不得写通过结论。
8. 若需求变更已推翻原验收标准、实施文档或测试结论，必须先回开相邻文档并使当前最终验收状态失效待重验。

## 权责边界与不负责事项

- 只负责后置最终放行，不代替 `acceptance-criteria-rules` 编写前置验收标准。
- 不代替 `functional-validation-rules` 或 `test-regression-rules` 执行测试。
- 不代替 `implementation-review-rules` 或 `project-change-review-rules` 执行审核。
- 不把最终验收结论回写成需求、实施、测试或审核域的平行口径。

## 需要暂停并确认的条件

- 当前无法证明测试是否已经完成。
- 当前无法证明审核是否已经完成。
- 验收标准与实施结果之间存在明显口径冲突。
- 需求已发生变更，但验收标准、实施文档或测试结果尚未同步更新。

## 执行通过 / 驳回标准

- 通过：能够基于需求主文档、验收标准、实施文档、测试结果和审核结果形成最终放行结论，并逐条说明通过 / 不通过 / 阻断状态。
- 驳回：测试或审核未完成就提前放行，或没有对照验收标准逐条判定，或把最终验收结论散落在其他文档中。

## 执行结果归档要求

- 将最终放行结论记录到 `artifact-storage-rules` 约定的最终验收文档中。
- 文档文件名、根目录和同文档更新策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 同一个需求只保留一份最终验收文档；若发生重验，应在同一份文档中更新最新结论并保留失效原因。
- 归档内容至少包含输入材料清单、逐条验收判定、阻断项、遗留项和最终放行结论。

## references 读取规则

- 默认先读 `references/final-acceptance-checklist.md`。
- 在决定最终验收文档的根目录、命名模板和同文档更新策略时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在输出或更新结构化最终验收文档时，再读 `references/final-acceptance-template.md`。
- 只有在判断与相邻 skill 的边界时，再读 `references/final-acceptance-boundaries.md`。
