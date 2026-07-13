Set-StrictMode -Version Latest

$script:EnvironmentSchemaVersion = 2
$script:AllowedSources = @("winget", "scoop-existing", "chocolatey-existing")
$script:StatusExitCodes = @{
    ready = 0
    degraded = 0
    rolled_back = 0
    blocked = 10
    busy = 11
    failed = 12
    rollback_refused = 13
}

function New-EnvironmentResult {
    <#
    [参数]
    - Mode：本次环境操作模式。
    - RunId：本次运行的唯一标识。
    [返回]
    - 统一的有序环境结果对象。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$Mode, [string]$RunId)

    # 1. 固定初始化失败状态，避免调用方把尚未检查的环境误判为可继续。
    return [ordered]@{
        schemaVersion = $script:EnvironmentSchemaVersion
        runId = $RunId
        mode = $Mode
        status = "failed"
        canContinue = $false
        requiredReady = $false
        restartRequired = $false
        results = @()
        issues = @()
        changes = @()
    }
}

function Add-EnvironmentIssue {
    <#
    [参数]
    - Result：待追加问题的统一结果对象。
    - Code、Severity、Message、ToolKey：问题标识、级别、说明与可选工具键。
    [返回]
    - 无；直接更新 Result.issues。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param(
        [System.Collections.IDictionary]$Result,
        [string]$Code,
        [string]$Severity,
        [string]$Message,
        [string]$ToolKey
    )

    # 1. 仅记录稳定字段，便于后续状态机按严重级别判断是否阻断。
    $issue = [ordered]@{ code = $Code; severity = $Severity; message = $Message }
    # 2. 工具键只在存在时写入，避免无关问题产生空字段。
    if ($ToolKey) { $issue.toolKey = $ToolKey }
    $Result.issues += [pscustomobject]$issue
}

function Get-EnvironmentStatePaths {
    <#
    [参数]
    - StateDirectory：可选的状态根目录。
    - JournalPath：可选的运行日志路径。
    [返回]
    - 含 marker、锁、案例和事务路径的对象。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$StateDirectory, [string]$JournalPath)

    # 1. 调用方未隔离状态目录时，使用用户级默认目录集中保存环境证据。
    $root = if ($StateDirectory) { $StateDirectory } else { Join-Path $env:LOCALAPPDATA "Codex\windows-powershell-environment" }
    $journal = if ($JournalPath) { $JournalPath } else { Join-Path $root "last-run.json" }
    return [pscustomobject]@{
        root = $root
        marker = Join-Path $root "session-marker.json"
        lock = Join-Path $root "session.lock"
        discovered = Join-Path $root "discovered-tools.json"
        cases = Join-Path $root "failure-cases.json"
        journal = $journal
        runs = Join-Path $root "runs"
    }
}

function Write-Utf8NoBom {
    <#
    [参数]
    - Path：目标文件路径。
    - Content：要写入的文本。
    [返回]
    - 无；以 UTF-8 无 BOM 写入文件。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$Path, [string]$Content)

    # 1. 显式指定无 BOM UTF-8，避免 PowerShell 版本差异造成状态文件编码漂移。
    [IO.File]::WriteAllText($Path, $Content, [Text.UTF8Encoding]::new($false))
}

function Save-EnvironmentJson {
    <#
    [参数]
    - Value：需要序列化的对象。
    - Path：目标 JSON 文件路径。
    - AllowWrite：是否允许真实写入。
    [返回]
    - 无；允许写入时原子替换目标文件。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Value, [string]$Path, [switch]$AllowWrite)

    # 1. WhatIf 路径不创建目录或临时文件，保证审计没有状态副作用。
    if (-not $AllowWrite) { return }
    # 2. 先写入同目录临时文件再替换，避免中断时留下半份 JSON。
    $parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    $temporary = "$Path.$PID.$([guid]::NewGuid().ToString('N')).tmp"
    $content = $Value | ConvertTo-Json -Depth 30
    Write-Utf8NoBom -Path $temporary -Content ($content + [Environment]::NewLine)
    Move-Item -LiteralPath $temporary -Destination $Path -Force
}

function Read-EnvironmentJson {
    <#
    [参数]
    - Path：待读取的 JSON 文件路径。
    - DefaultValue：文件缺失或无效时返回的安全默认值。
    - AllowWrite：是否允许隔离损坏文件。
    [返回]
    - 解析后的对象，或 DefaultValue。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$Path, [object]$DefaultValue, [switch]$AllowWrite)

    # 1. 不存在的状态文件按首次运行处理，不把它视为异常。
    if (-not (Test-Path -LiteralPath $Path)) { return $DefaultValue }
    try {
        # 2. 只接受 UTF-8 JSON，防止错误状态污染后续环境判断。
        $value = Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($null -ne $value) { return $value }
    } catch {
        if ($AllowWrite) {
            # 损坏文件先保留证据再回退默认值，避免覆盖后失去排查来源。
            $corrupt = "$Path.corrupt.$(Get-Date -Format yyyyMMddHHmmss)"
            Move-Item -LiteralPath $Path -Destination $corrupt -Force -ErrorAction SilentlyContinue
        }
    }
    return $DefaultValue
}

function Get-EnvironmentHash {
    <#
    [参数]
    - Path：需要计算摘要的文件路径。
    [返回]
    - 文件不存在时返回 $null，否则返回 SHA-256 十六进制摘要。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$Path)

    # 1. 以共享读方式计算摘要，为安全回滚提供文件漂移依据。
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $stream = [IO.File]::Open($Path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
    try {
        $sha256 = [Security.Cryptography.SHA256]::Create()
        try {
            $bytes = $sha256.ComputeHash($stream)
            return ([BitConverter]::ToString($bytes) -replace "-", "")
        } finally {
            $sha256.Dispose()
        }
    } finally {
        $stream.Dispose()
    }
}

function Find-ApplicationCommand {
    <#
    [参数]
    - Candidates：按优先级排列的可执行命令候选。
    [返回]
    - 第一个可解析命令的实际路径；未找到时返回 $null。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string[]]$Candidates)

    # 1. 按候选顺序解析真实应用路径，避免只根据 PATH 文本猜测可用性。
    foreach ($candidate in $Candidates) {
        $command = Get-Command $candidate -CommandType Application, ExternalScript -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($command) {
            $path = if ($command.Path) { [string]$command.Path } else { [string]$command.Source }
            if ($path) { return $path }
        }
    }
    return $null
}

