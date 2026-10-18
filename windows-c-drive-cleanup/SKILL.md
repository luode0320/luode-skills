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
```

**⚠️ 解析坑（2026-10-15 实测踩过）**：不要用 `$line -match 'Bytes\s*:'` 或找 `字节:` 文本行——中文系统摘要块标签是「字节:」，且 `-match 'Bytes'` 在 GBK 输出下必然失配，导致**全部目录被误报为 0 GB**（假阴性，最危险）。正确做法是**按行序号解析**：摘要块固定 6 列（总数/复制/跳过/不匹配/失败/其他），逐行捕获「标签: 6 个数字」的行，第 3 行（索引 2）就是字节数：

```powershell
function Get-DirBytes($path) {
    if (-not (Test-Path -LiteralPath $path)) { return -1 }   # 不存在
    $out = robocopy $path 'C:\__stat_dummy__' /L /S /NJH /NFL /NDL /NP /BYTES /XJ /R:0 /W:0
    $rows = @()
    foreach ($line in $out) {
        if ($line -match '^\s*\S+\s*:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)') {
            $rows += [int64]$Matches[1]
        }
    }
    if ($rows.Count -ge 3) { return $rows[2] }   # 第3行=字节
    if ($rows.Count -ge 1) { return $rows[-1] }
    return -2
}
```

`robocopy` 对不可读目录返回错误码，但 `/L` 只读列举不影响文件。全盘扫 `C:\` 与 `C:\Users\<用户>` 顶层各耗时数十秒，耐心等。

扫描目标清单：

| 类别 | 路径 |
|---|---|
| 用户临时 | %LOCALAPPDATA%\Temp |
| 系统临时 | C:\Windows\Temp、C:\Windows\Prefetch（普通权限可能 N/A，报告标注即可） |
| 更新缓存 | C:\Windows\SoftwareDistribution\Download |
| 浏览器缓存 | %LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache；Edge 同构 |
| 开发缓存 | %LOCALAPPDATA%\go-build、%USERPROFILE%\go\pkg\mod、%USERPROFILE%\.gradle\caches、%LOCALAPPDATA%\npm-cache、%USERPROFILE%\.cargo\registry\cache、%LOCALAPPDATA%\uv\cache、%LOCALAPPDATA%\pnpm、%USERPROFILE%\.cache\puppeteer、%LOCALAPPDATA%\pip\cache、.m2\.nuget（存在才统计） |
| 回收站 | C:\$Recycle.Bin |
| WSL 虚拟磁盘 | %LOCALAPPDATA%\Packages\*\LocalState\ext4.vhdx（只报告大小） |

**本机实测的大头（2026-10-15，C 盘已用 191 GB 时）**，按此优先级找空间，勿只盯常规 Temp：

| 项目 | 大小 | 路径 | 分级 |
|---|---|---|---|
| go-build 构建缓存 | 5.82 GB | %LOCALAPPDATA%\go-build | 低 |
| gradle caches | 3.58 GB | %USERPROFILE%\.gradle\caches | 低 |
| go mod | 3.36 GB | %USERPROFILE%\go\pkg\mod | 低 |
| npm-cache | 1.84 GB | %LOCALAPPDATA%\npm-cache | 低 |
| Chrome 端侧 AI 模型 | 3.98 GB | ...\Chrome\User Data\OptGuideOnDeviceModel | 中（删除后按需重下） |
| Codex 运行时缓存 | 3.25 GB | %USERPROFILE%\.cache\codex-runtimes | 中 |
| Codex 历史会话 | 3.08 GB | %USERPROFILE%\.codex\sessions + archived_sessions | 中（删了不可恢复） |
| WSL ext4.vhdx | 34.57 GB | %LOCALAPPDATA%\Packages\*\LocalState\ext4.vhdx | 禁删，只可压缩 |

注意 `%LOCALAPPDATA%\Google`（Chrome 5.15G + DriveFS 3.32G）与 `%LOCALAPPDATA%\Programs`（QuarkCloudDrive 3.69G 等）也是大项，但 DriveFS 云盘缓存可能含未同步数据、Programs 是已装程序，**默认列为禁动/仅报告**。

报告产出：HTML 表格（分类/路径/大小/建议/风险分级：低=可重建缓存、中=浏览器缓存建议手动清、高=禁动项）→ present_files 打开 → AskUserQuestion 让用户勾选执行范围（多选：系统临时文件 / 开发缓存 / 回收站 / 全部扫描分析；执行方式：先报告 / 直接清安全项）。

## 第二步：执行清理（严格按用户确认的范围）

官方命令优先（比手删稳，自动处理只读权限）：

```powershell
# go.exe 在 C:\Program Files\Go\bin\go.exe（PATH 里可能没有，用全路径）
& 'C:\Program Files\Go\bin\go.exe' clean -modcache   # 清 %USERPROFILE%\go\pkg\mod
& 'C:\Program Files\Go\bin\go.exe' clean -cache      # 清 %LOCALAPPDATA%\go-build（本机 5.82G，最大单项）
npm cache clean --force
pip cache purge
uv cache clean
pnpm store prune
# gradle: 直接删 %USERPROFILE%\.gradle\caches 整个子目录（3.58G，下次构建重下）
# cargo:  直接删 %USERPROFILE%\.cargo\registry\cache 子目录
# puppeteer: 直接删 %USERPROFILE%\.cache\puppeteer（浏览器二进制，下次安装重下）
```

**⚠️ npm/uv/pnpm 输出走 stderr，PowerShell 会报 `NativeCommandError`**（红字），但退出码为 0、操作实际成功——例如 `uv cache clean` 报错后紧跟着 `Removed 2170 files (95.5MiB)`。判定成功看输出里的 `Removed N files` / `Removed N packages` 行，不要被红字误导为失败。

Temp 清理：先对已确认的目标使用 `Remove-Item -LiteralPath '<目标目录>' -Recurse -ErrorAction Stop`，默认不加 `-Force`；被占用或权限不足时保留失败项并报告，不用 `SilentlyContinue` 隐藏结果。分批执行，每批后可复核。执行前确认当前工具的可写范围覆盖目标绝对路径；用户确认删除范围不等于工具已有该路径的写权限。

**⚠️ 整目录删 Temp 会连带删掉工具自己的输出文件**（2026-10-15 实测）：CLI 把任务输出写在 `%LOCALAPPDATA%\Temp\qoder-cli\...`，一条 `Remove-Item <Temp> -Recurse` 之后工具回读输出文件失败，报 `bash output unavailable`，命令结果丢失。**正确做法：逐项循环 + try/catch 计数**，既拿到 ok/fail 统计又避免误伤：

```powershell
$ok = 0; $fail = 0
Get-ChildItem -LiteralPath $target -Force -ErrorAction SilentlyContinue | ForEach-Object {
    try { Remove-Item -LiteralPath $_.FullName -Recurse -ErrorAction Stop; $ok++ }
    catch { $fail++ }   # 被占用/权限不足，保留不报错
}
# 结果写 UTF-8 文件再读，避免 GBK 控制台乱码
[System.IO.File]::WriteAllLines($log, $lines, [System.Text.UTF8Encoding]::new($false))
```

本机实测：Temp 2665 项成功 / 52 项被占用跳过，属正常。

**⚠️ 辅助脚本必须纯 ASCII**（2026-10-15 实测）：`Write` 工具产出的是无 BOM 的 UTF-8，而 `powershell.exe -File` 按系统 ANSI(GBK) 读脚本，脚本内任何中文字符串都会触发 `ParserError: 缺少“)”`。**临时 .ps1 一律只写英文**；需要中文报告就写进 HTML 或 UTF-8 文本文件（用 `WriteAllLines` + UTF8Encoding），不要靠控制台回显。

**⚠️ `C:\Windows\SoftwareDistribution\Download` 需管理员**（2026-10-15 实测）：普通权限下 12 项全部 `拒绝访问`。不要尝试提权绕过，如实报告并给出用户手动执行的管理员命令。

**⚠️ `Clear-RecycleBin` 本机不可用**（2026-10-15 实测）：报 `系统找不到指定的文件夹`（Win32Exception），与 COM/Add-Type 通道一样失效。先只读复核回收站实际大小（`robocopy 'C:\$Recycle.Bin' ...`），若本就近乎为空（实测仅 129 字节）则直接跳过并说明。

**命令策略拦截处理：**

- 目录盘点与删除必须分成不同的工具调用；不要把 `Get-ChildItem -Force` 等盘点操作和 `Remove-Item` 删除拼进同一段 PowerShell 命令。删除命令只包含已确认的目标及删除动作，避免盘点参数影响危险命令识别。
- 删除前分别判断两种权限：① 当前工具/沙箱对目标路径的写入范围；② 命令策略是否允许该删除动作。文件系统 ACL、工具可写范围和危险命令审批是不同层次，满足其中一项不代表其他项也满足。
- 若目标在当前可写范围之外（例如 `workspace-write` 未包含 `%LOCALAPPDATA%\Temp` 下的目标），不要发起删除命令。只有当前工具明确提供针对该目标/动作的正式审批入口时，才通过该入口请求授权；不得用 `cmd`、WSL、Bash、其他 shell、提权进程或另一个执行通道绕过范围限制。
- 若工具返回 `blocked by policy`，先依据工具提供的拒绝元数据区分“路径/沙箱权限不足”与“命令被危险命令策略拦截”。错误没有说明原因时标记为“拒绝原因未确认”，不得把推测写成事实；只读复核目标状态并如实报告，不能据此声称命令已经运行或文件已删除。
- 危险命令策略拦截时立即结束当前删除调用；若拒绝原因未确认，仍只保持未确认，不推断根因。Remove-Item -Force（尤其与 -Recurse 同用）可能被策略拦截；approval_policy=never 时不会出现交互审批。不得在本轮自动重试、改参数试探、换 shell/通道或自行调整策略；应说明 Skill 不能解除宿主/工具策略。
- 后续轮次若用户明确再次授权删除同一精确目标，无论前次拒绝原因是否确认，都将该消息视为一个新的请求：先只读核对目标仍存在、删除范围未变，并重新核验当前工具的可写范围和可用执行入口。只有当前入口明确可写该目标且可执行该动作时，最多执行一次单独的不带 -Force 精确删除；用户授权只允许重新评估，不会覆盖平台拒绝。
- 若该次新调用再次返回 blocked by policy（包括原因仍未知），立即停止，不再进行删除尝试。只有当前执行配置发生可核验且确实影响该目标写入范围或该删除动作策略的变化，或当前工具出现适用于该目标/动作的正式逐项审批入口，并且用户在后续轮次再次明确授权，才可重新评估一次；无关配置变化不构成恢复条件。未来会话是否能执行取决于当时工具的实际权限，Skill 更新本身不保证放行。
- 只有当前工具显示了正式审批入口且用户已确认的目标范围未变，才可通过该入口申请这一次具体删除的审批；若获批，仍只执行精确目标。没有审批入口或审批被拒绝时停止，不继续删除。
- 只有在不带 `-Force` 的精确删除已实际运行并确因只读/隐藏属性失败，且当前命令策略提供正式逐项审批入口时，才可在用户确认范围内申请对 `-Force` 的单次审批；不得把 `-Force` 当作 Temp 清理默认参数。

## WSL ext4.vhdx 压缩（2026-09-05 首次实测，2026-10-15 复测）

### ✅ 有效路径（首选，免管理员、零数据风险）

1. 先摸清分布，**确认不碰业务数据**（containerd/docker、/apps 数据库、/home 项目一律不动）：
   `wsl -d <发行版> -u root -- bash -c "du -xh -d1 / ; du -xh -d1 /var/lib"`
   本机实测分布：containerd 13G + mysql8.1 5.9G（/apps）+ /root 4G（含 .cache/go-build 2.9G）+ /home 2.4G + /var/log 0.4G。
2. WSL 内清理（发行版名先 `wsl -l -q` 确认，常为 `Ubuntu` 而非 `Ubuntu-24.04`）：
   `wsl -d <发行版> -u root -- bash -c "<命令>"`
   - **`go clean -cache` 在 root 下无效**（root 的 PATH 无 go，`which go` 报 no-go-in-path，GOCACHE 为空）→ 直接 `rm -rf /root/.cache/go-build`（本机 2.9G）
   - `apt-get clean`
   - `journalctl --rotate && journalctl --vacuum-size=50M`（**不先 rotate 直接 vacuum 会 freed 0B**；本机实测 freed 340M）
   - 清 `/tmp`
3. `fstrim -v /`（discard 标记全部空闲块；本机实测 trimmed 978 GiB，`df` 显示 31G → 28G）
4. `wsl --shutdown`
5. **重启电脑** → vhdmp 在挂载周期内自动回收空洞（2026-09-05 实测 43.63 → 19.11 GB，回收 24.5 GB）
6. 验证：vhdx 文件大小、`df -h /`（内部数据应原样）、WSL 正常启动

**⚠️ `wsl --shutdown` 后 vhdx 文件不会立即变小**（2026-10-15 复测确认）：fstrim + shutdown 完成后立刻查 vhdx 仍是 34.57 GB（分毫未动）。空洞回收由 vhdmp 在**下次挂载周期**（即重启电脑）完成，**不要据此判定压缩失败**。Agent 无法自行重启，应在汇报中明确请用户重启，并说明重启后预期还会再释放数 GB。

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
- 回收站删除通道（COM/Add-Type/Clear-RecycleBin）不可用——缓存类本就永久删除，无影响；普通文件删除走确认流程。
- 大目录统计一律 robocopy /L 法，勿信 Get-ChildItem 对 Temp 的统计；robocopy 输出解析必须按行序号（见第一步），勿匹配 `Bytes`/`字节:` 文本。
- 控制台是 GBK，PowerShell 回显中文必乱码；结果一律写 UTF-8 文件再读。
- 临时 .ps1 脚本只用英文（见第二步解析坑）。
- 全盘扫描 `C:\` 顶层 + `C:\Users\<用户>` 顶层 + `%LOCALAPPDATA%` 顶层（>500MB 过滤）足够定位大头，实测约 1-2 分钟。
- HTML 报告用 `Start-Process '<报告绝对路径>.html'` 在默认浏览器打开（本机无 present_files 工具）。
- 清理完**收尾删掉自己创建的临时 .ps1/.txt**，只保留 HTML 报告给用户。

## 汇报模板

表格：操作 / 释放量 / 状态 ✅❌ + **C 盘剩余空间前后对比（核心指标）** + 未动的可选项（浏览器缓存、其他开发缓存）作为后续建议。

**2026-10-15 实测基准**（可作为量级参考）：C 盘 206.19 GB，剩余 14.97 GB 起步；清完开发缓存 + Temp + WSL 内缓存后 → **剩余 33.74 GB（净释放 ~18.8 GB）**，其中开发缓存 ~15.5G、Temp ~3.6G、WSL 内 ~3.4G。WSL vhdx 待重启后再收数 GB。

汇报必须如实列出**未完成项及原因**（如 `SoftwareDistribution\Download` 需管理员、回收站通道不可用），不要含糊带过或谎报成功。最后单列「还需你操作一步」小节（如重启电脑），并给出可选项的管理员命令原文。
