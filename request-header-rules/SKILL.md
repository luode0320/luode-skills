---
name: request-header-rules
description: 当新增或修改认证头、trace-id、span-id、租户头、幂等键、客户端上下文头、X-Forwarded-* 逻辑时自动触发。负责统一请求头分类、来源可信度、透传边界和消费规则，避免把请求参数、日志字段和安全策略混进 Header 约定；不要用它代替 api-request-rules、logging-trace-rules 或 auth-security-rules。
---

# 请求头规则

只在“哪些信息应放 Header、这些 Header 谁能写、谁能信、如何透传”这个问题上使用这个 skill。
如果当前问题是请求参数模型、日志记录点或鉴权策略本身，请转交对应 skill。

## Skill 作用与适用场景

- 统一认证头、trace 头、span 头、租户头、幂等键、客户端上下文头和转发头的分类与职责。
- 约束 Header 来源可信度、透传边界、覆盖规则和消费位置。
- 防止把请求参数、日志字段、业务规则或安全策略误塞进 Header 约定。
- 为接口、日志、鉴权和联调场景提供稳定的请求上下文基线。

## 自动触发信号

- 新增或修改认证头、trace-id、span-id、租户头、幂等键、客户端上下文头、`X-Forwarded-*` 逻辑。
- 需要决定某个信息应放 Header、query、body 还是日志字段时。
- 需要确认 Header 是否应透传、是否允许客户端自传、是否允许网关覆盖时。
- 发现上下游对同一 Header 的含义、命名或可信来源不一致时。

## 进入后先做什么

1. 先识别当前 Header 属于认证、链路追踪、租户上下文、幂等控制、代理转发还是客户端上下文。
2. 判断 Header 的写入方、透传方和最终消费方分别是谁。
3. 明确该 Header 是否可由客户端提供，还是只能由网关或服务端生成。
4. 区分当前问题是 Header 契约问题，还是请求参数、日志记录或安全校验问题。

## 默认执行流程

1. 默认先读 `references/header-categories-and-trust.md`，确定 Header 分类和可信边界。
2. 如果涉及透传、覆盖、网关注入和代理头，再读 `references/propagation-and-forwarding.md`。
3. 如果需要对照正反例或区分 Header / 参数 / 日志边界，再读 `references/header-boundaries-and-examples.md`。
4. 输出 Header 分类、命名、可信来源、透传规则和禁止用法。
5. 如果问题本质变成鉴权、日志或请求模型问题，停止停留在 Header 层并转交相邻 skill。

## 权责边界与不负责事项

- 只负责 Header 约定、可信来源和透传边界，不负责请求参数设计，那属于 `api-request-rules`。
- 不负责日志记录点、trace 字段落日志还是审计日志，那属于 `logging-trace-rules`。
- 不负责认证鉴权策略、对象级授权和输入校验，那属于 `auth-security-rules`。
- 不把业务查询条件、业务控制字段和大块业务数据伪装成 Header。
- 不默认所有 Header 都能跨服务透传，也不默认所有客户端自传 Header 都可信。

## 需要暂停并确认的条件

- 当前 Header 既可能由客户端传入，也可能由网关重写，可信边界不清。
- 当前 Header 修改会影响上下游已有契约或代理配置。
- 当前团队试图用 Header 携带核心业务参数、业务筛选条件或超长上下文数据。
- `X-Forwarded-*`、真实 IP、租户头、认证头之间的优先级和覆盖关系不清。

## 执行通过 / 驳回标准

- 通过：Header 分类清楚，可信来源明确，透传和覆盖规则可解释，且没有把参数、日志或安全策略混进 Header 契约。
- 驳回：Header 含义混乱、来源不可信、透传链断裂，或用 Header 承载不该放入协议头的业务语义。

## 执行结果归档要求

- 将 Header 结论记录到接口契约、联调说明、网关说明或评审记录中。
- 归档内容至少包含 Header 名称、用途、来源、透传路径、可信边界和兼容影响。
- 如果新增了网关注入或幂等 Header，必须同步记录生成方、覆盖方和失效条件。

## references 读取规则

- 默认先读 `references/header-categories-and-trust.md`。
- 只有在涉及透传、代理和网关覆盖时，再读 `references/propagation-and-forwarding.md`。
- 只有在需要边界判定和正反例时，再读 `references/header-boundaries-and-examples.md`。
