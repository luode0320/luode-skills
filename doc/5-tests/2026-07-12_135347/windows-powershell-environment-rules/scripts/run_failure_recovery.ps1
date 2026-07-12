[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Output "[START] Windows PowerShell failure recovery test"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..\..")).Path
$initializer = Join-Path $repoRoot "windows-powershell-environment-rules\scripts\initialize_windows_powershell.ps1"
$wrapper = Join-Path $repoRoot "windows-powershell-environment-rules\scripts\recover_windows_command.ps1"
$utf8 = [Text.UTF8Encoding]::new($false)
$tempRoot = Join-Path $env:TEMP "codex-powershell-recovery-test-$(Get-Date -Format yyyyMMddHHmmss)"

try {
    New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null

    # 1. 验证损坏的用户状态不会在 StrictMode 下阻断 Audit。
    Write-Output "[STEP] Malformed discovered state falls back safely"
    [IO.File]::WriteAllText((Join-Path $tempRoot "discovered-tools.json"), "{}", $utf8)
    & powershell.exe -NoLogo -NoProfile -File $initializer -Mode Audit -SkipToolInstall -StateDirectory $tempRoot | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Audit rejected a malformed discovered state file." }

    # 2. 验证新会话首次执行写 marker，TTL 内第二次幂等跳过。
    Write-Output "[STEP] SessionEnsure creates a complete marker and is TTL-idempotent"
    $sessionRoot = Join-Path $tempRoot "session"
    & powershell.exe -NoLogo -NoProfile -File $initializer -Mode SessionEnsure -ToolBundle Core -SkipToolInstall -SkipTerminalDefault -StateDirectory $sessionRoot -SessionTtlMinutes 60 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "SessionEnsure first run failed." }
    $marker = Get-Content (Join-Path $sessionRoot "session-marker.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $marker.complete) { throw "SessionEnsure did not write a complete marker." }
    & powershell.exe -NoLogo -NoProfile -File $initializer -Mode SessionEnsure -ToolBundle Core -SkipToolInstall -SkipTerminalDefault -StateDirectory $sessionRoot -SessionTtlMinutes 60 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "SessionEnsure second run failed." }

    # 3. 验证 canonical 命令不重复登记到 discovered 状态。
    Write-Output "[STEP] Known manifest recovery verifies without duplicate discovered entry"
    $knownRoot = Join-Path $tempRoot "known"
    & powershell.exe -NoLogo -NoProfile -File $initializer -Mode RecoverCommand -OnlyCommand rg.exe -StateDirectory $knownRoot | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Known command recovery failed." }
    if (Test-Path (Join-Path $knownRoot "discovered-tools.json")) { throw "Canonical command was incorrectly added to discovered state." }

    # 4. 验证精确包映射可以登记已存在的非 canonical 命令。
    Write-Output "[STEP] Exact package mapping registers an already-present non-manifest command"
    $dynamicRoot = Join-Path $tempRoot "dynamic"
    & powershell.exe -NoLogo -NoProfile -File $initializer -Mode RecoverCommand -OnlyCommand cmd.exe -CommandPackageId Fixture.Cmd -SkipToolInstall -StateDirectory $dynamicRoot | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Exact dynamic mapping did not verify an existing command." }
    $dynamic = Get-Content (Join-Path $dynamicRoot "discovered-tools.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    if (@($dynamic.tools).Count -ne 1 -or $dynamic.tools[0].command -ne "cmd.exe") { throw "Dynamic discovered state was not registered or was duplicated." }

    # 5. 验证未知命令不猜包，只记录 candidate。
    Write-Output "[STEP] Unknown command records candidate without package guessing"
    $unknownRoot = Join-Path $tempRoot "unknown"
    & powershell.exe -NoLogo -NoProfile -File $wrapper -CommandName codex-missing-command.exe -ExitCode 127 -StateDirectory $unknownRoot | Out-Null
    if ($LASTEXITCODE -eq 0) { throw "Unknown command recovery unexpectedly succeeded without an exact package ID." }
    $cases = Get-Content (Join-Path $unknownRoot "failure-cases.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($cases.cases[0].state -ne "candidate") { throw "Unknown command was not recorded as candidate." }

    Write-Output "[PASS] SessionEnsure, malformed state, canonical/dynamic recovery and candidate routing"
}
catch {
    Write-Output ("[FAIL] {0}" -f $_.Exception.Message)
    exit 1
}
finally {
    if (Test-Path -LiteralPath $tempRoot) { Remove-Item -LiteralPath $tempRoot -Recurse -Force }
    Write-Output "[END] Windows PowerShell failure recovery test"
}
