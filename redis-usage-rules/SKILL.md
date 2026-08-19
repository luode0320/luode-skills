---
name: redis-usage-rules
description: 当新增或修改 Redis 操作、缓存读写、键值查询、TTL 检查、Redis 监控、备份导出导入、FLUSHDB 清理或 redis-cli 命令时自动触发。负责统一 Redis 实例的连接约定、类型识别读取、键健康检查、监控判读、备份恢复格式与危险操作安全红线；连接配置必须使用 REDIS_HOST/PORT/DB/PASSWORD 环境变量约定，读取必须按 TYPE 自动分发，FLUSHDB 必须双确认；不要用它代替 database-query-rules（SQL/GORM 访问）、database-schema-rules（表结构）或缓存 key 设计/失效策略约束（项目级缓存策略）。
---
# Redis 使用与运维规则

只在"Redis 实例怎么连、键怎么读、健康状态怎么看、备份怎么做、危险操作怎么防"这个问题上使用这个 skill。
如果当前问题是 SQL/Repository/GORM 访问，请转交 `database-query-rules`；如果是表结构、字段、索引和迁移脚本，请转交 `database-schema-rules`；如果是缓存 key 设计、过期策略、并发保护，那属于项目级缓存策略约束（项目级 `redis-usage-rules-project` 主题），不在本 skill 范围。

## Skill 作用与适用场景

- 统一 Redis 连接配置约定：`REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` / `REDIS_PASSWORD` 四个环境变量，缺省 `127.0.0.1:6379/0`，有密码时追加 `-a <PASSWORD> --no-auth-warning`。
- 统一键读取方式：任何读取先 `TYPE <key>` 自动分发，按 string / list / set / hash / zset 五大数据类型选择对应读法，并展示 TTL。
- 统一键健康检查：`KEYS <pattern>`（默认 `*`）逐键输出 `key [type] TTL` 对齐列表与总计数。
- 统一监控判读口径：`INFO` / `INFO stats` / `SLOWLOG` 的提炼要点与命中率、内存碎片率、ops/sec 的计算口径。
- 统一备份导出/导入行格式：`TYPE|key|ttl|值` 单行格式，五类数据可无损迁移。
- 统一危险操作安全红线：`FLUSHDB` 必须展示待删数量并键入 `YES FLUSH` 双确认后才执行。
- 防止把 Redis 运维操作做成一次性随手命令、把凭据硬编码、或在生产实例上直接 `MONITOR` / `KEYS '*'` 造成阻塞。

## 自动触发信号

- 新增或修改 Redis 连接、查询、写入、删除、TTL/类型检查、键列举。
- 需要检查 Redis 键健康状态、数据类型验证、内存/命中率统计或慢日志。
- 需要生成 Redis 备份、导入恢复或确认清理（FLUSHDB / DEL 批量）。
- 需要 lint Redis 配置或核对连接参数约定。
- 发现 Redis 相关代码直接硬编码连接串、绕过类型识别直接 GET、或缺少安全确认就执行清库。

## 进入后先做什么

1. 先确认当前是 Redis 运维操作，而不是缓存 key 设计或 SQL 访问问题；是则转交对应 skill。
2. 确认连接参数来自环境变量约定（`REDIS_HOST`/`REDIS_PORT`/`REDIS_DB`/`REDIS_PASSWORD`），不硬编码。
3. 确认操作前先校验连通性（`PING` 必须返回 `PONG`）与 `redis-cli` 可用性。
4. 确认读取类操作按 `TYPE` 分发而非一律 `GET`。
5. 确认危险操作（FLUSHDB / 批量 DEL / 导入覆盖）有安全确认步骤。

## 默认执行流程

1. 默认先读 `references/redis-usage-and-commands.md`，确认连接约定、类型识别读取、键健康检查、写入删除与输出规范。
2. 如果涉及监控、备份、导入恢复或危险操作，再读 `references/redis-monitoring-backup-and-safety.md`。
3. 按操作类型输出：连接校验结果、读取键的类型与 TTL、健康检查汇总、监控判读结论、备份文件格式说明或安全确认记录。
4. 每个操作记录审计日志（时间戳 + 操作摘要）。
5. 如果问题本质落回缓存 key 设计 / 过期策略 / 并发保护，停止停留在本 skill 并转给项目级缓存策略约束。

## 权责边界与不负责事项

- 只负责 Redis 运维操作规则，不负责缓存 key 设计、过期策略和并发保护——那属于项目级缓存策略约束（项目级 `redis-usage-rules-project` 主题），本 skill 不重复定义。
- 不负责 SQL、Repository、DAO、Mapper、GORM 访问——那属于 `database-query-rules`。
- 不负责表结构、字段、索引和迁移脚本——那属于 `database-schema-rules`。
- 不负责业务侧客户端封装位点（如是否直建客户端、目录归属）——那属于 `package-structure-rules` 的 Redis 目录位点约定。
- 不承诺替任何工具链（如 bash 脚本、Python redis-py）维护实现，只输出规则与命令清单。
- 不允许把凭据硬编码进代码、配置或日志；不允许跳过 `FLUSHDB` 双确认；不允许在生产实例无确认执行 `MONITOR` 或 `KEYS '*'`。

## 需要暂停并确认的条件

- 当前涉及清空数据库（FLUSHDB）或批量删除大量键，必须先展示影响数量并获得 `YES FLUSH` 级确认。
- 当前要在生产或共享实例上执行 `MONITOR`、`KEYS '*'` 全量扫描或全量导出，需先评估阻塞风险并确认。
- 当前导入备份会覆盖已有键，需先确认覆盖策略与幂等保护。
- 当前环境没有 `redis-cli`，需要先按安装指引补齐（Windows 环境走 WSL），不要跳过预检硬跑。

## 执行通过 / 驳回标准

- 通过：连接参数来自环境变量约定；读取按类型分发并展示 TTL；健康检查、监控判读、备份格式均符合本 skill 规则；危险操作有双确认证据；操作有日志审计记录。
- 驳回：连接串硬编码、凭据写入日志、一律 `GET` 不识别类型、生产实例无确认执行 `MONITOR`/`KEYS '*'`、`FLUSHDB` 无双确认、备份格式偏离 `TYPE|key|ttl|值`、或把缓存 key 设计问题误当作运维问题处理。

## 执行结果归档要求

- 将连接配置来源、读取键清单、健康检查/监控判读结论、备份文件路径与格式、安全确认记录写入任务记录或评审记录。
- 归档内容至少包含：操作类型、涉及键范围、TTL/类型信息、监控指标判读、备份文件位置、危险操作确认证据。
- 若调整了连接约定或备份格式，必须记录兼容影响与观察点。

## references 读取规则

- 默认先读 `references/redis-usage-and-commands.md`。
- 只有在涉及监控、备份、导入恢复或危险操作时，再读 `references/redis-monitoring-backup-and-safety.md`。
