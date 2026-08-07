[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RequestPath,

    [Parameter(Mandatory = $true)]
    [string]$ResponsePath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$FixedVaultRoot = 'D:\obsidian_data'
$FixedKnowledgePrefix = ([char]0x77e5).ToString() + ([char]0x8bc6).ToString() + ([char]0x5e93).ToString() + '/'
$AllowedOperations = @(
    'doctor', 'search', 'search_context', 'read', 'create', 'append', 'open',
    # 迭代治理只读组
    'property_read', 'properties', 'backlinks', 'files', 'orphans',
    # 迭代治理写操作组；delete 固定进回收站，不透传 permanent
    'property_set', 'move', 'delete'
)
# 只读组直接回传 CLI 输出，不需要写入回读
$ReadOnlyOperations = @('property_read', 'properties', 'backlinks', 'files', 'orphans')
# 需要校验 vault 相对路径的操作；orphans 与 files 的 folder 单独处理
$PathOperations = @(
    'read', 'create', 'append', 'open',
    'property_read', 'properties', 'backlinks', 'property_set', 'move', 'delete'
)

function Get-RequestValue {
    param(
        [Parameter(Mandatory = $true)]$Request,
        [Parameter(Mandatory = $true)][string]$Name,
        $Default = $null
    )

    $property = $Request.PSObject.Properties[$Name]
    if ($null -eq $property) {
        return $Default
    }
    return $property.Value
}

function Write-AdapterResponse {
    param([Parameter(Mandatory = $true)]$Response)

    $directory = Split-Path -Parent $ResponsePath
    if (-not [string]::IsNullOrWhiteSpace($directory) -and -not (Test-Path -LiteralPath $directory)) {
        [System.IO.Directory]::CreateDirectory($directory) | Out-Null
    }
    $json = $Response | ConvertTo-Json -Depth 8 -Compress
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($ResponsePath, $json, $utf8)
}

function Get-ExitCodeFor {
    param([Parameter(Mandatory = $true)][string]$Code)

    if ($Code -in @('INVALID_ARGUMENT', 'PATH_OUTSIDE_KNOWLEDGE', 'LEGACY_NESTED_VAULT_MODEL')) {
        return 2
    }
    if ($Code -in @('UNSUPPORTED_HOST', 'WSL_INTEROP_UNAVAILABLE', 'POWERSHELL_UNAVAILABLE')) {
        return 3
    }
    if ($Code -in @('CLI_NOT_FOUND', 'OBSIDIAN_APP_UNAVAILABLE')) {
        return 4
    }
    if ($Code -in @('VAULT_NOT_REGISTERED', 'VAULT_ROOT_AMBIGUOUS')) {
        return 5
    }
    if ($Code -eq 'READBACK_MISMATCH') {
        return 7
    }
    return 6
}

function Throw-AdapterError {
    param(
        [Parameter(Mandatory = $true)][string]$Code,
        [Parameter(Mandatory = $true)][string]$Message
    )

    throw ($Code + '|' + $Message)
}

function Normalize-WindowsPath {
    param([Parameter(Mandatory = $true)][string]$Path)

    return $Path.Trim().Replace('/', '\').TrimEnd('\').ToLowerInvariant()
}

function Find-ObsidianCli {
    $override = [Environment]::GetEnvironmentVariable('OBSIDIAN_CLI_PATH')
    $candidates = @()
    if (-not [string]::IsNullOrWhiteSpace($override)) {
        $candidates += $override
    }
    if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
        $candidates += (Join-Path $env:LOCALAPPDATA 'Programs\Obsidian\Obsidian.com')
    }
    if (-not [string]::IsNullOrWhiteSpace($env:ProgramFiles)) {
        $candidates += (Join-Path $env:ProgramFiles 'Obsidian\Obsidian.com')
    }
    $programFilesX86 = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
    if (-not [string]::IsNullOrWhiteSpace($programFilesX86)) {
        $candidates += (Join-Path $programFilesX86 'Obsidian\Obsidian.com')
    }
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    Throw-AdapterError 'CLI_NOT_FOUND' 'The official Obsidian CLI was not found.'
}

function Find-ObsidianApp {
    param([Parameter(Mandatory = $true)][string]$CliPath)

    $override = [Environment]::GetEnvironmentVariable('OBSIDIAN_APP_PATH')
    if (-not [string]::IsNullOrWhiteSpace($override) -and (Test-Path -LiteralPath $override -PathType Leaf)) {
        return (Resolve-Path -LiteralPath $override).Path
    }
    $candidate = Join-Path (Split-Path -Parent $CliPath) 'Obsidian.exe'
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        return (Resolve-Path -LiteralPath $candidate).Path
    }
    Throw-AdapterError 'OBSIDIAN_APP_UNAVAILABLE' 'The Obsidian application executable was not found.'
}

