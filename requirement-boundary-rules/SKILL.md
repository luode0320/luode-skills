---
name: requirement-boundary-rules
description: 当需求边界不清、影响范围不明、兼容性不明确、是否允许改旧逻辑不清楚，或需要区分当前需求、历史问题、需求变更和验收偏差时触发。负责明确改动边界和影响面，并将边界结论持续更新到 `requirement-intake-rules` 约定、且路径与命名由 `artifact-storage-rules` 统一定义的同一份需求主文档中；不要用它代替需求缺口识别或 Bug 根因定位 skill。
---

# 需求边界判定规则

只在判断“这件事到底算不算当前需求范围”时使用这个 skill。
如果当前问题是信息缺失，先交给 `requirement-gap-rules`；如果已经确定是历史缺陷，转入 Bug 域。

## Skill 作用与适用场景

- 判断当前问题属于当前需求、需求变更还是历史问题。
- 明确本次允许改哪些层、哪些模块、哪些旧逻辑。
- 识别兼容性影响面和上下游影响面。
- 将边界结论回写到当前需求对应、由 `artifact-storage-rules` 统一约定的同一份需求主文档中。
- 防止把历史遗留缺陷混入当前需求一起做。

## 自动触发信号

- 用户说“顺手一起改一下旧逻辑”。
- 需求实施中暴露出历史问题，不确定该不该一起处理。
- 验收不通过，但原因不确定是理解偏差还是代码缺陷。
- 当前需求可能影响旧接口、旧页面、旧流程或兼容行为。

## 进入后先做什么

1. 先列出当前明确属于本次需求的目标。
2. 再列出被顺带发现的问题、旧逻辑或兼容风险。
3. 判断这些内容属于当前需求、需求变更还是历史缺陷。
4. 找到当前需求对应的需求主文档；如果还没有，就按 `artifact-storage-rules` 的路径与命名模板初始化同一份文档。
5. 给出“纳入本次 / 拆出去 / 转 Bug 域”的结论，并准备回写到该文档。

## 默认执行流程

1. 默认先读 `references/boundary-checklist.md`，判断当前改动边界和影响面。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认需求主文档根目录、入口文件模板和同文档复用策略。
3. 如果涉及历史问题与需求变更的区分，再读 `references/history-vs-change.md`。
4. 如果涉及验收不通过或理解偏差判断，再读 `references/acceptance-routing-examples.md`。
5. 输出当前需求范围、排除项、兼容影响面和建议流转路径，并更新到当前需求对应的需求主文档。
6. 如果该需求还没有文档，则按 `artifact-storage-rules` 的中央目录与入口模板创建同一份需求文档后再更新。
7. 如果问题不属于当前需求范围，不要在需求域内硬做下去。

## 权责边界与不负责事项

- 只负责边界和归属判断，不负责补齐缺失信息，那属于 `requirement-gap-rules`。
- 不负责静态定位或运行时定位代码缺陷，那属于 Bug 域。
- 不直接制定完整验收标准，那属于 `acceptance-criteria-rules`。
- 不因为“可以一起改”就默认放宽边界。
- 不为同一个需求单独新建边界文档；边界结论只能更新同一个需求主文档。

## 需要暂停并确认的条件

- 当前问题既像需求变更，又像历史缺陷，无法单边归类。
- 本次需求如果纳入兼容性调整，会明显扩大改动范围。
- 用户要求同时处理多个历史问题，但未确认这些问题是否并入当前任务。
- 验收不通过，但无法判断是需求理解偏差还是实现错误。

## 执行通过 / 驳回标准

- 通过：能够明确指出哪些属于当前需求、哪些属于需求变更、哪些属于历史问题，以及这些项应如何流转，并将结论回写到同一个需求主文档。
- 驳回：把边界说不清，或把历史问题和当前需求混在一起推进，或把需求偏差直接误判成 Bug。

## 执行结果归档要求

- 将边界结论、排除项、兼容影响面和流转建议记录到当前需求对应的需求主文档。
- 所有需求域相关 skill 都应复用同一个需求文档；边界规则只更新其中的范围、排除项和流转结论。
- 需求主文档的根目录、入口文件模板和复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 归档内容至少包含当前需求范围、拆出项、转 Bug 项和原因。
- 如果本次边界天然清晰且无争议，也应在同一份需求文档中体现最终边界结论，而不是完全不留痕。

## references 读取规则

- 默认先读 `references/boundary-checklist.md`。
- 在定位当前需求主文档、创建初始文档或判断是否继续更新同一文档时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在区分历史问题和需求变更时，再读 `references/history-vs-change.md`。
- 只有在处理验收不通过的归因时，再读 `references/acceptance-routing-examples.md`。
