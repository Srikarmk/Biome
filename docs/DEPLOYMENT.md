# Cloud Run Deployment Guide

## Overview

This guide walks through deploying Biome Coaching Agent to Google Cloud Run for the hackathon submission.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and configured
3. **Docker** installed (for local testing)
4. **$100 Google Cloud credit** (from hackathon)
5. **Working local development** (backend + frontend tested)

## Strategy: Two-Service Deployment (+0.4 Bonus Points!)

Deploy as **two separate Cloud Run services** to maximize hackathon score:

1. **biome-backend** - FastAPI + ADK + MediaPipe (this repo)
2. **biome-frontend** - React UI (split from this repo)

**Benefit**: +0.4 bonus points for "Multiple Cloud Run Services"

---

## Phase 1: Prepare Google Cloud Project

### 1.1 Create/Select Project

```bash
# Create new project
gcloud projects create biome-coaching-prod --name="Biome Coaching"

# Or select existing
gcloud config set project YOUR_PROJECT_ID

# Verify
gcloud config get-value project
```

### 1.2 Enable Required APIs

```bash
# Enable Cloud Run
gcloud services enable run.googleapis.com

# Enable Cloud Build (for container builds)
gcloud services enable cloudbuild.googleapis.com

# Enable Artifact Registry
gcloud services enable artifactregistry.googleapis.com

# Enable Cloud SQL (for database)
gcloud services enable sqladmin.googleapis.com

# Enable Cloud Storage (for videos)
gcloud services enable storage.googleapis.com
```

### 1.3 Set Environment Variables

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export SERVICE_NAME_BACKEND=biome-backend
export SERVICE_NAME_FRONTEND=biome-frontend
```

---

## Phase 2: Set Up Cloud SQL (Database)

### 2.1 Create PostgreSQL Instance

```bash
# Create Cloud SQL instance (this takes 5-10 minutes)
gcloud sql instances create biome-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION \
  --root-password=YOUR_SECURE_PASSWORD \
  --storage-type=SSD \
  --storage-size=10GB

# Wait for instance to be ready
gcloud sql instances list
```

### 2.2 Create Database

```bash
# Create database
gcloud sql databases create biome_coaching \
  --instance=biome-db

# Get connection name
gcloud sql instances describe biome-db --format="value(connectionName)"
# Output example: PROJECT_ID:REGION:biome-db
```

### 2.3 Apply Schema

```bash
# Connect via Cloud SQL Proxy (local machine)
cloud_sql_proxy -instances=PROJECT_ID:REGION:biome-db=tcp:5432 &

# In another terminal, run schema
psql "postgresql://postgres:YOUR_PASSWORD@127.0.0.1:5432/biome_coaching" \
  -f schema.sql

# Verify tables created
psql "postgresql://postgres:YOUR_PASSWORD@127.0.0.1:5432/biome_coaching" \
  -c "\dt"
```

---

## Phase 3: Deploy Backend (FastAPI + ADK)

### 3.1 Test Docker Build Locally

```bash
# Build image
docker build -t biome-backend:test .

# Test locally
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY=your-key \
  -e DATABASE_URL=postgresql://... \
  biome-backend:test

# Test endpoint
curl http://localhost:8080/health
```

### 3.2 Deploy to Cloud Run

```bash
# Deploy (Cloud Build will build from source)
gcloud run deploy $SERVICE_NAME_BACKEND \
  --source . \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --memory=4Gi \
  --cpu=2 \
  --timeout=300s \
  --max-instances=10 \
  --set-env-vars="GOOGLE_API_KEY=your-gemini-key" \
  --set-env-vars="DATABASE_URL=postgresql://postgres:PASSWORD@/biome_coaching?host=/cloudsql/PROJECT_ID:REGION:biome-db" \
  --add-cloudsql-instances=PROJECT_ID:REGION:biome-db \
  --set-env-vars="DEBUG=false" \
  --set-env-vars="PORT=8080"
```

**Important**: Replace placeholders:
- `your-gemini-key` with actual Gemini API key
- `PASSWORD` with Cloud SQL password
- `PROJECT_ID` with your project ID
- `REGION` with your region (e.g., us-central1)

### 3.3 Get Backend URL

```bash
# Get service URL
gcloud run services describe $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --format="value(status.url)"

# Example output: https://biome-backend-xxxxx.run.app

# Save to variable
export BACKEND_URL=$(gcloud run services describe $SERVICE_NAME_BACKEND --region=$REGION --format="value(status.url)")

# Test endpoint
curl $BACKEND_URL/health
```

---

## Phase 4: Deploy Frontend (React) - Separate Service

### 4.1 Prepare Frontend for Deployment

```bash
# Update frontend to use backend URL
# Edit Dockerfile.frontend or add env var during build

# Build with backend URL
docker build -f Dockerfile.frontend \
  --build-arg REACT_APP_API_URL=$BACKEND_URL \
  -t biome-frontend:test .

# Test locally
docker run -p 8080:8080 biome-frontend:test
```

### 4.2 Deploy Frontend to Cloud Run

```bash
# Deploy frontend as separate service
gcloud run deploy $SERVICE_NAME_FRONTEND \
  --source . \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --memory=512Mi \
  --cpu=1 \
  --timeout=60s \
  --set-env-vars="REACT_APP_API_URL=$BACKEND_URL"
```

### 4.3 Get Frontend URL

```bash
# Get frontend URL
FRONTEND_URL=$(gcloud run services describe $SERVICE_NAME_FRONTEND --region=$REGION --format="value(status.url)")

