[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# [参数] 无
# [返回] 无
# 最近修改时间: 2026-07-13 21:42:35，提供 PowerShell 环境 v2 的完全隔离回归入口。
function Assert-Condition {
    param([bool]$Condition, [string]$Message)

    # 1. 让每个测试断言在失败点立即停止，避免后续步骤掩盖根因。
    if (-not $Condition) { throw $Message }
}

# [参数] ShellPath 子进程 shell；Initializer 环境入口；Arguments 命名参数；WorkingDirectory 工作目录
# [返回] 包含 JSON 结果与退出码的对象
# 最近修改时间: 2026-07-13 21:42:35，通过子进程调用避免入口脚本的 exit 结束测试进程。
function Invoke-EnvironmentScript {
    param([string]$ShellPath, [string]$Initializer, [hashtable]$Arguments, [string]$WorkingDirectory)

    # 1. 统一把 hashtable 展开为命名参数，保持 PS5 与 PS7 测试输入一致。
    $argumentList = @("-NoLogo", "-NoProfile", "-File", $Initializer)
    foreach ($key in $Arguments.Keys) {
        $argumentList += "-$key"
        if ($Arguments[$key] -isnot [switch] -and $Arguments[$key] -ne $true) { $argumentList += [string]$Arguments[$key] }
    }
    Push-Location $WorkingDirectory
    try {
        $output = & $ShellPath @argumentList 6>$null
        $text = $output | Out-String
        $jsonStart = $text.IndexOf("{")
        $jsonEnd = $text.LastIndexOf("}")
        if ($jsonStart -lt 0 -or $jsonEnd -lt $jsonStart) { throw "Environment script returned no JSON result: $text" }
        return [pscustomobject]@{ exitCode = $LASTEXITCODE; result = ($text.Substring($jsonStart, $jsonEnd - $jsonStart + 1) | ConvertFrom-Json) }
    } finally {
        Pop-Location
    }
}

# [参数] Path 目标文件路径
# [返回] SHA-256 十六进制文本或空值
# 最近修改时间: 2026-07-13 21:42:35，使用 .NET 流避免 WhatIf 影响 hash 读取。
function Get-FileHashText {
    param([string]$Path)

    # 1. 测试只读计算 hash，用于证明真实用户文件没有被夹具触碰。
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $stream = [IO.File]::Open($Path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
    try {
        $hash = [Security.Cryptography.SHA256]::Create()
        try { return ([BitConverter]::ToString($hash.ComputeHash($stream)) -replace "-", "") } finally { $hash.Dispose() }
    } finally { $stream.Dispose() }
}

Write-Output "[START] Windows PowerShell environment v2 isolated regression"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..\..")).Path
$skillRoot = Join-Path $repoRoot "windows-powershell-environment-rules"
$initializer = Join-Path $skillRoot "scripts\initialize_windows_powershell.ps1"
$recovery = Join-Path $skillRoot "scripts\recover_windows_command.ps1"
$shellPath = (Get-Process -Id $PID).Path
$temporaryRoot = Join-Path $env:TEMP ("codex-psenv-v2-" + [guid]::NewGuid().ToString("N"))
$terminalFixture = Join-Path $temporaryRoot "settings.json"
$stateRoot = Join-Path $temporaryRoot "state"
$profileRoot = Join-Path $temporaryRoot "profiles"
$userTerminal = Join-Path $env:LOCALAPPDATA "Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
$userTerminalHash = Get-FileHashText -Path $userTerminal

try {
    New-Item -ItemType Directory -Path $temporaryRoot -Force | Out-Null

    # 1. 必需条件通过时应返回 ready。
    $doctor = Invoke-EnvironmentScript -ShellPath $shellPath -Initializer $initializer -Arguments @{ Mode = "Doctor"; Policy = "RequiredOnly"; SkipEncodingBootstrap = $true; StateDirectory = $stateRoot; OutputFormat = "Json" } -WorkingDirectory $skillRoot
    Assert-Condition ($doctor.exitCode -eq 0 -and $doctor.result.status -eq "ready") "RequiredOnly doctor did not return ready."
    Write-Output "[PASS] TEST-PSENV-001 RequiredOnly ready"

    # 2. Extended 中可选工具缺失时必须是 degraded，且 marker 可复用。
    $session = Invoke-EnvironmentScript -ShellPath $shellPath -Initializer $initializer -Arguments @{ Mode = "SessionEnsure"; Policy = "Extended"; SkipToolInstall = $true; TestMode = $true; ProfileRoot = $profileRoot; StateDirectory = $stateRoot; OutputFormat = "Json" } -WorkingDirectory $skillRoot
    $marker = Get-Content -LiteralPath (Join-Path $stateRoot "session-marker.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    Assert-Condition ($session.exitCode -eq 0 -and $session.result.status -eq "degraded" -and $marker.complete) "Optional tools incorrectly blocked SessionEnsure."
    Write-Output "[PASS] TEST-PSENV-002 Optional tools degrade without blocking"

    # 3. WhatIf 不得创建状态文件或改写 Terminal fixture。
    $whatIfText = @'
{
  // keep this comment
  "profiles": { "list": [] }
}
'@
    [IO.File]::WriteAllText($terminalFixture, $whatIfText, [Text.UTF8Encoding]::new($false))
    $whatIfState = Join-Path $temporaryRoot "whatif-state"
    $whatIf = Invoke-EnvironmentScript -ShellPath $shellPath -Initializer $initializer -Arguments @{ Mode = "Apply"; Policy = "RequiredOnly"; SkipToolInstall = $true; TestMode = $true; ProfileRoot = $profileRoot; TerminalSettingsPath = $terminalFixture; StateDirectory = $whatIfState; WhatIf = $true; OutputFormat = "Json" } -WorkingDirectory $skillRoot
    Assert-Condition ($whatIf.exitCode -eq 0 -and -not (Test-Path -LiteralPath $whatIfState) -and (Get-Content -LiteralPath $terminalFixture -Raw -Encoding UTF8) -eq $whatIfText) "WhatIf wrote state or Terminal settings."
    Write-Output "[PASS] TEST-PSENV-003 WhatIf has no side effects"

    # 4. JSONC Apply 保留注释，Rollback 只在文件未漂移时恢复。
    $terminalText = @'
{
  // preserve this comment
  "defaultProfile": "{11111111-1111-1111-1111-111111111111}",
  "profiles": {
    "list": [
      { "guid": "{11111111-1111-1111-1111-111111111111}", "name": "Windows PowerShell", "commandline": "powershell.exe" },
    ],
  },
}
'@
    [IO.File]::WriteAllText($terminalFixture, $terminalText, [Text.UTF8Encoding]::new($false))
    $applyState = Join-Path $temporaryRoot "apply-state"
    $apply = Invoke-EnvironmentScript -ShellPath $shellPath -Initializer $initializer -Arguments @{ Mode = "Apply"; Policy = "RequiredOnly"; SkipToolInstall = $true; TestMode = $true; ProfileRoot = $profileRoot; TerminalSettingsPath = $terminalFixture; StateDirectory = $applyState; OutputFormat = "Json" } -WorkingDirectory $skillRoot
    $changedText = Get-Content -LiteralPath $terminalFixture -Raw -Encoding UTF8
    Assert-Condition ($apply.exitCode -eq 0 -and $changedText -match "preserve this comment" -and $changedText -match "PowerShell 7") "Terminal JSONC patch was not preserved."
    $rollback = Invoke-EnvironmentScript -ShellPath $shellPath -Initializer $initializer -Arguments @{ Mode = "Rollback"; StateDirectory = $applyState; OutputFormat = "Json" } -WorkingDirectory $skillRoot
    Assert-Condition ($rollback.exitCode -eq 0 -and (Get-Content -LiteralPath $terminalFixture -Raw -Encoding UTF8) -eq $terminalText) "Terminal rollback did not restore original text."
    Write-Output "[PASS] TEST-PSENV-004 Terminal JSONC and rollback"

    # 5. Apply 后的外部改动必须阻止自动回滚。
    $applyAgain = Invoke-EnvironmentScript -ShellPath $shellPath -Initializer $initializer -Arguments @{ Mode = "Apply"; Policy = "RequiredOnly"; SkipToolInstall = $true; TestMode = $true; ProfileRoot = $profileRoot; TerminalSettingsPath = $terminalFixture; StateDirectory = $applyState; OutputFormat = "Json" } -WorkingDirectory $skillRoot
    Add-Content -LiteralPath $terminalFixture -Encoding UTF8 -Value "// user changed this later"
    $drift = Invoke-EnvironmentScript -ShellPath $shellPath -Initializer $initializer -Arguments @{ Mode = "Rollback"; StateDirectory = $applyState; OutputFormat = "Json" } -WorkingDirectory $skillRoot
    Assert-Condition ($applyAgain.exitCode -eq 0 -and $drift.exitCode -eq 13 -and $drift.result.status -eq "rollback_refused") "Rollback did not refuse drifted file."
    Write-Output "[PASS] TEST-PSENV-005 Rollback drift refusal"

    # 6. 未知命令不猜包，只记录 candidate。
    $candidateState = Join-Path $temporaryRoot "candidate-state"
    $candidateOutput = & $shellPath -NoLogo -NoProfile -File $recovery -CommandName "missing-tool.exe" -ExitCode 127 -StateDirectory $candidateState
    $candidateExit = $LASTEXITCODE
    $candidate = $candidateOutput | Out-String | ConvertFrom-Json
    $casebook = Get-Content -LiteralPath (Join-Path $candidateState "failure-cases.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    Assert-Condition ($candidateExit -eq 10 -and $candidate.status -eq "blocked" -and $casebook.cases[0].state -eq "candidate") "Unknown command recovery guessed an installation."
    Write-Output "[PASS] TEST-PSENV-006 Unknown command candidate"

    # 7. 假包管理器只应收到自己 source 的精确包 ID，安装后仍必须通过真实版本探针。
    $fakeBin = Join-Path $temporaryRoot "fake-bin"
    $fakeState = Join-Path $temporaryRoot "fake-state"
    $fakeManifest = Join-Path $temporaryRoot "fake-manifest.json"
    $fakeLog = Join-Path $temporaryRoot "package-manager.log"
    New-Item -ItemType Directory -Path $fakeBin -Force | Out-Null
    $oldPath = $env:Path
    $oldFakeBin = $env:FAKE_BIN
    $oldFakeLog = $env:FAKE_LOG
    $env:Path = "$fakeBin;$env:Path"
    $env:FAKE_BIN = $fakeBin
    $env:FAKE_LOG = $fakeLog
    $scoopScript = "@echo off`r`n" + 'echo %*>>"%FAKE_LOG%"' + "`r`n" + 'echo @echo off> "%FAKE_BIN%\fake-tool.cmd"' + "`r`n" + 'echo echo fake-tool 1.0>> "%FAKE_BIN%\fake-tool.cmd"' + "`r`nexit /b 0`r`n"
    [IO.File]::WriteAllText((Join-Path $fakeBin "scoop.cmd"), $scoopScript, [Text.UTF8Encoding]::new($false))
    $manifest = [ordered]@{
        schema_version = 2
        scope = "windows-user"
        source_order = @("scoop-existing", "winget")
        policies = [ordered]@{ RequiredOnly = @("fake-tool"); Core = @("fake-tool"); Extended = @("fake-tool") }
        tools = @([ordered]@{
            key = "fake-tool"
            commands = @("fake-tool.cmd")
            version_probe = [ordered]@{ arguments = @("--version") }
            required = $true
            host_requirements = @("PowerShell7")
            packages = [ordered]@{
                "scoop-existing" = [ordered]@{ id = "Fixture.Scoop"; scope = "user" }
                winget = [ordered]@{ id = "Fixture.Winget"; scope = "user" }
            }
        })
    }
    [IO.File]::WriteAllText($fakeManifest, ($manifest | ConvertTo-Json -Depth 12), [Text.UTF8Encoding]::new($false))
    try {
        $fakeApply = Invoke-EnvironmentScript -ShellPath $shellPath -Initializer $initializer -Arguments @{ Mode = "Apply"; Policy = "RequiredOnly"; SkipEncodingBootstrap = $true; SkipTerminalDefault = $true; StateDirectory = $fakeState; ManifestPathOverride = $fakeManifest; OutputFormat = "Json" } -WorkingDirectory $skillRoot
        $managerLog = Get-Content -LiteralPath $fakeLog -Raw -Encoding UTF8
        Assert-Condition ($fakeApply.exitCode -eq 0 -and $fakeApply.result.status -eq "ready" -and $managerLog -match "install Fixture.Scoop" -and $managerLog -notmatch "Fixture.Winget") "Package source mapping was not exact."
    } finally {
        $env:Path = $oldPath
        $env:FAKE_BIN = $oldFakeBin
        $env:FAKE_LOG = $oldFakeLog
    }
    Write-Output "[PASS] TEST-PSENV-007 Exact package source mapping"

    # 8. Git Bash 必须从 Git 安装目录识别，不能把 Windows 的 bash.exe launcher 当成 Git Bash。
    $git = Get-Command git.exe -CommandType Application -ErrorAction Stop | Select-Object -First 1
    $gitRoot = Split-Path (Split-Path $git.Source -Parent) -Parent
    $gitBash = Join-Path $gitRoot "bin\bash.exe"
    $platform = if (Test-Path -LiteralPath $gitBash) { (& $gitBash -lc "uname -s" | Out-String).Trim() } else { "" }
    Assert-Condition ($platform -match "MINGW|MSYS") "Git Bash was not resolved from Git for Windows."
    Write-Output "[PASS] TEST-PSENV-008 Git Bash identity"

    # 9. 测试结束前确认真实 Terminal 没有被 fixture 改动。
    Assert-Condition ((Get-FileHashText -Path $userTerminal) -eq $userTerminalHash) "Isolated tests changed real Windows Terminal settings."
    Write-Output "[PASS] TEST-PSENV-009 Real user settings unchanged"
    Write-Output "[PASS] Windows PowerShell environment v2 isolated regression"
}
catch {
    Write-Output ("[FAIL] {0}" -f $_.Exception.Message)
    exit 1
}
finally {
    if (Test-Path -LiteralPath $temporaryRoot) { Remove-Item -LiteralPath $temporaryRoot -Recurse -Force }
    Write-Output "[END] Windows PowerShell environment v2 isolated regression"
}
