# 改动前备份与可还原完整规程

> SKILL.md 只保留强制摘要，本文是唯一细则来源。
> **核心原则：无还原点，不改动（No restore point, no change）。**
>
> 服务器操作一定会有意外。agent 可能执行失败、可能执行成功但效果不符预期、用户也可能事后要求撤销。
> 因此凡是会改变服务器状态的写操作，**执行前必须先建立可验证的还原点**，且任何时刻都能回到 agent 改动之前的状态。

## 1. 核心原则

| # | 原则 | 含义 |
| --- | --- | --- |
| 1 | 先备份，后改动 | 写操作开始前，还原点必须已创建并验证通过；没有可用还原点不得动手 |
| 2 | 失败即回滚 | agent 执行失败或效果不符预期时，**主动**回滚到改动前状态，不等待用户开口 |
| 3 | 可验证 | 备份必须存在、非空、可读；回滚后必须验证已真正恢复 |
| 4 | 不叠加 | 不把多个不可逆操作串成一步；每步独立可回滚 |
| 5 | 留痕 | 还原点清单落盘并回报用户（ID、备份对象、一键回滚命令） |
| 6 | 不假设 | 现状必须真实探查（`ls`、`systemctl status`、`docker inspect`），不得凭记忆或推测 |

## 2. 适用范围

### 2.1 必须先建还原点（写操作）

| 类别 | 典型操作 |
| --- | --- |
| 文件/目录 | 新增、修改、删除、移动、重命名、权限变更（`chmod`/`chown`） |
| 配置文件 | 任何 `*.conf`、`*.yml`、`*.json`、`*.env` 内容变更 |
| 服务 | `systemctl start/stop/restart/reload/enable/disable` |
| 软件包 | `apt/yum/dnf/pip/npm` 安装、卸载、升级 |
| 数据库 | DDL（建/改/删表）、批量 DML、导入导出 |
| 容器 | `docker run/rm/stop`、镜像拉取替换、卷与网络操作、`docker compose up/down` |
| 网络与安全 | `iptables`/`ufw`/`firewalld` 规则变更、`sysctl` 调整 |
| 系统配置 | `cron`、用户与用户组、`sudoers`、环境变量、开机项 |
| 其他 | 任何 `sudo` 前缀的写入动作 |

### 2.2 免还原点（只读白名单）

`ls`、`cat`、`head`、`tail`、`df`、`du`、`free`、`uptime`、`ps`、`top -bn1`、`uname`、`whoami`、`hostname`、`ss -tlnp`、`netstat -tlnp`、`systemctl status`、`journalctl`、`docker ps`、`docker inspect`、`docker logs` 等不改变状态的命令。

### 2.3 例外与边界

- **用户当轮显式豁免**：用户明确说"不用备份，直接改"时，必须在回复中显式声明「本次无还原点」并由用户确认后方可执行；该豁免只对当轮那条改动生效，不跨轮继承。
- **L1 硬禁止命令**：不因"已备份"而放行，仍按 SKILL.md 的 L1 规则拒绝。
- **纯诊断/纯查询**：不产生写入，不建还原点。
- **磁盘空间不足**：先 `df -h` 评估；空间不足以完成备份时**禁止强行改动**，先报告并请用户处置。

## 3. 还原点 ID 与落点

