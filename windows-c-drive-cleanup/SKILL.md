---
name: windows-c-drive-cleanup
description: 清理 Windows C 盘（临时文件、开发工具缓存、回收站）与压缩 WSL ext4.vhdx 虚拟磁盘。当用户要求"清理 C 盘 / 释放磁盘空间 / C 盘满了 / WSL 占用过大 / vhdx 压缩"时使用。含只读扫描→用户确认→执行的安全流程，以及 luode 本机实测验证过的有效路径与坑点清单。
---

# Windows C 盘清理与 WSL vhdx 压缩

## 铁律（不可跳过）

1. **两步走**：先只读扫描出报告 → 用户确认范围后才执行删除。扫描阶段禁止删除/移动任何文件。
2. **缓存类删除 = 永久删除**（不走回收站，否则无法真正释放空间），必须在确认清单中向用户明示。
3. **禁动清单**：WSL ext4.vhdx 本体（禁删，只可压缩）、WSL 内 /home 项目数据、containerd/docker 数据、C:\Windows 系统目录、回收站（清空前先问）。
4. 全部完成后复核释放量，汇报前后对比。

## 第一步：只读扫描（PowerShell）

磁盘概况：

```powershell
$d = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
# FreeSpace/1GB = 剩余；Size-FreeSpace = 已用
```

目录大小统计。**坑：Get-ChildItem -Recurse 统计用户 Temp 会报 Win32Exception 且显示 0 MB 假数据**，改用 robocopy（只读列出，可信）：

```powershell
$out = robocopy '<目标目录>' 'C:\__stat_dummy__' /L /S /NJH /NFL /NDL /NP /BYTES /XJ /R:0 /W:0
# 中文系统找"字节:"行,第一个数字 = 总字节
```

扫描目标清单：

| 类别 | 路径 |
|---|---|
| 用户临时 | %LOCALAPPDATA%\Temp |
| 系统临时 | C:\Windows\Temp、C:\Windows\Prefetch（普通权限可能 N/A，报告标注即可） |
| 更新缓存 | C:\Windows\SoftwareDistribution\Download |
| 浏览器缓存 | %LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache；Edge 同构 |
| 开发缓存 | %LOCALAPPDATA%\npm-cache、%LOCALAPPDATA%\pip\cache、%USERPROFILE%\go\pkg\mod、%USERPROFILE%\.cargo\registry、%LOCALAPPDATA%\uv\cache、%LOCALAPPDATA%\pnpm、.gradle\.m2\.nuget（存在才统计） |
| 回收站 | C:\$Recycle.Bin |
| WSL 虚拟磁盘 | %LOCALAPPDATA%\Packages\*\LocalState\ext4.vhdx（只报告大小） |

报告产出：HTML 表格（分类/路径/大小/建议/风险分级：低=可重建缓存、中=浏览器缓存建议手动清、高=禁动项）→ present_files 打开 → AskUserQuestion 让用户勾选执行范围（多选：系统临时文件 / 开发缓存 / 回收站 / 全部扫描分析；执行方式：先报告 / 直接清安全项）。

## 第二步：执行清理（严格按用户确认的范围）

官方命令优先（比手删稳，自动处理只读权限）：

```powershell
go clean -modcache           # go\pkg\mod，go.exe 在 C:\Program Files\Go\bin\go.exe
npm cache clean --force
pip cache purge
uv cache clean
pnpm store prune
# cargo: 删 %USERPROFILE%\.cargo\registry\cache 子目录
```

Temp 清理：`Remove-Item -Recurse -Force -ErrorAction SilentlyContinue`（被占用文件自动跳过，不影响运行中程序）。分批执行，每批后可复核。

## WSL ext4.vhdx 压缩（2026-09-05 本机实测）

### ✅ 有效路径（首选，免管理员、零数据风险）

1. WSL 内清理（发行版名先 `wsl -l -q` 确认，常为 `Ubuntu` 而非 `Ubuntu-24.04`）：
   `wsl -d <发行版> -u root -- bash -c "<命令>"`
   - `apt-get clean`
   - `journalctl --rotate && journalctl --vacuum-size=50M`（**不先 rotate 直接 vacuum 会 freed 0B**）
   - 清 `~/.cache`、`/tmp`
   - 先 `du -xh -d1 /` 与 `du -xh -d1 /var/lib` 摸清分布，**确认不碰业务数据**；containerd/docker 数据默认不动
2. `fstrim -v /`（discard 标记全部空闲块）
3. `wsl --shutdown`
4. **重启电脑** → vhdmp 在挂载周期内自动回收空洞（实测 43.63 → 19.11 GB，回收 24.5 GB）
5. 验证：vhdx 文件大小、`df -h /`（内部数据应原样）、WSL 正常启动

### ❌ 无效路径（本机实测，勿再踩）

- `diskpart /s <脚本>`：静默失败（7-12 秒退出、无输出、无效果、拿不到日志）。`attach vdisk readonly` 后若未 detach 会锁死 vhdx（WSL 报 ERROR_SHARING_VIOLATION），重启解锁。
- `Optimize-VHD`：需管理员 + Hyper-V 模块；`Start-Process powershell/cmd -Verb RunAs` 会被 WorkBuddy 工具安全策略拦截（LOLBin 检测）；`Start-Process diskpart` 放行但拿不到输出，等于盲跑。
- `wsl --manage --set-sparse true`：WSL 2.7.12 起被微软禁用（数据损坏风险），禁止 `--allow-unsafe`。

### 🔧 兜底：export → unregister → import（仅当重启法无效）

```powershell
wsl --export <发行版> D:\wsl-backup\<名>.tar
# 铁律:tar 验证(文件大小 ≥ WSL 内 df used 量级 + tar -tf 抽查 home/<用户> 关键路径)通过前,禁止 unregister
wsl --unregister <发行版>
wsl --import <发行版> <新目录如 C:\Users\<user>\WSL\<名>> <tar> --version 2
# import 后默认用户变 root:/etc/wsl.conf 追加 [user] 下 default=<用户名>,再 wsl --shutdown
```

import 到新目录，避免与 Store 版 Ubuntu 包目录（CanonicalGroupLimited.*）纠缠。

## 环境要点（luode 本机）

- `cmd /c` 被 PowerShell 工具直接拦截，一律用 PowerShell 原生语法。
- 回收站删除通道（COM/Add-Type）不可用——缓存类本就永久删除，无影响；普通文件删除走确认流程。
- 大目录统计一律 robocopy /L 法，勿信 Get-ChildItem 对 Temp 的统计。

## 汇报模板

表格：操作 / 释放量 / 状态 ✅❌ + **C 盘剩余空间前后对比（核心指标）** + 未动的可选项（浏览器缓存、其他开发缓存）作为后续建议。
