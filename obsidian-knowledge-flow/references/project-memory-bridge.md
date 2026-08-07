# 项目记忆/风格桥接

## 目标

本文件定义一条**选择性、单条可复用事实**的桥梁：让 `project-memory-rules` 维护的 `PROJECT_MEMORY.md` 和 `project-style-rules` 维护的 `PROJECT_STYLE.md` 里，判断为**跨项目通用**的条目，能够被选择性沉淀成 Obsidian vault 里的一篇知识笔记。

这不是整份文件同步，也不是镜像备份。`project-memory-layout.md` 第5行的边界原则继续成立：项目本地记忆负责当前项目的启动上下文，Obsidian vault 负责跨项目、跨会话的选择性知识检索与沉淀，两条链路必须分开管理。本文件只是在这条边界上开一个窄口子——只搬运"这一条规则/写法本身"，不搬运"这份文件"。

## 初判标准（project-memory-rules / project-style-rules 侧）

写入 `PROJECT_MEMORY.md`/`PROJECT_STYLE.md` 条目的同一步骤里，用下面四条标准做初判；**必须同时满足**才可标记为桥接候选，任一条不满足则不标记。这一步只做本地文本判断，不调用 bridge，不产生任何 vault 副作用，可以每次增量更新都做。

1. **通用性删除测试**（核心标准）：把条目里的项目名、具体表名/字段名、具体服务名、具体域名/IP、具体接口路径、具体配置值从描述中删除后，条目是否仍然成立、仍然能指导其它项目做同样的实现或风格选择。
   - 成立示例："错误处理必须用 `errors.Wrap` 保留原始 error 链，禁止裸 `return err`"——删除项目名后仍成立，是可迁移的编码规范。
   - 不成立示例："`user_profile` 表的 `status=2` 表示已注销"——删除项目名后不成立，是项目专属数据字典事实，不得标记。
2. **类型白名单测试**：
   - `project-memory-rules` 侧：条目 `entities[].类型` 属于 `规则`、`流程节点`、`方法`（仅方法职责/调用规范层面，不含具体路径）三类之一时才可能通过；`字段`、`表`、`缓存键`、`常量`、`配置项`、`术语`（若该术语是本项目专属业务口径）默认排除，不得标记。
   - `project-style-rules` 侧：条目 `类型` 属于方法风格、注释风格、结构体风格、错误处理写法、日志写法、异步写法、命名风格、工具调用写法这类与语言/框架惯例相关的类型时才可能通过；如果 `示例` 字段里的代码片段本身耦合了本项目专属包路径、专属类型名且无法脱敏抽象为通用写法，则排除。
3. **适用范围显式标注测试**：条目的 `适用范围` 必须由写入方明确判断为"通用"/"团队规范"/"跨项目"，而不是"仅本项目"/"本项目业务特有"；无法判断时默认按"仅本项目"处理，不标记。
4. **稳定性门槛**：条目 `状态` 必须为 `启用`（对应机器索引区 `active`），且不是本轮刚形成、仍待用户确认的猜测；`conflicted`、`stale`、`deprecated`、`retired`（或人类阅读区对应的冲突/过期/废弃状态）一律不标记。

## 标记字段

四条全部满足时，在该条目本身追加一个**可选字段**，不改变既有必填字段结构：

- `project-memory-rules` 机器索引区：对应 `entities[]` 记录里追加 `bridge_candidate: true`（缺省即视为 `false`，不需要在其余条目上出现该字段）。
- `project-style-rules` 风格条目：条目字段列表里追加可选字段 `跨项目候选: 是`（缺省即视为"否"）。

标记本身不调用 bridge，写入方也不因为标记而改变本地写入流程或格式。

## 复核标准（obsidian-knowledge-flow 侧）

这是第二层复核，也是唯一真正调用 bridge 的地方。会话总结、阶段收口或最终回复前，按 [capture-retrieve-distill.md](capture-retrieve-distill.md) 的"总结阶段捕获流程"执行：

1. 把"本轮 `project-memory-rules`/`project-style-rules` 标记为 `bridge_candidate: true` / `跨项目候选: 是` 的条目"作为一类信息来源，与既有四类来源（稳定事实、用户偏好、决策流程、来源调试经验）并列扫描。
2. 对候选条目套用 `capture-retrieve-distill.md` 既有"排除不应捕获的信息"规则（纯闲聊、未确认猜测、secret 等）做兜底过滤。
3. 即使一层已标记候选，若二层判断内容仍隐含项目专属信息（例如删除测试有遗漏），可以直接不沉淀，或降级放入 `知识库/00-Inbox/`；一层标记不是"必须写"的强制通道，只是候选信号。

## 落点与目录

- 来自 `project-memory-rules` 的跨项目候选 → `知识库/20-Knowledge/project-rules/<slug>.md`
- 来自 `project-style-rules` 的跨项目候选 → `知识库/20-Knowledge/code-style/<slug>.md`

这两个子目录与 [vault-layout.md](vault-layout.md) 已有的"按 owner 分子目录"模式（类比 `execution-failure-cases/<owner>/`）保持一致，不新增顶层分类。

## 去重规则

- 沉淀前必须先按标题/别名/标签走 bridge `search`；命中已有笔记时执行 `append`（追加一条"本条规则已被以下项目采用：项目A（日期）、项目B（日期）"的来源记录），不得 `create` 重复笔记。
- 判定"是否命中同一条规则"沿用 [note-schema.md](note-schema.md) 已有排序启发式（标题/别名精确匹配 +5，标签命中 +3 等），达到高置信度才判定为同一笔记。
- 未命中才 `create` 新笔记。frontmatter 复用 [note-schema.md](note-schema.md) 通用字段，`source_refs` 记录来源项目的 `project_id`、来源文件（`PROJECT_MEMORY.md` 或 `PROJECT_STYLE.md`）和条目标题/别名，**不摘录整段项目原文**，正文只保留"通用性删除测试"后仍成立的那部分描述，即天然已经脱敏、去项目化的表达。
- 每次 `create` 或 `append` 仍按 `capture-retrieve-distill.md` 既有规则，返回 `verified=true` 后才登记引用台账。

## 边界（强调不做什么）

- 不同步整份 `PROJECT_MEMORY.md`/`PROJECT_STYLE.md`，不做镜像备份。
- 不反向让 vault 笔记覆盖或改写项目本地文件。
- 不改变项目本地四件套的本地读取顺序、工具选择（仍为标准文件工具）。
- `project-memory-rules`/`project-style-rules` 本身不直接调用 bridge；实际检索、去重、创建、追加统一交给 `obsidian-knowledge-flow` 在收口阶段处理。
- 不新增 Obsidian 四态（检索/沉淀/不适用/阻断）之外的第五种状态；本机制只是"沉淀"分支下的一类新信息来源。

## 验证映射

| 场景 | 证据 |
| --- | --- |
| 桥接候选标记字段、初判标准与复核流程一致性 | 纯文档一致性自查（术语、引用可达性、边界不回归），无独立 TEST-OBS 编号 |