| 项 | 值 |
| --- | --- |
| 还原点 ID | `RP-<alias>-<YYYYMMDDTHHMMSSZ>`（UTC，例：`RP-cpa-server-20261011T091530Z`） |
| 远端根目录 | `~/.agent-backups/<TS>/`（权限 700） |
| 本地镜像（可选） | `C:\Users\luode\.ssh\backups\<alias>\<TS>\`（仅关键配置，用 scp 拉回） |

远端目录结构：

```
~/.agent-backups/20261011T091530Z/
├── manifest.md     # 还原点清单（人可读，含每项回滚动作）
├── rollback.sh     # 一键回滚脚本（按记录顺序逆序还原）
├── paths.list      # 本次备份的原始路径列表
├── files/          # 文件级备份（cp -a 副本）
├── dirs/           # 目录级备份（tar.gz）
├── db/             # 数据库逻辑备份（dump）
├── docker/         # 容器 inspect / 镜像 tag 记录
└── misc/           # 防火墙、cron、包版本等文本快照
```

## 4. 备份策略矩阵

| 对象类型 | 备份（远端） | 还原 | 验证方式 |
| --- | --- | --- | --- |
| 单文件/配置 | `cp -a <f> <B>/files/<name>` | `cp -a <B>/files/<name> <f>` | `sha256sum` 与记录比对 |
| 目录 | `tar czf <B>/dirs/<name>.tar.gz -C <parent> <name>` | `rm -rf <dir> && tar xzf <B>/dirs/<name>.tar.gz -C <parent>` | `tar tzf` 能列出内容 |
| 目标不存在（新增场景） | 记录 `MISSING` | `rm -rf <path>` | 确认路径已不存在 |
| systemd 服务 | `systemctl is-active/is-enabled <svc>`；`cp -a /etc/systemd/system/<svc>.service <B>/misc/` | 还原 unit 文件 → `systemctl daemon-reload` → 恢复 active/enabled 状态 | `systemctl status <svc>` |
| 软件包 | `dpkg -l <pkg>` 或 `rpm -q <pkg>` 记录版本 | 新增的卸载；升级的按版本回退 | 版本号比对 |
| MySQL/MariaDB | `mysqldump --single-transaction <db> > <B>/db/<db>.sql` | `mysql <db> < <B>/db/<db>.sql` | 表数/行数比对 |
| PostgreSQL | `pg_dump <db> > <B>/db/<db>.sql` | `psql <db> < <B>/db/<db>.sql` | 同上 |
| Redis | `redis-cli --rdb <B>/db/dump.rdb`；关键配置 `CONFIG GET *` 导出 | 停服 → 替换 `dump.rdb` → 启服 | `redis-cli DBSIZE` |
| Docker 容器 | `docker inspect <c> > <B>/docker/<c>.json`；记录镜像 tag、端口、挂载、网络 | 按 inspect 记录重建容器 | `docker ps` + `docker inspect` 比对 |
| Docker 卷 | `docker run --rm -v <vol>:/v -v <B>/docker:/b alpine tar czf /b/<vol>.tar.gz -C /v .` | 反向解包回卷 | `docker run ... tar tzf` |
| 防火墙 | `iptables-save > <B>/misc/iptables.rules`；或 `ufw status verbose > <B>/misc/ufw.txt` | `iptables-restore < <B>/misc/iptables.rules` | `iptables -L -n` 比对 |
| cron | `crontab -l > <B>/misc/<user>.crontab` | `crontab < <B>/misc/<user>.crontab` | `crontab -l` 比对 |
| 用户/权限 | `getent passwd <u>`、`stat -c '%a %U:%G' <path>` 记录 | 按记录重建 | 重新比对 |

> `<B>` 指本次还原点目录 `~/.agent-backups/<TS>`。

## 5. 三阶段强制流程

### 阶段 1：改动前 —— 建立还原点

1. **侦察现状**：真实执行只读命令确认目标存在与当前状态，不得凭记忆。
2. **声明目标**：回复中给出 `→ 目标: <alias> (<host>:<port>)`。
3. **创建还原点**：优先使用 `scripts/backup_before_change.sh`（见第 6 节）；手工执行时按第 4 节矩阵逐项备份。
4. **验证备份**：`ls -l` 确认存在且非空；`tar tzf` 能列目录；`sha256sum` 可计算。
   **任一项验证失败即禁止继续改动。**
5. **生成清单**：写入 `manifest.md` 与 `rollback.sh`。
6. **回报用户**：还原点 ID、备份对象清单、一键回滚命令。

### 阶段 2：改动中 —— 保持可回滚

- 优先原子操作：用 `mv` 覆盖而非"先删后建"；用 `install`/`cp` 保留原文件后再切换。
- 分步执行，每步单独校验退出码；不把多个不可逆操作串成一条命令。
- 改动过程中**不得删除、覆盖、清理**本次或历史还原点。

### 阶段 3：改动后 —— 验证，失败即回滚

验证清单（按改动类型选取）：

| 改动类型 | 验证动作 |
| --- | --- |
| 服务 | `systemctl status <svc>` 为 active；端口 `ss -tlnp` 在听；`journalctl -u <svc> -n 50` 无新报错 |
| 配置文件 | 语法校验（`nginx -t`、`sshd -t`、`docker compose config` 等）；服务 reload 后无报错 |
| 应用 | 按业务做功能探测（HTTP 状态码、接口返回、页面可访问） |
| 数据库 | 目标表/库存在、行数合理、关键查询可执行 |
| 容器 | `docker ps` 状态为 Up、`docker logs` 无异常、端口可达 |
| 网络 | 规则生效且未切断当前 SSH 会话（改防火墙前务必先确认放行 22 端口） |

- **成功**：在 `manifest.md` 标记 `保留`，告知用户还原点位置与清理时机。
- **失败或未达预期**：立即执行第 7 节回滚流程。
- **回滚也失败**：停止一切后续改动，保留现场，按第 7.3 节报告。

## 6. 自动化脚本

`scripts/backup_before_change.sh`（本地运行，通过 SSH 在远端建还原点）：

```bash
bash scripts/backup_before_change.sh \
  --host <host> --port <port> --user <user> \
  --key "C:/Users/luode/.ssh/id_ed25519_<alias>" \
  --alias <alias> \
  --path /etc/nginx/nginx.conf \
  --path /root/app/config.yml \
  --path /root/app/data \
  --tag "nginx 配置调整"
