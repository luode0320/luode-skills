---
name: windows-powershell-environment-rules
description: 当 Windows 环境需要检查或准备 PowerShell 专项入口、Windows Terminal 用户级默认 profile、UTF-8 profile 或常用 Windows CLI 工具，或执行过程中出现命令缺失时触发。负责优先使用 PowerShell 7、以 RequiredOnly 完成会话准备、按精确的“每个包源各自包 ID”恢复 command-not-found、返回可机器读取的状态和退出码，并记录脱敏失败案例和用户级 discovered tools；不替换 powershell.exe、不猜测未知包、不改变 WSL 原生命令路径。
---

# Windows PowerShell 环境准备规则

本 skill 只管理 Windows 用户级 PowerShell 专项环境。普通仓库命令继续使用 Git Bash / bash，编译、运行、测试和调试继续按 `windows-wsl-execution-rules` 路由到 WSL。

先看结果再决定是否继续：`ready` 表示当前要求都满足，`degraded` 表示必需条件已满足但有可选限制，两者都可以继续；只有 `blocked`、`busy`、`failed` 或 `rollback_refused` 才不能把当前操作当成已准备好。

## 自动触发信号

- Windows 环境中检测到当前 PowerShell 主版本低于 7，或找不到 `pwsh.exe`。
- 用户要求把 PowerShell 7 设为默认、准备 Windows Terminal 或修复 PowerShell 专项入口。
- 用户要求安装 `rg`、`fd`、`fzf`、`jq`、`yq` 等本 skill 白名单工具。
- Windows 专项脚本需要稳定的 UTF-8 profile 和可验证的工具 PATH。
- 新会话开始、会话 TTL 过期或会话状态缺失时，必须先运行 `SessionEnsure`。它默认只检查 `RequiredOnly`，不会把未要求的扩展工具当成会话阻断。
- PowerShell `CommandNotFoundException`、`command-not-found`、Windows “not recognized/找不到”错误或已知 manifest 命令缺失时，进入 `RecoverCommand`；恢复最多一次安装尝试和一次真实版本探针验证。
- 未知命令只有在调用方提供精确、已批准的 `PackageId` 时才可尝试安装；不执行 `winget search` 猜包。
- 安装并验证成功的非 canonical 命令写入用户级 `discovered-tools.json` 和脱敏 `failure-cases.json`；它们只为后续精确恢复保留证据，不会自动扩大 `SessionEnsure` 的检查范围，运行时也不直接修改 canonical `tool-manifest.yaml`。
- 该 skill 不能拦截 runtime 中所有任意 shell 调用；只有显式调用 wrapper 或未来接入 runtime hook 的路径能自动恢复。

## 默认边界

**PowerShell 专项调用默认优先 PowerShell 7（`pwsh`），Windows PowerShell 5.1 仅在 pwsh7 缺失且升级被阻断时回退；能用 bash / WSL 完成的普通仓库与执行类命令一律不走 PowerShell。完整判定以 `windows-wsl-execution-rules` 的 `## PowerShell 使用优先级阶梯（硬约束）` 为准。**

- “默认 PowerShell”只表示 Windows Terminal 默认 profile 和 agent 的 PowerShell 专项调用优先使用 `pwsh.exe -NoLogo`。
- 永不替换、重命名或覆盖系统 `powershell.exe`，保留 Windows PowerShell 5.1 作为旧脚本回退。
- 不修改 VS Code 终端、不修改全局 Git 配置、不把 Windows 工具当作 WSL 原生工具。
- 只安装缺失项；已有工具不做无请求的版本升级。
- `SessionEnsure` 和 `Doctor` 默认使用 `RequiredOnly`；显式 `Apply` 默认使用 `Extended`。需要更小或更大的范围时，调用方必须明确传入 `-Policy RequiredOnly|Core|Extended`。
- 默认输出是 JSON。调用方必须读取 `status`、`canContinue`、`requiredReady`、`restartRequired`、`results`、`issues` 和 `changes`，不得只看命令是否返回了文本。
- `-WhatIf` 只能产生计划中的 `changes`，不得写状态、profile、Terminal、journal 或调用包管理器安装。

## 执行流程

