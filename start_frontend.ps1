# Biome Coaching Agent - Frontend Startup Script
# This script starts the React development server
#
# NOTE: To split into separate repos for +0.4 bonus points, copy these files to new repo:
#   - src/, public/, package.json, tailwind.config.js, tsconfig.json, Dockerfile.frontend, .dockerignore.frontend, LICENSE

Write-Host "🎨 Starting Biome Coaching Agent Frontend..." -ForegroundColor Cyan
Write-Host ""

# Check if node_modules exists
if (!(Test-Path "node_modules")) {
    Write-Host "❌ Node modules not found!" -ForegroundColor Red
    Write-Host "Please run setup first:" -ForegroundColor Yellow
    Write-Host "  npm install" -ForegroundColor Yellow
    exit 1
}

# Set PORT to avoid conflicts
if (-not $env:PORT) {
    $env:PORT = 3000
}

Write-Host "📦 Starting React development server..." -ForegroundColor Green
Write-Host "Frontend will be available at: http://localhost:$env:PORT" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

npm start

