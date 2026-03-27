# Node / Python 模块样板

## 用途

用于 Node.js 和 Python 项目中决定模块目录、分层边界和依赖方向。

## 常见目录职责

- `routers` / `routes`
  处理路由声明和入口绑定。
- `controllers` / `handlers`
  处理请求输入输出、调用业务层并组织响应。
- `services`
  承载业务流程和业务组合逻辑。
- `repositories` / `dao`
  承载数据库或存储访问。
- `models` / `schemas`
  承载数据结构、ORM 模型、校验模型或序列化模型。
- `middleware`
  承载鉴权、日志、追踪、上下文注入等横切逻辑。
- `config`
  承载配置读取、环境装配和设置定义。
- `constants`
  承载稳定常量、状态码、配置键。
- `utils`
  承载无状态、跨模块复用的小工具。

## 依赖方向

- `routes` -> `controllers/handlers` -> `services` -> `repositories`
- `models/schemas` 根据框架职责可被入口层和数据层共享，但不要变成万能目录
- `middleware` 只做横切处理，不承载完整业务流程
- `utils`、`constants`、`config` 不应反向依赖业务层

## 特别提醒

- 同一个项目不要同时混用多套命名，如一部分叫 `service`，另一部分叫 `usecases`，除非边界非常明确。
- `schemas` 既可能是请求校验模型，也可能是数据库模型，要在项目内保持含义稳定。
- Python 的模块文件不要因为临时方便而散落在根目录，优先归入清晰职责目录。
