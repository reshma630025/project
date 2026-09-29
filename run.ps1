# TrustGuard AI Runner Script for PowerShell
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting TrustGuard AI Deepfake Detection Server" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening Application at http://127.0.0.1:8000/ ..." -ForegroundColor Green
Start-Process "http://127.0.0.1:8000/"

Write-Host "Starting FastAPI Backend Server on port 8000..." -ForegroundColor Yellow
& python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
