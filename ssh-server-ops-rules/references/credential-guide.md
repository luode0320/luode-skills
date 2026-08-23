# 凭证引导完整流程

> 本文档定义「用户提供用户名/密码 → 密钥认证常驻」的完整操作细节。SKILL.md 只保留摘要，细节以本文为准。

## 1. 凭证模型

| 项 | 位置 | 说明 |
| --- | --- | --- |
| 私钥 | `C:\Users\luode\.ssh\id_ed25519_<alias>` | 每主机一钥，权限收紧 |
| 公钥 | `C:\Users\luode\.ssh\id_ed25519_<alias>.pub` | 推送到服务器 `~/.ssh/authorized_keys` |
| 服务器配置 | `C:\Users\luode\.ssh\servers.json` | 只存连接信息，**不含密码** |
| 密码 | 仅存在于首次连接进程内存 | 推送公钥成功后即弃 |

> 非 Windows 环境（Linux/macOS）把 `C:\Users\luode\.ssh` 替换为 `~/.ssh`。

## 2. 首次接入详细步骤

### 步骤 1：收集连接信息

| 参数 | 是否必填 | 缺省规则 |
| --- | --- | --- |
| `alias` | 否 | 域名取主域（`api.example.com` → `api`）；IP 把 `.` 换成 `-`（`192.168.1.100` → `192-168-1-100`）；用户指定则用指定值 |
| `host` | 是 | — |
| `port` | 否 | 22 |
| `username` | 是 | — |
| `password` | 是 | 仅首次需要 |

### 步骤 2：检查/生成密钥对

```bash
# 已存在则复用，不重复生成
ls "C:\Users\luode\.ssh\id_ed25519_<alias>" 2>/dev/null || \
ssh-keygen -t ed25519 -f "C:\Users\luode\.ssh\id_ed25519_<alias>" -N "" -C "luode@<alias>"
```

Windows 上生成后立即收紧私钥权限（否则 OpenSSH 拒绝使用）：

```bash
icacls "C:\Users\luode\.ssh\id_ed25519_<alias>" /inheritance:r /grant:r "%USERNAME%:R"
```

### 步骤 3：密码首连推送公钥

本机依赖已预置（2026-08-22 验证）：`ssh2` 已装入 managed Node 工作区，运行脚本时设置 `NODE_PATH` 即可：

```bash
NODE_PATH="C:/Users/luode/.workbuddy/binaries/node/workspace/node_modules" \
"C:/Users/luode/.workbuddy/binaries/node/versions/22.22.2/node.exe" \
  scripts/push_pubkey.js --host <host> --port <port> --user <username> \
  --pubkey "C:\Users\luode\.ssh\id_ed25519_<alias>.pub"
```

若在其他环境运行（依赖未装），一次性安装：

```bash
cd "D:\谷歌云盘\luode-skills\ssh-server-ops-rules"
npm install ssh2   # 或全局安装后设置 NODE_PATH
```

执行推送（密码走环境变量，不落命令行）：

```bash
SSH_PASSWORD='<password>' node scripts/push_pubkey.js \
  --host <host> --port <port> --user <username> \
  --pubkey "C:\Users\luode\.ssh\id_ed25519_<alias>.pub"
```

脚本行为（幂等）：

1. 用 password 认证建立 SSH 连接（readyTimeout 30s）。
2. 读取本地公钥文件内容。
3. 远端执行：`mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys`。
4. 检查 `authorized_keys` 是否已包含该公钥；已包含则跳过（幂等），否则追加并换行。
5. 关闭连接，退出码 0 表示成功。

### 步骤 4：验证密钥登录

```bash
ssh -i "C:\Users\luode\.ssh\id_ed25519_<alias>" -p <port> -o StrictHostKeyChecking=accept-new \
  <username>@<host> "echo ok && uname -a"
```

- 成功：进入步骤 5。
- 失败（认证失败）：检查公钥是否真的追加成功（可临时用密码连一次 `cat ~/.ssh/authorized_keys` 核对）、服务器 `sshd_config` 是否允许密钥认证（`PubkeyAuthentication yes`）。
- 首次连接出现 host key 确认提示：用 `-o StrictHostKeyChecking=accept-new` 自动接受并写入 `known_hosts`。

### 步骤 5：配置落盘

读取 `C:\Users\luode\.ssh\servers.json`（不存在则初始化），按 alias 追加或更新条目：

```json
{
  "servers": [
    {
      "alias": "api",
      "host": "api.example.com",
      "port": 22,
      "user": "root",
      "keyPath": "C:\\Users\\luode\\.ssh\\id_ed25519_api"
    }
  ]
}
```

写入后回读校验 JSON 可解析、条目完整。**此文件禁止包含 password 字段**。

## 3. servers.json Schema

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `alias` | string | 是 | 唯一标识，密钥命名与命令引用都用它 |
| `host` | string | 是 | IP 或域名 |
| `port` | number | 否 | 默认 22 |
| `user` | string | 是 | 登录用户名 |
| `keyPath` | string | 是 | 私钥绝对路径（Windows 用双反斜杠或正斜杠） |

## 3.5 多服务器目标解析（路由规则）

