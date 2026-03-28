# 接口入口职责边界

## 用途

用于判断 controller、router 到底该做什么，不该做什么。

**重要：必须以 `package-structure-rules` 为基准，不使用 handler 包名。**

## 入口层应负责

- 路由声明与入口绑定（使用 internal/router）
- 参数接入与基础调用组织
- 调用业务层
- 返回响应对象

## 入口层不应负责

- 复杂业务编排
- 深层领域规则判断
- 直接写数据库访问细节
- 把多个不相干动作混到一个入口

## 原则

- 入口层应薄，不应成为业务中心。
- 入口层只负责把请求安全、清晰地引到正确的业务逻辑。
- 使用 `internal/controller`、`internal/router`，不使用 handler 包名。
