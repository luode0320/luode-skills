param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("check", "generate", "init-project-agents")]
    [string]$Action,
    [string]$Prompt = "",
    [string]$Out = "output/imagegen/output.png",
    [string]$Size = "1024x1024",
    [string]$Quality = "medium",
    [string]$Model = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$DefaultCodexHome = Join-Path $env:USERPROFILE ".codex"
$RelativeCodexHome = Resolve-Path (Join-Path $ScriptRoot "..\..\..\..") | Select-Object -ExpandProperty Path
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { if (Test-Path -LiteralPath $DefaultCodexHome) { $DefaultCodexHome } else { $RelativeCodexHome } }
$BootstrapScript = Join-Path $ScriptRoot "bootstrap_imagegen_env.py"
$ImageGenScript = Join-Path $ScriptRoot "image_gen.py"
$ProjectRoot = if ($env:IMAGEGEN_PROJECT_ROOT) { $env:IMAGEGEN_PROJECT_ROOT } else { (Get-Location).Path }

if (-not (Test-Path -LiteralPath $BootstrapScript)) {
    throw "bootstrap_imagegen_env.py not found: $BootstrapScript"
}

if (-not (Test-Path -LiteralPath $ImageGenScript)) {
    throw "image_gen.py not found: $ImageGenScript"
}

$BootstrapLines = @(& python $BootstrapScript --shell powershell --codex-home $CodexHome --project-root $ProjectRoot)
foreach ($Line in $BootstrapLines) {
    if ($Line) {
        Invoke-Expression $Line
    }
}

$ResolvedModel = if ($Model) {
    $Model
} elseif ($env:IMAGEGEN_MODEL) {
    $env:IMAGEGEN_MODEL
} else {
    "gpt-image-2"
}

if ($Action -eq "init-project-agents") {
    python $BootstrapScript --shell powershell --codex-home $CodexHome --project-root $ProjectRoot --init-project-agents-image-config | Out-Null
    Write-Host "Initialized AGENTS.md imagegen template at project root if it was missing."
    exit 0
}

if ($Action -eq "check") {
    Write-Host "CODEX_HOME: $CodexHome"
    Write-Host "IMAGEGEN_PROJECT_ROOT: $ProjectRoot"
    Write-Host "ImageGen CLI: $ImageGenScript"
    Write-Host ("OPENAI_API_KEY: " + $(if ($env:OPENAI_API_KEY) { "SET" } else { "MISSING" }))
    Write-Host ("OPENAI_BASE_URL: " + $(if ($env:OPENAI_BASE_URL) { "SET" } else { "MISSING" }))
    Write-Host ("OPENAI_API_KEY source: " + $(if ($env:IMAGEGEN_OPENAI_API_KEY_SOURCE) { $env:IMAGEGEN_OPENAI_API_KEY_SOURCE } else { "unknown" }))
    Write-Host ("OPENAI_BASE_URL source: " + $(if ($env:IMAGEGEN_OPENAI_BASE_URL_SOURCE) { $env:IMAGEGEN_OPENAI_BASE_URL_SOURCE } else { "unknown" }))
    Write-Host ("IMAGEGEN_MODEL: " + $ResolvedModel)
    Write-Host ("IMAGEGEN_FALLBACK_MODEL: " + $(if ($env:IMAGEGEN_FALLBACK_MODEL) { $env:IMAGEGEN_FALLBACK_MODEL } else { "unset" }))
    Write-Host ("IMAGEGEN_PRIORITY_RULE: " + $(if ($env:IMAGEGEN_PRIORITY_RULE) { $env:IMAGEGEN_PRIORITY_RULE } else { "unset" }))
    if ($env:IMAGEGEN_PROJECT_AGENTS_MD) {
        Write-Host "Project AGENTS.md: $env:IMAGEGEN_PROJECT_AGENTS_MD"
    }
    @'
import importlib.util
mods=["openai","PIL"]
for mod in mods:
    status = "OK" if importlib.util.find_spec(mod) else "MISSING"
    print(f"{mod}={status}")
'@ | python -
    python $ImageGenScript generate --prompt "dry run test imagegen system entry" --size 1024x1024 --out output/imagegen/dry-run-test.png --dry-run
    exit 0
}

if (-not $Prompt) {
    throw "Prompt is required when Action=generate"
}

$Command = @(
    "python",
    $ImageGenScript,
    "generate",
    "--prompt", $Prompt,
    "--model", $ResolvedModel,
    "--quality", $Quality,
    "--size", $Size,
    "--out", $Out
)

if ($DryRun) {
    $Command += "--dry-run"
}

& $Command[0] $Command[1..($Command.Length - 1)]
