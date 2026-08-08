---
schema_version: 1
doc_id: "CYCLE-PSR-DIR-USAGE-01"
doc_type: implementation_cycle
source_ids: ["REQ-PSR-DIR-USAGE-001"]
status: accepted
current_slice: "CYCLE-01 Schema 扩展与目录收敛"
updated_at: "2026-08-08"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 目录用法入口升级：CYCLE-01 Schema 扩展与目录收敛

结论：完成 Catalog Schema 扩展和目录事实收敛。影响：Catalog 条目新增 31 个工具包目录，已有 7 个条目追加元数据字段，4 个新字段（related_skills、usage_recipes、package_alias、example_scope）可被后续 guide 子命令消费。范围：Schema 扩展、Catalog 工具包目录补齐、backend-util-layout.md 双向索引标注。非范围：不改动既有 CLI 子命令和目录树。变化：Schema 新增 4 个 optional 字段，Catalog 从 70 条扩展到 101 条，backend-util-layout.md 表格新增 Catalog ID 列。完成标准：Schema 语法校验通过，Catalog 覆盖 backend-util-layout.md 所有工具目录，无遗漏。术语说明：related_skills 是关联 skill 列表；usage_recipes 是 recipe 索引列表；package_alias 是 Go 包别名；example_scope 是示例范围。验证状态：Schema 校验通过，Catalog 101 条，所有 utils 条目标注 related_skills。

## 完成的最小任务

- T01-01：Schema 扩展 4 个 optional 字段
- T01-02：Catalog 新增 31 个工具包条目，7 个已有条目追加元数据
- T01-03：backend-util-layout.md 表格新增 Catalog ID 列
