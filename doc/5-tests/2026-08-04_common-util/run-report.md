# `common/util` 测试运行报告

| 证据 ID | 入口 | 结果 | 备注 |
|---|---|---|---|
| `EVD-T22-01-TEST` | `query --artifact common-util`、`render --project-kind backend` | PASS | Catalog 与目录树统一 |
| `EVD-T22-02-TEST` | `backend_common_util_layout_test.py` | PASS | `5/5`，含四语言与 adoption |
| `EVD-T22-03-DOC` | requirement/implementation_cycle/test/style_regression profile | PASS | 新增文档 `valid: true`；implementation_cycle 严格追踪通过，test/style_regression 通过 |

## 基线测试说明

全仓逐文件执行 16 个活动测试文件时，15 个文件通过；`artifact-delivery-gate-rules/validate_engineering_docs_test.py` 的一个 fixture 失败和一个错误引用均指向缺失的历史 `F:\luode-skills\doc\7-验收\...` 文件，与本轮改动文件无引用关系。本轮不修改范围外历史验收资产，故该失败保留为基线阻断事实。

## 环境边界

仅使用本地 Python、仓库文件和 `tempfile.TemporaryDirectory`；未连接数据库、缓存、消息队列、HTTP/RPC 上游或真实业务项目。
