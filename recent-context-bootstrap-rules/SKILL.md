---
name: recent-context-bootstrap-rules
description: 当当前会话刚开始、缺少历史上下文、用户直接提出与当前项目相关的需求、Bug、编码、测试或交付问题时自动触发；也可在 context-compression-rules 按共享 context-recovery-contract 确认缺少继续任务所需的近期事实后被条件调用。负责优先从 `artifact-storage-rules` 约定的近 3 天需求、测试、Bug、文档、项目专属 skill 根目录和 git 提交中提取最近活动，并按需加载系统的所有 skills 与当前项目根目录下 `./skill`、`./.skills` 的 skill 清单；如果当前任务涉及整项目分析、架构梳理或模块总览，也可额外读取根目录 `项目设计.md` 及其同类设计文档作为弱参考源，但不把它当成最新事实；不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线、project-design-doc-rules 的设计文档同步，或当前主域本身的分析执行。
---

# 新会话上下文预热规则

只在新会话缺少最近项目事实时自动触发，或在压缩恢复已明确判定 `recent_context_state=missing` 后被条件调用。
当前上下文已充分、任务与项目无关，或压缩恢复仍是 `uncertain` 时不得触发。

## Skill 作用与适用场景

- 为新会话补充与当前任务直接相关的近 3 天项目事实。
- 为压缩恢复只补共享契约记录的明确缺失项，不重复执行完整恢复流程。
- 优先压缩最近需求、Bug、测试、文档、Skill 和提交，不做深度历史回忆。
- 按需建立全局与项目 Skill 的最小能力索引，完成后立即让路给主域。
- 项目设计类文档只能作为弱参考，不能压过当前代码、工作区和最近变更。

## 自动触发信号

- 新会话刚开始，当前任务与项目直接相关且缺少必要的最近事实。
- 用户在新会话说“继续”“接着上次做”“看看最近改了什么再做”，但本轮没有足够上下文。
- 当前任务强依赖最近几天项目动态，轻量预热能显著降低误判。
- `context-compression-rules` 已按共享契约记录 `recent_context_state=missing` 和明确缺失项。

## 进入后先做什么

1. 确认入口是新会话缺上下文，或压缩恢复的条件调用；其他场景立即让路。
2. 条件调用时读取 `../context-compression-rules/references/context-recovery-contract.md`，只处理已记录的缺失项。
3. 将扫描范围限制为近 3 天，并优先读取 `artifact-storage-rules` 定义的现有来源；目录不存在时跳过。
4. 按需读取系统 Skill 与项目 `./skill`、`./.skills` 的 frontmatter 和 agents 元数据，不加载无关正文。
5. 整项目分析场景才弱读取项目设计类文档，并明确标注弱参考。
6. 输出来源、补齐项、仍缺项和主域交接点，然后退出。

## 默认执行流程

1. 读取 `references/bootstrap-sources.md` 确认近 3 天来源、优先级和缺省处理。
2. 压缩恢复条件调用时先读取共享 `context-recovery-contract.md`，锁定缺失项与最大扫描边界。
3. 按需加载最小 Skill 索引，并读取 `references/boundary-rules.md` 确认让路关系。
4. 需要统一摘要时读取 `references/output-format.md`。
5. 扫描相关来源和必要的 Git 提交线索；不扩大到完整历史。
6. 输出相关事实、来源、时间范围、弱参考、仍缺项和主域交接点。
7. 立即让路，不在预热层继续主任务。

## 权责边界与不负责事项

- 不负责完整历史回忆、长期项目时间线或设计文档同步。
- 不代替需求、Bug、编码、测试、审查、验收或交付。
- 不把“近 3 天没有材料”解释成“任务没有前置上下文”，也不以猜测补缺。
- 不因预热获得材料就恢复或扩大编码、Git、部署等授权。
- 用户明确停止、终止或不要继续时，不得通过预热重启任务。

## 需要暂停并确认的条件

- 当前任务与项目无关，扫描只会引入噪音。
- 当前上下文已足够，或压缩恢复状态不是明确的 `missing`。
- 近 3 天没有可靠材料，无法补齐已记录缺失项。
- 来源冲突且无法以当前代码、工作区或用户消息裁决。
- 用户明确暂停、停止、终止或限制扫描范围。

## 执行通过 / 驳回标准

- 通过：仅在合法入口触发，在限定时间和缺失项范围内提供来源、补齐项、仍缺项与交接点。
- 驳回：每次压缩都自动触发、扩大扫描边界、把弱参考写成事实、恢复历史授权或停留在预热层执行主任务。

## 执行结果归档要求

- 默认不新建持久化文档；预热结果进入当前会话或主任务既有产物。
- 条件调用至少记录原缺失项、补齐来源、补齐结果和仍然阻断的内容。
- 持久化由主域或项目记忆 Owner 决定，本 skill 不越权写入。

## references 读取规则

- 最近来源：`references/bootstrap-sources.md`
- 共享恢复契约：`../context-compression-rules/references/context-recovery-contract.md`，仅条件调用时必读
- 边界与不触发：`references/boundary-rules.md`
- 摘要格式：`references/output-format.md`
