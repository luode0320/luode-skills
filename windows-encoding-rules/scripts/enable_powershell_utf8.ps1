[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet("Audit", "Apply", "Rollback")]
    [string]$Mode = "Apply",
    [ValidateSet("Json", "Human")]
    [string]$OutputFormat = "Human",
    [string]$TransactionPath,
    [switch]$TestMode,
    [string]$ProfileRoot,
    [switch]$SkipExecutionPolicy
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$beginMarker = "# codex-powershell-utf8-begin"
$endMarker = "# codex-powershell-utf8-end"
$utf8Block = @'
chcp 65001 > $null
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$PSDefaultParameterValues['Set-Content:Encoding'] = 'utf8'
$PSDefaultParameterValues['Add-Content:Encoding'] = 'utf8'
'@
$managedBlock = @"
$beginMarker
$utf8Block
$endMarker
"@.TrimEnd()
function New-Result {
    <#
    [参数]
    - Status：本次操作的稳定状态。
    - Message：面向调用方的简短说明。
    [返回]
    - 统一的结构化结果对象。
    最近修改时间
    2026-07-13 21:52:49：为环境编排与隔离测试提供可机器读取的结果。
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$Status,
        [Parameter(Mandatory = $true)]
        [string]$Message
    )
    # 1. 统一构造调用方可直接消费的结果字段。
    [ordered]@{
        schemaVersion = 2
        mode = $Mode
        status = $Status
        success = $Status -in @("ready", "rolled_back")
        message = $Message
        transactionPath = $TransactionPath
        executionPolicy = $null
        profiles = @()
    }
}
function Write-Result {
    <#
    [参数]
    - Result：统一结果对象。
    [返回]
    - 无；按调用方要求输出 JSON 或人类可读摘要。
    最近修改时间
    2026-07-13 21:52:49：统一成功、拒绝回滚和失败时的输出格式。
    #>
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$Result
    )
    # 1. 自动化调用优先输出 JSON，人工调用保留简短摘要。
    if ($OutputFormat -eq "Json") {
        $Result | ConvertTo-Json -Depth 12
        return
    }
    Write-Output ("PowerShell UTF-8 {0}: {1}" -f $Result.status, $Result.message)
    foreach ($profile in @($Result.profiles)) {
        $profileState = if ($profile.changed) { "已更新" } elseif ($profile.verified) { "已验证" } else { "未更新" }
        Write-Output ("[{0}] {1}: {2}" -f $profile.label, $profileState, $profile.path)
    }
}
function Get-Sha256 {
    <#
    [参数]
    - Path：需要计算摘要的文件路径。
    [返回]
    - 文件不存在时返回 $null，否则返回 SHA-256 十六进制摘要。
    最近修改时间
    2026-07-13 21:52:49：为安全回滚提供文件漂移判断依据。
    #>
    param([Parameter(Mandatory = $true)][string]$Path)
    # 1. 缺失文件没有摘要，避免把不存在误报成空文件。
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $null
    }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}
