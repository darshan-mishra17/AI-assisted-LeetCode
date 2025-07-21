# PowerShell deploy script for Render

Write-Host "🚀 Preparing for Render deployment..." -ForegroundColor Green

# Add all changes
git add .

# Commit changes
git commit -m "Configure for Render deployment"

# Push to GitHub (make sure you have a remote set up)
git push origin main

Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
Write-Host "🌐 Now go to render.com and create a new Web Service" -ForegroundColor Yellow
Write-Host "📁 Root Directory: Backend" -ForegroundColor Cyan
Write-Host "🐍 Environment: Python 3" -ForegroundColor Cyan
Write-Host "🔨 Build Command: pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "▶️  Start Command: uvicorn app.main:app --host 0.0.0.0 --port `$PORT" -ForegroundColor Cyan
