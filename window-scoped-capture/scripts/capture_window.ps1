# scripts/capture_window.ps1
# Window-scoped screenshot plus in-window click/key delivery.
#
# Why this exists: a full-screen grab captures every other application and
# depends on which window is in the foreground; global cursor injection lands
# on whatever happened to be under the pointer. This script instead:
#   1) captures only the selected process window via PrintWindow (the window may
#      be occluded without leaking other apps into the image);
#   2) delivers clicks/keys with PostMessage straight to that window, so it never
#      steals focus and never touches the real system cursor or keyboard.
#
# ASCII only on purpose: Windows PowerShell 5.1 reads .ps1 as ANSI, so non-ASCII
# text inside a script breaks its own syntax.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File capture_window.ps1 -List
#   powershell -NoProfile -ExecutionPolicy Bypass -File capture_window.ps1 -ProcessName <PROCESS_NAME> -Tag 01_menu
#   powershell -NoProfile -ExecutionPolicy Bypass -File capture_window.ps1 -Tag 02_admin -SendKeys F12
#   powershell -NoProfile -ExecutionPolicy Bypass -File capture_window.ps1 -Tag 03_center -Clicks "0.5,0.51"

param(
    [string]$ProcessName = "target",
    [int]$Hwnd = 0,
    [string]$OutDir = "output/window_shots",
    [string]$Tag = "shot",
    [string[]]$Clicks = @(),
    [string[]]$SendKeys = @(),
    [int]$WaitMs = 1500,
    [switch]$List
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

public class WinPick {
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    public delegate bool EnumProc(IntPtr h, IntPtr p);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr p);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] public static extern int GetWindowTextW(IntPtr h, StringBuilder s, int n);
    [DllImport("user32.dll")] public static extern int GetWindowThreadProcessId(IntPtr h, out int pid);
    [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
    [DllImport("user32.dll")] public static extern IntPtr PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);

    public const uint WM_MOUSEMOVE = 0x0200;
    public const uint WM_LBUTTONDOWN = 0x0201;
    public const uint WM_LBUTTONUP = 0x0202;
    public const uint WM_KEYDOWN = 0x0100;
    public const uint WM_KEYUP = 0x0101;

    public static List<IntPtr> ByPid(int pid) {
        var found = new List<IntPtr>();
        EnumWindows((h, p) => {
            if (!IsWindowVisible(h)) return true;
            int wpid; GetWindowThreadProcessId(h, out wpid);
            if (wpid != pid) return true;
            var sb = new StringBuilder(8); GetWindowTextW(h, sb, 8);
            if (sb.Length == 0) return true;
            RECT r; GetClientRect(h, out r);
            if (r.Right - r.Left < 64 || r.Bottom - r.Top < 64) return true;
            found.Add(h);
            return true;
        }, IntPtr.Zero);
        return found;
    }

    public static string Title(IntPtr h) {
        var sb = new StringBuilder(512); GetWindowTextW(h, sb, 512); return sb.ToString();
    }

    public static string Label(IntPtr h) {
        RECT r; GetClientRect(h, out r);
        return "hwnd=" + h + " size=" + (r.Right - r.Left) + "x" + (r.Bottom - r.Top) + " title=" + Title(h);
    }

    public static void ClickAt(IntPtr h, int x, int y) {
        IntPtr lp = (IntPtr)((y << 16) | (x & 0xFFFF));
        PostMessage(h, WM_MOUSEMOVE, IntPtr.Zero, lp);
        System.Threading.Thread.Sleep(80);
        PostMessage(h, WM_LBUTTONDOWN, (IntPtr)1, lp);
        System.Threading.Thread.Sleep(80);
        PostMessage(h, WM_LBUTTONUP, IntPtr.Zero, lp);
    }

    // Posts the key only to the target window: no real keyboard, no focus change.
    public static void TapKey(IntPtr h, int vk) {
        PostMessage(h, WM_KEYDOWN, (IntPtr)vk, IntPtr.Zero);
        System.Threading.Thread.Sleep(80);
        PostMessage(h, WM_KEYUP, (IntPtr)vk, IntPtr.Zero);
    }

    public static int VkOf(string name) {
        switch (name.ToUpperInvariant()) {
            case "F1": return 0x70; case "F2": return 0x71; case "F3": return 0x72;
            case "F4": return 0x73; case "F5": return 0x74; case "F6": return 0x75;
            case "F7": return 0x76; case "F8": return 0x77; case "F9": return 0x78;
            case "F10": return 0x79; case "F11": return 0x7A; case "F12": return 0x7B;
            case "ESC": case "ESCAPE": return 0x1B;
            case "TAB": return 0x09; case "SPACE": return 0x20; case "ENTER": return 0x0D;
            default: return -1;
        }
    }
}
"@