function Quote-WindowsArgument {
    param([Parameter(Mandatory = $true)][string]$Value)

    if ($Value.Length -eq 0) {
        return '""'
    }
    $escaped = [System.Text.StringBuilder]::new()
    [void]$escaped.Append('"')
    $slashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') {
            $slashes++
            continue
        }
        if ($character -eq '"') {
            [void]$escaped.Append(('\' * (($slashes * 2) + 1)))
            [void]$escaped.Append('"')
            $slashes = 0
            continue
        }
        if ($slashes -gt 0) {
            [void]$escaped.Append(('\' * $slashes))
            $slashes = 0
        }
        [void]$escaped.Append($character)
    }
    if ($slashes -gt 0) {
        [void]$escaped.Append(('\' * ($slashes * 2)))
    }
    [void]$escaped.Append('"')
    return $escaped.ToString()
}

function Invoke-ObsidianCli {
    param(
        [Parameter(Mandatory = $true)][string]$CliPath,
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds
    )

    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $commandArguments = @($Arguments)
    $extension = [System.IO.Path]::GetExtension($CliPath)
    # Contract fixtures use an explicit interpreter; production still executes Obsidian.com directly.
    if ($extension.Equals('.ps1', [System.StringComparison]::OrdinalIgnoreCase)) {
        $startInfo.FileName = Join-Path $PSHOME 'powershell.exe'
        $commandArguments = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $CliPath) + $Arguments
    } elseif ($extension.Equals('.py', [System.StringComparison]::OrdinalIgnoreCase)) {
        $pythonPath = [Environment]::GetEnvironmentVariable('OBSIDIAN_TEST_PYTHON')
        if ([string]::IsNullOrWhiteSpace($pythonPath)) {
            Throw-AdapterError 'CLI_FAILED' 'The contract fixture Python interpreter is unavailable.'
        }
        $startInfo.FileName = $pythonPath
        $commandArguments = @($CliPath) + $Arguments
    } else {
        $startInfo.FileName = $CliPath
    }
    $startInfo.Arguments = (($commandArguments | ForEach-Object { Quote-WindowsArgument ([string]$_) }) -join ' ')
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
    $startInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    if (-not $process.Start()) {
        Throw-AdapterError 'CLI_FAILED' 'The Obsidian CLI could not be started.'
    }
    # Start both drains before waiting so a large response cannot fill the redirected pipe.
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $finished = $process.WaitForExit($TimeoutSeconds * 1000)
    if (-not $finished) {
        try {
            $process.Kill()
        } catch {
            # The timed out CLI may already have exited between the checks.
        }
        $process.WaitForExit()
        $stdoutTask.Wait()
        $stderrTask.Wait()
        Throw-AdapterError 'CLI_TIMEOUT' 'The Obsidian CLI timed out.'
    }
    $process.WaitForExit()
    $stdout = $stdoutTask.Result
    $stderr = $stderrTask.Result
    return [pscustomobject]@{
        ExitCode = $process.ExitCode
        StdOut = $stdout
        StdErr = $stderr
    }
}

function Test-AppUnavailable {
    param([Parameter(Mandatory = $true)]$Result)

    if ($Result.ExitCode -eq 0) {
        return $false
    }
    $text = (($Result.StdErr + "`n" + $Result.StdOut).ToLowerInvariant())
    return $text.Contains('unable to find obsidian') -or $text.Contains('cannot find obsidian')
}

# [Parameters] Result: the completed CLI process; RejectErrorPayload: whether this preflight command has no user-content output.
# [Returns] True only when the process succeeded and any required preflight payload is not an Error response.
# Last modified: 2026-07-13 15:52:23 Preserve user note bodies that legitimately begin with Error:.
function Test-CliOperationSuccess {
    param(
        [Parameter(Mandatory = $true)]$Result,
        [bool]$RejectErrorPayload = $false
    )

    # 1. User-facing commands can return arbitrary Markdown, so only preflight commands may interpret Error: as a CLI failure.
    if ($Result.ExitCode -ne 0) {
        return $false
    }
    if (-not $RejectErrorPayload) {
        return $true
    }
    $output = ($Result.StdOut + "`n" + $Result.StdErr).TrimStart()
    return -not $output.StartsWith('Error:', [System.StringComparison]::OrdinalIgnoreCase)
}

# [Parameters] CliPath: official CLI path; AutoStart: whether one hidden start is allowed; StartupWaitSeconds and TimeoutSeconds: bounded recovery budgets.
# [Returns] Startup attempt metadata and verified CLI version.
# Last modified: 2026-07-13 15:52:23 Reject Error: payloads only while version preflight has no user-content ambiguity.
function Assert-CliReady {
    param(
        [Parameter(Mandatory = $true)][string]$CliPath,
        [Parameter(Mandatory = $true)][bool]$AutoStart,
        [Parameter(Mandatory = $true)][int]$StartupWaitSeconds,
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds
    )

    # 1. Version output is preflight metadata, so an Error: payload is a CLI failure rather than note content.
    $attempts = 1
    $startedApp = $false
    $result = Invoke-ObsidianCli $CliPath @('version') $TimeoutSeconds
    if (Test-CliOperationSuccess $result $true) {
        return [pscustomobject]@{ Attempts = $attempts; StartedApp = $startedApp; Version = $result.StdOut.Trim() }
    }
    if (-not (Test-AppUnavailable $result)) {
        Throw-AdapterError 'CLI_FAILED' 'The Obsidian CLI failed before vault discovery.'
    }
    if (-not $AutoStart) {
        Throw-AdapterError 'OBSIDIAN_APP_UNAVAILABLE' 'The Obsidian application is unavailable.'
    }

    $appPath = Find-ObsidianApp $CliPath
    # Test seams can use an interpreter shim; real Obsidian starts as the normal hidden executable.
    $appExtension = [System.IO.Path]::GetExtension($appPath)
    if ($appExtension.Equals('.ps1', [System.StringComparison]::OrdinalIgnoreCase)) {
        Start-Process -FilePath (Join-Path $PSHOME 'powershell.exe') -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $appPath) -WindowStyle Hidden | Out-Null
    } elseif ($appExtension.Equals('.py', [System.StringComparison]::OrdinalIgnoreCase)) {
        $pythonPath = [Environment]::GetEnvironmentVariable('OBSIDIAN_TEST_PYTHON')
        if ([string]::IsNullOrWhiteSpace($pythonPath)) {
            Throw-AdapterError 'OBSIDIAN_APP_UNAVAILABLE' 'The contract fixture Python interpreter is unavailable.'
        }
        Start-Process -FilePath $pythonPath -ArgumentList @($appPath) -WindowStyle Hidden | Out-Null
    } else {
        Start-Process -FilePath $appPath -WindowStyle Hidden | Out-Null
    }
    $startedApp = $true
    $deadline = [DateTime]::UtcNow.AddSeconds($StartupWaitSeconds)
    do {
        Start-Sleep -Milliseconds 500
        $attempts++
        $result = Invoke-ObsidianCli $CliPath @('version') $TimeoutSeconds
        if (Test-CliOperationSuccess $result $true) {
            return [pscustomobject]@{ Attempts = $attempts; StartedApp = $startedApp; Version = $result.StdOut.Trim() }
        }
    } while ([DateTime]::UtcNow -lt $deadline)

    Throw-AdapterError 'OBSIDIAN_APP_UNAVAILABLE' 'The Obsidian application did not become available after one startup attempt.'
}

# [Parameters] CliPath: official CLI path; TimeoutSeconds: bounded vault discovery timeout.
# [Returns] The single selector registered for the fixed vault root.
# Last modified: 2026-07-13 15:52:23 Keep Error: rejection scoped to vault-list preflight output.
function Resolve-VaultSelector {
    param(
        [Parameter(Mandatory = $true)][string]$CliPath,
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds
    )

    # 1. Vault listing is structured preflight output, not user-authored Markdown.
    $result = Invoke-ObsidianCli $CliPath @('vaults', 'verbose') $TimeoutSeconds
    if (-not (Test-CliOperationSuccess $result)) {
        Throw-AdapterError 'CLI_FAILED' 'The Obsidian CLI could not list registered vaults.'
    }
    $expected = Normalize-WindowsPath $FixedVaultRoot
    $matches = @()
    foreach ($line in $result.StdOut -split "`r?`n") {
        if ([string]::IsNullOrWhiteSpace($line)) {
            continue
        }
        # 2. The CLI emits vault records with a tab; reject only unstructured Error: output before whitespace fallback parsing.
        if (-not $line.Contains("`t") -and $line.TrimStart().StartsWith('Error:', [System.StringComparison]::OrdinalIgnoreCase)) {
            Throw-AdapterError 'CLI_FAILED' 'The Obsidian CLI returned an invalid vault listing.'
        }
        $parts = $line -split "`t", 2
        if ($parts.Count -ne 2) {
            $parts = $line -split '\s+', 2
        }
        if ($parts.Count -ne 2) {
            continue
        }
        if ((Normalize-WindowsPath $parts[1]) -eq $expected) {
            $matches += $parts[0].Trim()
        }
    }
    # Do not collapse duplicate registrations: the contract requires exactly one matching record.
    $selectors = @($matches | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    if ($selectors.Count -eq 0) {
        Throw-AdapterError 'VAULT_NOT_REGISTERED' 'No registered vault matches the fixed vault root.'
    }
    if ($selectors.Count -ne 1) {
        Throw-AdapterError 'VAULT_ROOT_AMBIGUOUS' 'More than one registered vault matches the fixed vault root.'
    }
    return $selectors[0]
}

function Test-KnowledgePath {
    param(
        [Parameter(Mandatory = $true)][string]$Path
    )

    # Validate against the fixed prefix again because the adapter must not trust bridge input.
    if ([string]::IsNullOrWhiteSpace($Path) -or $Path -ne $Path.Trim()) {
        Throw-AdapterError 'PATH_OUTSIDE_KNOWLEDGE' 'path is outside the fixed knowledge prefix.'
    }
    $normalizedPath = $Path.Replace('\', '/')
    if ($normalizedPath.StartsWith('/') -or $normalizedPath -match '^[A-Za-z]:' -or $Path.StartsWith('\\') -or -not $normalizedPath.StartsWith($FixedKnowledgePrefix, [System.StringComparison]::Ordinal)) {
        Throw-AdapterError 'PATH_OUTSIDE_KNOWLEDGE' 'path is outside the configured knowledge prefix.'
    }
    $parts = $normalizedPath.Split('/')
    if ($parts.Count -lt 2) {
        Throw-AdapterError 'PATH_OUTSIDE_KNOWLEDGE' 'path is outside the configured knowledge prefix.'
    }
    foreach ($part in $parts) {
        if ([string]::IsNullOrWhiteSpace($part) -or $part -in @('.', '..') -or $part.EndsWith(' ') -or $part.EndsWith('.')) {
            Throw-AdapterError 'PATH_OUTSIDE_KNOWLEDGE' 'path contains an invalid segment.'
        }
        foreach ($character in $part.ToCharArray()) {
            if ([int][char]$character -lt 32 -or '<>:"|?*'.IndexOf($character) -ge 0) {
                Throw-AdapterError 'PATH_OUTSIDE_KNOWLEDGE' 'path contains an invalid character.'
            }
        }
    }
    return $normalizedPath
}

# [Parameters] Request: adapter request object received from bridge or a direct caller.
# [Returns] None; invalid input raises a stable adapter error before invoking the CLI.
# Last modified: 2026-07-13 15:52:23 Mirror bridge limit validation for callers that bypass it.
function Assert-Request {
    param([Parameter(Mandatory = $true)]$Request)

    # 1. Validate the frozen request envelope before any CLI discovery or vault operation.
    if ((Get-RequestValue $Request 'schema_version') -ne 1) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'schema_version must equal 1.'
    }
    $operation = [string](Get-RequestValue $Request 'operation')
    if ($operation -notin $AllowedOperations) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'operation is not allowed.'
    }
    $knowledgePrefix = [string](Get-RequestValue $Request 'knowledge_prefix')
    if ($knowledgePrefix -ne $FixedKnowledgePrefix) {
        Throw-AdapterError 'PATH_OUTSIDE_KNOWLEDGE' 'knowledge_prefix must equal the fixed knowledge prefix.'
    }
    $vaultRoot = [string](Get-RequestValue $Request 'vault_root')
    if ((Normalize-WindowsPath $vaultRoot) -ne (Normalize-WindowsPath $FixedVaultRoot)) {
        $legacyRoot = Normalize-WindowsPath ($FixedVaultRoot + '\' + $FixedKnowledgePrefix.TrimEnd('/'))
        if ((Normalize-WindowsPath $vaultRoot) -eq $legacyRoot) {
            Throw-AdapterError 'LEGACY_NESTED_VAULT_MODEL' 'The nested vault root is not supported.'
        }
        Throw-AdapterError 'INVALID_ARGUMENT' 'vault_root must equal the fixed vault root.'
    }
    $timeoutSeconds = Get-RequestValue $Request 'timeout_seconds' 30
    $startupWaitSeconds = Get-RequestValue $Request 'startup_wait_seconds' 15
    $chunkChars = Get-RequestValue $Request 'chunk_chars' 1800
    # ConvertFrom-Json may materialize numeric request fields as Int64 on Windows PowerShell.
    if (($timeoutSeconds -isnot [int] -and $timeoutSeconds -isnot [long]) -or $timeoutSeconds -lt 1 -or $timeoutSeconds -gt 300) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'timeout_seconds is outside the supported range.'
    }
    if (($startupWaitSeconds -isnot [int] -and $startupWaitSeconds -isnot [long]) -or $startupWaitSeconds -lt 0 -or $startupWaitSeconds -gt 15) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'startup_wait_seconds is outside the supported range.'
    }
    if (($chunkChars -isnot [int] -and $chunkChars -isnot [long]) -or $chunkChars -lt 1 -or $chunkChars -gt 1800) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'chunk_chars is outside the supported range.'
    }
    if ($operation -in $PathOperations) {
        $normalizedPath = Test-KnowledgePath ([string](Get-RequestValue $Request 'path'))
        $Request.PSObject.Properties['path'].Value = $normalizedPath
    }
    # 1. move 的目标路径与 files 的枚举目录同样受固定知识前缀约束。
    if ($operation -eq 'move') {
        $normalizedTarget = Test-KnowledgePath ([string](Get-RequestValue $Request 'to'))
        $Request.PSObject.Properties['to'].Value = $normalizedTarget
    }
    if ($operation -eq 'files' -and $null -ne (Get-RequestValue $Request 'folder')) {
        $normalizedFolder = Test-KnowledgePath ([string](Get-RequestValue $Request 'folder'))
        $Request.PSObject.Properties['folder'].Value = $normalizedFolder
    }
    if ($operation -in @('property_read', 'property_set') -and [string]::IsNullOrWhiteSpace([string](Get-RequestValue $Request 'property_name'))) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'property operations require a property name.'
    }
    if ($operation -eq 'property_set' -and [string]::IsNullOrWhiteSpace([string](Get-RequestValue $Request 'property_value'))) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'property_set requires a property value.'
    }
    if ($operation -in @('search', 'search_context')) {
        if ([string]::IsNullOrWhiteSpace([string](Get-RequestValue $Request 'query'))) {
            Throw-AdapterError 'INVALID_ARGUMENT' 'search requests require a query.'
        }
        $limit = Get-RequestValue $Request 'limit' 10
        if (($limit -isnot [int] -and $limit -isnot [long]) -or $limit -lt 1 -or $limit -gt 100) {
            Throw-AdapterError 'INVALID_ARGUMENT' 'limit must be an integer between 1 and 100.'
        }
    }
    if ($operation -in @('create', 'append') -and $null -eq (Get-RequestValue $Request 'content')) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'write requests require content.'
    }
}

