# EVD-TASK-RT-C09-01-IMPL

## 实现

- 新增 `release_test_engine.cli.load_interface_contract_assets`，按项目根解析 manifest、inventory、reusable params，并输出三方 provenance、状态、失败类型和 `requires_refresh`。
- 新增 `release_test_engine.discovery.load_inventory`，严格区分缺失、非法 YAML、根类型错误、非对象记录和非 local 路径。
- `run_pipeline` 只把同步元数据传给 `write_report(sync_metadata=...)`，不替换 `InterfaceIR`、依赖图或参数解析输入；新增 `strict_contracts` 门禁开关和 CLI 参数。
- 所有文件使用 UTF-8；原始三方资产只读，未覆盖长期基线。

## 追踪

`SRC-USER-RT-001 -> DEC-RT-001/007 -> REQ-RT-001/002/008 -> AC-RT-001/008/009 -> TASK-RT-C09-01 -> cli.py/discovery.py/report.py -> test_contract_asset_sync.py -> EVD-TASK-RT-C09-01-*`
