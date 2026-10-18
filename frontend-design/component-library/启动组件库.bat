@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Pearl Glass Component Library - Dev Server

rem ============================================================
rem Double-click launcher for the Pearl Glass component library dev server.
rem Keep this file pure ASCII: cmd.exe reads .bat by byte offset, so switching
rem the code page mid-file makes it resume mid-character and run the fragment.
rem Chinese prompts live in scripts\launch-message.mjs and are printed by node.
rem Stop: Ctrl+C or close this window; the port is released when the process exits.
rem Last modified: 2026-10-18 12:05:00; reason: force npm install on every launch to ensure latest dependencies.
rem ============================================================

chcp 65001 >nul

node scripts\launch-message.mjs welcome
if errorlevel 1 goto no_node

rem 1. Always install dependencies to ensure we have the latest locked versions.
node scripts\launch-message.mjs prepare
call npm install
if errorlevel 1 goto install_failed

node scripts\launch-message.mjs start

call npm run dev
set "EXIT_CODE=%errorlevel%"

rem 2. Keep the window open on abnormal exit so the error text is readable.
if not "%EXIT_CODE%"=="0" (
  node scripts\launch-message.mjs exit %EXIT_CODE%
  pause
)

exit /b %EXIT_CODE%

:no_node
node scripts\launch-message.mjs no-node 2>nul
echo   [FAIL] Node.js not found. Install Node.js 18+ from https://nodejs.org/
echo.
pause
exit /b 1

:install_failed
node scripts\launch-message.mjs install-failed 2>nul
echo   [FAIL] npm install failed. Check network or proxy, then retry.
echo          Manual fallback: npm install
echo.
pause
exit /b 1