function Invoke-CommandProbe {
    <#
    [参数]
    - Tool：含命令候选和版本探针定义的工具对象。
    [返回]
    - 路径、版本文本、主版本号与探针成功状态。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Tool)

    # 1. 先确认当前宿主可解析命令，缺失时不执行安装器或版本探针。
    $path = Find-ApplicationCommand -Candidates @($Tool.commands)
    if (-not $path) {
        return [pscustomobject]@{ path = $null; version = $null; major = $null; success = $false }
    }

    try {
        # 2. 执行 manifest 规定的探针，并在有最低版本要求时一并校验主版本。
        $arguments = @($Tool.version_probe.arguments)
        $output = & $path @arguments 2>&1
        $text = ($output | Out-String).Trim()
        $success = $LASTEXITCODE -eq 0
        $major = $null
        $minimumMajorProperty = $Tool.version_probe.PSObject.Properties["minimum_major"]
        if ($minimumMajorProperty -and $minimumMajorProperty.Value) {
            $version = $null
            if ([version]::TryParse($text, [ref]$version)) { $major = $version.Major }
            $success = $success -and ($null -ne $major -and $major -ge [int]$minimumMajorProperty.Value)
        }
        return [pscustomobject]@{ path = $path; version = $text; major = $major; success = $success }
    } catch {
        return [pscustomobject]@{ path = $path; version = $_.Exception.Message; major = $null; success = $false }
    }
}

function Read-ToolManifest {
    <#
    [参数]
    - ManifestPath：JSON 兼容 YAML manifest 的路径。
    [返回]
    - 通过结构校验的 manifest 对象。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$ManifestPath)

    try {
        # 1. 使用 PowerShell 内置 JSON 解析，避免为读取 manifest 引入额外模块依赖。
        $manifest = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    } catch {
        throw "tool-manifest.yaml must be JSON-compatible YAML: $($_.Exception.Message)"
    }
    # 2. 校验 schema、工具键、命令和策略引用，拒绝有歧义的安装来源。
    if ($manifest.schema_version -ne 2 -or $manifest.scope -ne "windows-user") { throw "Unsupported tool manifest schema." }
    if (-not $manifest.tools -or -not $manifest.policies) { throw "Tool manifest is missing tools or policies." }

    $keys = @{}
    $commands = @{}
    foreach ($tool in @($manifest.tools)) {
        if (-not $tool.key -or $keys.ContainsKey([string]$tool.key)) { throw "Tool manifest contains a duplicate or empty key." }
        $keys[[string]$tool.key] = $true
        if (-not $tool.commands -or -not $tool.version_probe -or -not $tool.version_probe.arguments) { throw "Tool '$($tool.key)' is missing commands or version probe." }
        foreach ($command in @($tool.commands)) {
            $normalized = ([string]$command).ToLowerInvariant()
            if ($commands.ContainsKey($normalized)) { throw "Tool manifest command '$command' is duplicated." }
            $commands[$normalized] = [string]$tool.key
        }
    }
    foreach ($policy in @($manifest.policies.PSObject.Properties)) {
        foreach ($key in @($policy.Value)) {
            if (-not $keys.ContainsKey([string]$key)) { throw "Policy '$($policy.Name)' references unknown tool '$key'." }
        }
    }
    return $manifest
}

function Get-PolicyTools {
    <#
    [参数]
    - Manifest：已验证的工具 manifest。
    - Policy：要解析的工具策略名称。
    [返回]
    - 属于该策略的工具对象数组。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Manifest, [string]$Policy)

    # 1. 先确认策略存在，再按 manifest 顺序选取其声明的工具。
    $property = $Manifest.policies.PSObject.Properties[$Policy]
    if (-not $property) { throw "Unknown environment policy '$Policy'." }
    $wanted = @($property.Value)
    return @($Manifest.tools | Where-Object { $_.key -in $wanted })
}

function Get-PackageManagers {
    <#
    [参数]
    - RequestedManager：调用方指定的包管理器，或 Auto。
    [返回]
    - 当前可用且符合请求范围的包管理器数组。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$RequestedManager)

    # 1. 只登记当前已解析到的包管理器，禁止为恢复命令自行下载新的包管理器。
    $managers = @()
    $winget = Find-ApplicationCommand -Candidates @("winget.exe", "winget")
    $scoop = Find-ApplicationCommand -Candidates @("scoop.cmd", "scoop.ps1")
    $choco = Find-ApplicationCommand -Candidates @("choco.exe", "choco")
    if ($winget) { $managers += [pscustomobject]@{ source = "winget"; path = $winget } }
    if ($scoop) { $managers += [pscustomobject]@{ source = "scoop-existing"; path = $scoop } }
    if ($choco) { $managers += [pscustomobject]@{ source = "chocolatey-existing"; path = $choco } }
    if ($RequestedManager -and $RequestedManager -ne "Auto") {
        # 2. 显式来源只返回对应已存在管理器，防止静默降级到其他来源。
        $source = switch ($RequestedManager) { "Winget" { "winget" } "Scoop" { "scoop-existing" } "Chocolatey" { "chocolatey-existing" } }
        return @($managers | Where-Object { $_.source -eq $source })
    }
    return $managers
}

function Get-ExactPackage {
    <#
    [参数]
    - Tool：待恢复的 manifest 或动态工具。
    - Managers、SourceOrder：可用包管理器和来源优先级。
    - RequestedSource、PackageId：动态命令的精确来源与包标识。
    [返回]
    - 可安装的精确包对象；不存在确认映射时返回 $null。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Tool, [object[]]$Managers, [string[]]$SourceOrder, [string]$RequestedSource, [string]$PackageId)

    if ($RequestedSource -or $PackageId) {
        # 1. 动态命令必须同时提供来源和包 ID，避免把命令缺失升级为搜索猜包。
        if (-not $RequestedSource -or -not $PackageId) { throw "Dynamic command recovery requires both CommandSource and CommandPackageId." }
        if ($RequestedSource -notin $script:AllowedSources -or $PackageId -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]+$') { throw "The requested package source or package ID is invalid." }
        $manager = @($Managers | Where-Object { $_.source -eq $RequestedSource } | Select-Object -First 1)
        if ($manager.Count -ne 1) { throw "Requested package manager '$RequestedSource' is unavailable." }
        return [pscustomobject]@{ source = $RequestedSource; path = $manager[0].path; id = $PackageId; scope = "user" }
    }

    # 2. canonical 工具只使用自身在当前来源的映射，绝不复用其他包源 ID。
    foreach ($source in $SourceOrder) {
        $mapping = if ($Tool.packages) { $Tool.packages.PSObject.Properties[$source] } else { $null }
        if (-not $mapping -or -not $mapping.Value.id) { continue }
        $manager = @($Managers | Where-Object { $_.source -eq $source } | Select-Object -First 1)
        if ($manager.Count -eq 1) {
            return [pscustomobject]@{ source = $source; path = $manager[0].path; id = [string]$mapping.Value.id; scope = if ($mapping.Value.scope) { [string]$mapping.Value.scope } else { "user" } }
        }
    }
    return $null
}