function Read-Utf8ProfileText {
    <#
    [参数]
    - Path：UTF-8 profile 文件路径。
    [返回]
    - 文本内容、是否存在以及 UTF-8 BOM 状态。
    最近修改时间
    2026-07-13 21:52:49：拒绝不安全的非 UTF-8 解码，避免覆盖旧 profile。
    #>
    param([Parameter(Mandatory = $true)][string]$Path)
    # 1. 先区分新 profile 与已有 profile，保留原始 BOM 选择。
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return [pscustomobject]@{ Exists = $false; Text = ""; HasBom = $false }
    }
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $hasBom = $bytes.Length -ge 3 -and $bytes[0] -eq 239 -and $bytes[1] -eq 187 -and $bytes[2] -eq 191
    $decoder = New-Object System.Text.UTF8Encoding($false, $true)
    try {
        $text = $decoder.GetString($bytes)
    } catch {
        throw "Profile is not valid UTF-8 and will not be changed: $Path"
    }
    if ($text.Length -gt 0 -and [int][char]$text[0] -eq 65279) {
        $text = $text.Substring(1)
    }
    return [pscustomobject]@{ Exists = $true; Text = $text; HasBom = $hasBom }
}
function Write-Utf8ProfileText {
    <#
    [参数]
    - Path：目标 profile 文件路径。
    - Text：要写入的 UTF-8 文本。
    - HasBom：是否保留原有 UTF-8 BOM。
    [返回]
    - 无。
    最近修改时间
    2026-07-13 21:52:49：以显式 UTF-8 写入并保留原 profile 的 BOM 选择。
    #>
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][bool]$HasBom
    )
    # 1. 先确保目录存在，再以显式 UTF-8 编码写入完整内容。
    $directory = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }
    $encoder = New-Object System.Text.UTF8Encoding($HasBom)
    [System.IO.File]::WriteAllText($Path, $Text, $encoder)
}
function Get-UpdatedProfileText {
    <#
    [参数]
    - Existing：profile 当前文本。
    [返回]
    - 写入 UTF-8 初始化片段后的 profile 文本。
    最近修改时间
    2026-07-13 21:52:49：拒绝重复或嵌套标记，避免静默破坏用户内容。
    #>
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Existing)
    # 1. 先验证受管标记唯一且完整，避免覆盖不确定的用户内容。
    $beginCount = [regex]::Matches($Existing, [regex]::Escape($beginMarker)).Count
    $endCount = [regex]::Matches($Existing, [regex]::Escape($endMarker)).Count
    if ($beginCount -ne $endCount -or $beginCount -gt 1) {
        throw "UTF-8 profile markers are duplicated or incomplete; manual repair is required."
    }
    $newLine = if ($Existing -match "`r`n") { "`r`n" } else { "`n" }
    if ($beginCount -eq 1) {
        $pattern = "(?s)$([regex]::Escape($beginMarker)).*?$([regex]::Escape($endMarker))"
        return [regex]::Replace($Existing, $pattern, $managedBlock)
    }
    if ([string]::IsNullOrWhiteSpace($Existing)) {
        return $managedBlock + $newLine
    }
    return $Existing.TrimEnd("`r", "`n") + $newLine + $newLine + $managedBlock + $newLine
}
function Get-PowerShell7Command {
    <#
    [参数]
    - 无。
    [返回]
    - 已验证的 PowerShell 7 应用程序信息；不可用时返回 $null。
    最近修改时间
    2026-07-13 21:52:49：继续优先 PowerShell 7，同时保留 Windows PowerShell 5.1。
    #>
    # 1. 只接受真实应用程序，并在无 profile 子进程中验证版本。
    $command = @(Get-Command pwsh -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1)
    if ($null -eq $command) {
        return $null
    }
    $path = [string]$command.Path
    if ([string]::IsNullOrWhiteSpace($path)) {
        return $null
    }
    $versionText = & $path -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' 2>$null | Select-Object -Last 1
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace([string]$versionText)) {
        return $null
    }
    try {
        $version = [version]([string]$versionText).Trim()
    } catch {
        return $null
    }
    if ($version.Major -lt 7) {
        return $null
    }
    return [pscustomobject]@{ Path = $path; Version = $version }
}
function Get-ProfilePathsFromShell {
    <#
    [参数]
    - ShellExecutable：要查询的 PowerShell 可执行文件。
    [返回]
    - 该 shell 实际报告的两个 CurrentUser profile 路径。
    最近修改时间
    2026-07-13 21:52:49：真实模式不再猜测 Documents 路径，兼容重定向目录。
    #>
    param([Parameter(Mandatory = $true)][string]$ShellExecutable)
    # 1. 由目标 shell 自己报告 profile，兼容 Documents 重定向。
    $query = '$result = [ordered]@{ allHosts = $PROFILE.CurrentUserAllHosts; currentHost = $PROFILE.CurrentUserCurrentHost }; $result | ConvertTo-Json -Compress'
    $json = & $ShellExecutable -NoLogo -NoProfile -Command $query 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace([string]$json)) {
        throw "Unable to discover profile paths from $ShellExecutable"
    }
    $paths = $json | ConvertFrom-Json
    if ([string]::IsNullOrWhiteSpace([string]$paths.allHosts) -or [string]::IsNullOrWhiteSpace([string]$paths.currentHost)) {
        throw "Profile discovery returned incomplete paths from $ShellExecutable"
    }
    return $paths
}
function Get-TargetProfiles {
    <#
    [参数]
    - 无。
    [返回]
    - 要更新或审计的 PowerShell 7 与 Windows PowerShell profile 列表。
    最近修改时间
    2026-07-13 21:52:49：测试模式使用隔离根目录，真实模式通过目标 shell 的 $PROFILE 取路径。
    #>
    # 1. 测试模式固定映射到隔离目录，真实模式只采用 shell 报告的路径。
    $targets = @()
    $powerShell7 = Get-PowerShell7Command
    if ($null -ne $powerShell7) {
        if ($TestMode) {
            $targets += [pscustomobject]@{ Label = "PowerShell7-CurrentUserAllHosts"; Path = Join-Path $ProfileRoot "PowerShell7\profile.ps1"; Shell = $powerShell7.Path }
            $targets += [pscustomobject]@{ Label = "PowerShell7-CurrentUserCurrentHost"; Path = Join-Path $ProfileRoot "PowerShell7\Microsoft.PowerShell_profile.ps1"; Shell = $powerShell7.Path }
        } else {
            $paths = Get-ProfilePathsFromShell -ShellExecutable $powerShell7.Path
            $targets += [pscustomobject]@{ Label = "PowerShell7-CurrentUserAllHosts"; Path = [string]$paths.allHosts; Shell = $powerShell7.Path }
            $targets += [pscustomobject]@{ Label = "PowerShell7-CurrentUserCurrentHost"; Path = [string]$paths.currentHost; Shell = $powerShell7.Path }
        }
    }
    $legacyShell = "powershell.exe"
    if ($TestMode) {
        $targets += [pscustomobject]@{ Label = "WindowsPowerShell-CurrentUserAllHosts"; Path = Join-Path $ProfileRoot "WindowsPowerShell\profile.ps1"; Shell = $legacyShell }
        $targets += [pscustomobject]@{ Label = "WindowsPowerShell-CurrentUserCurrentHost"; Path = Join-Path $ProfileRoot "WindowsPowerShell\Microsoft.PowerShell_profile.ps1"; Shell = $legacyShell }
    } else {
        $paths = Get-ProfilePathsFromShell -ShellExecutable $legacyShell
        $targets += [pscustomobject]@{ Label = "WindowsPowerShell-CurrentUserAllHosts"; Path = [string]$paths.allHosts; Shell = $legacyShell }
        $targets += [pscustomobject]@{ Label = "WindowsPowerShell-CurrentUserCurrentHost"; Path = [string]$paths.currentHost; Shell = $legacyShell }
    }
    return @($targets)
}
function Test-ShellUtf8Profile {
    <#
    [参数]
    - Target：待验证的 shell 与 profile 信息。
    [返回]
    - UTF-8 编码探针结果。
    最近修改时间
    2026-07-13 21:52:49：测试模式显式加载临时 profile，避免读取真实用户配置。
    #>
    param([Parameter(Mandatory = $true)][pscustomobject]$Target)
    # 1. 生成无 profile 探针；测试模式再显式加载单个临时 profile。
    $probe = @'
$result = [ordered]@{
  inputEncoding = [ordered]@{ webName = [Console]::InputEncoding.WebName; codePage = [Console]::InputEncoding.CodePage; preambleLength = ([Console]::InputEncoding.GetPreamble()).Length }
  outputEncoding = [ordered]@{ webName = [Console]::OutputEncoding.WebName; codePage = [Console]::OutputEncoding.CodePage; preambleLength = ([Console]::OutputEncoding.GetPreamble()).Length }
  dollarOutputEncoding = [ordered]@{ webName = $OutputEncoding.WebName; codePage = $OutputEncoding.CodePage; preambleLength = ($OutputEncoding.GetPreamble()).Length }
  chcp = (cmd /c chcp)
}
$result | ConvertTo-Json -Compress -Depth 6
'@
    if ($TestMode) {
        $escapedPath = $Target.Path.Replace("'", "''")
        $probe = ". '$escapedPath'`n$probe"
    }
    $json = & $Target.Shell -NoLogo -NoProfile -Command $probe 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace([string]$json)) {
        throw "UTF-8 probe returned empty output for $($Target.Shell)"
    }
    $parsed = $json | ConvertFrom-Json
    $success = $parsed.inputEncoding.webName -eq "utf-8" -and [int]$parsed.inputEncoding.codePage -eq 65001
    $success = $success -and $parsed.outputEncoding.webName -eq "utf-8" -and [int]$parsed.outputEncoding.codePage -eq 65001
    $success = $success -and $parsed.dollarOutputEncoding.webName -eq "utf-8" -and [int]$parsed.dollarOutputEncoding.codePage -eq 65001
    $success = $success -and ([string]$parsed.chcp -match "65001")
    return [pscustomobject]@{ Success = $success; Raw = $parsed }
}
function Save-Transaction {
    <#
    [参数]
    - Transaction：要持久化的事务对象。
    [返回]
    - 无。
    最近修改时间
    2026-07-13 21:52:49：每次 profile 写入后立即落盘备份与 hash 证据。
    #>
    param([Parameter(Mandatory = $true)][System.Collections.IDictionary]$Transaction)
    # 1. 为事务目录补齐父级后，持久化最新备份和 hash 证据。
    $directory = Split-Path -Parent $TransactionPath
    if (-not [string]::IsNullOrWhiteSpace($directory) -and -not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }
    $Transaction | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $TransactionPath -Encoding UTF8
}
function New-DefaultTransactionPath {
    <#
    [参数]
    - 无。
    [返回]
    - 默认 Apply 的用户级事务文件路径。
    最近修改时间
    2026-07-13 21:52:49：保留无参数调用兼容，同时为回滚保存证据。
    #>
    # 1. 无显式路径时使用用户级目录，避免污染 skill 仓库。
    $base = if ([string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) { $HOME } else { $env:LOCALAPPDATA }
    $runId = Get-Date -Format "yyyyMMddHHmmssfff"
    return (Join-Path $base "Codex\windows-encoding\runs\utf8-$runId.json")
}
function Invoke-ProfileRollback {
    <#
    [参数]
    - 无；读取 TransactionPath 指向的 Apply 事务。
    [返回]
    - 已恢复或因文件漂移拒绝恢复的结构化结果。
    最近修改时间
    2026-07-13 21:52:49：只在 Apply 后 hash 未变化时恢复，保护用户后续编辑。
    #>
    # 1. 先验证事务可读，再统一检查所有 profile 是否发生漂移。
    if ([string]::IsNullOrWhiteSpace($TransactionPath) -or -not (Test-Path -LiteralPath $TransactionPath -PathType Leaf)) {
        throw "Rollback requires an existing -TransactionPath."
    }
    $transaction = Get-Content -LiteralPath $TransactionPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ([int]$transaction.schemaVersion -ne 2 -or $null -eq $transaction.profiles) {
        throw "Transaction schema is invalid; rollback will not guess recovery data."
    }
    $result = New-Result -Status "rolled_back" -Message "UTF-8 profile transaction restored."
    $refused = @()
    foreach ($profile in @($transaction.profiles)) {
        if (-not $profile.changed) {
            continue
        }
        $currentHash = Get-Sha256 -Path ([string]$profile.path)
        if ($currentHash -ne [string]$profile.afterHash) {
            $refused += [string]$profile.path
        }
    }
    if ($refused.Count -gt 0) {
        $result.status = "rollback_refused"
        $result.success = $false
        $result.message = "Rollback refused because profiles changed after Apply: " + ($refused -join ", ")
        return $result
    }
    foreach ($profile in @($transaction.profiles)) {
        if (-not $profile.changed) {
            continue
        }
        if ($PSCmdlet.ShouldProcess([string]$profile.path, "Restore UTF-8 profile backup")) {
            if ([bool]$profile.existedBefore) {
                [System.IO.File]::WriteAllBytes([string]$profile.path, [System.IO.File]::ReadAllBytes([string]$profile.backupPath))
            } else {
                Remove-Item -LiteralPath ([string]$profile.path) -Force
            }
        }
        $result.profiles += [ordered]@{ label = $profile.label; path = $profile.path; changed = $true; verified = $true; beforeHash = $profile.beforeHash; afterHash = $profile.afterHash }
    }
    return $result
}
function Invoke-CurrentUserExecutionPolicy {
    <#
    [参数]
    - 无。
    [返回]
    - 当前用户执行策略变更状态。
    最近修改时间
    2026-07-13 21:52:49：测试与审计绝不修改执行策略，正式 Apply 保留兼容行为。
    #>
    # 1. 审计和测试只报告策略状态；正式 Apply 才可能变更 CurrentUser。
    $before = Get-ExecutionPolicy -Scope CurrentUser
    if ($TestMode -or $SkipExecutionPolicy) {
        return [ordered]@{ changed = $false; skipped = $true; before = $before; after = $before; manualRollbackOnly = $false }
    }
    if ($PSCmdlet.ShouldProcess("CurrentUser", "Set PowerShell execution policy to RemoteSigned")) {
        try {
            Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force -ErrorAction Stop
        } catch {
            $message = $_.Exception.Message
            $errorId = $_.FullyQualifiedErrorId
            $afterFailure = Get-ExecutionPolicy -Scope CurrentUser
            $overrideSucceeded = $errorId -eq "ExecutionPolicyOverride,Microsoft.PowerShell.Commands.SetExecutionPolicyCommand"
            $overrideSucceeded = $overrideSucceeded -or $message -match "updated your execution policy successfully"
            if (-not ($overrideSucceeded -and $afterFailure -eq "RemoteSigned")) {
                throw
            }
        }
    }
    $after = Get-ExecutionPolicy -Scope CurrentUser
    return [ordered]@{ changed = $before -ne $after; skipped = $false; before = $before; after = $after; manualRollbackOnly = $before -ne $after }
}

try {
    if ($TestMode) {
        if ([string]::IsNullOrWhiteSpace($ProfileRoot) -or -not [System.IO.Path]::IsPathRooted($ProfileRoot)) {
            throw "-TestMode requires an absolute temporary -ProfileRoot."
        }
        if ([System.IO.Path]::GetFullPath($ProfileRoot).TrimEnd('\\') -eq [System.IO.Path]::GetFullPath($HOME).TrimEnd('\\')) {
            throw "-TestMode ProfileRoot must not be the user home directory."
        }
        $SkipExecutionPolicy = $true
    } elseif (-not [string]::IsNullOrWhiteSpace($ProfileRoot)) {
        throw "-ProfileRoot is only allowed with -TestMode; real mode must use each shell's `$PROFILE."
    }
    if ($Mode -eq "Rollback") {
        $rollbackResult = Invoke-ProfileRollback
        Write-Result -Result $rollbackResult
        if ($rollbackResult.status -eq "rollback_refused") { exit 13 }
        exit 0
    }
    $targets = @(Get-TargetProfiles)
    if ($Mode -eq "Audit") {
        $auditResult = New-Result -Status "ready" -Message "UTF-8 profile audit completed without changes."
        foreach ($target in $targets) {
            $current = Read-Utf8ProfileText -Path $target.Path
            $markerCount = [regex]::Matches($current.Text, [regex]::Escape($beginMarker)).Count
            $verified = $markerCount -eq 1 -and [regex]::Matches($current.Text, [regex]::Escape($endMarker)).Count -eq 1
            if (-not $verified) { $auditResult.status = "needs_apply"; $auditResult.success = $false }
            $auditResult.profiles += [ordered]@{ label = $target.Label; path = $target.Path; shell = $target.Shell; changed = $false; verified = $verified; exists = $current.Exists; beforeHash = Get-Sha256 -Path $target.Path; afterHash = $null }
        }
        if ($auditResult.status -eq "needs_apply") { $auditResult.message = "One or more profiles require UTF-8 initialization." }
        Write-Result -Result $auditResult
        exit 0
    }
    if ([string]::IsNullOrWhiteSpace($TransactionPath)) {
        $TransactionPath = New-DefaultTransactionPath
    }
    $backupRoot = "$TransactionPath.backups"
    $transaction = [ordered]@{ schemaVersion = 2; mode = "Apply"; createdAt = (Get-Date).ToString("o"); testMode = [bool]$TestMode; profiles = @(); executionPolicy = $null }
    $result = New-Result -Status "ready" -Message "PowerShell UTF-8 profiles are active."
    foreach ($target in $targets) {
        $current = Read-Utf8ProfileText -Path $target.Path
        $updated = Get-UpdatedProfileText -Existing $current.Text
        $beforeHash = Get-Sha256 -Path $target.Path
        $changed = $current.Text -ne $updated
        $backupPath = $null
        if ($changed -and $PSCmdlet.ShouldProcess($target.Path, "Apply UTF-8 PowerShell profile block")) {
            if ($current.Exists) {
                if (-not (Test-Path -LiteralPath $backupRoot)) { New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null }
                $backupPath = Join-Path $backupRoot ("{0}.bak" -f ([guid]::NewGuid().ToString("N")))
                [System.IO.File]::WriteAllBytes($backupPath, [System.IO.File]::ReadAllBytes($target.Path))
            }
            Write-Utf8ProfileText -Path $target.Path -Text $updated -HasBom $current.HasBom
        }
        $afterHash = Get-Sha256 -Path $target.Path
        $profileRecord = [ordered]@{ label = $target.Label; path = $target.Path; shell = $target.Shell; existedBefore = $current.Exists; changed = $changed; backupPath = $backupPath; beforeHash = $beforeHash; afterHash = $afterHash; verified = $false }
        $transaction.profiles += $profileRecord
        if (-not $WhatIfPreference) { Save-Transaction -Transaction $transaction }
        $probe = if ($WhatIfPreference) { [pscustomobject]@{ Success = $false; Raw = $null } } else { Test-ShellUtf8Profile -Target $target }
        $profileRecord.verified = $probe.Success
        $result.profiles += [ordered]@{ label = $target.Label; path = $target.Path; shell = $target.Shell; changed = $changed; backupPath = $backupPath; beforeHash = $beforeHash; afterHash = $afterHash; verified = $probe.Success; inputEncoding = if ($null -eq $probe.Raw) { $null } else { $probe.Raw.inputEncoding }; outputEncoding = if ($null -eq $probe.Raw) { $null } else { $probe.Raw.outputEncoding }; dollarOutputEncoding = if ($null -eq $probe.Raw) { $null } else { $probe.Raw.dollarOutputEncoding }; chcp = if ($null -eq $probe.Raw) { $null } else { $probe.Raw.chcp } }
        if (-not $WhatIfPreference) { Save-Transaction -Transaction $transaction }
    }
    $result.executionPolicy = Invoke-CurrentUserExecutionPolicy
    $transaction.executionPolicy = $result.executionPolicy
    if (-not $WhatIfPreference) { Save-Transaction -Transaction $transaction }
    if ($WhatIfPreference) {
        $result.status = "what_if"
        $result.success = $true
        $result.message = "WhatIf completed without changing profiles, transaction files, or execution policy."
    } elseif (@($result.profiles | Where-Object { -not $_.verified }).Count -gt 0) {
        $result.status = "failed"
        $result.success = $false
        $result.message = "One or more UTF-8 profile probes failed."
    }
    Write-Result -Result $result
    if ($result.status -eq "failed") { exit 1 }
    exit 0
} catch {
    $failure = New-Result -Status "failed" -Message $_.Exception.Message
    Write-Result -Result $failure
    exit 1
}
