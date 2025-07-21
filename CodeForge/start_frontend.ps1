# PowerShell script to start CodeForge Frontend
Write-Host "Starting CodeForge Frontend Server..." -ForegroundColor Green

Set-Location "C:\Users\HP\OneDrive\Desktop\CodeForge\Frontend"

Write-Host "Installing dependencies..." -ForegroundColor Yellow
npm install

Write-Host "Starting React development server..." -ForegroundColor Yellow
npm run dev
