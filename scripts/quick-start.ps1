# Quick Start - Biome Backend with Database
# Single command to start everything

Write-Host "🚀 Biome Quick Start" -ForegroundColor Cyan
Write-Host ""

# Start database if not running
Write-Host "1️⃣  Checking database..." -ForegroundColor Yellow
$containerRunning = docker ps --filter "name=biome_agent-postgres-1" --filter "status=running" --format "{{.Names}}"
if (-not $containerRunning) {
    Write-Host "   Starting PostgreSQL..." -ForegroundColor Gray
    docker-compose -f docker-compose-db.yml up -d | Out-Null
    Start-Sleep -Seconds 5
}
Write-Host "   ✅ Database running" -ForegroundColor Green

# Set environment variables (OVERRIDE any .env file)
Write-Host ""
Write-Host "2️⃣  Configuring environment..." -ForegroundColor Yellow
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/biome_coaching"
$env:PORT = "8080"
$env:DEBUG = "true"
$env:RELOAD = "true"

Write-Host "   ✅ DATABASE_URL = postgresql://...@localhost:5433/biome_coaching" -ForegroundColor Green
Write-Host "   ✅ PORT = 8080" -ForegroundColor Green

if (-not $env:GOOGLE_API_KEY -or $env:GOOGLE_API_KEY -eq "") {
    Write-Host "   ⚠️  GOOGLE_API_KEY not set (will use placeholder)" -ForegroundColor Yellow
    $env:GOOGLE_API_KEY = "placeholder-key"
} else {
    Write-Host "   ✅ GOOGLE_API_KEY is set" -ForegroundColor Green
}

# Apply schema if needed
Write-Host ""
Write-Host "3️⃣  Checking database schema..." -ForegroundColor Yellow
$tableCheck = docker exec biome_agent-postgres-1 psql -U postgres -d biome_coaching -c "\dt" 2>&1
if ($tableCheck -match "analysis_sessions") {
    Write-Host "   ✅ Schema exists" -ForegroundColor Green
} else {
    Write-Host "   Creating schema..." -ForegroundColor Gray
    Get-Content schema.sql | docker exec -i biome_agent-postgres-1 psql -U postgres -d biome_coaching | Out-Null
    Write-Host "   ✅ Schema created" -ForegroundColor Green
}

# Start backend
Write-Host ""
Write-Host "4️⃣  Starting backend server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Backend: http://localhost:8080" -ForegroundColor White
Write-Host "  Health: http://localhost:8080/health" -ForegroundColor White
Write-Host "  Docs: http://localhost:8080/docs" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Use Python 3.11 (MediaPipe requires 3.11, not 3.13)
py -3.11 api_server.py

