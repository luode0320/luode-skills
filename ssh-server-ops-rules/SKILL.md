---
name: ssh-server-ops-rules
description: >-
  SSH 远程服务器运维规则。支持多服务器连接管理、命令执行、文件传输、系统监控、
  服务管理、日志查看等 Linux/Unix 服务器运维场景。核心特性是「凭证引导」：用户
  只需提供一次服务器用户名/密码，agent 自动在 C:\Users\luode\.ssh 下生成 ed25519
  密钥对，通过密码首连把公钥推送到服务器 authorized_keys，后续全部走密钥认证，
  密码用后即弃、不落盘。当用户提到"ssh 连接/执行/上传/下载/监控/服务/日志"、
  "连一下服务器"、"远程服务器"、"服务器运维"、"登录服务器"、"给服务器配密钥"、
  "服务器上跑命令"时触发。
---

# SSH 远程服务器运维

> SSH 远程服务器管理工具，支持多服务器连接管理、命令执行、文件传输、系统监控、服务管理、日志查看等 Linux/Unix 服务器运维。凭证策略：**密码只用一次（首次推公钥），之后全部密钥认证**。

## 何时使用（触发条件）

- 用户提到 `ssh 连接 / 执行 / 上传 / 下载 / 监控 / 服务 / 日志` 等运维动作，指向 Linux/Unix 服务器。
- 用户提供服务器 `用户名/密码`，要求连接或执行操作。
- 用户说"连一下服务器""登录服务器""在服务器上跑命令""给服务器配一下免密登录"。
- 用户要求批量操作多台服务器。

如果只是解释 SSH 原理、不涉及实际连接，则只说明、不落盘、不生成密钥。

## 能力清单

| 功能 | 说明 |
| --- | --- |
| 🔌 凭证引导 | 用户给用户名/密码 → 自动生成密钥对 → 推送公钥 → 配置落盘 → 密钥认证 |
| 💻 命令执行 | 远程单条/多条/批量命令执行，返回退出码与输出 |
| 📤 文件上传 | scp 上传文件或目录到服务器 |
| 📥 文件下载 | scp 从服务器下载文件或目录 |
| ⚙️ 服务管理 | systemctl 启停/状态/开机自启 |
| 📋 日志查看 | journalctl、tail -f、按服务/关键字过滤 |
| 📊 系统监控 | CPU/内存/磁盘/负载/进程/网络快照 |

## 凭证模型（核心规则）