function Invoke-ExactPackageInstall {
    <#
    [参数]
    - Package：已确认来源、路径、包 ID 和范围的安装对象。
    - AllowWrite：是否允许执行真实安装。
    [返回]
    - 含计划状态、成功状态和说明的安装结果。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Package, [switch]$AllowWrite)

    # 1. WhatIf 仅返回计划，确保不会触发网络、UAC 或软件安装副作用。
    if (-not $AllowWrite) { return [pscustomobject]@{ planned = $true; success = $false; message = "WhatIf prevented package installation." } }
    try {
        # 2. 按来源调用对应安装命令，避免将 Winget 参数或 ID 误传给其他管理器。
        if ($Package.source -eq "winget") {
            & $Package.path install --id $Package.id --exact --source winget --scope $Package.scope --silent --disable-interactivity --accept-source-agreements --accept-package-agreements
        } elseif ($Package.source -eq "scoop-existing") {
            & $Package.path install $Package.id
        } elseif ($Package.source -eq "chocolatey-existing") {
            & $Package.path install $Package.id --yes --no-progress
        }
        if ($LASTEXITCODE -ne 0) { return [pscustomobject]@{ planned = $false; success = $false; message = "Package manager exited with $LASTEXITCODE." } }
        return [pscustomobject]@{ planned = $false; success = $true; message = "Package manager completed." }
    } catch {
        return [pscustomobject]@{ planned = $false; success = $false; message = $_.Exception.Message }
    }
}

function Acquire-EnvironmentLock {
    <#
    [参数]
    - Paths：环境状态路径集合。
    - AllowWrite：是否允许创建真实锁。
    - RunId、Mode：锁元数据中的运行标识和操作模式。
    [返回]
    - 锁获取结果，以及持有互斥锁的文件流。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Paths, [switch]$AllowWrite, [string]$RunId, [string]$Mode)

    # 1. WhatIf 不占用真实锁，便于并发审计而不影响写入操作。
    if (-not $AllowWrite) { return [pscustomobject]@{ acquired = $true; stream = $null; planned = $true } }
    if (-not (Test-Path -LiteralPath $Paths.root)) { New-Item -ItemType Directory -Path $Paths.root -Force | Out-Null }
    if (Test-Path -LiteralPath $Paths.lock) {
        # 2. 只有能够独占打开旧锁时才回收，避免删除仍由其他进程持有的锁。
        try {
            $stale = [IO.File]::Open($Paths.lock, [IO.FileMode]::Open, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
            $stale.Dispose()
            Remove-Item -LiteralPath $Paths.lock -Force
        } catch {
            return [pscustomobject]@{ acquired = $false; stream = $null; planned = $false }
        }
    }
    try {
        # 3. 保持文件流存活来维持互斥，并写入最小元数据供人工排查。
        $stream = [IO.File]::Open($Paths.lock, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
        $metadata = @{ schemaVersion = 2; runId = $RunId; mode = $Mode; pid = $PID; acquiredAt = (Get-Date).ToString("o") } | ConvertTo-Json -Compress
        $bytes = [Text.UTF8Encoding]::new($false).GetBytes($metadata)
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush()
        return [pscustomobject]@{ acquired = $true; stream = $stream; planned = $false }
    } catch {
        return [pscustomobject]@{ acquired = $false; stream = $null; planned = $false }
    }
}

function Release-EnvironmentLock {
    <#
    [参数]
    - Lock：Acquire-EnvironmentLock 返回的锁对象。
    - Paths：环境状态路径集合。
    - AllowWrite：是否允许删除真实锁文件。
    [返回]
    - 无；释放文件流并在适用时删除锁文件。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Lock, [object]$Paths, [switch]$AllowWrite)

    # 1. 先释放文件句柄再删除锁文件，避免 Windows 文件锁阻止清理。
    if ($Lock -and $Lock.stream) { $Lock.stream.Dispose() }
    if ($AllowWrite -and (Test-Path -LiteralPath $Paths.lock)) { Remove-Item -LiteralPath $Paths.lock -Force -ErrorAction SilentlyContinue }
}

function Test-SessionMarkerFresh {
    <#
    [参数]
    - Marker：已读取的会话标记对象。
    [返回]
    - 标记完整、状态可继续且尚未过期时返回 $true。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Marker)

    # 1. 只复用完整的 ready/degraded 标记，防止阻断或损坏状态被缓存为成功。
    if (-not $Marker -or -not $Marker.complete -or -not $Marker.expiresAt) { return $false }
    if ($Marker.status -notin @("ready", "degraded")) { return $false }
    try { return ([datetime]$Marker.expiresAt -gt (Get-Date)) } catch { return $false }
}

function Set-ResultStatus {
    <#
    [参数]
    - Result：含问题列表的统一结果对象。
    [返回]
    - 无；按必需与可选问题回填状态字段。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([System.Collections.IDictionary]$Result)

    # 1. 必需问题阻断，可选问题仅降级；这是避免非适用工具误阻断会话的核心分层。
    $requiredIssues = @($Result.issues | Where-Object { $_.severity -eq "required" })
    $optionalIssues = @($Result.issues | Where-Object { $_.severity -eq "optional" })
    if ($requiredIssues.Count -gt 0) {
        $Result.status = "blocked"
        $Result.canContinue = $false
        $Result.requiredReady = $false
    } elseif ($optionalIssues.Count -gt 0) {
        $Result.status = "degraded"
        $Result.canContinue = $true
        $Result.requiredReady = $true
    } else {
        $Result.status = "ready"
        $Result.canContinue = $true
        $Result.requiredReady = $true
    }
}

function Inspect-EnvironmentTools {
    <#
    [参数]
    - Result：待写入检查结果的统一对象。
    - Tools、Managers、SourceOrder：策略工具、可用管理器和包源顺序。
    - InstallMissing、AllowWrite：是否安装缺失项及是否允许真实写入。
    [返回]
    - 无；逐工具追加结果和问题。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param(
        [System.Collections.IDictionary]$Result,
        [object[]]$Tools,
        [object[]]$Managers,
        [string[]]$SourceOrder,
        [switch]$InstallMissing,
        [switch]$AllowWrite
    )

    # 1. 每个策略工具先走真实版本探针，确保“命令存在”不被误判为可用。
    foreach ($tool in $Tools) {
        $probe = Invoke-CommandProbe -Tool $tool
        $action = "checked"
        $severity = if ($tool.required) { "required" } else { "optional" }
        if (-not $probe.success -and $InstallMissing) {
            # 2. 缺失时只按精确映射安装，防止跨包源复用 ID 或搜索未知软件。
            $package = Get-ExactPackage -Tool $tool -Managers $Managers -SourceOrder $SourceOrder
            if ($package) {
                $install = Invoke-ExactPackageInstall -Package $package -AllowWrite:$AllowWrite
                $action = if ($install.planned) { "install_planned" } elseif ($install.success) { "installed" } else { "install_failed" }
                if ($install.success) { $probe = Invoke-CommandProbe -Tool $tool }
                if (-not $install.success -and -not $install.planned) { Add-EnvironmentIssue -Result $Result -Code "package_install_failed" -Severity $severity -Message $install.message -ToolKey $tool.key }
            } else {
                Add-EnvironmentIssue -Result $Result -Code "no_exact_package_mapping" -Severity $severity -Message "No available package manager has an exact mapping for '$($tool.key)'." -ToolKey $tool.key
            }
        }
        if (-not $probe.success -and -not (@($Result.issues | Where-Object { $_.toolKey -eq $tool.key }).Count -gt 0)) {
            Add-EnvironmentIssue -Result $Result -Code "command_missing_or_probe_failed" -Severity $severity -Message "Command '$($tool.commands[0])' is missing or its version probe failed." -ToolKey $tool.key
        }
        $Result.results += [pscustomobject]@{ key = $tool.key; command = $tool.commands[0]; required = [bool]$tool.required; action = $action; result = $probe }
    }
}

