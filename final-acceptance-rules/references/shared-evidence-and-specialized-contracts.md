# 最终放行的共享证据与专属契约

## 用途

本文件是 `CYCLE-SS-05` 的条件路由落点：将该 owner 的共享证据、暂停、结论、归档与阻断细则从入口文件下沉到可按需读取的 reference。自动触发入口、触发 aliases、阶段职责、用户习惯、授权、安全、停止边界、输出和证据归档均保持有效；不得因下沉而省略任何原有检查。

## 使用顺序

1. 先由同目录 `SKILL.md` 依据原自动触发条件确认本 owner 的专属阶段。
2. 在读取证据、作出结论、归档或处理阻断前读取本文件。
3. 按本文件中的原有 references 路由读取细节；专属阶段职责仍以 `SKILL.md` 为准。
4. `code-review-automation-rules` 仍是提交级专责审查入口，不得因本文件的通用证据契约被合并、删除或替代。

## 保护语义

- 保留自动触发与原 `description`、trigger aliases；没有命中本 owner 的专属条件时不得误触发。
- 保留用户习惯、授权与停止边界、local 环境安全、输出协议、证据归档、回滚/重验和任务阻断规则。
- 本文件是 owner 内的引用化去重，不是删除 owner、合并阶段职责或用模型默认能力替代规则。

## 原 owner 细则（迁移自 `SKILL.md`）

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
