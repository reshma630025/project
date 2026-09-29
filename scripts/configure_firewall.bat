@echo off
title TrustGuard AI — Configure Windows Firewall (Port 8000)

echo =================================================================
echo        TRUSTGUARD AI -- WINDOWS FIREWALL CONFIGURATION
echo =================================================================
echo.
echo Adding inbound firewall rule for TCP Port 8000 on Private/Domain networks...
echo (Allows other devices on your local Wi-Fi to connect to TrustGuard AI)
echo.

netsh advfirewall firewall add rule name="TrustGuard AI Server (Port 8000)" dir=in action=allow protocol=TCP localport=8000 profile=private,domain >nul 2>&1

if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Windows Firewall rule "TrustGuard AI Server (Port 8000)" added successfully.
) else (
    echo [NOTICE] Adding firewall rules requires Administrator privileges.
    echo If LAN devices cannot connect, right-click this script and select "Run as administrator".
)

echo.
echo Verifying rule...
netsh advfirewall firewall show rule name="TrustGuard AI Server (Port 8000)"

echo.
pause
