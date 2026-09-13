---
name: sqlite
description: "正确使用 SQLite：并发与 WAL 模式、外键 pragma、类型亲和性、表结构变更限制、性能 pragma、VACUUM 维护、备份安全、索引、事务与批量写入优化、Go/GORM 纯 Go 驱动接入、MySQL 迁移方言适配。适用于新建/接入 SQLite 库、Go+GORM 接入 SQLite、MySQL 转 SQLite 迁移、排查 SQLITE_BUSY/锁等待、批量写入慢、外键不生效、文件膨胀、备份问题场景。触发词：sqlite、sqlite3、数据库锁、SQLITE_BUSY、wal 模式、外键不生效、pragma、VACUUM、批量插入慢、内存数据库、:memory:、db 文件损坏、sqlite 备份、busy_timeout、gorm、glebarez、mysql 转 sqlite。"
license: MIT
metadata:
  displayName: "SQLite 正确使用"
  version: "1.2.0"
  author: "Clawhub Developer"
---

# SQLite 正确使用

SQLite 正确性与性能手册。**先走「工作流」再查「知识区」**：建库接入、并发排障、备份、批量写入各有固定流程；细节按主题知识区深入。

## 工作流

### 新建/接入数据库工作流
1. **每连接必设 pragma**（SQLite 不持久化这些）：
   ```sql
   PRAGMA journal_mode=WAL;      -- 读写并发
   PRAGMA foreign_keys=ON;       -- 外键默认关！
   PRAGMA busy_timeout=5000;     -- 写锁等待 5s
   ```
2. **建表**：主键用显式 `INTEGER PRIMARY KEY`（别依赖 ROWID，VACUUM 会变）；日期存 TEXT(ISO8601) 或 INTEGER(时间戳)；布尔用 INTEGER 0/1。
3. **建索引**：查询热点列加索引；可用部分/表达式索引；`EXPLAIN QUERY PLAN` 验证走索引。
4. **验证**：`PRAGMA foreign_keys` 返回 1；并发读写实测无 `SQLITE_BUSY`。

### 并发/锁排查流程
1. 现象 `SQLITE_BUSY`：先确认 `busy_timeout` 已设（默认 0 = 立即失败）。
2. 确认 WAL 已开启（`PRAGMA journal_mode` 返回 `wal`）。
3. 读后写模式死锁：把事务改成 `BEGIN IMMEDIATE`（提前拿写锁）。
4. 仍冲突：确认没有长事务/没关的写连接（`sqlite3` 命令行 `.databases` 检查）。

### 备份流程
1. **禁止直接复制 db 文件**（写入中会损坏）；WAL 下还需 `-wal`/`-shm` 一起。
2. 用官方方式：sqlite3 命令行 `.backup backup.db`，或 SQL `VACUUM INTO 'backup.db'`（3.27+，生成独立副本）。
3. 验证：`PRAGMA integrity_check` 返回 `ok`。

### 批量写入优化流程
1. 默认 autocommit，逐条 INSERT 很慢。
2. 包事务：`BEGIN; INSERT...; INSERT...; COMMIT;`（可快 10-100 倍）。
3. 配合 `PRAGMA synchronous=NORMAL`（WAL 下安全与速度平衡）。
4. 验证：万条写入耗时显著下降；事务回滚行为正确。

## Concurrency (Biggest Gotcha)

- Only one writer at a time—concurrent writes queue or fail; not for high-write workloads
- Enable WAL mode: `PRAGMA journal_mode=WAL`—allows reads during writes, huge improvement
- Set busy timeout: `PRAGMA busy_timeout=5000`—waits 5s before SQLITE_BUSY instead of failing immediately
- WAL needs `-wal` and `-shm` files—don't forget to copy them with main database
- `BEGIN IMMEDIATE` to grab write lock early—prevents deadlocks in read-then-write patterns

## Foreign Keys (Off by Default!)

