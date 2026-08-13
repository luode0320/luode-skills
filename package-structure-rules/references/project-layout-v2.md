# 代码位置目录规则 V2：三类项目完整目录树

目录标记：`[必需·提交]`、`[条件·提交]`、`[生成·忽略]`、`[运行·忽略]`。条件目录仅在项目真实启用对应能力时创建。

## 统一规范目录与扩展目录

1. **规范目录的含义**：目录树列出的目录名称、职责与落点是统一规范。凡命中这些语义的代码必须落到对应规范目录，不得新建同义别名目录（如 `svc/`、`ctrl/`、`handler/`、`biz/`、`dao/`）绕开规范。
2. **目录树是规范集合，不是白名单穷举**：`<source-root>/`、`business/<domain>/`、后端项目根、前端 `src/`、`src/modules/<domain>/` 允许存在规范外目录；存量规范外目录不判违规，也不强制迁移。
3. **新增规范外目录的确认闸门（强制）**：agent 新增任何不属于目录树规范的目录前，必须先向用户说明目录名、职责、为什么无法落到规范目录，并取得**当前轮显式同意**；未取得同意时只能落到规范目录或停下来询问，不得以"看起来更合理""顺手建一个"为由自行创建。
4. **扩展目录准入四条**（同意后仍须全部满足）：
   - 不落在 `forbidden_paths`（根 `data/`、`schema/`、`protocol/`、源码根 `util/`、`infrastructure/` 等）；
   - 不位于 `allowed_children` 已声明父目录下（`config/`、`database/model/`、`database/sql/`、`common/`、`scripts/`、`deploy/`、`integration/`、`utils/discovery/` 的子目录集合仍封闭）；
   - 不与任何规范目录职责重复，也不是规范目录的同义别名；
   - 创建后按 `architecture-doc-rules` 更新 `doc/1-架构/2-目录树.md`。
5. **扩展目录不获得引用特权**：跨业务域导入仍只允许目标域 `rpc/`；业务域内除 `rpc/` 外的**任何**目录（含扩展目录）都是私有层。
6. **Catalog 边界**：`placement_catalog.py query` 只对规范目录返回唯一位置；扩展目录不进入 Catalog、不由 `init` 创建、`check` 也不为其背书。

## 旧项目渐进采纳

本目录树是新项目和新独立逻辑的 V2 目标结构；旧项目通过 `doc/1-架构/3-目录规则收敛清单.yaml` 逐步采纳，不自动迁移用户目录或文件。

- `adopted_paths` 只登记可由 V2 Catalog 唯一匹配的相对路径。登记后可按该 Catalog 路径的允许子目录和内容类型扩展，不得以名称相似为由扩展到其他位置。
- `legacy_source_roots` 记录采纳时已存在的遗留源码根、目录和文件快照。此类目录只允许维护现有源码，禁止新增源码文件、源码目录或独立模块。
- 遗留目录与 V2 目录相似但未被唯一匹配时，必须人工登记为 `legacy_source_roots` 才能沿用；未登记的新增业务或独立新逻辑必须按 V2 Catalog 落位。
- `strict` 与 `legacy` 保持既有检查语义；`adoption` 策略读取收敛清单执行渐进检查。`check`、`init`、`render` 仅消费规则或清单，绝不创建、改写或补全清单。

## 前后端在同一个项目

