---
name: knowledge-flow
description: 将固定根目录的 Google Drive 知识库作为跨项目知识库管理，并与项目根目录四件套分层：父目录通用规则、PROJECT_CURRENT.md、PROJECT_MEMORY.md 和 PROJECT_HISTORY.md 负责项目本地启动上下文，知识库仍采用选择性默认触发。每轮先判断知识库四态（检索、沉淀、不适用、阻断）；只有问题依赖跨项目历史决策、知识库内容、用户偏好、重复实体或既有笔记时才通过标准文件工具检索，收口形成可复用事实、决策、流程、定义、偏好、来源或调试经验时才通过标准文件工具沉淀；知识库可迭代更新而非只增量堆积。适用于知识库、Markdown 知识管理、第二大脑、知识图谱、自动会话笔记、知识提取、快速回忆、本地笔记库、知识库检索、会话总结沉淀、执行失败持续学习和文件系统笔记操作场景。
---

# 知识库知识流

## 目标

用本 skill 把一个 Google Drive 同步的普通 Markdown 文件夹变成固定根目录、文件系统驱动、本地优先、可自生长的跨项目知识库，同时明确项目本地四件套与知识库不混用。它围绕五条循环工作：

- retrieve: 在会话开始、上下文恢复或回答依赖历史知识的问题前，先从知识库检索相关笔记。
- capture: 在会话总结或阶段收口时，把有复用价值的会话信息保存为 Markdown 笔记。
- distill: 把会话中的稳定事实、决策、流程、定义和偏好沉淀为长期知识。
- iterate: 写入前先判定新信息是补充、矛盾未裁决还是取代旧结论；判为取代时按分级处置改状态、归档或删除旧笔记，并双向写入接替关系。知识库因此可迭代更新，而不是只增量堆积。
- learn: 把已确认的非预期执行失败转成一篇追加式、脱敏的执行案例笔记；笔记同时保存反例、正例、验证证据和状态事件，供后续精确检索。

所有笔记读写使用标准文件工具（Get-Content、Set-Content、Add-Content、Move-Item、Remove-Item、rg、Select-String），不再依赖任何 CLI 桥接层。

## 项目本地四件套边界

项目启动上下文由项目目录父目录的当前平台规则文件，以及项目根目录下的三个文件组成：

1. PROJECT_CURRENT.md：当前目标、范围、状态、待办、阻断、验证和交接点，覆盖式维护，最大 51,200 字节。
2. PROJECT_MEMORY.md：稳定项目规则、关键决策和少量长期事实；已有机器索引区继续保留，不承载当前状态或历史流水。
3. PROJECT_HISTORY.md：关键历史事件，只追加；普通启动不读，只有历史追问、当前状态不足或真实卡点时窄读。

固定读取顺序是"父目录规则 -> PROJECT_CURRENT.md -> PROJECT_MEMORY.md"，缺失的项目文件先创建最小 UTF-8 模板。

## 选择性默认判定

仓库任务默认先做轻量判断。判断结果必须归入以下四类：

- 不适用: 当前问题不依赖历史知识、知识库内容、长期用户偏好或重复实体，本轮也没有值得未来复用的事实；记录判断即可，不读写知识库。
- 检索: 当前问题依赖历史决策、项目事实、用户偏好、重复实体、知识库内容，或出现"上次""之前""我们约定""当时怎么说"等信号；必须通过文件工具检索并读取匹配笔记后再引用。
- 沉淀: 会话总结、阶段收口或最终回复前，按 [capture-retrieve-distill.md](references/capture-retrieve-distill.md) 的「沉淀触发硬信号」清单对照判断，命中任一必须沉淀；判断依据要写进状态字段（如 `知识库:沉淀（命中信号2 推翻旧归因）`）。沉淀前先查同主题近似笔记，再决定创建、追加还是取代。不要求每轮都有沉淀，但要求写明依据。
- 阻断: 本应检索或沉淀，但知识库目录不存在、不可读，或写入后回读失败；必须说明阻断原因。

## 固定根目录

本 skill 只认一个固定的知识库根目录：

- 固定根目录：D:\谷歌云盘\知识库\

不要再通过环境变量、配置文件或候选路径重新推导。固定映射一旦已知，后续所有检索、捕获和沉淀都直接以此目录为准。

所有笔记读写都必须限制在上述目录下。禁止通过符号链接、相对路径 ..、盘符或 UNC 写出该范围。

## 工作流程

1. 先读取项目本地四件套
2. 再判断当前阶段和知识库状态
3. 直接使用固定映射，并按场景读取参考文件：
   - 决定目录落点时读 [knowledge-layout.md](references/knowledge-layout.md)。
   - 读写笔记前读 [file-operations.md](references/file-operations.md)，确认路径安全规则与写后回读流程。
   - 决定笔记字段、组件和双链规则时读 [note-schema.md](references/note-schema.md)。
   - 执行捕获、检索、沉淀流程时读 [capture-retrieve-distill.md](references/capture-retrieve-distill.md)。
   - 处理执行失败正反例、去重、状态事件和自动学习时读 [execution-case-notes.md](references/execution-case-notes.md)。
   - 处理冲突、过期笔记或敏感信息时读 [conflict-staleness.md](references/conflict-staleness.md)。
   - 做行为验证时读 [validation-checklist.md](references/validation-checklist.md)。
   - 处理 project-memory-rules / project-style-rules 跨项目候选沉淀时读 [project-memory-sync.md](references/project-memory-sync.md)。
   - 需要项目身份与跨宿主路径别名口径时读 [project-memory-layout.md](references/project-memory-layout.md)。
