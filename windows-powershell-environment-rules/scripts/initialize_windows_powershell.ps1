[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet("Audit", "Apply", "Rollback", "SessionEnsure", "RecoverCommand")]
    [string]$Mode = "Audit",
    [ValidateSet("Core", "Extended")]
    [string]$ToolBundle = "Extended",
    [ValidateSet("Auto", "Winget", "Scoop", "Chocolatey")]
    [string]$PackageManager = "Auto",
    [string]$TerminalSettingsPath,
    [switch]$SkipTerminalDefault,
    [switch]$SkipToolInstall,
    [string]$JournalPath,
    [string]$OnlyCommand,
    [string]$CommandPackageId,
    [string]$CommandProbe = "--version",
    [ValidateSet("winget", "scoop-existing", "chocolatey-existing")]
    [string]$CommandSource,
    [string]$StateDirectory,
    [int]$SessionTtlMinutes = 360
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = Split-Path -Parent $scriptRoot
$manifestPath = Join-Path $skillRoot "references\tool-manifest.yaml"
$fixedProfileGuid = "{0f6c1b72-7c86-4a5f-a8f4-3e9ac8f5e6c1}"
$stateRoot = if ($StateDirectory) { $StateDirectory } else { Join-Path $env:LOCALAPPDATA "Codex\windows-powershell-environment" }
if (-not $JournalPath) {
    $JournalPath = Join-Path $stateRoot "last-run.json"
}
$discoveredToolsPath = Join-Path $stateRoot "discovered-tools.json"
$failureCasebookPath = Join-Path $stateRoot "failure-cases.json"
$sessionMarkerPath = Join-Path $stateRoot "session-marker.json"
$sessionLockPath = Join-Path $stateRoot "session.lock"

# 输出不进入成功对象流，避免状态文本污染恢复结果。
# [参数] Level 日志级别；Message 脱敏状态文本
# [返回] 无
# 最近修改时间: 2026-07-12 15:12:00，将状态改为 Information 流以保持对象返回值可组合。
function Write-Status {
    param([string]$Level, [string]$Message)
    # 1. 将状态写入 Information 流，保持成功对象流只包含业务结果。
    Write-Information ("[{0}] {1}" -f $Level, $Message) -InformationAction Continue
}

function Test-IsWindows {
    return ($env:OS -eq "Windows_NT")
}

function Test-IsAdministrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# 合并进程、机器和用户 PATH，并去除重复段。
# [参数] 无
# [返回] 无
# 最近修改时间: 2026-07-12 15:12:00，保留进程注入路径并避免递归拼接导致环境变量超长。
function Update-ProcessPath {
    # 1. 合并三个 PATH 来源并按原顺序去重，避免子进程环境逐次膨胀。
    $processPath = [Environment]::GetEnvironmentVariable("Path", "Process")
    $machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $parts = @($processPath, $machinePath, $userPath) |
        ForEach-Object { if ($_){ $_ -split ';' } } |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        Select-Object -Unique
    if ($parts.Count -gt 0) {
        $env:Path = ($parts -join ";")
    }
}

function Find-Command {
    param([string]$Name)
    Update-ProcessPath
    $command = @(Get-Command $Name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1)
    if ($command) {
        $commandPath = [string]$command.Path
        if ($commandPath) {
            return $commandPath
        }
        return [string]$command.Source
    }
    return $null
}

# 探测命令真实路径、版本文本和主版本门槛。
# [参数] CommandName 命令名；Probe 版本参数
# [返回] 包含 path、version、major、success 的对象
# 最近修改时间: 2026-07-12 15:12:00，PowerShell 7 需要真实解析主版本而非仅判断进程存在。
function Get-VersionProbe {
    param([string]$CommandName, [string]$Probe)
    # 1. 解析真实路径并执行版本探针。
    $path = Find-Command $CommandName
    if (-not $path) {
        return [pscustomobject]@{ path = $null; version = $null; major = $null; success = $false }
    }
    try {
        # 2. PowerShell 7 使用自身版本表，确保 5.1/6.x 不被误判为合格。
        if ($CommandName -eq "pwsh.exe") {
            $version = & $path -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' 2>&1
            $text = ($version | Out-String).Trim()
            $parsed = $null
            $success = [version]::TryParse($text, [ref]$parsed)
            return [pscustomobject]@{ path = $path; version = $text; major = if ($success) { $parsed.Major } else { $null }; success = ($success -and $LASTEXITCODE -eq 0) }
        } else {
            $version = & $path $Probe 2>&1
        }
        $text = ($version | Out-String).Trim()
        return [pscustomobject]@{ path = $path; version = $text; major = $null; success = ($LASTEXITCODE -eq 0) }
    } catch {
        return [pscustomobject]@{ path = $path; version = $_.Exception.Message; major = $null; success = $false }
    }
}

