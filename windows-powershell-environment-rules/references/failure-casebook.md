# Windows PowerShell 命令失败案例库

本文件定义 Windows PowerShell 环境 Skill 的失败案例归属与动态状态格式。真实运行状态写入用户级 `%LOCALAPPDATA%\Codex\windows-powershell-environment\failure-cases.json`，不直接修改仓库规则文件。

## 路由

- PowerShell `CommandNotFoundException`、Windows 命令解析失败、Windows 包安装/版本探针失败：归属 `windows-powershell-environment-rules`。
- WSL 原生 shell、`/mnt/*.exe` 互操作、Linux exit code `127`：归属 `windows-wsl-execution-rules`；先做 `command -v` 路径隔离。
- 业务行为错误：转交 `bug-*`；错误映射/重试设计：转交 `error-handling-rules`。

## 状态

`observed -> classified -> candidate -> verified` 是默认记录路径。权限阻断、未确认的包映射、网络失败和一次性抖动只能记录为 `blocked` 或 `candidate`，不得自动晋级为 `active`。

## 自动恢复边界

1. 只有 manifest 或显式传入的精确 package ID 才允许尝试安装。
2. 包源必须是已存在且允许的 `winget`、Scoop 或 Chocolatey；不执行远程安装脚本，不绕过 UAC。
3. 同一命令只允许一次安装/版本探针复验；失败后记录脱敏状态并停止。
4. 安装成功后写入用户级 `discovered-tools.json`，后续 `SessionEnsure` 会自动纳入检查；canonical `tool-manifest.yaml` 仍需维护阶段显式晋级，避免运行时修改 Skill 资产。
5. 未知命令不执行 `winget search` 猜包；没有精确映射时只记录 candidate。

## Runtime and State Contract

- `SessionEnsure` is the session-entry operation. It uses a TTL marker and an atomic state lock; an incomplete apply writes `complete=false` so the next session can retry without treating the environment as healthy.
- `RecoverCommand` is the only supported automatic recovery entry. It accepts a manifest mapping or an explicitly supplied exact package ID, performs one install attempt and one real version probe, then records `verified`, `blocked`, or `candidate`.
- `discovered-tools.json` entries are accepted on later sessions only when `verified=true`, the package ID and executable name pass the allow-list grammar, and the source is empty or one of the existing approved managers.
- The canonical manifest is never mutated at runtime. A discovered entry becomes canonical only through an explicit reviewed Skill change.
- Failure summaries are UTF-8, atomically replaced, deduplicated, length-limited, and redacted. The wrapper cannot intercept arbitrary agent shell calls unless a runtime hook explicitly invokes it.
