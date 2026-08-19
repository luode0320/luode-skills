# Redis 监控 / 备份 / 安全红线

> 归属 owner：`redis-usage-rules`。本文件承载 Redis 监控判读、备份导出/导入格式、危险操作安全红线与工具链安装指引，与 `redis-usage-and-commands.md` 互补。

## 一、安装指引（redis-cli 缺失）

| 平台 | 安装命令 |
| --- | --- |
| Ubuntu/Debian | `sudo apt-get install redis-tools` |
| CentOS/RHEL | `sudo yum install redis` |
| macOS | `brew install redis` |
| Alpine | `apk add redis` |
| Windows | 无官方 redis-cli，统一走 WSL：`wsl -e bash -c "sudo apt-get install redis-tools"` |

## 二、监控判读

### 2.1 实时监控（慎用）

- `MONITOR` 直通输出实例上全部命令，`Ctrl+C` 停止。
- 生产/共享实例**必须确认后才执行**：MONITOR 会放大流量与日志开销，禁止无确认开启。

### 2.2 服务器信息（INFO）

- `INFO [section]`；无参时提炼以下四块：
  - **version**：`redis_version`
  - **uptime**：`uptime_in_seconds`，换算为 `天/时/分` 展示
  - **clients**：`connected_clients`
  - **memory / keyspace**：`used_memory_human` 与各 `dbN` 键分布

### 2.3 统计聚合（stats 判读口径）

| 指标 | 来源 | 判读口径 |
| --- | --- | --- |
| 内存使用 / 峰值 | `INFO memory` → `used_memory` / `used_memory_peak` | 字节换算后展示 |
| 碎片率 | `INFO memory` → `mem_fragmentation_ratio` | 明显大于 1 表示内存碎片偏高 |
| 命中 / 未命中 | `INFO stats` → `keyspace_hits` / `keyspace_misses` | 命中率 = 命中 ÷ (命中 + 未命中) × 100%，总数为 0 时记 0 |
| 总键数 | `DBSIZE` | 当前库键数 |
| 按库分布 | `INFO keyspace` → `dbN` 行 | 逐库展示 |
| 连接数 | `INFO clients` → `connected_clients` / `blocked_clients` | 阻塞数异常升高提示等待问题 |
| ops/sec | `INFO stats` → `instantaneous_ops_per_sec` | 当前每秒操作数 |

### 2.4 慢日志

- `SLOWLOG GET <count>`（默认 10 条），用于定位慢命令；结合 `CONFIG GET slowlog-log-slower-than` 核对慢日志阈值配置（即"配置 lint"入口）。

## 三、备份导出 / 导入格式（可无损迁移）

### 3.1 导出行格式

每键一行，统一为 `TYPE|key|ttl|值`（单行，`|` 分隔）：

| 类型 | 值序列化 |
| --- | --- |
| `STRING` | 原始值 |
| `LIST` | 元素逗号分隔（`LRANGE 0 -1` 结果 `paste -sd ','`） |
| `SET` | 成员逗号分隔（`SMEMBERS` 结果 `paste -sd ','`） |
| `HASH` | `field=value` 两两配对后逗号分隔（`HGETALL` 结果按行配对、`=` 连接） |
| `ZSET` | `member:score` 两两配对后逗号分隔（`ZRANGE WITHSCORES` 结果按行配对、`:` 连接） |

- 不支持/未知类型：写 `# SKIP|key|unsupported type: <type>` 注释行，导入时跳过并计数。
- TTL 为 `-1`（永久）时 ttl 列原样记录；为正整数时记录剩余秒数，导入时重建过期。
- 导出遍历用 `KEYS '*'`，生产大库优先 `SCAN` 或确认后执行（阻塞风险同键健康检查节）。

### 3.2 导入重建映射

| 行类型 | 重建命令 |
| --- | --- |
| `STRING` | `SET <key> <value>` |
| `LIST` | 先 `DEL` 再逐元素 `RPUSH` |
| `SET` | 先 `DEL` 再逐成员 `SADD` |
| `HASH` | 先 `DEL` 再逐对 `HSET` |
| `ZSET` | 先 `DEL` 再逐对 `ZADD <score> <member>` |

- TTL 为正整数时，重建后补 `EXPIRE <key> <ttl>`；`# SKIP` 行跳过并计数。
- 导入会覆盖同名键：先确认覆盖策略与幂等保护，再执行。

## 四、危险操作安全红线（强制）

1. **FLUSHDB 双确认**：执行前先展示 `DBSIZE` 待删数量，必须键入 `YES FLUSH` 才执行；输入不匹配则中止，不删除任何数据。禁止任何形式的无条件 `FLUSHDB` / `FLUSHALL`。
2. **批量 DEL**：涉及多键删除时按返回值区分结果；大批量删除先评估影响面。
3. **生产实例**：`MONITOR`、`KEYS '*'` 全量扫描、全量导出、`FLUSHDB` 都属于需要确认的操作，默认禁止直接执行。
4. **凭据安全**：密码只经环境变量传递，日志与归档摘要不回显明文密码；命令行 `-a` 传参必须带 `--no-auth-warning`。

## 五、操作日志审计

- 每个操作写一条审计日志：`[时间戳] 操作摘要`（如 `FLUSHDB: confirmed, dbsize was 123`、`EXPORT: file=backup.dat count=50`）。
- 日志落点与保留策略由项目约定（不沿用外部 skill 的 `~/.local/share/redis-helper` 专属路径）；摘要不得包含凭据。

## 六、典型命令速查

```bash
# 监控
redis-cli INFO server                      # version / uptime
redis-cli INFO memory                      # used_memory / mem_fragmentation_ratio
redis-cli INFO stats                       # keyspace_hits / keyspace_misses / ops
redis-cli INFO keyspace                    # 各 dbN 分布
redis-cli SLOWLOG GET 10                   # 慢日志

# 备份导出（逐键）
printf 'STRING|%s|%s|%s\n' "$key" "$ttl" "$(redis-cli --raw GET "$key")"

# 备份导入（按类型重建 + 补 TTL）
redis-cli SET "$key" "$value"
redis-cli EXPIRE "$key" "$ttl"             # ttl 为正整数时

# 危险操作（必须双确认）
redis-cli DBSIZE                           # 先展示待删数量
# 键入 "YES FLUSH" 后才执行：
redis-cli FLUSHDB
```
