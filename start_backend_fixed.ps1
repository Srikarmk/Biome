# Biome Backend - Fixed for Docker PostgreSQL on port 5433
Write-Host "Starting Biome Backend..." -ForegroundColor Cyan

# Set environment variables
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/biome_coaching"
if (-not $env:GOOGLE_API_KEY) {
    Write-Host "Warning: GOOGLE_API_KEY not set!" -ForegroundColor Yellow
    $env:GOOGLE_API_KEY = "your-key-here"
}

Write-Host "Database: $env:DATABASE_URL" -ForegroundColor Green
Write-Host "Starting on port 8080..." -ForegroundColor Green
Write-Host ""

python api_server.py

