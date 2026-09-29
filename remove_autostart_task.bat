@echo off
title TrustGuard AI — Remove Windows Auto-Start

cd /d "%~dp0"

echo Removing Windows Scheduled Task: TrustGuardAI-AutoStart...
schtasks /delete /tn "TrustGuardAI-AutoStart" /f >nul 2>&1

echo Removing Windows User Startup folder shortcut...
python -c "import os; p=os.path.join(os.environ.get('APPDATA',''), r'Microsoft\Windows\Start Menu\Programs\Startup\TrustGuardAI-AutoStart.vbs'); os.remove(p) if os.path.exists(p) else None"

echo Auto-start configuration removed.
pause
