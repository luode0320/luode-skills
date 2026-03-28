---
name: api-request-rules
description: 当新增或修改请求参数、DTO、body 结构、参数校验或请求模型时触发。负责统一请求结构、参数表达和基础校验边界；必须以 api-endpoint-rules 为基准，只使用 POST 请求，所有参数通过 JSON body 传递；不要用它代替接口入口设计、响应结构或业务规则本身。
---

# 接口请求规则

只在判断"请求参数该放在哪里、怎么表达、怎么校验"时使用这个 skill。
如果当前问题是入口职责、响应结构或错误处理，请转交相邻接口类 skill。

**重要：本 skill 必须以 `api-endpoint-rules` 为基准，只使用 POST 请求，所有请求参数必须通过 JSON body 传递；不使用 path 参数、query 参数；统一在 controller 中使用 ShouldBindJSON 进行参数绑定和处理。**

## Skill 作用与适用场景

- 统一使用 JSON body 作为唯一的请求参数载体（不使用 path、query 参数）。
- 统一必填字段、可选字段和基础参数校验表达方式。
- 约束请求结构只表达输入契约，不吞掉业务规则本身。
- 防止把参数校验、业务校验和响应处理混成一层。
- 统一在 controller 中使用 ShouldBindJSON 进行参数绑定和错误处理。

## 自动触发信号

- 新增或修改 body 结构、请求 DTO、请求模型。
- 新增或修改参数校验器。
- 试图使用 path 参数或 query 参数（必须提醒统一使用 JSON body）。
- 不确定某个校验属于基础参数校验还是业务规则校验。
- controller 中没有使用 ShouldBindJSON 进行参数绑定。

## 进入后先做什么

1. 先确认当前接口入口已经稳定，且只使用 POST 请求。
2. 确认所有请求参数通过 JSON body 传递，不使用 path 参数、query 参数。
3. 判断字段属于写入载荷还是辅助上下文。
4. 明确哪些字段必须传、哪些字段可选。
5. 区分基础格式校验和真正的业务规则校验。
6. 确认在 controller 中使用 ShouldBindJSON 进行参数绑定和错误处理。

## 默认执行流程

1. 先确认遵循 `api-endpoint-rules` 的约定：只使用 POST 请求，所有参数通过 JSON body 传递。
2. 默认先读 `references/request-shape-boundaries.md`，判断 JSON body、DTO 的边界。
3. 如果涉及参数必填、可选和格式校验，再读 `references/parameter-validation-rules.md`。
4. 如果需要对照常见正反例，再读 `references/request-examples.md`。
5. 输出请求结构建议、字段落点、校验层次、ShouldBindJSON 使用方式和不应放入请求层的逻辑。
6. 请求结构稳定后，再交给响应、错误处理等后续 skill 继续收口。

## 权责边界与不负责事项

- 只负责请求结构和基础参数校验，不代替 `api-endpoint-rules` 设计入口职责。
- 不代替 `api-response-rules` 设计返回结构。
- 不代替业务层判断复杂业务规则是否成立。
- 不把鉴权、租户、trace 等请求头问题混入参数模型设计。
- 必须遵循 `api-endpoint-rules` 的约定，只使用 POST + JSON body。

## 需要暂停并确认的条件

- 试图使用 path 参数或 query 参数（必须提醒统一使用 JSON body）。
- 校验条件已经超出基础参数层，明显进入业务规则层。
- DTO 设计已经耦合到特定内部实现，可能泄漏内部模型。
- 请求结构调整会影响旧接口兼容性。

## 执行通过 / 驳回标准

- 通过：能明确字段落点在 JSON body、请求模型边界、必填 / 可选表达、基础参数校验层次、controller 中正确使用 ShouldBindJSON 进行参数绑定和错误处理。
- 驳回：使用了 path 或 query 参数、DTO 与内部模型混淆、把业务规则硬塞进参数校验、controller 中没有使用 ShouldBindJSON、或让请求结构失去稳定语义。

## 执行结果归档要求

- 如果本次定义了新的请求模型、调整了关键字段或改变了校验层次，将结论记录到 `analysis/` 或 `review/`。
- 归档内容至少包含请求目标、字段落点、校验规则、ShouldBindJSON 使用方式和兼容影响。
- 如果只是沿用既有清晰模式且无争议，可以不单独归档。

## references 读取规则

- 默认先读 `references/request-shape-boundaries.md`。
- 只有在判断校验表达时，再读 `references/parameter-validation-rules.md`。
- 只有在对照正反例时，再读 `references/request-examples.md`。
