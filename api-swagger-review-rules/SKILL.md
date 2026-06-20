---
name: api-swagger-review-rules
description: 【强制自动触发】当需要只检查后端 HTTP API 的 Swagger/OpenAPI 接入、接口文档同步、调试入口暴露、文档分组标签、路径或环境开关是否合规时触发。只读镜像版本，严格沿用 `api-swagger-rules` 的 Swagger/OpenAPI 标准，不新增文档规范，不直接改代码；默认优先并行；适合在文档收口前做并行预审。
---

# Swagger/OpenAPI 检查镜像规则

## 目标

只检查当前后端 HTTP API 是否满足 `api-swagger-rules` 的文档与调试入口标准，不执行修改。

## 源规则

以下判定严格沿用源 skill：

- 接口代码、请求模型、响应模型与 Swagger/OpenAPI 文档保持同步
- 统一接口最小文档字段、分组标签、鉴权说明和示例要求
- 统一调试入口在各环境中的开放策略
- 不混用多套 Swagger/OpenAPI 方案

## 自动触发信号

- 新增或修改后端 HTTP API。
- 新增或修改 Swagger/OpenAPI 框架、文档注解、文档生成脚本或 UI 暴露入口。
- 新增或修改接口分组 tag、接口摘要、接口说明、鉴权说明、请求体/响应体文档定义。
- 实现评审中发现接口代码已改，但文档或注解没有同步。

## 进入后先做什么

1. 先确认当前项目是否存在后端 HTTP API，以及是否存在联调或接口调试诉求。
2. 如果存在 HTTP API，先确认项目是否已经有统一的 Swagger/OpenAPI 主方案。
3. 确认当前接口应补哪些最小文档字段。
4. 再对照 `api-endpoint-rules`、`api-request-rules`、`api-response-rules`。

## 默认执行流程

1. 先读取 `api-swagger-rules`。
2. 如需判断文档同步要求，再读源 skill 的对应 references。
3. 如需判断暴露策略和安全边界，再读源 skill 的对应 references。
4. 输出当前项目是否需要 Swagger/OpenAPI、统一方案边界和调试入口结论。
5. 不直接改代码，只输出缺口。

## 权责边界与不负责事项

- 不代替 `api-endpoint-rules` 设计接口入口职责。
- 不代替 `api-request-rules` 设计请求 DTO 和字段校验。
- 不代替 `api-response-rules` 设计统一响应结构。
- 不把 Swagger/OpenAPI 注解当成普通业务注释处理。

## 需要暂停并确认的条件

- 项目是否真的存在需要联调/调试的 HTTP API 仍不明确。
- 当前仓库已经混用两套及以上 Swagger/OpenAPI 方案。
- 当前接口包含内部管理能力、敏感调试能力或高风险运维入口。
- 生产环境希望开放 Swagger UI，但没有保护措施。

## 执行通过 / 驳回标准

- 通过：存在 HTTP API 且需要联调/调试的项目已采用统一 Swagger/OpenAPI 方案；接口文档包含最小必填项；接口路径、请求模型、响应模型与文档保持同步。
- 驳回：项目明明长期依赖 HTTP API 联调，却没有统一 Swagger/OpenAPI 方案；或代码已改但接口文档未同步；或同一项目混用多套方案。

## 执行结果归档要求

- 如果本轮新增或调整了 Swagger/OpenAPI 访问路径、环境开关、鉴权方式或接口分组策略，应在评审结论或项目说明中补一句可追溯说明。
- 如果项目从“无 Swagger/OpenAPI”切换为“有统一方案”，应在相关实施记录中明确方案入口和使用范围。

## 读取规则

- 默认先读 `api-swagger-rules`。
- 只有在判断代码与文档同步要求时，再读源 skill 的对应 references。
- 只有在判断暴露策略和安全边界时，再读源 skill 的对应 references。
