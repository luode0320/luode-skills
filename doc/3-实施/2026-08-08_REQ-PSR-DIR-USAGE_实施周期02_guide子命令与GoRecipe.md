---
schema_version: 1
doc_id: "CYCLE-PSR-DIR-USAGE-02"
doc_type: implementation_cycle
source_ids: ["REQ-PSR-DIR-USAGE-001"]
status: accepted
current_slice: "CYCLE-02 guide 子命令与 Go Recipe"
updated_at: "2026-08-08"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 目录用法入口升级：CYCLE-02 guide 子命令与 Go Recipe

结论：完成 guide CLI 子命令和首批六类 Go recipe 文档。影响：可从 CLI 查询目录用法，从 recipe 文档获取代码示例。范围：新增 directory-usage-routing.md 索引文档、guide 子命令、usage-recipes-go.md 六类 recipe（convert/time/cache/redis/json/log/http）。非范围：不改动既有子命令行为。变化：guide 子命令支持 category 别名映射，六类 recipe 包含完整代码示例。完成标准：guide 子命令对六类 recipe 正确输出，recipe 文档格式通过。

## 完成的最小任务

- T02-01：directory-usage-routing.md 索引文档
- T02-02：guide CLI 子命令（含 category 别名映射）
- T02-03：usage-recipes-go.md 六类 Go recipe

## 交互示例

```bash
python placement_catalog.py guide --category time --language go
python placement_catalog.py guide --category conversion --language go
python placement_catalog.py guide --category cache --technology redis --language go
python placement_catalog.py guide --category json --language go
python placement_catalog.py guide --category log --language go
python placement_catalog.py guide --category http --language go
```
