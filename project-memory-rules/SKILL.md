---
name: project-memory-rules
description: 从对话、代码与项目文档中抽取并维护项目本地四件套：`PROJECT_CURRENT.md` 保存可交接的当前状态并覆盖更新，`PROJECT_MEMORY.md` 保存稳定规则、关键决策和长期事实，`PROJECT_HISTORY.md` 只追加关键历史事件。`PROJECT_MEMORY.md` 继续保留兼容的“人类阅读区 + 底部机器索引区”结构，但不再作为当前状态或历史流水的唯一承载文件；不得新增 `PROJECT_MEMORY_INDEX.yaml` 等平行记忆根文件。
---

# 项目记忆规则

## 核心目标

维护项目根目录下的项目本地记忆四件套，其中 `PROJECT_MEMORY.md` 负责稳定长期事实并保留“双区协同”结构：

1. 人类阅读区：面向人工浏览、总结和快速回忆。
2. 机器索引区：位于文件底部的固定受管区，面向稳定检索、去重、冲突处理和后续 skill 复用。

当前状态和历史事件不进入上述双区：当前状态写入 `PROJECT_CURRENT.md`，历史事件追加到 `PROJECT_HISTORY.md`。

## 适用场景

- 记录项目中的指标、参数、表字段、缓存键、变量、公式、常量、状态、术语、脚本职责、方法映射或别名。
- 从代码中抽取长期稳定事实，并持续回写到 `PROJECT_MEMORY.md`。
- 对话中出现新的明确事实、旧事实被修订、废弃或冲突时，增量更新 `PROJECT_MEMORY.md`；当前任务进度覆盖写入 `PROJECT_CURRENT.md`，重要完成或阻断事件追加到 `PROJECT_HISTORY.md`。
- 用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 补充更新 md”等聚合指令时，作为四件套的记忆维护方参与统一编排。

## 双区模型

`PROJECT_MEMORY.md` 内部固定为两层，且只承载稳定规则、关键决策和长期事实：

1. 人类阅读区
- 中文可读、按主题组织。
- 用于总结核心事实、长期规则和重要映射关系。
- 是机器索引区的渲染视图，不是唯一事实源。

2. 机器索引区
- 固定标题：`## 机器索引区`
- 固定使用 `yaml` fenced block 承载结构化索引。
- 用于维护实体、关系、证据、上下文、生命周期和检索提示。
- 属于 `PROJECT_MEMORY.md` 的内嵌受管区，不是第二个主文件。

## 默认流程

1. 启动时先读取 `PROJECT_CURRENT.md`，再读取 `PROJECT_MEMORY.md`；缺失文件由 bootstrap 创建。读取当前状态时识别任务投影托管区，投影 schema、指纹、状态和 `update_plan` payload 统一交给 `task-plan-rehydration-rules`。
2. 读取当前的 `PROJECT_MEMORY.md` 全文，而不是只读某个词条。
3. 检查底部是否已有固定 `## 机器索引区`；若缺失，先补齐最小骨架。
4. 再读取当前对话、相关代码与已有项目文档，按来源优先级抽取明确事实。
5. 先在机器索引区中按 `entity_id + 类型 + 作用域 + 别名 + 来源` 定位现有实体。
6. 若命中原实体，则更新该实体、关系、证据、上下文与生命周期；若未命中，则新增结构化实体。
7. 机器索引区更新完成后，再将稳定结果同步到人类阅读区。
8. 当前状态覆盖写入 `PROJECT_CURRENT.md`，必须控制在 51,200 字节以内；超限先压缩并阻断。
9. 重要历史事件追加到 `PROJECT_HISTORY.md`，不得覆盖旧事件；普通启动不读取历史，只有历史追问、状态不足或真实卡点时窄读。
10. 若本次更新涉及口径切换、字段改名、状态迁移或冲突处理，再按需追加 `变更记录`。
11. 后续对话与其他 skill 按“父目录规则 -> `PROJECT_CURRENT.md` -> `PROJECT_MEMORY.md`”读取启动上下文；历史文件按需窄读。

## 写入规则

