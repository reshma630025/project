@echo off
setlocal enabledelayedexpansion
title TrustGuard AI — Permanent Local Server & Platform Launcher

cd /d "%~dp0"

echo =================================================================
echo        TRUSTGUARD AI -- PERMANENT LOCAL SERVER (LOCAL + LAN)
echo =================================================================
echo.

:: 1. Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo       ERROR: Python is not installed or not in PATH. Please install Python.
    pause
    exit /b
)

:: 2. Check required packages
echo [2/6] Checking required packages...
python -c "import fastapi, uvicorn, torch, pandas" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo       Missing required packages. Attempting to install...
    python -m pip install -r requirements.txt >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        python -m pip install fastapi uvicorn torch pandas scikit-learn pillow >nul 2>&1
    )
)

:: 3. Detect the computer's active IPv4 LAN Address using Python
set "LAN_IP="
for /f "tokens=*" %%i in ('python scripts\detect_lan_ip.py 2^>nul') do (
    set "LINE=%%i"
    if "!LINE:~0,14!"=="ACTUAL_LAN_IP=" (
        set "LAN_IP=!LINE:~14!"
    )
)

if "%LAN_IP%"=="" set "LAN_IP=127.0.0.1"
echo [3/6] Detected Active LAN IPv4 Address: %LAN_IP%

:: 4. Check if port 8000 is already active and responding
echo [4/6] Checking server port 8000...
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo       Server is already running on port 8000. Skipping duplicate process launch.
) else (
    echo       Starting FastAPI backend on 0.0.0.0:8000 (Python)...
    start "TrustGuard AI Server" /min python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
)

:: 5. Wait until /api/status responds successfully
echo [5/6] Waiting for backend /api/status health check to respond...
set "SERVER_READY=0"
for /l %%k in (1,1,20) do (
    if "!SERVER_READY!"=="0" (
        python -c "import urllib.request; resp=urllib.request.urlopen('http://127.0.0.1:8000/api/status', timeout=1); exit(0 if resp.getcode()==200 else 1)" >nul 2>&1
        if !ERRORLEVEL! equ 0 (
            set "SERVER_READY=1"
        ) else (
            timeout /t 1 /nobreak >nul
        )
    )
)

if "!SERVER_READY!"=="1" (
    echo       Backend health check passed: OK (HTTP 200).
) else (
    echo       Warning: Backend took longer than expected to report status.
)

:: Append to startup log
echo [%DATE% %TIME%] Server started/verified on 0.0.0.0:8000 (LAN: %LAN_IP%) >> logs\server.log

:: 6. Launch browser only after health check
echo [6/6] Opening TrustGuard AI in Google Chrome...
start chrome "http://%LAN_IP%:8000/" 2>nul
if %ERRORLEVEL% neq 0 (
    start "" "http://%LAN_IP%:8000/"
)

echo.
echo =================================================================
echo  TrustGuard AI Server is RUNNING.
echo.
echo  Localhost:
echo  http://127.0.0.1:8000/
echo  http://localhost:8000/
echo.
echo  LAN Access (Phone, Laptop, Tablet on same Wi-Fi):
echo  http://%LAN_IP%:8000/
echo.
echo  API Status Endpoint:
echo  http://%LAN_IP%:8000/api/status
echo =================================================================
echo.
echo Press any key to exit this launcher window (server will remain running in background)...
pause >nul
