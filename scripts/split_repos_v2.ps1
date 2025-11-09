# Monorepo → Separate Repos Split Script (UPDATED)
# Run this when ready to deploy for +0.4 bonus points
# Estimated time: 15 minutes

Write-Host "🔀 Splitting monorepo into backend + frontend repos..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path ".\biome_coaching_agent")) {
    Write-Host "❌ Error: Must run from biome_agent root directory" -ForegroundColor Red
    exit 1
}

# Create backend repo
Write-Host "📦 Creating backend repository..." -ForegroundColor Yellow
$backendPath = "..\biome-backend"

# Clean up old backend if exists
if (Test-Path $backendPath) {
    Write-Host "⚠️  Removing existing backend directory..." -ForegroundColor Yellow
    Remove-Item -Path $backendPath -Recurse -Force
}

New-Item -ItemType Directory -Path $backendPath -Force | Out-Null
Set-Location $backendPath
git init

# Copy backend files
Write-Host "  Copying backend files..." -ForegroundColor Cyan
Copy-Item -Path ..\biome_agent\api_server.py -Destination .
Copy-Item -Path ..\biome_agent\biome_coaching_agent -Destination . -Recurse
Copy-Item -Path ..\biome_agent\db -Destination . -Recurse
Copy-Item -Path ..\biome_agent\requirements.txt -Destination .
Copy-Item -Path ..\biome_agent\schema.sql -Destination .
Copy-Item -Path ..\biome_agent\env.example -Destination .  # ADDED: Environment template
Copy-Item -Path ..\biome_agent\docs -Destination . -Recurse  # ADDED: Architecture docs
Copy-Item -Path ..\biome_agent\Dockerfile.backend -Destination Dockerfile
Copy-Item -Path ..\biome_agent\.dockerignore.backend -Destination .dockerignore
Copy-Item -Path ..\biome_agent\LICENSE -Destination . -ErrorAction SilentlyContinue

# Create comprehensive backend README
@"
# Biome Backend - AI Fitness Form Coach

**Cloud Run Hackathon 2025 - AI Agents Category**

## Tech Stack
* Google ADK + Gemini 2.0 Flash (AI orchestration)
* FastAPI (API server)
* MediaPipe (pose extraction)
* PostgreSQL (database)

## Features
* Generic smart analysis for 100+ exercises
* Token optimization (1.2M → 5K tokens)
* Real-time form feedback with coaching cues
* Production-ready with comprehensive error handling

## Quick Start (Local)
``````bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp env.example .env
# Edit .env with your GEMINI_API_KEY and DATABASE_URL

# Run server
python api_server.py
``````

## Deploy to Cloud Run
``````bash
gcloud run deploy biome-backend \
  --source . \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300s \
  --allow-unauthenticated \
  --set-env-vars="GEMINI_API_KEY=your_key,PORT=8080"
``````

## Architecture
See `docs/ARCHITECTURE.md` for complete system architecture and data flow diagrams.

## Testing Results
* Bench Press: 9.3/10 with specific coaching
* Generic analysis working for any exercise
* 30-40 second average processing time
"@ | Out-File -FilePath README.md -Encoding utf8

# Create .gitignore for backend
@"
__pycache__/
*.pyc
*.pyo
.env
uploads/
.venv/
venv/
*.log
.DS_Store
"@ | Out-File -FilePath .gitignore -Encoding utf8

git add .
git commit -m "feat: Backend for Cloud Run - ADK + Gemini + MediaPipe

* Generic smart analysis for 100+ exercises
* Token optimization (1.2M → 5K tokens)
* Production-ready error handling
* Tested: Bench Press (9.3/10)

Ready for Cloud Run deployment."

Write-Host "✅ Backend repo created at: $backendPath" -ForegroundColor Green

# Create frontend repo  
Set-Location ..
Write-Host "`n📦 Creating frontend repository..." -ForegroundColor Yellow
$frontendPath = "..\biome-frontend"

# Clean up old frontend if exists
if (Test-Path $frontendPath) {
    Write-Host "⚠️  Removing existing frontend directory..." -ForegroundColor Yellow
    Remove-Item -Path $frontendPath -Recurse -Force
}

New-Item -ItemType Directory -Path $frontendPath -Force | Out-Null
Set-Location $frontendPath
git init

