Write-Host "🔥 FINAL CORS AND AI FIX TEST 🔥" -ForegroundColor Red
Write-Host "================================" -ForegroundColor Yellow

Write-Host "`n1. Testing backend health..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "https://ai-assisted-leetcode.onrender.com/health"
    Write-Host "✅ Backend is UP: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend is DOWN!" -ForegroundColor Red
}

Write-Host "`n2. Testing CORS preflight..." -ForegroundColor Cyan
try {
    $options = Invoke-RestMethod -Uri "https://ai-assisted-leetcode.onrender.com/ai/hint" -Method OPTIONS -Headers @{
        "Origin" = "https://ai-assisted-leet-code.vercel.app"
        "Access-Control-Request-Method" = "POST"
    }
    Write-Host "✅ CORS preflight works" -ForegroundColor Green
} catch {
    Write-Host "❌ CORS OPTIONS failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n3. Testing AI endpoint..." -ForegroundColor Cyan
try {
    $body = @{
        problem_id = "1"
        user_code = "// test code"
        language = "python"
        hint_type = "hint"
    } | ConvertTo-Json

    $ai_response = Invoke-RestMethod -Uri "https://ai-assisted-leetcode.onrender.com/ai/hint" -Method POST -Headers @{
        "Content-Type" = "application/json"
        "Origin" = "https://ai-assisted-leet-code.vercel.app"
    } -Body $body

    Write-Host "✅ AI endpoint works! Response:" -ForegroundColor Green
    Write-Host $ai_response.hint -ForegroundColor White
} catch {
    Write-Host "❌ AI endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🚀 SUMMARY:" -ForegroundColor Yellow
Write-Host "If you saw ✅ for all 3 tests, everything is working!" -ForegroundColor Green
Write-Host "If you saw ❌ errors, you need to push the backend changes first." -ForegroundColor Red
