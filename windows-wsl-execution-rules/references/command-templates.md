# 命令模板

代码放在 WSL 文件系统内（`/home/<user>/<project>`）。只有执行类命令进入 WSL；Windows 下普通仓库命令优先使用 Git Bash / bash。PowerShell 只在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。

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

执行不需要包裹，不代表回复里的文件引用也能直接用 `/home/...`：只要用户从 Windows 桌面访问，项目内文件路径仍要转换成 `\\wsl.localhost\<distro>\home\<user>\<project>\...`（判定依据是用户查看环境，不是 agent 运行位置，规则见下方）。

这里的命令如果在 WSL 内报 `permission denied` 或行为跟预期的 Linux 版不一致，很可能是 PATH 里混进了 Windows 版同名工具（比如把 Windows 打包的 `rg.exe` 当成了 WSL 原生 `rg`）。新会话第一次执行这类命令时可顺手用 `command -v <tool>` 自检一次，排查方法见 `references/tool-path-interop.md`。

## agent 在 Windows（如 Claude Desktop GUI）

普通命令默认用 Git Bash / bash；执行类命令通过 `wsl.exe --cd` 进 WSL。默认发行版省略 `-d`，多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`。

普通命令示例（留在 Git Bash / bash）：

```bash
cd //wsl.localhost/<distro>/home/<user>/<project>
rg "TODO"
git status
```

```bash
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

看代码、改代码、搜索、规则检查和多数 git 操作都留在 Git Bash / bash，经 `//wsl.localhost/<distro>/home/<user>/<project>` 或等价 Windows 可访问路径访问 WSL 文件。PowerShell 仅用于 Windows 专项场景；使用 PowerShell 写文件时仍必须显式指定 UTF-8。

回复用户时同样按用户可访问路径引用项目内文件：项目在 WSL 且用户从 Windows 桌面访问时，普通文本路径、Markdown 链接、审查证据路径和总结路径都使用 `\\wsl.localhost\<distro>\home\<user>\<project>\...`；只有 `wsl.exe --cd` 参数、WSL shell 命令和日志原文保留 `/home/<user>/<project>`。

## PowerShell 专项模板

只有在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时才用这部分模板。

```powershell
# 逻辑运算里的 cmdlet 单独加括号
if ((Test-Path $configPath) -and ($env:APPDATA)) {
    $json = Get-Content -Encoding UTF8 $configPath -Raw | ConvertFrom-Json
}
```

```powershell
# 路径优先 Join-Path，带空格的 exe 用 & 调用
$tool = Join-Path $env:ProgramFiles "dotnet\\dotnet.exe"
& $tool build
```

```powershell
# JSON 输出显式带 Depth
$payload | ConvertTo-Json -Depth 10 | Out-File -Encoding utf8 result.json
```

```powershell
# 老版 Windows PowerShell 遇到日志乱码时显式转 UTF-8
Get-Content app.log | Set-Content -Encoding utf8 app-utf8.log
```

PowerShell 专项模板解决的是“已经进入 PowerShell 后怎么写”，不改变主路由：普通仓库命令仍优先 Git Bash / bash，执行类动作仍优先 `wsl.exe --cd` 进入 WSL。

## WSL 内缓存目录建议

```bash
export GOCACHE=$HOME/.cache/go-build
export GOMODCACHE=$HOME/go/pkg/mod
```

## 说明

- `<distro>` 是 WSL 发行版名，用 `wsl.exe -l -v` 查看。
- 代码已在 WSL，不再使用 `/mnt/<drive>` 路径。
- 若命令依赖 `nvm`、`asdf`、`pyenv` 等 shell 初始化，可改用 `wsl.exe --cd /home/<user>/<project> bash -lic "<command>"`。
- 进入 PowerShell 专项场景后，额外遵守 `references/powershell-fallback-patterns.md`。
- 纯 Windows 项目，或当前任务不会真实启动程序时，不要因为模板存在就误切 WSL。
