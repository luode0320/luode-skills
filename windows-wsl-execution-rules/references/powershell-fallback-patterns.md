# PowerShell 专项保底模式

这份 reference 只在已经确认“当前动作必须进入 PowerShell”的前提下使用。
默认 shell 路由仍然遵循主 skill：普通仓库命令优先 Git Bash / bash，执行类命令优先 `wsl.exe --cd` 进入 WSL。PowerShell 专项入口默认使用 PowerShell 7+ 的 `pwsh`；`powershell.exe` 5.1 只在 PowerShell 7 安装/升级被阻断时作为兼容回退。

## 适用场景

- 运行 `.ps1` 脚本
- 使用 Windows 专用 cmdlet
- 做 PowerShell profile / 编码初始化
- 用户明确要求 PowerShell

## 运行时选择

1. 进入专项场景前，先运行 `pwsh -NoProfile -Command '$PSVersionTable.PSVersion'`，确认主版本至少为 7。
2. 如果 `pwsh` 不存在或版本不满足，先调用 `windows-powershell-environment-rules` 完成环境审计/安装；不要直接把 `powershell.exe` 当成默认入口。
3. 环境准备因权限、网络或包管理器被阻断时，才允许用 `powershell.exe -NoProfile` 回退到 Windows PowerShell 5.1，并在 Web cmdlet 中显式加 `-UseBasicParsing`。
4. 调用环境入口时读取 JSON `status`：`ready` 或 `degraded` 可以继续当前 PowerShell 专项动作；`blocked`、`busy`、`failed` 或 `rollback_refused` 必须停止。`SessionEnsure` 默认只检查 `RequiredOnly`，不能因为扩展工具缺失而强行改走 5.1。
5. Windows CLI 在 Git Bash 中不可见时，先让环境 Skill 从 `git.exe` 安装根目录的 `bin\\bash.exe` 并以 `uname -s` 的 `MINGW|MSYS` 验证；不得用裸 `bash.exe`。若实际命中 `wsl.exe`、Linux `127` 或 `/mnt/*.exe`，保持本 skill owner，不调用 Windows 包安装恢复。

## 语法保底规则

### 1. 逻辑运算里的 cmdlet 必须加括号

```powershell
if ((Test-Path "a") -or (Test-Path "b")) { ... }
if ((Get-Item $x) -and ($y -eq 5)) { ... }
```

不要写：

```powershell
if (Test-Path "a" -or Test-Path "b") { ... }
```

### 2. 脚本默认 ASCII-only

- 状态文本用 `[OK]`、`[WARN]`、`[X]`
- 不在 `.ps1` 和 inline PowerShell 里放 emoji、勾叉符号或花体字符

### 3. 属性访问前先 null check

```powershell
if ($array -and $array.Count -gt 0) { ... }
if ($text) { $text.Length }
```

不要直接假设对象一定存在。

### 4. 复杂插值先落变量

```powershell
$value = $obj.prop.sub
Write-Output "Value: $value"
```

不要把过长属性链直接塞进字符串插值里。

## 路径与调用规则

### 1. 变量路径优先 `Join-Path`

```powershell
$configPath = Join-Path $env:USERPROFILE "config.json"
$dataDir = Join-Path $ScriptDir "data"
```

### 2. 带空格的可执行文件路径要加引号，并配合 `&`

```powershell
& "C:\Program Files\dotnet\dotnet.exe" build ...
```

### 3. 文件系统操作优先 PowerShell 原生命令

| 动作 | 不推荐 | 推荐 |
| --- | --- | --- |
| 删除 | `del /f /q file` | `Remove-Item -Force file` |
| 复制 | `copy a b` | `Copy-Item a b` |
| 移动 | `move a b` | `Move-Item a b` |
| 建目录 | `mkdir folder` | `New-Item -ItemType Directory -Path folder` |

## 编码与重定向

### 1. 写文件显式 UTF-8

```powershell
Get-Content -Encoding UTF8 file.txt
Set-Content -Encoding UTF8 file.txt $content
Out-File -Encoding utf8 file.txt
```

### 2. 老版 Windows PowerShell 遇到重定向乱码时显式转 UTF-8

```powershell
Get-Content log.txt | Set-Content -Encoding utf8 log_utf8.txt
```

### 3. 5.1 Web cmdlet 回退参数

Windows PowerShell 5.1 的 `Invoke-WebRequest`、`Invoke-RestMethod` 及 `iwr` / `irm` 别名必须显式使用 `-UseBasicParsing`。PowerShell 7 默认路径不需要依赖该兼容开关，但保留它不会改变主路由。

### 4. 需要把错误也写进 UTF-8 日志时

```powershell
some-command 2>&1 | Out-File -Encoding UTF8 log.txt
```

是否需要这类重定向补救，继续受 `windows-encoding-rules` 约束。

## JSON 与错误处理

### 1. `ConvertTo-Json` 显式带 `-Depth`

```powershell
$json = $data | ConvertTo-Json -Depth 10
```

### 2. `try/catch/finally` 保持简单

- 开发期优先失败快：`$ErrorActionPreference = "Stop"`
- 清理动作放 `finally`
- 不在 `try` 里把控制流写得过碎

## 最小模板

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

try {
    Write-Output "[OK] Done"
    exit 0
}
catch {
    Write-Warning "Error: $_"
    exit 1
}
```

## 与主 skill 的关系

- 这份 reference 解决“既然已经进了 PowerShell，那怎么别踩坑”；专项运行时优先是 `pwsh` 7+
- 不回答“当前任务该不该进 PowerShell”
- “该不该进” 仍由 `windows-wsl-execution-rules/SKILL.md` 的主路由决定
- 环境 Skill 只管理 Windows 用户级 PowerShell、Windows CLI 和已确认的 Git Bash 可见性；它的 Windows 侧成功不等于 WSL 原生工具可用。WSL 工具继续使用 `command -v` 和本 skill 的恢复链路验证。
