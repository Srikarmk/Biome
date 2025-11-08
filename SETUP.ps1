# Quick Setup Script for Biome Coaching Agent
# Run this to set up Python 3.11 environment

Write-Host "`n=== Biome Coaching Agent Setup ===" -ForegroundColor Cyan

# Check for Python 3.11
Write-Host "`nChecking for Python 3.11..." -ForegroundColor Yellow
$py311 = py -3.11 --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Python 3.11 not found!" -ForegroundColor Red
    Write-Host "`n  CRITICAL: MediaPipe requires Python 3.11 (not 3.12, not 3.13)" -ForegroundColor Yellow
    Write-Host "`n  Install Python 3.11:" -ForegroundColor Cyan
    Write-Host "    winget install Python.Python.3.11" -ForegroundColor White
    Write-Host "`n  Or download from: https://www.python.org/downloads/release/python-3119/" -ForegroundColor White
    Write-Host ""
    exit 1
}
Write-Host "  [OK] Found: $py311" -ForegroundColor Green

# Remove old venv if exists
if (Test-Path ".venv") {
    Write-Host "`nRemoving old virtual environment..." -ForegroundColor Yellow
    Remove-Item .venv -Recurse -Force
}

# Create new venv with Python 3.11
Write-Host "`nCreating virtual environment with Python 3.11..." -ForegroundColor Yellow
py -3.11 -m venv .venv

# Activate and install
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "`nTo activate the environment, run:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "`nThen start the backend:" -ForegroundColor Cyan
Write-Host "  `$env:DATABASE_URL='postgresql://postgres:postgres@localhost:5433/biome_coaching'" -ForegroundColor White
Write-Host "  `$env:PORT=8000" -ForegroundColor White
Write-Host "  python api_server.py" -ForegroundColor White
Write-Host ""

