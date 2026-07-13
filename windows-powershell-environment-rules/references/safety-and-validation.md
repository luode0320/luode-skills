# 安全与验证契约

这份契约保证环境检查不会把“当前不需要的条件”误报成阻断：先看必需条件是否满足，再记录可选限制。所有写入都必须可追溯、可停止，并且不能覆盖用户在之后作出的修改。

## 权限

- 默认只使用当前用户范围；不自动修改系统 PATH、系统级 profile 或 `powershell.exe`。
- 包管理器必须是本机已经存在且可执行的 `winget`、Scoop 或 Chocolatey。来源优先级为 `winget`、`scoop-existing`、`chocolatey-existing`，但只有该来源本身存在精确映射时才可使用。
- 需要管理员权限的安装直接记录为环境阻断，等待用户在提升后的终端重新运行；不绕过 UAC。
- `SessionEnsure` 和 `Doctor` 默认采用 `RequiredOnly`。扩展工具、Terminal 或非当前 shell 的可见性不足只形成 `degraded`，不阻断可继续的会话。
- `SessionEnsure` 和 `Apply` 使用同一状态锁。持锁操作尚未结束时返回 `busy`；残留锁只能在确认不再被占用后回收。
- `RecoverCommand` 对同一输入最多允许一次恢复安装和一次真实版本探针；失败后进入 `candidate` 或 `blocked`，不得无变化重试。
- 未知命令不执行包搜索猜测；只有 manifest 的精确来源映射，或调用方同时提供通过格式校验的 exact `Source` 与 `PackageId`，才允许安装。
- `-WhatIf` 只报告计划变更，不能创建状态、marker、journal、profile 或 Terminal 文件，也不能调用包管理器。

## Terminal 设置

- Stable Windows Terminal 设置优先使用已发现的 `settings.json`；无法唯一确定路径时停止。
- 修改前保存备份并记录 SHA-256，修改后重新解析 JSONC 并确认 `defaultProfile` 与 PowerShell 7 profile GUID 一致。
- JSONC 解析、目标 GUID 冲突、最小补丁、写入或回读失败时，恢复本次 Terminal 写入并停止；不得把整份设置无关格式化后继续。
- profile 写入由 `windows-encoding-rules` 的事务结果交给环境 journal 编排。只有记录了备份、`beforeHash` 与 `afterHash` 的 profile 才可被环境回滚。

## 工具验证

- 以 manifest command 的实际解析路径与版本探针为准，不以包管理器退出码为准；包管理器退出 `0` 但探针失败仍是失败。
- 每个包源都有自己的精确包 ID。不能把 Winget ID 传给 Scoop 或 Chocolatey；当前来源无映射时记录限制并停止该工具恢复。
- Git Bash 必须从 `git.exe` 对应安装根目录的 `bin\\bash.exe` 找到，并以 `uname -s` 的 `MINGW` 或 `MSYS` 确认。`wsl.exe` 或裸 `bash.exe` 不能作为 Git Bash 证据。
- WSL 工具必须另行用 `command -v` 验证，不能复用 Windows 侧结果；Linux `127`、`/mnt/*.exe` 或 WSL launcher 问题转交 `windows-wsl-execution-rules`。
- 用户级 `discovered-tools.json` 与 `failure-cases.json` 必须 UTF-8、原子替换、去重并限制记录长度；失败摘要必须脱敏，不写 token、密码、密钥或完整绝对路径。
- 已验证的动态工具只为精确恢复保存证据；`check_only` 条目不能自动安装，任何 discovered 条目都不能自动加入后续 `SessionEnsure` 的策略。
- canonical `references/tool-manifest.yaml` 不允许运行时自动修改。动态发现结果先进入用户状态文件，经过人工审查后再显式维护 manifest。
- Skill wrapper 只能覆盖显式接入的命令恢复路径；没有 runtime hook 时不得声称已拦截所有 agent shell 调用。

## 回滚

- JSON 结果中的 `status` 是唯一的放行依据：`ready`、`degraded` 和 `rolled_back` 的退出码为 `0`；`blocked` 为 `10`；`busy` 为 `11`；`failed` 为 `12`；`rollback_refused` 为 `13`。
- Journal 至少记录运行时间、设置备份路径、原 defaultProfile、写入的 profile GUID、安装成功的包 ID、使用的包源、版本探针和文件 hash。
- 回滚只恢复 journal 中的 Terminal 或 profile 文件，且当前 SHA-256 必须仍等于 Apply 后 hash；不一致时返回 `rollback_refused`，绝不覆盖用户后续修改。
- 回滚不卸载软件包，也不删除用户原有工具。没有 journal、缺少 hash 或事务记录损坏时停止，不猜测恢复内容。
