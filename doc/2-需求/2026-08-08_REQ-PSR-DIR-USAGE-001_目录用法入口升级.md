---
schema_version: 1
doc_id: "REQ-PSR-DIR-USAGE-001"
doc_type: requirement
source_ids: ["SRC-PSR-DIR-USAGE-001"]
status: accepted
version: "v1.0"
current_slice: "目录用法入口升级"
updated_at: "2026-08-08"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 目录用法入口升级

结论：package-structure-rules 从"目录位置规则"升级为"目录驱动的用法入口"，让 Catalog 每个目录节点都能关联代码风格、工具包写法、实用 recipe 和相关 skill。影响：编码时从目录查询直接获得用法指引，不再需要分别查多个 skill。范围：Catalog Schema 扩展元数据字段、guide CLI 子命令、directory-usage-routing.md 索引文档、usage-recipes-go.md 首批六类 Go recipe。非范围：不改动其他 skill 的 SKILL.md 正文，不改动既有 query/render/init/check/hash 子命令行为，不修改 project-layout-v2.md 目录树本身。变化：新增 guide 子命令、新增 4 个 Catalog 元数据字段、新增 2 个参考文档。完成标准：Schema 扩展校验通过，guide 子命令对六类 recipe 正确输出，5 个契约测试全绿，字典生成退出码 0。术语说明：guide 是 CLI 用法查询子命令；recipe 是跨 skill 的代码用法示例。验证状态：计划已执行完毕，5/5 测试通过。

## 需求来源与决策

| 来源 | 内容 |
| --- | --- |
| SRC-PSR-DIR-USAGE-001 | 用户要求 package-structure-rules 从目录树入口关联代码风格、工具包写法和相邻 skill |

## 功能需求

| 需求 ID | 描述 |
| --- | --- |
| REQ-GUIDE-001 | Schema 新增 related_skills、usage_recipes、package_alias、example_scope 四个 optional 字段 |
| REQ-GUIDE-002 | Catalog 中所有 utils 条目都标注元数据字段 |
| REQ-GUIDE-003 | guide CLI 子命令支持按 category/technology/language 查询目录用法 |
| REQ-GUIDE-004 | 首批 Go recipe 覆盖 convert/time/cache/redis/json/log/http 六类 |
| REQ-GUIDE-005 | 目录用法索引文档 directory-usage-routing.md 作为文档索引入口 |

## 验收标准

| AC ID | 条件 |
| --- | --- |
| AC-GUIDE-001 | guide --category time --language go 返回 timeUtil 别名 |
| AC-GUIDE-002 | guide --category conversion --language go 返回 utils/convert |
| AC-GUIDE-003 | guide --category cache --technology redis --language go 返回 utils/cache/redis |
| AC-GUIDE-004 | 所有 utils 条目标注 related_skills |
| AC-GUIDE-005 | backend-util-layout.md 中每个目录在 Catalog 中有对应条目 |
