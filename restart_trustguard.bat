@echo off
title TrustGuard AI — Restart Local Server

cd /d "%~dp0"

echo Restarting TrustGuard AI Server...
call stop_trustguard.bat
timeout /t 2 /nobreak >nul
call start_trustguard.bat
