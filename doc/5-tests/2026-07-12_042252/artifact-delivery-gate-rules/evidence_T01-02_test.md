# EVD-T01-02-TEST-01 测试证据

## 入口

`python -X utf8 doc/5-tests/2026-07-12_042252/artifact-delivery-gate-rules/test_handoff_contract.py`

## 结果

2026-07-12 04:29:05 +08:00，退出码 `0`。五类 profile 正例通过；缺章节、占位词、`N/A` 无证据三个负例按预期阻断；`N/A` 有原因与证据正例通过。

## 覆盖

| ID | 覆盖内容 | 结果 |
| --- | --- | --- |
| `EVD-T01-02-TEST-01` | 契约关键条款与 profile 字段矩阵 | PASS |
| `EVD-T01-02-TEST-02` | requirement/acceptance/implementation_master/overview/cycle 正例 | PASS |
| `EVD-T01-02-TEST-03` | 缺章节、占位词、N/A 无证据负例 | BLOCKED（符合预期） |
| `EVD-T01-02-TEST-04` | N/A 有原因与证据 | PASS |
| `EVD-T01-02-TEST-05` | 校验器七项 unittest | PASS |

## 环境边界

仅使用本地 Python 和仓库文件，未连接 test/prod 数据库、缓存、消息队列或外部服务。
