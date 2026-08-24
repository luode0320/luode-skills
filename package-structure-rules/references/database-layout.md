# 数据库、自动迁移与执行脚本规则

`database/` 是关系型数据库、Redis、Mongo 等数据存储服务的连接、模型、Repository、Mapper、事务、自动迁移源码与手工执行脚本的唯一入口。

| 路径 | 允许内容 | 禁止内容 |
|---|---|---|
| `database/connection/` | 关系型数据库、Redis、Mongo 等数据存储服务的连接、连接池、方言和客户端初始化源码 | 业务流程、业务实体、执行脚本 |
| `database/model/` | `db/`、`redis/`、`mongo/` 三类数据存储模型子目录 | 直接文件、执行脚本、业务实体 |
| `database/model/db/` | 关系型数据库表映射、ORM 和持久化模型源码 | Redis/Mongo 模型、执行脚本 |
| `database/model/redis/` | Redis Key、Hash、缓存值等数据模型源码 | 关系型数据库/Mongo 模型、执行脚本 |
| `database/model/mongo/` | Mongo 集合与文档模型源码 | 关系型数据库/Redis 模型、执行脚本 |
| `database/migration/` | 注册、排序、执行上下文与公共接口源码 | 执行脚本、业务查询 |
| `database/migration/field/{create,read,update,delete}/` | 对应字段结构的自动迁移源码 | `.sql`、索引迁移、业务数据写入 |
| `database/migration/index/{create,read,update,delete}/` | 对应索引结构的自动迁移源码 | `.sql`、字段迁移、普通业务查询 |
| `database/scripts/` | `sql/`、`js/`、`lua/` 三类执行脚本子目录 | 直接文件、生产源码、业务实体 |
| `database/scripts/sql/` | `ddl/`、`index/`、`field/` 三类独立 SQL 子目录 | 直接文件、生产源码 |
| `database/scripts/sql/ddl/` | 人工或数据库工具直接执行的建表、改表与约束 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/scripts/sql/index/` | 人工或数据库工具直接执行的索引 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/scripts/sql/field/create/` | 人工或数据库工具直接执行的新增字段 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/scripts/sql/field/update/` | 人工或数据库工具直接执行的修改字段 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/scripts/sql/field/delete/` | 人工或数据库工具直接执行的删除字段 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/scripts/js/` | 人工或数据库工具直接执行的 Mongo shell 脚本 `.js` 文件 | 生产源码、非 `.js` 文件、子目录 |
| `database/scripts/lua/` | 人工或数据库工具直接执行的 Redis 执行脚本 `.lua` 文件 | 生产源码、非 `.lua` 文件、子目录 |

`read/` 只读取数据库结构元数据，不是业务 Repository 查询；它只属于自动迁移生产源码，不对应独立字段 SQL。迁移错误必须返回给启动或迁移命令；不得吞错继续启动。

`database/scripts/` 按执行文件类型分子目录（`sql/`、`js/`、`lua/`），与根 `scripts/database/`（已禁止）无关；后续新增脚本类型按扩展目录准入（allowed_children + entry + 文档同步）扩展。旧 `database/sql/` 已废弃，命中即禁止；存量项目在 `doc/1-架构/3-目录规则收敛清单.yaml` 中登记 `legacy_source_roots` 快照，不自动迁移。
