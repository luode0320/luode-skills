<#
.SYNOPSIS
  验证 NTFS junction 挂载状态与数据完整性。

.DESCRIPTION
  检查指定路径是否为 junction、指向哪里、目标目录是否存在、文件数是否一致，
  并执行写入穿透测试（可选）。用于 gdrive-junction-mount skill 的挂载后验证。

.EXAMPLE
  .\mount_verify.ps1 -MountPath "C:\Users\luode\.zcode\cli\memories" -Target "D:\谷歌云盘\zcode-memories"

.EXAMPLE
  .\mount_verify.ps1 -MountPath "F:\blog" -Target "D:\谷歌云盘\blog" -WriteTest
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$MountPath,

    [Parameter(Mandatory = $true)]
    [string]$Target,

    [switch]$WriteTest
)

$ErrorActionPreference = 'Stop'

function Write-Step([string]$msg) { Write-Host "[*] $msg" -ForegroundColor Cyan }

Write-Step "检查挂载点身份: $MountPath"
$item = Get-Item -LiteralPath $MountPath -Force
if ($item.LinkType -eq 'Junction') {
    Write-Host "  LinkType : Junction" -ForegroundColor Green
    Write-Host "  Target   : $($item.Target -join '; ')" -ForegroundColor Green
} else {
    Write-Host "  LinkType : (空/非 junction)" -ForegroundColor Yellow
    Write-Host "  ! 该路径不是 junction，挂载未生效或已回滚。" -ForegroundColor Yellow
}

Write-Step "检查目标目录存在性: $Target"
if (Test-Path -LiteralPath $Target) {
    Write-Host "  目标存在" -ForegroundColor Green
} else {
    Write-Host "  目标不存在！junction 会指向无效位置。" -ForegroundColor Red
}

Write-Step "对比文件数"
$srcCount = (Get-ChildItem -LiteralPath $MountPath -Recurse -File -Force -ErrorAction SilentlyContinue).Count
$dstCount = (Get-ChildItem -LiteralPath $Target -Recurse -File -Force -ErrorAction SilentlyContinue).Count
Write-Host "  挂载点文件数: $srcCount"
Write-Host "  目标文件数 : $dstCount"
if ($srcCount -eq $dstCount) {
    Write-Host "  一致" -ForegroundColor Green
} else {
    Write-Host "  不一致（注意：Git Bash find 可能不穿透 junction，请用本脚本口径核对）" -ForegroundColor Yellow
}

if ($WriteTest) {
    Write-Step "写入穿透测试"
    $testFile = Join-Path $MountPath '_mount_test.tmp'
    try {
        Set-Content -LiteralPath $testFile -Value 'ok' -Encoding UTF8
        if (Test-Path -LiteralPath (Join-Path $Target '_mount_test.tmp')) {
            Write-Host "  写入穿透成功：挂载点可写，目标可见" -ForegroundColor Green
        } else {
            Write-Host "  写入穿透失败：目标未出现该文件" -ForegroundColor Red
        }
    } finally {
        Remove-Item -LiteralPath $testFile -Force -ErrorAction SilentlyContinue
    }
}

Write-Step "完成"
