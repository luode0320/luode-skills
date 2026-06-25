# 团队推荐目录与工作流

代码放在 WSL 文件系统内（`/home/<user>/<project>`）。编译、运行、测试、调试都在 WSL 中完成。

## 推荐目录

- WSL 内：`/home/<user>/<project>`
- Windows 侧访问（看代码/改代码）：`\\wsl.localhost\<distro>\home\<user>\<project>`

## 两种 agent 运行位置

### agent 在 WSL（推荐）

- 直接 `cd /home/<user>/<project>` 后执行 `go test` / `go run` / `dlv`，无需任何包裹
- 进程天然在 WSL，联网正常

### agent 在 Windows（如 Claude Desktop GUI）

- shell 默认用 Git Bash
- 看代码、改代码、git：经 `\\wsl.localhost\<distro>\home\<user>\<project>` 访问
- 编译、运行、测试、调试：`wsl.exe --cd /home/<user>/<project> <command>`

## 命令入口（agent 在 Windows 时）

默认发行版省略 `-d`；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`：

```powershell
wsl.exe --cd /home/<user>/<project> go test ./...
wsl.exe --cd /home/<user>/<project> go run ./cmd/<app>
```

## 缓存目录建议

```bash
export GOCACHE=$HOME/.cache/go-build
export GOMODCACHE=$HOME/go/pkg/mod
```

## 注意事项

- 代码在 WSL 原生文件系统，I/O 性能好，无需 bind mount 或 `/mnt` 换算。
- `wsl.exe --cd` 后用 WSL 内路径 `/home/<user>/<project>`；Windows 编辑器访问用 `\\wsl.localhost\...`。
- 如需固定化操作，可在 Windows 侧封装统一入口脚本：统一工作目录、统一 WSL 发行版名。
