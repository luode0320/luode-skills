param(
    [string]$RepoRoot = "C:\Users\Administrator\.codex\skills",
    [ValidateSet("all", "pre-delete", "post-delete")]
    [string]$Phase = "all",
    [switch]$ReuseExisting
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputRoot = Join-Path $scriptRoot "outputs"
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null

$sampleFile = Join-Path $scriptRoot "sample_comment_target.go"

$cases = @(
    @{
        phase = "pre-delete"
        round = "round2"
        id = "T2-01"
        prompt = '这个注释该不该写，应该放在哪一段代码上方？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-placement-granularity-rules")
        forbidden = @("comment-completion-gate-rules")
    },
    @{
        phase = "pre-delete"
        round = "round2"
        id = "T2-02"
        prompt = '这个方法补注释时，[参数]、[返回]、最近修改时间怎么补？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-completion-gate-rules")
        forbidden = @("comment-placement-granularity-rules")
    },
    @{
        phase = "pre-delete"
        round = "round2"
        id = "T2-03"
        prompt = '这个方法已经写了“查询订单/更新状态”两个普通注释，要不要改成 1. 2. 编号？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-completion-gate-rules")
        forbidden = @("comment-placement-granularity-rules")
    },
    @{
        phase = "pre-delete"
        round = "round2"
        id = "T2-04"
        prompt = '这个英文错误注释要不要保留原文，中文解释怎么写？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("chinese-comment-rules")
        forbidden = @("comment-placement-granularity-rules", "comment-completion-gate-rules")
    },
    @{
        phase = "pre-delete"
        round = "round2"
        id = "T2-05"
        prompt = 'Swagger 接口注释怎么写？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("api-swagger-rules")
        forbidden = @("comment-placement-granularity-rules", "comment-completion-gate-rules", "chinese-comment-rules")
    },
    @{
        phase = "pre-delete"
        round = "round2"
        id = "T2-06"
        prompt = '这个新改的方法既要补函数头注释，也想判断缓存失效分支要不要加风险注释。请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-completion-gate-rules", "comment-placement-granularity-rules")
        forbidden = @()
    },
    @{
        phase = "pre-delete"
        round = "round3"
        id = "T3-01"
        prompt = '这个 Go 方法刚改过，请优先看未提交改动，补 [参数] / [返回] / 最近修改时间，并判断重试分支是否需要步骤注释。请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-completion-gate-rules", "comment-placement-granularity-rules")
        forbidden = @()
    },
    @{
        phase = "pre-delete"
        round = "round3"
        id = "T3-02"
        prompt = '这个方法要补注释，第三方返回的 fixed error message 要不要保留原文，中文怎么写更自然？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-completion-gate-rules", "chinese-comment-rules")
        forbidden = @()
    },
    @{
        phase = "pre-delete"
        round = "round3"
        id = "T3-03"
        prompt = '这个结构体字段注释该写在字段上方还是行尾？里面的 HTTP header 名称要不要翻译成中文？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-placement-granularity-rules", "chinese-comment-rules")
        forbidden = @()
    },
    @{
        phase = "pre-delete"
        round = "round4"
        id = "T4-01"
        prompt = "使用 `$code-comment-rules` 检查文件 $sampleFile 中的注释规则是否完整承接：请先执行 Skill 命中检查，再用 4 条以内总结需要补的关键规则，不要修改文件。"
        required = @("code-comment-rules")
        forbidden = @()
    },
    @{
        phase = "pre-delete"
        round = "round4"
        id = "T4-02"
        prompt = "请读取文件 $sampleFile，先执行 Skill 命中检查，再用 4 条以内总结如果现在补注释，必须关注哪些改动位点注释闸门与注释放置问题，不要修改文件。"
        required = @("comment-completion-gate-rules", "comment-placement-granularity-rules")
        forbidden = @()
    },
    @{
        phase = "pre-delete"
        round = "round4"
        id = "T4-03"
        prompt = "请读取文件 $sampleFile，先执行 Skill 命中检查，再只说明其中 third-party fixed error message 那段注释是否该保留原文、中文解释该怎么处理，不要修改文件。"
        required = @("chinese-comment-rules")
        forbidden = @("comment-placement-granularity-rules", "comment-completion-gate-rules")
    },
    @{
        phase = "post-delete"
        round = "round5"
        id = "T5-01"
        prompt = '这个注释该不该写，应该放在哪一段代码上方？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-placement-granularity-rules")
        forbidden = @("code-comment-rules")
    },
    @{
        phase = "post-delete"
        round = "round5"
        id = "T5-02"
        prompt = '这个方法补注释时，[参数]、[返回]、最近修改时间怎么补？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("comment-completion-gate-rules")
        forbidden = @("code-comment-rules")
    },
    @{
        phase = "post-delete"
        round = "round5"
        id = "T5-03"
        prompt = '这个英文错误注释要不要保留原文，中文解释怎么写？请先执行 Skill 命中检查，只输出命中的 skill 列表和一句理由。'
        required = @("chinese-comment-rules")
        forbidden = @("comment-placement-granularity-rules", "comment-completion-gate-rules", "code-comment-rules")
    }
)

if ($Phase -eq "pre-delete") {
    $cases = $cases | Where-Object { $_.phase -eq "pre-delete" }
}
elseif ($Phase -eq "post-delete") {
    $cases = $cases | Where-Object { $_.phase -eq "post-delete" }
}

$summary = @()

foreach ($case in $cases) {
    $roundDir = Join-Path $outputRoot $case.round
    New-Item -ItemType Directory -Path $roundDir -Force | Out-Null

    $messageFile = Join-Path $roundDir "$($case.id).txt"
    if ((Test-Path $messageFile) -and -not $ReuseExisting) {
        Remove-Item $messageFile -Force
    }

    Write-Host "[START] $($case.round) $($case.id)"
    Write-Host "[PROMPT] $($case.prompt)"

    if (-not ((Test-Path $messageFile) -and $ReuseExisting)) {
        $null = & codex exec `
            -C $RepoRoot `
            -s read-only `
            --skip-git-repo-check `
            --ephemeral `
            -o $messageFile `
            $case.prompt
    }

    $message = Get-Content -Path $messageFile -Raw
    $prefix = ($message -split "理由")[0]
    $hits = [regex]::Matches($prefix, "[a-z][a-z0-9-]+-rules") | ForEach-Object { $_.Value } | Select-Object -Unique
    $hitLine = ($hits | ForEach-Object { $_ }) -join "、"

    $missingRequired = @($case.required | Where-Object { $hitLine -notmatch [regex]::Escape($_) })
    $hitForbidden = @($case.forbidden | Where-Object { $hitLine -match [regex]::Escape($_) })
    $status = if ($missingRequired.Count -eq 0 -and $hitForbidden.Count -eq 0) { "PASS" } else { "FAIL" }

    Write-Host "[RESULT] $($case.id) => $status"
    Write-Host "[HITS] $hitLine"

    $summary += [pscustomobject]@{
        phase = $case.phase
        round = $case.round
        id = $case.id
        required = ($case.required -join ", ")
        forbidden = ($case.forbidden -join ", ")
        actual_hits = $hitLine
        status = $status
        missing_required = ($missingRequired -join ", ")
        hit_forbidden = ($hitForbidden -join ", ")
        output_file = $messageFile.Replace($RepoRoot + "\", "")
    }
}

$summaryJson = Join-Path $outputRoot "summary-$Phase.json"
$summaryMd = Join-Path $outputRoot "summary-$Phase.md"

$summary | ConvertTo-Json -Depth 5 | Set-Content -Path $summaryJson -Encoding UTF8

$lines = @(
    "# Codex 触发验证汇总（$Phase）",
    "",
    "| Round | Case | Required | Forbidden | Actual Hits | Status | Missing Required | Hit Forbidden | Output |",
    "|---|---|---|---|---|---|---|---|---|"
)

foreach ($item in $summary) {
    $lines += "| $($item.round) | $($item.id) | $($item.required) | $($item.forbidden) | $($item.actual_hits) | $($item.status) | $($item.missing_required) | $($item.hit_forbidden) | $($item.output_file) |"
}

$lines | Set-Content -Path $summaryMd -Encoding UTF8

Write-Host "[DONE] Summary JSON => $summaryJson"
Write-Host "[DONE] Summary MD   => $summaryMd"
