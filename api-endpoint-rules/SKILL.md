---
name: api-endpoint-rules
description: 当新增或修改 controller、router、handler、路由声明、HTTP 方法、接口 CRUD 路径命名、接口入口职责或超时入口边界时触发。负责统一接口入口设计、路径命名和 HTTP 方法语义；不要用它代替请求参数、响应结构或错误处理规则。
---

# 接口入口规则

只在判断“接口入口该怎么定义、落在哪层、路径怎么命名、HTTP 方法怎么选”时使用这个 skill。
如果当前问题是请求字段、响应包装、错误响应或鉴权细节，请转交相邻接口类 skill。

## Skill 作用与适用场景

- 明确 controller / router / handler 的入口职责边界。
- 统一路径命名、HTTP 方法语义和基础 CRUD 入口设计。
- 约束接口入口只做入口层工作，不直接吞掉业务层职责。
- 防止把请求结构、响应格式和错误处理混进入口定义规则。

## 自动触发信号

- 新增接口或路由。
- 修改 controller、router、handler 入口代码。
- 调整路径命名、HTTP 方法或 CRUD 入口设计。
- 不确定某段逻辑该放在接口入口还是业务层。

## 进入后先做什么

1. 先确认当前是 HTTP / RPC / Web 路由入口问题。
2. 再判断这段逻辑属于路由装配、请求接入还是业务实现。
3. 明确路径命名对象、资源语义和 HTTP 动词语义。
4. 确认入口层只承担接入职责，不直接下沉复杂业务。

## 默认执行流程

1. 默认先读 `references/endpoint-responsibility.md`，判断入口层职责边界。
2. 如果涉及路径命名和方法语义，再读 `references/path-and-method-semantics.md`。
3. 如果涉及 CRUD 接口或典型反例，再读 `references/endpoint-examples.md`。
4. 输出入口落点、路径命名、方法选择和不应放在入口层的逻辑结论。
5. 入口定义稳定后，再交给 `api-request-rules`、`api-response-rules` 等后续 skill 细化。

## 权责边界与不负责事项

- 只负责接口入口设计，不代替 `api-request-rules` 设计参数结构。
- 不代替 `api-response-rules` 设计成功 / 错误 / 分页返回结构。
- 不代替 `error-handling-rules` 设计异常分类和重试降级路径。
- 不把复杂业务编排、领域判断或数据访问直接塞进 controller / handler。

## 需要暂停并确认的条件

- 当前接口语义不清，无法判断资源对象和操作动词。
- 设计会影响既有接口契约或旧路径兼容性。
- 一个入口打算同时承载多个不相干业务动作。
- 当前看起来像入口问题，实则涉及接口整体契约重构。

## 执行通过 / 驳回标准

- 通过：能明确接口入口职责、路径命名、HTTP 方法语义和不应放入入口层的逻辑边界。
- 驳回：路径命名含糊、HTTP 方法乱用、controller / handler 承担过多业务逻辑，或把请求 / 响应规则混作入口问题。

## 执行结果归档要求

- 如果本次定义了新接口入口、调整了既有路径或改变了入口职责边界，将结论记录到 `analysis/` 或 `review/`。
- 归档内容至少包含接口目标、入口层结论、路径命名、方法语义和兼容影响。
- 如果只是沿用现有清晰模式且无争议，可以不单独归档。

## references 读取规则

- 默认先读 `references/endpoint-responsibility.md`。
- 只有在判断路径命名和 HTTP 语义时，再读 `references/path-and-method-semantics.md`。
- 只有在对照 CRUD 与反例时，再读 `references/endpoint-examples.md`。
