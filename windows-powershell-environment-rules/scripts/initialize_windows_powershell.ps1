[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet("Audit", "Apply", "Rollback", "SessionEnsure", "RecoverCommand", "Doctor")]
    [string]$Mode = "Audit",
    [ValidateSet("RequiredOnly", "Core", "Extended")]
    [string]$Policy,
    [ValidateSet("Core", "Extended")]
    [string]$ToolBundle,
    [ValidateSet("Auto", "Winget", "Scoop", "Chocolatey")]
    [string]$PackageManager = "Auto",
    [string]$TerminalSettingsPath,
    [switch]$SkipTerminalDefault,
    [switch]$SkipToolInstall,
    [switch]$SkipEncodingBootstrap,
    [switch]$TestMode,
    [string]$ProfileRoot,
    [string]$JournalPath,
    [string]$OnlyCommand,
    [string]$CommandPackageId,
    [string]$CommandProbe = "--version",
    [ValidateSet("winget", "scoop-existing", "chocolatey-existing")]
    [string]$CommandSource,
    [string]$StateDirectory,
    [string]$ManifestPathOverride,
    [int]$SessionTtlMinutes = 360,
    [ValidateSet("Auto", "PowerShell7", "WindowsPowerShell", "Cmd", "GitBash")]
    [string]$ShellHost = "Auto",
    [ValidateSet("Json", "Human")]
    [string]$OutputFormat = "Json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = Split-Path -Parent $scriptRoot
$manifestPath = Join-Path $skillRoot "references\tool-manifest.yaml"
$modulePath = Join-Path $scriptRoot "PowerShellEnvironment.Core.psm1"

if ($ToolBundle) {
    Write-Warning "ToolBundle is deprecated; use Policy."
    if (-not $Policy) { $Policy = $ToolBundle }
}
if ($ManifestPathOverride) { $manifestPath = (Resolve-Path -LiteralPath $ManifestPathOverride -ErrorAction Stop).Path }
if ($ShellHost -eq "Auto") { $ShellHost = "PowerShell7" }

$allowWrite = $false
if ($Mode -in @("Apply", "SessionEnsure", "RecoverCommand", "Rollback")) {
    $target = if ($StateDirectory) { $StateDirectory } else { "$env:LOCALAPPDATA\Codex\windows-powershell-environment" }
    $allowWrite = $PSCmdlet.ShouldProcess($target, "$Mode Windows PowerShell environment")
}

Import-Module $modulePath -Force
$result = Invoke-PowerShellEnvironment -Mode $Mode -Policy $Policy -PackageManager $PackageManager -ManifestPath $manifestPath -StateDirectory $StateDirectory -JournalPath $JournalPath -SessionTtlMinutes $SessionTtlMinutes -SkipToolInstall:$SkipToolInstall -TerminalSettingsPath $TerminalSettingsPath -SkipTerminalDefault:$SkipTerminalDefault -SkipEncodingBootstrap:$SkipEncodingBootstrap -TestMode:$TestMode -ProfileRoot $ProfileRoot -AllowWrite:$allowWrite -OnlyCommand $OnlyCommand -CommandPackageId $CommandPackageId -CommandProbe $CommandProbe -CommandSource $CommandSource -ShellHost $ShellHost

if ($OutputFormat -eq "Human") {
    Write-Output ("{0}: canContinue={1}; requiredReady={2}" -f $result.status, $result.canContinue, $result.requiredReady)
    foreach ($issue in @($result.issues)) { Write-Output ("- [{0}] {1}" -f $issue.severity, $issue.message) }
} else {
    $result | ConvertTo-Json -Depth 30
}
exit (Get-EnvironmentExitCode -Result $result)