# [参数] Content: 待写入的 Markdown 正文；ChunkChars: 单次 CLI 写入的最大字符数。
# [返回] 按自然换行边界拆分、可由 append 的隐含换行无损拼接的正文分块。
# 最近修改时间: 2026-07-13 18:38:00 按自然换行切块并配合 append 的隐含前置换行保持长正文一致。
function Split-Content {
    param(
        [Parameter(Mandatory = $true)][string]$Content,
        [Parameter(Mandatory = $true)][int]$ChunkChars
    )

    # 1. 空正文保留一个空分块，维持 create/append 的既有调用契约。
    if ($Content.Length -eq 0) {
        return @('')
    }
    $chunks = @()
    $remaining = $Content
    while ($remaining.Length -gt $ChunkChars) {
        # 2. 优先在限制内最后一个换行处分块，并消费该换行，让 append 自动补出的换行保持正文不变。
        $maxIndex = [Math]::Min($ChunkChars - 1, $remaining.Length - 1)
        $boundary = $remaining.LastIndexOf("`n", $maxIndex)
        if ($boundary -lt 0) {
            $boundary = $ChunkChars
            $consumeLength = $boundary
        } else {
            $consumeLength = $boundary + 1
        }
        $chunks += $remaining.Substring(0, $boundary)
        $remaining = $remaining.Substring($consumeLength)
    }
    # 3. 最后一块保留原始结尾，append 仅在正文没有换行时补隐含换行。
    $chunks += $remaining
    return $chunks
}