```

脚本行为：

1. 生成 UTC 时间戳与还原点 ID。
2. 远端创建 `~/.agent-backups/<TS>/` 与子目录（权限 700）。
3. 上传路径清单，逐项备份（文件 `cp -a`、目录 `tar czf`、不存在记 `MISSING`）。
4. 生成 `manifest.md`（含原路径、类型、备份文件、大小、sha256、回滚动作）。
5. 生成并 `chmod +x` 一键回滚脚本 `rollback.sh`。
6. 输出还原点 ID、备份目录、manifest 路径与回滚命令。

退出码非 0 表示备份未完成，**禁止继续改动**。

## 7. 回滚操作规程

### 7.1 触发条件

- 命令非零退出，且未能在当步即时修复。
- 命令成功但验证不通过（服务未起、端口未听、功能异常、日志报错）。
- 用户要求撤销本次改动。

### 7.2 回滚步骤

1. **声明**：`→ 回滚还原点: RP-<alias>-<TS>（目标 <alias> <host>:<port>）`。
2. **查冲突**：确认改动期间用户或其他进程是否已产生新改动；若有，先向用户确认再回滚（避免覆盖新的有效变更）。
3. **执行**：`ssh -i <key> -p <port> <user>@<host> "bash ~/.agent-backups/<TS>/rollback.sh"`，或按 `manifest.md` 逐项手工还原。
4. **验证恢复**：服务状态、端口监听、配置文件哈希、功能探测全部回到改动前水平。
5. **报告**：回滚结果、已验证的恢复项、还原点是否保留。

### 7.3 回滚失败处理

- 立即停止后续所有改动，不得继续叠加。
- **保留现场**：不清理还原点、不删除半成品文件。
- 报告必须包含：已尝试的回滚动作、当前实际状态、与改动前状态的剩余差异、可用还原点位置。
- 给出手动恢复指引：从 `manifest.md` 逐项列出"原路径 → 备份文件 → 恢复命令"，便于用户或人工介入。
- 必要时建议用户从服务器快照/备份系统恢复（如云厂商快照）。

## 8. 保留与清理

- 还原点默认保留 **≥ 24 小时**，或保留至用户确认改动稳定。
- 清理需用户确认；清理前确认改动已稳定、无需再回滚。
- 清理只删除 `~/.agent-backups/` 下过期目录，不得使用宽泛通配符误删。

## 9. 安全与边界

- 备份目录权限 700；备份内容可能含密钥、口令、业务数据，**禁止**流入 Git 仓库或聊天记录。
- 备份前评估磁盘空间（`df -h`），空间不足先报告，不强行改动。
- 备份文件命名与路径避免单引号等特殊字符；脚本遇到异常字符应报错退出而非静默跳过。
- 回滚本身是"恢复到改动前状态"的降险动作，默认放行；但若会覆盖期间产生的新改动，必须先确认。
- L1 硬禁止命令即使以"回滚"名义出现，仍按 L1 处理。
