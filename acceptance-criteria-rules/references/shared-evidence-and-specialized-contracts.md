# 前置验收标准的共享证据与专属契约

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

1. 先确认需求目标和边界已经基本稳定。
2. 把用户期望拆成可观察、可判断、可复核的结果描述。
3. 补齐成功条件、失败条件、异常处理、边界限制和范围外说明。
4. 找到当前来源对象（需求或 Bug）对应的验收标准文档；如果还没有，就按 `artifact-storage-rules` 的命名模板初始化单独的验收标准文档。
5. 检查这些标准是否真的能被实现和测试直接使用，并准备回写到该验收标准文档。

## 默认执行流程

1. 默认先读 `references/acceptance-template.md`，先按统一结构写验收标准。
2. 如需继续展开，再读 `references/testable-criteria-checklist.md`，需要检查验收标准是否真的可测可判。
3. 需要对照边界或正反例时，再读 `references/acceptance-boundaries.md`，需要判断验收标准与需求边界、测试执行的边界。
4. 输出结构化验收标准、边界口径和验证关注点，并更新到当前来源对象对应的验收标准文档。
5. 如果该来源对象还没有验收标准文档，则按 `artifact-storage-rules` 约定的命名规则创建；如同一天存在多个近似标题，在不改变中文语义前提下补充更具体描述以避免重名。
6. 对复杂验收路径补齐图形化说明（至少一张流程图或决策矩阵表），并检查与文字标准一致。
7. 验收标准明确后，如果当前实现路径仍复杂、涉及多个模块或多个验证点，先转交 `implementation-planning-rules`；只有实施路径已经足够清晰时，才可直接进入实现。
8. 功能正确性验证转交 `functional-validation-rules`，兼容性和旧能力回归转交 `test-regression-rules`。

## 权责边界与不负责事项

- 只负责写清验收标准，不直接执行测试，那属于测试域。
- 不代替 `requirement-intake-rules` 的 `gap-routing` 补基础信息；前提没补齐时不要硬写验收。
- 不代替 `requirement-boundary-rules` 决定是否允许修改旧逻辑，但要把范围外写清。
- 不把实现方案、技术细节和验收标准混写在一起。
- 不把验收标准直接混写进需求文档或 Bug 文档；验收标准必须单独维护在 `artifact-storage-rules` 约定的验收标准文档中。

## 需要暂停并确认的条件

- 来源对象目标和边界还不稳定，写出来的验收标准随时会失效。
- 连输入输出和关键场景都不清，无法写成可验证条件。
- 主路径、异常路径或兼容要求存在明显争议。
- 当前团队想用测试执行结果反推验收标准，而不是先定义标准。

## 执行通过 / 驳回标准

- 通过：能够形成可验证、可测试、可复核的验收口径，至少覆盖主流程、异常流程、边界条件、范围外事项和通过标准，并回写到当前来源对象对应的验收标准文档。
- 驳回：仍停留在“体验更好”“支持一下”“处理正确”这类抽象描述，无法指导实现与验证。

## 执行结果归档要求

- 将验收标准记录到 `artifact-storage-rules` 约定的验收标准文档中，不与需求文档或 Bug 文档混写。
- 文档文件名、根目录和同文档更新策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 同一个来源对象的验收标准应持续更新同一份验收标准文档，而不是重复新建多份平行验收记录。
- 归档内容至少包含场景、输入、预期结果、异常分支和范围外说明。
- 对多分支或高风险场景，归档应附图形化表达（流程图或决策表）以减少口径歧义。
- 如后续验收标准发生变化，应保留版本差异，避免实现和测试口径错位。

## 极致完整性与可执行性硬闸门

- 每条 `AC-*` 必须绑定至少一个 `REQ-*` / `RULE-*`，并写清场景、前置状态、输入样本、执行动作、预期输出、异常结果、边界、清理方式和通过/失败判定。
- “符合预期”“处理正确”“体验良好”等抽象表述必须改写成可观察断言、数值阈值、错误码、状态或证据文件；无法量化时必须说明判定人、判定依据和复核证据。
- 主路径、异常路径、边界路径和范围外路径必须分开列出；缺少任一路径时写 `N/A + 原因 + 证据`，不能省略。
- L2 及以上至少保留一张与验收 ID 对应的 Mermaid 流程图或决策图；跨角色场景必须补时序图，状态迁移必须补状态图。
- 验收标准必须能被实施计划直接引用，不能要求实施模型自行决定测试数据、环境、断言或清理方式。未决验收口径必须阻断进入实施规划。

## references 读取规则

- 默认先读 `references/acceptance-template.md`。
- 当验收标准需要交给普通模型执行，或需求复杂度为 L2 及以上时，同时读取 `../requirement-intake-rules/references/extreme-completeness-standard.md`，复用稳定 ID、N/A 证据、图形和双向追踪契约。
- 在决定验收标准文档的根目录、命名模板和同文档更新策略时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在 检查验收标准是否可验证 时，再读 `references/testable-criteria-checklist.md`。
- 只有在 判断与相邻 skill 的边界或对照样例 时，再读 `references/acceptance-boundaries.md`。
- 输出验收标准前，必须读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`。正文必须先说明本次验收是否适用；不适用时写明原因和依据而不阻断，只有明确必需且无替代验证时才阻断。
- 同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，将浏览器、第三方和专项验收条件写入 `review_acceptance_gates`，不要用缺少外部条件替代“本次不适用”的判定。
