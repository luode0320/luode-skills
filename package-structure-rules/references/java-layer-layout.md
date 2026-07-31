# Java 后端物理位置映射

Java 私有源码根为 `src/main/java/<base-package>/`，其下只使用 `router/`、`controller/`、`util/`、`business/<domain>/`。`src/main/java/<base-package>/util/` 直接存放可依赖项目其他包的高关联工具函数；不得创建其子目录。业务域 `rpc/` 直接存放 `String operation(String requestJson)` 形式的公开跨域入口；根级 `database/`、`utils/`、`common/`、`global/`、`crontask/`、`async/`、`middleware/` 与 Java 源码根并列。

项目根 `utils/` 只允许工具包子目录，所有实现必须位于 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。业务域内采用 `api/`、`service/`、`entity/`、`base/`、`constant/`、`init/`、`crontask/`、`util/`；业务域 `util/` 保留为域私有辅助能力。关系型数据库的 ORM 与持久化模型只放 `database/model/db/`；Redis 与 Mongo 模型分别放 `database/model/redis/`、`database/model/mongo/`。
