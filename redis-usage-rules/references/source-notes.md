# 来源记录（source-notes）

> 归属：`redis-usage-rules`。记录外部吸收来源与落点，保证可追溯。

## self-dev-redis__skillhub（2026-08-19 吸收）

- **来源名称**：self-dev-redis（Redis 数据库操作）
- **来源形态**：skillhub 市场安装包（`C:\Users\luode\.workbuddy\skills\self-dev-redis__skillhub`，SKILL.md 31 行 + `scripts/script.sh` 657 行 bash）
- **来源版本**：v3.0.3；安装时间 2026-08-19 23:10:57（installedAt 1787152257393）
- **来源 URL**：skillhub 本地安装；作者 BytesAgain，`_skillhub_meta.json` 记录 source: skillhub，license MIT-0
- **吸收日期**：2026-08-19
- **落点**（新建独立 skill `redis-usage-rules/`，用户已确认）：
  - `SKILL.md`（主文件，仿 `database-query-rules` 结构）
  - `references/redis-usage-and-commands.md`（连接约定 / 类型识别读取 / 键健康检查 / 写入删除 / 输出规范）
  - `references/redis-monitoring-backup-and-safety.md`（监控判读 / 备份导出导入格式 / 危险操作红线 / 安装指引 / 日志审计）
  - `references/workbuddy-absorption-map.md`（吸收裁决表）
- **裁决依据**：只吸收规则与 redis-cli 命令清单（用户已确认），不转写 657 行 bash 脚本；FLUSHDB 双确认、凭据环境变量传递等安全红线原样吸收并扩展为本地红线；生产实例 MONITOR/KEYS 需确认、Windows 走 WSL 为本地补充适配。
- **已删除源**：已删除（2026-08-19）`C:\Users\luode\.workbuddy\skills\self-dev-redis__skillhub` 与仓库同步副本 `D:\谷歌云盘\luode-skills\self-dev-redis__skillhub`（同一次安装的两个落点，哈希一致）。删除前备份至 `C:\Users\luode\.workbuddy\plans\redis-src-backup-20260819\self-dev-redis-user-c.zip` / `self-dev-redis-repo-d.zip`（各 6 文件，解压校验通过）。
- **状态**：已吸收，源 skill 已删除。
