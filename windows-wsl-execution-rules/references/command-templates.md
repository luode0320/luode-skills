# 命令模板

代码留在 Windows 目录，Go 运行行为通过 `wsl.exe` 进入 WSL，路径直接用 WSL 自动挂载 `/mnt/<drive>/...`，无需 bind mount 或手动挂载。

默认使用 WSL 默认发行版（命令省略 `-d`）；如有多个发行版需指定，先用 `wsl.exe -l -v` 查看实际名称，再加 `-d <发行版名>`。

## 通用模板

```powershell
wsl.exe --cd <wsl_path> <command>
```

## Go 项目（团队主要技术栈）

> 看代码、改代码、git 操作用 Git Bash；编译、测试、运行、调试、依赖都走 WSL。

```powershell
# 编译
wsl.exe --cd /mnt/d/luode/<project> go build ./...

# 测试（全量）
wsl.exe --cd /mnt/d/luode/<project> go test ./...

# 测试（指定包）
wsl.exe --cd /mnt/d/luode/<project> go test ./internal/...

# 运行 / 启动服务
wsl.exe --cd /mnt/d/luode/<project> go run ./cmd/<app>

# 调试
wsl.exe --cd /mnt/d/luode/<project> dlv debug ./cmd/<app>

# 依赖下载
wsl.exe --cd /mnt/d/luode/<project> go mod download
```

## Node / pnpm / npm

```powershell
wsl.exe --cd /mnt/d/luode/<project> pnpm install
wsl.exe --cd /mnt/d/luode/<project> pnpm test
wsl.exe --cd /mnt/d/luode/<project> pnpm dev
```

## WSL 内缓存目录建议

为减少 Windows 盘缓存问题，在 WSL 中设置（可写入 shell 配置持久生效）：

```bash
export GOCACHE=$HOME/.cache/go-build
export GOMODCACHE=$HOME/go/pkg/mod
```

## 说明

- 看代码、改代码、git 提交与拉取直接在 Git Bash 用 Windows 路径执行，无需走 WSL。
- 不要把 Windows 路径（`D:\...`）直接传给 WSL 内部命令；`--cd` 后必须是 `/mnt/<drive>/...` 格式。
- 若命令依赖 `nvm`、`asdf`、`pyenv` 等 shell 初始化，可改用 `wsl.exe --cd <wsl_path> bash -lic "<command>"`。