- `PRAGMA foreign_keys=ON` required per connection—not persisted in database
- Without it, foreign key constraints silently ignored—data integrity broken
- Check before relying: `PRAGMA foreign_keys` returns 0 or 1
- ON DELETE CASCADE only works if foreign_keys is ON

## Type System

- Type affinity, not strict types—INTEGER column accepts "hello" without error
- `STRICT` tables enforce types—but only SQLite 3.37+ (2021)
- No native DATE/TIME—use TEXT as ISO8601 or INTEGER as Unix timestamp
- BOOLEAN doesn't exist—use INTEGER 0/1; TRUE/FALSE are just aliases
- REAL is 8-byte float—same precision issues as any float

## Schema Changes

- `ALTER TABLE` very limited—can add column, rename table/column; that's mostly it
- Can't change column type, add constraints, or drop columns (until 3.35)
- Workaround: create new table, copy data, drop old, rename—wrap in transaction
- `ALTER TABLE ADD COLUMN` can't have PRIMARY KEY, UNIQUE, or NOT NULL without default

## Go + GORM 接入（纯 Go 驱动，MySQL 迁移实证 2026-09）

- **驱动选型（CGO_ENABLED=0 硬约束）**：GORM 用 `github.com/glebarez/sqlite`（封装 modernc.org/sqlite，纯 Go）；禁用 `gorm.io/driver/sqlite` 与 `mattn/go-sqlite3`（走 CGO，无 gcc 的环境 / Docker golang:alpine 编译直接失败）。纯 Go 驱动下 `CGO_ENABLED=0 go build` 天然可用。
- **DSN pragma（glebarez 特有语法）**：`dbPath + "?_pragma=busy_timeout(5000)&_pragma=journal_mode(WAL)"`——WAL 与 busy_timeout 生产必配，写法与原生 PRAGMA 语句不同。
- **ORM 模型 tag 禁写 MySQL 方言**（SQLite 建表直接语法错误，迁移时逐个清理）：
  - `COMMENT:'…'` 列注释 → SQLite 无列级注释，语义由模型代码注释承载；
  - `ON UPDATE CURRENT_TIMESTAMP` → SQLite 无此子句，更新时间靠 GORM autoUpdateTime（`UpdatedAt` 字段名约定）或业务显式赋值兜底；
  - `type:bigint unsigned` → SQLite 无 unsigned；整型自增主键干脆移除自定义 type，让驱动对 primaryKey+autoIncrement 自动生成 `INTEGER PRIMARY KEY AUTOINCREMENT`（AUTOINCREMENT 只能跟 INTEGER PRIMARY KEY，写 `bigint` 会破坏该生成）；
  - `varchar(n)/text/datetime/bigint` 靠类型亲和保留无害；`tinyint` 建议归一为 `integer`。
- **索引方言**：元数据检查 MySQL `INFORMATION_SCHEMA.STATISTICS` → `sqlite_master WHERE type='index'`；建索引 MySQL `ALTER TABLE t ADD INDEX` → `CREATE INDEX`（SQLite 无 ADD INDEX 语法），或直接 `CREATE INDEX IF NOT EXISTS`（原生幂等）。
- **建库流程**：无需 CREATE DATABASE——单文件库：先 `os.MkdirAll(filepath.Dir(dbPath), …)` 确保目录存在，再 gorm.Open；打开失败必须阻断启动（复用 MySQL 的"建库失败即 fail-fast"语义）。
- **版本控制**：数据目录与 `*.db`、`*.db-wal`、`*.db-shm`（WAL 伴生文件）必须进 `.gitignore`。
- **配置收敛**：MySQL 五连接参数（host/port/user/password/dbname）→ 一个文件路径（yaml/db_path + env 覆盖）；容器部署 `ENV DB_PATH=/data/xx.db` + `VOLUME /data` 持久化数据。
- **迁移前确认旧数据去留**：MySQL 存量数据不会自动过来；开发期数据可弃，生产数据需另写导入脚本（建表后 `INSERT INTO sqlite SELECT ...` 或中间格式）。

