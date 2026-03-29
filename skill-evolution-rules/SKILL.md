---
name: skill-evolution-rules
description: 当研发任务已经进入需求、Bug、编码、审查、测试或交付主流程，且当前已命中的 skill 在执行中暴露出触发不准、规则缺失、边界不清、references 不足、归档约定缺失或无法覆盖当前高频场景，继续推进只能依赖临时口头补充时触发。负责判断这是业务问题还是 skill 问题，明确应补哪个现有 skill、是否需要新增相邻 skill、给出最小完善建议，并在必要时先暂停当前任务；待 skill 更新并重新加载后，再回到原任务继续执行。不要用它代替需求补齐、Bug 定位或具体代码实现。
---

# Skill 演进规则

只在“当前卡点来自 skill 体系本身不完善”时使用这个 skill。
如果当前问题本质上是需求不清、Bug 未定位、代码没写对、测试没做完，不要把业务问题错判成 skill 问题。

## Skill 作用与适用场景

- 识别当前阻塞到底是业务问题、工程问题，还是 skill 缺口问题。
- 判断应补当前 skill、补相邻 skill，还是确实需要新增一个独立 skill。
- 输出最小化完善建议，避免因为一个小空档就重写整套规则。
- 在 gap 会直接影响当前任务正确性时，先阻断主流程，要求补 skill 后再继续。
- 在 gap 只是非阻断型细节时，允许先记录建议，再继续当前任务。
- 让 skill 体系具备“边用边补、补完重载、继续执行”的自演进能力。

## 自动触发信号

 - 当前已经命中了某个 skill，但执行时发现它没有覆盖当前真实高频场景。
 - 当前 skill 的 `description` 触发信号过宽、过窄或经常误命中。
 - 当前 skill 的正文只有原则，没有足够流程、判定标准或相邻边界说明。
 - 当前 skill 的 `references/` 信息明显过空，导致复杂场景只能临时口头补规则。
 - 当前任务已经因为 skill 缺口反复停顿、重复解释或临时手写补丁式规则。
 - 团队在执行中明确提出“这个 skill 还不完善，应该先补 skill 再继续”。
 - 当前 gap 已经不是一次性例外，而是未来会重复命中的稳定场景。

## 进入后先做什么

1. 先写清当前正在执行哪个主任务、命中了哪个 skill、卡在了哪一步。
2. 先判断这是不是业务信息缺口、Bug 证据缺口或测试条件缺口，而不是先假定 skill 有问题。
3. 如果确实是 skill gap，再判断缺的是触发 description、执行流程、边界、references、归档约定还是验收标准。
4. 先倾向补现有 skill，不默认新增 skill。
5. 只有在场景高频、职责边界稳定、现有 skill 明显承接不住时，才建议新增独立 skill。
6. 判断当前 gap 是否会直接影响当前任务正确性，决定是否先暂停主流程。

## 默认执行流程

1. 默认先读 `references/gap-signals.md`，确认当前到底是不是 skill gap，而不是业务问题或环境问题。
2. 再读 `references/evolution-decision-matrix.md`，判断应补旧 skill、补相邻 skill、只补 references，还是确实新增独立 skill。
3. 如果需要留痕或回写阻断结论，再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认项目文档根目录和当前主任务记录的复用策略。
4. 需要输出结构化完善建议时，再读 `references/improvement-output-template.md`。
5. 需要明确“补完 skill 以后如何继续当前主流程”时，再读 `references/resume-workflow.md`。
6. 输出本次 skill gap 结论：目标 skill、缺口类型、是否阻断、最小修改建议、建议修改文件、修改后验收方式、回到原任务的重启点。
7. 如果 gap 属于阻断级，先暂停当前任务，完善 skill 并重新加载后，再回到原主流程继续。
8. 如果 gap 属于非阻断级，可以先记录建议，再在当前任务收口后安排 skill 回补，但不能假装这个 gap 不存在。

## 权责边界与不负责事项

- 只负责识别和推动 skill 演进，不代替需求澄清、Bug 定位、编码实现、测试验证。
- 不把一次性低频例外一律升级成“必须新增 skill”。
- 不因为发现小缺口就无限放大改造范围，优先采用最小回补。
- 不在当前任务本质还是业务问题时，错误地把锅甩给 skill 体系。
- 不直接替用户决定要不要大规模重构整套 skill，必须给出理由和边界。

## 需要暂停并确认的条件

- 当前无法判断这是业务问题还是 skill gap。
- 当前要改的不只是一个 skill，而是会牵动多个域的大范围重构。
- 团队希望新增独立 skill，但其职责与现有 skill 高度重叠。
- 当前 gap 会直接影响本次实现正确性、验证可靠性或归档一致性。
- 当前建议仍停留在“感觉不够好”，无法具体说明要补什么。

## 执行通过 / 驳回标准

- 通过：能够明确说清楚是哪个 skill 不完善、缺在哪里、为什么会影响当前任务、建议补哪些文件、是否阻断当前任务，以及补完后从哪一步继续。
- 驳回：只是泛泛地说“这个 skill 不行”，没有目标 skill、没有缺口类型、没有修改建议、没有恢复路径，或把业务问题误判成 skill 问题。

## 执行结果归档要求

- 如果 gap 属于阻断级、会影响多个任务重复命中，或需要后续正式修改 skill，默认在 `artifact-storage-rules` 约定的项目文档根目录中留存一份 skill 完善建议。
- 如果当前已有需求主文档、Bug 根目录或测试主说明，也应在对应主记录中简要写明“当前任务因哪个 skill 缺口被阻断 / 被提醒回补”。
- 归档内容至少包含当前任务、目标 skill、缺口类型、阻断级别、建议修改文件、建议修改内容、验收方式和恢复执行点。
- 项目文档根目录和当前主任务记录的复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。

## references 读取规则

- 默认先读 `references/gap-signals.md`。
- 只有在判断该补旧 skill、补相邻 skill 还是新增独立 skill 时，再读 `references/evolution-decision-matrix.md`。
- 只有在需要输出正式完善建议时，再读 `references/improvement-output-template.md`。
- 只有在需要决定归档位置或回写当前主任务记录时，再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在需要明确补完后如何回到原任务继续执行时，再读 `references/resume-workflow.md`。
