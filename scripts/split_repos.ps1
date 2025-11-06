# Monorepo → Separate Repos Split Script
# Run this when ready to deploy for +0.4 bonus points
# Estimated time: 15 minutes

Write-Host "🔀 Splitting monorepo into backend + frontend repos..." -ForegroundColor Cyan
Write-Host ""

# Create backend repo
Write-Host "📦 Creating backend repository..." -ForegroundColor Yellow
$backendPath = "..\biome-backend"
New-Item -ItemType Directory -Path $backendPath -Force | Out-Null
Set-Location $backendPath
git init

# Copy backend files
Copy-Item -Path ..\biome_agent\api_server.py -Destination .
Copy-Item -Path ..\biome_agent\biome_coaching_agent -Destination . -Recurse
Copy-Item -Path ..\biome_agent\db -Destination . -Recurse
Copy-Item -Path ..\biome_agent\requirements.txt -Destination .
Copy-Item -Path ..\biome_agent\schema.sql -Destination .
Copy-Item -Path ..\biome_agent\Dockerfile.backend -Destination Dockerfile
Copy-Item -Path ..\biome_agent\.dockerignore.backend -Destination .dockerignore
Copy-Item -Path ..\biome_agent\LICENSE -Destination .

# Create backend README (minimal)
echo "# Biome Backend
FastAPI + ADK + MediaPipe

Setup: pip install -r requirements.txt
Run: python api_server.py
Deploy: gcloud run deploy --source ." > README.md

git add .
git commit -m "Initial backend setup for Cloud Run"
Write-Host "✅ Backend repo created at: $backendPath" -ForegroundColor Green

# Create frontend repo  
Set-Location ..
Write-Host "`n📦 Creating frontend repository..." -ForegroundColor Yellow
$frontendPath = "..\biome-frontend"
New-Item -ItemType Directory -Path $frontendPath -Force | Out-Null
Set-Location $frontendPath
git init

# Copy frontend files
Copy-Item -Path ..\biome_agent\src -Destination . -Recurse
Copy-Item -Path ..\biome_agent\public -Destination . -Recurse
Copy-Item -Path ..\biome_agent\package.json -Destination .
Copy-Item -Path ..\biome_agent\package-lock.json -Destination .
Copy-Item -Path ..\biome_agent\tailwind.config.js -Destination .
Copy-Item -Path ..\biome_agent\tsconfig.json -Destination .
Copy-Item -Path ..\biome_agent\postcss.config.js -Destination .
Copy-Item -Path ..\biome_agent\Dockerfile.frontend -Destination Dockerfile
Copy-Item -Path ..\biome_agent\.dockerignore.frontend -Destination .dockerignore
Copy-Item -Path ..\biome_agent\LICENSE -Destination .

# Create frontend README (minimal)
echo "# Biome Frontend
React + TypeScript + Tailwind

Setup: npm install
Run: npm start
Deploy: gcloud run deploy --source ." > README.md

# Create .env.production for Cloud Run backend URL
echo "REACT_APP_API_URL=https://biome-backend-XXXXX.run.app" > .env.production.example

git add .
git commit -m "Initial frontend setup for Cloud Run"
Write-Host "✅ Frontend repo created at: $frontendPath" -ForegroundColor Green

# Done
Set-Location ..\biome_agent
Write-Host "`n🎉 Split complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Push both repos to GitHub (make public)" -ForegroundColor White
Write-Host "  2. Deploy backend: cd ..\biome-backend && gcloud run deploy biome-backend --source ." -ForegroundColor White
Write-Host "  3. Deploy frontend: cd ..\biome-frontend && gcloud run deploy biome-frontend --source ." -ForegroundColor White
Write-Host "  4. Update frontend .env.production with backend URL" -ForegroundColor White
Write-Host "  5. Redeploy frontend with correct backend URL" -ForegroundColor White
Write-Host "`n✨ This gives you +0.4 bonus points for multiple Cloud Run services!" -ForegroundColor Magenta
Write-Host ""

