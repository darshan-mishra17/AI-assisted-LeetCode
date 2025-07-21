# PowerShell script to start CodeForge Backend
Write-Host "Starting CodeForge Backend Server..." -ForegroundColor Green

Set-Location "C:\Users\HP\OneDrive\Desktop\CodeForge\Backend"

Write-Host "Starting server on http://127.0.0.1:8000" -ForegroundColor Yellow
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