function Normalize-ReadbackText {
    param([Parameter(Mandatory = $true)][string]$Text)

    # 1. Windows CLI stdout may normalize newlines; compare logical Markdown text as LF.
    return $Text.Replace("`r`n", "`n").Replace("`r", "`n")
}

# [参数] CliPath: official CLI path; Selector: fixed-root vault selector; Request: validated operation request.
# [返回] Operation output and readback verification state.
# Last modified: 2026-07-13 18:38:00 Accept append's implicit leading newline during readback while preserving exact create comparison.
function Invoke-VaultOperation {
    param(
        [Parameter(Mandatory = $true)][string]$CliPath,
        [Parameter(Mandatory = $true)][string]$Selector,
        [Parameter(Mandatory = $true)]$Request
    )

    $operation = [string](Get-RequestValue $Request 'operation')
    $timeoutSeconds = [int](Get-RequestValue $Request 'timeout_seconds' 30)
    $base = @('vault=' + $Selector)
    if ($operation -eq 'doctor') {
        return [pscustomobject]@{ Output = ''; Verified = $true }
    }
    if ($operation -eq 'search' -or $operation -eq 'search_context') {
        $command = if ($operation -eq 'search_context') { 'search:context' } else { 'search' }
        # Keep query= and limit= intact: inline array concatenation can split each key from its value.
        $queryArgument = 'query=' + [string](Get-RequestValue $Request 'query')
        $limitArgument = 'limit=' + [string](Get-RequestValue $Request 'limit' 10)
        $result = Invoke-ObsidianCli $CliPath ($base + @($command, $queryArgument, $limitArgument)) $timeoutSeconds
        if (-not (Test-CliOperationSuccess $result)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian search command failed.' }
        return [pscustomobject]@{ Output = $result.StdOut; Verified = $true }
    }
    if ($operation -eq 'read' -or $operation -eq 'open') {
        # This CLI version accepts file= for read/open; path= returns an Error: payload with exit code zero.
        $fileArgument = 'file=' + [string](Get-RequestValue $Request 'path')
        $result = Invoke-ObsidianCli $CliPath ($base + @($operation, $fileArgument)) $timeoutSeconds
        if (-not (Test-CliOperationSuccess $result)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian read command failed.' }
        return [pscustomobject]@{ Output = $result.StdOut; Verified = $true }
    }
    if ($operation -in $ReadOnlyOperations) {
        # 1. 与 read/open 不同，这五个命令实测均接受 path=；orphans 不接受任何路径参数。
        $arguments = switch ($operation) {
            'property_read' { @('property:read', ('path=' + [string](Get-RequestValue $Request 'path')), ('name=' + [string](Get-RequestValue $Request 'property_name'))) }
            'properties' { @('properties', ('path=' + [string](Get-RequestValue $Request 'path')), 'format=json') }
            'backlinks' { @('backlinks', ('path=' + [string](Get-RequestValue $Request 'path')), 'total') }
            'files' {
                $folder = Get-RequestValue $Request 'folder'
                if ([string]::IsNullOrWhiteSpace([string]$folder)) { @('files') } else { @('files', ('folder=' + [string]$folder)) }
            }
            'orphans' { @('orphans') }
        }
        $result = Invoke-ObsidianCli $CliPath ($base + $arguments) $timeoutSeconds
        if (-not (Test-CliOperationSuccess $result)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian read-only command failed.' }
        return [pscustomobject]@{ Output = $result.StdOut; Verified = $true }
    }
    if ($operation -eq 'property_set') {
        $propertyName = [string](Get-RequestValue $Request 'property_name')
        $propertyValue = [string](Get-RequestValue $Request 'property_value')
        $arguments = @(
            'property:set',
            ('path=' + [string](Get-RequestValue $Request 'path')),
            ('name=' + $propertyName),
            ('value=' + $propertyValue),
            ('type=' + [string](Get-RequestValue $Request 'property_type' 'text'))
        )
        $result = Invoke-ObsidianCli $CliPath ($base + $arguments) $timeoutSeconds
        # 1. 写属性不返回用户正文，退出码为零的 Error 载荷同样视为失败。
        if (-not (Test-CliOperationSuccess $result $true)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian property:set command failed.' }
        # 2. 回读同一属性并逐字比对，证明值确实落盘。
        $readback = Invoke-ObsidianCli $CliPath ($base + @('property:read', ('path=' + [string](Get-RequestValue $Request 'path')), ('name=' + $propertyName))) $timeoutSeconds
        if (-not (Test-CliOperationSuccess $readback)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian property readback failed.' }
        if ((Normalize-ReadbackText $readback.StdOut).Trim() -ne (Normalize-ReadbackText $propertyValue).Trim()) {
            Throw-AdapterError 'READBACK_MISMATCH' ('Property ' + $propertyName + ' readback does not match the written value.')
        }
        return [pscustomobject]@{ Output = $result.StdOut; Verified = $true }
    }
    if ($operation -eq 'move') {
        $sourcePath = [string](Get-RequestValue $Request 'path')
        $targetPath = [string](Get-RequestValue $Request 'to')
        $result = Invoke-ObsidianCli $CliPath ($base + @('move', ('path=' + $sourcePath), ('to=' + $targetPath))) $timeoutSeconds
        # 1. 目标目录不存在时 CLI 以退出码零返回 ENOENT 载荷，原文件保持无损。
        if (-not (Test-CliOperationSuccess $result $true)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian move command failed; the target folder must already exist.' }
        # 2. 回读两端：新路径必须可读，旧路径必须已不可读。
        #    存在性探测必须用严格模式，因为 properties 对不存在的文件以退出码零返回 Error 载荷。
        $targetProbe = Invoke-ObsidianCli $CliPath ($base + @('properties', ('path=' + $targetPath), 'format=json')) $timeoutSeconds
        if (-not (Test-CliOperationSuccess $targetProbe $true)) { Throw-AdapterError 'READBACK_MISMATCH' 'The moved note is not readable at the target path.' }
        $sourceProbe = Invoke-ObsidianCli $CliPath ($base + @('properties', ('path=' + $sourcePath), 'format=json')) $timeoutSeconds
        if (Test-CliOperationSuccess $sourceProbe $true) { Throw-AdapterError 'READBACK_MISMATCH' 'The source note is still readable after the move.' }
        return [pscustomobject]@{ Output = $result.StdOut; Verified = $true }
    }
    if ($operation -eq 'delete') {
        $deletePath = [string](Get-RequestValue $Request 'path')
        # 1. 固定省略 permanent，删除只进回收站以保留可恢复性。
        $result = Invoke-ObsidianCli $CliPath ($base + @('delete', ('path=' + $deletePath))) $timeoutSeconds
        if (-not (Test-CliOperationSuccess $result $true)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian delete command failed.' }
        # 2. 回读原路径，必须已不可读；同样使用严格模式识别 Error 载荷。
        $probe = Invoke-ObsidianCli $CliPath ($base + @('properties', ('path=' + $deletePath), 'format=json')) $timeoutSeconds
        if (Test-CliOperationSuccess $probe $true) { Throw-AdapterError 'READBACK_MISMATCH' 'The deleted note is still readable.' }
        return [pscustomobject]@{ Output = $result.StdOut; Verified = $true }
    }

    $content = [string](Get-RequestValue $Request 'content')
    # 1. Force a collection so one short write has the same loop contract as chunked content.
    $chunks = @(Split-Content $content ([int](Get-RequestValue $Request 'chunk_chars' 1800)))
    $pathArgument = 'path=' + [string](Get-RequestValue $Request 'path')
    for ($index = 0; $index -lt $chunks.Count; $index++) {
        # Keep the payload as one argument; inline array expressions can split the content after '='.
        $contentArgument = 'content=' + [string]$chunks[$index]
        if ($operation -eq 'create' -and $index -eq 0) {
            $arguments = @($base) + @('create', $pathArgument, $contentArgument, 'overwrite')
        } else {
            $arguments = @($base) + @('append', $pathArgument, $contentArgument)
        }
        $result = Invoke-ObsidianCli $CliPath $arguments $timeoutSeconds
        # 1. create/append do not return user-authored Markdown, so a zero-exit Error: payload is a CLI failure.
        if (-not (Test-CliOperationSuccess $result $true)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian write command failed.' }
    }

    $verified = $true
    if ([bool](Get-RequestValue $Request 'verify_readback' $true)) {
        # Preserve file= and its value as one CLI argument during readback.
        $readbackFileArgument = 'file=' + [string](Get-RequestValue $Request 'path')
        $readback = Invoke-ObsidianCli $CliPath ($base + @('read', $readbackFileArgument)) $timeoutSeconds
        if (-not (Test-CliOperationSuccess $readback)) { Throw-AdapterError 'CLI_FAILED' 'The Obsidian readback command failed.' }
        $readbackText = Normalize-ReadbackText $readback.StdOut
        $expectedText = Normalize-ReadbackText $content
        $appendSuffixMatches = $readbackText.EndsWith($expectedText, [System.StringComparison]::Ordinal) -or $readbackText.EndsWith(($expectedText + "`n"), [System.StringComparison]::Ordinal)
        if (($operation -eq 'create' -and $readbackText -ne $expectedText) -or ($operation -eq 'append' -and -not $appendSuffixMatches)) {
            Throw-AdapterError 'READBACK_MISMATCH' ('Readback length ' + $readbackText.Length + ' does not match expected length ' + $expectedText.Length + '.')
        }
    }
    return [pscustomobject]@{ Output = ''; Verified = $verified }
}

try {
    if (-not (Test-Path -LiteralPath $RequestPath -PathType Leaf)) {
        Throw-AdapterError 'INVALID_ARGUMENT' 'The request JSON file does not exist.'
    }
    $requestText = [System.IO.File]::ReadAllText($RequestPath, [System.Text.Encoding]::UTF8)
    $request = $requestText | ConvertFrom-Json
    Assert-Request $request
    $cliPath = Find-ObsidianCli
    $timeoutSeconds = [int](Get-RequestValue $request 'timeout_seconds' 30)
    $ready = Assert-CliReady $cliPath ([bool](Get-RequestValue $request 'auto_start' $true)) ([int](Get-RequestValue $request 'startup_wait_seconds' 15)) $timeoutSeconds
    $selector = Resolve-VaultSelector $cliPath $timeoutSeconds
    $operationResult = Invoke-VaultOperation $cliPath $selector $request
    $response = [ordered]@{
        schema_version = 1
        ok = $true
        code = 'OK'
        operation = [string](Get-RequestValue $request 'operation')
        host = 'windows'
        transport = 'windows-direct'
        cli_path = $cliPath
        vault_root = $FixedVaultRoot
        vault_selector = $selector
        started_app = $ready.StartedApp
        attempts = $ready.Attempts
        verified = $operationResult.Verified
        data = @{ output = $operationResult.Output; version = $ready.Version }
    }
    Write-AdapterResponse $response
    exit 0
} catch {
    $message = $_.Exception.Message
    $code = 'CLI_FAILED'
    $separator = $message.IndexOf('|')
    if ($separator -gt 0) {
        $code = $message.Substring(0, $separator)
        $message = $message.Substring($separator + 1)
    }
    $response = [ordered]@{
        schema_version = 1
        ok = $false
        code = $code
        message = $message
    }
    Write-AdapterResponse $response
    exit (Get-ExitCodeFor $code)
}
