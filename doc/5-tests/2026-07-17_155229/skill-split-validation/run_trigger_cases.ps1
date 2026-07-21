[CmdletBinding()]
param(
    [switch]$Help,
    [string]$RepoRoot = "",
    [string]$CasesRoot = "",
    [ValidateSet("all", "pre-delete", "post-delete")]
    [string]$Phase = "all"
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Output "Usage: run_trigger_cases.ps1 [-Phase all|pre-delete|post-delete] [-RepoRoot <path>] [-CasesRoot <path>] [-Help]"
    Write-Output "Runs local fixture validation through validate_skill_split.py."
    Write-Output "Modes: size, mapping, trigger, pre-delete, post-delete."
    Write-Output "The script never deletes or modifies real skill directories."
    exit 0
}

try {
    # 1. 固定入口、仓库和 fixture 目录，所有路径交由 Python 入口做边界校验。
    $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
        $RepoRoot = (Get-Item -LiteralPath $scriptRoot).Parent.Parent.Parent.Parent.FullName
    }
    if ([string]::IsNullOrWhiteSpace($CasesRoot)) {
        $CasesRoot = Join-Path $scriptRoot "cases"
    }

    $validator = Join-Path $scriptRoot "validate_skill_split.py"
    if (-not (Test-Path -LiteralPath $validator -PathType Leaf)) {
        throw "validator not found: $validator"
    }
    if (-not (Test-Path -LiteralPath $CasesRoot -PathType Container)) {
        throw "fixture directory not found: $CasesRoot"
    }

    $modes = if ($Phase -eq "all") {
        @("size", "mapping", "trigger", "pre-delete", "post-delete")
    }
    elseif ($Phase -eq "pre-delete") {
        @("pre-delete")
    }
    else {
        @("post-delete")
    }

    # 2. 按阶段调用同一个 Python 入口，确保 all、pre-delete 和 post-delete 使用同一组 fixture。
    Write-Host "[START] Skill split trigger fixture validation"
    Write-Host "[STEP] RepoRoot=$RepoRoot"
    Write-Host "[STEP] CasesRoot=$CasesRoot"
    Write-Host "[STEP] Phase=$Phase"
    foreach ($mode in $modes) {
        Write-Host "[STEP] Running mode=$mode"
        & python "-X" "utf8" $validator "--mode" $mode "--root" $RepoRoot "--cases" $CasesRoot
        if ($LASTEXITCODE -ne 0) {
            throw "validator failed for mode=$mode with exit code $LASTEXITCODE"
        }
    }
    # 3. 明确本入口只验证 fixture，不删除真实 skill 或刷新字典。
    Write-Host "[PASS] Skill split trigger fixture validation"
    Write-Host "[DONE] No real skill directory was deleted or modified"
    exit 0
}
catch {
    Write-Error "[FAIL] $($_.Exception.Message)"
    exit 1
}
