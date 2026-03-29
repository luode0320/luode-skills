---
name: api-endpoint-rules
description: 当新增或修改 controller、router、路由声明、HTTP 方法、接口路径命名、接口入口职责或超时入口边界时触发。负责统一接口入口设计、路径命名和强制使用 POST 方法；必须以 package-structure-rules 为基准，不使用 handler 包名；不要用它代替请求参数、响应结构或错误处理规则。
---

# 接口入口规则

只在判断"接口入口该怎么定义、落在哪层、路径怎么命名、HTTP 方法怎么选"时使用这个 skill。
如果当前问题是请求字段、响应包装、错误响应或鉴权细节，请转交相邻接口类 skill。

**重要：本 skill 必须以 `package-structure-rules` 为基准，不使用 handler 包名；所有 API 接口强制使用 POST 请求，JSON 作为 body；不允许使用 GET、PATCH、PUT、DELETE 等其他请求类型。**

## Skill 作用与适用场景

- 明确 controller / router 的入口职责边界（不使用 handler）。
- 统一路径命名、强制使用 POST 方法和 JSON body。
- 约束接口入口只做入口层工作，不直接吞掉业务层职责。
- 防止把请求结构、响应格式和错误处理混进入口定义规则。
- 确保接口路径名称语义清晰、类型清楚，通过路径区分操作类型（如 /orders/get、/orders/del、/orders/add）。

## 强制规则：Go 路由注册写法（internal/router）

- 路由注册必须显式声明，不使用通用路由包装器（如 `registerPostRoutes`、route 列表驱动）隐藏具体接口声明。
- 路由 path 必须在注册处直接硬编码，不使用路径常量引用（除全局根前缀如 `/api/walletPay` 外）。
- 每个接口使用 `group.POST("/path", controller.Method)` 直接注册。
- 接口注释放在注册语句上一行，不在参数行内写注释，避免 `gofmt` 自动拆行影响可读性。
- 禁止使用 `GET/PATCH/PUT/DELETE`；所有接口统一 `POST + JSON body`。
- 禁止在 path 中使用 `:id` 或 `{id}` 风格参数；查询类接口也通过 `POST body` 传参。

## 自动触发信号

- 新增接口或路由。
- 修改 controller、router 入口代码（不使用 handler）。
- 调整路径命名、HTTP 方法或接口设计。
- 不确定某段逻辑该放在接口入口还是业务层。
- 使用了非 POST 请求类型（GET、PATCH、PUT、DELETE 等）。
- 路径命名没有明确区分操作类型。

## 进入后先做什么

1. 先确认当前是 HTTP / RPC / Web 路由入口问题。
2. 再判断这段逻辑属于路由装配、请求接入还是业务实现。
3. 确认所有接口强制使用 POST 请求，JSON 作为 body。
4. 明确路径命名对象、资源语义和操作类型（通过路径区分 get/add/del/update 等）。
5. 确认入口层只承担接入职责，不直接下沉复杂业务。
6. 确认使用 `internal/controller`、`internal/router`，不使用 handler 包名。

## 默认执行流程

1. 先确认遵循 `package-structure-rules` 的约定：使用 `internal/controller`、`internal/router`，不使用 handler 包名。
2. 默认先读 `references/endpoint-responsibility.md`，判断入口层职责边界。
3. 如果涉及路径命名和方法语义，再读 `references/path-and-method-semantics.md`。
4. 如果涉及接口或典型反例，再读 `references/endpoint-examples.md`。
5. 输出入口落点、路径命名、强制使用 POST 方法和不应放在入口层的逻辑结论。
6. 入口定义稳定后，再交给 `api-request-rules`、`api-response-rules` 等后续 skill 细化。

## 权责边界与不负责事项

- 只负责接口入口设计，不代替 `api-request-rules` 设计参数结构。
- 不代替 `api-response-rules` 设计成功 / 错误 / 分页返回结构。
- 不代替 `error-handling-rules` 设计异常分类和重试降级路径。
- 不把复杂业务编排、领域判断或数据访问直接塞进 controller。
- 必须遵循 `package-structure-rules` 的约定，不使用 handler 包名。

## 需要暂停并确认的条件

- 当前接口语义不清，无法判断资源对象和操作动词。
- 设计会影响既有接口契约或旧路径兼容性。
- 一个入口打算同时承载多个不相干业务动作。
- 当前看起来像入口问题，实则涉及接口整体契约重构。
- 试图使用非 POST 请求类型。

## 执行通过 / 驳回标准

- 通过：能明确接口入口职责、路径命名语义清晰且包含操作类型、强制使用 POST 方法 + JSON body、使用 internal/controller/internal/router 而不使用 handler、明确不应放入入口层的逻辑边界。
- 驳回：路径命名含糊、使用了非 POST 请求类型、controller 承担过多业务逻辑、使用了 handler 包名、或把请求 / 响应规则混作入口问题。

## 执行结果归档要求

- 如果本次定义了新接口入口、调整了既有路径或改变了入口职责边界，将结论记录到 `analysis/` 或 `review/`。
- 归档内容至少包含接口目标、入口层结论、路径命名、POST 方法语义和兼容影响。
- 如果只是沿用现有清晰模式且无争议，可以不单独归档。

## references 读取规则

- 默认先读 `references/endpoint-responsibility.md`。
- 只有在判断路径命名和 POST 语义时，再读 `references/path-and-method-semantics.md`。
- 只有在对照接口与反例时，再读 `references/endpoint-examples.md`。