function Get-TerminalSettingsCandidate {
    if ($TerminalSettingsPath) {
        return (Resolve-Path -LiteralPath $TerminalSettingsPath -ErrorAction Stop).Path
    }
    [array]$candidates = @(
        (Join-Path $env:LOCALAPPDATA "Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"),
        (Join-Path $env:LOCALAPPDATA "Microsoft\Windows Terminal\settings.json")
    ) | Where-Object { Test-Path -LiteralPath $_ }
    if ($candidates.Count -eq 1) {
        return $candidates[0]
    }
    if ($candidates.Count -eq 0) {
        return $null
    }
    throw "Multiple Windows Terminal settings files found; pass -TerminalSettingsPath explicitly."
}

function ConvertFrom-Jsonc {
    param([string]$Text)
    $builder = [Text.StringBuilder]::new()
    $inString = $false
    $escaped = $false
    $lineComment = $false
    $blockComment = $false
    for ($index = 0; $index -lt $Text.Length; $index++) {
        $character = $Text[$index]
        $next = if ($index + 1 -lt $Text.Length) { $Text[$index + 1] } else { [char]0 }
        if ($lineComment) {
            if ($character -eq "`n") { $lineComment = $false; [void]$builder.Append($character) }
            continue
        }
        if ($blockComment) {
            if ($character -eq "*" -and $next -eq "/") { $blockComment = $false; $index++ }
            continue
        }
        if ($inString) {
            [void]$builder.Append($character)
            if ($escaped) { $escaped = $false }
            elseif ($character -eq "\") { $escaped = $true }
            elseif ($character -eq '"') { $inString = $false }
            continue
        }
        if ($character -eq '"') { $inString = $true; [void]$builder.Append($character); continue }
        if ($character -eq "/" -and $next -eq "/") { $lineComment = $true; $index++; continue }
        if ($character -eq "/" -and $next -eq "*") { $blockComment = $true; $index++; continue }
        [void]$builder.Append($character)
    }
    $withoutComments = $builder.ToString()
    $withoutTrailingCommas = [regex]::Replace($withoutComments, ",\s*([}\]])", '$1')
    return ($withoutTrailingCommas | ConvertFrom-Json)
}

function Write-Utf8NoBom {
    param([string]$Path, [string]$Content)
    $encoding = [Text.UTF8Encoding]::new($false)
    [IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Save-Json {
    param([object]$Value, [string]$Path)
    $content = $Value | ConvertTo-Json -Depth 30
    Write-Utf8NoBom -Path $Path -Content ($content + [Environment]::NewLine)
}

# 读取 canonical manifest，并合并经过验证的用户级 discovered 工具。
# [参数] 无
# [返回] 当前工具条目数组
# 最近修改时间: 2026-07-12 15:12:00，增加动态状态 schema 与白名单校验，阻止篡改状态诱导安装。
function Read-Manifest {
    # 1. 读取 canonical manifest 的最小字段集。
    $entries = @()
    foreach ($line in (Get-Content -LiteralPath $manifestPath -Encoding UTF8)) {
        if ($line -match '^\s+- id:\s*(\S+)\s*$') {
            $entries += [pscustomobject]@{ id = $Matches[1]; command = $null; probe = "--version"; minimum_major = $null; discovered = $false }
        } elseif ($line -match '^\s+command:\s*(\S+)\s*$' -and $entries.Count -gt 0) {
            $entries[-1].command = $Matches[1]
        } elseif ($line -match '^\s+version_probe:\s*''(.*)''\s*$' -and $entries.Count -gt 0) {
            $entries[-1].probe = $Matches[1]
        } elseif ($line -match '^\s+minimum_major:\s*(\d+)\s*$' -and $entries.Count -gt 0) {
            $entries[-1].minimum_major = [int]$Matches[1]
        }
    }
    # 2. 仅合并 verified 且通过 ID、命令和来源白名单的动态条目。
    $discovered = Read-JsonOrDefault -Path $discoveredToolsPath -DefaultValue ([pscustomobject]@{ tools = @() })
    $discoveredItems = if ((Get-PropertyNames $discovered) -contains "tools") { @($discovered.tools) } else { @() }
    foreach ($item in $discoveredItems) {
        $itemProperties = Get-PropertyNames $item
        $sourceAllowed = (-not ($itemProperties -contains "source")) -or ([string]$item.source -in @("", "winget", "scoop-existing", "chocolatey-existing"))
        $idAllowed = ([string]$item.id -match '^[A-Za-z0-9][A-Za-z0-9._-]+$')
        $commandAllowed = ([string]$item.command -match '^[A-Za-z0-9._-]+\.(exe|cmd|bat|ps1)$')
        if (($itemProperties -contains "id") -and ($itemProperties -contains "command") -and ($itemProperties -contains "versionProbe") -and ($itemProperties -contains "verified") -and [bool]$item.verified -and $sourceAllowed -and $idAllowed -and $commandAllowed -and $item.versionProbe) {
            # 动态字段组：包 ID、命令、探针和 verified 标记共同构成可复用安装契约。
            $entries += [pscustomobject]@{ id = [string]$item.id; command = [string]$item.command; probe = [string]$item.versionProbe; minimum_major = $null; discovered = $true }
        }
    }
    # 3. Core 保留核心 canonical 工具，同时不丢失已验证动态工具。
    if ($ToolBundle -eq "Core") {
        $core = @("Microsoft.PowerShell", "BurntSushi.ripgrep.MSVC", "sharkdp.fd", "junegunn.fzf", "jqlang.jq")
        return @($entries | Where-Object { $_.id -in $core -or $_.discovered })
    }
    return $entries
}

# 发现本机已存在且允许使用的包管理器入口。
# [参数] 无
# [返回] 包管理器名称与可执行路径对象数组
# 最近修改时间: 2026-07-12 15:12:00，兼容 Scoop 外部脚本入口并保持来源白名单。
function Get-PackageManagers {
    # 1. 按固定优先级发现本机已有的包管理器。
    $managers = @()
    $winget = Find-Command "winget.exe"
    $scoop = Find-Command "scoop.cmd"
    if (-not $scoop) {
        $scoopCommand = Get-Command "scoop.ps1" -CommandType ExternalScript -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($scoopCommand) { $scoop = [string]$scoopCommand.Source }
    }
    $choco = Find-Command "choco.exe"
    if ($winget) { $managers += [pscustomobject]@{ name = "Winget"; path = $winget } }
    if ($scoop) { $managers += [pscustomobject]@{ name = "Scoop"; path = $scoop } }
    if ($choco) { $managers += [pscustomobject]@{ name = "Chocolatey"; path = $choco } }
    return $managers
}

function Install-WithManager {
    param([object]$Entry, [object]$Manager)
    Write-Status "INFO" ("Installing {0} via {1}" -f $Entry.id, $Manager.name)
    if ($Manager.name -eq "Winget") {
        & $Manager.path install --id $Entry.id --exact --source winget --scope user --silent --disable-interactivity --accept-source-agreements --accept-package-agreements
    } elseif ($Manager.name -eq "Scoop") {
        & $Manager.path install $Entry.id
    } else {
        if (-not (Test-IsAdministrator)) { throw "Chocolatey installation requires an elevated PowerShell session." }
        & $Manager.path install $Entry.id --yes --no-progress
    }
    if ($LASTEXITCODE -ne 0) { throw ("{0} returned exit code {1}." -f $Manager.name, $LASTEXITCODE) }
}

# 检查、安装并用真实版本探针验证单个工具条目。
# [参数] Entry 工具条目；Managers 可用包管理器；Installed 已安装 ID 集合
# [返回] 工具验证结果对象
# 最近修改时间: 2026-07-12 15:12:00，加入最低主版本校验并保持一次恢复预算。
function Ensure-Entry {
    param([object]$Entry, [object[]]$Managers, [System.Collections.ArrayList]$Installed)
    # 1. 先探针检查并应用最低版本门槛。
    $existing = Get-VersionProbe -CommandName $Entry.command -Probe $Entry.probe
    # 2. 版本低于 manifest 门槛时继续进入安装路径，避免只因命令存在而跳过升级。
    $minimumMajor = if ((Get-PropertyNames $Entry) -contains "minimum_major" -and $null -ne $Entry.minimum_major) { [int]$Entry.minimum_major } else { $null }
    $meetsMinimum = ($null -eq $minimumMajor -or ($null -ne $existing.major -and [int]$existing.major -ge $minimumMajor))
    if ($existing.path -and $existing.success -and $meetsMinimum) {
        Write-Status "OK" ("{0}: {1} [{2}]" -f $Entry.command, $existing.version, $existing.path)
        return $existing
    }
    # 2. 测试或权限受限时只记录缺失，不绕过安装边界。
    if ($SkipToolInstall) {
        Write-Status "WARN" ("Missing {0}; installation skipped." -f $Entry.command)
        return $existing
    }
    $ordered = $Managers
    if ($PackageManager -ne "Auto") { $ordered = @($Managers | Where-Object { $_.name -eq $PackageManager }) }
    if ($ordered.Count -eq 0) { throw ("No usable package manager for {0}." -f $Entry.id) }
    $lastError = $null
    # 3. 每个 manager 最多进行一次安装与一次真实验证。
    foreach ($manager in $ordered) {
        try {
            Install-WithManager -Entry $Entry -Manager $manager
            [void]$Installed.Add($Entry.id)
            $verified = Get-VersionProbe -CommandName $Entry.command -Probe $Entry.probe
            $verifiedMinimum = ($null -eq $minimumMajor -or ($null -ne $verified.major -and [int]$verified.major -ge $minimumMajor))
            if (-not $verified.path -or -not $verified.success -or -not $verifiedMinimum) { throw ("{0} installed but command version verification failed." -f $Entry.command) }
            Write-Status "OK" ("Verified {0}: {1}" -f $Entry.command, $verified.version)
            return $verified
        } catch {
            $lastError = $_.Exception.Message
            Write-Status "WARN" ("{0} failed: {1}" -f $manager.name, $lastError)
        }
    }
    if ($Entry.id -eq "Microsoft.PowerShell") {
        throw ("Unable to install required package {0}: {1}" -f $Entry.id, $lastError)
    }
    Write-Status "WARN" ("Unable to install optional package {0}: {1}" -f $Entry.id, $lastError)
    return [pscustomobject]@{ path = $null; version = $lastError; success = $false }
}

function Set-TerminalPowerShellProfile {
    param([string]$Path, [string]$BackupPath)
    $original = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    if (-not (Test-Path -LiteralPath $BackupPath)) {
        Copy-Item -LiteralPath $Path -Destination $BackupPath -Force
    }
    $settings = ConvertFrom-Jsonc -Text $original
    if (-not $settings.profiles) { throw "Windows Terminal settings has no profiles object." }
    $profiles = @($settings.profiles.list)
    $matches = @($profiles | Where-Object { [string]$_.guid -eq $fixedProfileGuid })
    if ($matches.Count -eq 0) {
        $profiles += [pscustomobject]@{ guid = $fixedProfileGuid; name = "PowerShell 7"; commandline = "pwsh.exe -NoLogo"; hidden = $false }
    } elseif ($matches.Count -gt 1) {
        throw "Windows Terminal settings contains duplicate managed PowerShell 7 profiles."
    }
    $settings.profiles.list = $profiles
    $settings.defaultProfile = $fixedProfileGuid
    $tempPath = "$Path.codex.tmp"
    Save-Json -Value $settings -Path $tempPath
    Move-Item -LiteralPath $tempPath -Destination $Path -Force | Out-Null
    $roundTrip = ConvertFrom-Jsonc -Text (Get-Content -LiteralPath $Path -Raw -Encoding UTF8)
    if ([string]$roundTrip.defaultProfile -ne $fixedProfileGuid) { throw "Windows Terminal defaultProfile verification failed." }
    Write-Status "OK" ("Windows Terminal default profile is PowerShell 7: {0}" -f $Path)
}

function Invoke-EncodingBootstrap {
    $encodingScript = Join-Path (Split-Path -Parent $skillRoot) "windows-encoding-rules\scripts\enable_powershell_utf8.ps1"
    $pwsh = Find-Command "pwsh.exe"
    if (-not $pwsh) { throw "PowerShell 7 is unavailable for UTF-8 profile initialization." }
    & $pwsh -NoLogo -NoProfile -File $encodingScript
    if ($LASTEXITCODE -ne 0) { throw "UTF-8 profile initialization failed." }
}

function Write-Journal {
    param([object]$Journal)
    $parent = Split-Path -Parent $JournalPath
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    Save-Json -Value $Journal -Path $JournalPath
}

# 以临时文件替换方式保存 UTF-8 JSON 状态。
# [参数] Value 要保存的对象；Path 目标路径
# [返回] 无
# 最近修改时间: 2026-07-12 15:12:00，使用唯一临时名避免并发写入互相覆盖。
function Save-AtomicJson {
    param(
        [Parameter(Mandatory = $true)][object]$Value,
        [Parameter(Mandatory = $true)][string]$Path
    )
    # 1. 先准备目录，再用唯一临时文件原子替换目标。
    $parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $tempPath = "$Path.$PID.$([guid]::NewGuid().ToString('N')).tmp"
    Save-Json -Value $Value -Path $tempPath
    Move-Item -LiteralPath $tempPath -Destination $Path -Force | Out-Null
}

# 读取 UTF-8 JSON，解析失败时返回安全默认对象。
# [参数] Path 状态路径；DefaultValue 默认对象
# [返回] JSON 对象或默认对象
# 最近修改时间: 2026-07-12 15:12:00，为状态文件损坏提供可恢复入口。
function Read-JsonOrDefault {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][object]$DefaultValue
    )
    # 1. 文件不存在时直接使用安全默认结构。
    if (-not (Test-Path -LiteralPath $Path)) {
        return $DefaultValue
    }
    # 2. JSON 损坏时只重建状态，不把原始文本传播到案例库。
    try {
        $value = Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($null -ne $value) { return $value }
    } catch {
        Write-Status "WARN" ("Unable to read state file {0}; rebuilding it." -f $Path)
    }
    return $DefaultValue
}

# 读取对象属性名，避免 StrictMode 下访问缺失 schema 字段。
# [参数] Object 待检查对象
# [返回] 属性名数组
# 最近修改时间: 2026-07-12 15:12:00，为损坏状态文件提供统一 schema guard。
function Get-PropertyNames {
    param([object]$Object)
    # 1. 通过属性集合读取 schema，避免直接访问缺失属性触发 StrictMode。
    if ($null -eq $Object) { return @() }
    return @($Object.PSObject.Properties | ForEach-Object { $_.Name })
}

# 规范化可执行命令名并限制扩展名。
# [参数] Name 原始命令名
# [返回] 小写命令名或空值
# 最近修改时间: 2026-07-12 15:12:00，统一 manifest、恢复和案例库的命令键。
function Normalize-CommandName {
    param([string]$Name)
    # 1. 去除引号和路径前缀，并统一可执行扩展名。
    if ([string]::IsNullOrWhiteSpace($Name)) { return $null }
    $normalized = [IO.Path]::GetFileName($Name.Trim().Trim('"', "'"))
    if ($normalized -notmatch '\.(exe|cmd|bat|ps1)$') { $normalized = "$normalized.exe" }
    return $normalized.ToLowerInvariant()
}

# 清理失败摘要中的换行、凭据片段和路径信息。
# [参数] Reason 原始失败摘要
# [返回] 限长脱敏摘要
# 最近修改时间: 2026-07-12 15:12:00，避免 failure casebook 落盘敏感信息。
function ConvertTo-SafeReason {
    param([string]$Reason)
    # 1. 清理换行和凭据片段，再替换路径并限制摘要长度。
    if ([string]::IsNullOrWhiteSpace($Reason)) { return "unspecified" }
    $safe = $Reason -replace "`r|`n", " "
    $safe = $safe -replace "(?i)(token|password|secret|api[-_]?key)\s*[:=]\s*\S+", '$1=[redacted]'
    $safe = $safe -replace "(?i)(bearer\s+)[^\s]+", '$1[redacted]'
    $safe = $safe -replace "(?i)(private[-_ ]?key|authorization)\s*[:=]\s*\S+", '$1=[redacted]'
    $safe = $safe -replace "(?i)([A-Za-z]:\\|\\\\|/mnt/|/home/)[^\s]+", "<path>"
    if ($safe.Length -gt 300) { $safe = $safe.Substring(0, 300) }
    return $safe
}

# 按规范化命令名查找 canonical 或 verified discovered 映射。
# [参数] CommandName 命令名
# [返回] 首个匹配条目或空值
# 最近修改时间: 2026-07-12 15:12:00，统一恢复入口的命令映射查询。
function Get-ManifestEntryByCommand {
    param([string]$CommandName)
    # 1. 规范化命令后查询合并后的 manifest。
    $normalized = Normalize-CommandName $CommandName
    if (-not $normalized) { return $null }
    $entries = @(Read-Manifest)
    return ($entries | Where-Object { (Normalize-CommandName $_.command) -eq $normalized } | Select-Object -First 1)
}

# 原子创建环境状态锁并清理明确过期的锁文件。
# [参数] 无
# [返回] 是否成功取得锁
# 最近修改时间: 2026-07-12 15:12:00，避免会话与恢复操作并发改写同一状态。
function Acquire-SessionLock {
    # 1. 先检查明确过期锁，再用 CreateNew 保证并发竞争只有一个胜者。
    if (Test-Path -LiteralPath $sessionLockPath) {
        $lockAge = (Get-Date) - (Get-Item -LiteralPath $sessionLockPath).LastWriteTime
        if ($lockAge.TotalMinutes -lt 30) {
            return $false
        }
        Remove-Item -LiteralPath $sessionLockPath -Force -ErrorAction SilentlyContinue
    }
    try {
        $parent = Split-Path -Parent $sessionLockPath
        if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        $stream = [IO.File]::Open($sessionLockPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        $stream.Dispose()
        return $true
    } catch {
        return $false
    }
}

# 判断完整会话 marker 是否仍在 TTL 内。
# [参数] 无
# [返回] marker 是否可信且未过期
# 最近修改时间: 2026-07-12 15:12:00，拒绝负时间差和 complete=false marker。
function Test-SessionMarkerFresh {
    # 1. 只有 complete marker 且时间差在合法 TTL 内才允许跳过检查。
    $marker = Read-JsonOrDefault -Path $sessionMarkerPath -DefaultValue ([pscustomobject]@{ completedAt = $null; complete = $false })
    if ((Get-PropertyNames $marker) -contains "complete" -and -not [bool]$marker.complete) { return $false }
    if (-not $marker.completedAt) { return $false }
    try {
        $age = ((Get-Date) - [datetime]$marker.completedAt).TotalMinutes
        return ($age -ge 0 -and $age -lt $SessionTtlMinutes)
    } catch { return $false }
}

# 执行新会话环境准备，并在 journal 完整时写入 marker。
# [参数] 无（读取脚本级会话参数）
# [返回] 无
# 最近修改时间: 2026-07-12 15:12:00，增加子进程参数继承与不完整 Apply 的可重试状态。
function Invoke-SessionEnsure {
    # 1. 先复用可信 marker，避免同一会话重复安装。
    if (Test-SessionMarkerFresh) {
        Write-Status "OK" "Session environment check already completed within the TTL."
        return
    }
    # 2. 竞争锁时让另一个会话负责当前准备，避免重复改写。
    if (-not (Acquire-SessionLock)) {
        Write-Status "WARN" "Another session environment check is active; skipping duplicate work."
        return
    }
    try {
        # 3. 使用命名参数启动 Apply 子进程，并继承状态目录与测试开关。
        Write-Status "INFO" "Running automatic session environment audit/apply."
        # 子进程参数字段组：显式传递状态目录，避免自调用落到默认状态位置。
        $childArgs = @{
            Mode = "Apply"
            ToolBundle = $ToolBundle
            PackageManager = $PackageManager
            JournalPath = $JournalPath
            StateDirectory = $stateRoot
        }
        if ($TerminalSettingsPath) { $childArgs.TerminalSettingsPath = $TerminalSettingsPath }
        if ($SkipTerminalDefault) { $childArgs.SkipTerminalDefault = $true }
        if ($SkipToolInstall) { $childArgs.SkipToolInstall = $true }
        & $PSCommandPath @childArgs
        if ($LASTEXITCODE -ne 0) { throw "Automatic session environment apply failed with exit code $LASTEXITCODE." }
        # 4. journal 缺失、为空或含失败结果时不写成功 marker，保留下一会话重试机会。
        if (-not (Test-Path -LiteralPath $JournalPath)) {
            # marker 字段组：complete=false 明确阻止后续会话误跳过检查。
            Save-AtomicJson -Path $sessionMarkerPath -Value ([pscustomobject]@{ completedAt = (Get-Date).ToString("o"); ttlMinutes = $SessionTtlMinutes; complete = $false; incomplete = @("journal-missing"); version = 1 })
            Write-Status "WARN" "Automatic session environment apply produced no journal; completion marker was not trusted."
            return
        }
        $appliedJournal = Read-JsonOrDefault -Path $JournalPath -DefaultValue ([pscustomobject]@{ results = @() })
        $journalResults = if ((Get-PropertyNames $appliedJournal) -contains "results") { @($appliedJournal.results) } else { @() }
        if ($journalResults.Count -eq 0) {
            # marker 字段组：journal-invalid 保留失败原因，下一会话仍可重试。
            Save-AtomicJson -Path $sessionMarkerPath -Value ([pscustomobject]@{ completedAt = (Get-Date).ToString("o"); ttlMinutes = $SessionTtlMinutes; complete = $false; incomplete = @("journal-invalid"); version = 1 })
            Write-Status "WARN" "Automatic session environment apply journal was empty or invalid; completion marker was not trusted."
            return
        }
        $incomplete = @()
        foreach ($journalResult in $journalResults) {
            $journalResultProperties = Get-PropertyNames $journalResult
            if ($journalResultProperties -notcontains "result") {
                $incomplete += $journalResult
                continue
            }
            $resultProperties = Get-PropertyNames $journalResult.result
            if (($resultProperties -notcontains "success") -or $journalResult.result.success -eq $false) {
                $incomplete += $journalResult
            }
        }
        if ($incomplete.Count -gt 0) {
            $incompleteIds = @($incomplete | ForEach-Object { if ((Get-PropertyNames $_) -contains "id") { $_.id } else { "invalid-result" } })
            # marker 字段组：记录失败条目而不删除 journal 证据。
            Save-AtomicJson -Path $sessionMarkerPath -Value ([pscustomobject]@{ completedAt = (Get-Date).ToString("o"); ttlMinutes = $SessionTtlMinutes; complete = $false; incomplete = $incompleteIds; version = 1 })
            Write-Status "WARN" ("Automatic session environment apply is incomplete: {0}." -f ($incompleteIds -join ", "))
            return
        }
        # marker 字段组：只有所有 journal 结果成功才允许 complete=true。
        Save-AtomicJson -Path $sessionMarkerPath -Value ([pscustomobject]@{ completedAt = (Get-Date).ToString("o"); ttlMinutes = $SessionTtlMinutes; complete = $true; version = 1 })
        Write-Status "OK" "Automatic session environment check completed."
    } finally {
        Remove-Item -LiteralPath $sessionLockPath -Force -ErrorAction SilentlyContinue
    }
}

# 登记经过真实探针验证的非 canonical 工具。
# [参数] Entry 工具条目；Verification 探针结果；SourceName 包源标识
# [返回] 无
# 最近修改时间: 2026-07-12 15:12:00，写入 verified 标记供后续会话安全合并。
function Register-DiscoveredTool {
    param([object]$Entry, [object]$Verification, [string]$SourceName)
    # 1. 去除同命令旧记录并追加 verified 探针结果。
    $state = Read-JsonOrDefault -Path $discoveredToolsPath -DefaultValue ([pscustomobject]@{ version = 1; tools = @() })
    $existingItems = if ((Get-PropertyNames $state) -contains "tools") { @($state.tools) } else { @() }
    $items = @($existingItems | Where-Object { $_.command -ne $Entry.command })
    # discovered 字段组：保存来源、路径、版本和 verified 状态供后续白名单读取。
    $items += [pscustomobject]@{
        id = $Entry.id
        command = $Entry.command
        versionProbe = $Entry.probe
        source = $SourceName
        path = $Verification.path
        version = $Verification.version
        verified = $true
        registeredAt = (Get-Date).ToString("o")
    }
    Save-AtomicJson -Path $discoveredToolsPath -Value ([pscustomobject]@{ version = 1; tools = $items })
}

# 写入去重且脱敏的命令失败案例。
# [参数] CommandName 命令名；Reason 失败摘要；CaseState 案例状态
# [返回] 无
# 最近修改时间: 2026-07-12 15:12:00，修复状态参数与状态对象同名覆盖并增强坏 schema 容错。
function Register-FailureCase {
    param([string]$CommandName, [string]$Reason, [string]$CaseState = "candidate")
    # 1. 先规范化命令并过滤损坏的旧案例。
    $normalized = Normalize-CommandName $CommandName
    if (-not $normalized) { return }
    $casebook = Read-JsonOrDefault -Path $failureCasebookPath -DefaultValue ([pscustomobject]@{ version = 1; cases = @() })
    $existingCases = if ((Get-PropertyNames $casebook) -contains "cases") { @($casebook.cases) } else { @() }
    $cases = @($existingCases | Where-Object { (Get-PropertyNames $_) -contains "command" -and $_.command -ne $normalized })
    # failure case 字段组：命令、owner、脱敏原因和状态组成可追踪案例。
    $cases += [pscustomobject]@{
        command = $normalized
        category = "environment"
        owner = "windows-powershell-environment-rules"
        reason = (ConvertTo-SafeReason $Reason)
        state = $CaseState
        recordedAt = (Get-Date).ToString("o")
    }
    Save-AtomicJson -Path $failureCasebookPath -Value ([pscustomobject]@{ version = 1; cases = $cases })
}

# 按 manifest 或精确包 ID 恢复单个缺失命令。
# [参数] CommandName 命令名；PackageId 精确包 ID；Probe 版本参数；SourceName 包源
# [返回] 已验证的命令结果对象
# 最近修改时间: 2026-07-12 15:12:00，加入状态锁、未知命令 candidate 路由和动态工具登记。
function Invoke-CommandRecovery {
    param([string]$CommandName, [string]$PackageId, [string]$Probe, [string]$SourceName)
    # 1. 先取得共享状态锁，保证恢复与会话检查不会并发覆盖状态。
    if (-not (Acquire-SessionLock)) {
        throw "Another environment state operation is active; retry command recovery once after it completes."
    }
    try {
        # 2. canonical 映射优先；未知命令必须显式提供 exact package ID。
        $normalized = Normalize-CommandName $CommandName
        if (-not $normalized) {
            throw "Command recovery requires a command name."
        }
    $existing = Get-ManifestEntryByCommand $normalized
    # 3. 未知命令无精确映射时只记录 candidate，禁止猜包安装。
    if (-not $existing -and [string]::IsNullOrWhiteSpace($PackageId)) {
        Register-FailureCase -CommandName $normalized -Reason "Unknown command requires explicit exact package mapping; no package discovery was attempted." -CaseState "candidate"
            throw "Unknown command '$normalized' was not installed; provide an exact approved package mapping."
    }
    if (-not $existing -and $PackageId -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]+$') {
        Register-FailureCase -CommandName $normalized -Reason "Package ID failed the approved identifier contract." -CaseState "candidate"
            throw "Package ID for '$normalized' is not an approved exact identifier."
    }
    $entry = if ($existing) { $existing } else { [pscustomobject]@{ id = $PackageId; command = $normalized; probe = $Probe } }
    $managers = @(Get-PackageManagers)
    if ($SourceName) {
        $sourceManagerName = switch ($SourceName) {
            "winget" { "Winget" }
            "scoop-existing" { "Scoop" }
            "chocolatey-existing" { "Chocolatey" }
        }
        $managers = @($managers | Where-Object { $_.name -eq $sourceManagerName })
    }
    $installed = [System.Collections.ArrayList]::new()
    $verification = @(Ensure-Entry -Entry $entry -Managers $managers -Installed $installed | Where-Object { $_ -isnot [string] } | Select-Object -Last 1)
    if ($verification.Count -ne 1) {
        throw "Command recovery did not produce a verification result for '$normalized'."
    }
    $verification = $verification[0]
    if (-not $verification.success) {
        $failureReason = if ([string]::IsNullOrWhiteSpace([string]$verification.version)) { "command missing or installation skipped" } else { [string]$verification.version }
        Register-FailureCase -CommandName $normalized -Reason $failureReason -CaseState "blocked"
            throw "Command recovery failed for '$normalized'."
    }
    # 4. 只有非 canonical 命令才写入 discovered，避免后续 Audit 重复条目。
    if (-not $existing) {
        Register-DiscoveredTool -Entry $entry -Verification $verification -SourceName $SourceName
    }
    Register-FailureCase -CommandName $normalized -Reason "Exact manifest mapping installed and version probe verified." -CaseState "verified"
        return $verification
    } finally {
        Remove-Item -LiteralPath $sessionLockPath -Force -ErrorAction SilentlyContinue
    }
}

if (-not (Test-IsWindows)) { throw "This skill only runs on Windows." }
if (-not (Test-Path -LiteralPath $stateRoot)) { New-Item -ItemType Directory -Path $stateRoot -Force | Out-Null }

if ($Mode -eq "SessionEnsure") {
    Invoke-SessionEnsure
    exit 0
}

if ($Mode -eq "RecoverCommand") {
    $recovered = Invoke-CommandRecovery -CommandName $OnlyCommand -PackageId $CommandPackageId -Probe $CommandProbe -SourceName $CommandSource
    $recovered | ConvertTo-Json -Depth 10
    exit 0
}

if ($Mode -eq "Rollback") {
    if (-not (Test-Path -LiteralPath $JournalPath)) { throw "No journal found at $JournalPath." }
    $journal = Get-Content -LiteralPath $JournalPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($journal.terminalBackup -and (Test-Path -LiteralPath $journal.terminalBackup) -and $journal.terminalSettings) {
        Copy-Item -LiteralPath $journal.terminalBackup -Destination $journal.terminalSettings -Force
        Write-Status "OK" ("Restored Windows Terminal settings from {0}" -f $journal.terminalBackup)
    }
    Write-Status "INFO" "Package uninstall is intentionally manual; existing user tools are never removed automatically."
    exit 0
}

$managers = @(Get-PackageManagers)
$entries = @(Read-Manifest)
$installed = [System.Collections.ArrayList]::new()
$results = @()
Write-Status "INFO" ("Mode={0}; PowerShell={1}; Admin={2}; Managers={3}" -f $Mode, $PSVersionTable.PSVersion, (Test-IsAdministrator), (($managers.name -join ", ")))
foreach ($entry in $entries) {
    if ($Mode -eq "Audit") {
        $results += [pscustomobject]@{ id = $entry.id; command = $entry.command; result = (Get-VersionProbe -CommandName $entry.command -Probe $entry.probe) }
    } else {
        $results += [pscustomobject]@{ id = $entry.id; command = $entry.command; result = (Ensure-Entry -Entry $entry -Managers $managers -Installed $installed) }
    }
}

if ($Mode -eq "Apply") {
    Invoke-EncodingBootstrap
    $terminalPath = Get-TerminalSettingsCandidate
    $backupPath = $null
    if (-not $SkipTerminalDefault) {
        if (-not $terminalPath) { throw "Windows Terminal settings.json was not found." }
        $previousJournal = $null
        if (Test-Path -LiteralPath $JournalPath) {
            try {
                $previousJournal = Get-Content -LiteralPath $JournalPath -Raw -Encoding UTF8 | ConvertFrom-Json
            } catch {
                $previousJournal = $null
            }
        }
        if ($previousJournal -and $previousJournal.terminalSettings -eq $terminalPath -and $previousJournal.terminalBackup -and (Test-Path -LiteralPath $previousJournal.terminalBackup)) {
            $backupPath = $previousJournal.terminalBackup
        } else {
            $backupPath = "$terminalPath.codex.$(Get-Date -Format yyyyMMddHHmmss).bak"
        }
        Set-TerminalPowerShellProfile -Path $terminalPath -BackupPath $backupPath
    }
    Write-Journal -Journal ([pscustomobject]@{
        createdAt = (Get-Date).ToString("o")
        terminalSettings = $terminalPath
        terminalBackup = $backupPath
        installedPackageIds = @($installed)
        results = $results
    })
    Write-Status "OK" ("Journal written to {0}" -f $JournalPath)
}

if ($Mode -eq "Audit") {
    $results | ConvertTo-Json -Depth 10
}