```text
<fullstack-workspace>/
├── .github/                              # [条件·提交] GitHub 自动化
│   ├── workflows/                         # [条件·提交] 聚合工作流
│   ├── actions/                           # [条件·提交] 复合 Action
│   ├── ISSUE_TEMPLATE/                    # [条件·提交] Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md           # [条件·提交] PR 模板
├── .gitlab/                               # [条件·提交] GitLab 流水线配置
│   └── ci/                                # [条件·提交] 流水线片段
├── .devcontainer/                         # [条件·提交] 开发容器
├── .vscode/                               # [必需·提交] VSCodex 启动和任务配置
│   ├── launch.json                        # [必需·提交] 联合调试配置
│   ├── tasks.json                         # [必需·提交] dev、build、docker-build 任务

│   ├── settings.json                      # [条件·提交] 团队设置
│   └── extensions.json                    # [条件·提交] 推荐扩展
├── backend/                               # [必需·提交] 完整独立后端项目
│   ├── main.<ext>                          # [条件·提交] 同仓后端默认二进制入口
│   ├── cmd/                                # [条件·提交] 同仓后端额外二进制入口
│   │   └── <binary>/                       # [条件·提交] 单个额外二进制目录
│   │       └── main.<ext>                  # [条件·提交] 同仓后端额外入口
│   └── config/                              # [必需·提交] 同仓后端唯一配置根
│       ├── load.<ext>                        # [条件·提交] 配置加载与解析入口；环境识别支持 -env、APP_ENV、ENV，优先级 -env > APP_ENV > ENV > local
│       ├── model.<ext>                       # [条件·提交] 配置结构定义
│       ├── yaml/                            # [条件·提交] 按环境拆分的外部 YAML；与 embedded/ 互斥二选一；只存放配置数据
│       └── embedded/                        # [条件·提交] 源码内 YAML 字符串；与 yaml/ 互斥二选一，推荐优先使用；允许源码私密配置，默认不依赖环境变量
├── frontend/                              # [必需·提交] 完整独立前端项目
├── test/                                   # [必需·提交] 唯一活动测试代码根，按被测源码目录镜像
├── integration/                           # [条件·提交] 仅限前后端联调资产
│   ├── contracts/                         # [条件·提交] 联调契约根
│   │   ├── http/                          # [条件·提交] HTTP 契约
│   │   ├── event/                         # [条件·提交] 事件契约
│   │   └── rpc/                           # [条件·提交] RPC 契约
│   └── compose/                           # [条件·提交] 联调 Compose
├── doc/                                   # [必需·提交] 工作区研发产物根
│   ├── 1-架构/                            # [必需·提交] 架构与目录树
│   ├── 2-需求/                            # [必需·提交] 需求产物
│   ├── 3-实施/                            # [必需·提交] 实施产物
│   ├── 4-bugs/                            # [必需·提交] Bug 产物
│   ├── 5-tests/                           # [必需·提交] 测试研发产物入口
│   ├── 6-review/                          # [必需·提交] 测试后的风格回归记录
│   └── data/                              # [条件·提交] Markdown 数据资产
│       └── images/                        # [条件·提交] 文档图片与截图
├── build.sh                               # [必需·提交] 聚合打包入口
├── docker-build.sh                        # [必需·提交] 聚合镜像构建入口
├── go.work                                # [条件·提交] Go 工作区成员声明
├── pnpm-workspace.yaml                    # [条件·提交] Node 工作区成员声明
├── package.json                           # [条件·提交] 聚合命令
├── .gitlab-ci.yml                         # [条件·提交] GitLab 主入口
├── .editorconfig                          # [必需·提交] UTF-8 与格式规则
├── .gitattributes                         # [必需·提交] 文本与换行规则
├── .gitignore                             # [必需·提交] 忽略规则
├── .dockerignore                          # [条件·提交] 镜像排除规则
├── Dockerfile                              # [必需·提交] 工作区统一镜像定义
├── AGENTS.md                              # [必需·提交] 工作区协作规则
├── CLAUDE.md                              # [必需·提交] Claude Code 工作区协作规则；正文与 AGENTS.md 一致
├── PROJECT_CURRENT.md                     # [必需·提交] 当前状态
├── PROJECT_MEMORY.md                      # [必需·提交] 稳定决策
├── PROJECT_HISTORY.md                     # [必需·提交] 重要历史
├── PROJECT_STYLE.md                       # [条件·提交] 长期风格
└── README.md                              # [必需·提交] 工作区入口
```

工作区根 `test/` 是唯一活动测试代码目录，按被测源码目录镜像；`doc/5-tests/` 仅保存说明与证据，历史可执行资产只读保留。

同仓后端的二进制入口只放在 `backend/`：默认入口为 `backend/main.<ext>`，额外入口为 `backend/cmd/<binary>/main.<ext>`；工作区根不放 `main.<ext>`，也不建立根 `cmd/` 作为后端入口。

工作区根禁止业务 `config/`、`data/`、`database/`、`swag/`、`schema/`、`resources/`、`scripts/`、`util/`、`utils/`、`common/`、`deploy/`。不建立 `integration/virtualization/`、`integration/doc/`、`integration/tests/`、`integration/scripts/`、`integration/fixtures/`。工作区根的 `AGENTS.md` 与 `CLAUDE.md` 必须同时提交且正文完全一致。

## 后端独立项目

