# 吸收裁决表（workbuddy-absorption-map）

> 归属：`redis-usage-rules`。记录外部 skill 精华的吸收裁决，来源可回指，每行含「整理去重」列。

## self-dev-redis__skillhub（2026-08-19 吸收）

**来源**：本地安装 `C:\Users\luode\.workbuddy\skills\self-dev-redis__skillhub`（skillhub 安装，v3.0.3，MIT-0，SKILL.md 31 行极简无 references + `scripts/script.sh` 657 行 bash，15 个子命令）。仓库内另有同步副本 `D:\谷歌云盘\luode-skills\self-dev-redis__skillhub`（同一安装的两个落点，哈希一致、installedAt 相同）。

**裁决结果**：合并 16 条 / 保留本地 4 条 / 拒绝 3 条。

| 外部精华 | 裁决 | 落点 | 整理去重 |
|---------|------|------|---------|
| R1 连接构建（REDIS_HOST/PORT/DB/PASSWORD 环境变量 + `-a` 密码 + `--no-auth-warning`） | 合并 | `references/redis-usage-and-commands.md` 一、连接约定 | 本地此前无 Redis 连接约定，纯新增 |
| R2 连通性校验（PING→PONG，失败三分诊） | 合并 | 同一、连接约定 | 纯新增 |
| R3 环境预检（redis-cli 缺失 → 分平台安装指引） | 合并 | `references/redis-monitoring-backup-and-safety.md` 一、安装指引 | 补充 Windows 走 WSL 适配（本地 `wsl-service-deploy` 仅覆盖服务部署，不覆盖 cli 安装） |
| R4 类型自动识别读取（TYPE 分发五大数据类型） | 合并 | `redis-usage-and-commands.md` 二、类型自动识别读取 | 纯新增 |
| R5-R9 各类型读法（GET/LLEN+LRANGE/SCARD+SMEMBERS/HLEN+HGETALL/ZCARD+ZRANGE WITHSCORES，超 100 条截断） | 合并 | 同上 | 合并为一张映射表，不逐类型重复展开 |
| R10 TTL 语义（-2 不存在 / -1 永久 / 正整数剩余秒） | 合并 | 同上二、TTL 语义 | 纯新增 |
| R11-R14 写入/删除/列举/大小（SET 透传校验 OK / DEL 按返回值区分 / KEYS 对齐列表 / DBSIZE） | 合并 | 同上三 | 四类操作合并为一张表 |
| R15-R18 监控判读（MONITOR/INFO 提炼/STATS 命中率·碎片率·ops/SLOWLOG） | 合并 | `redis-monitoring-backup-and-safety.md` 二、监控判读 | 统计口径收敛为一张指标表；补充生产实例 MONITOR/KEYS 需确认的本地红线 |
| R19-R20 备份导出/导入格式（`TYPE\|key\|ttl\|值` 单行格式，五类序列化，# SKIP 跳过行） | 合并 | 同上三、备份导出/导入格式 | 导出/导入重建映射合并描述，不复制外部脚本实现 |
| R21 危险操作双确认（FLUSHDB 前展示 DBSIZE，必须键入 `YES FLUSH`） | 合并 | 同上四、危险操作安全红线 | 扩展为 FLUSHDB/批量 DEL/生产实例三类红线 |
| R22 操作日志审计（时间戳 + 摘要） | 合并 | 同上五、操作日志审计 | 日志落点改为项目约定，不搬 `~/.local/share/redis-helper` 专属路径 |
| R23 输出规范（✓/!/✗ 前缀、100 条截断、字节自动换算） | 合并 | `redis-usage-and-commands.md` 四、输出规范 | 纯新增 |
| 业务侧不直建 Redis 客户端，走 database/connection/ 目录位点 | 保留本地 | `package-structure-rules`（已有 Redis 目录位点约定） | 不重复定义，SKILL.md 权责边界交叉引用 |
| 缓存 key 设计/过期策略/并发保护 | 保留本地 | `project-local-skills-rules` 项目级 `redis-usage-rules` 主题（scope-and-splitting.md:24） | 不重复定义，SKILL.md 权责边界显式互斥 |
| SQL/GORM 访问规则 | 保留本地 | `database-query-rules`（更强） | 不重复定义 |
| 本地通用规范（可读性/命名等） | 保留本地 | `code-generation-style-rules` 等编码基线域 | 不重复定义 |
| 657 行 bash 脚本整套 CLI 工作流 | 拒绝 | — | 铁律禁复制外部整套工作流；Windows 无官方 redis-cli，脚本不可直接复用 |
| `~/.local/share/redis-helper` 专属存储形态 | 拒绝 | — | 宿主无关机制形态，日志落点改为项目约定 |
| SKILL.md 宣称的"配置 lint" | 拒绝 | — | 源脚本实际无 CONFIG 子命令，名实不符；仅以 SLOWLOG 阈值核对（`CONFIG GET slowlog-log-slower-than`）作为配置检查入口 |

**整理去重统计**：本地此前无 Redis 运维操作规则，本次净增 1 个新 skill 目录（SKILL.md + 4 references，约 240 行）。通过与 `package-structure-rules`、`project-local-skills-rules`、`database-query-rules`、编码基线域交叉引用实现净增最小化；五类读法合并为映射表、四类写操合并为一张表，未逐条复制外部脚本实现。

**已删除源**：已删除（2026-08-19）。`C:\Users\luode\.workbuddy\skills\self-dev-redis__skillhub` 与 `D:\谷歌云盘\luode-skills\self-dev-redis__skillhub`（同一次安装的两个落点，哈希一致）；删除前已备份至 `C:\Users\luode\.workbuddy\plans\redis-src-backup-20260819\`（zip 各 6 文件，解压校验通过），详见 `source-notes.md`。