echo "Frontend: $FRONTEND_URL"
echo "Backend: $BACKEND_URL"
```

---

## Phase 5: Configure CORS and Test

### 5.1 Update Backend CORS

Update `api_server.py` to allow frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://biome-frontend-xxxxx.run.app",  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy backend:
```bash
gcloud run deploy $SERVICE_NAME_BACKEND --source . --region=$REGION
```

### 5.2 End-to-End Test

1. Visit frontend URL: `https://biome-frontend-xxxxx.run.app`
2. Upload test video (squat or push-up)
3. Verify analysis completes
4. Check results display correctly

---

## Phase 6: Monitoring and Debugging

### 6.1 View Logs

```bash
# Backend logs
gcloud run services logs read $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --limit=50

# Frontend logs
gcloud run services logs read $SERVICE_NAME_FRONTEND \
  --region=$REGION \
  --limit=50

# Follow logs in real-time
gcloud run services logs tail $SERVICE_NAME_BACKEND --region=$REGION
```

### 6.2 Check Resource Usage

```bash
# Get service details
gcloud run services describe $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --format=yaml

# Check instance count
gcloud run services describe $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --format="value(status.traffic[0].percent)"
```

### 6.3 Common Issues

**Issue**: Container times out during startup
```bash
# Solution: Increase timeout
gcloud run services update $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --timeout=300s
```

**Issue**: Out of memory error
```bash
# Solution: Increase memory
gcloud run services update $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --memory=8Gi
```

**Issue**: Database connection fails
```bash
# Verify Cloud SQL connection
gcloud sql instances describe biome-db

# Check if instance is running
gcloud sql instances list

# Restart if needed
gcloud sql instances restart biome-db
```

---

## Phase 7: Cost Optimization

### 7.1 Monitor Spending

```bash
# Check current spending
gcloud billing accounts list

# Set budget alerts (via Console)
# Go to: Billing > Budgets & Alerts
# Create alert at $50, $75, $90
```

### 7.2 Resource Limits

```bash
# Limit max instances (prevent runaway costs)
gcloud run services update $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --max-instances=10

# Set minimum instances to 0 (cost savings)
gcloud run services update $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --min-instances=0
```

### 7.3 Clean Up After Hackathon

```bash
# Delete Cloud Run services
gcloud run services delete $SERVICE_NAME_BACKEND --region=$REGION
gcloud run services delete $SERVICE_NAME_FRONTEND --region=$REGION

# Delete Cloud SQL instance
gcloud sql instances delete biome-db

# Delete container images
gcloud artifacts repositories delete default --location=$REGION
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Local development working (backend + frontend)
- [ ] Database schema tested locally
- [ ] Test videos uploaded successfully
- [ ] Analysis pipeline produces results
- [ ] Docker build succeeds locally

### Cloud Setup
- [ ] Google Cloud project created
- [ ] APIs enabled (Cloud Run, SQL, Storage, Build)
- [ ] gcloud CLI configured (`gcloud auth login`)
- [ ] $100 credit applied

### Database
- [ ] Cloud SQL instance created
- [ ] Database `biome_coaching` created
- [ ] Schema applied successfully
- [ ] Connection string configured

### Backend Deployment
- [ ] Dockerfile.backend builds without errors
- [ ] Environment variables configured
- [ ] Cloud SQL connection set up
- [ ] Service deployed successfully
- [ ] Health endpoint returns 200
- [ ] Backend URL obtained and saved

### Frontend Deployment
- [ ] Dockerfile.frontend builds correctly
- [ ] REACT_APP_API_URL points to backend
- [ ] Service deployed successfully
- [ ] Frontend loads in browser
- [ ] API calls reach backend

### Testing
- [ ] Upload test video through UI
- [ ] Processing completes without errors
- [ ] Results display correctly
- [ ] No CORS errors in console
- [ ] Database stores results

### Hackathon Submission
- [ ] Both service URLs documented
- [ ] Architecture diagram created
- [ ] Demo video recorded (< 3 minutes)
- [ ] Public GitHub repository
- [ ] README updated with deployment URLs

---

## Troubleshooting

### MediaPipe Installation Issues

If deployment fails due to MediaPipe size:

```dockerfile
# Optimize Dockerfile
FROM python:3.11-slim

# Install only required system libraries
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Use --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt
```

### Video Upload Fails

Check upload size limits:

```bash
# Cloud Run has 32MB request limit for synchronous
# For large videos, use Cloud Storage signed URLs

# Update backend to generate signed URLs
# Frontend uploads directly to GCS
# Backend polls GCS for completion
```

### Cold Start Latency

Enable minimum instances for faster response:

```bash
# Keep 1 instance warm (costs more but faster)
gcloud run services update $SERVICE_NAME_BACKEND \
  --region=$REGION \
  --min-instances=1
```

---

## Bonus Points Checklist

✅ **Using Google AI Model** (+0.4)
- Implemented: Gemini 2.0 Flash in agent.py

✅ **Multiple Cloud Run Services** (+0.4)
- Backend service: biome-backend
- Frontend service: biome-frontend

⚠️ **Blog Post** (+0.4)
- Write about: Building with ADK, Cloud Run deployment experience
- Publish on: Medium, dev.to, or personal blog
- Must mention: "Created for Cloud Run Hackathon"

⚠️ **Social Media Post** (+0.4)
- Post on: LinkedIn or X (Twitter)
- Include: #CloudRunHackathon
- Share: Demo link, architecture diagram, key learnings

**Maximum Score**: 6.6 points (5.0 base + 1.6 bonus)

---

## Support Resources

- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Cloud SQL Docs**: https://cloud.google.com/sql/docs
- **ADK Documentation**: Check ADK folder in repo
- **Hackathon Forum**: Check Discord/Slack for help

---

**Good luck with your deployment!** 🚀

Remember: Test early, deploy often, monitor closely.

