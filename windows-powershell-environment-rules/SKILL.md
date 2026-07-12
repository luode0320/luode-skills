---
name: windows-powershell-environment-rules
description: 当 Windows 环境需要检查或准备 PowerShell 专项入口、Windows Terminal 用户级默认 profile、UTF-8 profile 或常用 Windows CLI 工具，或执行过程中出现命令缺失时触发。负责优先使用 PowerShell 7、幂等安装 manifest 工具、按精确映射恢复 command-not-found、记录脱敏失败案例和用户级 discovered tools，并在新会话入口自动检查；不替换 powershell.exe、不猜测未知包、不改变 WSL 原生命令路径。
---

# Windows PowerShell 环境准备规则

本 skill 只管理 Windows 用户级 PowerShell 专项环境。普通仓库命令继续使用 Git Bash / bash，编译、运行、测试和调试继续按 `windows-wsl-execution-rules` 路由到 WSL。

## 自动触发信号

- Windows 环境中检测到当前 PowerShell 主版本低于 7，或找不到 `pwsh.exe`。
- 用户要求把 PowerShell 7 设为默认、准备 Windows Terminal 或修复 PowerShell 专项入口。
- 用户要求安装 `rg`、`fd`、`fzf`、`jq`、`yq` 等本 skill 白名单工具。
- Windows 专项脚本需要稳定的 UTF-8 profile 和可验证的工具 PATH。
- 新会话开始、会话 TTL 过期或会话状态缺失时，必须先运行 `SessionEnsure`。
- PowerShell `CommandNotFoundException`、`command-not-found`、Windows “not recognized/找不到”错误或已知 manifest 命令缺失时，进入 `RecoverCommand`；恢复最多一次安装尝试和一次真实版本探针验证。
- 未知命令只有在调用方提供精确、已批准的 `PackageId` 时才可尝试安装；不执行 `winget search` 猜包。
- 安装并验证成功的非 canonical 命令写入用户级 `discovered-tools.json` 和脱敏 `failure-cases.json`，供后续会话合并读取；运行时不直接修改 canonical `tool-manifest.yaml`。
- 该 skill 不能拦截 runtime 中所有任意 shell 调用；只有显式调用 wrapper 或未来接入 runtime hook 的路径能自动恢复。

## 默认边界

- “默认 PowerShell”只表示 Windows Terminal 默认 profile 和 agent 的 PowerShell 专项调用优先使用 `pwsh.exe -NoLogo`。
- 永不替换、重命名或覆盖系统 `powershell.exe`，保留 Windows PowerShell 5.1 作为旧脚本回退。
- 不修改 VS Code 终端、不修改全局 Git 配置、不把 Windows 工具当作 WSL 原生工具。
- 只安装缺失项；已有工具不做无请求的版本升级。

## 执行流程

1. 新会话先运行 `scripts/initialize_windows_powershell.ps1 -Mode SessionEnsure`；它使用 TTL marker 与原子锁避免重复并发安装。
2. 首次准备或显式审计时运行 `scripts/initialize_windows_powershell.ps1 -Mode Audit`，确认 OS、PowerShell 版本、包管理器、管理员状态、Terminal 设置路径和工具命令路径。
3. `Apply` 模式先安装并验证 PowerShell 7，再运行 `windows-encoding-rules/scripts/enable_powershell_utf8.ps1`，随后逐项安装并验证缺失工具。
4. 配置 Windows Terminal 前创建带时间戳的备份；JSONC 解析或回读失败时恢复备份并停止。
5. 每次写入后启动新的 `pwsh -NoLogo -NoProfile` 子进程验证版本与 UTF-8 编码；`Rollback` 只处理本次 journal 记录的设置和新安装项。

## 包源与权限

- 包源顺序固定为 `winget`、已存在的 Scoop、已存在的 Chocolatey；系统自带 `curl.exe` 只验证，不作为待安装包。
- 所有包都使用 `references/tool-manifest.yaml` 中的精确 ID；不执行未固定来源的远程脚本。
- 当前用户没有管理员权限时，优先使用用户级安装；若包要求提升权限，记录阻断并停止，不自动绕过 UAC。
- 失败后按 `execution-failure-learning-rules` 分类，不对同一输入无变化重复安装。
- 命令恢复必须使用 `scripts/recover_windows_command.ps1`；未知命令无精确包 ID 时只记录 candidate，不安装。

## WSL 隔离

Windows 侧 `rg.exe`、`fd.exe` 或其他工具安装成功，不代表 WSL 工具合规。进入 WSL 项目后仍必须用 `command -v` 检查原生路径；命中 `/mnt/` 下的 Windows 二进制时按 WSL 规则修复。

## 验收标准

- `pwsh` 主版本为 7 或更高，`powershell.exe` 仍可调用。
- Windows Terminal `defaultProfile` 指向唯一的 PowerShell 7 profile，重复执行不会产生重复 profile。
- Windows PowerShell 5.1 和 PowerShell 7 的用户 profile 均通过 UTF-8 探针。
- manifest 中缺失工具逐项安装并通过实际版本命令验证，已有工具保持不变。
- 失败时保留脱敏日志和 journal，能够恢复 Terminal 设置；禁止以仅退出码为 0 作为成功依据。

## 入口

```powershell
& .\scripts\initialize_windows_powershell.ps1 -Mode Audit
& .\scripts\initialize_windows_powershell.ps1 -Mode Apply -ToolBundle Extended
& .\scripts\initialize_windows_powershell.ps1 -Mode SessionEnsure
& .\scripts\recover_windows_command.ps1 -CommandName rg.exe -ErrorText 'The term rg is not recognized'
& .\scripts\recover_windows_command.ps1 -CommandName acme.exe -PackageId Contoso.AcmeCli -Source winget -ErrorText 'command not found'
& .\scripts\initialize_windows_powershell.ps1 -Mode Rollback
```
