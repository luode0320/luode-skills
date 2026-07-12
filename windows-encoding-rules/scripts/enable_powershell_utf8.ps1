[CmdletBinding()]
param()

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
"@

try {
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force -ErrorAction Stop
} catch {
    $message = $_.Exception.Message
    $errorId = $_.FullyQualifiedErrorId
    $currentUserPolicy = Get-ExecutionPolicy -Scope CurrentUser
    # A Bypass parent can still trigger ExecutionPolicyOverride after CurrentUser is updated.
    $overrideSucceeded = $errorId -eq "ExecutionPolicyOverride,Microsoft.PowerShell.Commands.SetExecutionPolicyCommand"
    $overrideSucceeded = $overrideSucceeded -or $message -match "updated your execution policy successfully"

    if (-not ($overrideSucceeded -and $currentUserPolicy -eq "RemoteSigned")) {
        throw
    }
}

function Get-PowerShell7Command {
    <#
    [Parameters]
    None.
    [Returns]
    PowerShell 7 command metadata, or $null when unavailable.
    Last modified
    2026-07-12 13:51:01 Prefer PowerShell 7 while retaining the legacy fallback.
    #>
    # 1. Resolve an application command so functions and aliases cannot masquerade as pwsh.
    $pwshCommand = @(Get-Command pwsh -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1)
    if ($null -eq $pwshCommand) {
        return $null
    }

    $executablePath = [string]$pwshCommand.Path
    if ([string]::IsNullOrWhiteSpace($executablePath)) {
        $executablePath = [string]$pwshCommand.Source
    }
    if ([string]::IsNullOrWhiteSpace($executablePath)) {
        return $null
    }

    # 2. Read the version from a no-profile child process so user output cannot pollute the probe.
    $versionText = & $executablePath -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' 2>$null | Select-Object -Last 1
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace([string]$versionText)) {
        return $null
    }

    try {
        $versionTextTrimmed = ([string]$versionText).Trim()
        $version = [version]$versionTextTrimmed
    } catch {
        return $null
    }

    # 3. Accept major version 7 or newer; otherwise keep the Windows PowerShell 5.1 fallback.
    if ($version.Major -lt 7) {
        return $null
    }

    return [pscustomobject]@{
        Path = $executablePath
        Version = $version
    }
}

function Get-TargetProfiles {
    <#
    [Parameters]
    [pscustomobject]$PowerShell7Command - verified PowerShell 7 command metadata, or null.
    [Returns]
    User PowerShell profiles to initialize and verify.
    Last modified
    2026-07-12 13:51:01 Prefer PowerShell 7 while retaining Windows PowerShell 5.1 profiles.
    #>
    param(
        [Parameter(Mandatory = $false)]
        [AllowNull()]
        [pscustomobject]$PowerShell7Command
    )

    # 1. Add PowerShell 7 profiles first so the specialized entry uses the new shell.
    $targets = @()
    if ($null -ne $PowerShell7Command) {
        $powerShell7Dir = Join-Path $HOME "Documents\\PowerShell"
        $targets += [pscustomobject]@{
            Label = "PowerShell7-CurrentUserAllHosts"
            Path = Join-Path $powerShell7Dir "profile.ps1"
            Shell = $PowerShell7Command.Path
        }
        $targets += [pscustomobject]@{
            Label = "PowerShell7-CurrentUserCurrentHost"
            Path = Join-Path $powerShell7Dir "Microsoft.PowerShell_profile.ps1"
            Shell = $PowerShell7Command.Path
        }
    }

    # 2. Always retain Windows PowerShell 5.1 profiles for legacy entry points.
    $windowsPowerShellDir = Join-Path $HOME "Documents\\WindowsPowerShell"
    $targets += [pscustomobject]@{
        Label = "WindowsPowerShell-CurrentUserAllHosts"
        Path = Join-Path $windowsPowerShellDir "profile.ps1"
        Shell = "powershell.exe"
    }
    $targets += [pscustomobject]@{
        Label = "WindowsPowerShell-CurrentUserCurrentHost"
        Path = Join-Path $windowsPowerShellDir "Microsoft.PowerShell_profile.ps1"
        Shell = "powershell.exe"
    }

    $seen = @{}
    foreach ($target in $targets) {
        if (-not $seen.ContainsKey($target.Path)) {
            $seen[$target.Path] = $true
            $target
        }
    }
}

