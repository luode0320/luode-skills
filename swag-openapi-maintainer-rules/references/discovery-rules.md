# 发现规则

本文件定义如何从当前代码发现全量 HTTP 接口契约。当前代码是唯一真相源；旧 Swagger、旧 Apifox、README 或历史记忆只能作为线索，不能覆盖真实代码。

## 路由扫描

必须从真实路由入口读取所有 HTTP method + path：

- router 文件、route group、middleware 装配、模块路由注册函数。
- 常见方法：`GET`、`POST`、`PUT`、`PATCH`、`DELETE`、`OPTIONS`、`HEAD`。
- 常见框架写法：`group.GET(...)`、`router.POST(...)`、`HandleFunc(...).Methods(...)`、注解式 route、OpenAPI 生成式 route。

扫描结果至少包含：

- method
- path
- router source file
- router source line
- route group / prefix
- middleware / auth hints
- controller symbol

## Controller 追踪

每个 route 必须追到 controller 方法或等价处理函数，读取：

- 请求绑定方式：path、query、header、cookie、body、form、multipart。
- 请求 DTO / struct / class / schema 来源。
- 请求字段中文注释、结构体中文注释和 header 语义说明来源。
- 成功响应结构。
- 错误响应结构。
- 统一响应包装。
- 响应字段中文注释、统一包装字段说明和错误提示说明来源。
- 鉴权、签名、租户、语言、trace header 等要求。

如果 route 无法追到 controller，允许生成待确认项，但不能凭猜测补字段。

## DTO / Model 追踪

字段必须来自真实代码：

- 请求 DTO、响应 DTO、model、entity、serializer、validator、binding tag、json tag、注释。
- 枚举、默认值、必填、nullable、数组、map、嵌套对象、分页结构。
- 中文说明优先从字段注释、结构体注释、wrapper 注释、鉴权注释和项目内文档提取。
- 统一响应包装与错误包装必须读取实际代码，不能按团队习惯猜。

## 接口索引

生成 YAML 前先构建内部接口索引。每条接口至少包含：

- `method`
- `path`
- `operationId`
- `tag`
- `summary`
- `summary_source`
- `source_router_file`
- `source_controller_file`
- `request_schema`
- `response_schema`
- `auth`
- `headers`
- `description_sources`
- `output_yaml_filename`

接口索引可作为内存对象，也可临时落盘；正式长期映射必须写入 `swag/.swag-manifest.yaml`。

## 冲突处理

- 同一路径同一 method 多次注册：必须列为冲突，暂停自动覆盖。
- 路由存在但 controller 缺失：生成待确认并阻断该接口通过验收。
- DTO 字段名与 JSON tag 冲突：以真实序列化字段为准，并记录来源。
- 中文说明缺失时，先补充来源证据；只有在字段名、DTO 名、route 上下文足够清晰时，才允许受控推导。
- 接口中文 `summary` 缺失时，允许按 route 动词、controller 名、DTO 名和现有中文注释推导短中文接口名；若仍无法稳定得到结果，标记 `summary_source: unresolved` 并回退纯路径文件名。
- 旧文档与当前代码冲突：以当前代码为准。
