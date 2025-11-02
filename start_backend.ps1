# Biome Coaching Agent - Backend Startup Script
# This script starts the custom FastAPI backend server
#
# NOTE: To split into separate repos for +0.4 bonus points, copy these files to new repo:
#   - api_server.py, biome_coaching_agent/, db/, requirements.txt, schema.sql, Dockerfile, .dockerignore, LICENSE

Write-Host "🚀 Starting Biome Coaching Agent Backend..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path ".venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

# Check for required environment variables
if (-not $env:GOOGLE_API_KEY) {
    Write-Host "⚠️  GOOGLE_API_KEY not set!" -ForegroundColor Yellow
    Write-Host "Setting placeholder - replace with your actual key:" -ForegroundColor Yellow
    $env:GOOGLE_API_KEY = "your-gemini-api-key-here"
}

if (-not $env:DATABASE_URL) {
    Write-Host "📊 Using default DATABASE_URL..." -ForegroundColor Gray
    $env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/biome_coaching"
}

Write-Host ""
Write-Host "Environment Configuration:" -ForegroundColor Cyan
Write-Host "  API Key: $($env:GOOGLE_API_KEY.Substring(0, [Math]::Min(20, $env:GOOGLE_API_KEY.Length)))..." -ForegroundColor Gray
Write-Host "  Database: $env:DATABASE_URL" -ForegroundColor Gray
Write-Host ""

# Start the backend server
# Set PORT for local development (Cloud Run uses 8080, but locally 8000 is easier)
if (-not $env:PORT) {
    $env:PORT = 8000
    Write-Host "🔧 Starting FastAPI server on http://localhost:8000..." -ForegroundColor Green
} else {
    Write-Host "🔧 Starting FastAPI server on http://localhost:$env:PORT..." -ForegroundColor Green
}
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python api_server.py