function Get-ManifestToolByCommand {
    <#
    [参数]
    - Manifest：已验证的工具 manifest。
    - CommandName：调用方提供的命令名或路径。
    [返回]
    - 第一个命令候选匹配的工具对象；无匹配时返回空数组。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Manifest, [string]$CommandName)

    # 1. 先归一化路径与引号，避免同一命令以不同调用形式无法匹配 manifest。
    $leaf = [IO.Path]::GetFileName($CommandName.Trim().Trim('"', "'"))
    return @($Manifest.tools | Where-Object { @($_.commands) -contains $leaf -or @($_.commands) -contains $leaf.ToLowerInvariant() } | Select-Object -First 1)
}

function Register-EnvironmentCase {
    <#
    [参数]
    - Paths：环境状态路径集合。
    - CommandName、State、Reason：案例命令、状态和原始原因。
    - AllowWrite：是否允许写入案例库。
    [返回]
    - 无；更新脱敏且有上限的失败案例库。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Paths, [string]$CommandName, [string]$State, [string]$Reason, [switch]$AllowWrite)

    # 1. 读取历史案例并清理敏感片段，避免错误信息把凭据写入用户状态目录。
    $default = [pscustomobject]@{ schemaVersion = 2; cases = @() }
    $casebook = Read-EnvironmentJson -Path $Paths.cases -DefaultValue $default -AllowWrite:$AllowWrite
    $safeReason = ($Reason -replace "`r|`n", " ") -replace "(?i)(token|password|secret|api[-_]?key)\\s*[:=]\\s*\\S+", '$1=[redacted]'
    if ($safeReason.Length -gt 300) { $safeReason = $safeReason.Substring(0, 300) }
    $key = ([IO.Path]::GetFileName($CommandName)).ToLowerInvariant()
    # 2. 用命令键去重并限制数量，保留最新证据而不让案例文件无限增长。
    $existing = @($casebook.cases | Where-Object { $_.command -eq $key } | Select-Object -First 1)
    $cases = @($casebook.cases | Where-Object { $_.command -ne $key })
    $cases += [pscustomobject]@{ command = $key; owner = "windows-powershell-environment-rules"; state = $State; reason = $safeReason; firstSeen = if ($existing) { $existing[0].firstSeen } else { (Get-Date).ToString("o") }; lastSeen = (Get-Date).ToString("o"); attemptCount = if ($existing) { [int]$existing[0].attemptCount + 1 } else { 1 } }
    Save-EnvironmentJson -Value ([pscustomobject]@{ schemaVersion = 2; cases = @($cases | Select-Object -Last 100) }) -Path $Paths.cases -AllowWrite:$AllowWrite
}

function Register-DiscoveredTool {
    <#
    [参数]
    - Paths：环境状态路径集合。
    - Tool、Probe、Package：已验证工具、探针结果和精确安装包。
    - AllowWrite：是否允许写入发现工具记录。
    [返回]
    - 无；更新不参与 SessionEnsure 的发现工具记录。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Paths, [object]$Tool, [object]$Probe, [object]$Package, [switch]$AllowWrite)

    # 1. 仅保存探针已成功且来源精确的动态工具，避免未知命令扩大会话检查范围。
    $default = [pscustomobject]@{ schemaVersion = 2; tools = @() }
    $state = Read-EnvironmentJson -Path $Paths.discovered -DefaultValue $default -AllowWrite:$AllowWrite
    $command = [string]$Tool.commands[0]
    $items = @($state.tools | Where-Object { $_.command -ne $command })
    $items += [pscustomobject]@{
        key = [string]$Tool.key
        command = $command
        versionProbe = @($Tool.version_probe.arguments)
        source = [string]$Package.source
        packageId = [string]$Package.id
        check_only = $false
        verified = $true
        resolvedPath = [string]$Probe.path
        version = [string]$Probe.version
        registeredAt = (Get-Date).ToString("o")
    }
    Save-EnvironmentJson -Value ([pscustomobject]@{ schemaVersion = 2; tools = @($items | Select-Object -Last 100) }) -Path $Paths.discovered -AllowWrite:$AllowWrite
}

function Get-GitBashPath {
    <#
    [参数]
    - 无。
    [返回]
    - 从 Git for Windows 安装根目录解析出的 bash.exe 路径；未找到时返回 $null。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    # 1. 通过 git.exe 反推 Git Bash，避免把系统 PATH 中的 wsl.exe 误认为 Git Bash。
    $git = Find-ApplicationCommand -Candidates @("git.exe", "git")
    if (-not $git) { return $null }
    $gitRoot = Split-Path (Split-Path $git -Parent) -Parent
    $bash = Join-Path $gitRoot "bin\bash.exe"
    if (Test-Path -LiteralPath $bash) { return $bash }
    return $null
}

function Test-HostVisibility {
    <#
    [参数]
    - Tool：待检查的工具对象。
    - ShellHost：目标 Windows shell 类型。
    [返回]
    - 目标 shell 是否适用、是否可见及诊断详情。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Tool, [string]$ShellHost)

    # 1. Git Bash 与 CMD 使用自身的可见性命令，避免用当前 PowerShell PATH 替代目标 shell。
    $commandName = [string]$Tool.commands[0]
    if ($ShellHost -eq "GitBash") {
        $bash = Get-GitBashPath
        if (-not $bash) { return [pscustomobject]@{ applicable = $false; visible = $false; detail = "Git Bash is not installed." } }
        $platform = (& $bash -lc "uname -s" 2>$null | Out-String).Trim()
        if ($platform -notmatch "MINGW|MSYS") { return [pscustomobject]@{ applicable = $false; visible = $false; detail = "Resolved bash is not Git Bash." } }
        & $bash -lc "command -v $commandName" 2>$null | Out-Null
        return [pscustomobject]@{ applicable = $true; visible = $LASTEXITCODE -eq 0; detail = $platform }
    }
    if ($ShellHost -eq "Cmd") {
        cmd.exe /d /c "where $commandName >nul 2>nul"
        return [pscustomobject]@{ applicable = $true; visible = $LASTEXITCODE -eq 0; detail = "cmd" }
    }
    # 2. PowerShell 宿主复用版本探针，确保可见性与实际执行能力一致。
    $probe = Invoke-CommandProbe -Tool $Tool
    return [pscustomobject]@{ applicable = $true; visible = $probe.success; detail = $probe.path }
}

