# Go 包结构样板

## 用途

用于 Go 项目中决定 `cmd`、`internal`、`pkg` 以及常见业务目录的职责边界。

## 推荐层次

- `cmd/`
  放启动入口、二进制装配和启动参数，不承载核心业务逻辑。
- `internal/`
  放项目私有业务代码，是大多数业务目录的主落点。
- `pkg/`
  只在确实需要对外复用的稳定公共包时使用，不要把所有代码都丢进去。

## 常见目录职责

- `router` 或 `routes`
  路由注册和入口装配。只做路由组织，不写业务逻辑。
- `controller` 或 `handler`
  处理 HTTP 输入输出、参数转换和响应映射。不要直接写复杂业务。
- `service`
  承载业务流程、业务组合和领域规则。
- `repository`
  承载数据库、缓存或外部存储访问。
- `model` 或 `domain`
  承载核心数据结构、领域对象或持久化模型。
- `middleware`
  承载鉴权、日志、追踪、限流等横切入口逻辑。
- `config`
  承载配置读取、配置装配和配置结构定义。
- `constants`
  承载稳定常量、枚举型值和固定配置键。
- `utils`
  只放稳定、无明显业务状态、跨模块可复用的小工具；不要把业务流程塞进去。

## 依赖方向

- `router/routes` -> `controller/handler` -> `service` -> `repository`
- `middleware` 可以依赖稳定公共层，谨慎依赖 `service`
- `utils`、`constants`、`config` 不应反向依赖业务层

## 特别提醒

- `router` 和 `controller` 不一定要同时存在；如果框架已把两者合一，不要机械复制两层。
- 不要为了一个文件新建一个 Go 包，除非后续会稳定扩展。
- `utils` 不是兜底垃圾桶；一旦出现明显业务语义，应回到 `service` 或其他明确目录。