# Copy frontend files
Write-Host "  Copying frontend files..." -ForegroundColor Cyan
Copy-Item -Path ..\biome_agent\src -Destination . -Recurse
Copy-Item -Path ..\biome_agent\public -Destination . -Recurse
Copy-Item -Path ..\biome_agent\package.json -Destination .
Copy-Item -Path ..\biome_agent\package-lock.json -Destination .
Copy-Item -Path ..\biome_agent\tailwind.config.js -Destination .
Copy-Item -Path ..\biome_agent\tsconfig.json -Destination .
Copy-Item -Path ..\biome_agent\postcss.config.js -Destination .
Copy-Item -Path ..\biome_agent\Dockerfile.frontend -Destination Dockerfile
Copy-Item -Path ..\biome_agent\.dockerignore.frontend -Destination .dockerignore
Copy-Item -Path ..\biome_agent\LICENSE -Destination . -ErrorAction SilentlyContinue

# Create comprehensive frontend README
@"
# Biome Frontend - AI Fitness Form Coach

**Cloud Run Hackathon 2025 - AI Agents Category**

## Tech Stack
* React 19 + TypeScript
* Tailwind CSS
* React Router

## Features
* Modern, responsive UI
* Real-time analysis progress tracking
* Video playback with issue markers
* Comprehensive results display

## Quick Start (Local)
``````bash
# Install dependencies
npm install

# Set backend URL
echo "REACT_APP_API_URL=http://localhost:8080" > .env.development

# Run dev server
npm start
``````

## Deploy to Cloud Run
``````bash
# Set backend URL (update with your backend URL)
echo "REACT_APP_API_URL=https://biome-backend-xxxxx-uc.a.run.app" > .env.production

# Deploy
gcloud run deploy biome-frontend \
  --source . \
  --region us-central1 \
  --memory 512Mi \
  --allow-unauthenticated
``````

## Environment Variables
* ``REACT_APP_API_URL``: Backend API URL (required)

## UI Updates
After deployment, you can update the UI and redeploy:
``````bash
# Make changes
git commit -am "ui: Improve design"

# Redeploy (takes 5-10 minutes)
gcloud run deploy biome-frontend --source .
``````
"@ | Out-File -FilePath README.md -Encoding utf8

# Create .env templates
@"
# Backend API URL for local development
REACT_APP_API_URL=http://localhost:8080
"@ | Out-File -FilePath .env.development -Encoding utf8

@"
# Backend API URL for production (UPDATE THIS!)
REACT_APP_API_URL=https://biome-backend-XXXXX-uc.a.run.app
"@ | Out-File -FilePath .env.production.example -Encoding utf8

# Create .gitignore for frontend
@"
node_modules/
build/
.env.local
.env.production
.DS_Store
*.log
"@ | Out-File -FilePath .gitignore -Encoding utf8

git add .
git commit -m "feat: Frontend for Cloud Run - React + TypeScript

* Modern responsive UI
* Real-time progress tracking
* Video playback with markers
* Comprehensive results display

Ready for Cloud Run deployment."

Write-Host "✅ Frontend repo created at: $frontendPath" -ForegroundColor Green

# Done
Set-Location ..\biome_agent
Write-Host "`n🎉 Split complete!" -ForegroundColor Green
Write-Host "`n📋 Summary:" -ForegroundColor Yellow
Write-Host "  Backend:  $backendPath" -ForegroundColor White
Write-Host "  Frontend: $frontendPath" -ForegroundColor White
Write-Host "`n🚀 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Create GitHub repos: biome-backend, biome-frontend" -ForegroundColor White
Write-Host "  2. Push backend:" -ForegroundColor White
Write-Host "     cd $backendPath" -ForegroundColor Gray
Write-Host "     git remote add origin https://github.com/YOUR_USERNAME/biome-backend.git" -ForegroundColor Gray
Write-Host "     git branch -M main" -ForegroundColor Gray
Write-Host "     git push -u origin main" -ForegroundColor Gray
Write-Host "  3. Push frontend:" -ForegroundColor White
Write-Host "     cd $frontendPath" -ForegroundColor Gray
Write-Host "     git remote add origin https://github.com/YOUR_USERNAME/biome-frontend.git" -ForegroundColor Gray
Write-Host "     git branch -M main" -ForegroundColor Gray
Write-Host "     git push -u origin main" -ForegroundColor Gray
Write-Host "  4. Deploy backend to Cloud Run" -ForegroundColor White
Write-Host "  5. Update frontend .env.production with backend URL" -ForegroundColor White
Write-Host "  6. Deploy frontend to Cloud Run" -ForegroundColor White
Write-Host "`n✨ This gives you +0.4 bonus points for multiple Cloud Run services!" -ForegroundColor Magenta
Write-Host ""

