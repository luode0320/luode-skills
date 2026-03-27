# 安全边界判定

## 用途

用于区分安全基线问题与 Header、请求参数、错误处理、日志 trace 等横切规则。

## 属于 auth-security-rules

- 认证方式、鉴权控制点、对象级授权、输入校验
- 敏感信息保护、上传下载安全、外部请求安全
- 前端 / 后端 / 浏览器边界上的最终授权和敏感数据暴露问题

## 不属于 auth-security-rules

- Header 命名、来源可信度和透传契约
- 请求参数放 path、query 还是 body
- 错误应该在哪里处理、何时重试、何时降级
- 日志字段、trace 透传和审计记录点本身

## 回流规则

- 如果问题核心是 Header 能否信任、能否透传，回流 `request-header-rules`。
- 如果问题核心是请求模型结构，回流 `api-request-rules`。
- 如果问题核心是错误处理机制，回流 `error-handling-rules`。
- 如果问题核心是日志与 trace 字段，回流 `logging-trace-rules`。
