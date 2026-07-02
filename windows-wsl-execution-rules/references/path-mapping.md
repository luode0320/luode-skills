# 路径访问规则

代码放在 WSL 文件系统内。根据 agent 运行位置，用不同路径形式访问。

## 路径形式

| 用途 | 路径形式 | 示例 |
|------|---------|------|
| WSL 内执行（agent 在 WSL，或 `wsl.exe --cd`） | `/home/<user>/<project>` | `/home/luode/myapp` |
| Windows 侧看代码/改代码（agent 在 Windows） | `\\wsl.localhost\<distro>\home\<user>\<project>` | `\\wsl.localhost\Ubuntu\home\luode\myapp` |
| 面向用户输出的项目内文件引用（agent 在 Windows） | `\\wsl.localhost\<distro>\home\<user>\<project>\<relative-path>` | `\\wsl.localhost\Ubuntu-24.04\home\luode\code\ellipal_admin\doc\6-审查\a.md` |

## 说明

- `<distro>` 是 WSL 发行版名，用 `wsl.exe -l -v` 查看（如 `Ubuntu`、`Ubuntu-24.04`）。
- **只有执行类命令才用 WSL 内路径 `/home/<user>/<project>`**（agent 在 Windows 时配合 `wsl.exe --cd`）。
- **Windows 侧编辑器/文件访问用 `\\wsl.localhost\<distro>\...`** —— 这是 Windows 访问 WSL 原生文件的官方稳定方式。
- **所有面向用户展示的项目内文件引用都用用户当前环境可打开的路径**：项目在 WSL 且用户从 Windows 桌面访问时，Markdown 链接、普通文本路径、审查报告证据路径、总结里的文件路径都使用 `\\wsl.localhost\<distro>\...`，不要把 `/home/...` 当成用户可打开路径输出。
- 代码已在 WSL 内，**不再使用 `/mnt/<drive>`**（那是访问 Windows 盘的路径）。

## 注意事项

- 不要把 WSL 路径（`/home/...`）和 Windows UNC 路径（`\\wsl.localhost\...`）混用在同一命令上下文。
- `wsl.exe --cd` 后必须是 WSL 内路径 `/home/<user>/<project>`，不是 UNC 路径。
- 回复用户时，若引用的是项目内文件而不是命令参数，应优先按项目根目录的 Windows 访问路径输出；只有命令、日志原文或 WSL shell 上下文保留 `/home/...`。
- 路径含空格时整体放进引号。
- 搜索、读文件、改规则、普通 git 盘点等非执行动作，不要为了统一格式强行改成 `/home/...` 上下文。
