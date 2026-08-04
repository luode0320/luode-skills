# 后端根 utils 与 common/util 规则

后端根 `utils/` 是可独立复制的技术工具包、SDK 与无业务状态能力唯一根；不得再使用 `infrastructure/`。`utils/` 根只能包含工具包子目录，不得直接存放代码、配置或其他文件；工具包的代码文件必须位于至少一层子目录中。`utils/` 的实现不得依赖项目其他包，只可依赖自身工具包、语言标准库和第三方依赖。

`common/util/` 与根 `utils/` 职责不同：它直接存放可依赖项目其他包的高关联工具函数，禁止建立子目录，不承载业务流程。业务域 `business/<domain>/util/` 仍只存放该业务域私有辅助能力；源码根 `util/` 不再建立。

项目无关、可独立复制的工具包或 SDK 进入根 `utils/<package>/`；需要引用项目配置、公共结构或其他项目包的工具函数进入 `common/util/<function>.<ext>`。

| 分类 | 二级技术目录 | 职责 |
|---|---|---|
| 时间与并发 | `utils/time/`、`utils/async/`、`utils/convert/`、`utils/http/` | 时间转换、协程与任务辅助、字符串数字转换、通用 HTTP Client |
| IP 与地址归属 | `utils/ip/` | 请求 IP 提取、规范化、公私网判断，以及离线库或第三方 GeoIP 的国家/地区归属查询适配；不承载代理信任策略、风控或业务黑白名单。 |
| 定时调度 | `utils/cron/` | Cron 调度库技术封装（如 robfig/cron），供业务侧 `crontask/` 定时任务入口调用 |
| 序列化 | `utils/json/` | JSON 序列化与反序列化技术工具封装 |
| 日志 | `utils/log/` | 统一日志框架封装（如 zap/logrus），提供项目唯一日志调用入口 |
| 缓存 | `utils/cache/redis/`、`utils/cache/mongo/` | 缓存、Session、锁和临时文档型数据适配 |
| 消息 | `utils/mq/kafka/`、`utils/mq/rabbitmq/`、`utils/mq/rocketmq/`、`utils/mq/nats/` | 消息队列客户端与编解码 |
| 搜索 | `utils/search/elasticsearch/`、`utils/search/opensearch/`、`utils/search/meilisearch/` | 搜索服务客户端与查询适配 |
| 存储 | `utils/storage/oss/`、`utils/storage/file/` | 对象存储与文件系统适配 |
| 远程调用 | `utils/rpc/grpc/`、`utils/rpc/thrift/`、`utils/api/<provider>/` | RPC 与第三方业务 API 客户端 |
| 身份和秘密 | `utils/auth/oauth/`、`utils/auth/oidc/`、`utils/auth/ldap/`、`utils/secret/kms/`、`utils/secret/vault/` | 外部认证和密钥服务接入 |
| 通知和支付 | `utils/notification/*/`、`utils/payment/*/` | 渠道 SDK 与协议转换 |
| 服务发现 | `utils/discovery/polaris/`、`utils/discovery/nacos/` | 腾讯北极星、阿里 Nacos 注册与发现 |
| 协议定义 | `utils/protobuf/` | Protobuf 与 gRPC 定义源 |

禁止 `utils/graphql/`、`utils/asyncapi/`、`utils/avro/`、`utils/api/http/`。通用 HTTP 只能位于 `utils/http/`。后端项目根和语言源码根均不得再建立旧的 `util/` 工具包目录；旧项目只能通过 adoption 的 legacy 快照渐进迁移。

Go 项目中，以下目录内部 `package` 声明使用带 `Util` 后缀的别名，目录路径本身不变：`utils/time`→`timeUtil`、`utils/json`→`jsonUtil`、`utils/log`→`logUtil`、`utils/http`→`httpUtil`（这四个是为了避免与同名标准库包冲突）；`utils/cron`→`cronUtil`（`cron` 本身不与标准库冲突，只是为了和其余工具包保持统一的 `xxxUtil` 命名风格）。其余目录 package 名与目录名一致。详见 `code-style-consistency-rules/references/go-coding-rules.md`。
