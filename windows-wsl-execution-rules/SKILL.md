---
name: windows-wsl-execution-rules
description: 当仓库代码位于 Windows 目录（C:\、D:\ 等盘符路径），但 Go 进程需要在 WSL 中运行时触发。核心约束：代码留在 Windows 目录不迁移；看代码/改代码/git 操作用 Git Bash；go build/run/test/dlv/mod 等一切 Go 运行行为必须通过 wsl.exe 进入 WSL 执行（Windows 上启动的 Go 进程无法联网，且二进制面向 Linux）。执行方式直接用 WSL 自动挂载路径 /mnt/<drive>/...，无需 bind mount 或手动挂载；命令格式 wsl.exe -d <distro> --cd <wsl_path> <command>。不要用它代替具体语言/框架实现、测试策略或编码规则。
---

# Windows 目录 + WSL 运行项目规范

## 适用场景

仓库代码保留在 Windows 文件系统中，但 Go 进程必须在 WSL 中启动时使用本规范。典型情况：

- Codex Desktop / VSCode 运行在 Windows 上
- 项目代码位于 `D:\luode\...` 或 `C:\Users\...`
- Windows 上启动的 Go 进程无法联网
- 需要在 WSL 中执行 `go test`、`go run`、`dlv` 等命令

## 核心原则

1. 代码文件保留在 Windows 目录，不要求迁移到 WSL 文件系统。
2. 看代码、改代码、git 操作（提交、拉取、status/diff/log）用 Git Bash 直接在 Windows 侧完成。
3. 所有 Go 运行行为（build/run/test/dlv/mod）都通过 `wsl.exe` 进入 WSL 执行。
4. 进入 WSL 后路径使用 WSL 自动挂载格式 `/mnt/<drive>/...`，**不需要 bind mount 或手动挂载**。
5. 依赖下载、测试、构建、调试统一在 WSL 中完成。

## 执行环境分工

| 操作类型 | 执行环境 |
|---------|---------|
| 看代码、改代码（读写文件、搜索、列目录） | Git Bash |
| git 提交、拉取、status / diff / log | Git Bash |
| 编译 `go build` | **WSL** |
| 运行 `go run` / 启动服务 | **WSL** |
| 测试 `go test` | **WSL** |
| 调试 `dlv` | **WSL** |
| 依赖 `go mod download` / `go get` | **WSL** |

**为什么 Go 进程必须走 WSL：** Windows 上启动的 Go 进程无法联网，且编译产物面向 Linux；只有 WSL 进程才能正常运行和联网。

## 路径约定

代码留在 Windows 目录，执行时换算为 WSL 自动挂载路径：

| Windows 路径 | WSL 路径 |
|-------------|---------|
| `D:\luode\<project>` | `/mnt/d/luode/<project>` |
| `C:\Users\luode\...\w-m` | `/mnt/c/Users/luode/.../w-m` |

换算规则：盘符转小写 → 去掉 `:` → `\` 改为 `/` → 前缀 `/mnt/`。

- 不要把 Windows 路径（`D:\...`）直接传给 WSL 内部命令。
- 从 PowerShell / Git Bash 启动 WSL 时，用 `wsl.exe --cd <wsl_path>` 指定工作目录。

## 命令模板

默认使用 WSL 默认发行版（命令省略 `-d`）；如有多个发行版需指定，先用 `wsl.exe -l -v` 查看实际名称，再加 `-d <发行版名>`：

```powershell
# 测试
wsl.exe --cd /mnt/d/luode/<project> go test ./...

# 运行
wsl.exe --cd /mnt/d/luode/<project> go run ./cmd/<app>

# 调试
wsl.exe --cd /mnt/d/luode/<project> dlv debug ./cmd/<app>

# 依赖下载
wsl.exe --cd /mnt/d/luode/<project> go mod download
```

## WSL 内缓存目录建议

为减少 Windows 盘带来的缓存问题，建议在 WSL 中设置（可写入 shell 配置持久生效）：

```bash
export GOCACHE=$HOME/.cache/go-build
export GOMODCACHE=$HOME/go/pkg/mod
```

## 依赖管理规则

`go mod download` / `go get` / `go test` / `go run` / `dlv` 都应在 WSL 内执行，不要在 Windows 本地 Go 环境中执行。

## 排障

出现以下问题，优先按 WSL 运行链路排查：

- Windows 侧 Go 无法联网
- 依赖下载失败
- `go test` 行为和 WSL 不一致
- 进程启动后无法访问外部网络

## 不推荐做法

- 不要直接在 Windows 原生 Go 环境中跑需要联网的项目。
- 不要混用 Windows 路径和 WSL 命令上下文。
- 不要为了运行而来回迁移仓库存放位置。
- 不要把"代码在 Windows"误解为"只能用 Windows 进程运行"。

## 约束总结

**代码可以留在 Windows 目录，但 Go 进程必须通过 `wsl.exe` 在 WSL 中启动。**

## 与其他规则的协作

- 涉及 Windows 中文编码、PowerShell 落盘细节时，联动 `windows-encoding-rules`。
- 涉及仓库长期规则沉淀时，联动 `project-agents-bootstrap`，把本规范写入仓库规则文件（`AGENTS.md` / `CLAUDE.md`）。

## 参考资料读取规则

- 默认先读 `references/command-templates.md`
- 需要路径换算细节时读 `references/path-mapping.md`
- 需要 VSCode 调试配置时读 `references/vscode-debug-config.md`
- 需要团队工作流时读 `references/recommended-workflow.md`
