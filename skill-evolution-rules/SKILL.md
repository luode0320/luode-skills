---
name: skill-evolution-rules
description: 当新增、修改、拆分、合并、迁移或退休团队内部 skill，或发现现有 skill 边界失衡、触发描述失真、references 结构失控时触发。负责维护 skill 体系自身的拆分与演进规则；不要用它代替业务 skill 编写业务细则。
---

# Skill 体系演进规则

只在维护 skill 体系本身时使用这个 skill。
如果当前任务只是完善某一个业务 skill 的正文细节，而不涉及体系结构调整，不要升级到体系演进层。

## Skill 作用与适用场景

- 判断当前变化属于新增、拆分、合并、迁移还是退休。
- 约束 skill 的命名、触发描述、正文边界和 references 结构不要失控。
- 识别哪些规则应该独立成 skill，哪些规则只适合进入现有 skill 的 references。
- 输出受影响 skill 清单、调整顺序和迁移范围。

## 自动触发信号

- 需要新增一个团队内部 skill。
- 发现某个 skill 过宽、过细、抢职责或漏职责。
- 需要把一部分 rules 从 A skill 迁到 B skill。
- 需要合并重复 skill，或退休已经不再适用的 skill。
- 发现 `description`、`SKILL.md` 或 `references/` 结构已经偏离统一规范。

## 进入后先做什么

1. 先判断本次演进属于新增、拆分、合并、迁移还是退休。
2. 再判断影响的是触发层、正文边界、references 结构还是归档规范。
3. 列出受影响的 skill 与文件。
4. 确认是否会影响已稳定 skill 的触发边界或主次关系。

## 默认执行流程

1. 先读取 `references/evolution-patterns.md`，确定本次属于哪种演进模式。
2. 如果涉及拆分或合并，再读取 `references/split-merge-boundaries.md` 判断边界是否合理。
3. 如果涉及 references 或内容迁移，再读取 `references/migration-checklist.md` 检查迁移影响。
4. 输出演进建议、影响范围、执行顺序、需要同步更新的 skill 清单。
5. 在结构决策稳定后退出，不直接代写业务 skill 的具体规则。

## 权责边界与不负责事项

- 只负责维护 skill 体系本身，不代替业务 skill 编写业务规范。
- 不因为发现一个 skill 有问题，就顺手重写整个体系。
- 不绕过既定波次计划，直接大规模改造所有 skill。
- 不把“可继续补充到 references 的小规则”轻易提升为独立 skill。

## 需要暂停并确认的条件

- 拆分后边界仍不清，无法说清各 skill 的职责。
- 合并后 `description` 会明显过宽，导致误触发风险上升。
- 迁移 references 会影响多个已经稳定的 skill，且影响面暂时无法控制。
- 打算退休某个 skill，但它仍承担关键触发职责，且没有明确替代者。

## 执行通过 / 驳回标准

- 通过：能够明确给出演进类型、影响的 skill、调整边界、迁移顺序和需要同步更新的文件。
- 驳回：只有抽象建议，没有明确改动对象、边界、顺序，或让体系变得更混乱、更难触发。

## 执行结果归档要求

- 将演进建议、影响范围、迁移决策、遗留问题记录到 `reports/` 或 `analysis/`。
- 归档内容至少包含当前问题、涉及的 skill、调整理由、拟执行顺序和风险点。
- 如果只是确认“暂不拆、不合并、不迁移”，也要记录结论，避免后续重复讨论。

## references 读取规则

- 默认先读 `references/evolution-patterns.md`。
- 只有在判断是否拆分或合并时，再读 `references/split-merge-boundaries.md`。
- 只有在需要迁移内容、调整 references 或同步多 skill 时，再读 `references/migration-checklist.md`。