function ConvertFrom-Jsonc {
    <#
    [参数]
    - Text：待解析的 JSONC 文本。
    [返回]
    - 移除注释和尾逗号后解析得到的 JSON 对象。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$Text)

    # 1. 按字符扫描注释状态，保留字符串内的 // 与转义字符，避免破坏合法设置值。
    $builder = [Text.StringBuilder]::new()
    $inString = $false
    $escaped = $false
    $lineComment = $false
    $blockComment = $false
    for ($index = 0; $index -lt $Text.Length; $index++) {
        $character = $Text[$index]
        $next = if ($index + 1 -lt $Text.Length) { $Text[$index + 1] } else { [char]0 }
        if ($lineComment) {
            if ($character -eq "`n") { $lineComment = $false; [void]$builder.Append($character) }
            continue
        }
        if ($blockComment) {
            if ($character -eq "*" -and $next -eq "/") { $blockComment = $false; $index++ }
            continue
        }
        if ($inString) {
            [void]$builder.Append($character)
            if ($escaped) { $escaped = $false }
            elseif ($character -eq "\") { $escaped = $true }
            elseif ($character -eq '"') { $inString = $false }
            continue
        }
        if ($character -eq '"') { $inString = $true; [void]$builder.Append($character); continue }
        if ($character -eq "/" -and $next -eq "/") { $lineComment = $true; $index++; continue }
        if ($character -eq "/" -and $next -eq "*") { $blockComment = $true; $index++; continue }
        [void]$builder.Append($character)
    }
    # 2. 仅在注释移除后清理尾逗号，再交给标准 JSON 解析器验证结构。
    $withoutComments = $builder.ToString()
    return ([regex]::Replace($withoutComments, ",\s*([}\]])", '$1') | ConvertFrom-Json)
}

function Find-JsoncMatchingArrayEnd {
    <#
    [参数]
    - Text：JSONC 原文。
    - Start：profiles.list 数组起始方括号的位置。
    [返回]
    - 对应闭合方括号索引；未找到时返回 -1。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$Text, [int]$Start)

    # 1. 在字符串和注释外跟踪数组深度，确保补丁插入点不受嵌套对象影响。
    $depth = 0
    $inString = $false
    $escaped = $false
    $lineComment = $false
    $blockComment = $false
    for ($index = $Start; $index -lt $Text.Length; $index++) {
        $character = $Text[$index]
        $next = if ($index + 1 -lt $Text.Length) { $Text[$index + 1] } else { [char]0 }
        if ($lineComment) { if ($character -eq "`n") { $lineComment = $false }; continue }
        if ($blockComment) { if ($character -eq "*" -and $next -eq "/") { $blockComment = $false; $index++ }; continue }
        if ($inString) {
            if ($escaped) { $escaped = $false }
            elseif ($character -eq "\") { $escaped = $true }
            elseif ($character -eq '"') { $inString = $false }
            continue
        }
        if ($character -eq '"') { $inString = $true; continue }
        if ($character -eq "/" -and $next -eq "/") { $lineComment = $true; $index++; continue }
        if ($character -eq "/" -and $next -eq "*") { $blockComment = $true; $index++; continue }
        if ($character -eq "[") { $depth++ }
        if ($character -eq "]") { $depth--; if ($depth -eq 0) { return $index } }
    }
    return -1
}

function Get-TerminalSettingsPath {
    <#
    [参数]
    - TerminalSettingsPath：调用方显式指定的设置文件路径。
    [返回]
    - 唯一可用的 Windows Terminal 设置路径；没有时返回 $null。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$TerminalSettingsPath)

    # 1. 显式路径优先，调用方可用它消除多个 Terminal 安装渠道的歧义。
    if ($TerminalSettingsPath) { return (Resolve-Path -LiteralPath $TerminalSettingsPath -ErrorAction Stop).Path }
    # 2. 自动发现只能接受唯一候选，避免悄悄修改错误的 Terminal 配置。
    $candidates = @(
        (Join-Path $env:LOCALAPPDATA "Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"),
        (Join-Path $env:LOCALAPPDATA "Microsoft\Windows Terminal\settings.json")
    ) | Where-Object { Test-Path -LiteralPath $_ }
    if ($candidates.Count -eq 0) { return $null }
    if ($candidates.Count -gt 1) { throw "Multiple Windows Terminal settings files found; pass TerminalSettingsPath explicitly." }
    return $candidates[0]
}

