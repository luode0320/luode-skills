# Go 包结构样例

## 用途

用于 Go 项目中判断 `main.go`、`internal`、`utils`、`common`、`global`、`middleware`、`crontask` 以及常见业务目录的职责边界。

## 项目根目录规则

### 场景一：前后端在一个根目录的项目

如果前后端代码在同一个根目录下，例如：
- `admin-go/` - 后端 Go 项目
- `admin-vue/` - 前端 Vue 项目

则 Go 包结构规则应用于后端子目录（如 `admin-go/`），即：
- `admin-go/main.go`
- `admin-go/internal/`
- `admin-go/common/`
- `admin-go/global/`
- `admin-go/middleware/`
- `admin-go/crontask/`
- `admin-go/async/`
- `admin-go/utils/`

其中 `utils/`、`common/`、`global/`、`middleware/` 根目录默认只放子目录，具体实现文件放在对应子目录下。

### 场景二：单纯的 Go 项目

如果是单纯的 Go 项目（没有前端代码在同一根目录），则直接在项目根目录下应用本规则，即：
- 项目根目录/main.go
- 项目根目录/internal/
- 项目根目录/common/
- 项目根目录/global/
- 项目根目录/middleware/
- 项目根目录/crontask/
- 项目根目录/async/
- 项目根目录/utils/

其中 `utils/`、`common/`、`global/`、`middleware/` 根目录默认只放子目录，具体实现文件放在对应子目录下。

## 推荐层次

- 项目根目录 `main.go`
  默认把启动入口直接放在项目根目录的 `main.go`。这里只做启动装配、依赖初始化、路由挂载和服务启动，不承载核心业务逻辑。除非项目确实存在多个独立二进制入口，否则不要默认引入 `cmd/`。
- `internal/`
  放项目私有业务代码，是大多数业务目录的主落点。对于单二进制 Go 服务，项目私有代码默认优先放在 `internal/` 下。这里可以包含项目自适应的实现细节，也可以包含只对当前项目成立的 `utils` 子包。
- `internal/router/`
  负责路由注册和入口装配。默认使用 `router`，不要使用 `routes`。
- `internal/controller/`
  负责 HTTP 输入输出、参数转换和响应映射。默认使用 `controller`，不要使用 `handler`。
- `internal/service/`
  负责业务流程、领域规则和跨仓储编排。`internal/service/` 根目录默认先拆业务子目录（如 `internal/service/order/`、`internal/service/user/`），具体实现文件放在子目录中，避免大平层。
- `internal/entity/`
  存放 API 结构体，包括请求结构体、响应结构体、第三方 API 结果结构体等。这里只存放数据结构定义，不包含业务逻辑。
- `internal/<adapter>/`
  放项目私有的协议适配层或基础设施适配层，例如 `internal/chain`、`internal/wss`。这类目录可以存在，不强制要求统一固定名称，但必须表达清晰职责，不能退化成新的杂项目录。
- `utils/`
  放可以稳定复用、可迁移到其他项目的公共包。它是对外复用的稳定公共层，不是 `pkg/` 的替代写法，而是直接表达"稳定可移植工具包"的职责。`utils/` 根目录默认只放子目录，具体实现放 `utils/<name>/*.go`。
- `common/`
  放和当前项目存在依赖关系、但在多个模块之间通用的公共包。它也是工具型或支撑型目录，但不要求可直接迁移到其他项目。`common/` 根目录默认只放子目录，具体实现放 `common/<name>/*.go`。
- `common/model/`
  负责数据库持久化模型、核心数据结构、领域对象。专门处理数据库相关的数据结构定义。
- `common/model/sql/`
  存放 SQL 表结构创建文件、数据库初始化脚本、迁移脚本等 SQL 文件，例如 `xx.sql`、`migrate.sql` 等。
- `common/repository/`
  负责数据库、缓存或外部存储访问。专门处理数据库操作、数据持久化和数据查询。
- `common/msg/`
  存放错误消息、国际化处理等静态数据。需要区分多语言，按语言组织消息内容。
- `common/constant/`
  存放静态硬编码数据，如常量定义、枚举值、固定配置等。
- `global/`
  放已经初始化完成、可能被多个位置直接引用的全局实例或全局引用入口。例如 `global/config`、`global/database`。这里承载的是"全局已装配对象"，不是普通配置读取逻辑或业务服务。`global/` 既不是对外公共复用包，也不是 `internal/` 下的私有变体；项目私有的全局实例入口也必须放在根级 `global/`，不允许使用 `internal/global` 或 `internal/runtimectx`。`global/` 根目录默认只放子目录，具体实现放 `global/<name>/*.go`。
- `middleware/`
  放鉴权、日志、追踪、限流等横切入口逻辑。`middleware` 作为明确的入口层目录单独存在，不放进 `internal/`。在单服务私有项目里，`internal/middleware` 视为不合规。`middleware/` 根目录默认只放子目录，具体实现放 `middleware/<name>/*.go`。
- `crontask/`
  放 cron 定时任务入口、任务注册、调度装配和定时触发逻辑。**专门处理基于 cron 表达式的定时调度任务**，如每分钟执行、每小时执行、每天执行等定时任务。`crontask` 属于最外层次的入口包，和 `common`、`global`、`middleware` 同级，不放进 `internal/`。在单服务私有项目里，`internal/crontask` 视为不合规。
- `async/`
  处理所有 goroutine 异步相关的功能需求，包括异步消费、常驻执行、队列执行、后台任务等。**专门处理通过 goroutine 启动的异步执行逻辑**，不依赖 cron 定时调度。`async` 属于最外层次的入口包，和 `common`、`global`、`middleware`、`crontask` 同级，不放进 `internal/`。

