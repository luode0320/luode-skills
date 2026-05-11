---
name: api-response-rules
description: 当新增或修改返回体、响应包装器、分页结构、错误响应结构、兼容字段、版本字段或统一响应模型时触发。负责统一响应格式和兼容策略；成功响应和错误响应都必须包含状态码、状态、消息、数据四个字段；若本次改动影响 Swagger/OpenAPI 成功响应、错误响应或分页文档，应与 api-swagger-rules 同步生效；不要用它代替错误处理流程、异常分类或接口入口职责规则。
---

# 接口响应规则

只在判断"接口应该怎么返回、成功响应怎么包、错误响应怎么表达、分页和兼容字段怎么放"时使用这个 skill。
如果当前问题是异常分类、重试降级、错误处理路径或 Swagger/OpenAPI 响应文档同步，请转交相邻 skill。

**重要：成功响应和错误响应都必须包含状态码、状态、消息、数据四个字段。**
**重要：响应解析必须使用明确结构体承接，禁止使用 `map[string]interface{}`、`any`、`json.RawMessage` 作为响应解析入口。**

## Skill 作用与适用场景

- 统一成功响应、错误响应和分页响应的结构表达。
- 强制响应解析使用明确结构体，字段通过 `json` tag 显式声明。
- 约束兼容字段和版本字段的放置方式。
- 保证调用方能稳定理解响应契约。
- 要求成功响应、错误响应、分页结构和兼容字段说明与 `api-swagger-rules` 保持同步。
- 防止把错误处理流程整体混进响应模型层。
- 确保成功响应和错误响应都包含状态码、状态、消息、数据四个字段。

## 自动触发信号

- 新增或修改返回体、统一响应包装器。
- 新增或修改错误响应结构、分页结构、兼容字段或版本字段。
- 不确定某个字段该放在顶层响应还是业务数据体内。
- 不确定接口是否需要统一包裹返回结构。
- 成功响应或错误响应缺少状态码、状态、消息、数据四个字段中的任何一个。
- 准备使用 `map[string]interface{}`、`any`、`json.RawMessage` 直接解析响应体。

## 进入后先做什么

1. 先确认接口入口和请求结构已经稳定。
2. 再判断当前返回是成功结果、错误结果还是分页结果。
3. 明确业务数据、元信息、错误信息和兼容字段的层次。
4. 判断是否需要考虑旧客户端兼容或版本演进。
5. 确认成功响应和错误响应都包含状态码、状态、消息、数据四个字段。
6. 明确响应 DTO 结构并完成字段映射，禁止弱类型容器接收响应。

## 默认执行流程

1. 默认先读 `references/response-shape-baseline.md`，确定响应整体结构。
2. 如果涉及分页、错误或兼容字段，再读 `references/response-variants.md`。
3. 如果需要对照典型正反例，再读 `references/response-examples.md`。
4. 输出成功响应、错误响应、分页结构和兼容字段放置结论。
5. 确认成功响应和错误响应都包含状态码、状态、消息、数据四个字段。
6. 如果当前接口需要 Swagger/OpenAPI 文档或调试入口，请同步交给 `api-swagger-rules` 更新响应文档。
7. 如果问题已经上升到异常处理流程，停止停留在响应层并转交 `error-handling-rules`。
8. 当存在“先解析 map 再手工取字段”的旧代码时，优先改为 DTO 结构化解析。

## 权责边界与不负责事项

- 只负责响应格式，不代替 `error-handling-rules` 设计异常处理流程。
- 不代替 `api-endpoint-rules` 处理入口职责和 HTTP 语义。
- 不代替 `api-request-rules` 设计请求模型。
- 不代替 `api-swagger-rules` 维护 Swagger/OpenAPI 成功响应、错误响应、分页响应和示例。
- 不把日志字段、trace 透传、重试降级等横切策略塞进响应结构本身。
- 确保成功响应和错误响应都包含状态码、状态、消息、数据四个字段。
- 不允许用 `map[string]interface{}`、`any`、`json.RawMessage` 作为响应解析入口容器。

## 需要暂停并确认的条件

- 当前接口是否需要统一包装仍不清楚。
- 兼容字段和版本字段会影响既有客户端解析。
- 错误响应结构调整会波及大量旧调用方。
- 响应层已经无法单独收口，问题实质变成了错误处理机制设计。
- 成功响应或错误响应缺少状态码、状态、消息、数据四个字段中的任何一个。
- 响应字段仍通过 map key 手工读取，未落到明确 DTO。

## 执行通过 / 驳回标准

- 通过：能明确成功 / 错误 / 分页响应结构及兼容字段放置方式，且边界稳定；成功响应和错误响应都包含状态码、状态、消息、数据四个字段；响应解析使用明确 DTO。
- 驳回：返回结构层次混乱、错误信息散落、分页元信息无统一位置、把错误处理逻辑整体写进响应层、成功响应或错误响应缺少必要字段，或响应解析仍为 map/any/RawMessage。

## 结构体解析示例（Go）

```go
type PriceItem struct {
	CType    string `json:"cType"`
	USDPrice string `json:"usdPrice"`
}

type PriceResponse struct {
	Status bool        `json:"status"`
	Msg    string      `json:"msg"`
	Data   []PriceItem `json:"data"`
}

var resp PriceResponse
if err := json.Unmarshal(rawBody, &resp); err != nil {
	return err
}
if !resp.Status {
	return fmt.Errorf("price service failed: %s", resp.Msg)
}
```

反例（禁止）：

```go
var payload map[string]interface{}
_ = json.Unmarshal(rawBody, &payload)
status, _ := payload["status"].(bool)
```

## 执行结果归档要求

- 如果本次定义了统一响应结构、修改了错误响应或兼容字段策略，将结论记录到 `analysis/` 或 `review/`。
- 归档内容至少包含响应目标、结构结论、成功响应字段、错误响应字段、兼容影响和调用方风险。
- 如果只是沿用现有清晰结构且无争议，可以不单独归档。

## references 读取规则

- 默认先读 `references/response-shape-baseline.md`。
- 只有在处理错误、分页和兼容字段时，再读 `references/response-variants.md`。
- 只有在对照正反例时，再读 `references/response-examples.md`。
