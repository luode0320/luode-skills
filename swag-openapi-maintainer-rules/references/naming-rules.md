# 命名与 Manifest 规则

本文件定义 `swag/` 输出结构、单接口文件命名、冲突处理、manifest 和过期清理规则。

## 输出结构

正式输出目录固定为项目根目录 `swag/`：

```text
swag/
  openapi.yaml
  api_buySell_sell_getHistory_卖出历史.yaml
  api_buySell_sell_hasUnreadHistory_未读历史标记.yaml
  supported_onramps_all_法币渠道列表.yaml
  .swag-manifest.yaml
```

禁止在 `swag/` 外生成并行正式 OpenAPI / Swagger YAML。

## 上游服务子目录结构与命名

本项目主动发起的外部第三方 API 和公司内部其他服务调用，统一称为上游接口，独立落在 `swag/<vendor-slug>/`。采用 B1 结构：每个上游服务子目录自成一套可独立导入的文档资产，不与自有接口或其他上游服务共用 manifest。

```text
swag/
  openapi.yaml
  .swag-manifest.yaml
  moonpay/
    openapi.yaml
    .swag-manifest.yaml
    v3_currencies_币种列表.yaml
```

约束如下：

- `<vendor-slug>` 必须是稳定的 ASCII 小写 slug，只允许 `[a-z0-9-]`，且不得为空；同一上游服务刷新时必须复用原 slug。
- 只允许一层上游服务子目录，即 `swag/<vendor-slug>/`；不在上游子目录下继续嵌套 vendor 目录。
- 上游子目录复用本文件的单接口路径名、method 冲突、中文后缀清洗和长度截断规则。
- 根 `swag/` 只维护自有接口；根 `openapi.yaml` 不聚合上游接口，根 manifest 也不得登记上游文件。

上游 manifest 至少包含以下字段：

```yaml
generated_by: swag-openapi-maintainer-rules
source_type: upstream
upstream: moonpay
base_url: https://api.moonpay.com
coverage: partial
updated_at: "2026-07-14 10:00:00"
openapi_file: openapi.yaml
interfaces:
  - method: GET
    path: /v3/currencies
    operationId: v3_currencies_get
    summary: 币种列表
    summary_source: explicit
    file: v3_currencies_币种列表.yaml
    generated: true
    source_client_file: internal/client/moonpay/currencies.go
    source_symbols:
      - MoonpayClient.ListCurrencies
    discovery_confidence: high
```

- `source_type` 是区分自有与上游的唯一开关；上游固定使用 `upstream`。
- `upstream` 必须等于当前子目录名；`base_url` 必须记录代码实际使用或配置解析后的上游根地址。
- `coverage: partial` 表示只记录本项目代码实际调用并成功确定契约的接口子集，不代表上游服务的完整 API 面。
- `source_client_file`、`source_symbols` 和 `discovery_confidence` 用于回溯出站调用来源；无法稳定确定 method、path、响应消费结构或来源文件时，必须标记待确认并阻断该接口通过。
- 每个接口的 `file` 必须是当前上游子目录内的裸文件名，不得包含 `/`、`\\` 或 `..`；`openapi_file` 也只能指向当前子目录内的保留文件。

## 单接口文件命名

基础规则：

1. 去掉 path 开头的 `/`。
2. `/` 替换为 `_`。
3. 保留原 path 大小写，避免 `buySell` 等业务路径变形后不易追踪。
4. 路径参数去掉包裹符号，保留参数名。
5. 若同一路径存在多个 method，基础路径名末尾追加小写 method。
6. 基础路径名后追加 `_中文简要说明`。
7. 空路径或根路径写为 `root`，再按是否有中文后缀决定最终文件名。

示例：

- `/supported/onramps/all` -> `supported_onramps_all_法币渠道列表.yaml`
- `/api/buySell/sell/getHistory` -> `api_buySell_sell_getHistory_卖出历史.yaml`
- `GET /users/{id}` -> `users_id_get_用户详情.yaml`
- `/api/buySell/sell/sellConfirmation` + `11. 卖出确认` -> `api_buySell_sell_sellConfirmation_卖出确认.yaml`

## 中文简要说明来源

单接口文件名中的中文简要说明优先级如下：

1. 接口已有明确中文 `summary`。
2. controller、route 注释或项目内现有接口文档中的中文接口名。
3. 按受控推导规则自动生成短中文说明。

`operationId` 继续保持 path + method 的稳定规则，不把中文说明混入 `operationId`。

## 中文后缀清洗

中文简要说明进入文件名之前，必须做稳定清洗：

1. 先去掉中文简介开头的数字前缀、序号包裹符号和无业务意义的特殊符号，例如 `1. `、`11.`、`1、`、`（1）`、`【1】`、`-`、`_`、`.`。
2. 空白折叠为单个 `_`。
3. Windows 非法文件名字符 `\\ / : * ? " < > |` 替换为 `_`。
4. 连续 `_` 折叠为一个。
5. 去掉首尾 `_`、空格、句点和残留装饰符号。
6. 清洗后后缀默认最多保留 24 个字符，避免文件名过长。

清洗后的中文后缀必须可复现；同一接口多次刷新应得到同一个后缀。
若显式 `summary` 本身带编号，只保留编号后的接口中文简介本体，不把编号写进文件名。

## 无法稳定得到中文说明时的回退

- 若接口没有显式中文 `summary`，允许按受控推导规则自动生成短中文说明。
- 若自动推导后仍无法得到稳定中文说明，可回退到纯路径文件名，例如 `supported_onramps_all.yaml`。
- 发生回退时，manifest 中必须记录：
  - `summary: ""`
  - `summary_source: unresolved`
- 禁止静默丢失状态；即使回退旧文件名，也必须让后续刷新能感知当前接口仍缺中文简要说明。

## Apifox 导入目录行为

- 单接口 YAML 的文件名只决定磁盘落点，不应用于在 Apifox 中制造额外父目录。
- 单接口 YAML 默认不通过 `tags` 进行目录分组；导入后接口应直接进入用户选中的目标目录。
- 总 YAML 可保留 `tags`，由 Apifox 按全量文档需要做模块分组。

## Method 冲突处理

如果同一路径只有一个 method，基础路径名不追加 method。

如果同一路径存在多个 method，所有同路径文件都追加小写 method，再拼中文后缀：

- `supported_onramps_all_get_法币渠道列表.yaml`
- `supported_onramps_all_post_新增法币渠道.yaml`

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
    summary: 法币渠道列表
    summary_source: explicit
    file: supported_onramps_all_法币渠道列表.yaml
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
4. 若中文简要说明变化导致文件名变化，且旧文件由本 skill 生成，则在 manifest 更新后删除旧文件。
5. 删除前必须确认目标路径仍在 `swag/` 目录内，禁止路径穿越。

上游清理必须额外满足目录隔离守卫：

1. 只有上游子目录内 `source_type: upstream` 且 `generated: true` 的文件可由该上游 manifest 清理。
2. 根 manifest 的清理只能作用于根 `swag/` 裸文件，不能解析或删除任何子目录文件。
3. 上游 manifest 只能清理自身 vendor slug 目录内的裸文件，禁止通过 `file` 字段跨目录、回到根目录或进入其他上游目录。

## OperationId

`operationId` 默认由 path + method 生成：

- 去掉开头 `/`
- `/` 替换 `_`
- `{id}` / `:id` 转为 `id`
- 追加小写 method

示例：`GET /supported/onramps/all` -> `supported_onramps_all_get`。
