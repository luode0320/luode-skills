---
name: windows-wsl-execution-rules
description: 当项目代码位于 WSL 文件系统内（如 `/home/user/project`）、且当前任务发生在 Windows 环境时触发。核心边界：只有执行类动作才优先进入 WSL，例如编译、运行/启动程序、测试、调试、会真实启动运行时的依赖安装；看代码、改代码、搜索、读写规则文件、普通 git 操作与多数只读检查默认优先使用 Git Bash / bash。PowerShell 不作为 Windows 下普通仓库命令入口，只在 `.ps1` 脚本、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。agent 在 WSL 时直接访问代码与执行；agent 在 Windows 时（如 Claude Desktop GUI），普通命令通过 Git Bash / bash 访问 `//wsl.localhost/distro/...` 或等价 Windows 可访问路径，执行类动作再用 `wsl.exe --cd /home/user/project target-command` 进 WSL。无论文件写入发生在 Windows、WSL 还是 Linux，都必须遵守 UTF-8 文件写入规则，禁止 GBK/ANSI/默认编码落盘。纯 Windows 项目或不需要启动执行的任务，不要误切到 WSL。不要用它代替具体语言/框架实现、测试策略或编码规则。
---

# Windows / WSL 执行规范（代码在 WSL）

## 适用场景

项目代码放在 WSL 文件系统内（如 `/home/<user>/<project>`），开发在 Windows 环境进行，且需要明确区分“普通命令”和“执行类命令”。

## 核心架构：先看 agent 在哪运行

### 情况一：agent 在 WSL（推荐，最简单）

- 代码在 WSL、agent 在 WSL，本地直接访问
- 直接执行 `go build` / `go test` / `go run` / `dlv`，**无需任何包裹**
- 进程天然在 WSL，联网正常

### 情况二：agent 在 Windows（如 Claude Desktop GUI）

- **shell 选择**：普通仓库命令优先使用 Git Bash / bash；PowerShell 不作为普通仓库命令入口，只在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用
- **看代码、改代码**：通过 `\\wsl.localhost\<distro>\home\<user>\<project>` 访问 WSL 文件
- **普通命令默认不切 WSL**：搜索、读文件、改文件、规则检查、普通 `git status` / `git diff` / `git log` 等，默认留在 Git Bash / bash
- **文件写入仍按 UTF-8**：普通读写留在 Git Bash / bash 时，脚本语言读写必须显式声明 UTF-8；不得因为路径在 WSL 或命令未进 WSL 就依赖 GBK / ANSI / shell 默认编码
- **执行类命令再进 WSL**：编译、运行、启动程序、测试、调试，以及会真实启动运行时的依赖安装，通过 `wsl.exe --cd /home/<user>/<project> <command>` 执行

## 什么算执行类命令

- 会产出或启动可执行程序的命令：如 `go build`、`go run`、`npm start`、`pnpm dev`、`python app.py`
- 会真实跑测试或调试器的命令：如 `go test`、`pytest`、`dlv debug`
- 启动程序、测试、调试和联调命令必须使用 local 本地配置、本地数据库和本地服务；不得通过 WSL 启动连接 `test` / `prod` / `staging` 数据库、缓存、消息队列、HTTP/RPC 上游或其他非 local 服务。
- 会依赖 WSL 运行时环境才能正确完成的安装/准备动作：如 `go mod download`、需要 Linux 环境的 `npm install`
- 不启动程序的普通仓库操作 **不算** 执行类命令：如 `rg`、`ls`、`cat`、规则文件检查、文档修改、普通 git 盘点

## 为什么只有执行类动作优先在 WSL

- 只有 WSL 进程才能正常联网（Windows 上启动的进程受网络管控）
- 运行产物与调试链路面向 Linux，执行时需要留在 WSL
- 普通读写、搜索、git 盘点不依赖 Linux 运行时，强行切 WSL 反而容易引入路径、权限和工具解析问题

## 路径约定

代码在 WSL 内，两种访问方式：

