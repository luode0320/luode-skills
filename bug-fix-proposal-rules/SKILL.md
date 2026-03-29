---
name: bug-fix-proposal-rules
description: 当问题已定位，需要形成修改建议、风险评估、备选方案并判断是否应等待用户确认时触发。负责把 Bug 域稳定交接到编码域，并统一记录到 Bug 根目录；不要用它代替根因定位或直接实施编码修复。
---

# Bug 修复建议规则

只在根因已经足够明确、准备从“定位”进入“修改决策”时使用这个 skill。
如果当前根因还不稳定，先回到 `bug-root-cause-rules` 或 `bug-runtime-debug-rules`，不要提前谈修复方案。

## Skill 作用与适用场景

- 把定位结果整理成可执行的修改建议。
- 评估修改范围、风险点、回归影响和备选方案。
- 判断当前问题是否必须先等用户确认，还是可以直接进入编码。
- 将修复建议、风险评估和确认结论统一沉淀到当前 Bug 根目录。
- 作为 Bug 域到编码域的稳定交接层。

## 自动触发信号

- 根因已经基本明确，准备讨论如何改。
- 修改方案可能影响公共模块、共享逻辑、数据库行为或兼容性。
- 需要比较多个修复方向的风险和代价。
- 需要明确哪些情况应先给建议、等确认后再编码。
- 需要把修复建议继续记录到同一个 Bug 根目录中，避免和前序定位记录分散。

## 进入后先做什么

1. 先确认根因结论是否足够稳定。
2. 为当前 Bug 确认统一的根目录，具体路径、目录名和入口文件统一遵循 `artifact-storage-rules`。
3. 列出至少一个主修复方案和必要的影响面。
4. 如果存在明显替代路线，也列出备选方案。
5. 判断当前方案是否必须先经用户确认。

## 默认执行流程

1. 默认先读 `references/fix-proposal-template.md`，按统一模板组织修复建议。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认 Bug 根目录、入口 `README.md` 和同一 Bug 持续复用同一根目录的策略。
3. 如果需要判断风险和影响范围，再读 `references/risk-assessment-checklist.md`。
4. 如果需要判断何时必须等确认、何时可以直接编码，再读 `references/confirm-before-coding.md`。
5. 输出主方案、备选方案、风险点、影响范围、验证方式和确认建议。
6. 将本轮修复建议和确认结论写回当前 Bug 根目录。
7. 在确认条件未满足前，不直接进入编码实施。

## 权责边界与不负责事项

- 只负责修复建议与交接，不负责重新定位根因。
- 不代替编码类 skill 直接实施代码修改。
- 不把“想到一个修复方式”直接等同于“方案已通过”。
- 不跳过风险说明和验证方式，直接给出模糊修复建议。

## 需要暂停并确认的条件

- 根因仍存在多个竞争假设。
- 修改范围会明显扩大到公共模块、共享接口或兼容行为。
- 方案会影响数据库结构、接口契约或已有流程。
- 存在两个以上方案且代价差异明显，需要用户决策。
- 当前 Bug 还没有建立统一的 Bug 根目录，导致修复建议与前序定位记录可能再次分散。

## 执行通过 / 驳回标准

- 通过：能明确给出主方案、影响范围、风险点、验证方式，以及是否需要确认；相关结论统一落在当前 Bug 根目录下。
- 驳回：方案仍停留在口号层，如“改一下这里看看”，完全不说明风险、范围和验证方法，或没有把修复建议继续写回当前 Bug 根目录。

## 执行结果归档要求

- 将修复建议、影响范围、风险评估、确认结论统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 当前 Bug 根目录必须包含 `README.md`，至少写明根因摘要、主方案、备选方案、风险点、验证方式、确认结论和下一步动作。
- Bug 根目录、入口 `README.md` 和同一 Bug 根目录复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果明确结论是“可直接进入编码”，也要保留该判断依据，并继续沿用同一个 Bug 根目录进入后续修复与验证。

## references 读取规则

- 默认先读 `references/fix-proposal-template.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在评估影响范围和风险时，再读 `references/risk-assessment-checklist.md`。
- 只有在判断是否必须先确认时，再读 `references/confirm-before-coding.md`。
