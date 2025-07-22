# AI Mentor Setup Script - Initialize Advanced AI capabilities for Windows

Write-Host "🤖 Setting up Advanced AI Mentor for CodeForge..." -ForegroundColor Green

# Navigate to backend directory
Set-Location -Path "Backend"

Write-Host "📦 Installing Python AI dependencies..." -ForegroundColor Yellow

# Install the advanced AI mentor dependencies
$dependencies = @(
    "langchain>=0.1.0",
    "langchain-community>=0.0.10", 
    "langchain-groq>=0.0.1",
    "chromadb>=0.4.0",
    "sentence-transformers>=2.2.0",
    "openai>=1.3.0",
    "tiktoken>=0.5.0",
    "numpy>=1.24.0",
    "pandas>=2.0.0"
)

foreach ($dep in $dependencies) {
    Write-Host "Installing $dep..." -ForegroundColor Cyan
    pip install $dep
}

Write-Host "✅ Python dependencies installed successfully!" -ForegroundColor Green

Write-Host "🔧 Setting up vector database..." -ForegroundColor Yellow

# Create chroma database directory
if (!(Test-Path -Path "chroma_db")) {
    New-Item -ItemType Directory -Path "chroma_db" | Out-Null
    New-Item -ItemType File -Path "chroma_db/.gitkeep" | Out-Null
}

Write-Host "✅ Vector database directory created!" -ForegroundColor Green

Write-Host "📄 Setting up environment variables..." -ForegroundColor Yellow

# Check if .env file exists, if not create it
if (!(Test-Path -Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Cyan
    if (Test-Path -Path ".env.example") {
        Copy-Item ".env.example" ".env"
    } else {
        "# CodeForge Backend Environment Variables" | Out-File -FilePath ".env" -Encoding UTF8
    }
}

# Add AI mentor variables if they don't exist
$envContent = Get-Content ".env" -ErrorAction SilentlyContinue
if ($envContent -notmatch "GROQ_API_KEY") {
    $aiConfig = @"

# AI Mentor Configuration
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
CHROMADB_PATH=./chroma_db
AI_MENTOR_MODEL=mixtral-8x7b-32768
AI_MENTOR_TEMPERATURE=0.1
ENABLE_ADVANCED_AI=true
"@
    Add-Content -Path ".env" -Value $aiConfig
}

Write-Host "✅ Environment variables configured!" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 AI Mentor setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Get your Groq API key from: https://console.groq.com/" -ForegroundColor White
Write-Host "2. Update the GROQ_API_KEY in your .env file" -ForegroundColor White  
Write-Host "3. Restart your backend server" -ForegroundColor White
Write-Host "4. Test the AI mentor in the problem detail pages" -ForegroundColor White
Write-Host ""
Write-Host "🚀 The AI Mentor now supports:" -ForegroundColor Cyan
Write-Host "   • Personalized hints with context awareness" -ForegroundColor White
Write-Host "   • Comprehensive code quality analysis" -ForegroundColor White
Write-Host "   • Interactive concept explanations" -ForegroundColor White
Write-Host "   • Advanced debugging assistance" -ForegroundColor White
Write-Host "   • Personalized learning paths" -ForegroundColor White
Write-Host "   • Vector-based knowledge storage" -ForegroundColor White
Write-Host "   • Conversation history tracking" -ForegroundColor White
Write-Host ""
Write-Host "💡 Pro tip: The AI mentor gets smarter as you use it more!" -ForegroundColor Magenta

# Return to original directory
Set-Location -Path ".."