```text
<backend-project>/
├── .github/                                 # [条件·提交] GitHub 自动化
│   ├── workflows/                           # [条件·提交] 后端检查、构建与发布工作流
│   ├── actions/                             # [条件·提交] 工作流复用的复合 Action
│   ├── ISSUE_TEMPLATE/                      # [条件·提交] Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md             # [条件·提交] Pull Request 模板
├── .gitlab/                                 # [条件·提交] GitLab 流水线片段
│   └── ci/                                  # [条件·提交] 后端流水线引用的片段
├── .devcontainer/                           # [条件·提交] 开发容器
├── .vscode/                                 # [必需·提交] 启动、调试和任务配置
│   ├── launch.json                          # [必需·提交] 本地调试配置
│   ├── tasks.json                           # [必需·提交] 本地任务配置

│   ├── settings.json                        # [条件·提交] 团队设置
│   └── extensions.json                      # [条件·提交] 推荐扩展
├── main.<ext>                               # [条件·提交] 独立后端默认二进制入口
├── cmd/                                     # [条件·提交] 仅用于额外二进制入口
│   └── <binary>/                            # [条件·提交] 单个额外二进制目录
│       └── main.<ext>                       # [条件·提交] 额外二进制入口
├── config/                                  # [必需·提交] 唯一配置根
│   ├── load.<ext>                            # [条件·提交] 配置加载与解析入口；环境识别支持 -env、APP_ENV、ENV，优先级 -env > APP_ENV > ENV > local
│   ├── model.<ext>                           # [条件·提交] 配置结构定义
│   ├── yaml/                                # [必需·提交] 按环境拆分的外部 YAML；允许有意持久化凭据原值；只存放配置数据
│   │   └── config_<env>.yaml                 # [条件·提交] 兼容 `.yml`；标准环境为 local、test、prod
│   └── embedded/                            # [条件·提交] 按环境拆分的源码内 YAML 字符串；与 yaml/ 互斥二选一，推荐优先使用；允许源码私密配置，默认不依赖环境变量；只存放配置数据
│       └── config_<env>_yaml.<ext>           # [条件·提交] Go 使用 config_<env>_yaml.go；格式名后置规避 Go 测试文件命名；允许源码私密配置，源码优先且默认不依赖环境变量
├── test/                                     # [必需·提交] 唯一活动测试代码根，按源码目录镜像
├── database/                                # [条件·提交] 数据存储代码和资产唯一根
│   ├── connection/                          # [条件·提交] 关系型数据库、Redis、Mongo 等数据存储服务的连接、连接池与客户端初始化
│   ├── model/                               # [条件·提交] 数据存储模型分类根；根目录禁止直接文件
│   │   ├── db/                              # [条件·提交] 关系型数据库表映射、ORM 与持久化模型
│   │   ├── redis/                           # [条件·提交] Redis Key、Hash、缓存值等数据模型
│   │   └── mongo/                           # [条件·提交] Mongo 集合与文档模型
│   ├── repository/                          # [条件·提交] 仅数据库访问
│   ├── mapper/                              # [条件·提交] 持久化与领域转换
│   ├── transaction/                         # [条件·提交] 事务上下文
│   ├── generated/                           # [生成·忽略] 数据库生成代码
│   ├── migration/                           # [条件·提交] 自动迁移生产源码
│   │   ├── field/                           # [条件·提交] 字段迁移
│   │   │   ├── create/                      # [条件·提交] 创建字段
│   │   │   ├── read/                        # [条件·提交] 读取字段结构
│   │   │   ├── update/                      # [条件·提交] 更新字段结构
│   │   │   └── delete/                      # [条件·提交] 受控删除字段
│   │   └── index/                           # [条件·提交] 索引迁移
│   │       ├── create/                      # [条件·提交] 创建索引
│   │       ├── read/                        # [条件·提交] 读取索引结构
│   │       ├── update/                      # [条件·提交] 更新索引
│   │       └── delete/                      # [条件·提交] 受控删除索引
│   └── sql/                                 # [条件·提交] 独立 SQL 文件根；禁止生产源码与直接文件
│       ├── ddl/                             # [条件·提交] 直接存放建表、改表与约束 `.sql` 文件
│       ├── index/                           # [条件·提交] 直接存放索引 `.sql` 文件
│       └── field/                           # [条件·提交] 字段变更 SQL 分类根；禁止直接文件
│           ├── create/                      # [条件·提交] 直接存放新增字段 `.sql` 文件
│           ├── update/                      # [条件·提交] 直接存放修改字段 `.sql` 文件
│           └── delete/                      # [条件·提交] 直接存放删除字段 `.sql` 文件
├── swag/                                    # [条件·提交] Swag 正式输出；内部规则由专属 Owner 管理
├── resources/                               # [条件·提交] 运行时只读资源
│   ├── templates/                           # [条件·提交] 模板
│   ├── i18n/                                # [条件·提交] 国际化资源
│   ├── static/                              # [条件·提交] 后端静态文件
│   └── certificates/                        # [条件·提交] 公开证书与 CA
├── utils/                                   # [条件·提交] 可独立复制的技术工具包与 SDK 根；根目录只允许工具包子目录，禁止直接存放文件或依赖项目其他包
│   ├── time/                                # [条件·提交] 时间与时区转换
│   ├── cron/                                # [条件·提交] Cron 调度库技术封装（如 robfig/cron），供业务侧 crontask/ 定时任务入口调用
│   ├── async/                               # [条件·提交] 异步协程与并发辅助
│   ├── convert/                             # [条件·提交] 字符串与数字双向转换
│   ├── decimal/                             # [条件·提交] Decimal 高精度数值类型封装，数据库扫描与金额运算
│   ├── http/                                # [条件·提交] 通用 HTTP Client
│   ├── ip/                                  # [条件·提交] 请求 IP 提取、标准化、公私网判断与地址归属查询工具
│   ├── json/                                # [条件·提交] JSON 序列化与反序列化技术工具封装
│   ├── log/                                 # [条件·提交] 统一日志框架封装
│   ├── cache/                               # [条件·提交] 缓存适配
│   │   ├── redis/                           # [条件·提交] Redis
│   │   └── mongo/                           # [条件·提交] Mongo 缓存
│   ├── mq/                                  # [条件·提交] 消息队列适配
│   │   ├── kafka/                           # [条件·提交] Kafka
│   │   ├── rabbitmq/                        # [条件·提交] RabbitMQ
│   │   ├── rocketmq/                        # [条件·提交] RocketMQ
│   │   └── nats/                            # [条件·提交] NATS
│   ├── search/                              # [条件·提交] 搜索服务适配
│   │   ├── elasticsearch/                   # [条件·提交] Elasticsearch
│   │   ├── opensearch/                      # [条件·提交] OpenSearch
│   │   └── meilisearch/                     # [条件·提交] Meilisearch
│   ├── storage/                             # [条件·提交] 存储适配
│   │   ├── oss/                             # [条件·提交] 对象存储
│   │   └── file/                            # [条件·提交] 文件系统
│   ├── rpc/                                 # [条件·提交] RPC 适配
│   │   ├── grpc/                            # [条件·提交] gRPC
│   │   └── thrift/                          # [条件·提交] Thrift
│   ├── api/                                 # [条件·提交] 第三方业务 API
│   │   ├── binance/                         # [条件·提交] Binance
│   │   └── wechat/                          # [条件·提交] 微信非支付 API
│   ├── auth/                                # [条件·提交] 外部认证
│   │   ├── oauth/                           # [条件·提交] OAuth
│   │   ├── oidc/                            # [条件·提交] OIDC
│   │   └── ldap/                            # [条件·提交] LDAP
│   ├── secret/                              # [条件·提交] 外部密钥服务
│   │   ├── kms/                             # [条件·提交] KMS
│   │   └── vault/                           # [条件·提交] Vault
│   ├── notification/                        # [条件·提交] 通知通道
│   │   ├── email/                           # [条件·提交] 邮件
│   │   ├── sms/                             # [条件·提交] 短信
│   │   ├── telegram/                        # [条件·提交] Telegram
│   │   └── webhook/                         # [条件·提交] Webhook
│   ├── payment/                             # [条件·提交] 支付通道
│   │   ├── alipay/                          # [条件·提交] 支付宝
│   │   ├── wechatpay/                       # [条件·提交] 微信支付
│   │   └── stripe/                          # [条件·提交] Stripe
│   ├── discovery/                           # [条件·提交] 服务发现和注册
│   │   ├── polaris/                         # [条件·提交] 腾讯北极星
│   │   └── nacos/                           # [条件·提交] 阿里 Nacos
│   └── protobuf/                            # [条件·提交] Protobuf 和 gRPC 定义源
├── common/                                  # [条件·提交] 跨模块公共结构
│   ├── request/                             # [条件·提交] 请求 DTO
│   ├── response/                            # [条件·提交] 响应 DTO
│   ├── constant/                            # [条件·提交] 稳定常量和枚举
│   ├── error/                               # [条件·提交] 错误类型与错误码
│   ├── validation/                          # [条件·提交] 通用校验
│   ├── dto/                                 # [条件·提交] 跨域共享领域模型与数据传输对象
│   ├── page/                                # [条件·提交] 分页请求与响应协议
│   ├── msg/                                 # [条件·提交] 国际化消息码与消息渲染源码；文案数据在 resources/i18n/
│   └── util/                                # [条件·提交] 可依赖项目其他包的高关联工具函数；代码文件直接放此目录，禁止子目录
├── global/                                  # [条件·提交] 已装配共享引用
│   └── <capability>/                        # [条件·提交] 单项共享引用
├── crontask/                                # [条件·提交] Cron 入口
│   └── <task>/                              # [条件·提交] 单个任务入口
├── async/                                   # [条件·提交] Worker 与消费者入口
│   └── <worker>/                            # [条件·提交] 单个 Worker 入口
├── middleware/                              # [条件·提交] 横切中间件
│   ├── authentication/                      # [条件·提交] 身份认证
│   ├── authorization/                       # [条件·提交] 授权
│   ├── logging/                             # [条件·提交] 请求日志
│   ├── trace/                               # [条件·提交] Trace 传播
│   ├── request-id/                          # [条件·提交] 请求标识
│   ├── rate-limit/                          # [条件·提交] 限流
│   ├── recovery/                            # [条件·提交] 异常恢复
│   ├── cors/                                # [条件·提交] 跨域控制
│   ├── idempotency/                         # [条件·提交] 幂等控制
│   ├── timeout/                             # [条件·提交] 超时控制
│   ├── compression/                         # [条件·提交] 压缩
│   └── security-headers/                    # [条件·提交] 安全响应头
├── <source-root>/                           # [必需·提交] 当前语言唯一源码根
│   ├── router/                              # [条件·提交] 路由装配
│   ├── controller/                          # [条件·提交] 输入与响应映射
│   └── business/                            # [必需·提交] 业务域根
│       └── <domain>/                        # [必需·提交] 单业务域
│           ├── api/                         # [条件·提交] 域内 API 调用
│           ├── service/                     # [必需·提交] 业务流程
│           ├── entity/                      # [条件·提交] 领域实体
│           ├── base/                        # [条件·提交] 业务基础结构
│           ├── constant/                    # [条件·提交] 域常量
│           ├── init/                        # [条件·提交] 域初始化
│           ├── crontask/                    # [条件·提交] 域定时任务实现
│           ├── util/                        # [条件·提交] 域私有辅助；不属于根 utils/ 或 common/util/
│           └── rpc/                         # [条件·提交] 对其他微业务公开的 JSON 字符串通信函数；代码文件直接落盘，禁止子目录
├── scripts/                                 # [条件·提交] 工程脚本
│   ├── dev/                                 # [条件·提交] 本地开发脚本
│   └── build/                               # [条件·提交] 构建脚本
├── tools/                                   # [条件·提交] 独立开发工具
│   └── <tool>/                              # [条件·提交] 单工具目录
├── deploy/                                  # [条件·提交] 部署资产
│   ├── docker/                              # [条件·提交] Docker 资产
│   ├── compose/                             # [条件·提交] Compose 资产
│   ├── kubernetes/                          # [条件·提交] Kubernetes Manifest
│   └── proxy/                               # [条件·提交] 代理配置
├── doc/                                     # [必需·提交] 研发产物根
│   ├── 1-架构/                              # [必需·提交] 后端架构、边界与真实目录树
│   ├── 2-需求/                              # [必需·提交] 后端需求产物
│   ├── 3-实施/                              # [必需·提交] 后端实施总览、周期与最小任务
│   ├── 4-bugs/                              # [必需·提交] 后端 Bug 与诊断产物
│   ├── 5-tests/                             # [必需·提交] 测试规则与研发产物入口
│   ├── 6-review/                            # [必需·提交] 测试后的风格回归记录
│   └── data/                                # [条件·提交] Markdown 引用的数据资产
│       └── images/                          # [条件·提交] 文档图片与截图
├── var/                                     # [运行·忽略] 运行期可变数据
│   ├── tmp/                                 # [运行·忽略] 临时文件
│   ├── cache/                               # [运行·忽略] 本地缓存
│   ├── logs/                                # [运行·忽略] 本地日志
│   ├── uploads/                             # [运行·忽略] 本地上传
│   └── run/                                 # [运行·忽略] PID 和 Socket
├── bin/                                     # [生成·忽略] 二进制输出
├── build/                                   # [生成·忽略] 构建输出
├── target/                                  # [生成·忽略] Java 构建输出
├── .cache/                                  # [生成·忽略] 工具缓存
├── build.sh                                 # [必需·提交] 统一打包入口
├── docker-build.sh                          # [必需·提交] 镜像构建入口
├── Dockerfile                                # [必需·提交] 后端镜像定义
├── AGENTS.md                                # [必需·提交] 后端项目协作规则
├── CLAUDE.md                                # [必需·提交] Claude Code 后端项目协作规则；正文与 AGENTS.md 一致
├── PROJECT_CURRENT.md                       # [必需·提交] 当前任务、范围、状态与交接
├── PROJECT_MEMORY.md                        # [必需·提交] 稳定决策与长期事实
├── PROJECT_HISTORY.md                       # [必需·提交] 重要历史事件
├── PROJECT_STYLE.md                         # [条件·提交] 后端长期代码风格
└── README.md                                # [必需·提交] 项目入口
```

