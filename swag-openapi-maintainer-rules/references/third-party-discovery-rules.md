# 上游/第三方出站接口发现规则

本文件定义如何从业务项目当前代码发现本项目主动调用的外部第三方 API 和公司内部其他服务接口。当前代码是唯一真相源；不联网抓取官方文档，不把上游完整 API 列表误当成本项目实际调用面。

## 发现范围与真相源

必须覆盖业务代码中所有主动发起的出站 HTTP 调用，包括：

- HTTP client、SDK wrapper、RPC 网关或项目内通用请求封装的调用点。
- 外部第三方 API 和公司内部其他服务；两者都落在上游服务子目录，不另设第二套目录模型。
- 代码中实际构造出的 method、path、query、header、request body、响应解码类型和错误处理分支。

发现顺序固定为：

1. 扫描 client、request builder、SDK wrapper、HTTP 方法调用和响应解码入口。
2. 从请求构造代码确定 HTTP method + path；从 base URL 常量、配置键或 client 初始化确定上游服务与 `base_url`。
3. 追踪请求 DTO、序列化字段、header/鉴权和响应消费结构体；字段说明优先按 `description-rules.md` 的上游分支取真实中文来源。
4. 按上游服务建立稳定 ASCII `vendor-slug`，写入 `swag/<vendor-slug>/` 独立成套产物。
5. 在 manifest 的每个接口上记录 `source_client_file`、`source_symbols` 与 `discovery_confidence`，使 YAML 可以回溯到代码调用点。

## 方法、路径与服务判定

- method 必须来自实际请求调用参数、请求 builder 或封装方法的明确分支，不能只根据函数名猜测。
- path 必须来自实际 URL path 模板、常量、路由拼接或可静态求值的参数；动态拼接无法稳定求值时，接口标记待确认并阻断通过。
- `base_url` 必须来自代码常量、local 配置映射或 client 初始化的实际解析结果；禁止用生产环境或网络探测结果补证据。
- 同一上游服务的不同 base URL 变体只有在代码明确区分服务边界时才拆分 vendor slug；无法稳定区分时列为冲突，不得覆盖生成。
- 同一 method + path 在同一上游重复发现时，必须合并真实来源或报告冲突，不能静默生成两份 operation。

## 响应结构与中文说明

- 只记录本项目实际消费到的响应字段；未被代码读取或解码的上游字段不为了“补全官方模型”而写入。
- 响应结构体、字段 tag、解码逻辑和调用方读取代码优先于历史接口文档。
- 官方文档只能作为离线、受控的补充线索，且必须能与代码消费字段对应；不允许在线抓取或凭官方文档编造本项目未消费的字段。
- 第三方自身的鉴权、错误结构和响应包装按真实代码表达，不套用本项目自有接口的统一响应包装规则。
- 无法确认字段含义时保留待确认状态并阻断该接口通过，不以英文名或猜测性中文描述伪造完成。

## 发现置信度与 coverage

`discovery_confidence` 只表示代码证据强度：

- `high`：method、path、base URL、响应消费结构和来源符号均由静态代码明确确定。
- `medium`：存在一个可验证的配置解析或封装间接层，但调用链和最终字段仍可回溯。
- `low`：存在动态 URL、反射、运行时注册或无法静态解析的关键部分；必须列待确认，不能作为已通过接口交付。

上游 manifest 使用 `coverage: partial`，因为它只代表本项目已发现并实际调用的接口子集。不得声称该 manifest 覆盖上游服务全部接口。

## 与相邻规则的边界

- `naming-rules.md` 负责 vendor slug、B1 目录、manifest 字段、单接口文件名和清理隔离；本文件只负责发现证据。
- `schema-rules.md` 负责第三方 OpenAPI 的 servers、鉴权和响应 schema 结构；本文件只提供真实来源和消费范围。
- `description-rules.md` 负责中文字段说明来源与禁止编造边界；本文件只规定第三方说明必须回溯代码消费。
- `test-program-rules` 负责先探测、再建模和离线测试程序结构；本文件不替代测试实现。
- `code-readability-rules` 与 `implementation-review-rules` 负责 client/响应结构体代码的可读性和审查；本文件不要求修改业务代码。
- `api-request-rules` 约束本项目对外暴露接口的请求模型；上游请求属于出站调用发现，不能反向修改业务 DTO 契约。

## 发现完成标准

每个上游接口必须同时具备：

- 稳定 vendor slug、`base_url`、method、path 和 operationId。
- 至少一个 `source_client_file` 与可回溯的 `source_symbols`。
- 只包含已消费字段的请求/响应 schema 与中文说明来源。
- `source_type: upstream`、`upstream` 与子目录名一致、`coverage: partial`。
- 若任一关键证据缺失，manifest 必须保留待确认状态并阻断该接口通过，而不是生成一个看似完整的 YAML。
