# Redis 使用与命令清单（连接 / 类型识别读取 / 键健康检查 / 写入删除 / 输出规范）

> 归属 owner：`redis-usage-rules`。本文件是 Redis 连接与日常键操作规则的唯一承载，与 `redis-monitoring-backup-and-safety.md` 互补（后者承载监控、备份与安全红线）。

## 一、连接约定

### 1.1 连接参数一律来自环境变量（禁止硬编码）

| 变量 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `REDIS_HOST` | 否 | `127.0.0.1` | Redis 主机 |
| `REDIS_PORT` | 否 | `6379` | Redis 端口 |
| `REDIS_DB` | 否 | `0` | 数据库编号 |
| `REDIS_PASSWORD` | 否 | 空 | 认证密码，仅经环境变量传递 |

- 连接命令统一构建为：`redis-cli -h <HOST> -p <PORT> -n <DB>`；设置密码时追加 `-a <PASSWORD> --no-auth-warning`。
- `--no-auth-warning` 必须带上：抑制 redis-cli 对命令行密码的告警输出，避免污染脚本输出。
- 凭据不得写入代码、配置仓库或日志文件；密码出现在命令行参数中是 redis-cli 接口的固有行为，属可接受范围，但日志摘要不得回显明文密码。

### 1.2 连通性校验（每次操作前）

- 先发 `PING`，返回值必须为 `PONG` 才算连通。
- 失败时按以下三选一给出定位提示并中止，不猜测：
  1. Redis 服务未启动；
  2. 主机/端口错误（检查 `REDIS_HOST`、`REDIS_PORT`）；
  3. 密码错误（检查 `REDIS_PASSWORD`）。

### 1.3 环境预检（redis-cli 缺失）

- 每个操作前用 `command -v redis-cli` 检查；缺失时给出分平台安装指引并中止（详见 `redis-monitoring-backup-and-safety.md` 安装指引节）。
- Windows 本机无官方 redis-cli：统一走 WSL（`wsl -e bash -c "redis-cli ..."`）或容器内执行，不绕过预检。

## 二、类型自动识别读取（键健康检查核心）

任何读取先 `TYPE <key>` 分发，**禁止一律 `GET`**：

| TYPE 结果 | 含义与处理 |
| --- | --- |
| `string` | `GET <key>` 取值 + `TTL <key>` 显示；TTL `-1` 显示 "no expiry" |
| `list` | `LLEN <key>` 得长度 + `LRANGE <key> 0 -1` 取值；超过 100 条截断并提示 |
| `set` | `SCARD <key>` 得成员数 + `SMEMBERS <key>` 列成员；超过 100 条截断并提示 |
| `hash` | `HLEN <key>` 得字段数 + `HGETALL <key>`（按 field/value 两两配对成行）；超过 100 条截断并提示 |
| `zset` | `ZCARD <key>` 得成员数 + `ZRANGE <key> 0 -1 WITHSCORES`（score→value 两两配对）；超过 100 条截断并提示 |
| `none` | 键不存在，警告并退出 |
| 其他/未知 | 回退 `GET` → `DUMP` 兜底展示，无法展示则说明"不支持的类型" |

### TTL 语义（统一判读口径）

| TTL 值 | 语义 | 展示 |
| --- | --- | --- |
| `-2` | 键不存在 | 警告 |
| `-1` | 永久（无过期） | 提示 "no expiry" |
| 正整数 | 剩余秒数 | 显示 `N s` |

### 键健康检查（列表扫描）

- `KEYS <pattern>`（默认 `*`），逐键输出对齐列表：`key  [type]  TTL: Ns`，末尾附总计数；无键时输出 `(no keys found)`。
- 注意：`KEYS '*'` 在大库上会阻塞服务，生产/共享实例优先改用 `SCAN` 游标迭代，或明确确认后才执行全量列举。

## 三、写入 / 删除 / 列举 / 大小

| 操作 | 命令 | 校验规则 |
| --- | --- | --- |
| 写入 | `SET <key> <value> [额外参数...]` | 额外参数（如 `EX 60`）原样透传；返回值必须为 `OK`，否则报错并中止 |
| 删除 | `DEL <key> [key...]` | 支持多键；按返回值区分"已删除 N 个"与"键不存在（无删除）" |
| 列举 | `KEYS <pattern>` | 见上文"键健康检查" |
| 大小 | `DBSIZE` | 返回当前库键数 |

## 四、输出规范

- 统一前缀：成功 `[✓]`、警告 `[!]`、错误 `[✗]`（错误走 stderr），区块标题用分隔线。
- 数据量保护：任何列表/成员/字段展示默认截断 100 条，超出时显式提示总数。
- 字节自动换算：内存等字节数按 `GB/MB/KB/B` 换算后展示（`>= 1GB` 显示 GB，`>= 1MB` 显示 MB，`>= 1KB` 显示 KB，否则 B）。
- 操作审计：每个操作写一条日志（时间戳 + 操作摘要，如 `GET: key=x type=string`），日志落点由项目约定，不写入凭据。

## 五、典型命令速查

```bash
# 连接校验
redis-cli -h 127.0.0.1 -p 6379 -n 0 PING          # 期望 PONG

# 类型识别读取
redis-cli --raw TYPE <key>
redis-cli --raw TTL <key>
redis-cli --raw GET <key>                          # string
redis-cli --raw LRANGE <key> 0 -1                  # list
redis-cli --raw SMEMBERS <key>                     # set
redis-cli --raw HGETALL <key>                      # hash（field/value 两两配对）
redis-cli --raw ZRANGE <key> 0 -1 WITHSCORES       # zset（score→value 两两配对）

# 写入 / 删除 / 大小
redis-cli SET <key> <value> [EX <seconds>]         # 校验返回 OK
redis-cli DEL <key> [key...]
redis-cli DBSIZE
```
