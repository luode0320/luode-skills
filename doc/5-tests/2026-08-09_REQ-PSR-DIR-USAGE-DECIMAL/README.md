---
schema_version: 1
doc_id: "TEST-PSR-DIR-USAGE-DECIMAL-20260809"
doc_type: test
source_ids: ["REQ-PSR-DIR-USAGE-001", "CHG-PSR-DIR-USAGE-DECIMAL-001", "CYCLE-PSR-DIR-USAGE-04"]
status: accepted
version: "v1.0"
current_slice: "Decimal 目录收录真实测试"
updated_at: "2026-08-09"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# Decimal 目录收录真实测试

结论：本轮已验证 Decimal 目录收录可被 Catalog 查询，目录树、recipe 和索引与 Catalog 一致，专项测试全绿。影响：所有按本规则组织 Go 后端的项目可在编码前通过 guide 查询 Decimal 唯一落点与用法。范围：`package-structure-rules` 的 reference、Catalog、SKILL 示例与活动测试。非范围：真实业务 Decimal 行为、testnet/live 连接和非 local 环境。变化：新增 4 个 Decimal 专项测试，专项测试从 5 个增至 9 个。完成标准：9/9 专项测试通过，文档门禁 PASS，6-review 为 STYLE: PASS。术语说明：guide 是 CLI 用法查询子命令；recipe 是跨 skill 的代码用法示例。验证状态：已通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联任务 | `T04-01` 至 `T04-05` |
| 测试环境 | local 工作树、Windows Python、临时目录 |
| 可执行测试 | `test/package-structure-rules/backend_utils_usage_routing_test.py` |
| 证据边界 | 仅记录脱敏命令和结果，不记录任何秘密原值 |

## 测试矩阵

| TEST | 入口 | 断言 | 失败预期 |
|---|---|---|---|
| `TEST-PSR-DIR-USAGE-01` | guide --category decimal --language go | 返回 decimalUtil 别名与完整元数据 | 无结果或别名错误 |
| `TEST-PSR-DIR-USAGE-02` | project-layout-v2.md 检查 | 后端目录树包含 decimal 节点 | 目录树无 decimal |
| `TEST-PSR-DIR-USAGE-03` | usage-recipes-go.md 检查 | 包含 decimal 小节与 decimalUtil 引用 | 无小节或引用缺失 |
| `TEST-PSR-DIR-USAGE-04` | directory-usage-routing.md 检查 | 包含 utils/decimal 索引行 | 索引缺失 |
| `TEST-PSR-DIR-USAGE-05` | backend_utils_usage_routing_test.py | 9/9 通过 | 任一用例失败 |
| `TEST-PSR-DIR-USAGE-06` | py_compile 与 git diff --check | 退出码 0、无 whitespace 错误 | 任一命令失败 |
| `TEST-PSR-DIR-USAGE-07` | 文档门禁 | requirement/implementation_overview/implementation_cycle/style_regression 全 PASS | 任一 profile 失败 |

## 真实测试命令

```powershell
python -X utf8 package-structure-rules/scripts/placement_catalog.py guide --category decimal --language go
python -X utf8 -m unittest discover -s test/package-structure-rules -p backend_utils_usage_routing_test.py -v
python -X utf8 -m py_compile test/package-structure-rules/backend_utils_usage_routing_test.py
python -X utf8 -m py_compile package-structure-rules/scripts/placement_catalog.py
git diff --check
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile requirement --doc doc/2-需求/2026-08-08_REQ-PSR-DIR-USAGE-001_目录用法入口升级.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_overview --doc doc/3-实施/2026-08-08_REQ-PSR-DIR-USAGE-001_实施总览.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc doc/3-实施/2026-08-09_REQ-PSR-DIR-USAGE-001_实施周期04_Decimal目录用法收录.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile test --doc doc/5-tests/2026-08-09_REQ-PSR-DIR-USAGE-DECIMAL/README.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile style_regression --doc doc/6-review/2026-08-08_REQ-PSR-DIR-USAGE_6-review.md --root F:\luode-skills --strict
```

## 本轮实测结果

| TEST | 状态 | 证据 |
|---|---|---|
| `TEST-PSR-DIR-USAGE-01` | guide Decimal 查询通过 | `EVD-TASK-04-02-TEST-01` |
| `TEST-PSR-DIR-USAGE-02` | 目录树包含 decimal 节点 | `EVD-TASK-04-02-TEST-02` |
| `TEST-PSR-DIR-USAGE-03` | recipe 文档包含 decimal 小节 | `EVD-TASK-04-03-TEST-01` |
| `TEST-PSR-DIR-USAGE-04` | 索引文档包含 utils/decimal | `EVD-TASK-04-03-TEST-02` |
| `TEST-PSR-DIR-USAGE-05` | 专项测试 9/9 通过 | `EVD-TASK-04-03-TEST-03` |
| `TEST-PSR-DIR-USAGE-06` | py_compile 与 git diff --check 通过 | `EVD-TASK-04-04-TEST-01` |
| `TEST-PSR-DIR-USAGE-07` | 文档门禁全 PASS | `EVD-TASK-04-01-TEST-01` |

## 任务证据台账

| 任务 | IMPL | TEST | STYLE |
|---|---|---|---|
| `T04-01` | `EVD-TASK-04-01-IMPL-01` | `EVD-TASK-04-01-TEST-01` | `EVD-TASK-04-01-STYLE-01` |
| `T04-02` | `EVD-TASK-04-02-IMPL-01` | `EVD-TASK-04-02-TEST-01` | `EVD-TASK-04-02-STYLE-01` |
| `T04-03` | `EVD-TASK-04-03-IMPL-01` | `EVD-TASK-04-03-TEST-01` | `EVD-TASK-04-03-STYLE-01` |
| `T04-04` | `EVD-TASK-04-04-IMPL-01` | `EVD-TASK-04-04-TEST-01` | `EVD-TASK-04-04-STYLE-01` |
| `T04-05` | `EVD-TASK-04-05-IMPL-01` | `EVD-TASK-04-05-TEST-01` | `EVD-TASK-04-05-STYLE-01` |

## 验证结论

七项测试均达到完成标准；未发现 Decimal 目录收录破坏既有 guide、目录树、recipe 或索引行为。既有全量回归中 8 个配置 `source_policy` 字段未同步失败与本次改动无关。

## 测试边界

- 本轮只使用 local 工作树和临时目录，不连接数据库、缓存、消息队列、HTTP/RPC 上游或 test/prod 环境。
- 本轮不写入任何 API key、token、密码、私钥、连接串或其它秘密原值。
- 图片资产决策：N/A + 原因：本任务只验证文本规则、Catalog、目录树、recipe 和测试脚本，无界面或视觉产物 + 证据：上述测试矩阵。

## 追踪附录

| 规则变化 | TEST | 风格证据 |
|---|---|---|
| Decimal Catalog 条目与 guide 查询 | `TEST-PSR-DIR-USAGE-01` | `EVD-TASK-04-02-STYLE-01` |
| 目录树、recipe、索引与 Catalog 一致 | `TEST-PSR-DIR-USAGE-02/03/04` | `EVD-TASK-04-02/03-STYLE-01` |
| 专项测试与文档门禁 | `TEST-PSR-DIR-USAGE-05/06/07` | `EVD-TASK-04-04-STYLE-01` |
