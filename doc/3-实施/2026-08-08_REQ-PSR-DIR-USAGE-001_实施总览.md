---
schema_version: 1
doc_id: "IMP-OVERVIEW-DIR-USAGE-001"
doc_type: implementation_overview
source_ids: ["REQ-PSR-DIR-USAGE-001"]
status: accepted
version: "v1.0"
complexity: L2
current_slice: "目录用法入口升级"
baseline_commit: "N/A + 原因：本轮在已有工作树基础上继续推进 + 证据：git status --short"
template_version: "implementation-overview-v1"
updated_at: "2026-08-08"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
style_regression: required_after_tests
---

# 目录用法入口升级：实施总览

结论：package-structure-rules 从"目录位置规则"升级为"目录驱动的用法入口"，让 Catalog 每个目录节点都能关联代码风格、工具包写法、实用 recipe 和相关 skill。影响：编码时从目录查询直接获得用法指引，不再需要分别查多个 skill。范围：Catalog Schema 扩展元数据字段、guide CLI 子命令、directory-usage-routing.md 索引文档、usage-recipes-go.md 首批六类 Go recipe、契约测试和工程文档。非范围：不改动其他 skill 的 SKILL.md 正文，不改动既有 query/render/init/check/hash 子命令行为，不修改 project-layout-v2.md 目录树本身。变化：新增 guide 子命令、新增 4 个 Catalog 元数据字段、新增 2 个参考文档。完成标准：Schema 扩展校验通过，guide 子命令对六类 recipe 正确输出，5 个契约测试全绿，字典生成退出码 0。术语说明：guide 是 CLI 用法查询子命令；recipe 是跨 skill 的代码用法示例。验证状态：已执行完毕，5/5 测试通过，字典生成退出码 0。

## 当前计划最终方案简要说明

package-structure-rules 通过扩展 Catalog 元数据字段（related_skills、usage_recipes、package_alias、example_scope）、新增 guide CLI 子命令和 directory-usage-routing.md 索引文档，让 Catalog 能做"目录 -> 关联 skill -> recipe 示例"的多跳路由。具体编码写法仍由 time-util-rules、common-util-rules、code-generation-style-rules 等专业 skill 拥有，package-structure-rules 只做索引和转发。

## 实施周期总览

| 顺序 | 周期 ID | 期次定位 | 单一周期目标 | 进入条件 | 收口条件 | 文档 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CYCLE-01 | 第一期 | Schema 扩展 + 目录事实收敛 | 计划确认 | Schema 校验通过，Catalog 101 条 | 实施周期01 |
| 2 | CYCLE-02 | 第二期 | guide 子命令 + 六类 Go recipe | CYCLE-01 完成 | guide 六类 recipe 正确输出 | 实施周期02 |
| 3 | CYCLE-03 | 第三期 | 测试、工程文档与收口 | CYCLE-02 完成 | 5/5 测试通过，字典退出码 0 | 工程文档 |

## 最小任务清单与追踪矩阵

| 周期内顺序 | 任务 ID | 垂直切片目标 | 预计文件数 | 真实测试 | 完成条件 | 停止条件 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | T01-01 | Schema 扩展 4 个 optional 字段 | 1 | 无 | Schema 语法校验通过 | 破坏既有测试 |
| 2 | T01-02 | Catalog 新增 31 个工具包条目 | 1 | 无 | 无遗漏 | 无法正确定义 |
| 3 | T01-03 | backend-util-layout.md 标注 Catalog ID | 1 | 无 | 每行标注 | 发现不一致 |
| 4 | T02-01 | directory-usage-routing.md 索引文档 | 1 | 无 | 格式检查通过 | 格式检查失败 |
| 5 | T02-02 | guide CLI 子命令 | 1 | 有 | 5 个测试通过 | 破坏既有子命令 |
| 6 | T02-03 | usage-recipes-go.md 六类 Go recipe | 1 | 无 | 格式检查通过 | 格式检查失败 |
| 7 | T03-01 | 契约测试 5 个 | 1 | 有 | 5/5 通过 | 测试失败 |
| 8 | T03-02 | 工程文档 4 个 | 4 | 无 | 格式检查通过 | 格式检查失败 |
| 9 | T03-03 | 全量回归与字典生成 | 0 | 有 | 三项验证通过 | 任一验证失败 |
| 10 | T03-04 | 项目记忆同步 | 3 | 无 | 文件更新完成 | 无 |

## 真实测试安排

| 测试 ID | 任务 | 命令/入口 | 断言 | 失败预期 |
| --- | --- | --- | --- | --- |
| TC-1 | T02-02 | guide --category time --language go | 返回 timeUtil 别名 | 无结果或别名错误 |
| TC-2 | T02-02 | guide --category conversion --language go | 返回 utils/convert | 无结果或路径错误 |
| TC-3 | T02-02 | guide --category cache --technology redis --language go | 返回 utils/cache/redis | 无结果 |
| TC-4 | T01-02 | 检查所有 utils 条目标注 related_skills | 无缺失 | 有缺失 |
| TC-5 | T01-02/T01-03 | backend-util-layout 与 Catalog 一致性 | 无遗漏 | 有遗漏 |
| TC-6 | T03-03 | run_python_tests.py | 全绿 | 2 个既有失败不阻断 |
| TC-7 | T03-03 | generate_dictionary.py | 退出码 0 | 非零退出码 |
