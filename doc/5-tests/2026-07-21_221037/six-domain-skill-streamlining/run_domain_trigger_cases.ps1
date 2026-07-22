param(
    [string]$RepoRoot = "F:\luode-skills",
    [string]$CasesRoot = "doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining",
    [ValidateSet("baseline", "trigger", "pre-delete", "post-delete", "all")]
    [string]$Phase = "baseline",
    [string]$OnlySource = ""
)
$ErrorActionPreference = "Stop"
$manifest = Join-Path $CasesRoot "mapping/domain-streamlining-manifest.yaml"
$validator = Join-Path $CasesRoot "validate_domain_streamlining.py"
$env:PYTHONUTF8 = "1"
$arguments = @(
    "-B",
    $validator,
    "--repo-root", $RepoRoot,
    "--manifest", $manifest,
    "--phase", $Phase
)
if ($OnlySource) {
    $arguments += @("--only-source", $OnlySource)
}
python @arguments
if ($LASTEXITCODE -ne 0) {
    Write-Error "domain streamlining validator failed"
    exit $LASTEXITCODE
}