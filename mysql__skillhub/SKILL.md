---
name: mysql
description: "编写正确高效的 MySQL 查询：字符集与排序规则（utf8mb4）、索引设计、UPSERT、事务与锁（InnoDB）、GROUP BY 严格模式、连接管理、复制感知、慢查询性能优化。适用于编写/审查 MySQL SQL、排查慢查询/死锁/乱码、索引优化场景。触发词：mysql、sql 查询、慢查询、explain、死锁、锁等待、utf8mb4、字符集乱码、索引优化、事务隔离、ON DUPLICATE KEY、连接池、主从复制、group by 报错、mysql 报错。"
license: MIT
metadata:
  displayName: "MySQL 查询与优化"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# MySQL 查询与优化

MySQL 专属查询正确性与性能手册。**先走「工作流」再查「知识区」**：写查询、查慢查询、解死锁分别有固定流程；知识点按主题索引文件深入。

## 工作流

### 写查询工作流
1. 确认字符集：库/表/连接统一 `utf8mb4`（`SET NAMES utf8mb4`）。
2. 写 SQL：注意 MySQL 特有语法（`LIMIT offset,count`、`IFNULL`、`ON DUPLICATE KEY UPDATE`）。
3. `EXPLAIN` 验证：`type` 期望 `ref`/`range`，出现 `ALL` 则检查索引。
4. 检查聚合：`ONLY_FULL_GROUP_BY` 下非聚合列必须进 `GROUP BY`。
5. 测试边界：空表、NULL 列、重复键（UPSERT 的 affected rows 语义）。

### 慢查询排查流程
1. `SHOW PROCESSLIST` 找长时间运行的查询，`KILL <id>` 必要时终止。
2. `EXPLAIN` 目标 SQL，定位全表扫描/索引失效列。
3. 确认连接与字符集：排序规则不一致的 JOIN 会杀性能。
4. 优化手段：加索引 → 覆盖索引 → 拆分查询 → 应用层缓存（MySQL 8 已移除 query cache，别依赖）。
5. 大表 DDL/碎片整理用 `pt-online-schema-change` 而非直接 `OPTIMIZE TABLE`（会锁表）。

### 死锁/锁等待排查流程
1. 确认隔离级别：InnoDB 默认 `REPEATABLE READ`（next-key locking 是死锁常见源）。
2. 看锁等待：`innodb_lock_wait_timeout` 默认 50s，超时即报错。
3. 业务代码必须**捕获死锁并重试**（死锁是预期事件，不是异常状态）。
4. 队列消费场景：MySQL 8 用 `FOR UPDATE SKIP LOCKED`，避免行锁互相阻塞。

## Quick Reference

| Topic | File |
|-------|------|
| Index design deep dive | `indexes.md` |
| Transactions and locking | `transactions.md` |
| Query optimization | `queries.md` |
| Production config | `production.md` |

## Character Set Traps

- `utf8` is broken—only 3 bytes, can't store emoji; always use `utf8mb4`
- `utf8mb4_unicode_ci` for case-insensitive sorting; `utf8mb4_bin` for exact byte comparison
- Collation mismatch in JOINs kills performance—ensure consistent collation across tables
- Connection charset must match: `SET NAMES utf8mb4` or connection string parameter
- Index on utf8mb4 column larger—may hit index size limits; consider prefix index

## Index Differences from PostgreSQL

- No partial indexes—can't `WHERE active = true` in index definition
- No expression indexes until MySQL 8.0.13—must use generated columns before that
- TEXT/BLOB needs prefix length: `INDEX (description(100))`—without length, error
- No INCLUDE for covering—add columns to index itself: `INDEX (a, b, c)` to cover c
- Foreign keys auto-indexed only in InnoDB—verify engine before assuming

## UPSERT Patterns

- `INSERT ... ON DUPLICATE KEY UPDATE`—not standard SQL; needs unique key conflict
- `LAST_INSERT_ID()` for auto-increment—no RETURNING clause like PostgreSQL
- `REPLACE INTO` deletes then inserts—changes auto-increment ID, triggers DELETE cascade
- Check affected rows: 1 = inserted, 2 = updated (counter-intuitive)

