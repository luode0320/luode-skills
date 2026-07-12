# 安全与验证契约

## 权限

- 默认只使用当前用户范围；不自动修改系统 PATH、系统级 profile 或 `powershell.exe`。
- 包管理器必须是本机已经存在且可执行的 `winget`、Scoop 或 Chocolatey。
- 需要管理员权限的安装直接记录为环境阻断，等待用户在提升后的终端重新运行。
- `SessionEnsure` 使用用户级 TTL marker 和原子锁；锁竞争时跳过重复安装，过期锁只在超过 30 分钟后清理。
- `RecoverCommand` 与会话检查共享状态锁，单次失败最多允许一次恢复安装和一次真实版本探针验证；失败后进入 `candidate` 或 `blocked`，不得无变化重试。
- 未知命令不执行包搜索猜测；只有 manifest 精确映射或调用方提供通过格式校验的 exact `PackageId` 才能安装。

## Terminal 设置

- Stable Windows Terminal 设置优先使用已发现的 `settings.json`；无法唯一确定路径时停止。
- 修改前复制备份，修改后重新解析 JSONC 并确认 `defaultProfile` 与 PowerShell 7 profile GUID 一致。
- 解析失败、profile 重复或原文件写入失败时恢复备份。

## 工具验证

- 以 manifest 的 command 实际解析路径为准，不以包管理器退出码为准。
- 每个命令都必须运行版本探针；已有命令只记录，不执行无请求升级。
- WSL 工具必须另行用 `command -v` 验证，不能复用 Windows 侧结果。
- 用户级 `discovered-tools.json` 与 `failure-cases.json` 必须 UTF-8、原子替换、去重并限制记录长度；失败摘要必须脱敏，不写 token、密码、密钥或完整绝对路径。
- canonical `references/tool-manifest.yaml` 不允许运行时自动修改。动态发现结果先进入用户状态文件，经过人工审查后再显式维护 manifest。
- Skill wrapper 只能覆盖显式接入的命令恢复路径；没有 runtime hook 时不得声称已拦截所有 agent shell 调用。

## 回滚

Journal 至少记录运行时间、设置备份路径、原 defaultProfile、写入的 profile GUID、安装成功的包 ID、使用的包源和验证结果。回滚只恢复 journal 中的内容，不删除用户原有工具。
