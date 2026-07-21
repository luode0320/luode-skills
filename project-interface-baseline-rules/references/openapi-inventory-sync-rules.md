# Swagger/OpenAPI 双索引同步规则

本文件定义 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 的同步关系。两者都来自当前代码接口事实，不允许各自独立漂移。

## 核心原则

- 当前代码是唯一真相源；历史基线、旧 swag、旧测试报告只能作为参考证据。
- `swag/.swag-manifest.yaml` 是接口文档索引，负责记录 OpenAPI 文件、operationId、来源文件和生成状态。
- `doc/5-tests/基线/interface-inventory.yaml` 是上线测试索引，负责记录接口测试契约、风险等级、参数来源、判定规则和历史测试结论。
- 正常项目中两个索引都应存在；任一缺失都视为接口契约资产不完整，必须先从当前代码刷新两边。

## 三方对账对象

每次上线测试前必须对比三组接口集合，接口身份统一使用 `HTTP method + path`：

1. 当前代码扫描结果：来自路由、controller / handler、OpenAPI 注释、现有测试和接口文档。
2. `swag/.swag-manifest.yaml`：来自 `swag-openapi-maintainer-rules` 刷新的接口文档索引。
3. `doc/5-tests/基线/interface-inventory.yaml`：来自上线测试长期接口基线。

三方集合一致后，才允许进入测试范围筛选、参数构造和测试执行。

## 漂移分类

### 缺失索引

- manifest 缺失、inventory 存在：不能只补 manifest；必须先刷新 `swag/`，再用刷新后的 manifest 同步 inventory。
- inventory 缺失、manifest 存在：不能只从旧 manifest 补 inventory；必须先确认 manifest 来自当前代码，再生成 inventory。
- 两者都缺失：先刷新 `swag/`，再冷启动 `doc/5-tests/基线/`。

### 当前代码新增接口

- 当前代码存在，manifest 和 inventory 都缺失：刷新 `swag/`，并把接口补入 inventory，完整度可为 `待确认`。
- 当前代码存在，manifest 存在但 inventory 缺失：补入 inventory，`schema_sync_status` 写 `missing_in_inventory`。
- 当前代码存在，inventory 存在但 manifest 缺失：刷新 `swag/`，`schema_sync_status` 暂写 `missing_in_swag`，不得直接进入测试执行。

### 当前代码删除接口

- 当前代码不存在，manifest 和 inventory 都存在：`swag-openapi-maintainer-rules` 清理 manifest 标记为生成的单接口 YAML，inventory 标记 `deprecated` 或增加 `废弃标记` 待确认项。
- 当前代码不存在但只有一侧仍存在：保留证据，写入 `missing_in_code`，需要人工确认是否为扫描漏报或接口废弃。

### schema 漂移

- 请求 schema hash 或响应 schema hash 变化时，inventory 写入新的 `request_schema_hash` / `response_schema_hash`。
- `schema_sync_status` 写 `schema_changed`，`最近测试结论` 写 `待重测`。
- 该接口 `可复用参数影响字段` 对应的 `reusable-params.yaml` 样本必须标记为 `stale`，本轮复用前必须复验。

## inventory OpenAPI 同步字段

`interface-inventory.yaml` 中每个接口应维护以下字段：

```yaml
openapi_operation_id: supported_onramps_all_get
openapi_file: supported_onramps_all.yaml
openapi_manifest_updated_at: "2026-07-02 18:30:00"
request_schema_hash: "<sha256 或空字符串>"
response_schema_hash: "<sha256 或空字符串>"
schema_sync_status: synced
```

`schema_sync_status` 允许值：

- `synced`：当前代码、manifest、inventory 三方一致。
- `missing_in_swag`：当前代码或 inventory 存在，但 manifest 缺失。
- `missing_in_inventory`：当前代码或 manifest 存在，但 inventory 缺失。
- `schema_changed`：OpenAPI 请求或响应 schema hash 变化。
- `deprecated`：当前代码已找不到该接口。
- `blocked`：缺少关键同步证据，不能自动判断。

## 同步报告

每次对账必须输出 `interface-sync-report.yaml`，至少包含：

```yaml
summary:
  scanned_interface_count: 0
  manifest_interface_count: 0
  inventory_interface_count: 0
  updated_inventory_count: 0
  missing_manifest: false
  missing_inventory: false
  requires_dual_refresh: false
  schema_changed_count: 0
  affected_reusable_param_count: 0
  synced_count: 0
  updated_at: "2026-07-02 18:30:00"
missing_in_swag: []
missing_in_inventory: []
missing_in_code: []
schema_changed: []
affected_reusable_params: []
synced: []
```

## 阻断条件

- `swag/.swag-manifest.yaml` 缺失且未重新刷新 `swag/`。
- `interface-inventory.yaml` 缺失且未重新刷新测试基线。
- 当前代码、manifest、inventory 三方接口集合不一致且未生成同步报告。
- P0 / P1 接口存在 `missing_in_swag`、`missing_in_inventory`、`schema_changed` 或 `blocked`，但仍准备自动放行。
- schema 漂移影响可复用参数，但未把相关样本标记为 `stale`。
- 报告只口头说明同步结果，未落盘到当轮测试资产目录。

## 推荐脚本入口

优先复用通用脚本：

```bash
python project-interface-release-execution-rules/scripts/generate_release_test_plan.py sync-interface-contract-assets \
  --project-root . \
  --manifest swag/.swag-manifest.yaml \
  --inventory doc/5-tests/基线/interface-inventory.yaml \
  --reusable-params doc/5-tests/基线/reusable-params.yaml \
  --output doc/5-tests/<时间戳>_上线前项目接口测试/ascii-artifacts/interface-sync-report.yaml
```

如果脚本报告 `requires_dual_refresh: true`，必须先执行 `swag-openapi-maintainer-rules` 刷新 `swag/`，再重新运行本同步命令。
