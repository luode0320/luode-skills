# 团队推荐目录与工作流

为"Windows 编辑、WSL 运行 Go 项目"的团队提供一套简单流程。代码留在 Windows 目录，Go 进程通过 `wsl.exe` 在 WSL 中启动，路径直接用 `/mnt/<drive>/...`，无需 bind mount。

## 推荐目录

项目真实文件放在 Windows 盘符目录，例如：

- `D:\luode\<project>` → WSL 路径 `/mnt/d/luode/<project>`

## 协作分工

- **Windows 侧（Git Bash / 编辑器）**：
  - Codex 桌面端 / VSCode 编辑真实文件
  - 看代码、改代码、文件搜索
  - git 提交、拉取、status / diff / log
- **WSL 侧**：
  - 编译、测试、运行、调试
  - 依赖下载（`go mod download` / `go get`）
  - 所有需要联网的 Go 进程

## VS Code 用法

二选一即可：

1. 直接打开 Windows 目录 `D:\luode\<project>`
2. 用 WSL Remote 打开 `/mnt/d/luode/<project>`

两者都可行，但 Go 命令执行仍落在 WSL 中。

## 命令入口

从 Windows 侧通过 `wsl.exe --cd` 进入 WSL 执行（默认发行版；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`）：

```powershell
wsl.exe --cd /mnt/d/luode/<project> go test ./...
wsl.exe --cd /mnt/d/luode/<project> go run ./cmd/<app>
```

## 缓存目录建议

为减少 Windows 盘缓存问题，在 WSL 中设置（写入 shell 配置持久生效）：

```bash
export GOCACHE=$HOME/.cache/go-build
export GOMODCACHE=$HOME/go/pkg/mod
```

## 注意事项

- 代码留在 Windows 目录，不要为了运行而迁移到 WSL 文件系统。
- 不要把 Windows 路径直接传给 WSL 内部命令；`--cd` 后用 `/mnt/<drive>/...`。
- 如需固定化操作，可在 Windows 侧封装统一入口脚本：统一工作目录、统一 Go 缓存目录、统一 WSL 发行版名。
