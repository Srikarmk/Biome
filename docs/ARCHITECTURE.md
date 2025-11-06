# Biome Coaching Agent - Architecture

## System Overview

Biome is an AI-powered fitness form coaching application that analyzes workout videos and provides real-time, actionable feedback to improve technique and prevent injuries.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERACTION                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Upload Video
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   REACT FRONTEND (PORT 3000)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Landing Page  • Upload UI  • Results Display     │  │
│  │  • Real-time Progress  • Video Player with Markers  │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/REST API
                        │ (WebSocket optional)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│            FASTAPI BACKEND (PORT 8080/8000)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  /api/analyze  • POST video upload                   │  │
│  │  /api/results  • GET analysis results                │  │
│  │  /api/sessions • GET session status                  │  │
│  │  /health       • Health check                        │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Orchestrates
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               GOOGLE ADK AGENT (Root Agent)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Model: gemini-2.0-flash                             │  │
│  │  Reasoning: Form analysis & coaching feedback        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────── ADK TOOLS ──────────────────────────┐ │
│  │                                                        │ │
│  │  1. upload_video                                      │ │
│  │     └─> Validate & store video file                  │ │
│  │                                                        │ │
│  │  2. extract_pose_landmarks                            │ │
│  │     └─> MediaPipe Pose (33 landmarks per frame)      │ │
│  │     └─> Calculate joint angles (knee, hip, elbow)    │ │
│  │                                                        │ │
│  │  3. analyze_workout_form                              │ │
│  │     └─> Detect form issues with severity             │ │
│  │     └─> Generate coaching cues (actionable)          │ │
│  │     └─> Calculate overall score (0-10)               │ │
│  │                                                        │ │
│  │  4. save_analysis_results                             │ │
│  │     └─> Persist to PostgreSQL                        │ │
│  │     └─> Store issues, metrics, recommendations       │ │
│  │                                                        │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
┌─────────────────────┐  ┌──────────────────────┐
│  MEDIAPIPE POSE     │  │  GOOGLE GEMINI 2.0   │
│  (Computer Vision)  │  │  (AI Reasoning)      │
│                     │  │                      │
│  • Pose Detection   │  │  • Form Analysis     │
│  • Landmark Extract │  │  • Cue Generation    │
│  • Angle Calc       │  │  • Severity Scoring  │
└─────────────────────┘  └──────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                  POSTGRESQL DATABASE                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tables:                                             │  │
│  │  • analysis_sessions  (video metadata, status)       │  │
│  │  • analysis_results   (overall score, timing)        │  │
│  │  • form_issues        (type, severity, frames, cue)  │  │
│  │  • metrics            (actual vs target values)      │  │
│  │  • strengths          (positive feedback)            │  │
│  │  • recommendations    (next steps)                   │  │
│  │  • user_progress      (tracking over time)           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. React Frontend
- **Technology**: React 18 + TypeScript + Tailwind CSS
- **Key Features**:
  - Video upload with webcam recording support
  - Real-time progress tracking during analysis
  - Interactive video player with issue markers
  - Results visualization with severity color coding
- **Deployment**: Cloud Run (separate service for +0.4 bonus points)

### 2. FastAPI Backend
- **Technology**: FastAPI + Python 3.11+
- **Responsibilities**:
  - HTTP REST API endpoints
  - Video file handling (multipart/form-data)
  - ADK agent orchestration
  - CORS configuration for frontend
- **Deployment**: Cloud Run (primary service)

### 3. Google ADK Agent
- **Model**: Gemini 2.0 Flash (fast, cost-effective)
- **Pattern**: Single agent + 4 tools (not microservices)
- **Workflow**:
  1. Accept video upload request
  2. Call `upload_video` tool → create session
  3. Call `extract_pose_landmarks` tool → get body data
  4. Call `analyze_workout_form` tool → generate feedback
  5. Call `save_analysis_results` tool → persist to DB
  6. Return complete analysis to frontend

### 4. MediaPipe Pose
- **Purpose**: Computer vision for human pose estimation
- **Output**: 33 body landmarks per frame (x, y, z coordinates)
- **Processing**: 10 FPS (optimized for speed)
- **Calculations**: Joint angles (knee, hip, elbow, spine)

### 5. PostgreSQL Database
- **Schema**: 9 tables (see schema.sql)
- **Key Design**:
  - `analysis_sessions` = one per video upload
  - `analysis_results` = overall score + metadata
  - `form_issues` = specific problems detected
  - `metrics` = quantified measurements
  - Cascading deletes for data integrity

## Data Flow

### Upload → Analysis → Results

