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

## OperationId

`operationId` 默认由 path + method 生成：

- 去掉开头 `/`
- `/` 替换 `_`
- `{id}` / `:id` 转为 `id`
- 追加小写 method

示例：`GET /supported/onramps/all` -> `supported_onramps_all_get`。
