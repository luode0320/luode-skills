# PowerShell 专项保底模式

这份 reference 只在已经确认“当前动作必须进入 PowerShell”的前提下使用。
默认 shell 路由仍然遵循主 skill：普通仓库命令优先 Git Bash / bash，执行类命令优先 `wsl.exe --cd` 进入 WSL，PowerShell 只是专项入口。

## 适用场景

- 运行 `.ps1` 脚本
- 使用 Windows 专用 cmdlet
- 做 PowerShell profile / 编码初始化
- 用户明确要求 PowerShell

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

### 3. 需要把错误也写进 UTF-8 日志时

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

- 这份 reference 解决“既然已经进了 PowerShell，那怎么别踩坑”
- 不回答“当前任务该不该进 PowerShell”
- “该不该进” 仍由 `windows-wsl-execution-rules/SKILL.md` 的主路由决定
