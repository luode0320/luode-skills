[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$CommandName,
    [string]$PackageId,
    [string]$VersionProbe = "--version",
    [ValidateSet("winget", "scoop-existing", "chocolatey-existing")][string]$Source,
    [ValidateSet("Auto", "PowerShell7", "WindowsPowerShell", "Cmd", "GitBash")][string]$ShellHost = "Auto",
    [string]$ErrorText,
    [int]$ExitCode = 0,
    [string]$StateDirectory,
    [switch]$SkipToolInstall,
    [switch]$WhatIf
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$isCommandNotFound = ($ExitCode -eq 127) -or ($ErrorText -match "(?i)(commandnotfound|command not found|not recognized|找不到|无法将.*项识别)")
if (-not $isCommandNotFound) { Write-Error "The supplied failure does not match a command-not-found condition."; exit 2 }

$initializer = Join-Path $PSScriptRoot "initialize_windows_powershell.ps1"
$arguments = @{ Mode = "RecoverCommand"; OnlyCommand = $CommandName; StateDirectory = $StateDirectory; ShellHost = $ShellHost }
if ($Source) { $arguments.CommandSource = $Source }
if ($PackageId) { $arguments.CommandPackageId = $PackageId }
if ($SkipToolInstall) { $arguments.SkipToolInstall = $true }
if ($WhatIf) { $arguments.WhatIf = $true }
& $initializer @arguments
exit $LASTEXITCODE
