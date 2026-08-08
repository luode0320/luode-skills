---
schema_version: 1
doc_id: "STYLE-PSR-DIR-USAGE-20260808"
doc_type: style_regression
source_ids: ["REQ-PSR-DIR-USAGE-001"]
status: accepted
current_slice: "CYCLE-01/02/03 目录用法入口升级"
updated_at: "2026-08-08"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：目录用法入口升级

结论：完成目录用法入口升级，Schema 扩展、Catalog 目录事实收敛、guide 子命令、Go recipe 文档、契约测试全部通过。影响：package-structure-rules 从"目录位置规则"升级为"目录驱动的用法入口"。范围：Catalog Schema、Catalog 数据、CLI 子命令、索引文档、recipe 文档、契约测试。非范围：不改动其他 skill 的 SKILL.md 正文，不改动既有子命令行为。变化：新增 2 个参考文档、1 个测试文件、4 个工程文档。完成标准：5 个契约测试通过，Schema 校验通过，guide 子命令正确输出。术语说明：guide 是 CLI 用法查询子命令；recipe 是代码用法示例。验证状态：5/5 测试通过。

## 检查范围

- package-structure-rules/references/placement-catalog.schema.json
- package-structure-rules/references/placement-catalog.yaml
- package-structure-rules/references/backend-util-layout.md
- package-structure-rules/scripts/placement_catalog.py
- package-structure-rules/references/directory-usage-routing.md
- package-structure-rules/references/usage-recipes-go.md
- test/package-structure-rules/backend_utils_usage_routing_test.py

## 真实测试前置证据

- 5 个契约测试全部通过
- Schema 语法校验通过
- guide 子命令对六类 recipe 正确输出

## 6-review 结论

- STYLE: PASS

## 检查清单

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| UTF-8、Markdown 结构 | PASS | git diff --check |
| 目录归位 | PASS | 所有文件在预期位置 |
| guide 子命令正确输出 | PASS | 5 个契约测试全部通过 |
| Schema 扩展 | PASS | python -c 校验通过 |
| 全部测试 | PASS | 5/5 |

## 执行附录

所有命令只读取本地工作树，未连接外部服务。

## 追踪附录

REQ-PSR-DIR-USAGE-001 -> CYCLE-01/CYCLE-02/CYCLE-03 -> T01-01..T03-04 -> TEST 5/5 -> STYLE: PASS
