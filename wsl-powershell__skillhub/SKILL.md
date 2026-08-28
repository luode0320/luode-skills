---
name: wsl-powershell
description: Call Windows PowerShell from WSL to control the Windows host from a Linux environment. Triggers when the agent needs to execute PowerShell commands or .ps1 scripts from WSL, convert WSL/Windows paths, or query Windows services, processes, system info, and network state.
license: Apache-2.0
metadata:
  author: TYzzt
  version: "1.1"
  compatibility: WSL2 + Windows 10/11, Windows PowerShell 5.1 or PowerShell 7
---

# WSL-PowerShell Controller

Call Windows PowerShell from WSL to control the Windows host from a Linux environment.

## Trigger conditions

- Executing PowerShell commands or `.ps1` scripts from WSL.
- Querying Windows host state: services, processes, system info, network config.
- Converting paths between WSL (`/mnt/...`) and Windows (`C:\...`).
- Any task that needs Windows-native tooling from a Linux shell context.

## How It Works

WSL mounts Windows drives to `/mnt/`, allowing direct execution of Windows binaries:

- PowerShell: `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- CMD: `/mnt/c/Windows/System32/cmd.exe`

## PowerShell host selection (priority)

1. **PowerShell 7** (`/mnt/c/Program Files/PowerShell/7/pwsh.exe`) — preferred when available.
2. **Windows PowerShell 5.1** (`powershell.exe`) — fallback for compatibility only.

Inline invocations must always use the standard prefix:

```bash
# PowerShell 7 (default path)
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "<command>"

# Windows PowerShell 5.1 fallback (set UTF-8 output encoding inside the command)
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [Console]::OutputEncoding; <command>"
```

The canonical copy of this prefix lives in `windows-encoding-rules/SKILL.md` (section "调用 PowerShell 命令时的标准化前缀"); do not fork or drift from it. `psctl.sh` applies these rules automatically — prefer it over hand-built invocations.

## Usage

### Execute PowerShell Commands

```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "Your-Command"
```

### Execute PowerShell Scripts

```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -File "/mnt/c/path/to/script.ps1"
```

### Prefer the bundled controller

```bash
# Execute PowerShell command (auto host selection + standard prefix)
./psctl.sh "Get-Process | Select-Object -First 5 Name,Id"

# Execute a script file (Windows path or /mnt path; WSL-native paths use stdin mode)
./psctl.sh -f /mnt/c/scripts/myscript.ps1

# Force PowerShell Core
./psctl.sh -p "Get-Module -ListAvailable"

# Check PowerShell availability
./psctl.sh --check
```

## Common Examples

### System Information
```bash
# Get system info
powershell.exe -Command "Get-ComputerInfo"

# Get process list
powershell.exe -Command "Get-Process | Select-Object -First 10 Name,Id,CPU"

# Get service status
powershell.exe -Command "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -First 10 Name,DisplayName"
```

### File Operations
```bash
# List directory
powershell.exe -Command "Get-ChildItem C:\\Users"

# Copy file
powershell.exe -Command "Copy-Item C:\\source\\file.txt C:\\dest\\file.txt"

# Create file
powershell.exe -Command "New-Item -Path C:\\test.txt -ItemType File -Force"
```

### Process Management
```bash
# Start program
powershell.exe -Command "Start-Process notepad.exe"

# Stop process
powershell.exe -Command "Stop-Process -Name notepad -Force"
```

### Network Operations
```bash
# Get network config
powershell.exe -Command "Get-NetIPConfiguration"

# Ping test
powershell.exe -Command "Test-Connection -ComputerName google.com -Count 2"
```

## Path Conversion

WSL Path ↔ Windows Path:

- WSL: `/mnt/c/Users/Tao` ↔ Windows: `C:\Users\Tao`
- Use `wslpath` command:
  ```bash
  wslpath -w /mnt/c/Users  # Output: C:\Users
  wslpath -u C:\\Users     # Output: /mnt/c/Users
  ```

## Failure fallback decision table

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `command not found` / `not recognized` | Cmdlet missing in 5.1 or host not resolved | Re-run with PowerShell 7 (`-p`) or `psctl.sh --check` |
| Output is mojibake / Chinese broken | 5.1 ANSI default output encoding | Re-run via 5.1 standard prefix with UTF-8 preamble (`psctl.sh` does this automatically) |
| Script blocked / execution policy error | ExecutionPolicy restricts the script | Use `-ExecutionPolicy Bypass` in the prefix; never change policy globally |
| `$_.Status` quoting breaks in bash | Bash consumed `$` inside double quotes | Escape as `\$` or single-quote the whole `-Command` string |
| `C:\...` path not found from WSL | WSL path passed where a Windows path is required | Convert with `wslpath -w` or `psctl.sh -w` |
| `.ps1` on WSL-native path (no `/mnt`) | Windows cannot see the WSL filesystem | Use stdin mode (`psctl.sh -f` auto-falls back) or copy via `win-copy` |

Rules:

1. Never silently switch host or shell — state the fallback explicitly.
2. Preserve command intent; only translate syntax and paths.
3. For encoding-related failures, first re-run through `windows-encoding-rules` guidance; do not retry the same raw invocation unchanged.

## Notes

1. **Permissions**: Some operations require administrator privileges, use `-Verb RunAs` for elevated PowerShell
2. **Path Escaping**: Backslashes `\` in Windows paths must be escaped as `\\`
3. **Encoding**: PowerShell 5.1 outputs ANSI/UTF-16 by default, may need conversion — see `windows-encoding-rules`
4. **Execution Policy**: Running scripts may require `Set-ExecutionPolicy`

## Related skills (cross-references)

- `windows-encoding-rules` — canonical PowerShell standard prefix and UTF-8 writing policy (encoding failures).
- `charset-fix` — repairing already-corrupted Chinese/Unicode files.
- `wsl-windows-bridge` — `win-path` / `win-copy` / `win-ps` wrappers for WSL↔Windows interop and credential sync.
- `wsl-shell-reliability` — shell selection decision table (WSL vs PowerShell vs CMD).

## Security Tips

- Use caution with system-level commands
- Avoid deleting critical system files
- Test commands before executing in production
