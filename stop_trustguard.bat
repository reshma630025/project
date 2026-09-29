@echo off
setlocal enabledelayedexpansion
title TrustGuard AI — Stop Local Server

cd /d "%~dp0"

echo =================================================================
echo        TRUSTGUARD AI -- STOP LOCAL SERVER (PORT 8000)
echo =================================================================
echo.

set "FOUND=0"
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    set "PID=%%p"
    if defined PID (
        set "FOUND=1"
        echo Terminating process with PID: !PID!...
        taskkill /F /PID !PID! >nul 2>&1
    )
)

if "!FOUND!"=="1" (
    echo.
    echo TrustGuard AI server on port 8000 has been STOPPED.
    echo [%DATE% %TIME%] Server stopped via stop_trustguard.bat >> logs\server.log
) else (
    echo No active TrustGuard AI process found listening on port 8000.
)

echo.
echo Press any key to close...
timeout /t 3 >nul