function Get-TargetWindow {
    if ($Hwnd -ne 0) { return [IntPtr]$Hwnd }
    $proc = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -eq $proc) { throw "process not found: $ProcessName" }
    $cands = [WinPick]::ByPid($proc.Id)
    if ($cands.Count -eq 0) { throw "no visible window for $ProcessName (pid=$($proc.Id))" }
    $best = $cands[0]
    $bestArea = 0
    foreach ($h in $cands) {
        $r = New-Object WinPick+RECT
        [void][WinPick]::GetClientRect($h, [ref]$r)
        $area = ($r.Right - $r.Left) * ($r.Bottom - $r.Top)
        if ($area -gt $bestArea) { $bestArea = $area; $best = $h }
    }
    return $best
}

function Save-WindowShot {
    param([IntPtr]$Handle, [string]$Path)
    $r = New-Object WinPick+RECT
    [void][WinPick]::GetClientRect($Handle, [ref]$r)
    $w = $r.Right - $r.Left
    $h = $r.Bottom - $r.Top
    $bmp = New-Object System.Drawing.Bitmap($w, $h)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $hdc = $g.GetHdc()
    # flags=2 asks for the client area only: no title bar, no occluded windows.
    [void][WinPick]::PrintWindow($Handle, $hdc, 2)
    $g.ReleaseHdc($hdc)
    $bmp.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    return "${w}x${h}"
}

if ($List) {
    $proc = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -eq $proc) { Write-Output "WINDOW_CAPTURE: no process $ProcessName"; exit 2 }
    foreach ($h in [WinPick]::ByPid($proc.Id)) { Write-Output ("WINDOW_CAPTURE: " + [WinPick]::Label($h)) }
    exit 0
}

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

$target = Get-TargetWindow
$rect = New-Object WinPick+RECT
[void][WinPick]::GetClientRect($target, [ref]$rect)
$clientW = $rect.Right - $rect.Left
$clientH = $rect.Bottom - $rect.Top
Write-Output ("WINDOW_CAPTURE: target " + [WinPick]::Label($target))

$shotIndex = 0
$first = Join-Path $OutDir "$Tag.png"
$size = Save-WindowShot -Handle $target -Path $first
Write-Output "WINDOW_CAPTURE: saved $first ($size) window-scoped only"

foreach ($key in $SendKeys) {
    $vk = [WinPick]::VkOf($key)
    if ($vk -lt 0) { Write-Output "WINDOW_CAPTURE: skip unknown key $key"; continue }
    Write-Output ("WINDOW_CAPTURE: post key $key vk=0x" + $vk.ToString("X2"))
    [WinPick]::TapKey($target, $vk)
    Start-Sleep -Milliseconds $WaitMs
    $shotIndex += 1
    $next = Join-Path $OutDir ("{0}_key{1}.png" -f $Tag, $shotIndex)
    $size = Save-WindowShot -Handle $target -Path $next
    Write-Output "WINDOW_CAPTURE: saved $next ($size)"
}

foreach ($c in $Clicks) {
    $parts = $c.Split(",")
    if ($parts.Count -ne 2) { Write-Output "WINDOW_CAPTURE: skip bad click $c"; continue }
    $px = [int]($clientW * [double]$parts[0])
    $py = [int]($clientH * [double]$parts[1])
    Write-Output "WINDOW_CAPTURE: click client=($px,$py)"
    [WinPick]::ClickAt($target, $px, $py)
    Start-Sleep -Milliseconds $WaitMs
    $shotIndex += 1
    $next = Join-Path $OutDir ("{0}_click{1}.png" -f $Tag, $shotIndex)
    $size = Save-WindowShot -Handle $target -Path $next
    Write-Output "WINDOW_CAPTURE: saved $next ($size)"
}

Write-Output "WINDOW_CAPTURE: DONE out=$OutDir"
