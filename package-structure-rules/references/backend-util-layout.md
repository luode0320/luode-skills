# 后端根 utils 与源码根 util 规则

后端根 `utils/` 是可独立复制的技术工具包、SDK 与无业务状态能力唯一根；不得再使用 `infrastructure/`。`utils/` 根只能包含工具包子目录，不得直接存放代码、配置或其他文件；工具包的代码文件必须位于至少一层子目录中。`utils/` 的实现不得依赖项目其他包，只可依赖自身工具包、语言标准库和第三方依赖。

语言源码根的 `util/` 与根 `utils/` 职责不同：它直接存放可依赖项目其他包的高关联工具函数，禁止建立子目录，不承载业务流程。业务域 `business/<domain>/util/` 仍只存放该业务域私有辅助能力。

| 分类 | 二级技术目录 | 职责 |
|---|---|---|
| 时间与并发 | `utils/time/`、`utils/async/`、`utils/convert/`、`utils/http/` | 时间转换、协程与任务辅助、字符串数字转换、通用 HTTP Client |
| 缓存 | `utils/cache/redis/`、`utils/cache/mongo/` | 缓存、Session、锁和临时文档型数据适配 |
| 消息 | `utils/mq/kafka/`、`utils/mq/rabbitmq/`、`utils/mq/rocketmq/`、`utils/mq/nats/` | 消息队列客户端与编解码 |
| 搜索 | `utils/search/elasticsearch/`、`utils/search/opensearch/`、`utils/search/meilisearch/` | 搜索服务客户端与查询适配 |
| 存储 | `utils/storage/oss/`、`utils/storage/file/` | 对象存储与文件系统适配 |
| 远程调用 | `utils/rpc/grpc/`、`utils/rpc/thrift/`、`utils/api/<provider>/` | RPC 与第三方业务 API 客户端 |
| 身份和秘密 | `utils/auth/oauth/`、`utils/auth/oidc/`、`utils/auth/ldap/`、`utils/secret/kms/`、`utils/secret/vault/` | 外部认证和密钥服务接入 |
| 通知和支付 | `utils/notification/*/`、`utils/payment/*/` | 渠道 SDK 与协议转换 |
| 服务发现 | `utils/discovery/polaris/`、`utils/discovery/nacos/` | 腾讯北极星、阿里 Nacos 注册与发现 |
| 协议定义 | `utils/protobuf/` | Protobuf 与 gRPC 定义源 |

禁止 `utils/graphql/`、`utils/asyncapi/`、`utils/avro/`、`utils/api/http/`。通用 HTTP 只能位于 `utils/http/`。后端项目根不得再建立旧的 `util/` 工具包目录。
