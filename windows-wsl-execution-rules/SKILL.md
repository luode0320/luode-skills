---
name: windows-wsl-execution-rules
description: 当项目代码位于 WSL 文件系统内（如 /home/<user>/<project>）、在 Windows 环境下开发时触发。两种 agent 运行位置：agent 在 WSL 时直接访问代码、执行、调试，无需包裹；agent 在 Windows 时（如 Claude Desktop GUI），shell 默认用 Git Bash，看代码/改代码通过 \\wsl.localhost\<distro>\... 访问 WSL 文件，编译/运行/测试/调试通过 wsl.exe --cd /home/<user>/<project> <command> 进 WSL 执行（只有 WSL 进程能联网，二进制面向 Linux）。不再使用 /mnt 盘符路径。不要用它代替具体语言/框架实现、测试策略或编码规则。
---

# Windows / WSL 执行规范（代码在 WSL）

## 适用场景

项目代码放在 WSL 文件系统内（如 `/home/<user>/<project>`），开发在 Windows 环境进行。

## 核心架构：先看 agent 在哪运行

### 情况一：agent 在 WSL（推荐，最简单）

- 代码在 WSL、agent 在 WSL，本地直接访问
- 直接执行 `go build` / `go test` / `go run` / `dlv`，**无需任何包裹**
- 进程天然在 WSL，联网正常

### 情况二：agent 在 Windows（如 Claude Desktop GUI）

- **shell 默认用 Git Bash**
- **看代码、改代码**：通过 `\\wsl.localhost\<distro>\home\<user>\<project>` 访问 WSL 文件
- **编译、运行、测试、调试**：通过 `wsl.exe --cd /home/<user>/<project> <command>` 进 WSL 执行

## 为什么执行/调试必须在 WSL

- 只有 WSL 进程才能正常联网（Windows 上启动的进程受网络管控）
- 二进制面向 Linux，只能在 WSL 编译和运行

## 路径约定

代码在 WSL 内，两种访问方式：

| 用途 | 路径形式 |
|------|---------|
| WSL 内执行（agent 在 WSL，或 `wsl.exe --cd`） | `/home/<user>/<project>` |
| Windows 侧看代码/改代码（agent 在 Windows） | `\\wsl.localhost\<distro>\home\<user>\<project>` |

- `<distro>` 是 WSL 发行版名，用 `wsl.exe -l -v` 查看。
- **不再使用 `/mnt/<drive>`**——代码不在 Windows 盘。

## 执行环境分工（agent 在 Windows 时）

| 操作类型 | 执行方式 |
|---------|---------|
| 看代码、改代码（读写文件、搜索） | Git Bash，经 `\\wsl.localhost\...` 访问 |
| git 提交、拉取、status / diff / log | Git Bash（经 `\\wsl.localhost\...`）或 WSL 内 |
| 编译 / 运行 / 测试 / 调试 / 依赖 | `wsl.exe --cd /home/<user>/<project> <command>` |

## 命令模板（agent 在 Windows 时）

默认发行版省略 `-d`；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`：

```powershell
# 测试
wsl.exe --cd /home/<user>/<project> go test ./...
# 运行
wsl.exe --cd /home/<user>/<project> go run ./cmd/<app>
# 调试
wsl.exe --cd /home/<user>/<project> dlv debug ./cmd/<app>
# 依赖
wsl.exe --cd /home/<user>/<project> go mod download
```

agent 在 WSL 时直接执行，无需 `wsl.exe`：

```bash
cd /home/<user>/<project> && go test ./...
```

## WSL 内缓存目录建议

代码在 WSL 原生文件系统，I/O 性能好。Go 缓存默认即可，如需显式设置：

```bash
export GOCACHE=$HOME/.cache/go-build
export GOMODCACHE=$HOME/go/pkg/mod
```

## 不推荐做法

- 不要在 Windows 原生 Go 环境跑需联网的项目。
- 不要把 WSL 路径（`/home/...`）和 Windows 路径混用在同一命令上下文。
- agent 在 Windows 时，不要用 PowerShell 作默认 shell——用 Git Bash。
- 不要再用 `/mnt/<drive>`——代码已在 WSL，用 `/home/<user>/...` 与 `\\wsl.localhost\...`。

## 约束总结

**代码在 WSL；agent 在 WSL 直接干，agent 在 Windows 则 Git Bash 默认 shell + `\\wsl.localhost` 看代码、`wsl.exe --cd` 进 WSL 执行与调试。**

## 与其他规则的协作

- 涉及 Windows 中文编码、Git Bash 落盘细节时，联动 `windows-encoding-rules`。
- 涉及仓库长期规则沉淀时，联动 `project-agents-bootstrap`，把本规范写入仓库规则文件（`AGENTS.md` / `CLAUDE.md`）。

## 参考资料读取规则

- 默认先读 `references/command-templates.md`
- 需要路径访问细节时读 `references/path-mapping.md`
- 需要团队工作流时读 `references/recommended-workflow.md`
