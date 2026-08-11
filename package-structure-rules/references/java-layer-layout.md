# Java 后端物理位置映射

Java 私有源码根为 `src/main/java/<base-package>/`，其下统一规范目录为 `router/`、`controller/`、`business/<domain>/`；未列出且不在禁止清单的其他目录允许存在，新增须用户确认，且不得作为规范目录的别名。项目关联工具统一放在根 `common/util/`，直接存放可依赖项目其他包的 Java 文件，不得创建子目录。业务域 `rpc/` 直接存放 `String operation(String requestJson)` 形式的公开跨域入口；根级 `database/`、`utils/`、`common/`、`global/`、`crontask/`、`async/`、`middleware/` 与 Java 源码根并列。

项目根 `utils/` 只允许工具包子目录，所有实现必须位于 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。业务域内统一规范目录为 `api/`、`service/`、`entity/`、`base/`、`constant/`、`init/`、`crontask/`、`util/`；未列出的其他目录允许存在，新增须用户确认；业务域内除 `rpc/` 外的**任何**目录（含扩展目录）都是私有层。业务域 `util/` 保留为域私有辅助能力。关系型数据库的 ORM 与持久化模型只放 `database/model/db/`；Redis 与 Mongo 模型分别放 `database/model/redis/`、`database/model/mongo/`。
