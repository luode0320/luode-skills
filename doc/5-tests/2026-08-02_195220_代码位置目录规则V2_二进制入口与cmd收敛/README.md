---
schema_version: 1
doc_id: "TEST-PSR-BINARY-ENTRY-001"
doc_type: test
source_ids: ["REQ-PSR-BINARY-ENTRY-001", "CYCLE-PSR-15-001"]
status: accepted
version: "v1.0"
current_slice: "TASK-15-01..03"
updated_at: "2026-08-02 19:52:20"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 二进制入口与 cmd 收敛真实测试

结论：独立后端的主入口只能是根 `main.<ext>`，额外入口只能是 `cmd/<binary>/main.<ext>`；同仓后端对应放在 `backend/` 下。影响：非法入口会被严格策略拒绝，历史策略保持只读边界；范围：Catalog、CLI、根测试和研发文档；非范围：真实业务项目、外部服务和 Git 历史；变化：新增动态入口 pattern 的查询、检查和初始化拒绝验证；完成标准：全部本地测试均通过；术语说明：动态 pattern 是人工实现入口的规则，不是初始化目录；验证状态：已通过。

## 图片资产决策

图片资产决策：N/A + 原因：本测试只验证规则、命令和临时目录，不产生界面或视觉资产 + 证据：所有实测入口均为本地 Python 命令。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联周期 | `CYCLE-PSR-15-001` |
| 可执行测试代码 | `test/package-structure-rules/entrypoint_layout_test.py` |
| 环境 | local 工作树、Windows Python、临时目录 |
| 证据根 | 当前目录；未使用外部服务或非 local 配置 |

## 测试矩阵

| TEST | 命令/样本 | 通过标准 | 实测结果 |
| --- | --- | --- | --- |
| `TEST-PSR-BINARY-001` | query、render、Schema | 四个 pattern 唯一可查、可渲染且 Schema 要求 pattern 字段 | 通过 |
| `TEST-PSR-BINARY-002` | backend/fullstack 四条合法 Go 入口 | strict 返回 `0` | 通过 |
| `TEST-PSR-BINARY-003` | 六类非法入口、legacy、adoption | strict 返回 `2`；legacy 告警；adoption 保留登记快照；fixture 哈希不变 | 通过 |
| `TEST-PSR-BINARY-004` | `init --enable` primary/additional | 返回 `2`，不创建 `main.<ext>`、`cmd/`、`<binary>` 占位路径 | 通过 |
| `TEST-PSR-BINARY-005` | 项目目录契约与根测试入口 | 目录契约测试、全量 Python 入口、语法编译和差异检查均通过 | 通过 |

## 完成标准

- 所有测试只操作 local 工作树或自动删除的临时目录。
- `check`、legacy、adoption 与 init 的负向样本不会写入 fixture。
- N/A + 原因 + 证据：不连接数据库、缓存、消息队列、HTTP/RPC 或外部服务；证据为全部测试命令只调用本地 Python 和临时目录。

## 本轮实测结果

- `EVD-TASK-15-01-TEST-01`：`python -X utf8 -B test/package-structure-rules/entrypoint_layout_test.py` 返回 `5/5 OK`。
- `EVD-TASK-15-02-TEST-01`：`python -X utf8 -B test/package-structure-rules/project_layout_contract_test.py` 返回 `2/2 OK`。
- `EVD-TASK-15-03-TEST-01`：`python -X utf8 -B -m py_compile package-structure-rules/scripts/placement_catalog.py`、两类 binary-entrypoint query、全量 Python 入口、工程文档 profile、quick validation 与 `git diff --check` 均通过。

## 执行附录

可执行测试资产只保留在根 `test/package-structure-rules/`；本目录仅保存说明和测试证据，不新增可执行脚本。测试不创建外部状态；临时 fixture 由测试上下文自动清理。

## 追踪附录

`AC-PSR-BINARY-001..005` -> `TASK-15-01..03` -> `TEST-PSR-BINARY-001..005` -> `EVD-TASK-15-01-TEST-01..EVD-TASK-15-03-TEST-01` -> `STYLE-PSR-BINARY-ENTRY-001`。
