# Windows PowerShell 命令失败案例库

本文件定义 Windows PowerShell 环境 Skill 的失败案例归属与动态状态格式。真实运行状态写入用户级 `%LOCALAPPDATA%\Codex\windows-powershell-environment\failure-cases.json`，不直接修改仓库规则文件。

## 路由

- PowerShell `CommandNotFoundException`、Windows 命令解析失败、Windows 包安装/版本探针失败，以及 Git Bash 对 Windows CLI 的可见性失败：归属 `windows-powershell-environment-rules`。
- WSL 原生 shell、`wsl.exe` 路由、`/mnt/*.exe` 互操作、Linux exit code `127`：归属 `windows-wsl-execution-rules`；先做 `command -v` 路径隔离。
- 业务行为错误：转交 `bug-*`；错误映射/重试设计：转交 `error-handling-rules`。

## 状态

`observed -> classified -> candidate -> verified` 是默认记录路径。权限阻断、未确认的包映射、网络失败和一次性抖动只能记录为 `blocked` 或 `candidate`，不得自动晋级为 `active`。

## 自动恢复边界

1. 只有 manifest 或显式传入的精确 package ID 才允许尝试安装。
2. 包源必须是已存在且允许的 `winget`、Scoop 或 Chocolatey；不执行远程安装脚本，不绕过 UAC。
3. 同一命令只允许一次安装/版本探针复验；失败后记录脱敏状态并停止。
4. 安装和真实版本探针都成功后才写入用户级 `discovered-tools.json`。它不自动加入后续 `SessionEnsure`；没有精确安装来源的条目必须标为 `check_only`，不能用于自动安装。
5. 未知命令不执行 `winget search` 猜包；必须同时有精确 `Source` 与 `PackageId`，没有完整映射时只记录 candidate。
6. Git Bash 可见性必须由 Git for Windows 安装目录下的 `bin\\bash.exe` 和 `uname -s` 的 `MINGW|MSYS` 共同证明。若实际是 `wsl.exe` 或 Linux `127`，停止 Windows 恢复并转交 WSL owner。

## Runtime and State Contract

- `SessionEnsure` is the session-entry operation. It defaults to `RequiredOnly`, uses a TTL marker and an atomic state lock, and caches both `ready` and `degraded` as `complete=true`; optional limitations are not a retry loop or a session block.
- `RecoverCommand` is the only supported automatic recovery entry. It accepts a manifest mapping for the selected source or an explicitly supplied exact `Source` plus package ID, performs one install attempt and one real version probe, then records `verified`, `blocked`, or `candidate`.
- `discovered-tools.json` entries remain recovery evidence, not session policy. Later `SessionEnsure` never expands its tool set from discovered entries; entries without exact installation provenance are `check_only`.
- The canonical manifest is never mutated at runtime. A discovered entry becomes canonical only through an explicit reviewed Skill change.
- Failure summaries are UTF-8, atomically replaced, deduplicated, length-limited, and redacted. The wrapper cannot intercept arbitrary agent shell calls unless a runtime hook explicitly invokes it.
- Result status is authoritative: `ready`, `degraded` and `rolled_back` exit `0`; `blocked` exits `10`; `busy` exits `11`; `failed` exits `12`; `rollback_refused` exits `13`. Do not infer readiness from package-manager output alone.
- Terminal or profile recovery is allowed only for journal entries with a backup and Apply-after SHA-256. A different current hash means `rollback_refused`; installed packages are never automatically removed.