function Set-TerminalPowerShellProfile {
    <#
    [参数]
    - Result：统一环境结果对象。
    - Paths、RunId：事务目录定位信息。
    - TerminalSettingsPath：待补丁的 Windows Terminal JSONC 文件。
    - AllowWrite：是否允许真实备份和写入。
    [返回]
    - 无；向 Result.changes 追加计划或已应用的 Terminal 变更。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([System.Collections.IDictionary]$Result, [object]$Paths, [string]$RunId, [string]$TerminalSettingsPath, [switch]$AllowWrite)

    # 1. 先验证托管 GUID 没有与用户 profile 冲突，避免覆盖非本 Skill 创建的设置。
    $managedGuid = "{0f6c1b72-7c86-4a5f-a8f4-3e9ac8f5e6c1}"
    $original = Get-Content -LiteralPath $TerminalSettingsPath -Raw -Encoding UTF8
    $settings = ConvertFrom-Jsonc -Text $original
    if (-not $settings.profiles -or -not ($settings.profiles.PSObject.Properties.Name -contains "list")) { throw "Windows Terminal settings has no profiles.list array." }
    $matches = @($settings.profiles.list | Where-Object { [string]$_.guid -eq $managedGuid })
    if ($matches.Count -gt 1) { throw "Windows Terminal settings contains duplicate managed PowerShell 7 profiles." }
    if ($matches.Count -eq 1 -and (([string]$matches[0].name -ne "PowerShell 7") -or ([string]$matches[0].commandline -ne "pwsh.exe -NoLogo"))) { throw "Windows Terminal managed profile GUID conflicts with a user profile." }

    $updated = $original
    $newLine = if ($original -match "`r`n") { "`r`n" } else { "`n" }
    if ($matches.Count -eq 0) {
        # 2. 只在 profiles.list 闭合前插入最小文本片段，保留原有 JSONC 注释与格式。
        $listMatch = [regex]::Match($updated, '"list"\s*:\s*\[')
        if (-not $listMatch.Success) { throw "Windows Terminal settings does not contain profiles.list." }
        $arrayStart = $updated.IndexOf("[", $listMatch.Index)
        $arrayEnd = Find-JsoncMatchingArrayEnd -Text $updated -Start $arrayStart
        if ($arrayEnd -lt 0) { throw "Windows Terminal profiles.list array is not balanced." }
        $before = $updated.Substring(0, $arrayEnd)
        $after = $updated.Substring($arrayEnd)
        $trimmed = $before.TrimEnd()
        $empty = $trimmed.EndsWith("[")
        $trailingComma = $trimmed.EndsWith(",")
        $lineStart = $updated.LastIndexOf("`n", $arrayEnd - 1) + 1
        $closingIndent = $updated.Substring($lineStart, $arrayEnd - $lineStart) -replace '[^ \t].*$', ''
        $itemIndent = "$closingIndent  "
        $prefix = if ($empty -or $trailingComma) { "" } else { "," }
        $suffix = if ($trailingComma) { "," } else { "" }
        $profileText = $prefix + $newLine + $itemIndent + ('{ "guid": "' + $managedGuid + '", "name": "PowerShell 7", "commandline": "pwsh.exe -NoLogo", "hidden": false }') + $suffix + $newLine + $closingIndent
        $updated = $before + $profileText + $after
    }

    # 3. 仅替换 defaultProfile 的值；缺失时再在根对象追加该字段。
    $defaultMatch = [regex]::Match($updated, '"defaultProfile"\s*:\s*"(?:\\.|[^"\\])*"')
    if ($defaultMatch.Success) {
        $updated = $updated.Substring(0, $defaultMatch.Index) + ('"defaultProfile": "' + $managedGuid + '"') + $updated.Substring($defaultMatch.Index + $defaultMatch.Length)
    } else {
        $openBrace = $updated.IndexOf("{")
        if ($openBrace -lt 0) { throw "Windows Terminal settings has no root object." }
        $updated = $updated.Substring(0, $openBrace + 1) + $newLine + ('  "defaultProfile": "' + $managedGuid + '",') + $updated.Substring($openBrace + 1)
    }

    # 4. 先回读验证补丁语义，再按需备份并写入，避免写出无法被 Terminal 解析的文件。
    $roundTrip = ConvertFrom-Jsonc -Text $updated
    $roundTripMatches = @($roundTrip.profiles.list | Where-Object { [string]$_.guid -eq $managedGuid })
    if ($roundTripMatches.Count -ne 1 -or [string]$roundTrip.defaultProfile -ne $managedGuid) { throw "Windows Terminal patch validation failed." }

    $runDirectory = Join-Path $Paths.runs $RunId
    $backup = Join-Path $runDirectory "terminal-settings.jsonc.bak"
    $beforeHash = Get-EnvironmentHash -Path $TerminalSettingsPath
    if ($AllowWrite) {
        if (-not (Test-Path -LiteralPath $runDirectory)) { New-Item -ItemType Directory -Path $runDirectory -Force | Out-Null }
        Copy-Item -LiteralPath $TerminalSettingsPath -Destination $backup -Force
        Write-Utf8NoBom -Path $TerminalSettingsPath -Content $updated
    }
    $afterHash = if ($AllowWrite) { Get-EnvironmentHash -Path $TerminalSettingsPath } else { $null }
    $Result.changes += [pscustomobject]@{ kind = "terminal_settings"; path = $TerminalSettingsPath; backupPath = $backup; beforeHash = $beforeHash; afterHash = $afterHash; planned = -not $AllowWrite }
}

