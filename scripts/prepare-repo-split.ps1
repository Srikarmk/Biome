# Biome Repository Split Preparation Script
# Purpose: Prepare for splitting monorepo into backend + frontend for Cloud Run deployment
# Bonus: +0.4 points for multiple Cloud Run services
# 
# This script DOES NOT actually split the repo - it creates a checklist and
# documentation for manual splitting when ready to deploy.

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Biome Repo Split Preparation" -ForegroundColor Cyan
Write-Host "  +0.4 Bonus Points Strategy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path "api_server.py")) {
    Write-Host "❌ Error: Run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Running from correct directory" -ForegroundColor Green
Write-Host ""

# Create scripts directory if it doesn't exist
$scriptsDir = "scripts"
if (!(Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Path $scriptsDir | Out-Null
}

# Create preparation checklist
$checklistFile = "scripts/REPO_SPLIT_CHECKLIST.md"

$checklistContent = @"
# Repository Split Checklist for Cloud Run Deployment

## Goal: +0.4 Bonus Points!

Deploy two separate Cloud Run services:
1. **biome-backend** - FastAPI + ADK + MediaPipe
2. **biome-frontend** - React + Tailwind

## Why Split?

- ✅ **+0.4 hackathon bonus points** for multiple Cloud Run services
- ✅ **Independent scaling** - frontend and backend scale separately
- ✅ **Cleaner deployments** - smaller containers, faster deploys
- ✅ **Better organization** - clear separation of concerns

---

## Phase 1: Pre-Split Testing

Before splitting, ensure everything works in monorepo:

### Backend Tests
- [ ] Start backend: ``python api_server.py``
- [ ] Health check: ``curl http://localhost:8080/health``
- [ ] Upload test video through API
- [ ] Verify analysis completes
- [ ] Check database has results

### Frontend Tests
- [ ] Start frontend: ``npm start``
- [ ] Opens on http://localhost:3000
- [ ] Can upload video through UI
- [ ] Shows processing progress
- [ ] Displays results correctly

### Integration Tests
- [ ] Backend + Frontend work together
- [ ] CORS configured correctly
- [ ] Video upload → analysis → results flow works
- [ ] Database stores all data

---

## Phase 2: Create Backend Repository

### 2.1 Create New Repo

```bash
# On GitHub, create new repository: biome-backend
# Clone locally
git clone https://github.com/YOUR_USERNAME/biome-backend.git
cd biome-backend
```

### 2.2 Copy Backend Files

From monorepo, copy these files/directories:

**Core Backend:**
- [ ] ``api_server.py``
- [ ] ``requirements.txt``
- [ ] ``Dockerfile``
- [ ] ``.dockerignore``
- [ ] ``schema.sql``

**Agent Code:**
- [ ] ``biome_coaching_agent/`` (entire directory)
  - [ ] ``__init__.py``
  - [ ] ``agent.py``
  - [ ] ``config.py``
  - [ ] ``exceptions.py``
  - [ ] ``logging_config.py``
  - [ ] ``tools/`` (all tools)

**Database:**
- [ ] ``db/`` (entire directory)
  - [ ] ``__init__.py``
  - [ ] ``connection.py``
  - [ ] ``queries.py``

**Documentation:**
- [ ] ``README.md`` (create new, backend-specific)
- [ ] ``LICENSE``
- [ ] ``docs/DEPLOYMENT.md``
- [ ] ``docs/ARCHITECTURE.md``
- [ ] ``env.example``

**Scripts:**
- [ ] ``start_backend.ps1``
- [ ] ``start_backend_fixed.ps1``

### 2.3 Create Backend README.md

```markdown
# Biome Backend - AI Fitness Coach API

FastAPI + Google ADK + MediaPipe + Gemini 2.0

## Quick Start

\`\`\`bash
# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp env.example .env
# Edit .env with your GOOGLE_API_KEY

# Database
psql -U postgres -c "CREATE DATABASE biome_coaching;"
psql -U postgres -d biome_coaching -f schema.sql

# Run
python api_server.py
\`\`\`

## Endpoints

- ``POST /api/analyze`` - Upload video for analysis
- ``GET /api/results/{session_id}`` - Get analysis results
- ``GET /health`` - Health check

## Tech Stack

- FastAPI 0.104+
- Google ADK (Agent Development Kit)
- Gemini 2.0 Flash
- MediaPipe Pose
- PostgreSQL 15+

## Cloud Run Deployment

See ``docs/DEPLOYMENT.md`` for detailed instructions.

\`\`\`bash
gcloud run deploy biome-backend --source . --region us-central1
\`\`\`

## License

See LICENSE file.
```

### 2.4 Backend Git Setup

```bash
cd biome-backend
git add .
git commit -m "Initial backend setup for Cloud Run deployment"
git branch -M main
git push -u origin main
```

---

## Phase 3: Create Frontend Repository

### 3.1 Create New Repo

```bash
# On GitHub, create new repository: biome-frontend
# Clone locally
git clone https://github.com/YOUR_USERNAME/biome-frontend.git
cd biome-frontend
```

### 3.2 Copy Frontend Files

From monorepo, copy these files/directories:

**React App:**
- [ ] ``src/`` (entire directory)
  - [ ] ``App.tsx``
  - [ ] ``index.tsx``
  - [ ] ``index.css``
  - [ ] ``components/``
  - [ ] ``pages/``

**Public Assets:**
- [ ] ``public/`` (entire directory)
  - [ ] ``index.html``
  - [ ] ``favicon.ico``
  - [ ] ``logo192.png``
  - [ ] ``logo512.png``
  - [ ] ``manifest.json``
  - [ ] ``robots.txt``

**Configuration:**
- [ ] ``package.json``
- [ ] ``package-lock.json``
- [ ] ``tsconfig.json``
- [ ] ``tailwind.config.js``
- [ ] ``postcss.config.js``

**Deployment:**
- [ ] ``Dockerfile.frontend`` → rename to ``Dockerfile``
- [ ] ``.dockerignore.frontend`` → rename to ``.dockerignore``

**Documentation:**
- [ ] ``README.md`` (create new, frontend-specific)
- [ ] ``LICENSE``

### 3.3 Create Frontend README.md

```markdown
# Biome Frontend - AI Fitness Coach UI

React 18 + TypeScript + Tailwind CSS

## Quick Start

\`\`\`bash
# Install
npm install

# Configure backend URL
# Create .env.local
echo "REACT_APP_API_URL=http://localhost:8080" > .env.local

# Run
npm start
\`\`\`

Opens on http://localhost:3000

## Features

- 📹 Video upload with webcam recording
- ⏱️ Real-time analysis progress
- 📊 Interactive results with video timeline
- 🎯 Form issues with severity indicators
- 💪 Coaching cues and recommendations

## Tech Stack

- React 18 + TypeScript
- Tailwind CSS
- React Router v7
- react-webcam

## Cloud Run Deployment

\`\`\`bash
# Build
docker build -t biome-frontend .

# Deploy
gcloud run deploy biome-frontend \
  --image gcr.io/PROJECT_ID/biome-frontend \
  --region us-central1 \
  --set-env-vars REACT_APP_API_URL=https://biome-backend-xxx.run.app
\`\`\`

## Environment Variables

- ``REACT_APP_API_URL`` - Backend API URL

## License

See LICENSE file.
```

### 3.4 Frontend Git Setup

```bash
cd biome-frontend
git add .
git commit -m "Initial frontend setup for Cloud Run deployment"
git branch -M main
git push -u origin main
```

---

## Phase 4: Deploy to Cloud Run

### 4.1 Deploy Backend First

```bash
cd biome-backend

# Set project
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy biome-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300s \
  --set-env-vars GOOGLE_API_KEY=your-key \
  --set-env-vars DATABASE_URL=postgresql://...

# Get URL
gcloud run services describe biome-backend \
  --region us-central1 \
  --format="value(status.url)"
```

**Save backend URL**: ``https://biome-backend-xxxxx.run.app``

### 4.2 Deploy Frontend

```bash
cd biome-frontend

# Deploy with backend URL
gcloud run deploy biome-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --set-env-vars REACT_APP_API_URL=https://biome-backend-xxxxx.run.app

# Get URL
gcloud run services describe biome-frontend \
  --region us-central1 \
  --format="value(status.url)"
```

**Save frontend URL**: ``https://biome-frontend-xxxxx.run.app``

### 4.3 Update CORS in Backend

Update ``api_server.py`` with frontend URL:

```python
allow_origins=[
    "https://biome-frontend-xxxxx.run.app",
    "http://localhost:3000",  # Keep for dev
],
```

Redeploy backend:
```bash
gcloud run deploy biome-backend --source . --region us-central1
```

---

## Phase 5: Verification

### 5.1 Test Deployed Services

- [ ] Visit frontend URL in browser
- [ ] Upload test video
- [ ] Verify processing completes
- [ ] Check results display
- [ ] No CORS errors in console

### 5.2 Update Hackathon Submission

**Devpost Submission Fields:**

- [ ] **Hosted URL**: https://biome-frontend-xxxxx.run.app
- [ ] **GitHub URLs**: 
  - Backend: https://github.com/USER/biome-backend
  - Frontend: https://github.com/USER/biome-frontend
- [ ] **Tech Used**: Mention "Multiple Cloud Run Services"
- [ ] **Bonus Points**: Note both services in description

### 5.3 Architecture Diagram

Update to show two services:

```
Frontend (Cloud Run) → Backend (Cloud Run) → Database (Cloud SQL)
```

---

## Phase 6: Maintain Monorepo (Optional)

**Keep monorepo for development**:
- Easier local development
- Single git history
- Shared ADK context for Cursor AI

**Deploy from split repos**:
- Production deployments
- Clean separation for Cloud Run
- Bonus points for hackathon

**Workflow**:
1. Develop in monorepo
2. Test locally (both together)
3. When ready to deploy:
   - Copy changes to backend repo → deploy
   - Copy changes to frontend repo → deploy

---

## Troubleshooting

### Issue: CORS errors after deployment

**Solution**: Update backend CORS with actual frontend URL
- Edit ``api_server.py``
- Add frontend URL to ``allow_origins``
- Redeploy backend

### Issue: Frontend can't reach backend

**Solution**: Check ``REACT_APP_API_URL`` environment variable
- Must be set during build time, not runtime
- Rebuild frontend with correct URL
- Redeploy

### Issue: Build times too long

**Solution**: Optimize Dockerfiles
- Use multi-stage builds
- Cache layers effectively
- Minimize dependencies

---

## Bonus Points Tracking

✅ **Multiple Cloud Run Services** (+0.4)
- Backend deployed: biome-backend
- Frontend deployed: biome-frontend

✅ **Using Google AI Model** (+0.4)
- Gemini 2.0 Flash

⚠️ **Blog Post** (+0.4)
- Write about deployment experience
- Publish before Nov 10, 2025

⚠️ **Social Media** (+0.4)
- Post with #CloudRunHackathon
- Link to deployed app

**Maximum Score**: 6.6/6.6 points

---

## Final Checklist

- [ ] Both services deployed successfully
- [ ] Frontend + backend communicate correctly
- [ ] No errors in logs
- [ ] Database connected
- [ ] URLs documented
- [ ] GitHub repos public
- [ ] README files updated
- [ ] Architecture diagram shows both services
- [ ] Demo video mentions multiple services
- [ ] Devpost submission highlights separation

---

**You're ready for deployment!** 🚀

Split when ready, deploy both services, earn those bonus points!

"@

# Write checklist file
Set-Content -Path $checklistFile -Value $checklistContent

Write-Host "✓ Created: $checklistFile" -ForegroundColor Green
Write-Host ""

# Display summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Preparation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Read the checklist: scripts/REPO_SPLIT_CHECKLIST.md" -ForegroundColor White
Write-Host "2. Test everything locally first" -ForegroundColor White
Write-Host "3. When ready to deploy:" -ForegroundColor White
Write-Host "   - Create biome-backend repository" -ForegroundColor White
Write-Host "   - Create biome-frontend repository" -ForegroundColor White
Write-Host "   - Follow deployment steps" -ForegroundColor White
Write-Host ""
Write-Host "Benefits:" -ForegroundColor Yellow
Write-Host "  ✓ +0.4 bonus points (multiple Cloud Run services)" -ForegroundColor Green
Write-Host "  ✓ Independent scaling" -ForegroundColor Green
Write-Host "  ✓ Cleaner deployments" -ForegroundColor Green
Write-Host ""
Write-Host "Keep developing in this monorepo, deploy from split repos!" -ForegroundColor Cyan
Write-Host ""

