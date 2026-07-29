# 数据库、自动迁移与独立 SQL 规则

`database/` 是连接、ORM 模型、Repository、Mapper、事务、自动迁移源码与独立 SQL 的唯一入口。

| 路径 | 允许内容 | 禁止内容 |
|---|---|---|
| `database/migration/` | 注册、排序、执行上下文与公共接口源码 | 独立 SQL、业务查询 |
| `database/migration/field/{create,read,update,delete}/` | 对应字段结构的自动迁移源码 | `.sql`、索引迁移、业务数据写入 |
| `database/migration/index/{create,read,update,delete}/` | 对应索引结构的自动迁移源码 | `.sql`、字段迁移、普通业务查询 |
| `database/sql/ddl/` | 人工或数据库工具直接执行的 DDL SQL | 生产源码 |
| `database/sql/index/` | 人工或数据库工具直接执行的索引 SQL | 生产源码 |

`read/` 只读取数据库结构元数据，不是业务 Repository 查询。迁移错误必须返回给启动或迁移命令；不得吞错继续启动。