function Invoke-EncodingTransaction {
    <#
    [参数]
    - Paths、RunId：环境运行目录和唯一标识。
    - Mode、AllowWrite：编码脚本操作模式及是否允许真实写入。
    - TestMode、ProfileRoot：隔离测试开关与临时 profile 根目录。
    [返回]
    - 编码事务路径、结构化结果和脚本退出码。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param(
        [object]$Paths,
        [string]$RunId,
        [string]$Mode,
        [switch]$AllowWrite,
        [switch]$TestMode,
        [string]$ProfileRoot
    )

    # 1. 编码脚本拥有 profile 事务；环境脚本只传入同一 run 的事务路径并消费结构化结果。
    $skillRoot = Split-Path -Parent $PSScriptRoot
    $encodingScript = Join-Path (Split-Path -Parent $skillRoot) "windows-encoding-rules\scripts\enable_powershell_utf8.ps1"
    if (-not (Test-Path -LiteralPath $encodingScript)) { throw "UTF-8 encoding script was not found." }
    $shell = Find-ApplicationCommand -Candidates @("pwsh.exe", "powershell.exe")
    if (-not $shell) { throw "No PowerShell executable is available for UTF-8 profile verification." }
    # 2. 组装隔离且可回滚的调用参数，WhatIf 时显式阻止编码脚本写入。
    $transaction = Join-Path (Join-Path $Paths.runs $RunId) "utf8-transaction.json"
    $arguments = @("-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $encodingScript, "-Mode", $Mode, "-OutputFormat", "Json", "-TransactionPath", $transaction)
    if ($TestMode) { $arguments += "-TestMode"; $arguments += "-ProfileRoot"; $arguments += $ProfileRoot }
    if (-not $AllowWrite) { $arguments += "-WhatIf" }
    # 3. 只接受 JSON 结果，避免父流程从人类输出推断 profile 事务是否成功。
    $output = & $shell @arguments 2>&1
    $text = ($output | Out-String).Trim()
    try { $result = $text | ConvertFrom-Json } catch { throw "UTF-8 transaction returned invalid JSON: $text" }
    return [pscustomobject]@{ transactionPath = $transaction; result = $result; exitCode = $LASTEXITCODE }
}

function Invoke-EncodingRollback {
    <#
    [参数]
    - TransactionPath：编码脚本产生的事务文件路径。
    - AllowWrite：是否允许真实恢复 profile。
    [返回]
    - 编码脚本返回的结构化回滚结果。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([string]$TransactionPath, [switch]$AllowWrite)

    # 1. 仅让编码脚本回滚它自身记录的 profile，避免环境脚本猜测 profile 内容。
    $skillRoot = Split-Path -Parent $PSScriptRoot
    $encodingScript = Join-Path (Split-Path -Parent $skillRoot) "windows-encoding-rules\scripts\enable_powershell_utf8.ps1"
    # 2. 使用可用 PowerShell 委派回滚，并保留 WhatIf 的零写入语义。
    $shell = Find-ApplicationCommand -Candidates @("pwsh.exe", "powershell.exe")
    $arguments = @("-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $encodingScript, "-Mode", "Rollback", "-OutputFormat", "Json", "-TransactionPath", $TransactionPath)
    if (-not $AllowWrite) { $arguments += "-WhatIf" }
    $output = & $shell @arguments 2>&1
    $text = ($output | Out-String).Trim()
    try { return ($text | ConvertFrom-Json) } catch { throw "UTF-8 rollback returned invalid JSON: $text" }
}

function Invoke-PowerShellEnvironment {
    <#
    [参数]
    - Mode、Policy、PackageManager：环境操作、工具策略和包管理器选择。
    - ManifestPath、StateDirectory、JournalPath：规则与状态存储路径。
    - SessionTtlMinutes、SkipToolInstall、TerminalSettingsPath、SkipTerminalDefault、SkipEncodingBootstrap：会话和可选步骤控制项。
    - TestMode、ProfileRoot、AllowWrite：隔离测试和真实写入控制项。
    - OnlyCommand、CommandPackageId、CommandProbe、CommandSource、ShellHost：命令恢复和宿主可见性参数。
    [返回]
    - 统一的环境状态、问题、变更和可继续标识。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param(
        [string]$Mode,
        [string]$Policy,
        [string]$PackageManager,
        [string]$ManifestPath,
        [string]$StateDirectory,
        [string]$JournalPath,
        [int]$SessionTtlMinutes,
        [switch]$SkipToolInstall,
        [string]$TerminalSettingsPath,
        [switch]$SkipTerminalDefault,
        [switch]$SkipEncodingBootstrap,
        [switch]$TestMode,
        [string]$ProfileRoot,
        [switch]$AllowWrite,
        [string]$OnlyCommand,
        [string]$CommandPackageId,
        [string]$CommandProbe,
        [string]$CommandSource,
        [string]$ShellHost
    )

    # 1. 初始化本次运行的结果和状态路径，所有后续证据都绑定同一 runId。
    $runId = [guid]::NewGuid().ToString("N")
    $result = New-EnvironmentResult -Mode $Mode -RunId $runId
    $paths = Get-EnvironmentStatePaths -StateDirectory $StateDirectory -JournalPath $JournalPath
    try {
        $manifest = Read-ToolManifest -ManifestPath $ManifestPath
        $sourceOrder = @($manifest.source_order)
        $managers = @(Get-PackageManagers -RequestedManager $PackageManager)

        if ($Mode -eq "RecoverCommand") {
            # 2. 命令恢复先确认 manifest 或精确动态映射，禁止未知命令触发猜测性安装。
            $tool = Get-ManifestToolByCommand -Manifest $manifest -CommandName $OnlyCommand
            $isDynamic = -not $tool
            if (-not $tool) {
                if (-not $CommandSource -or -not $CommandPackageId) {
                    Register-EnvironmentCase -Paths $paths -CommandName $OnlyCommand -State "candidate" -Reason "Unknown command has no exact approved package mapping." -AllowWrite:$AllowWrite
                    $result.status = "blocked"; $result.canContinue = $false; $result.requiredReady = $true
                    Add-EnvironmentIssue -Result $result -Code "unknown_command" -Severity "required" -Message "Unknown command requires CommandSource and CommandPackageId." -ToolKey $OnlyCommand
                    return [pscustomobject]$result
                }
                $dynamicProbe = if ($CommandProbe) { @($CommandProbe) } else { @("--version") }
                $tool = [pscustomobject]@{ key = "dynamic-$([IO.Path]::GetFileNameWithoutExtension($OnlyCommand))"; commands = @($OnlyCommand); version_probe = [pscustomobject]@{ arguments = $dynamicProbe }; required = $false; packages = $null }
            }
            $probe = Invoke-CommandProbe -Tool $tool
            $package = $null
            if ($isDynamic) {
                $package = Get-ExactPackage -Tool $tool -Managers $managers -SourceOrder $sourceOrder -RequestedSource $CommandSource -PackageId $CommandPackageId
            }
            if (-not $probe.success -and -not $SkipToolInstall) {
                if (-not $package) { $package = Get-ExactPackage -Tool $tool -Managers $managers -SourceOrder $sourceOrder -PackageId $null -RequestedSource $null }
                $install = Invoke-ExactPackageInstall -Package $package -AllowWrite:$AllowWrite
                if ($install.success) { $probe = Invoke-CommandProbe -Tool $tool }
            }
            if ($probe.success) {
                $result.status = "ready"; $result.canContinue = $true; $result.requiredReady = $true
                $visibility = Test-HostVisibility -Tool $tool -ShellHost $ShellHost
                if ($visibility.applicable -and -not $visibility.visible) { $result.restartRequired = $true; Add-EnvironmentIssue -Result $result -Code "path_visibility" -Severity "optional" -Message "The command exists but is not visible in the requested shell; start a fresh shell." -ToolKey $tool.key; $result.status = "degraded" }
                if ($isDynamic -and $package) { Register-DiscoveredTool -Paths $paths -Tool $tool -Probe $probe -Package $package -AllowWrite:$AllowWrite }
                Register-EnvironmentCase -Paths $paths -CommandName $OnlyCommand -State "verified" -Reason "Version probe succeeded." -AllowWrite:$AllowWrite
                $result.results += [pscustomobject]@{ key = $tool.key; command = $tool.commands[0]; required = $false; action = "recovered"; result = $probe }
            } else {
                $result.status = "blocked"; $result.canContinue = $false; $result.requiredReady = $true
                Add-EnvironmentIssue -Result $result -Code "recovery_failed" -Severity "required" -Message "Command recovery did not pass its version probe." -ToolKey $tool.key
                Register-EnvironmentCase -Paths $paths -CommandName $OnlyCommand -State "blocked" -Reason "Installation or version probe failed." -AllowWrite:$AllowWrite
            }
            return [pscustomobject]$result
        }

        if ($Mode -eq "Rollback") {
            # 3. 只按 journal 恢复未漂移文件，检测到用户后续修改必须拒绝覆盖。
            $journal = Read-EnvironmentJson -Path $paths.journal -DefaultValue $null -AllowWrite:$false
            if (-not $journal -or -not $journal.changes) { throw "No compatible journal is available for rollback." }
            foreach ($change in @($journal.changes)) {
                if ($change.kind -eq "utf8_profiles") {
                    $encodingRollback = Invoke-EncodingRollback -TransactionPath $change.transactionPath -AllowWrite:$AllowWrite
                    if ($encodingRollback.status -eq "rollback_refused") {
                        $result.status = "rollback_refused"; $result.canContinue = $false; $result.requiredReady = $true
                        Add-EnvironmentIssue -Result $result -Code "encoding_rollback_drift" -Severity "required" -Message $encodingRollback.message -ToolKey "utf8_profiles"
                        return [pscustomobject]$result
                    }
                    $result.changes += [pscustomobject]@{ kind = "utf8_profiles"; transactionPath = $change.transactionPath; restored = $true; planned = -not $AllowWrite }
                    continue
                }
                if (-not $change.backupPath -or -not $change.path -or -not $change.afterHash) { continue }
                if ((Get-EnvironmentHash -Path $change.path) -ne $change.afterHash) {
                    $result.status = "rollback_refused"; $result.canContinue = $false; $result.requiredReady = $true
                    Add-EnvironmentIssue -Result $result -Code "rollback_drift" -Severity "required" -Message "Rollback refused because '$($change.path)' changed after Apply." -ToolKey $null
                    return [pscustomobject]$result
                }
                if ($AllowWrite) { Copy-Item -LiteralPath $change.backupPath -Destination $change.path -Force }
                $result.changes += [pscustomobject]@{ kind = "restored"; path = $change.path; planned = -not $AllowWrite }
            }
            $result.status = "rolled_back"; $result.canContinue = $true; $result.requiredReady = $true
            return [pscustomobject]$result
        }

        # 4. 会话和 Doctor 默认 RequiredOnly，避免扩展工具不足阻断当前专项操作。
        $effectivePolicy = if ($Policy) { $Policy } elseif ($Mode -in @("SessionEnsure", "Doctor")) { "RequiredOnly" } else { "Extended" }
        $tools = @(Get-PolicyTools -Manifest $manifest -Policy $effectivePolicy)
        if ($Mode -eq "SessionEnsure") {
            # 5. 新鲜 marker 仅缓存 ready/degraded，直接复用时不会触发重复安装。
            $marker = Read-EnvironmentJson -Path $paths.marker -DefaultValue $null -AllowWrite:$AllowWrite
            if (Test-SessionMarkerFresh -Marker $marker) {
                $result.status = [string]$marker.status; $result.canContinue = $true; $result.requiredReady = $true
                $result.results += [pscustomobject]@{ key = "session-marker"; command = $null; required = $true; action = "cached"; result = $marker }
                return [pscustomobject]$result
            }
        }

        # 6. 写入模式先取得互斥锁，再执行工具、编码和 Terminal 事务，避免并发互相覆盖状态。
        $mutatingMode = $Mode -in @("Apply", "SessionEnsure")
        $lock = if ($mutatingMode) { Acquire-EnvironmentLock -Paths $paths -AllowWrite:$AllowWrite -RunId $runId -Mode $Mode } else { $null }
        if ($mutatingMode -and -not $lock.acquired) {
            $result.status = "busy"; $result.canContinue = $false; $result.requiredReady = $false
            Add-EnvironmentIssue -Result $result -Code "state_lock_busy" -Severity "required" -Message "Another environment operation is active." -ToolKey $null
            return [pscustomobject]$result
        }
        try {
            Inspect-EnvironmentTools -Result $result -Tools $tools -Managers $managers -SourceOrder $sourceOrder -InstallMissing:($mutatingMode -and -not $SkipToolInstall) -AllowWrite:$AllowWrite
            Set-ResultStatus -Result $result
            $encodingTransaction = $null
            if ($result.status -ne "blocked" -and -not $SkipEncodingBootstrap) {
                # 6.1 只有工具必需条件已通过才初始化 profile，避免阻断状态仍修改用户环境。
                $encodingMode = if ($mutatingMode) { "Apply" } else { "Audit" }
                $encodingTransaction = Invoke-EncodingTransaction -Paths $paths -RunId $runId -Mode $encodingMode -AllowWrite:$AllowWrite -TestMode:$TestMode -ProfileRoot $ProfileRoot
                $encodingStatus = [string]$encodingTransaction.result.status
                $encodingReady = $encodingStatus -in @("ready", "rolled_back", "what_if")
                $result.results += [pscustomobject]@{ key = "utf8_profiles"; command = "enable_powershell_utf8.ps1"; required = $true; action = $encodingMode.ToLowerInvariant(); result = $encodingTransaction.result }
                if (-not $encodingReady) {
                    Add-EnvironmentIssue -Result $result -Code "utf8_profile_not_ready" -Severity "required" -Message ([string]$encodingTransaction.result.message) -ToolKey "utf8_profiles"
                    Set-ResultStatus -Result $result
                } elseif ($mutatingMode -and $AllowWrite) {
                    $result.changes += [pscustomobject]@{ kind = "utf8_profiles"; transactionPath = $encodingTransaction.transactionPath; planned = $false }
                }
            }
            if ($Mode -eq "Apply" -and $result.status -ne "blocked" -and -not $SkipTerminalDefault) {
                # 6.2 Terminal 写入失败时立即回滚同一 run 的 profile，避免跨文件事务只完成一半。
                try {
                    $terminalPath = Get-TerminalSettingsPath -TerminalSettingsPath $TerminalSettingsPath
                    if (-not $terminalPath) { throw "Windows Terminal settings.json was not found." }
                    Set-TerminalPowerShellProfile -Result $result -Paths $paths -RunId $runId -TerminalSettingsPath $terminalPath -AllowWrite:$AllowWrite
                } catch {
                    if ($encodingTransaction -and $AllowWrite) { [void](Invoke-EncodingRollback -TransactionPath $encodingTransaction.transactionPath -AllowWrite:$true) }
                    throw
                }
            }
            if ($Mode -eq "SessionEnsure") {
                # 7. 将 ready/degraded 写为可复用标记，可选缺项只记录限制而不改变完成语义。
                $marker = [pscustomobject]@{ schemaVersion = 2; completedAt = (Get-Date).ToString("o"); expiresAt = (Get-Date).AddMinutes($SessionTtlMinutes).ToString("o"); complete = ($result.status -in @("ready", "degraded")); status = $result.status; policy = $effectivePolicy; optionalIssues = @($result.issues | Where-Object { $_.severity -eq "optional" } | ForEach-Object { $_.toolKey }) }
                Save-EnvironmentJson -Value $marker -Path $paths.marker -AllowWrite:$AllowWrite
            }
            if ($Mode -in @("Apply", "SessionEnsure")) {
                Save-EnvironmentJson -Value ([pscustomobject]$result) -Path $paths.journal -AllowWrite:$AllowWrite
            }
        } finally {
            # 8. 无论检查或事务结果如何都释放锁，避免异常路径永久阻断后续会话。
            if ($mutatingMode) { Release-EnvironmentLock -Lock $lock -Paths $paths -AllowWrite:$AllowWrite }
        }
        return [pscustomobject]$result
    } catch {
        # 捕获未分类内部异常并转换为 failed，确保调用方无需解析 PowerShell 异常文本。
        $result.status = "failed"; $result.canContinue = $false; $result.requiredReady = $false
        Add-EnvironmentIssue -Result $result -Code "environment_internal_error" -Severity "required" -Message $_.Exception.Message -ToolKey $null
        return [pscustomobject]$result
    }
}

function Get-EnvironmentExitCode {
    <#
    [参数]
    - Result：统一环境结果对象。
    [返回]
    - 与稳定状态对应的进程退出码；未知状态返回 12。
    最近修改时间
    2026-07-13 22:27:24：补齐环境核心模块的可维护注释。
    #>
    param([object]$Result)
    # 1. 只暴露已定义的稳定退出码，未知状态统一归为内部失败。
    if ($script:StatusExitCodes.ContainsKey([string]$Result.status)) { return [int]$script:StatusExitCodes[[string]$Result.status] }
    return 12
}

Export-ModuleMember -Function Invoke-PowerShellEnvironment, Get-EnvironmentExitCode
