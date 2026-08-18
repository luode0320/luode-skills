# Java 后端物理位置映射

Java 私有源码根为 `src/main/java/<base-package>/`，其下直连业务域 `<domain>/`，业务相关逻辑通过 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 四类版本化目录完全隔离；未列出且不在禁止清单的其他目录允许存在，新增须用户确认，且不得作为规范目录的别名。项目关联工具统一放在根 `common/util/`，直接存放可依赖项目其他包的 Java 文件，不得创建子目录。根级 `database/`、`utils/`、`common/`、`global/`、`crontask/`、`async/`、`middleware/` 与 Java 源码根并列。

项目根 `utils/` 只允许工具包子目录，所有实现必须位于 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。业务域级通用目录为 `api/`、`base/`、`constant/`、`util/` 与单文件 `init.<ext>`；版本化目录 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 内各自按版本隔离，版本从 `v1` 递增，包名用 `v?router`、`v?controller`、`v?entity`、`v?service` 别名引用。业务域之间禁止直接导入对方任何目录（无 `rpc/` 例外）。业务域 `util/` 保留为域私有辅助能力。关系型数据库的 ORM 与持久化模型只放 `database/model/db/`；Redis 与 Mongo 模型分别放 `database/model/redis/`、`database/model/mongo/`。