- 不创建 `PROJECT_MEMORY_INDEX.yaml`、`PROJECT_MEMORY.log.md` 或其他平行记忆根文件。
- `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md` 是项目本地记忆三文件；不得用其中一个替代另一个职责。
- `PROJECT_CURRENT.md` 采用覆盖式维护，UTF-8 字节数不得超过 51,200；超限必须阻断并压缩。覆盖普通当前状态时必须原样保留 `task-plan-rehydration-rules` 的唯一任务投影托管区，不得删除、复制、解析或改写其中字段。
- `PROJECT_HISTORY.md` 只追加关键事件；初始化或重复 bootstrap 不得覆盖已有历史。
- 不保留待确认区、草稿区或临时区。
- `PROJECT_MEMORY.md` 的标题、章节名、条目标题和字段名必须使用中文；英文只允许作为代码符号、文件名、原始字段名或别名保留。
- 机器索引区必须位于 `PROJECT_MEMORY.md` 底部，且标题固定为 `## 机器索引区`。
- 机器索引区缺失时必须自动补齐最小骨架；已存在时必须幂等更新，不得重复追加同名区块。
- 不写猜测内容；事实不明确、证据不足或身份无法确定时，不得直接写入“启用真相”。
- 同一指标、字段、规则或术语如果只是口径更新，必须回写原实体，不得额外新增同义冲突实体。
- 两条描述有重叠时，先尝试合并到同一主实体；确需并存时，必须通过 `适用范围`、`contexts` 或生命周期状态区分。
- 旧说法过时了，就直接替换为当前权威说法，并同步刷新 `更新时间`；若旧事实仍需保留，必须标记对应生命周期状态。
- 发生口径切换、字段改名、规则修订或冲突时，若会影响后续理解，必须在 `变更记录` 中追加简短原因说明。

## 来源优先级

- 来源排序、冲突裁决和 UTF-8 写入底线统一遵守 `references/project-knowledge-source-contract.md`。
- 本 Skill 只把契约应用于当前状态、稳定事实和历史事件；事实不明确时不得写入启用真相。

## 机器索引区结构

机器索引区默认至少包含以下结构：

- `version`
- `entities`
- `relations`
- `evidence`
- `contexts`
- `lifecycle`
- `retrieval_hints`
- `extensions`

字段定义与约束统一下沉到：

- [memory-index-schema.md](references/memory-index-schema.md)
- [memory-entity-types.md](references/memory-entity-types.md)
- [memory-relation-types.md](references/memory-relation-types.md)
- [memory-extraction-workflow.md](references/memory-extraction-workflow.md)
- [memory-retrieval-patterns.md](references/memory-retrieval-patterns.md)
- [memory-conflict-and-staleness.md](references/memory-conflict-and-staleness.md)

## 人类阅读区同步规则

- 人类阅读区保留中文主题结构，负责表达稳定事实，不直接承载全部机器字段。
- 机器索引区中的实体、关系、证据和状态是结构化事实底座；人类阅读区是经过归纳后的展示层。
- 同步时优先更新已有主题与原词条，不要随意改动无关章节。
- 若机器索引区存在 `conflicted`、`stale`、`deprecated` 或 `retired` 状态，人类阅读区必须同步其可见含义，不能继续展示成“当前启用事实”。

## 生命周期与冲突处理

- 默认状态以 `active` 为主，仅限证据明确且当前仍有效的事实。
- 旧口径失效但仍需保留历史上下文时，标记为 `deprecated` 或 `retired`。
- 证据过期、样本失真或后续验证失败时，标记为 `stale`。
- 高优先级来源与低优先级来源冲突、且无法立即裁决时，标记为 `conflicted`。
- 具体状态定义、迁移规则和处理建议参见 [memory-conflict-and-staleness.md](references/memory-conflict-and-staleness.md)。

## 记忆条目结构

人类阅读区的条目仍默认使用中文字段名：

- `别名`
- `类型`
- `定义`
- `来源`
- `适用范围`
- `更新时间`
- `状态`

可直接复用的主文档模板与双区同步说明，参见 [project-memory-template.md](references/project-memory-template.md)。
