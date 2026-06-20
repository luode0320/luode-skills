---
name: api-request-review-rules
description: 【强制自动触发】当需要只检查请求参数、DTO、body 结构、参数校验或请求模型是否符合接口请求规范时触发。只读镜像版本，严格沿用 `api-request-rules` 的请求结构标准，不新增请求规范，不直接改代码；默认优先并行；适合在请求结构收口前做并行预审。
---

# 接口请求检查镜像规则

## 目标

只检查当前请求模型是否满足 `api-request-rules` 的请求结构标准，不执行修改。

## 源规则

以下判定严格沿用源 skill：

- 只使用 POST 请求
- 所有参数通过 JSON body 传递
- 请求解析必须使用明确 DTO
- 禁止使用 map / any / RawMessage 作为请求入口
- `ShouldBindJSON` 应作为 controller 绑定方式

## 自动触发信号

- 新增或修改 body 结构、请求 DTO、请求模型。
- 新增或修改参数校验器。
- 试图使用 path 参数或 query 参数。
- 准备使用 `map[string]interface{}`、`any`、`json.RawMessage` 直接接请求体。

## 进入后先做什么

1. 先确认当前接口入口已经稳定，且只使用 POST 请求。
2. 确认所有请求参数通过 JSON body 传递。
3. 明确请求 DTO 结构。
4. 确认 controller 中使用 `ShouldBindJSON`。

## 默认执行流程

1. 先读取 `api-request-rules`。
2. 如需判断请求边界或正反例，再读源 skill 的对应 references。
3. 输出请求结构建议、字段落点、校验层次和 `ShouldBindJSON` 使用方式。
4. 不直接改代码，只输出缺口。

## 权责边界与不负责事项

- 不代替 `api-endpoint-rules` 设计入口职责。
- 不代替 `api-response-rules` 设计返回结构。
- 不代替 `api-swagger-rules` 维护请求字段说明和示例。
- 不代替业务层判断复杂业务规则是否成立。

## 需要暂停并确认的条件

- 试图使用 path 参数或 query 参数。
- 请求字段还在 map 中以字符串 key 手工读取，未落到明确 DTO。
- 校验条件已经超出基础参数层。
- DTO 设计已经耦合到特定内部实现。

## 执行通过 / 驳回标准

- 通过：字段落点在 JSON body、请求模型边界清晰、基础校验明确、controller 正确使用 `ShouldBindJSON`。
- 驳回：使用了 path/query 参数、请求仍用 map/any/RawMessage 解析，或让请求结构失去稳定语义。

## 执行结果归档要求

- 如果本次定义了新的请求模型、调整了关键字段或改变了校验层次，将结论记录到 `analysis/` 或 `review/`。
- 归档内容至少包含请求目标、字段落点、校验规则、`ShouldBindJSON` 使用方式和兼容影响。
- 如果只是沿用既有清晰模式且无争议，可以不单独归档。

## 读取规则

- 默认先读 `api-request-rules`。
- 只有在判断请求边界或正反例时，再读源 skill 的对应 references。
