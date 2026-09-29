@echo off
setlocal enabledelayedexpansion
title TrustGuard AI — Setup Windows Task Scheduler Auto-Start

cd /d "%~dp0"

echo =================================================================
echo        TRUSTGUARD AI -- SETUP WINDOWS AUTO-START TASK
echo =================================================================
echo.

set "TASK_NAME=TrustGuardAI-AutoStart"
set "TARGET_CMD=%~dp0start_trustguard_background.vbs"

echo Registering Scheduled Task: %TASK_NAME%
echo Target Program: %TARGET_CMD%
echo.

:: Try creating task with user logon trigger
schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \"%TARGET_CMD%\"" /sc ONLOGON /rl HIGHEST /f >nul 2>&1
if %ERRORLEVEL% neq 0 (
    :: Fallback without highest elevation flag for standard user privileges
    schtasks /create /tn "%TASK_NAME%" /tr "wscript.exe \"%TARGET_CMD%\"" /sc ONLOGON /f >nul 2>&1
)

if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Windows Task "%TASK_NAME%" created successfully.
    echo TrustGuard AI will automatically launch whenever you log into Windows.
) else (
    echo [NOTICE] Standard Task Scheduler registration required elevated privileges.
    echo Installing fallback Windows User Startup shortcut...
    python scripts\install_startup_shortcut.py
)

echo.
echo Also installing zero-admin Windows Startup folder shortcut for redundancy...
python scripts\install_startup_shortcut.py

echo.
echo =================================================================
echo Setup Complete!
echo =================================================================
echo.
pause
