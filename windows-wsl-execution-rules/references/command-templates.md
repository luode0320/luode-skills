# 命令模板

代码放在 WSL 文件系统内（`/home/<user>/<project>`）。只有执行类命令进入 WSL；普通命令仍优先 Git Bash / bash。

## agent 在 WSL（推荐）

直接执行，无需包裹：

```bash
cd /home/<user>/<project>

go build ./...
go test ./...
go run ./cmd/<app>
dlv debug ./cmd/<app>
go mod download
```

## agent 在 Windows（如 Claude Desktop GUI）

shell 默认用 Git Bash；执行类命令通过 `wsl.exe --cd` 进 WSL。默认发行版省略 `-d`，多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`。

普通命令示例（留在 Git Bash / bash）：

```bash
cd //wsl.localhost/<distro>/home/<user>/<project>
rg "TODO"
git status
```

```powershell
# 编译
wsl.exe --cd /home/<user>/<project> go build ./...

# 测试
wsl.exe --cd /home/<user>/<project> go test ./...

# 运行 / 启动服务
wsl.exe --cd /home/<user>/<project> go run ./cmd/<app>

# 调试
wsl.exe --cd /home/<user>/<project> dlv debug ./cmd/<app>

# 依赖下载
wsl.exe --cd /home/<user>/<project> go mod download
```

看代码、改代码、搜索、规则检查和多数 git 操作用 Git Bash / bash，经 `\\wsl.localhost\<distro>\home\<user>\<project>` 访问 WSL 文件。

## WSL 内缓存目录建议

```bash
export GOCACHE=$HOME/.cache/go-build
export GOMODCACHE=$HOME/go/pkg/mod
```

## 说明

- `<distro>` 是 WSL 发行版名，用 `wsl.exe -l -v` 查看。
- 代码已在 WSL，不再使用 `/mnt/<drive>` 路径。
- 若命令依赖 `nvm`、`asdf`、`pyenv` 等 shell 初始化，可改用 `wsl.exe --cd /home/<user>/<project> bash -lic "<command>"`。
- 纯 Windows 项目，或当前任务不会真实启动程序时，不要因为模板存在就误切 WSL。
