---
name: requirement-change-rules
description: 当已确认或已进入实现的需求被补充、修正、插入新条件、改变优先级、调整默认值、范围或交付物形态时专项自动触发。负责变更分类、影响失效传播、回流边界/Bug/拆分的判断，以及向验收、实施、测试和审查 Owner 发出重开与重规划信号；结论回写到 `requirement-intake-rules` 维护、由 `artifact-storage-rules` 定位的同一份需求主文档。它不拥有实施总览或实施周期结构；信息不全转 `requirement-intake-rules#gap-routing`，原实现不符合原需求转 Bug 域。
---

# 需求变更确认规则

## 职责与触发

- 只处理已经存在的需求发生语义变化，不处理初始接入或历史缺陷。
- 编码中追加字段、规则、页面、接口、异常分支，修改默认值、优先级、兼容、范围或交付物时自动触发。
- 修改、整理或完善已有需求 Markdown 时，必须执行变更影响检查；图形、边界、验收、计划、测试和审查结论受影响时必须标记失效。
- `CHG-*`、授权、旧值/新值、失效传播、回开和重验字段只由 `references/impact-recheck.md` 定义。

## 路由

- 只是初始资料、字段、流程或关键前提不全：转 `requirement-intake-rules#gap-routing`；可主动查证时先走 `initial-discovery`。
- 原实现不符合原需求、脱离本次变更仍是错误：转 Bug 域。
- 变更导致范围或兼容归属不清：转 `requirement-boundary-rules`。
- 变更导致需求显著增大或出现多个独立子系统：转 `requirement-splitting-rules`。
- 变更影响前置验收：回开 `acceptance-criteria-rules`；影响实施、测试或审查：发出失效和重规划信号，交对应 Owner 处理。

## 职责归位

- 本 Skill 更新唯一需求主文档中的变更记录、影响面、失效状态和决策结论，不定义实施总览、周期、文件/符号或测试命令的文档结构。
- 用户明确要求同时补充需求与实施文档时，必须先完成需求变更收口，再强制移交 `implementation-planning-rules` 更新受影响实施总览和周期，并核对哪些周期受影响、哪些不受影响；不得只补一侧。
- 原需求已实现后新增改动时，必须声明旧周期不可覆盖，并由 `implementation-planning-rules` 为本次改动创建新的实施周期闭环。
- 文件/符号、周期、任务、真实测试、清理和任务级回滚不得删除，而是由下游 Owner 根据本 Skill 的失效清单重新冻结。

## 最小执行流程

1. 读取 `../requirement-intake-rules/references/requirement-domain-shared-contract.md`，定位唯一需求主文档和当前 Owner。
2. 读取 `references/change-classification.md` 分类变更；读取 `references/impact-recheck.md` 生成唯一 `CHG-*`、旧值/新值、受影响结论和回开清单。
3. 需要正反例时读取 `references/change-decision-examples.md`，判断继续当前任务、拆新项、回流 boundary/splitting 或转 Bug。
4. 回写同一需求主文档，保留来源、差异、授权、图表影响、清理、回滚和证据；未授权默认值不得写成确定结论。
5. 根据失效清单依次回开前置验收、实施规划、测试和审查 Owner；最终落盘由 `artifact-delivery-gate-rules` 核验。

## 暂停、通过与驳回

- 暂停：变化内容含糊；会推翻既有边界、方案或测试但尚未确认；多次变更使原目标失真；变更来源或决策权不清。
- `P0/P1` 未授权时保持 `blocked`；P2 默认值也必须记录授权人、有效期和复核证据。用户明确暂停或停止时立即停止扩散。
- 通过：变化、分类、旧值/新值、影响失效、回开 Owner 和重验信号清晰，已回写同一主文档并保留回滚证据。
- 驳回：直接把新增条件塞进实现、把 Bug/gap/boundary 误判为 change、只更新需求不移交受影响实施/验收，或覆盖已完成旧周期。
- 变更关闭后必须由对应 Owner 重跑文档机器校验和受影响行为测试；证据不全不得恢复原完成状态。

## References

- 共享路由与保护语义：`../requirement-intake-rules/references/requirement-domain-shared-contract.md`
- 变更分类：`references/change-classification.md`
- `CHG-*`、失效传播、授权、回开与重验：`references/impact-recheck.md`
- 变更正反例：`references/change-decision-examples.md`
- 实施总览、周期、文件/符号和测试闭环：`../implementation-planning-rules/SKILL.md`
- 前置验收：`../acceptance-criteria-rules/SKILL.md`
- 文档路径与最终落盘：`../artifact-storage-rules/references/path-map.yaml`、`../artifact-delivery-gate-rules/references/plain-language-document-contract.md`、`../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`
