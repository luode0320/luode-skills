---
name: linux
description: "Linux 系统运维与排障：权限陷阱（chmod/chown/umask/ACL）、进程管理（kill/nohup/zombie）、文件系统（rm 安全/符号链接/inode）、磁盘空间排查（lsof/journalctl/docker）、网络（防火墙/端口/ss）、SSH 排障（权限/known_hosts）、systemd 服务、cron、内存与 OOM。适用于排查磁盘满、服务起不来、SSH 连不上、进程杀不掉、OOM 问题场景。触发词：linux、linux 报错、磁盘满、df、空间不足、服务起不来、systemctl、systemd、journalctl、ssh 连不上、权限不足、chmod、chown、进程杀不掉、kill、zombie、OOM、内存不足、cron 不执行、防火墙、端口占用、inode 满。"
license: MIT
metadata:
  displayName: "Linux 运维与排障"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# Linux 运维与排障

Linux 系统排障与正确操作手册。**先走「工作流」再查「知识区」**：磁盘满、服务异常、SSH 失败、进程管理各有固定排查流程；陷阱细节按主题知识区深入。

## 工作流

### 磁盘满排查流程
1. `df -h` 定位满的挂载点。
2. 空间被删文件占用：`lsof +L1` 找被进程持有但已删除的文件 → 重启对应进程释放。
3. 系统日志占用：`journalctl --vacuum-size=500M`；`du -sh /var/log/*` 找大日志。
4. 容器空间：`docker system prune -a`（确认后执行）。
5. inode 满（`df -i` 100% 但空间有）：大量小文件问题，`find /path -type f | wc -l` 定位目录。
6. **验证**：`df -h` 确认空间恢复。

### 服务起不来排查流程
1. `systemctl status <svc>` 看状态与错误（Active/Inactive/Failed）。
2. `journalctl -u <svc> -n 50 --no-pager` 看具体报错。
3. 检查 `enable` 与 `start` 是否都执行（enable 不启动服务）。
4. 依赖网络：`After=network-online.target`（不是 network.target）+ `Wants=network-online.target`。
5. 崩溃不重启：unit 加 `Restart=on-failure`。
6. **验证**：`systemctl is-active <svc>` 返回 active；`restart` 后连接保持（优先 reload 保连接）。

### SSH 连不上排查流程
1. 权限：`~/.ssh` 目录 700、私钥 600（错误权限 = 静默认证失败）。
2. known_hosts 过期：服务器重建后报 hash 不匹配 → `ssh-keygen -R <host>`。
3. 配置匹配：`~/.ssh/config` Host 块**第一个匹配生效**——具体主机放通配符前面。
4. 空闲断连：加 `ServerAliveInterval 60`。
5. **验证**：`ssh -v <host>` 能看到认证成功；`ssh <host> 'echo ok'` 返回 ok。

### 进程管理流程
1. `ps aux | grep <name>` 定位 PID；`kill <pid>` 先发 SIGTERM（可被忽略，进程有机会清理）。
2. 等待数秒后 `ps` 复查；仍存活才 `kill -9`（跳过清理，可能丢数据）。
3. zombie 进程杀不掉：其父进程必须 `wait()` 或杀掉父进程，zombie 由 init 回收。
4. 后台任务保活：`nohup cmd &` 或 `disown`（`&` 单独用终端关闭即死）。
5. **验证**：`ps` 确认进程消失/状态符合预期。

## Permission Traps
- `chmod 777` fixes nothing, breaks everything — find the actual owner/group issue
- Setuid on scripts is ignored for security — only works on binaries
- `chown -R` follows symlinks outside target directory — use `--no-dereference`
- Default umask 022 makes files world-readable — set 077 for sensitive systems
- ACLs override traditional permissions silently — check with `getfacl`

## Process Gotchas
- `kill` sends SIGTERM by default, not SIGKILL — process can ignore it
- `nohup` doesn't work if process already running — use `disown` instead
- Background job with `&` still dies on terminal close without `disown` or `nohup`
- Zombie processes can't be killed — parent must call wait() or be killed
- `kill -9` skips cleanup handlers — data loss possible, use SIGTERM first