源码根只选择一个：Go 为 `internal/`；Java 为 `src/main/java/<base-package>/`；Node.js 为 `src/`；Python 为 `src/<package>/`。
后端根治理文件必须直接位于项目根，不得放入 `<source-root>/`、`doc/` 或业务域；`AGENTS.md` 与 `CLAUDE.md` 同时存在并保持完全相同正文，目录规则只初始化文件位置，正文分别由 `project-rule-file-bootstrap-rules`、`project-memory-rules` 和 `project-style-rules` 维护。
`main.<ext>` 和 `cmd/<binary>/main.<ext>` 是人工创建的入口 pattern，不由 `init` 创建；`cmd/main.<ext>` 不满足 `<binary>` 目录层级。

独立后端配置使用 `config/embedded/` 或 `config/yaml/`（两者互斥，只能二选一，推荐优先使用 `config/embedded/`），按 `config_<env>` 拆分环境。`embedded/` 模式：Go 使用 `config_prod_yaml.go`、`config_test_yaml.go`、`config_local_yaml.go`，格式名必须后置因为 `config_test.go` 会被 Go 当成测试文件。`yaml/` 模式：外部 YAML 使用 `config_prod.yaml`、`config_test.yaml`、`config_local.yaml`，不参与编译因此不加 `_yaml` 后缀。`local`、`test`、`prod` 是标准环境名，环境名可按 `[a-z][a-z0-9_]*` 扩展但不得以 `_yaml` 结尾；只检查已有文件，不要求三种环境齐全。外部 YAML 与 embedded 源码均允许有意持久化 API key、密钥、密码等私密信息，但不得向 Agent 输出、日志、README、错误或测试报告泄露，详细安全边界和合法/非法示例见 `configuration-layout.md`。`config/yaml/` 与 `config/embedded/` 只存放配置数据，且严格互斥不可并存；`test/` 目录不承载配置数据源，测试所需的运行时配置数据统一使用 `config/` 下的 `test` 环境。`test/config/` 允许作为测试配置加载/解析逻辑的目录，这不属于配置数据源，而是测试代码的一部分。配置加载与结构定义由 `config/` 根下的 `load.<ext>`（配置加载与解析入口）与 `model.<ext>`（配置结构定义）两个源码文件承担；`load.<ext>` 环境识别支持 `-env`、`APP_ENV`、`ENV`，优先级 `-env > APP_ENV > ENV > local`。

