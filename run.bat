@echo off
cd /d "%~dp0"

echo ========================================
echo       TRUSTGUARD AI
echo ========================================
echo Starting backend server...
echo.

start "" /B python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

timeout /t 3 /nobreak >nul

start "" http://127.0.0.1:8000/

echo.
echo TrustGuard AI is running.
echo URL: http://127.0.0.1:8000/
echo.
pause  