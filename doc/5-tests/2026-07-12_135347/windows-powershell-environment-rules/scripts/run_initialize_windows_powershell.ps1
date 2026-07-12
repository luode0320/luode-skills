[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Output "[START] Windows PowerShell environment skill test"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..\..")).Path
$source = Join-Path $repoRoot "windows-powershell-environment-rules\scripts\initialize_windows_powershell.ps1"
$tempRoot = Join-Path $env:TEMP "codex-powershell-test-$(Get-Date -Format yyyyMMddHHmmss)"
$settingsPath = Join-Path $tempRoot "settings.json"
$journalPath = Join-Path $tempRoot "journal.json"
$utf8 = [Text.UTF8Encoding]::new($false)
$original = @'
{
  // Preserve this JSONC comment during the transaction.
  "defaultProfile": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
  "profiles": {
    "defaults": {},
    "list": [
      { "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}", "name": "Windows PowerShell", "commandline": "powershell.exe" },
    ],
  },
}
'@

try {
    New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
    [IO.File]::WriteAllText($settingsPath, $original, $utf8)
    Write-Output "[STEP] Apply against JSONC fixture"
    & powershell.exe -NoLogo -NoProfile -File $source -Mode Apply -SkipToolInstall -TerminalSettingsPath $settingsPath -JournalPath $journalPath
    if ($LASTEXITCODE -ne 0) { throw "Apply returned exit code $LASTEXITCODE." }

    $first = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $managed = @($first.profiles.list | Where-Object { $_.guid -eq "{0f6c1b72-7c86-4a5f-a8f4-3e9ac8f5e6c1}" })
    if ($managed.Count -ne 1) { throw "Expected exactly one managed PowerShell 7 profile." }
    if ($first.defaultProfile -ne "{0f6c1b72-7c86-4a5f-a8f4-3e9ac8f5e6c1}") { throw "defaultProfile was not updated." }

    Write-Output "[STEP] Reapply and assert idempotency"
    & powershell.exe -NoLogo -NoProfile -File $source -Mode Apply -SkipToolInstall -TerminalSettingsPath $settingsPath -JournalPath $journalPath
    if ($LASTEXITCODE -ne 0) { throw "Second Apply returned exit code $LASTEXITCODE." }
    $second = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $managedAgain = @($second.profiles.list | Where-Object { $_.guid -eq "{0f6c1b72-7c86-4a5f-a8f4-3e9ac8f5e6c1}" })
    if ($managedAgain.Count -ne 1) { throw "Apply is not idempotent." }

    Write-Output "[STEP] Rollback and assert original default profile"
    & powershell.exe -NoLogo -NoProfile -File $source -Mode Rollback -JournalPath $journalPath
    if ($LASTEXITCODE -ne 0) { throw "Rollback returned exit code $LASTEXITCODE." }
    $restoredText = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8
    if ($restoredText -notmatch '"defaultProfile"\s*:\s*"\{61c54bbd-c2c6-5271-96e7-009a87ff44bf\}"') { throw "Rollback did not restore the original profile." }
    if ($restoredText -match '0f6c1b72-7c86-4a5f-a8f4-3e9ac8f5e6c1') { throw "Rollback left the managed PowerShell 7 profile behind." }
    Write-Output "[PASS] Audit, JSONC Apply, idempotency and Rollback"
}
catch {
    Write-Output ("[FAIL] {0}" -f $_.Exception.Message)
    exit 1
}
finally {
    if (Test-Path -LiteralPath $tempRoot) { Remove-Item -LiteralPath $tempRoot -Recurse -Force }
    Write-Output "[END] Windows PowerShell environment skill test"
}
