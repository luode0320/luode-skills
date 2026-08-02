# 查找、引用与复用契约

## 查找顺序

1. 明确路径、文件名、符号或当前编辑文件优先。
2. 使用 `placement_catalog.py query` 取得唯一规范位置。
3. 在规范位置按名称、关键行为、输入和输出搜索同语义实现。
4. 需要调用链或影响面时使用 CodeGraph；索引不存在且处于只读规划时回退本地搜索。
5. 多候选无法依据当前文件、模块或语义裁决时再请求用户确认。

## 旧项目渐进采纳

先判断本次代码是维护已存在的遗留源码，还是新增业务、模块或独立逻辑：

1. 遗留代码仅在 `doc/1-架构/3-目录规则收敛清单.yaml` 的 `legacy_source_roots` 已登记根内维护；不得新增源码文件、目录或独立逻辑。
2. `adopted_paths` 只接受能由 V2 Catalog 返回唯一位置的路径；该路径的后续新增必须按 Catalog 的允许子目录、内容类型和扩展名规则执行。
3. 目录名称或职责相似不构成沿用依据。无法唯一匹配的既有遗留目录必须先人工登记为 `legacy_source_roots`，再进行维护。
4. 新业务、新模块和可独立演进的新逻辑始终通过 Catalog 查询 V2 唯一位置；不得以维护遗留目录为由回退到 `legacy_source_roots`。
5. `strict` 与 `legacy` 保持既有含义；`adoption` 策略以收敛清单决定 V2 路径扩展与遗留维护边界。`check`、`init`、`render` 都不得写入、更新或自动生成该清单。

## 引用方向

- 二进制启动装配只从对应入口文件开始：独立后端默认入口为根 `main.<ext>`，额外入口为 `cmd/<binary>/main.<ext>`；同仓后端入口为 `backend/main.<ext>` 或 `backend/cmd/<binary>/main.<ext>`。入口目录不承载可复用业务包，复用逻辑必须回到源码根、业务域或公共技术目录的规范位置。
- 路由与控制器可依赖业务层、根 `common/`、根 `middleware/`、根 `utils/` 与源码根 `util/` 的公开入口。
- 业务服务可依赖 `database/`、根 `common/`、根 `utils/`、源码根 `util/` 与本业务域代码。
- 根 `utils/` 只依赖自身子包、语言标准库与第三方依赖；不得依赖源码根、业务域、`database/`、`common/`、`global/` 或 `middleware/`。
- 源码根 `util/` 可依赖项目其他包，但不得承载业务流程；其实现文件必须直接放在该目录，禁止建立子目录。
- 调用方业务域只能导入目标业务域 `business/<domain>/rpc/` 的公开入口；不得导入目标域的 `api/`、`service/`、`entity/`、`base/`、`constant/`、`init/`、`crontask/` 或 `util/`。
- 目标域 `rpc/` 的公开函数固定接收 JSON 字符串并返回 JSON 字符串；它在本域内完成反序列化、校验、业务服务调用和响应序列化。任何成功、JSON 解析、校验或业务失败都返回符合根 `common/response.Response` 语义的 `code`、`status`、`message`、`data`，不跨域传递语言异常、内部实体或仓储模型。
- 根 `common/request/`、`common/response/`、`common/constant/`、`common/error/`、`common/validation/` 可作为稳定公共结构直接流通。根 `global/` 只能提供已装配的配置、日志、数据库连接和技术客户端等非业务运行引用，禁止保存、传递业务实体、业务列表、业务状态或可变业务缓存。
- `database/`、根 `utils/`、根 `common/`、根 `global/`、根 `middleware/` 禁止反向依赖具体业务域。
- `database/connection/` 只提供数据存储连接与客户端初始化，`database/model/{db,redis,mongo}/` 只承载相应存储模型；二者不得承载业务流程。独立字段 SQL 只能使用 `database/sql/field/{create,update,delete}/` 的直接 `.sql` 文件，自动迁移源码仍只在 `database/migration/`。
- `database/repository/` 不得调用迁移程序；自动迁移只允许启动装配、迁移命令和数据库初始化链路调用。
- 新增目录、删除目录或职责迁移后，更新 `doc/1-架构/2-目录树.md`。
