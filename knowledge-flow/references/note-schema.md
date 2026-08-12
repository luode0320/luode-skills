# 笔记结构与双链约定

## Frontmatter 字段

```yaml
---
id: 唯一标识（如 "knowledge-flow"）
type: 类型（knowledge / moc / source）
title: 人类可读标题
aliases: [别名列表]
tags: [标签列表]
status: 状态（active / superseded / archived / conflicted / stale / deprecated / retired）
created: 创建日期（ISO 8601）
updated: 最后更新日期
topics: [主题列表]
related: [相关笔记 wikilink]
entities: [关联实体名列表，纯文本]
supersedes: 此笔记取代的笔记 wikilink
superseded_by: 取代此笔记的笔记 wikilink
---
```

## 双链约定

- 使用 `[[笔记名]]` 格式链接其他笔记
- 文件名使用稳定、可读的名称
- 别名通过 frontmatter 的 aliases 字段管理
- **双链目标必须是库内真实存在的笔记**，由 `knowledge_index.py check` 校验，解析不到即不合规
- `entities` 只写纯文本实体名，不写 wikilink：它是检索维度而非跳转入口。实体导航走 `30-MOCs/` 的项目地图；早期要求 wikilink 时曾产生 8 处指向不存在实体笔记的死链
- 指向仓库文件、skill 名、项目记忆文件的引用用反引号写成普通代码文本，不用双链——它们不是知识库笔记

## 前置条件

- 所有笔记文件必须使用 UTF-8 编码
- 文件名不得包含 Windows 非法字符
- 新笔记必须包含完整的 frontmatter

## 状态互斥规则

- `superseded_by` 非空时 `status` 不得为 `active`
- 接替关系必须双向：新笔记写 `supersedes`，旧笔记写 `superseded_by`