## Performance Pragmas

- `PRAGMA optimize` before closing long-running connections—updates query planner stats
- `PRAGMA cache_size=-64000` for 64MB cache—negative = KB; default very small
- `PRAGMA synchronous=NORMAL` with WAL—good balance of safety and speed
- `PRAGMA temp_store=MEMORY` for temp tables in RAM—faster sorts and temp results

## Vacuum & Maintenance

- Deleted data doesn't shrink file—`VACUUM` rewrites entire database, reclaims space
- `VACUUM` needs 2x disk space temporarily—ensure enough room
- `PRAGMA auto_vacuum=INCREMENTAL` with `PRAGMA incremental_vacuum`—partial reclaim without full rewrite
- After bulk deletes, always vacuum or file stays bloated

## Backup Safety

- Never copy database file while open—corrupts if write in progress
- Use `.backup` command in sqlite3—or `sqlite3_backup_*` API
- WAL mode: `-wal` and `-shm` must be copied atomically with main file
- `VACUUM INTO 'backup.db'` creates standalone copy (3.27+)

## Indexing

- Covering indexes work—add extra columns to avoid table lookup
- Partial indexes supported (3.8+): `CREATE INDEX ... WHERE condition`
- Expression indexes (3.9+): `CREATE INDEX ON t(lower(name))`
- `EXPLAIN QUERY PLAN` shows index usage—simpler than PostgreSQL EXPLAIN

## Transactions

- Autocommit by default—each statement is own transaction; slow for bulk inserts
- Batch inserts: `BEGIN; INSERT...; INSERT...; COMMIT`—10-100x faster
- `BEGIN EXCLUSIVE` for exclusive lock—blocks all other connections
- Nested transactions via `SAVEPOINT name` / `RELEASE name` / `ROLLBACK TO name`

## Common Mistakes

- Using SQLite for web app with concurrent users—one writer blocks all; use PostgreSQL
- Assuming ROWID is stable—`VACUUM` can change ROWIDs; use explicit INTEGER PRIMARY KEY
- Not setting busy_timeout—random SQLITE_BUSY errors under any concurrency
- In-memory database `':memory:'`—each connection gets different database; use `file::memory:?cache=shared` for shared

## 适用边界

**何时用**：本地/嵌入式存储（桌面应用、工具、测试、单机服务）、中小规模数据、读多写少或低并发写场景。

**何时不用**：
- 高并发写 / 多用户 Web 应用 → 换 PostgreSQL/MySQL（SQLite 单写者瓶颈）→ 转 `mysql__skillhub`；
- 分布式/多机共享数据库 → 用数据库服务；
- 建表/字段/索引/迁移的强制规则 → 先读 `database-schema-rules`；
- Go 无 CGO 环境用纯 Go 驱动（`modernc.org/sqlite`）→ 转 `cgo-plugin-isolated-test`。

## 验收清单

- [ ] 每连接已设 `foreign_keys=ON`（并验证返回 1）
- [ ] WAL + `busy_timeout` 已配置，无随机 `SQLITE_BUSY`
- [ ] 主键用显式 `INTEGER PRIMARY KEY`，未依赖 ROWID
- [ ] 批量写入已包事务；长连接关闭前跑过 `PRAGMA optimize`
- [ ] 备份用 `.backup` / `VACUUM INTO`，未直接复制 db 文件
- [ ] 删除大量数据后执行过 `VACUUM`（或增量 vacuum）防文件膨胀
- [ ] Go/GORM 接入用纯 Go 驱动（glebarez/sqlite），模型 tag 无 MySQL 方言残留（COMMENT / ON UPDATE / bigint unsigned）
- [ ] 数据文件与 `*.db-wal`/`*.db-shm` 已加入版本控制忽略；容器部署已挂载数据卷
