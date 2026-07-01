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

function Get-TargetProfiles {
    $targets = @()

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

    $pwshCommand = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($pwshCommand) {
        $powerShell7Dir = Join-Path $HOME "Documents\\PowerShell"
        $targets += [pscustomobject]@{
            Label = "PowerShell7-CurrentUserAllHosts"
            Path = Join-Path $powerShell7Dir "profile.ps1"
            Shell = $pwshCommand.Source
        }
        $targets += [pscustomobject]@{
            Label = "PowerShell7-CurrentUserCurrentHost"
            Path = Join-Path $powerShell7Dir "Microsoft.PowerShell_profile.ps1"
            Shell = $pwshCommand.Source
        }
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
$result | ConvertTo-Json -Compress
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

$targets = @(Get-TargetProfiles)
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