前后端同仓时，以上配置目录整体下移到 `backend/config/`，工作区根不建立后端 `config/`；后端主入口为 `backend/main.<ext>`，额外入口为 `backend/cmd/<binary>/main.<ext>`。独立后端主入口为根 `main.<ext>`，`cmd/` 只允许出现 `cmd/<binary>/main.<ext>`；`cmd/main.<ext>`、同仓工作区根 `main.<ext>` 和工作区根 `cmd/` 均非法。

三类项目的活动测试程序、fixture、helper 和测试启动脚本统一放在项目根 `test/`，按被测源码目录镜像；`doc/5-tests/` 只保存说明与证据。前后端同仓不建立 `backend/test/` 或 `frontend/test/`，独立后端也不建立 `backend/test/`。

`<source-root>/`、`business/<domain>/` 和后端项目根未在目录树中列出的其他目录按「统一规范目录与扩展目录」规则处理（见上节）。

## 前端独立项目

```text
<frontend-project>/
├── .github/                                 # [条件·提交] GitHub 自动化
│   ├── workflows/                           # [条件·提交] 前端检查、构建与发布工作流
│   ├── actions/                             # [条件·提交] 工作流复用的复合 Action
│   ├── ISSUE_TEMPLATE/                      # [条件·提交] Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md             # [条件·提交] Pull Request 模板
├── .gitlab/                                 # [条件·提交] GitLab 流水线片段
│   └── ci/                                  # [条件·提交] 前端流水线引用的片段
├── .devcontainer/                           # [条件·提交] 开发容器
├── .vscode/                                 # [必需·提交] 启动、调试和任务配置
│   ├── launch.json                          # [必需·提交] 浏览器与开发服务器调试配置
│   ├── tasks.json                           # [必需·提交] 本地启动、构建与镜像任务
│   ├── settings.json                        # [条件·提交] 团队共享编辑器设置
│   └── extensions.json                      # [条件·提交] 前端框架与格式化扩展
├── config/                                  # [必需·提交] 唯一配置根
│   ├── yaml/                                # [条件·提交] 外部 YAML；与 embedded/ 互斥二选一
│   └── embedded/                            # [条件·提交] 源码内 YAML 字符串；与 yaml/ 互斥二选一，推荐优先使用
├── test/                                     # [必需·提交] 唯一活动测试代码根，按源码目录镜像
├── public/                                  # [必需·提交] 原样复制并按 URL 访问的公开文件
├── src/                                     # [必需·提交] 生产源码根
│   ├── app/                                 # [必需·提交] 启动和根装配
│   ├── router/                              # [条件·提交] 路由
│   ├── layouts/                             # [条件·提交] 跨页面布局
│   ├── modules/                             # [必需·提交] 业务域根
│   │   └── <domain>/                        # [必需·提交] 单业务域
│   │       ├── pages/                       # [条件·提交] 页面；与 views 互斥
│   │       ├── components/                  # [条件·提交] 域私有组件
│   │       ├── api/                         # [条件·提交] 域接口调用
│   │       ├── model/                       # [条件·提交] 域模型
│   │       ├── store/                       # [条件·提交] 域状态
│   │       ├── hooks/                       # [条件·提交] React Hook
│   │       ├── composables/                 # [条件·提交] Vue 组合式能力
│   │       ├── service/                     # [条件·提交] 域业务编排
│   │       ├── validation/                  # [条件·提交] 域校验
│   │       ├── data/                        # [条件·提交] 源码静态数据
│   │       └── styles/                      # [条件·提交] 域样式
│   ├── components/                           # [条件·提交] 跨域组件
│   ├── api/                                  # [必需·提交] 项目 API Client
│   ├── common/                               # [条件·提交] 项目级公共结构与公共能力
│   │   ├── request/                          # [条件·提交] 项目级请求结构
│   │   ├── response/                         # [条件·提交] 响应与分页结构
│   │   ├── event/                            # [条件·提交] 项目级事件结构
│   │   ├── command/                          # [条件·提交] 项目级写操作命令
│   │   ├── query/                            # [条件·提交] 项目级查询条件与结果
│   │   ├── constant/                         # [条件·提交] 跨域稳定常量与枚举
│   │   ├── error/                            # [条件·提交] 前端错误类型与映射
│   │   ├── validation/                       # [条件·提交] 跨域通用校验
│   │   ├── msg/                              # [条件·提交] 国际化消息码与消息渲染源码；词条数据在 src/locales/
│   │   └── util/                             # [条件·提交] 依赖前端项目约定的辅助能力
│   ├── util/                                 # [条件·提交] 项目无关的无业务状态工具
│   │   └── <capability>/                     # [条件·提交] 单项前端技术能力
│   ├── store/                                # [条件·提交] 全局状态
│   ├── hooks/                                # [条件·提交] React 项目级 Hook
│   ├── composables/                          # [条件·提交] Vue 项目级组合式能力
│   ├── directives/                           # [条件·提交] 自定义指令
│   ├── plugins/                              # [条件·提交] 插件装配
│   ├── services/                             # [条件·提交] 跨域协调服务
│   ├── middleware/                           # [条件·提交] 前端横切能力
│   │   ├── authentication/                   # [条件·提交] 登录态恢复与认证入口
│   │   ├── authorization/                    # [条件·提交] 路由、菜单与操作权限
│   │   ├── route/                            # [条件·提交] 导航守卫
│   │   ├── http/                             # [条件·提交] 请求与响应拦截链
│   │   ├── logging/                          # [条件·提交] 前端访问与异常日志
│   │   ├── trace/                            # [条件·提交] Trace 与关联标识
│   │   └── error/                            # [条件·提交] 全局异常捕获与用户反馈
│   ├── styles/                               # [必需·提交] 项目级样式
│   │   ├── tokens/                           # [条件·提交] 设计令牌
│   │   ├── themes/                           # [条件·提交] 主题定义
│   │   └── global/                           # [必需·提交] Reset 与全局样式
│   ├── assets/                               # [必需·提交] 需打包或 import 的资源
│   │   ├── images/                           # [条件·提交] 打包图片
│   │   ├── icons/                            # [条件·提交] 图标与 SVG
│   │   └── fonts/                            # [条件·提交] 字体与许可证
│   ├── locales/                              # [条件·提交] 国际化词条
│   ├── workers/                              # [条件·提交] Web Worker
│   ├── pwa/                                  # [条件·提交] PWA
│   └── generated/                            # [生成·忽略] 生成代码
│       └── api/                              # [生成·忽略] OpenAPI 生成客户端
├── scripts/                                  # [条件·提交] 工程脚本
│   ├── dev/                                  # [条件·提交] 本地开发脚本
│   └── build/                                # [条件·提交] 构建脚本
├── tools/                                    # [条件·提交] 独立开发工具
│   └── <tool>/                               # [条件·提交] 单个独立开发工具
├── deploy/                                   # [条件·提交] 部署资产
│   ├── docker/                               # [条件·提交] Docker
│   ├── compose/                              # [条件·提交] Compose
│   ├── kubernetes/                           # [条件·提交] Kubernetes
│   └── proxy/                                # [条件·提交] 代理配置
├── .storybook/                               # [条件·提交] Storybook
├── doc/                                      # [必需·提交] 研发产物根
│   ├── 1-架构/                               # [必需·提交] 前端架构、边界与真实目录树
│   ├── 2-需求/                               # [必需·提交] 前端需求产物
│   ├── 3-实施/                               # [必需·提交] 前端实施总览、周期与最小任务
│   ├── 4-bugs/                               # [必需·提交] 前端 Bug 与诊断产物
│   ├── 5-tests/                              # [必需·提交] 测试规则与研发产物入口
│   ├── 6-review/                             # [必需·提交] 测试后的风格回归记录
│   └── data/                                 # [条件·提交] Markdown 引用的数据资产
│       └── images/                           # [条件·提交] 文档图片与截图
├── dist/                                     # [生成·忽略] 生产构建输出
├── build/                                    # [生成·忽略] 构建输出
├── out/                                      # [生成·忽略] 静态导出
├── .cache/                                   # [生成·忽略] 工具缓存
├── build.sh                                  # [必需·提交] 前端统一打包入口
├── docker-build.sh                           # [条件·提交] 前端 Docker 镜像构建入口
├── Dockerfile                                # [必需·提交] 前端镜像定义
├── package.json                              # [必需·提交] 前端依赖与脚本入口
├── .gitlab-ci.yml                            # [条件·提交] GitLab 流水线主入口
├── .editorconfig                             # [必需·提交] UTF-8 与基础格式规则
├── .gitattributes                            # [必需·提交] 文本、二进制与 Shell 换行规则
├── .gitignore                                # [必需·提交] 构建产物与本地配置忽略规则
├── .dockerignore                             # [条件·提交] 镜像构建排除规则
├── AGENTS.md                                 # [必需·提交] 前端项目规则
├── CLAUDE.md                                 # [必需·提交] Claude Code 前端项目协作规则；正文与 AGENTS.md 一致
├── PROJECT_CURRENT.md                        # [必需·提交] 当前任务与交接状态
├── PROJECT_MEMORY.md                         # [必需·提交] 稳定决策与长期事实
├── PROJECT_HISTORY.md                        # [必需·提交] 重要历史事件
├── PROJECT_STYLE.md                          # [条件·提交] 前端长期风格
└── README.md                                 # [必需·提交] 前端启动、构建与部署入口
```

前端不建立 `src/config/` 或任意 `schema/`。`public/` 与 `src/assets/` 不得复制资源；React 只用 `hooks/`，Vue 只用 `composables/`。前端根的 `AGENTS.md` 与 `CLAUDE.md` 必须同时提交且正文完全一致。

前端 `src/` 与 `src/modules/<domain>/` 未在目录树中列出的其他目录按「统一规范目录与扩展目录」规则处理（见上节）。
