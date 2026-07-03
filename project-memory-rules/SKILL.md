---
name: project-memory-rules
description: 从对话、代码与项目文档中抽取并维护长期项目记忆，统一写入根目录 `PROJECT_MEMORY.md`。该文件继续作为唯一长期记忆主文件，但内部升级为“人类阅读区 + 底部机器索引区”的单文件双区结构；默认先更新机器索引区，再同步人类阅读区，不得新增 `PROJECT_MEMORY_INDEX.yaml` 等平行记忆根文件。
---

# 项目记忆规则

## 核心目标

维护项目根目录下唯一的长期记忆主文件 `PROJECT_MEMORY.md`，并将其升级为“双区协同”的单文件知识库：

1. 人类阅读区：面向人工浏览、总结和快速回忆。
2. 机器索引区：位于文件底部的固定受管区，面向稳定检索、去重、冲突处理和后续 skill 复用。

## 适用场景

- 记录项目中的指标、参数、表字段、缓存键、变量、公式、常量、状态、术语、脚本职责、方法映射或别名。
- 从代码中抽取长期稳定事实，并持续回写到主记忆文档。
- 对话中出现新的明确事实、旧事实被修订、废弃或冲突时，增量更新同一份主文档。
- 用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md / 补充更新 md”等聚合指令时，作为 `PROJECT_MEMORY.md` 的维护方参与统一编排。

## 双区模型

`PROJECT_MEMORY.md` 继续是唯一长期记忆主文件，但内部固定为两层：

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

1. 先读取当前的 `PROJECT_MEMORY.md` 全文，而不是只读某个词条。
2. 检查底部是否已有固定 `## 机器索引区`；若缺失，先补齐最小骨架。
3. 再读取当前对话、相关代码与已有项目文档，按来源优先级抽取明确事实。
4. 先在机器索引区中按 `entity_id + 类型 + 作用域 + 别名 + 来源` 定位现有实体。
5. 若命中原实体，则更新该实体、关系、证据、上下文与生命周期；若未命中，则新增结构化实体。
6. 机器索引区更新完成后，再将稳定结果同步到人类阅读区。
7. 若本次更新涉及口径切换、字段改名、状态迁移或冲突处理，再按需追加 `变更记录`。
8. 后续对话与其他 skill 优先读取更新后的 `PROJECT_MEMORY.md`。

## 写入规则

- 只保留一个长期记忆主文件：`PROJECT_MEMORY.md`。
- 不创建 `PROJECT_MEMORY_INDEX.yaml`、`PROJECT_MEMORY.log.md` 或其他平行记忆根文件。
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

1. 当前项目代码
2. 最近一次明确的对话确认
3. 已有项目文档
4. 旧记忆内容

来源冲突时，以高优先级来源为准；低优先级内容不能覆盖高优先级证据。

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