1. **密码用后即弃**：密码只存在于首次连接的进程内存（脚本参数或环境变量）中，公钥推送成功后立即丢弃，**任何配置文件、日志、会话记录都不得写入密码**。
2. **每主机一钥**：密钥文件按服务器别名命名 `id_ed25519_<alias>`，隔离性好，单台泄露不影响其他服务器。
3. **统一落点**：密钥与服务器配置默认存 `C:\Users\luode\.ssh\`（Windows），Linux/macOS 为 `~/.ssh/`。后续连接一律 `ssh -i <keyPath>`，不再需要密码。
4. **配置不含密码**：`servers.json` 只存 `alias / host / port / user / keyPath`，密码永不落盘。

## 首次接入流程（摘要）

完整步骤与异常处理见 `references/credential-guide.md`。

1. 收集：`alias`（缺省由 host 推断）、`host`、`port`（默认 22）、`username`、`password`。
2. 检查密钥：`C:\Users\luode\.ssh\id_ed25519_<alias>` 已存在则复用，不存在则生成：
   ```bash
   ssh-keygen -t ed25519 -f "C:\Users\luode\.ssh\id_ed25519_<alias>" -N "" -C "luode@<alias>"
   ```
3. 推送公钥（唯一需要密码的步骤）：
   ```bash
   node scripts/push_pubkey.js --host <host> --port <port> --user <username> --pubkey "C:\Users\luode\.ssh\id_ed25519_<alias>.pub"
   # 密码通过环境变量 SSH_PASSWORD 传入，避免出现在命令行/进程列表
   ```
4. 验证：`ssh -i "C:\Users\luode\.ssh\id_ed25519_<alias>" -p <port> <username>@<host> "echo ok && uname -a"`，失败则回到步骤 3 排查。
5. 配置落盘：把条目写入 `C:\Users\luode\.ssh\servers.json`（schema 见 credential-guide.md）。

> Windows 注意：OpenSSH 客户端对私钥权限敏感，若报 `UNPROTECTED PRIVATE KEY FILE`，用 `icacls` 收紧权限（见 credential-guide.md「常见错误」）。

## 日常使用规则

连接统一走密钥认证。以下命令模板中的 `<keyPath>/<user>/<host>/<port>` 一律从 `servers.json` 读取，禁止要求用户重复提供密码。

### 目标服务器解析（多服务器路由）

用户消息中若未给出完整 host，按以下优先级从 `servers.json` 解析目标，**唯一命中才执行，歧义必问询，禁止猜测**：

| 优先级 | 匹配方式 | 示例 |
| --- | --- | --- |
| ① | `alias` 精确匹配 | "去 api 那台" → alias=`api` |
| ② | `host` 精确匹配 | "连 10.38.1.20" → host=`10.38.1.20` |
| ③ | `host` 结尾匹配（IP 片段） | "5.211 那台" → host **以** `5.211` **结尾**，如 `10.0.5.211` |
| ④ | 仅登记一台 | servers.json 只有 1 条 → 直接用，无需指认 |

- 多台命中 / 零命中：列出 `servers.json` 全部条目（`alias | host | port | user`），请用户指定后再执行。
- 用户只说"连服务器/看服务器"且登记多台：同样先列清单，不默认选第一台。
- 执行前在回复中显式声明目标：`→ 目标: <alias> (<host>:<port>)`，供用户执行前校验。

| 动作 | 命令模板 |
| --- | --- |
| 执行命令 | `ssh -i <keyPath> -p <port> <user>@<host> "<cmd>"` |
| 批量执行 | 对 servers.json 中多个条目循环执行同一命令，逐台返回结果 |
| 上传文件 | `scp -i <keyPath> -P <port> <local> <user>@<host>:<remote>` |
| 下载文件 | `scp -i <keyPath> -P <port> <user>@<host>:<remote> <local>` |
| 服务状态 | `ssh -i <keyPath> ... "systemctl status <svc> --no-pager"` |
| 服务启停 | `ssh -i <keyPath> ... "sudo systemctl restart <svc>"`（需要 sudo 时先确认） |
| 查看日志 | `ssh -i <keyPath> ... "journalctl -u <svc> -n 100 --no-pager"` |
| 实时日志 | `ssh -i <keyPath> ... "tail -f /var/log/<file>"`（超时控制 10s 内停止） |
| 系统监控 | `ssh -i <keyPath> ... "uptime && free -h && df -h && top -bn1 | head -20"` |

## 安全规则

### 危险命令分级（root 权限下的行为边界）

服务器可能以 root 身份登录（agent 有能力执行任何命令），因此边界必须来自规则本身。按危险度分两级：

**L1 硬禁止**（默认拒绝执行，即使目标已确认；唯一豁免：用户在当前轮消息中逐字给出完整命令原文，且仅对那一条命令生效）：

- 删除根/系统关键路径：`rm -rf /`、`rm -rf /*`、`rm -rf /etc`、`/usr`、`/var`、`/boot`、`/home`（含等价变体如 `rm -rf /etc/`、带通配符的根路径删除）。
- 磁盘格式化/覆写：`mkfs.*`、`fdisk`/`parted` 写盘操作、`dd` 写入 `/dev/sd*` 等块设备。
- 清空关键文件/设备：`> /etc/passwd`、`echo ... > /dev/sd*`、`shred` 覆写系统路径。
- 数据库删库/清库：`DROP DATABASE`、`TRUNCATE`（需逐表确认）、`FLUSHALL`（redis）、`mongo --eval "db.dropDatabase()"`。
- 内核危险操作：直接写 `/proc/sys` 关键项（如 `drop_caches`）、`echo > /dev/mem`。

**L2 需确认**（执行前必须：① 声明目标服务器 `→ 目标: <alias> (<host>:<port>)`；② 向用户确认目标与影响范围；③ 高危类先做无害预览）：

- `rm -rf`/`rm` 删除具体路径（非 L1 根路径）。
- `sudo` 提权命令。
- 生产环境服务 `systemctl restart/stop`（`status` 无需确认）。
- 覆盖/替换配置文件、修改防火墙规则（`iptables`/`ufw`）。
- DDL 变更：`DROP TABLE`、`ALTER TABLE`（单表）。
- 批量执行中对多台服务器的写操作。

### 通用规则

- 私钥文件权限：Windows 用 `icacls ... /inheritance:r /grant:r "%USERNAME%:R"`；Linux/macOS 用 `chmod 600`。
- 公钥推送目标权限：远端 `~/.ssh` 为 700、`authorized_keys` 为 600（脚本已处理，人工操作时遵守）。
- 密码输入优先走环境变量（`SSH_PASSWORD`）或交互式输入，避免命令行明文暴露。
- 禁止把 `servers.json`、私钥内容、密码提交到任何 Git 仓库或聊天记录。
- 任何远程命令执行前，回复必须先声明目标服务器（`→ 目标: <alias> (<host>:<port>)`），确保连的是用户想连的那台。
- 日常只读运维命令（`systemctl status`、`journalctl`、`df`、`uptime`、`free`、`ps`、`top` 快照）白名单放行，无需逐条确认。

## References

- `references/credential-guide.md` — 凭证引导完整流程、servers.json schema、常见错误处理
- `scripts/push_pubkey.js` — 密码首连推送公钥脚本（Node + ssh2）