## Locking Traps

- `SELECT ... FOR UPDATE` locks rows—but gap locks may lock more than expected
- InnoDB uses next-key locking—prevents phantom reads but can cause deadlocks
- Lock wait timeout default 50s—`innodb_lock_wait_timeout` for adjustment
- `FOR UPDATE SKIP LOCKED` exists in MySQL 8+—queue pattern
- InnoDB default isolation is REPEATABLE READ, not READ COMMITTED like PostgreSQL
- Deadlocks are expected—code must catch and retry, not just fail

## GROUP BY Strictness

- `sql_mode` includes `ONLY_FULL_GROUP_BY` by default in MySQL 5.7+
- Non-aggregated columns must be in GROUP BY—unlike old MySQL permissive mode
- `ANY_VALUE(column)` to silence error when you know values are same
- Check sql_mode on legacy databases—may behave differently

## InnoDB vs MyISAM

- Always use InnoDB—transactions, row locking, foreign keys, crash recovery
- MyISAM still default for some system tables—don't use for application data
- Check engine: `SHOW TABLE STATUS`—convert with `ALTER TABLE ... ENGINE=InnoDB`
- Mixed engines in JOINs work but lose transaction guarantees

## Query Quirks

- `LIMIT offset, count` different order than PostgreSQL's `LIMIT count OFFSET offset`
- `!=` and `<>` both work; prefer `<>` for SQL standard
- No transactional DDL—`ALTER TABLE` commits immediately, can't rollback
- Boolean is `TINYINT(1)`—`TRUE`/`FALSE` are just 1/0
- `IFNULL(a, b)` instead of `COALESCE` for two args—though COALESCE works

## Connection Management

- `wait_timeout` kills idle connections—default 8 hours; pooler may not notice
- `max_connections` default 151—often too low; each uses memory
- Connection pools: don't exceed max_connections across all app instances
- `SHOW PROCESSLIST` to see active connections—kill long-running with `KILL <id>`

## Replication Awareness

- Statement-based replication can break with non-deterministic functions—UUID(), NOW()
- Row-based replication safer but more bandwidth—default in MySQL 8
- Read replicas have lag—check `Seconds_Behind_Master` before relying on replica reads
- Don't write to replica—usually read-only but verify

## Performance

- `EXPLAIN ANALYZE` only in MySQL 8.0.18+—older versions just EXPLAIN without actual times
- Query cache removed in MySQL 8—don't rely on it; cache at application level
- `OPTIMIZE TABLE` for fragmented tables—locks table; use pt-online-schema-change for big tables
- `innodb_buffer_pool_size`—set to 70-80% of RAM for dedicated DB server

## 适用边界

**何时用**：编写/审查 MySQL SQL、排查慢查询/死锁/乱码、索引与事务优化、连接与复制问题定位。

**何时不用**：
- 建表/字段/索引/迁移的强制规则 → 先读 `database-schema-rules`（含逻辑外键铁律）；
- SQL/Repository/DAO 查询层规范 → 转 `database-query-rules`；
- 数据库整体设计方法论（ER/范式/分库分表）→ 转 `self-ent-tech-database-design__skillhub`；
- SQLite 专属语法/行为 → 转 `sqlite__skillhub`；
- 生产环境大版本升级/备份恢复等重型运维 → 转人工 DBA。

## 验收清单

- [ ] 字符集统一 `utf8mb4`（含连接串），无乱码
- [ ] 查询已 `EXPLAIN`，无 `ALL` 全表扫描
- [ ] JOIN 两端排序规则一致
- [ ] `GROUP BY` 符合 `ONLY_FULL_GROUP_BY`（或明确用 `ANY_VALUE`）
- [ ] 死锁路径已捕获并重试；队列场景用了 `SKIP LOCKED`
- [ ] 写入路径外键列有索引（InnoDB 下外键自动索引，逻辑外键需手建）