4. 写入前必须先通过文件工具检索，优先更新或链接现有笔记
5. 保护用户手写内容，只做窄范围编辑
6. 写入后补齐必要的 backlinks；索引由 query 自动重建，只有高价值笔记才补 INDEX.md 入口

知识库目录、路径或读写入口出现非预期失败时，先触发 `execution-failure-learning-rules` 的 `recover`；确认根因并在同输入下复验通过后，才把经验写入案例笔记的 `candidate`。

冲突候选用只读巡检入口 `python knowledge-flow/scripts/audit_vault_knowledge.py --json`；它默认覆盖全库，只输出候选、不做任何写入，处置仍走分级处置。归组要求同主题且共享标签达到下限，或标题相似度达阈值，并排除导航笔记（`type: moc`），避免候选清单被误报淹没。用 `--folder` 收窄范围时得到的是局部结论，不得当成全库结论引用。

巡检有强制触发时机，不是想起来才跑：知识库状态判为「沉淀」的轮次，写入并回读通过后必须跑一次；本轮新写或改写的笔记若出现在任一候选组，必须当轮完成三态判定并落状态。历史存量不要求当轮裁决。

笔记头部合规用 `python knowledge-flow/scripts/knowledge_index.py check`：校验活动区必填字段、状态枚举、接替关系双向性和双链有效性，退出码非零即不合规。`90-Archive/` 按只读归档豁免。

`check` 同样有强制触发时机，不是想起来才跑：任何笔记写入并回读通过后必须跑一次，退出码非零时必须当轮修到合规。不合规的写入不得登记引用台账的沉淀条目，也不得宣称沉淀成功——校验能报错但没绑到写入动作上，等于没人看。

## 捕获规则

- 稳定事实、决策、流程、定义、偏好和可复用模式沉淀到 20-Knowledge/
- project-memory-rules/project-style-rules 标记为跨项目候选的条目按规则选择性沉淀
- 只有多个相关笔记已经形成主题网络，或明显能提升检索效率时，才创建或更新 30-MOCs/；反复出现的项目、仓库、工具用项目地图承接，不单独建实体笔记
- 不确定材料标 `confidence: medium` 或 `low` 并留在所属主题，不要把未确认内容伪装成高置信长期知识
- 写入前必须按 [capture-retrieve-distill.md](references/capture-retrieve-distill.md) 的「三态判定硬信号」显式判定补充 / 矛盾未裁决 / 取代，并写出判定依据；查重命中同主题笔记时必须写明「为什么不是取代」
- 判为取代时必须在同一轮内按分级处置改旧笔记状态、归档或删除，并与新笔记双向写入接替关系；只写一侧会被 `knowledge_index.py check` 拦下
- 每次写入后立即登记引用台账的沉淀条目；没有 readback 证据的写入不登记
- 不捕获纯闲聊、临时过程话术、未确认猜测、一次性中间草稿或对未来没有检索价值的信息
- 非预期执行失败只有在根因已确认且同输入、同成功标准的 local 复验通过后才进入 learn

## 检索规则

- 第一跳固定用机器索引：`python knowledge-flow/scripts/knowledge_index.py query --keyword "<词>"`。它覆盖全库 100%，按标题、别名、标签、topics、主题、路径六类结构化字段加正文匹配，返回命中原因与相关性排序，索引过期会自动重建
- 用别名、标签、实体名、来源名，以及可能的中英文变体扩展检索词，多查几个同义词而不是只查一个
- 索引命中为空时才退到 `rg` 全文兜底；手写 INDEX.md 与 30-MOCs 只作辅助线索，不作为覆盖全库的依据
- 回答前通过文件工具读取最强匹配笔记；`query` 的命中只是候选，未读取不得引用
- 每次读取后立即登记引用台账条目；只有真实读取成功的笔记可入表，检索命中但未读取的笔记不得入表
- 笔记名一律取自读写笔记时所用的相对路径的文件名部分
- 回答依赖检索结果时，引用本地笔记路径作为证据
- 已取代与已归档状态的笔记不作为当前事实：顺着接替关系跳到接替笔记
- 台账字段、登记时机与入表门槛见 [capture-retrieve-distill.md](references/capture-retrieve-distill.md) 的「引用台账」

## 文件系统约定

- 使用标准 Windows 文件工具读写笔记
- 所有文件操作必须使用 UTF-8 编码，写入后回读验证一致性
- 路径安全规则：所有笔记路径必须是相对知识库根 `D:\谷歌云盘\知识库\` 的裸相对路径（如 `20-Knowledge/topic/note.md`），禁止 ..、盘符、UNC 或 Windows 非法字符
- 禁止在笔记路径上再加 `知识库/` 前缀：根目录本身已经是 `知识库`，前缀叠加会生成嵌套目录 `D:\谷歌云盘\知识库\知识库\`
- 执行案例目录（20-Knowledge/execution-failure-cases/）禁止移动和删除，仅允许追加
