# 笔记结构

使用 YAML frontmatter 支撑机器检索，使用 Obsidian wikilink 支撑知识图谱导航。frontmatter 必须保持合法、紧凑。

## 通用 Frontmatter

```yaml
---
id: 20260706-142233-topic-slug
type: knowledge
title: "可读标题"
aliases: []
tags: []
status: active
created: 2026-07-06
updated: 2026-07-06
source_sessions: []
source_refs: []
related: []
entities: []
topics: []
confidence: medium
project_id: windows://d/path/to/project
project_name: project
project_root_native: D:\path\to\project
project_root_windows: D:\path\to\project
project_root_wsl: null
path_aliases: []
---
```

## 执行案例扩展字段

跨任务执行失败持续学习的笔记仍使用 `type: knowledge`，并增加 `knowledge_kind: execution_case`。其固定落点、正反例、去重和状态事件规则见 [execution-case-notes.md](execution-case-notes.md)。扩展字段如下：

- `knowledge_kind`: 固定为 `execution_case`。
- `case_key`: 由 owner、类别、工具主版本、稳定错误特征、脱敏输入摘要和 scope 组成的去重键。
- `owner_skill`: 唯一负责分类、恢复和解释案例的领域 skill。
- `category`、`environment`、`tool_or_model`、`tool_major`、`error_signature`、`input_fingerprint`、`scope`：用于精确检索和适用范围判断。

案例 frontmatter 的 `status` 是创建时缓存；追加式正文中的最后一条状态事件才是当前状态权威。不得依赖 frontmatter 覆盖历史事件，也不得通过重写 frontmatter 删除状态演进记录。

## 必填字段

- `id`: 稳定笔记 ID。除非 vault 已有约定，新笔记使用 `YYYYMMDD-HHmmss-slug`。
- `type`: 取值为 `inbox`、`session`、`knowledge`、`moc`、`entity`、`source`、`archive` 之一。
- `title`: 与笔记核心概念匹配的人类可读标题。
- `aliases`: 检索别名、缩写、中英文变体、仓库名或产品名。
- `tags`: 检索标签。少量稳定标签优于大量一次性标签。
- `status`: 普通笔记取值为 `active`、`stale`、`conflicted`、`deprecated`、`retired`、`archived` 之一；`knowledge_kind: execution_case` 额外允许 `candidate`、`superseded`、`rejected`，且当前状态以追加式状态事件为准。
- `created` 与 `updated`: 使用用户本地时区的 ISO 日期。
- `source_sessions`: 生成这篇笔记的会话笔记。
- `source_refs`: 外部来源笔记或 URL。
- `related`: 指向相关笔记的 wikilink。
- `entities`: 指向实体笔记的 wikilink。
- `topics`: 主题关键词或 MOC 链接。
- `confidence`: `low`、`medium` 或 `high`。
- `project_id`: 项目实体的 canonical ID；Windows 项目使用 `windows://<drive>/<normalized-path>`，WSL 项目使用 `wsl://<distro>/<absolute-linux-path>`。同一实体不得因为 Linux、UNC 或 Git Bash 路径别名重复创建。
- `project_name`: 人类可读项目名；`project_root_native`、`project_root_windows` 和 `project_root_wsl` 分别保留当前宿主、Windows 与 WSL 的规范路径，不适用字段使用 `null`。
- `path_aliases`: 记录已知等价路径别名，仅用于检索与追溯；不得替代 `project_id` 作为实体唯一键。

## 正文章节

使用能覆盖笔记用途的最小章节集合。

- 会话笔记：`## 摘要`、`## 关键事实`、`## 决策`、`## 待确认`、`## 可沉淀知识`。
- 知识笔记：`## 定义`、`## 适用范围`、`## 操作规则`、`## 证据`、`## 关联`。
- MOC：`## 入口`、`## 核心笔记`、`## 相关实体`、`## 待整理`。
- 实体笔记：`## 定义`、`## 别名`、`## 关联项目`、`## 重要记录`。
- 来源笔记：`## 来源`、`## 摘要`、`## 可复用信息`、`## 引用限制`。

## 可读组件

Markdown 笔记可以使用图形、列表和 Obsidian 组件提升阅读效率，但必须保持纯 Markdown 可读。

- 表格：适合对比决策、状态、字段、路径、命令和证据。
- 任务列表：适合保留待确认项、人工后续动作和复验清单。
- 普通列表：适合规则、流程、别名、约束和结论摘要。
- Obsidian callout：适合突出决策、风险、警告和证据，例如 `> [!NOTE]`、`> [!WARNING]`、`> [!TIP]`。
- Mermaid 图：适合流程图、依赖图和时序图；只在图形能明显降低理解成本时使用。
- wikilink/backlink：适合连接稳定实体、MOC、来源和长期知识。
- 代码围栏：只用于真实命令、配置、日志、JSON/YAML、Mermaid 或代码片段。

不要用 HTML 作为主要展示结构。不要为了视觉效果加入复杂排版、图片占位或非标准组件。

## 链接规则

- 用 wikilink 表达图谱边：`[[Note Title]]`；如果 vault 使用路径链接，则用 `[[path/to/Note|label]]`。
- 在正文中自然添加 backlink，不要机械堆砌所有可能关系。
- 优先链接稳定实体、MOC 和长期知识。会话之间互链是可选项。
- 如果被引用笔记不存在但应该存在，只有在能提升检索效率时，才创建简短实体笔记或 MOC。

## 更新规则

- 每次修改长期内容时更新 `updated`。
- 新证据添加到 `## 证据` 或最接近的等价章节中，不直接覆盖旧上下文。
- 保留用户手写段落，除非它已明确被更强证据取代。
- 更新已有笔记时优先追加带日期的小节、表格行或列表项，不批量重排全文。
- 执行案例不得覆盖原始反例、正例或状态事件；命中相同 `case_key` 时只通过 bridge `append` 追加新证据和状态事件。
