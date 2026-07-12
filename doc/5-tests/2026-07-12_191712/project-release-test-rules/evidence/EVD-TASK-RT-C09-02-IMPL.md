# EVD-TASK-RT-C09-02-IMPL

## 实现

- 在 `release_test_engine.graph.reconcile_contract_assets` 中冻结三方身份为规范化 `HTTP_METHOD /path`。
- 使用 JSON canonical sort + SHA-256 比较 request/response schema，输出缺失、重复 interface_id、schema_changed 和稳定 drift 证据。
- 对 schema 漂移涉及的 reusable 参数生成内存 projection：`candidate/reusable -> stale`，`failure_type=schema_changed`；不写回原始 reusable 文件。
- 新增 `release_test_engine.cli.sync_interface_contract_assets`，兼容 `generate_release_test_plan.py sync-interface-contract-assets`，报告只写指定 output。

## 追踪

`SRC-BASELINE-RT-001 -> DEC-RT-002/003 -> RULE-RT-002/003/005 -> AC-RT-002/003/009 -> TASK-RT-C09-02 -> graph.py/cli.py/generate_release_test_plan.py -> test_contract_reconcile.py -> EVD-TASK-RT-C09-02-*`