## Filesystem Traps
- Deleting open file doesn't free space until process closes it — check `lsof +L1`
- `rm -rf /path /` with accidental space = disaster — use `rm -rf /path/` trailing slash
- Inodes exhausted while disk shows space free — many small files problem
- Symlink loops cause infinite recursion — `find -L` follows them
- `/tmp` cleared on reboot — don't store persistent data there

## Disk Space Mysteries
- Deleted files held open by processes — `lsof +L1` shows them, restart process to free
- Reserved blocks (5% default) only for root — `tune2fs -m 1` to reduce
- Journal eating space — `journalctl --vacuum-size=500M`
- Docker overlay eating space — `docker system prune -a`
- Snapshots consuming space — check LVM, ZFS, or cloud provider snapshots

## Networking
- `localhost` and `127.0.0.1` may resolve differently — check `/etc/hosts`
- Firewall rules flushed on reboot unless saved — `iptables-save` or use firewalld/ufw persistence
- `netstat` deprecated — use `ss` instead
- Port below 1024 requires root — use `setcap` for capability instead
- TCP TIME_WAIT exhaustion under load — tune `net.ipv4.tcp_tw_reuse`

## SSH Traps
- Wrong permissions on ~/.ssh = silent auth failure — 700 for dir, 600 for keys
- Agent forwarding exposes your keys to remote admins — avoid on untrusted servers
- Known hosts hash doesn't match after server rebuild — remove old entry with `ssh-keygen -R`
- SSH config Host blocks: first match wins — put specific hosts before wildcards
- Connection timeout on idle — add `ServerAliveInterval 60` to config

## Systemd
- `systemctl enable` doesn't start service — also need `start`
- `restart` vs `reload`: restart drops connections, reload doesn't (if supported)
- Journal logs lost on reboot by default — set `Storage=persistent` in journald.conf
- Failed service doesn't retry by default — add `Restart=on-failure` to unit
- Dependency on network: `After=network.target` isn't enough — use `network-online.target`

## Cron Pitfalls
- Cron has minimal PATH — use absolute paths or set PATH in crontab
- Output goes to mail by default — redirect to file or `/dev/null`
- Cron uses system timezone, not user's — set TZ in crontab if needed
- Crontab lost if edited incorrectly — `crontab -l > backup` before editing
- @reboot runs on daemon restart too, not just system reboot

## Memory and OOM
- OOM killer picks "best" victim, often not the offender — check dmesg for kills
- Swap thrashing worse than OOM — monitor with `vmstat`
- Memory usage in `free` includes cache — "available" is what matters
- Process memory in `/proc/[pid]/status` — VmRSS is actual usage
- cgroups limit respected before system OOM — containers die first

## Commands That Lie
- `df` shows filesystem capacity, not physical disk — check underlying device
- `du` doesn't count sparse files correctly — file appears smaller than disk usage
- `ps aux` memory percentage can exceed 100% (shared memory counted multiple times)
- `uptime` load average includes uninterruptible I/O wait — not just CPU
- `top` CPU percentage is per-core — 400% means 4 cores maxed

## 适用边界

**何时用**：Linux 系统排障（磁盘/服务/SSH/进程/OOM）、权限与文件系统操作、systemd/cron 管理。

**何时不用**：
- Windows 系统操作 → 转 `windows-powershell-environment-rules`、`windows-encoding-rules`；
- 容器/Docker 内部编排 → 转 `docker__skillhub`、`docker-direct-deploy`；
- 远程服务器批量运维/连接管理 → 转 `ssh-server-ops-rules`；
- Bash/PowerShell 脚本语义 → 转 `bash__skillhub`、`powershell__skillhub`。

## 验收清单

- [ ] 排障已按对应「工作流」逐步执行（磁盘/服务/SSH/进程）
- [ ] `kill` 先 SIGTERM 后 SIGKILL；无滥用 `kill -9`
- [ ] `chmod 777` / `chown -R` 未作为通用手段（已定位真实 owner/权限问题）
- [ ] 服务改动后 `systemctl is-active` 验证；unit 已考虑 `Restart=on-failure`
- [ ] SSH 已检查目录/私钥权限与 known_hosts
- [ ] `rm -rf` 路径书写谨慎（无意外空格/尾斜杠陷阱）
