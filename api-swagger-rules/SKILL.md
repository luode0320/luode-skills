---
name: api-swagger-rules
description: 当新增或修改后端 HTTP API、Swagger/OpenAPI 框架接入、接口文档注解/注释、Swagger 调试入口、接口分组标签、文档暴露路径或 Swagger 环境开关时触发。负责统一 Swagger/OpenAPI 框架选型边界、接口文档最小必填项、请求/响应同步、调试可用性和暴露安全规则；对存在 HTTP API 且需要联调/调试的后端项目，默认要求使用统一的 Swagger/OpenAPI 方案；不要用它代替 api-endpoint-rules、api-request-rules、api-response-rules、普通业务注释规则或功能验证。
---

# Swagger / OpenAPI 规则

只在判断“后端 HTTP API 是否需要 Swagger/OpenAPI、应该如何接入、如何保持接口文档同步、如何开放调试入口”时使用这个 skill。
如果当前主要问题是接口入口职责、请求字段结构、响应包装或错误处理，请先转交相邻 API skill。

**重要：只要项目存在需要开发/测试联调或接口调试的后端 HTTP API，就默认要求项目使用统一的 Swagger/OpenAPI 方案；同一项目只保留一套主方案。**

## Skill 作用与适用场景

- 统一后端 HTTP API 项目的 Swagger/OpenAPI 接入基线。
- 要求接口代码、请求模型、响应模型与 Swagger/OpenAPI 文档保持同步。
- 统一接口最小文档字段、分组标签、鉴权说明和示例要求。
- 统一 Swagger/OpenAPI 调试入口在开发、测试、生产环境中的开放策略。
- 防止把 Swagger/OpenAPI 当成“普通注释”随手维护，最终导致接口文档漂移。
- 防止同一项目同时混用多套 Swagger/OpenAPI 方案。

## 自动触发信号

- 新增或修改后端 HTTP API。
- 新增或修改 Swagger/OpenAPI 框架、文档注解、文档生成脚本或 Swagger UI 暴露入口。
- 新增或修改接口分组 tag、接口摘要、接口说明、鉴权说明、请求体/响应体文档定义。
- 需要通过 Swagger/OpenAPI 页面直接调试接口。
- 需要决定开发环境、测试环境或生产环境是否开放 Swagger UI。
- 实现评审中发现接口代码已改，但 Swagger/OpenAPI 文档或注解没有同步。

## 进入后先做什么

1. 先确认当前项目是否存在后端 HTTP API，以及是否存在联调或接口调试诉求。
2. 如果存在 HTTP API，先确认项目是否已经有统一的 Swagger/OpenAPI 主方案；没有时默认补齐，不允许继续长期缺失。
3. 确认当前接口应补哪些最小文档字段：摘要、tag、请求体、成功响应、错误响应、鉴权要求、示例。
4. 再对照 `api-endpoint-rules`、`api-request-rules`、`api-response-rules`，确认路径、请求、响应与文档是否同步。
5. 确认哪些接口应隐藏、标记弃用或限制调试，不把内部接口和临时调试接口默认暴露出去。
6. 确认 Swagger/OpenAPI 在各环境中的开放策略，生产环境默认关闭或受控开放。

## 默认执行流程

1. 默认先读 `references/baseline-and-scope.md`，确认项目是否必须接入 Swagger/OpenAPI，以及最小交付基线。
2. 如果重点是“代码改了但文档怎么同步”，再读 `references/sync-and-annotation-rules.md`。
3. 如果重点是“哪些环境能开 Swagger、怎么保护调试入口”，再读 `references/exposure-and-security.md`。
4. 输出当前项目是否需要 Swagger/OpenAPI、应采用的统一方案边界、当前接口的文档同步要求和环境开放结论。
5. Swagger/OpenAPI 方案确定后，再回到 `api-endpoint-rules`、`api-request-rules`、`api-response-rules` 继续收口具体接口细节。

## 权责边界与不负责事项

- 只负责 Swagger/OpenAPI 方案、接口文档同步和调试入口规则，不代替 `api-endpoint-rules` 设计接口入口职责。
- 不代替 `api-request-rules` 设计请求 DTO 和字段校验。
- 不代替 `api-response-rules` 设计统一响应结构、错误响应结构和分页返回。
- 不把 Swagger/OpenAPI 注解/注释当成普通业务注释处理，那属于接口契约和调试入口规则。
- 不把 Swagger/OpenAPI 页面调试本身当成功能验证结论；是否正确仍交给测试域。
- 不要求纯定时任务、纯消息消费、纯内部工具库、无 HTTP API 的项目强行接入 Swagger/OpenAPI。

## 需要暂停并确认的条件

- 项目是否真的存在需要联调/调试的 HTTP API 仍不明确。
- 当前仓库已经混用两套及以上 Swagger/OpenAPI 方案，无法直接判断主方案。
- 当前接口包含内部管理能力、敏感调试能力或高风险运维入口，是否暴露需额外确认。
- 生产环境希望开放 Swagger UI，但没有鉴权、IP 限制、环境开关或其他保护措施。
- 接口代码、请求模型、响应模型和现有 Swagger/OpenAPI 文档冲突严重，无法直接判断以哪份为准。

## 执行通过 / 驳回标准

- 通过：存在 HTTP API 且需要联调/调试的项目已采用统一 Swagger/OpenAPI 方案；接口文档包含最小必填项；接口路径、请求模型、响应模型与 Swagger/OpenAPI 文档保持同步；开发/测试调试入口可用；生产环境默认关闭或受控开放。
- 驳回：项目明明长期依赖 HTTP API 联调，却没有统一 Swagger/OpenAPI 方案；或代码已改但接口文档未同步；或同一项目混用多套 Swagger/OpenAPI；或生产环境直接裸开 Swagger UI。

## 执行结果归档要求

- 一般不要求单独归档；接口文档与注解本身就是主要交付物。
- 如果本轮新增或调整了 Swagger/OpenAPI 访问路径、环境开关、鉴权方式或接口分组策略，应在评审结论或项目说明中补一句可追溯说明。
- 如果项目从“无 Swagger/OpenAPI”切换为“有统一方案”，应在相关实施记录中明确方案入口和使用范围。

## references 读取规则

- 默认先读 `references/baseline-and-scope.md`。
- 只有在判断代码与文档同步要求时，再读 `references/sync-and-annotation-rules.md`。
- 只有在判断暴露策略和安全边界时，再读 `references/exposure-and-security.md`。