1. 新会话先运行 `scripts/initialize_windows_powershell.ps1 -Mode SessionEnsure -Policy RequiredOnly -OutputFormat Json`；TTL marker 可缓存 `ready` 或 `degraded`，状态锁冲突返回 `busy`，不重复安装。
2. 首次准备或显式审计时运行 `scripts/initialize_windows_powershell.ps1 -Mode Audit -OutputFormat Json` 或 `-Mode Doctor`，确认 OS、PowerShell 版本、包管理器、Terminal 设置路径、工具命令路径和当前 shell 可见性。
3. `Apply` 默认使用 `Extended`；每个缺失工具必须先从 manifest 找到当前包源自己的精确包 ID，再安装并运行真实版本探针。缺少该包源映射时不安装，也不得把另一包源的 ID 直接复用。
4. 配置 Windows Terminal 前创建备份；JSONC 解析、最小补丁或回读失败时停止并恢复本次写入。profile 变更由编码脚本返回的事务结果交给环境 journal 编排，不能以口头成功代替证据。
5. `Rollback` 只恢复 journal 中记录的 Terminal 或 profile 文件，且当前 SHA-256 必须仍等于 Apply 后的 hash；检测到用户后续修改时返回 `rollback_refused`。软件包永不自动卸载。
6. 状态和退出码固定为：`ready`、`degraded`、`rolled_back` 为 `0`；`blocked` 为 `10`；`busy` 为 `11`；`failed` 为 `12`；`rollback_refused` 为 `13`。

## 包源与权限

- 包源顺序固定为 `winget`、已存在的 Scoop、已存在的 Chocolatey；系统自带 `curl.exe` 只验证，不作为待安装包。
- 所有包都使用 `references/tool-manifest.yaml` 中当前包源的精确 ID；Winget、Scoop、Chocolatey 的 ID 彼此独立，某来源没有精确映射时不可退回、搜索或猜测。
- 当前用户没有管理员权限时，优先使用用户级安装；若包要求提升权限，记录阻断并停止，不自动绕过 UAC。
- 失败后按 `execution-failure-learning-rules` 分类，不对同一输入无变化重复安装。
- 命令恢复必须使用 `scripts/recover_windows_command.ps1`；未知命令必须同时提供精确 `-Source` 与 `-PackageId`，缺一时只记录 candidate，不安装。

## WSL 隔离

Windows 侧 `rg.exe`、`fd.exe` 或其他工具安装成功，不代表 WSL 工具合规。Git Bash 可见性只能从已解析的 `git.exe` 安装根目录定位 `bin\\bash.exe`，并以 `uname -s` 的 `MINGW` 或 `MSYS` 结果确认；不得用裸 `bash.exe` 把 WSL launcher 误认成 Git Bash。进入 WSL 项目后仍必须用 `command -v` 检查原生路径；Linux `127`、`wsl.exe` 和 `/mnt/*.exe` 互操作问题交给 `windows-wsl-execution-rules`。

## 验收标准

- `pwsh` 主版本为 7 或更高，`powershell.exe` 仍可调用。
- Windows Terminal `defaultProfile` 指向唯一的 PowerShell 7 profile，重复执行不会产生重复 profile。
- Windows PowerShell 5.1 和 PowerShell 7 的用户 profile 均通过 UTF-8 探针。
- manifest 中缺失工具逐项安装并通过实际版本命令验证，已有工具保持不变。
- 可选工具、Terminal 或非当前 shell 的限制只返回 `degraded`，不会阻断 RequiredOnly 会话；明确必需且无替代验证的缺失必须返回 `blocked`。
- 失败时保留脱敏日志和 journal，能够在 hash 未漂移时恢复 Terminal 或已记录的 profile 设置；禁止以仅退出码为 0 作为成功依据。

## 入口

```powershell
& .\scripts\initialize_windows_powershell.ps1 -Mode Audit
& .\scripts\initialize_windows_powershell.ps1 -Mode Apply -Policy Extended
& .\scripts\initialize_windows_powershell.ps1 -Mode SessionEnsure -Policy RequiredOnly -OutputFormat Json
& .\scripts\initialize_windows_powershell.ps1 -Mode Doctor -OutputFormat Json
& .\scripts\recover_windows_command.ps1 -CommandName rg.exe -ErrorText 'The term rg is not recognized'
& .\scripts\recover_windows_command.ps1 -CommandName acme.exe -PackageId Contoso.AcmeCli -Source winget -ErrorText 'command not found'
& .\scripts\initialize_windows_powershell.ps1 -Mode Rollback
```
