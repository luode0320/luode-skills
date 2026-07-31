# 数据库、自动迁移与独立 SQL 规则

`database/` 是关系型数据库、Redis、Mongo 等数据存储服务的连接、模型、Repository、Mapper、事务、自动迁移源码与独立 SQL 的唯一入口。

| 路径 | 允许内容 | 禁止内容 |
|---|---|---|
| `database/connection/` | 关系型数据库、Redis、Mongo 等数据存储服务的连接、连接池、方言和客户端初始化源码 | 业务流程、业务实体、独立 SQL |
| `database/model/` | `db/`、`redis/`、`mongo/` 三类数据存储模型子目录 | 直接文件、独立 SQL、业务实体 |
| `database/model/db/` | 关系型数据库表映射、ORM 和持久化模型源码 | Redis/Mongo 模型、独立 SQL |
| `database/model/redis/` | Redis Key、Hash、缓存值等数据模型源码 | 关系型数据库/Mongo 模型、独立 SQL |
| `database/model/mongo/` | Mongo 集合与文档模型源码 | 关系型数据库/Redis 模型、独立 SQL |
| `database/migration/` | 注册、排序、执行上下文与公共接口源码 | 独立 SQL、业务查询 |
| `database/migration/field/{create,read,update,delete}/` | 对应字段结构的自动迁移源码 | `.sql`、索引迁移、业务数据写入 |
| `database/migration/index/{create,read,update,delete}/` | 对应索引结构的自动迁移源码 | `.sql`、字段迁移、普通业务查询 |
| `database/sql/ddl/` | 人工或数据库工具直接执行的建表、改表与约束 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/sql/index/` | 人工或数据库工具直接执行的索引 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/sql/field/create/` | 人工或数据库工具直接执行的新增字段 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/sql/field/update/` | 人工或数据库工具直接执行的修改字段 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |
| `database/sql/field/delete/` | 人工或数据库工具直接执行的删除字段 `.sql` 文件 | 生产源码、非 `.sql` 文件、子目录 |

`read/` 只读取数据库结构元数据，不是业务 Repository 查询；它只属于自动迁移生产源码，不对应独立字段 SQL。迁移错误必须返回给启动或迁移命令；不得吞错继续启动。