用户指认目标时按以下优先级解析，**唯一命中才执行，歧义必问询，禁止猜测**：

| 优先级 | 匹配方式 | 示例 |
| --- | --- | --- |
| ① | `alias` 精确匹配 | "去 api 那台" → `alias=api` |
| ② | `host` 精确匹配 | "连 10.38.1.20" → `host=10.38.1.20` |
| ③ | `host` 结尾匹配 | "5.211 那台" → `host` **以** `5.211` **结尾**（如 `10.0.5.211`、`172.16.5.211`） |
| ④ | 仅登记一台 | servers.json 只有 1 条 → 直接使用，无需指认 |

规则细节：

- **结尾匹配语义**：用户给出 IP 片段时，匹配 `host` 字符串以该片段结尾的条目；片段不含端口、不含前导点（`5.211` 而非 `.5.211`）。
- **多台命中 / 零命中**：列出 `servers.json` 全部条目（`alias | host | port | user`），请用户指定后再执行；用户只说"连服务器"且登记多台时同样先列清单，不默认选第一台。
- **执行前声明**：任何远程命令执行前，回复先声明 `→ 目标: <alias> (<host>:<port>)`，供用户执行前校验。
- **批量执行**：只有用户明确表达"全部/每台/批量"时才循环多台；单数表述一律走单目标解析。

## 4. 常见错误处理

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `UNPROTECTED PRIVATE KEY FILE` | Windows 私钥权限过宽 | `icacls "<keyPath>" /inheritance:r /grant:r "%USERNAME%:R"` |
| `Permission denied (publickey,password)` | 公钥未推送成功 / 认证方式被禁 | 核对 `authorized_keys` 内容；检查远端 `sshd_config` 的 `PubkeyAuthentication` |
| `Connection timed out` | 网络/防火墙 | 检查端口可达（`Test-NetConnection <host> -Port <port>`），确认安全组放行 |
| `Host key verification failed` | known_hosts 无记录或记录变化 | 确认服务器无误后 `-o StrictHostKeyChecking=accept-new` 或清理旧记录 |
| `bash: <cmd>: command not found` | 命令不在远端 PATH | 用绝对路径或先 `export PATH=...`；sudo 命令检查 `sudo -n` 免密可用性 |
| 脚本报 `Cannot find module 'ssh2'` | 依赖未安装 | `npm install ssh2`；或设 `NODE_PATH` 指向已装 ssh2 的 node_modules |

## 5. 安全红线

- 密码只允许出现在 `SSH_PASSWORD` 环境变量或进程参数中，推送完成立即清除 shell 会话内变量；不得写入文件、日志、聊天记录、`servers.json`。
- 私钥、`servers.json`、`known_hosts` 属于敏感文件，禁止进入 Git 仓库（如仓库恰好在 Google Drive 同步目录，注意同步范围）。
- 服务器下线/密钥轮换时：删除 `servers.json` 对应条目与本地私钥文件，避免遗留过期资产。

### 5.1 危险命令分级执行细则

**L1 硬禁止**（默认拒绝，唯一豁免 = 用户当前轮逐字给出完整命令原文，仅单条生效）：

| 类别 | 命令示例 | 说明 |
| --- | --- | --- |
| 根/系统路径删除 | `rm -rf /`、`rm -rf /etc`、`rm -rf /usr`、`rm -rf /*` | 含等价变体：带通配符、带尾部斜杠 |
| 磁盘格式化/覆写 | `mkfs.ext4 /dev/sdb`、`dd if=... of=/dev/sda`、`fdisk` 写盘 | 块设备级操作，不可逆 |
| 清空关键文件 | `> /etc/passwd`、`echo 1 > /dev/sda`、`shred` 系统路径 | 直接破坏系统文件/设备 |
| 删库/清库 | `DROP DATABASE`、`TRUNCATE`、`FLUSHALL`、`db.dropDatabase()` | 数据不可恢复 |
| 内核危险写 | `echo 1 > /proc/sys/vm/drop_caches`、写 `/dev/mem` | 影响系统稳定性 |

L1 豁免判定模板：用户消息中出现完整命令原文（如 `rm -rf /var/tmp/build-cache`）且不落入 L1 模式时，按 L2 处理；落入 L1 模式（如 `rm -rf /`）时，即使原文出现也拒绝并解释原因。

**L2 需确认**（三步：声明目标 → 说明影响 → 用户确认）：

- 执行前：`→ 目标: <alias> (<host>:<port>)` + 命令影响说明（删什么、改什么、影响面）。
- 无害预览：`rm`/`rm -rf` 前先 `ls -la <path>` 确认路径真实存在且非根；`dd`/`mkfs` 前先 `lsblk` 核对设备号；`iptables` 改动前先 `iptables -L -n` 备份现状。
- 生产服务重启：先 `systemctl status <svc>` 看当前状态再确认操作。

**白名单放行**（无需确认）：`systemctl status`、`journalctl`、`tail`、`cat`、`ls`、`df`、`du`、`free`、`uptime`、`ps`、`top -bn1`、`uname`、`whoami`、`hostname`、`ss -tlnp`、`netstat -tlnp` 等只读命令。
