[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CommandName,
    [string]$PackageId,
    [string]$VersionProbe = "--version",
    [ValidateSet("winget", "scoop-existing", "chocolatey-existing")]
    [string]$Source,
    [string]$ErrorText,
    [int]$ExitCode = 0,
    [string]$StateDirectory,
    [switch]$SkipToolInstall
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$initializer = Join-Path $scriptRoot "initialize_windows_powershell.ps1"
# 1. 仅把明确的 command-not-found 证据送入恢复入口，避免误装包。
$isCommandNotFound = ($ExitCode -eq 127) -or ($ErrorText -match "(?i)(commandnotfound|command not found|not recognized|找不到|无法将.*项识别)")
if (-not $isCommandNotFound) {
    Write-Error "The supplied failure does not match a command-not-found condition."
    exit 2
}

$arguments = @{
    Mode = "RecoverCommand"
    OnlyCommand = $CommandName
    CommandProbe = $VersionProbe
}
if ($PackageId) { $arguments.CommandPackageId = $PackageId }
if ($Source) { $arguments.CommandSource = $Source }
if ($StateDirectory) { $arguments.StateDirectory = $StateDirectory }
if ($SkipToolInstall) { $arguments.SkipToolInstall = $true }

try {
    # 2. 优先使用 PowerShell 7，只有 pwsh 不存在时才回退 Windows PowerShell 5.1。
    $wrapper = Get-Command pwsh.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $wrapper) { $wrapper = Get-Command powershell.exe -CommandType Application -ErrorAction Stop | Select-Object -First 1 }
    & $wrapper.Source -NoLogo -NoProfile -File $initializer @arguments
    if ($LASTEXITCODE -eq 0) { exit 0 }
    exit $LASTEXITCODE
} catch {
    Write-Error $_.Exception.Message
    exit 1
}