| 用途 | 路径形式 |
|------|---------|
| WSL 内执行类动作（agent 在 WSL，或 `wsl.exe --cd`） | `/home/<user>/<project>` |
| Windows 侧普通命令、看代码、改代码（agent 在 Windows） | Git Bash / bash 使用 `//wsl.localhost/<distro>/home/<user>/<project>`；Windows 工具显示使用 `\\wsl.localhost\<distro>\home\<user>\<project>` |
| 面向用户输出的项目内文件引用（agent 在 Windows） | `\\wsl.localhost\<distro>\home\<user>\<project>\<relative-path>` |

- `<distro>` 是 WSL 发行版名，用 `wsl.exe -l -v` 查看。
- 回复用户时，凡引用项目内文件都按用户当前环境可打开的路径输出；项目在 WSL 且用户从 Windows 桌面访问时，Markdown 链接、普通文本路径、审查证据路径、截图说明和最终总结中的项目内文件路径都使用 `\\wsl.localhost\<distro>\...`。
- 只有命令参数、WSL shell 上下文和日志原文保留 `/home/<user>/<project>`。
- **不再使用 `/mnt/<drive>`**——代码不在 Windows 盘。

## 执行环境分工（agent 在 Windows 时）

| 操作类型 | 执行方式 |
|---------|---------|
| 看代码、改代码、读写文件、搜索、规则检查 | Git Bash / bash，经 `//wsl.localhost/...` 或等价 Windows 可访问路径访问 |
| 普通 git 盘点、提交、拉取 | Git Bash / bash（经 `//wsl.localhost/...`），仅在仓库本身要求时再切 WSL |
| 编译 / 运行 / 启动程序 / 测试 / 调试 / 执行类依赖安装 | `wsl.exe --cd /home/<user>/<project> <command>` |

读写文件无论落在哪一层执行，都必须保持 UTF-8；Git Bash / bash 下优先使用脚本或工具的显式 UTF-8 选项，PowerShell 专项写文件时显式带 `-Encoding UTF8`，WSL / Linux 侧不把仓库文本转换为 GBK、ANSI 或其他本地编码。

## 命令模板（agent 在 Windows 时）

默认发行版省略 `-d`；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`：

```bash
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
- 不要为了调试或测试方便，把启动参数、环境变量或配置文件切到 `test` / `prod` / `staging` 等非 local 环境；local 不可用时记录为本地环境阻断。
- 不要把 WSL 路径（`/home/...`）和 Windows 路径混用在同一命令上下文。
- 不要在面向 Windows 桌面用户的项目内文件引用里输出 `/home/...` 作为可打开路径；这类路径应转换成 `\\wsl.localhost\...`。
- 不要把普通搜索、读文件、规则检查这类非执行动作一律切进 WSL。
- agent 在 Windows 时，不要把 PowerShell 当普通仓库命令的默认 shell；只有 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时才使用 PowerShell。
- 纯 Windows 项目，或本轮根本不会启动/执行程序的任务，不要为了“统一口径”硬套 WSL。
- 不要再用 `/mnt/<drive>`——代码已在 WSL，用 `/home/<user>/...` 与 `\\wsl.localhost\...`。

## 约束总结

**代码在 WSL 时：agent 在 WSL 直接干；agent 在 Windows 时普通仓库命令优先使用 Git Bash / bash，仅在编译、运行、启动程序、测试、调试等执行类动作时再用 `wsl.exe --cd` 进 WSL；PowerShell 只用于 Windows 专项场景。**

**所有代码、文档、配置、脚本、测试资产和生成类文本写入都必须保持 UTF-8；执行环境分层只决定命令在哪一侧运行，不改变文件编码规则。**

## 与其他规则的协作

- 涉及文件写入编码、Windows 中文编码、Git Bash / bash UTF-8 基线、PowerShell 专项 UTF-8 初始化与落盘细节时，联动 `windows-encoding-rules`。
- 涉及仓库长期规则沉淀时，联动 `project-agents-bootstrap`，把本规范写入仓库规则文件（`AGENTS.md` / `CLAUDE.md`）。

## 参考资料读取规则

- 默认先读 `references/command-templates.md`
- 需要路径访问细节时读 `references/path-mapping.md`
- 需要团队工作流时读 `references/recommended-workflow.md`