```
1. User uploads video (MP4/MOV/AVI/WebM)
   ↓
2. Frontend sends POST /api/analyze
   ↓
3. Backend saves file, creates session UUID
   ↓
4. ADK Agent calls upload_video tool
   ↓
5. ADK Agent calls extract_pose_landmarks
   - MediaPipe processes video at 10 FPS
   - Extracts 33 landmarks per frame
   - Calculates joint angles
   ↓
6. ADK Agent calls analyze_workout_form
   - Gemini reasons about pose data
   - Identifies form issues (knee valgus, depth, etc.)
   - Generates specific coaching cues
   - Calculates overall score (0-10)
   ↓
7. ADK Agent calls save_analysis_results
   - Inserts into 5 database tables
   - Marks session as "completed"
   ↓
8. Backend returns complete JSON response
   ↓
9. Frontend displays results with video timeline
```

## Technology Stack

### Backend
- **Framework**: FastAPI (async, auto-docs)
- **Agent**: Google ADK (Agent Development Kit)
- **AI Model**: Gemini 2.0 Flash
- **Computer Vision**: MediaPipe Pose
- **Database**: PostgreSQL 15+
- **ORM**: Raw SQL (psycopg3) - simple, fast

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: Tailwind CSS
- **Routing**: React Router v7
- **Video**: react-webcam + HTML5 video

### Deployment
- **Platform**: Google Cloud Run
- **Container**: Docker (multi-stage build)
- **Database**: Cloud SQL (PostgreSQL)
- **Storage**: Local (uploads/) → GCS (production)
- **CI/CD**: Cloud Build

## Scalability Considerations

### Current (Hackathon MVP)
- Single Cloud Run service
- Local file storage
- Synchronous processing
- 10 concurrent users

### Production Ready (Post-Hackathon)
- **Horizontal Scaling**: Cloud Run auto-scales
- **Async Processing**: Task queue for video analysis
- **Storage**: Google Cloud Storage for videos
- **Caching**: Redis for session status
- **CDN**: Cloud CDN for frontend assets
- **Database**: Cloud SQL with read replicas

## Security

### Current Implementation
- CORS configured for localhost + production domains
- File size validation (max 100MB)
- Video format validation (MP4/MOV/AVI/WebM)
- Database connection pooling
- Environment variable protection

### Production Enhancements
- JWT authentication on all endpoints
- Rate limiting (5 uploads per hour per user)
- Video malware scanning
- SQL injection protection (parameterized queries)
- HTTPS only (Cloud Run default)

## Performance Metrics

### Expected Performance (Hackathon)
- **Upload**: < 5 seconds (100MB video)
- **Pose Extraction**: ~1s per 10 frames (MediaPipe)
- **AI Analysis**: 2-5 seconds (Gemini Flash)
- **Database Save**: < 500ms
- **Total End-to-End**: 15-30 seconds for 1-minute video

### Optimizations
- FPS reduced to 10 (from 30) for speed
- MediaPipe model complexity = 1 (lighter model)
- Gemini Flash (faster than Pro)
- Batch database inserts
- Connection pooling

## Cloud Run Compliance

### Requirements Met
✅ Deployed to Cloud Run (HTTP service)  
✅ Uses Google ADK for agent logic  
✅ Uses Google AI model (Gemini 2.0 Flash)  
✅ Public GitHub repository  
✅ Architecture diagram (this document)  
✅ Demo video (< 3 minutes)  
✅ Comprehensive documentation  

### Bonus Points Earned
✅ +0.4 - Uses Gemini model  
⚠️ +0.4 - Multiple Cloud Run services (if frontend deployed separately)  
⚠️ +0.4 - Blog post (optional)  
⚠️ +0.4 - Social media post (optional)  

**Maximum Score**: 6.6/6.6 points possible

## Future Enhancements

### Phase 2 (Post-Hackathon)
1. **More Exercises**: Push-ups, deadlifts, planks
2. **Real-time Mode**: Live webcam analysis
3. **Mobile App**: React Native + on-device inference
4. **Social Features**: Share results, compare with friends
5. **Progress Tracking**: Longitudinal improvement charts
6. **Coach Dashboard**: Bulk user management

### Phase 3 (Production)
1. **Wearable Integration**: Smartwatch sensors
2. **3D Visualization**: Three.js pose rendering
3. **Multi-angle**: Sync multiple camera angles
4. **Offline Mode**: TensorFlow Lite on-device
5. **Team Features**: Group challenges, leaderboards

## Development Setup

See main README.md for detailed setup instructions.

Quick start:
```bash
# Backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python api_server.py

# Frontend
npm install
npm start
```

## Deployment

See DEPLOYMENT.md for Cloud Run deployment guide.

---

**Built for Google Cloud Run Hackathon 2025**  
**Category**: AI Agents  
**Tech Stack**: Google ADK + Gemini 2.0 + MediaPipe + FastAPI + React

