# 命名与 Manifest 规则

本文件定义 `swag/` 输出结构、单接口文件命名、冲突处理、manifest 和过期清理规则。

## 输出结构

正式输出目录固定为项目根目录 `swag/`：

```text
swag/
  openapi.yaml
  api_buySell_sell_getHistory.yaml
  api_buySell_sell_hasUnreadHistory.yaml
  supported_onramps_all.yaml
  .swag-manifest.yaml
```

禁止在 `swag/` 外生成并行正式 OpenAPI / Swagger YAML。

## 单接口文件命名

基础规则：

1. 去掉 path 开头的 `/`。
2. `/` 替换为 `_`。
3. 保留原 path 大小写，避免 `buySell` 等业务路径变形后不易追踪。
4. 路径参数去掉包裹符号，保留参数名：`/users/{id}` -> `users_id.yaml`。
5. 空路径或根路径写为 `root.yaml`。

示例：

- `/supported/onramps/all` -> `supported_onramps_all.yaml`
- `/api/buySell/sell/getHistory` -> `api_buySell_sell_getHistory.yaml`

## Method 冲突处理

如果同一路径只有一个 method，文件名不追加 method。

如果同一路径存在多个 method，所有同路径文件都追加小写 method：

- `supported_onramps_all_get.yaml`
- `supported_onramps_all_post.yaml`

如果清理前已有不带 method 的旧文件，且 manifest 标记为本 skill 生成，则在本次刷新时改名并删除旧文件。

## Manifest 结构

`swag/.swag-manifest.yaml` 至少包含：

```yaml
generated_by: swag-openapi-maintainer-rules
updated_at: "2026-07-02 18:30:00"
openapi_file: openapi.yaml
interfaces:
  - method: GET
    path: /supported/onramps/all
    operationId: supported_onramps_all_get
    file: supported_onramps_all.yaml
    generated: true
    source_router_file: internal/router/supported.go
    source_controller_file: internal/controller/supported.go
    source_symbols:
      - SupportedController.All
```

## 过期清理

每次“更新 swag”必须对比当前扫描接口与 manifest：

1. 当前扫描不到、manifest 里存在、且 `generated: true` 的单接口 YAML，默认删除。
2. 当前扫描不到但 `generated` 不是 true 的文件，不删除，只在 manifest 中标记 `orphaned`。
3. 不删除 `openapi.yaml` 和 `.swag-manifest.yaml`。
4. 删除前必须确认目标路径仍在 `swag/` 目录内，禁止路径穿越。

## OperationId

`operationId` 默认由 path + method 生成：

- 去掉开头 `/`
- `/` 替换 `_`
- `{id}` / `:id` 转为 `id`
- 追加小写 method

示例：`GET /supported/onramps/all` -> `supported_onramps_all_get`。