function Ensure-ProfileUtf8Block {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProfilePath
    )

    $profileDir = Split-Path -Parent $ProfilePath
    if (-not (Test-Path -LiteralPath $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    if (-not (Test-Path -LiteralPath $ProfilePath)) {
        Set-Content -LiteralPath $ProfilePath -Encoding UTF8 -Value ""
    }

    $existing = Get-Content -LiteralPath $ProfilePath -Raw -Encoding UTF8
    if ($existing -match [regex]::Escape($beginMarker) -and $existing -match [regex]::Escape($endMarker)) {
        $pattern = "(?s)$([regex]::Escape($beginMarker)).*?$([regex]::Escape($endMarker))"
        $updated = [regex]::Replace($existing, $pattern, $managedBlock.TrimEnd())
    } elseif ([string]::IsNullOrWhiteSpace($existing)) {
        $updated = $managedBlock.TrimEnd() + [Environment]::NewLine
    } else {
        $updated = $existing.TrimEnd() + [Environment]::NewLine + [Environment]::NewLine + $managedBlock.TrimEnd() + [Environment]::NewLine
    }

    Set-Content -LiteralPath $ProfilePath -Encoding UTF8 -Value $updated
}

function Test-ShellUtf8Profile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ShellExecutable
    )

    $probeScript = @'
$result = [ordered]@{
  inputEncoding = [ordered]@{
    webName = [Console]::InputEncoding.WebName
    codePage = [Console]::InputEncoding.CodePage
    preambleLength = ([Console]::InputEncoding.GetPreamble()).Length
  }
  outputEncoding = [ordered]@{
    webName = [Console]::OutputEncoding.WebName
    codePage = [Console]::OutputEncoding.CodePage
    preambleLength = ([Console]::OutputEncoding.GetPreamble()).Length
  }
  dollarOutputEncoding = [ordered]@{
    webName = $OutputEncoding.WebName
    codePage = $OutputEncoding.CodePage
    preambleLength = ($OutputEncoding.GetPreamble()).Length
  }
  chcp = (cmd /c chcp)
}
$result | ConvertTo-Json -Compress -Depth 6
'@

    $json = & $ShellExecutable -NoLogo -Command $probeScript
    if (-not $json) {
        throw "UTF-8 probe returned empty output for $ShellExecutable"
    }

    $parsed = $json | ConvertFrom-Json
    $codePageLine = [string]$parsed.chcp
    $chcpIsUtf8 = $codePageLine -match "65001"
    $inputIsUtf8 = $parsed.inputEncoding.webName -eq "utf-8" -and [int]$parsed.inputEncoding.codePage -eq 65001 -and [int]$parsed.inputEncoding.preambleLength -eq 0
    $outputIsUtf8 = $parsed.outputEncoding.webName -eq "utf-8" -and [int]$parsed.outputEncoding.codePage -eq 65001 -and [int]$parsed.outputEncoding.preambleLength -eq 0
    $dollarIsUtf8 = $parsed.dollarOutputEncoding.webName -eq "utf-8" -and [int]$parsed.dollarOutputEncoding.codePage -eq 65001 -and [int]$parsed.dollarOutputEncoding.preambleLength -eq 0

    [pscustomobject]@{
        Raw = $parsed
        Success = ($chcpIsUtf8 -and $inputIsUtf8 -and $outputIsUtf8 -and $dollarIsUtf8)
    }
}

# 1. Prefer PowerShell 7; installation belongs to the environment skill.
$powerShell7 = Get-PowerShell7Command
if ($null -eq $powerShell7) {
    Write-Output "PowerShell 7 command not found; Windows PowerShell 5.1 profiles remain enabled."
} else {
    Write-Output "PowerShell 7 detected: version=$($powerShell7.Version)"
}

$targets = @(Get-TargetProfiles -PowerShell7Command $powerShell7)
foreach ($target in $targets) {
    Ensure-ProfileUtf8Block -ProfilePath $target.Path
}

$results = @()
foreach ($target in $targets) {
    $probe = Test-ShellUtf8Profile -ShellExecutable $target.Shell
    $results += [pscustomobject]@{
        label = $target.Label
        path = $target.Path
        shell = $target.Shell
        success = $probe.Success
        chcp = $probe.Raw.chcp
        inputEncoding = $probe.Raw.inputEncoding
        outputEncoding = $probe.Raw.outputEncoding
        dollarOutputEncoding = $probe.Raw.dollarOutputEncoding
    }
}

$failed = @($results | Where-Object { -not $_.success })
if ($failed.Count -gt 0) {
    $failedJson = $failed | ConvertTo-Json -Depth 6
    throw "PowerShell UTF-8 verification failed: $failedJson"
}

$results | ForEach-Object {
    Write-Output "Updated PowerShell UTF-8 profile [$($_.label)]: $($_.path)"
    Write-Output "Verified [$($_.label)] via $($_.shell): chcp=$($_.chcp.Trim()) input=$($_.inputEncoding.webName)/$($_.inputEncoding.codePage) output=$($_.outputEncoding.webName)/$($_.outputEncoding.codePage) dollar=$($_.dollarOutputEncoding.webName)/$($_.dollarOutputEncoding.codePage)"
}
Write-Output "PowerShell UTF-8 persistence is active for new sessions."
