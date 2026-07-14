# OpenAPI / Swagger Schema 规则

本文件定义生成单接口 YAML 和总 YAML 时的 schema 规则。

## 版本

默认优先使用 OpenAPI 3.0.x 或 3.1.x。项目已有统一 Swagger 2.0 方案时可沿用 `swagger: "2.0"`，但同一项目只能保留一个主版本。

合法版本：

- `openapi: 3.0.x`
- `openapi: 3.1.x`
- `swagger: "2.0"`

## 单接口 YAML

每个单接口 YAML 必须是完整文档，不是 paths 片段：

- `openapi` 或 `swagger`
- `info`
- `paths`
- 必要的 `components` / `definitions`
- 必要的 `securitySchemes` / `securityDefinitions`

单接口 YAML 只包含一个接口 operation；如果同一 path 下同一单文件确实承载多个 method，必须能独立导入 Apifox。

为避免 Apifox 导入时自动新增父目录，单接口 YAML 的 operation 默认不写 `tags`。总 YAML 可保留 `tags` 供全量文档分组使用。

## 总 YAML

`swag/openapi.yaml` 必须包含当前扫描到的所有接口：

- `paths` 中 path 数 / operation 数与扫描结果一致。
- `components.schemas` 对重复 DTO 去重。
- `components.securitySchemes` 对鉴权方案去重。
- operation 的 request / response schema 优先使用 `$ref` 指向 components。

## 上游接口 schema 差异

`swag/<vendor-slug>/` 是上游服务独立成套的 OpenAPI 文档，不把上游接口合并进根 `swag/openapi.yaml`。上游文档必须额外遵守：

- `servers` 必须指向 manifest 的 `base_url`，且只能来自代码实际使用或 local 配置解析结果。
- 上游自身的 Bearer、API Key、签名、Cookie 等鉴权方案按上游调用代码表达，`securitySchemes` / `securityDefinitions` 的说明必须是中文；不得套用本项目自有接口的统一鉴权或统一响应包装。
- 上游响应只建模本项目实际请求并消费到的字段，`coverage: partial` 不代表上游服务完整 API；未消费字段不得为了补全模型而猜测加入。
- 上游错误响应、分页、状态码和包装结构以真实 client 解码与调用方分支为准；不能因为上游看起来像本项目接口就套用自有统一错误结构。
- 每个上游子目录仍须包含独立的 `openapi.yaml`、`.swag-manifest.yaml` 和单接口完整 YAML，复用本文件的版本、`servers`、`$ref`、中文说明和单接口无 `tags` 规则。

## 字段来源

字段必须来自真实代码：

- JSON 字段名来自 `json` tag、序列化注解或框架约定。
- 必填来自 binding / validate / required tag、构造逻辑或 DTO 定义。
- 类型来自语言类型、字段 tag、注释和 serializer。
- 枚举来自常量、枚举类型、validator、代码分支。
- 头部、请求参数、响应字段都必须有中文 `description`。
- description 优先来自字段注释；源码注释不足时允许按 `description-rules.md` 做受控推导，但不得编造业务含义、默认值、校验规则或失败语义。

## 请求与响应

- GET / DELETE 等无 body 的接口，按真实代码决定 query / path / header 参数。
- POST / PUT / PATCH body 必须按真实 request DTO 构造。
- 统一响应包装必须按真实 response wrapper 展开或引用。
- 错误响应至少覆盖项目统一错误结构；不能只写 200。
- body 根对象、响应根对象和统一包装字段也必须有中文说明。

## 鉴权与 Header

鉴权要求来自 middleware、route group、controller 注解或统一鉴权配置：

- Bearer Token
- Cookie / Session
- API Key
- Signature
- Tenant / Locale / Trace Header

以上方案无论通过参数还是安全方案表达，都必须带中文说明。

无法确认时写入待确认并阻断通过验收，不要猜。

## `$ref` 规则

- 含 `$ref` 的对象不得并列 `type`、`properties`、`items`、`required` 等 sibling 字段。
- 需要补 description 时优先放到被引用 schema 上。
- components 命名应稳定，优先使用真实 DTO / model 名。