## 常见目录职责

- `internal/router`
  负责路由注册和入口装配。默认使用 `router`，不要使用 `routes`。
- `internal/controller`
  负责 HTTP 输入输出、参数转换和响应映射。默认使用 `controller`，不要使用 `handler`。
- `internal/service`
  负责业务流程、领域规则和跨仓储编排。根目录默认先拆 `internal/service/<domain>/`，再放实现文件，避免把多个业务需求堆在 `internal/service/` 根目录。
- `internal/entity`
  存放 API 结构体，包括请求结构体、响应结构体、第三方 API 结果结构体等。这里只存放数据结构定义，不包含业务逻辑。
- `utils`
  只放稳定、职责清晰、没有明显业务状态的小工具。它不是兜底目录，也不是"暂时不知道放哪"的落点。根目录默认先拆 `utils/<name>/`，再放实现文件。
- `common`
  放项目相关但可在多个模块复用的公共支撑代码，例如和当前项目配置、基础设施、通用协议适配有关的复用逻辑。根目录默认先拆 `common/<name>/`，再放实现文件。
- `common/model`
  负责数据库持久化模型、核心数据结构、领域对象。默认使用 `model`，不要使用 `domain` 作为这层的目录名。专门处理数据库相关的数据结构定义。
- `common/model/sql`
  存放 SQL 表结构创建文件、数据库初始化脚本、迁移脚本等 SQL 文件，例如 `xx.sql`、`migrate.sql` 等。所有数据库相关的 SQL 文件都统一放在这里。
- `common/repository`
  负责数据库、缓存或外部存储访问。专门处理数据库操作、数据持久化和数据查询。
- `common/msg`
  存放错误消息、国际化处理等静态数据。需要区分多语言，按语言组织消息内容。
- `common/constant`
  存放静态硬编码数据，如常量定义、枚举值、固定配置等。
- `global`
  放已经装配完成的共享实例引用，例如配置实例、数据库实例、日志实例、缓存实例等。项目私有的全局实例入口也必须保持根级 `global/`，不要转成 `internal/global` 或 `internal/runtimectx`。根目录默认先拆 `global/<name>/`，再放实现文件。
- `middleware`
  放鉴权、日志、追踪、限流等横切入口逻辑。根目录默认先拆 `middleware/<name>/`，再放实现文件。
- `crontask`
  **专门负责 cron 定时任务**，包括定时任务命名、任务注册、调度入口和任务装配。这里处理的是基于 cron 表达式的定时触发入口，不承载横切中间件职责。任务调度注册和任务实现都放在 `crontask` 包内，不同任务使用任务自己的子包存放。
- `async`
  **专门负责 goroutine 异步执行**，处理所有异步相关的功能需求，包括异步消费、常驻执行、队列执行、后台任务等。这里处理的是通过 goroutine 启动的异步执行逻辑，不依赖 cron 定时调度。异步任务的调度和实现都放在 `async` 包内，不同异步功能使用自己的子包存放。

## 依赖方向

- 默认依赖方向为 `internal/router` -> `internal/controller` -> `internal/service` -> `common/repository`。
- `internal/service` 可以依赖 `common/model` 和 `common/repository` 进行数据操作。
- `common/model` 和 `common/repository` 作为公共数据层，可以被 `internal/service`、`internal/controller` 等业务层依赖。
- 分层推进时优先使用显式依赖注入逐层装配，优先通过构造函数、参数或明确的实例传递表达依赖关系。
- 不建议先做一批全局初始化实例，再让业务层反向回头依赖这些预设对象，避免真实依赖方向被隐藏。
- `middleware` 可以依赖稳定公共层或必要的业务接口，但要避免演变成新的业务承载层。
- `crontask` 可以依赖 `internal/service` 或稳定公共层完成任务编排，但不要把业务规则直接堆进定时任务入口层。
- `async` 可以依赖 `internal/service` 或稳定公共层完成异步任务编排，但不要把业务规则直接堆进异步任务入口层。
- `utils`、`common`、`global` 不应反向依赖具体业务目录。

## 特别提醒

- `internal/router` 和 `internal/controller` 不一定必须同时存在；如果框架已经把两者合一，不要机械复制两层。
- `utils` 不是垃圾桶。最外层可以有稳定可移植的 `utils`，`internal` 里也可以有项目内适配型 `utils` 子包；若服务层需要局部工具，放在对应业务子目录（如 `internal/service/order/utils.go`），不要直接放在 `internal/service/` 根目录。
- `utils`、`common`、`global`、`middleware` 根目录默认只放子目录，不直接放实现文件，避免循环依赖与命名冲突。
- `internal/service` 根目录默认只放业务子目录，不直接堆业务实现文件；规模增长时必须继续按域拆分子目录。
- `global`、`middleware`、`crontask` 是根级入口或根级全局目录；在单二进制 Go 服务里，`internal/global`、`internal/middleware`、`internal/crontask` 视为不合规。
- 不要为了放一个文件就新建一个目录；只有当职责会稳定扩展、边界明确时，才值得单独建目录。
- 如果某段代码已经明显带有业务语义，就应优先落到 `internal/service`、`internal/controller` 或其他明确业务目录，而不是继续留在 `utils` 或 `common`。
- `common/model` 和 `common/repository` 专门处理数据库相关，不应包含业务逻辑，只负责数据结构定义和数据访问操作。
- `router`、`controller`、`service` 作为项目私有业务代码，必须放在 `internal/` 包下，不应暴露在根级目录。
- 所有 SQL 表结构创建文件、数据库初始化脚本、迁移脚本等 SQL 文件（如 `xx.sql`）必须统一存放在 `common/model/sql/` 目录下，不得散落在其他位置。
