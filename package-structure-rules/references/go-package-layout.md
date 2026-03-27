# Go 包结构样例

## 用途

用于 Go 项目中判断 `main.go`、`internal`、`utils`、`common`、`global`、`middleware`、`crontask` 以及常见业务目录的职责边界。

## 推荐层次

- 项目根目录 `main.go`
  默认把启动入口直接放在项目根目录的 `main.go`。这里只做启动装配、依赖初始化、路由挂载和服务启动，不承载核心业务逻辑。除非项目确实存在多个独立二进制入口，否则不要默认引入 `cmd/`。
- `internal/`
  放项目私有业务代码，是大多数业务目录的主落点。对于单二进制 Go 服务，项目私有代码默认优先放在 `internal/` 下。这里可以包含项目自适应的实现细节，也可以包含只对当前项目成立的 `utils` 子包。
- `internal/<adapter>/`
  放项目私有的协议适配层或基础设施适配层，例如 `internal/chain`、`internal/wss`。这类目录可以存在，不强制要求统一固定名称，但必须表达清晰职责，不能退化成新的杂项目录。
- `utils/`
  放可以稳定复用、可迁移到其他项目的公共包。它是对外复用的稳定公共层，不是 `pkg/` 的替代写法，而是直接表达“稳定可移植工具包”的职责。
- `common/`
  放和当前项目存在依赖关系、但在多个模块之间通用的公共包。它也是工具型或支撑型目录，但不要求可直接迁移到其他项目。
- `global/`
  放已经初始化完成、可能被多个位置直接引用的全局实例或全局引用入口。例如 `global/config`、`global/database`。这里承载的是“全局已装配对象”，不是普通配置读取逻辑或业务服务。`global/` 既不是对外公共复用包，也不是 `internal/` 下的私有变体；项目私有的全局实例入口也必须放在根级 `global/`，不允许使用 `internal/global` 或 `internal/runtimectx`。
- `middleware/`
  放鉴权、日志、追踪、限流等横切入口逻辑。`middleware` 作为明确的入口层目录单独存在，不放进 `internal/`。在单服务私有项目里，`internal/middleware` 视为不合规。
- `crontask/`
  放定时任务入口、任务注册、调度装配和定时触发逻辑。`crontask` 属于最外层次的入口包，和 `common`、`global`、`middleware` 同级，不放进 `internal/`。在单服务私有项目里，`internal/crontask` 视为不合规。

## 常见目录职责

- `router`
  负责路由注册和入口装配。默认使用 `router`，不要使用 `routes`。
- `controller`
  负责 HTTP 输入输出、参数转换和响应映射。默认使用 `controller`，不要使用 `handler`。
- `service`
  负责业务流程、领域规则和跨仓储编排。
- `repository`
  负责数据库、缓存或外部存储访问。
- `model`
  负责核心数据结构、领域对象或持久化模型。默认使用 `model`，不要使用 `domain` 作为这层的目录名。
- `utils`
  只放稳定、职责清晰、没有明显业务状态的小工具。它不是兜底目录，也不是“暂时不知道放哪”的落点。
- `common`
  放项目相关但可在多个模块复用的公共支撑代码，例如和当前项目配置、基础设施、通用协议适配有关的复用逻辑。
- `global`
  放已经装配完成的共享实例引用，例如配置实例、数据库实例、日志实例、缓存实例等。项目私有的全局实例入口也必须保持根级 `global/`，不要转成 `internal/global` 或 `internal/runtimectx`。
- `crontask`
  负责定时任务命名、任务注册、调度入口和任务装配。这里处理的是定时触发入口，不承载横切中间件职责。任务调度注册和任务实现都放在 `crontask` 包内，不同任务使用任务自己的子包存放。
- `worker`
  只在项目确实存在独立异步消费、常驻执行或队列执行模型时再单独引入。不要把定时任务实现随意拆到 `worker`，导致 `crontask` 只剩空壳调度入口。

## 依赖方向

- 默认依赖方向为 `router` -> `controller` -> `service` -> `repository`。
- 分层推进时优先使用显式依赖注入逐层装配，优先通过构造函数、参数或明确的实例传递表达依赖关系。
- 不建议先做一批全局初始化实例，再让业务层反向回头依赖这些预设对象，避免真实依赖方向被隐藏。
- `middleware` 可以依赖稳定公共层或必要的业务接口，但要避免演变成新的业务承载层。
- `crontask` 可以依赖 `service` 或稳定公共层完成任务编排，但不要把业务规则直接堆进定时任务入口层，也不要把定时任务实现默认外拆到 `worker`。
- `utils`、`common`、`global` 不应反向依赖具体业务目录。

## 特别提醒

- `router` 和 `controller` 不一定必须同时存在；如果框架已经把两者合一，不要机械复制两层。
- `utils` 不是垃圾桶。最外层可以有稳定可移植的 `utils`，`internal` 里也可以有项目内适配型 `utils` 子包，`service` 目录下也可以存在局部的 `utils.go` 文件，但每一种都要有清晰边界。
- `global`、`middleware`、`crontask` 是根级入口或根级全局目录；在单二进制 Go 服务里，`internal/global`、`internal/middleware`、`internal/crontask` 视为不合规。
- 不要为了放一个文件就新建一个目录；只有当职责会稳定扩展、边界明确时，才值得单独建目录。
- 如果某段代码已经明显带有业务语义，就应优先落到 `service`、`controller`、`repository` 或其他明确业务目录，而不是继续留在 `utils` 或 `common`。
