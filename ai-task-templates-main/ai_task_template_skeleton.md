# AI Task Planning Template - Starter Framework

> **About This Template:** This is a systematic framework for planning and executing technical projects with AI assistance. Use this structure to break down complex features, improvements, or fixes into manageable, trackable tasks that AI agents can execute effectively.

---

## 1. Task Overview

### Task Title
<!-- Give your task a clear, specific name that describes what you're building or fixing -->
**Title:** Build Biome Coaching Agent - AI-Powered Workout Form Analysis System

### Goal Statement
<!-- Write one paragraph explaining what you want to achieve and why it matters for your project -->
**Goal:** Create an end-to-end AI coaching agent that analyzes workout videos and provides instant, evidence-based form feedback. The system will orchestrate video upload, pose extraction (MediaPipe), AI reasoning (Google ADK + Gemini), and real-time status updates via WebSockets. Users get actionable coaching cues with severity scores, frame-by-frame pinpointing, and injury risk flags—turning any short workout clip into a personalized coaching session.

---

## 2. Project Analysis & Current State

### Technology & Architecture
<!-- This is where you document your current tech stack so the AI understands your environment -->
- **Frameworks & Versions:**   - FastAPI 0.104+ (modern Python API framework - fast, async, auto-docs)
  - Google ADK (Python SDK for Gemini agents)
  - MediaPipe 0.10+ (pose estimation)
- **Language:** - Python 3.10+ (all backend services)
- **Database & ORM:** - PostgreSQL 15+ (relational database)
  - psycopg2 (raw SQL queries - simple and fast for hackathon)
- **UI & Styling:**   - React 18+ with TypeScript
  - Tailwind CSS + shadcn/ui components
- **Authentication:** None (open demo for hackathon)
- **Key Architectural Patterns:**
  - Single ADK Agent with Tool-based workflow
  - Tools: `upload_video`, `extract_pose_landmarks`, `analyze_workout_form`, `save_analysis_results`
  - Execution: ADK Runner orchestrates tool calls and reasoning
  - API Server: ADK FastAPI integration (`adk api_server`)
  - Real-time updates: ADK callbacks/WebSocket integration

### Current State
<!-- Describe what exists today - what's working, what's broken, what's missing -->
- ✅ Frontend UI exists (React + Tailwind)
- ✅ MediaPipe proof-of-concept works locally
- ❌ No backend API yet (need to build)
- ❌ No Google ADK agent implemented
- ❌ No database schema created
- ❌ No WebSocket infrastructure
My teammate built the front-end already, now the agent system need to be built.

## 3. Context & Problem Definition

### Problem Statement
<!-- This is where you clearly define the specific problem you're solving -->
User Pain Point: People who work out at home or in gyms lack immediate, expert feedback on their form. Poor form leads to:

Reduced workout effectiveness (not targeting intended muscles)
Increased injury risk (joint strain, muscle tears)
Plateaus in strength/fitness gains
Lack of confidence in self-directed training

Current Solutions Fall Short:

Personal trainers: Expensive ($50-150/session), scheduling friction
Mirror/Tempo devices: $1500+ hardware investment, limited exercise library
Generic YouTube tutorials: No personalized feedback, users can't self-diagnose issues

Why Now: Advances in pose estimation (MediaPipe) + reasoning AI (Gemini) make real-time, accurate form analysis feasible at consumer scale.

### Success Criteria
<!-- Define exactly how you'll know when this task is complete and successful -->
 User can upload 30-60s workout video and receive feedback within 15-30 seconds
 Agent identifies 3-5 common form issues per exercise with 80%+ accuracy
 Coaching cues are actionable (e.g., "Shift knees 2 inches back" vs "Bad form")
 WebSocket delivers progress updates every 2-3 seconds during analysis
 Frontend displays issues pinned to video timeline with frame-accurate scrubbing
 System handles 10 concurrent analyses without degradation
 Overall analysis score (0-100) correlates with expert trainer ratings (pilot test)

---

## 4. Development Mode Context

### Development Mode Context
<!-- This is where you tell the AI agent about your project's constraints and priorities -->
- **🚨 Project Stage:** NEW DEVELOPMENT - Hackathon MVP (Google ADK competition deadline)
- **Breaking Changes:** Fully acceptable - no legacy users or data to preserve
- **Data Handling:** Test data only; no production user data exists yet
- **User Base:** Demo users + judges; optimize for "wow factor" and technical demonstration
- **Priority:** SPEED > STABILITY (but maintain demo reliability)

Focus on happy path; graceful degradation for edge cases

---

## 5. Technical Requirements

### Functional Requirements
<!-- This is where the AI will understand exactly what the system should do - be specific about user actions and system behaviors -->

Video Upload & Session Management:

User can upload MP4/MOV/AVI/WebM video files up to 100MB, max 5 minutes duration
System validates file format, size, duration on upload
System creates unique sessionId and returns WebSocket URL immediately
User receives upload progress percentage (0-100%) during transfer

Pose Extraction (Vision Service):

MediaPipe extracts 33 body landmarks per frame at 10 FPS
System calculates key angles: knee flexion, hip hinge, spine alignment, elbow position
System outputs JSON with { frame, timestamp, landmarks[], metrics: { kneeAngle, hipAngle, ... } }
Vision service emits progress events every 10% completion

AI Agent Orchestration (Google ADK + Gemini):

Agent receives pose metrics JSON as input
Agent identifies exercise type automatically (squat, deadlift, push-up, etc.)
Agent generates structured feedback with:

Overall score (0-100) based on form quality across all frames
List of issues: { type, severity: 'severe'|'moderate'|'minor', frameRange: [start, end], cue, riskLevel }
Positive reinforcement for correct form segments


Agent emits agent_status events showing current reasoning step

Real-Time Status Updates (WebSocket):

When video processing starts, emit: { type: 'progress', progress: 5, currentStep: 'Uploading video', estimatedTimeRemaining: 25 }
During vision processing: { type: 'progress', progress: 40, currentStep: 'Analyzing movement', estimatedTimeRemaining: 12 }
During agent reasoning: { type: 'agent_status', visionAgent: 'complete', coachingAgent: 'running', tasks: ['Identifying knee valgus', 'Checking spine neutrality'] }
On completion: { type: 'analysis_complete', sessionId, resultId, overallScore, issueCount }
On error: { type: 'error', message, retryable: true|false }

Results Display (Frontend):

User sees overall score prominently (0-100 with color coding: red <60, yellow 60-80, green >80)
User sees list of issues sorted by severity, each showing:

Issue title (e.g., "Knee Valgus Detected")
Coaching cue (e.g., "Push knees outward to track over toes")
Severity badge and risk flag (injury risk: high/medium/low)
Frame range where issue occurs


User can click issue to jump video to that frame range
Video timeline shows colored bars indicating issue locations

### Non-Functional Requirements
<!-- This is where you define performance, security, and usability standards -->
- **Performance:** Total analysis time (upload → results): <30 seconds for 1-minute 720p video
WebSocket latency: <500ms from agent event to frontend render
Video player seeks to frame within 100ms of click
Support 10 concurrent analyses without queueing (scale horizontally later)
- **Security:** JWT authentication on all API endpoints
Video files stored with randomized UUIDs (not sequential IDs)
WebSocket connections require valid session token
Rate limit: 5 video uploads per user per hour
Sanitize all video metadata to prevent XSS
- **Usability:** Mobile-responsive UI (80% of users on mobile during workouts)
One-click "Record Video" button using device camera
Clear progress indicator always visible during analysis
"What does this mean?" tooltips for coaching jargon
- **Responsive Design:** Mobile (320-768px): Single column, stacked video + issues list
Tablet (768-1024px): Side-by-side video and scrollable issues
Desktop (>1024px): Video left (60%), issues right (40%) with sticky positioning
- **Theme Support:** Dark mode default (easier on eyes during gym lighting)
Light mode toggle in settings
Brand colors: Primary (electric blue #0066FF), Accent (neon green #00FF88)

### Technical Constraints
<!-- This is where you list limitations the AI agent must work within -->
Google ADK for agent orchestration (hackathon requirement)
Gemini 2.5 Pro or Flash (no OpenAI/Claude)
MediaPipe Pose (proven accuracy, free, runs locally)
WebSockets for real-time updates (not SSE or long polling)

---

## 6. Data & Database Changes

### Database Schema Changes

**Status:** Creating new database from scratch (no migrations needed for initial setup)

**Complete Schema (9 Tables):**
```sql
-- ============================================
-- CORE TABLES
-- ============================================

-- 1. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    profile_image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- 2. Exercises Table
CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'Upper Body', 'Lower Body', 'Core', 'Other'
    description TEXT,
    icon VARCHAR(10), -- Emoji icon
    is_popular BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Analysis Sessions Table (CORE - tracks each video upload)
CREATE TABLE analysis_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    exercise_id UUID REFERENCES exercises(id),
    exercise_name VARCHAR(100) NOT NULL, -- Store custom exercise names
    video_url TEXT NOT NULL,
    video_duration DECIMAL(10,2), -- in seconds
    file_size BIGINT, -- in bytes
    mime_type VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- 4. Analysis Results Table (CORE - stores AI analysis output)
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES analysis_sessions(id) ON DELETE CASCADE,
    overall_score DECIMAL(3,1) NOT NULL, -- 0.0 to 10.0
    total_frames INTEGER NOT NULL,
    processing_time DECIMAL(10,2), -- in seconds
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Form Issues Table (CORE - specific problems detected)
CREATE TABLE form_issues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID REFERENCES analysis_results(id) ON DELETE CASCADE,
    issue_type VARCHAR(100) NOT NULL, -- 'Knee Valgus', 'Back Rounding', etc.
    severity VARCHAR(20) NOT NULL, -- 'severe', 'moderate', 'minor'
    frame_start INTEGER NOT NULL,
    frame_end INTEGER NOT NULL,
    coaching_cue TEXT NOT NULL,
    confidence_score DECIMAL(3,2), -- 0.00 to 1.00
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Metrics Table (specific measurements)
CREATE TABLE metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID REFERENCES analysis_results(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL, -- 'Knee Angle', 'Hip Angle', etc.
    actual_value VARCHAR(50) NOT NULL,
    target_value VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'good', 'warning', 'error'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Strengths Table (positive feedback)
CREATE TABLE strengths (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID REFERENCES analysis_results(id) ON DELETE CASCADE,
    strength_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Recommendations Table (improvement suggestions)
CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID REFERENCES analysis_results(id) ON DELETE CASCADE,
    recommendation_text TEXT NOT NULL,
    priority INTEGER DEFAULT 1, -- 1 = highest priority
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. User Progress Table (tracking improvement over time)
CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    exercise_id UUID REFERENCES exercises(id),
    exercise_name VARCHAR(100) NOT NULL,
    average_score DECIMAL(3,1),
    total_analyses INTEGER DEFAULT 0,
    last_analysis_date TIMESTAMP,
    improvement_trend VARCHAR(20), -- 'improving', 'stable', 'declining'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX idx_analysis_sessions_user_id ON analysis_sessions(user_id);
CREATE INDEX idx_analysis_sessions_status ON analysis_sessions(status);
CREATE INDEX idx_analysis_sessions_created_at ON analysis_sessions(created_at DESC);
CREATE INDEX idx_analysis_results_session_id ON analysis_results(session_id);
CREATE INDEX idx_form_issues_result_id ON form_issues(result_id);
CREATE INDEX idx_form_issues_severity ON form_issues(severity);
CREATE INDEX idx_metrics_result_id ON metrics(result_id);
CREATE INDEX idx_strengths_result_id ON strengths(result_id);
CREATE INDEX idx_recommendations_result_id ON recommendations(result_id);
CREATE INDEX idx_user_progress_user_exercise ON user_progress(user_id, exercise_id);

-- ============================================
-- SEED DATA (Initial exercises)
-- ============================================

INSERT INTO exercises (name, category, icon, is_popular) VALUES
    ('Squat', 'Lower Body', '🏋️', true),
    ('Push-up', 'Upper Body', '💪', true),
    ('Deadlift', 'Lower Body', '⚡', true),
    ('Plank', 'Core', '🧘', true),
    ('Lunge', 'Lower Body', '🦵', true),
    ('Pull-up', 'Upper Body', '💪', true),
    ('Bench Press', 'Upper Body', '🏋️', false),
    ('Row', 'Upper Body', '🚣', false),
    ('Overhead Press', 'Upper Body', '🏋️', false),
    ('Hip Thrust', 'Lower Body', '🍑', false);
```

---

### Data Model Updates

**Python Pydantic Models (for FastAPI request/response validation):**
```python
# models/database.py - Database row representations

from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, UUID4

# ============================================
# USER MODELS
# ============================================

class User(BaseModel):
    id: UUID4
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True  # Allows Pydantic v2 to read from DB rows

# ============================================
# EXERCISE MODELS
# ============================================

class Exercise(BaseModel):
    id: UUID4
    name: str
    category: Literal["Upper Body", "Lower Body", "Core", "Other"]
    description: Optional[str] = None
    icon: Optional[str] = None
    is_popular: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# ANALYSIS MODELS (CORE)
# ============================================

class AnalysisSession(BaseModel):
    id: UUID4
    user_id: Optional[UUID4] = None  # None for demo without auth
    exercise_id: Optional[UUID4] = None
    exercise_name: str
    video_url: str
    video_duration: Optional[Decimal] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    status: Literal["pending", "processing", "completed", "failed"] = "pending"
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

class AnalysisResult(BaseModel):
    id: UUID4
    session_id: UUID4
    overall_score: Decimal  # 0.0 to 10.0
    total_frames: int
    processing_time: Optional[Decimal] = None
    created_at: datetime

    class Config:
        from_attributes = True

class FormIssue(BaseModel):
    id: UUID4
    result_id: UUID4
    issue_type: str
    severity: Literal["severe", "moderate", "minor"]
    frame_start: int
    frame_end: int
    coaching_cue: str
    confidence_score: Optional[Decimal] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Metric(BaseModel):
    id: UUID4
    result_id: UUID4
    metric_name: str
    actual_value: str
    target_value: str
    status: Literal["good", "warning", "error"]
    created_at: datetime

    class Config:
        from_attributes = True

class Strength(BaseModel):
    id: UUID4
    result_id: UUID4
    strength_text: str
    created_at: datetime

    class Config:
        from_attributes = True

class Recommendation(BaseModel):
    id: UUID4
    result_id: UUID4
    recommendation_text: str
    priority: int = 1
    created_at: datetime

    class Config:
        from_attributes = True

class UserProgress(BaseModel):
    id: UUID4
    user_id: UUID4
    exercise_id: Optional[UUID4] = None
    exercise_name: str
    average_score: Optional[Decimal] = None
    total_analyses: int = 0
    last_analysis_date: Optional[datetime] = None
    improvement_trend: Optional[Literal["improving", "stable", "declining"]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================
# API REQUEST/RESPONSE MODELS
# ============================================

class AnalysisSessionCreate(BaseModel):
    """Request model for creating a new analysis session"""
    exercise_name: str
    exercise_id: Optional[UUID4] = None
    video_url: str
    video_duration: Optional[float] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None

class AnalysisResultResponse(BaseModel):
    """Complete analysis response with all related data"""
    session: AnalysisSession
    result: AnalysisResult
    issues: list[FormIssue]
    metrics: list[Metric]
    strengths: list[Strength]
    recommendations: list[Recommendation]

class WebSocketEvent(BaseModel):
    """Base model for WebSocket events"""
    type: Literal["progress", "agent_status", "analysis_complete", "error"]
    data: dict

class ProgressEvent(BaseModel):
    """Progress update event"""
    type: Literal["progress"] = "progress"
    session_id: UUID4
    progress: int  # 0-100
    current_step: str
    estimated_time_remaining: int  # seconds

class AgentStatusEvent(BaseModel):
    """Agent status update event"""
    type: Literal["agent_status"] = "agent_status"
    session_id: UUID4
    vision_agent: Literal["idle", "running", "complete", "failed"]
    coaching_agent: Literal["idle", "running", "complete", "failed"]
    tasks: list[str]

class AnalysisCompleteEvent(BaseModel):
    """Analysis completion event"""
    type: Literal["analysis_complete"] = "analysis_complete"
    session_id: UUID4
    result_id: UUID4
    overall_score: Decimal

class ErrorEvent(BaseModel):
    """Error event"""
    type: Literal["error"] = "error"
    session_id: UUID4
    message: str
    code: str
```

---

### Data Migration Plan

**Phase 1: Initial Setup (Day 1 - No migration needed)**

Since this is a **greenfield project** (starting from scratch), there's no data to migrate. Steps:

1. **Create Database:**
```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE biome_coaching;
   
   # Connect to new database
   \c biome_coaching
```

2. **Run Schema Script:**
```bash
   # Execute the SQL schema from above
   psql -U postgres -d biome_coaching -f schema.sql
```

3. **Verify Tables Created:**
```bash
   # Check all tables exist
   psql -U postgres -d biome_coaching -c "\dt"
   
   # Should show 9 tables:
   # - users
   # - exercises
   # - analysis_sessions
   # - analysis_results
   # - form_issues
   # - metrics
   # - strengths
   # - recommendations
   # - user_progress
```

4. **Verify Seed Data:**
```bash
   # Check exercises were inserted
   psql -U postgres -d biome_coaching -c "SELECT name, category FROM exercises;"
   
   # Should show 10 exercises
```

**Phase 2: Hackathon Development (No migration - optional test data)**

For testing during development, optionally create mock data:
```sql
-- Optional: Create test user (if testing with auth)
INSERT INTO users (email, username, password_hash, first_name, last_name)
VALUES ('test@biome.app', 'testuser', 'hashed_password_here', 'Test', 'User');

-- Optional: Create test analysis session
INSERT INTO analysis_sessions (exercise_name, video_url, status)
VALUES ('Squat', '/uploads/test-squat.mp4', 'completed');
```

**Phase 3: Post-Hackathon Migrations (If schema changes needed)**

If you need to add/modify tables later, use migration pattern:
```sql
-- Example: Add new column to analysis_results
ALTER TABLE analysis_results 
ADD COLUMN ai_model_version VARCHAR(50);

-- Backfill existing rows
UPDATE analysis_results 
SET ai_model_version = 'gemini-2.0-flash' 
WHERE ai_model_version IS NULL;

-- Make it required going forward
ALTER TABLE analysis_results 
ALTER COLUMN ai_model_version SET NOT NULL;
```

**Backup Strategy (Production):**
```bash
# Before any schema changes in production:
pg_dump biome_coaching > backup_$(date +%Y%m%d_%H%M%S).sql

# If something breaks, restore:
psql biome_coaching < backup_20250129_143000.sql
```

**For Hackathon:** No backup/migration needed - if you break something, just drop and recreate:
```bash
# Nuclear option (dev only!)
psql -U postgres -c "DROP DATABASE biome_coaching;"
psql -U postgres -c "CREATE DATABASE biome_coaching;"
psql -U postgres -d biome_coaching -f schema.sql
```

---

## 7. ADK Agent & Tools Implementation

### Agent Architecture Rules
<!-- This is where you tell the AI agent how to structure your ADK-based backend -->

**Core Architecture Pattern: Single Agent + Tools (NOT Microservices)**

Google ADK uses an **agent-orchestrated** pattern where:
- One `root_agent` (defined in `agent.py`) serves as the intelligent orchestrator
- **Tools** are Python functions the agent calls (not separate services)
- ADK's **Runner** handles execution flow automatically
- Agent reasons about which tools to call and when

**Why This Matters for Biome:**
- MediaPipe pose extraction = Tool (not a microservice)
- Form analysis = Tool that leverages agent's reasoning
- Database operations = Tools call query functions
- Real-time updates = ADK callbacks (not manual WebSocket management)

---

### Project Structure (REQUIRED by ADK)

```
biome_coaching_agent/              # Main agent directory
├── __init__.py                    # MUST contain: from . import agent
├── agent.py                       # MUST define: root_agent = Agent(...)
├── config.py                      # Configuration (GCP project, DB connection, S3)
└── tools/                         # Agent capabilities (NOT microservices)
    ├── __init__.py
    ├── upload_video.py            # Handle video upload to storage
    ├── extract_pose_landmarks.py  # MediaPipe pose extraction
    ├── analyze_workout_form.py    # Form analysis with coaching cues
    ├── save_analysis_results.py   # Save to PostgreSQL
    └── notify_progress.py         # Real-time status updates

db/                                # Database layer (called by tools)
├── connection.py                  # PostgreSQL connection pool
└── queries.py                     # Raw SQL query functions

app.py                             # Optional: Custom FastAPI routes for file upload
requirements.txt                   # google-adk, mediapipe, psycopg2, boto3, etc.
schema.sql                         # PostgreSQL schema (from Section 6)
```

**ADK Discovery Convention:**
- Agent directory name: `biome_coaching_agent/`
- Must have `__init__.py` with: `from . import agent`
- Must have `agent.py` with: `root_agent = Agent(...)`
- This allows `adk web biome_coaching_agent/` to auto-discover your agent

---

### Root Agent Definition

**Location:** `biome_coaching_agent/agent.py`

**Required Pattern:**
```python
from google.adk.agents import Agent
from .tools import (
    upload_video,
    extract_pose_landmarks,
    analyze_workout_form,
    save_analysis_results,
    notify_progress
)

root_agent = Agent(
    name="biome_coaching_agent",
    model="gemini-2.0-flash",
    description="AI-powered fitness form coaching agent",
    instruction="""
    You are an expert fitness coach specializing in movement analysis.
    
    Your workflow:
    1. Accept video uploads (validate format, size, create session)
    2. Extract pose landmarks using MediaPipe (33 landmarks per frame)
    3. Analyze form (identify issues, generate coaching cues, calculate scores)
    4. Save results to database (issues, metrics, strengths, recommendations)
    5. Provide encouraging, specific feedback
    
    Common form issues to detect:
    - Knee Valgus (knees caving in) - High injury risk
    - Insufficient depth (squat not reaching parallel)
    - Forward lean (torso too horizontal)
    - Spine rounding (deadlift) - Disc injury risk
    
    Communication style:
    - Be encouraging and specific
    - Use frame numbers for precision
    - Prioritize injury prevention
    - Celebrate strengths
    """,
    tools=[
        upload_video,
        extract_pose_landmarks,
        analyze_workout_form,
        save_analysis_results,
        notify_progress
    ]
)
```

---

### Tool Implementation Patterns

**All tools follow this structure:**

```python
from google.adk.tools.tool_context import ToolContext

def tool_name(
    param1: str,
    param2: int,
    tool_context: ToolContext = None
) -> dict:
    """
    Brief description of what this tool does.
    
    Args:
        param1: Description
        param2: Description
        tool_context: ADK context for state management
        
    Returns:
        dict: Status and result data
    """
    try:
        # Implementation here
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

### Database Query Layer

**All database operations in:** `db/queries.py`

**Tools call these functions:**

```python
# db/queries.py
import psycopg2

def create_analysis_session(conn, session_id, user_id, exercise_name, video_url, duration, file_size):
    """Insert new analysis session."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analysis_sessions 
        (id, user_id, exercise_name, video_url, video_duration, file_size, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        RETURNING id
    """, (session_id, user_id, exercise_name, video_url, duration, file_size))
    return cursor.fetchone()[0]

def get_analysis_session(conn, session_id):
    """Get session by ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analysis_sessions WHERE id = %s", (session_id,))
    return cursor.fetchone()

# ... 15+ more query functions (see Section 6)
```

---

### Running the Agent

**Development (Interactive):**
```bash
adk web biome_coaching_agent/
# Opens browser UI for testing
```

**Production (API Server):**
```bash
adk api_server biome_coaching_agent/
# Auto-generates REST endpoints
```

**Custom File Upload:**
```python
# app.py - for custom /upload endpoint
from fastapi import FastAPI, UploadFile
from google.adk.runners import Runner
from biome_coaching_agent.agent import root_agent

app = FastAPI()

@app.post("/upload")
async def upload_video_endpoint(file: UploadFile):
    # Save file, trigger agent
    runner = Runner(root_agent)
    result = runner.run(user_input=f"Process video at {file.filename}")
    return result
```

---

## 8. Frontend Changes

### Frontend Status

**Current State:** Frontend already built by teammate (React + Tailwind CSS + shadcn/ui)

**No new components needed** - existing UI is complete

---

### Required Modifications

**1. API Configuration**
   - Update API base URL to point to Cloud Run deployment
   - Change from `localhost:8000` to Cloud Run URL
   - File: `frontend/src/config/api.ts` or similar

**2. Upload Component Integration**
   - Connect video upload to `/upload` endpoint (POST multipart/form-data)
   - Handle file validation on frontend (MP4/MOV/AVI/WebM, <100MB, <5min)
   - Display upload progress
   - File: Upload component

**3. Results Polling/WebSocket**
   - Implement status polling: `GET /sessions/{sessionId}` every 2 seconds
   - OR: Connect WebSocket for real-time updates (if implemented)
   - Update UI based on session status: pending → processing → completed
   - File: Results component

**4. Display Analysis Results**
   - Fetch complete results: `GET /sessions/{sessionId}/results`
   - Display: overall_score, form_issues list, metrics, strengths, recommendations
   - Video timeline with issue markers (click to jump to frame)
   - File: Results display component

---

### State Management

**No changes needed** - existing state management handles:
- Video upload state
- Processing status
- Analysis results display

---

## 9. Implementation Plan

### Phase-by-Phase Development Strategy

This implementation plan breaks down the Biome Coaching Agent development into 4 phases, optimized for a hackathon timeline (4-5 days). Each phase builds on the previous one with clear deliverables and specific file paths.

---

### **Phase 1: Foundation & Setup (Day 1 - 4 hours)**

**Goal:** Set up ADK agent structure, database, and verify basic tooling works

#### Tasks:

1. **Create ADK Agent Directory Structure**
   - [ ] Create `biome_coaching_agent/` directory
   - [ ] Create `biome_coaching_agent/__init__.py` with `from . import agent`
   - [ ] Create `biome_coaching_agent/agent.py`
   - [ ] Create `biome_coaching_agent/config.py`
   - [ ] Create `biome_coaching_agent/tools/` directory
   - [ ] Create `biome_coaching_agent/tools/__init__.py`

2. **Define Root Agent (Minimal Version)**
   - [ ] In `biome_coaching_agent/agent.py`:
     - Import Agent from google.adk
     - Define `root_agent` with name, model, description, instruction
     - Leave tools=[] empty for now
   - [ ] Write basic instruction prompt (coaching workflow overview)

3. **Set Up Database**
   - [ ] Install PostgreSQL (if not already installed)
   - [ ] Create database: `CREATE DATABASE biome_coaching;`
   - [ ] Run `schema.sql` to create all 9 tables
   - [ ] Verify tables: `\dt` command
   - [ ] Verify seed data: `SELECT * FROM exercises;`

4. **Create Database Connection Layer**
   - [ ] Create `db/` directory
   - [ ] Create `db/connection.py`:
     - Connection pool setup with psycopg2
     - `get_db_connection()` context manager
     - Connection string from environment variable
   - [ ] Create `db/queries.py` (empty for now, will fill in Phase 3)

5. **Install Dependencies**
   - [ ] Create `requirements.txt`:
google-adk
mediapipe==0.10.9
opencv-python
psycopg2-binary
python-dotenv
fastapi
uvicorn
boto3 # For S3 (optional for Phase 4)
   - [ ] Run: `pip install -r requirements.txt`

6. **Test Basic Agent**
   - [ ] Run: `adk web biome_coaching_agent/`
   - [ ] Verify agent loads in browser UI
   - [ ] Send test message: "Hello, analyze my squat"
   - [ ] Verify agent responds (no tools yet, just conversation)

**Deliverable:** Working ADK agent skeleton + database ready + agent responds to chat

**Files Created:**
- `biome_coaching_agent/__init__.py`
- `biome_coaching_agent/agent.py`
- `biome_coaching_agent/config.py`
- `biome_coaching_agent/tools/__init__.py`
- `db/connection.py`
- `db/queries.py` (skeleton)
- `requirements.txt`
- `schema.sql` (from Section 6)

---

### **Phase 2: Video Upload & Pose Extraction (Day 2 - 6 hours)**

**Goal:** Implement first two tools - video upload and MediaPipe pose extraction

#### Tasks:

1. **Implement upload_video Tool**
   - [ ] Create `biome_coaching_agent/tools/upload_video.py`
   - [ ] Function signature: `upload_video(video_file_path: str, exercise_name: str, user_id: Optional[str] = None, tool_context: ToolContext = None) -> dict`
   - [ ] Validate file exists and size < 100MB
   - [ ] Generate UUID for session_id
   - [ ] Copy video to `uploads/` directory (mkdir if needed)
   - [ ] Call `db.queries.create_analysis_session()` to save to DB
   - [ ] Return dict with status, session_id, video_url
   - [ ] Add comprehensive docstring

2. **Implement Database Query: create_analysis_session**
   - [ ] In `db/queries.py`:
   - [ ] Function: `create_analysis_session(conn, session_id, user_id, exercise_name, video_url, duration, file_size) -> str`
   - [ ] SQL: `INSERT INTO analysis_sessions (...) VALUES (...) RETURNING id`
   - [ ] Handle errors, return session_id

3. **Implement extract_pose_landmarks Tool**
   - [ ] Create `biome_coaching_agent/tools/extract_pose_landmarks.py`
   - [ ] Function signature: `extract_pose_landmarks(session_id: str, tool_context: ToolContext = None) -> dict`
   - [ ] Get video_url from database using session_id
   - [ ] Initialize MediaPipe Pose (model_complexity=1)
   - [ ] Open video with cv2.VideoCapture
   - [ ] Process at 10 FPS (skip frames for performance)
   - [ ] Extract 33 landmarks per frame
   - [ ] Calculate joint angles: `calculate_joint_angles()` helper
   - [ ] Calculate aggregate metrics: `calculate_aggregate_metrics()` helper
   - [ ] Detect exercise type: `detect_exercise_type()` helper (return "Squat" for hackathon)
   - [ ] Return dict with landmarks, metrics, detected_exercise

4. **Implement Helper Functions**
   - [ ] In same file: `calculate_joint_angles(landmarks: List[dict]) -> dict`
     - Calculate knee, hip, elbow angles using numpy
     - Use MediaPipe landmark indices (23-28 for legs)
   - [ ] In same file: `calculate_aggregate_metrics(frames: List[dict]) -> dict`
     - Calculate avg/min/max knee angles across frames
   - [ ] In same file: `detect_exercise_type(frames: List[dict]) -> str`
     - For hackathon: return "Squat" (hardcoded)

5. **Implement Database Query: get_analysis_session**
   - [ ] In `db/queries.py`:
   - [ ] Function: `get_analysis_session(conn, session_id) -> dict`
   - [ ] SQL: `SELECT * FROM analysis_sessions WHERE id = %s`
   - [ ] Return dict with video_url and other session data

6. **Implement Database Query: update_session_status**
   - [ ] In `db/queries.py`:
   - [ ] Function: `update_session_status(conn, session_id, status, error_message=None)`
   - [ ] SQL: `UPDATE analysis_sessions SET status = %s, updated_at = NOW() WHERE id = %s`

7. **Register Tools with Agent**
   - [ ] In `biome_coaching_agent/tools/__init__.py`:
     - Import upload_video and extract_pose_landmarks
     - Export in __all__
   - [ ] In `biome_coaching_agent/agent.py`:
     - Import tools: `from .tools import upload_video, extract_pose_landmarks`
     - Add to agent: `tools=[upload_video, extract_pose_landmarks]`

8. **Test Pose Extraction**
   - [ ] Create `test_videos/` directory
   - [ ] Download or record 30-second squat video
   - [ ] Save as `test_videos/sample_squat.mp4`
   - [ ] Run: `adk web biome_coaching_agent/`
   - [ ] In chat: "Process video at test_videos/sample_squat.mp4 for Squat exercise"
   - [ ] Verify: agent calls upload_video → extract_pose_landmarks
   - [ ] Check: Landmarks extracted, angles calculated
   - [ ] Check database: `SELECT * FROM analysis_sessions;`

**Deliverable:** Working video upload + MediaPipe pose extraction pipeline

**Files Created/Modified:**
- `biome_coaching_agent/tools/upload_video.py` (new)
- `biome_coaching_agent/tools/extract_pose_landmarks.py` (new)
- `biome_coaching_agent/tools/__init__.py` (modified)
- `biome_coaching_agent/agent.py` (modified - add tools)
- `db/queries.py` (add 3 functions)
- `test_videos/sample_squat.mp4` (test data)

---

### **Phase 3: Form Analysis & Database Persistence (Day 3 - 6 hours)**

**Goal:** Implement coaching analysis logic and save complete results to database

#### Tasks:

1. **Implement analyze_workout_form Tool**
   - [ ] Create `biome_coaching_agent/tools/analyze_workout_form.py`
   - [ ] Function signature: `analyze_workout_form(pose_data: dict, exercise_name: str, tool_context: ToolContext = None) -> dict`
   - [ ] Extract metrics from pose_data (avg_knee_angle, min_knee_angle, etc.)
   - [ ] Implement squat analysis logic:
     - Check depth: min_knee_angle < 90° = good depth
     - Check knee alignment (simplified for hackathon)
     - Identify issues with severity 1-10
     - Generate coaching cues (specific, actionable)
     - Note strengths (positive feedback)
   - [ ] Calculate overall_score (0-10): base 10, subtract penalties
   - [ ] Build metric comparisons (actual vs target values)
   - [ ] Build recommendations list
   - [ ] Return dict with overall_score, issues, metrics, strengths, recommendations

2. **Implement save_analysis_results Tool**
   - [ ] Create `biome_coaching_agent/tools/save_analysis_results.py`
   - [ ] Function signature: `save_analysis_results(session_id: str, analysis_data: dict, tool_context: ToolContext = None) -> dict`
   - [ ] Get DB connection
   - [ ] Call `create_analysis_result()` → get result_id
   - [ ] Loop through issues: call `create_form_issue()` for each
   - [ ] Loop through metrics: call `create_metric()` for each
   - [ ] Loop through strengths: call `create_strength()` for each
   - [ ] Loop through recommendations: call `create_recommendation()` for each
   - [ ] Call `update_session_status(session_id, "completed")`
   - [ ] Commit transaction
   - [ ] Return dict with result_id, confirmation

3. **Implement Database Queries (Analysis Results)**
   - [ ] In `db/queries.py`, add:
   - [ ] `create_analysis_result(conn, session_id, overall_score, total_frames, processing_time) -> str`
     - SQL: `INSERT INTO analysis_results (...) RETURNING id`
   - [ ] `create_form_issue(conn, result_id, issue_type, severity, coaching_cue, start_frame, end_frame)`
     - SQL: `INSERT INTO form_issues (...)`
   - [ ] `create_metric(conn, result_id, metric_name, actual_value, target_value, unit)`
     - SQL: `INSERT INTO metrics (...)`
   - [ ] `create_strength(conn, result_id, aspect, description)`
     - SQL: `INSERT INTO strengths (...)`
   - [ ] `create_recommendation(conn, result_id, category, suggestion, priority)`
     - SQL: `INSERT INTO recommendations (...)`

4. **Implement Database Queries (Fetch Results)**
   - [ ] In `db/queries.py`, add:
   - [ ] `get_analysis_result_by_session(conn, session_id) -> dict`
     - SQL: Complex JOIN across analysis_results, form_issues, metrics, strengths, recommendations
     - Return nested dict with all related data

5. **Register New Tools with Agent**
   - [ ] In `biome_coaching_agent/tools/__init__.py`:
     - Import analyze_workout_form and save_analysis_results
   - [ ] In `biome_coaching_agent/agent.py`:
     - Add to tools list

6. **Enhance Agent Instruction**
   - [ ] In `biome_coaching_agent/agent.py`:
   - [ ] Add detailed squat standards to instruction:
     - Knee angle targets
     - Common form issues definitions
     - Severity scoring guidelines
   - [ ] Add communication style guidance:
     - Be encouraging and specific
     - Frame issues as opportunities
     - Use frame numbers for precision

7. **Test Full Pipeline**
   - [ ] Run: `adk web biome_coaching_agent/`
   - [ ] Process same test video end-to-end
   - [ ] Verify all 4 tools called in sequence:
     1. upload_video
     2. extract_pose_landmarks
     3. analyze_workout_form
     4. save_analysis_results
   - [ ] Check database records:
     ```sql
     SELECT * FROM analysis_results WHERE session_id = '...';
     SELECT * FROM form_issues WHERE result_id = '...';
     SELECT * FROM metrics WHERE result_id = '...';
     SELECT * FROM strengths WHERE result_id = '...';
     ```
   - [ ] Verify coaching cues are specific and actionable

**Deliverable:** Complete analysis pipeline from video → results in database

**Files Created/Modified:**
- `biome_coaching_agent/tools/analyze_workout_form.py` (new)
- `biome_coaching_agent/tools/save_analysis_results.py` (new)
- `biome_coaching_agent/tools/__init__.py` (modified)
- `biome_coaching_agent/agent.py` (modified - add tools, enhance instruction)
- `db/queries.py` (add 6 query functions)

---

### **Phase 4: API Integration & Frontend Connection (Day 4 - 6 hours)**

**Goal:** Expose API endpoints for frontend, add file upload, test with real frontend

#### Tasks:

1. **Create Custom FastAPI App (for File Upload)**
   - [ ] Create `app.py` in project root
   - [ ] Import FastAPI, UploadFile
   - [ ] Create `/upload` endpoint:
     - Accept multipart/form-data video file
     - Accept exercise_name as form field
     - Save file to temp location
     - Trigger ADK agent with video path
     - Return session_id
   - [ ] Add CORS middleware for frontend (port 3000/5173)
   - [ ] Mount ADK routes if needed

2. **Start ADK API Server**
   - [ ] Test command: `adk api_server biome_coaching_agent/`
   - [ ] Verify endpoints available:
     - POST /sessions/{session_id}/run
     - GET /sessions/{session_id}
   - [ ] Document API responses

3. **Implement notify_progress Tool (Optional)**
   - [ ] Create `biome_coaching_agent/tools/notify_progress.py`
   - [ ] For hackathon: Can be a no-op that returns success
   - [ ] Or: Implement simple HTTP callback to frontend
   - [ ] Store progress in database for polling:
     - Add `progress` column to analysis_sessions
     - Update progress at each tool stage
   - [ ] Frontend polls GET /sessions/{session_id} for status

4. **Create Frontend Integration Test**
   - [ ] If frontend already exists:
     - Update API endpoint to localhost:8000 (or ADK port)
     - Test video upload → processing → results display
   - [ ] If frontend not ready:
     - Create simple HTML test page:
       ```html
       <form id="upload-form">
         <input type="file" name="video" accept="video/*">
         <input type="text" name="exercise_name" value="Squat">
         <button type="submit">Upload</button>
       </form>
       <div id="results"></div>
       ```
     - JavaScript to POST to /upload
     - Poll GET /sessions/{session_id} every 2 seconds
     - Display results when status='completed'

5. **Add Environment Configuration**
   - [ ] Create `.env` file with database URL, API keys
   - [ ] In `biome_coaching_agent/config.py`:
     - Load environment variables with python-dotenv
     - Export DB_CONNECTION_STRING, API_KEY, etc.

6. **Add Error Handling**
   - [ ] In each tool, wrap main logic in try/except
   - [ ] Return structured error responses:
     ```python
     {
       "status": "error",
       "message": "Descriptive error message",
       "code": "UPLOAD_FAILED"
     }
     ```
   - [ ] Update agent instruction to handle tool errors gracefully

7. **Test End-to-End with Frontend**
   - [ ] Start backend: `uvicorn app:app --reload` (if using custom app.py)
   - [ ] Or: `adk api_server biome_coaching_agent/`
   - [ ] Start frontend (if available): `npm run dev`
   - [ ] Upload test video through UI
   - [ ] Verify flow:
     1. Video uploads successfully
     2. Session created in DB
     3. Processing happens (can see in ADK web UI logs)
     4. Results appear in frontend
   - [ ] Test error cases:
     - Upload invalid file (too large)
     - Upload non-video file
     - Process video with no person visible

8. **Documentation & Demo Prep**
   - [ ] Create `README.md`:
     - Setup instructions
     - How to run database setup
     - How to start agent
     - API endpoint documentation
     - Example curl commands
   - [ ] Create demo script:
     - 3-5 test videos (good form, bad form, edge cases)
     - Expected coaching feedback for each
   - [ ] Prepare Devpost submission:
     - Screenshots of agent in action
     - Architecture diagram
     - Demo video (record screen)

**Deliverable:** Production-ready API + frontend integration + demo materials

**Files Created/Modified:**
- `app.py` (new - custom FastAPI app)
- `biome_coaching_agent/tools/notify_progress.py` (new - optional)
- `biome_coaching_agent/config.py` (modified - env vars)
- `.env` (new - secrets)
- `README.md` (new - documentation)
- `test.html` (new - simple test UI if needed)
- All tools (add error handling)

---

### **Phase 5: Polish & Optimization (Day 5 - Optional if time permits)**

**Goal:** Performance improvements, better error messages, demo polish

#### Tasks (Pick highest value items if time limited):

1. **Performance Optimization**
   - [ ] Profile MediaPipe processing time
   - [ ] Reduce FPS if needed (10 → 5 FPS for faster processing)
   - [ ] Add progress tracking within extract_pose_landmarks
   - [ ] Consider parallel processing for multiple uploads (future)

2. **Enhanced Coaching Feedback**
   - [ ] Add more exercise standards (deadlift, bench press)
   - [ ] Improve issue detection (knee valgus, buttwink, forward lean)
   - [ ] Add visual cues (frame ranges for scrubbing video)

3. **Better Error Messages**
   - [ ] User-friendly error messages in tools
   - [ ] Agent instruction: How to handle common errors
   - [ ] Logging: Add proper logging to all tools

4. **Demo Polish**
   - [ ] Test with 10+ videos
   - [ ] Refine agent instruction based on test results
   - [ ] Add example videos to repo
   - [ ] Create compelling demo narrative

5. **Optional: Real-time WebSocket**
   - [ ] Implement WebSocket server in app.py
   - [ ] Emit progress events from each tool
   - [ ] Frontend listens to WebSocket for live updates

**Deliverable:** Polished demo-ready application

---

### Task Completion Checklist Summary

**Phase 1 - Foundation (Must Have):**
- [ ] Agent structure created
- [ ] Database initialized
- [ ] Basic agent responds to chat

**Phase 2 - Core Pipeline (Must Have):**
- [ ] Video upload works
- [ ] Pose extraction works
- [ ] Data flows through tools

**Phase 3 - Analysis (Must Have):**
- [ ] Form analysis generates feedback
- [ ] Results saved to database
- [ ] Coaching cues are specific

**Phase 4 - Integration (Must Have):**
- [ ] API endpoints working
- [ ] Frontend can upload videos
- [ ] Results display correctly

**Phase 5 - Polish (Nice to Have):**
- [ ] Performance optimized
- [ ] Multiple exercises supported
- [ ] Demo materials ready

---

### Critical Path (Minimum Viable Demo)

If time is extremely limited, focus on this subset:

**Day 1:** Phase 1 (Foundation)
**Day 2:** Phase 2 (Upload + Pose) - Skip perfect error handling
**Day 3:** Phase 3 (Analysis) - Hardcode squat logic only
**Day 4:** Phase 4 (API) - Use simple HTML test page if frontend not ready

**Minimum Demo:** 
- Upload 1 squat video
- Extract pose landmarks
- Generate 2-3 coaching cues
- Display results in simple UI

This gets you a working demo for judges, even if not fully polished.

---

## 10. Task Completion Tracking

### Real-Time Progress Tracking
<!-- This is where you tell the AI agent to update progress as work is completed -->

**Tracking Philosophy:**
As you work through the implementation plan (Section 9), maintain real-time visibility of progress. This helps you stay on track during the hackathon timeline and quickly identify blockers.

---

### Progress Tracking System

**Use this format to track progress through each phase:**

#### **Current Phase Status**

```markdown
📍 **Currently Working On:** Phase [X] - [Phase Name]

**Phase Progress:** [X]/[Y] tasks completed ([Z]%)

**Current Task:** [Specific task you're working on right now]

**Time Spent:** [X] hours / [Y] hours estimated

**Blockers:** [None | List any blockers]
```

**Example:**
```markdown
📍 **Currently Working On:** Phase 2 - Video Upload & Pose Extraction

**Phase Progress:** 5/8 tasks completed (62%)

**Current Task:** Implementing extract_pose_landmarks tool - calculating joint angles

**Time Spent:** 4 hours / 6 hours estimated

**Blockers:** None
```

---

### Task Completion Format

**When you complete a task, update in this format:**

```markdown
✅ **Task Completed:** [Task description]
- **File(s) Modified/Created:** [List files with paths]
- **Lines of Code:** [Approximate LOC]
- **Testing Status:** [✅ Tested | ⚠️ Needs Testing | ❌ Not Yet Tested]
- **Notes:** [Any important implementation details, decisions made, or issues encountered]
- **Time Taken:** [X] minutes/hours
```

**Example:**
```markdown
✅ **Task Completed:** Implemented upload_video tool
- **File(s) Modified/Created:** 
  - biome_coaching_agent/tools/upload_video.py (new, 85 lines)
  - db/queries.py (added create_analysis_session function, 15 lines)
- **Lines of Code:** ~100 LOC
- **Testing Status:** ✅ Tested with sample_squat.mp4
- **Notes:** Using local file storage for hackathon. TODO: Add S3 integration post-demo. Session IDs are UUIDs.
- **Time Taken:** 45 minutes
```

---

### Phase Completion Report

**At the end of each phase, provide a summary:**

```markdown
## Phase [X] Completion Report

**Phase Name:** [Phase name]
**Status:** ✅ Complete | ⚠️ Partial | ❌ Blocked
**Completion Date:** [Date]
**Total Time:** [X] hours

### Completed Tasks:
- [✅] Task 1 description
- [✅] Task 2 description
- [✅] Task 3 description

### Skipped/Deferred Tasks:
- [⏭️] Task description - Reason for deferral

### Key Deliverables:
- [Deliverable 1]
- [Deliverable 2]

### Files Created/Modified:
- `path/to/file1.py` (new, 120 lines)
- `path/to/file2.py` (modified, +45 lines)
- `path/to/file3.sql` (new, 200 lines)

### Testing Results:
- [Test description] - ✅ Passed
- [Test description] - ⚠️ Partial (note why)

### Blockers Encountered:
- [Blocker 1] - Resolved by [solution]
- [Blocker 2] - Still open, workaround: [workaround]

### Next Phase Preview:
Starting Phase [X+1] - [Phase name]. Key focus: [brief description]

### Notes for Future Work:
- Technical debt: [Any shortcuts taken for speed]
- Optimization opportunities: [Performance improvements to consider]
- Known bugs: [Any non-critical issues to fix later]
```

---

### Daily Stand-up Format (Optional for Multi-Day Projects)

**At start of each work session:**

```markdown
## Daily Progress - [Date]

### Yesterday's Accomplishments:
- [What you completed yesterday]
- [Key wins or breakthroughs]

### Today's Goals:
- [ ] Goal 1 (Phase [X], Task [Y])
- [ ] Goal 2 (Phase [X], Task [Z])
- [ ] Goal 3 (Testing/Integration)

### Potential Blockers:
- [Blocker 1] - Plan: [how you'll handle it]
- [Blocker 2] - Need: [what you need to unblock]

### Time Budget:
- Available: [X] hours
- Allocated: [Y] hours to Phase [Z]
```

---

### File Change Log

**Maintain a running log of all files touched:**

```markdown
### File Change Log

| File Path | Status | Phase | LOC | Last Modified | Notes |
|-----------|--------|-------|-----|---------------|-------|
| biome_coaching_agent/agent.py | Modified | 1,2,3 | +150 | Day 3 | Added tools, enhanced instruction |
| biome_coaching_agent/tools/upload_video.py | Created | 2 | 85 | Day 2 | Video upload with validation |
| biome_coaching_agent/tools/extract_pose_landmarks.py | Created | 2 | 220 | Day 2 | MediaPipe integration |
| biome_coaching_agent/tools/analyze_workout_form.py | Created | 3 | 180 | Day 3 | Form analysis logic |
| db/queries.py | Modified | 2,3 | +180 | Day 3 | Added 9 query functions |
| schema.sql | Created | 1 | 250 | Day 1 | Database schema |
| app.py | Created | 4 | 65 | Day 4 | Custom FastAPI routes |
| requirements.txt | Created | 1 | 12 | Day 1 | Dependencies |
```

---

### Testing Checklist

**Track testing status for each component:**

```markdown
### Testing Status

#### Phase 1 - Foundation:
- [✅] Database tables created successfully
- [✅] Agent loads in ADK web UI
- [✅] Agent responds to basic chat

#### Phase 2 - Video Upload & Pose Extraction:
- [✅] Video upload with valid file succeeds
- [✅] Video upload with invalid file fails gracefully
- [✅] MediaPipe extracts landmarks from test video
- [✅] Joint angles calculated correctly
- [✅] Session created in database
- [⚠️] Large video (>100MB) validation (partial)

#### Phase 3 - Form Analysis:
- [✅] Squat analysis identifies depth correctly
- [✅] Form issues have severity scores
- [✅] Coaching cues are specific and actionable
- [✅] Results saved to all 5 database tables
- [❌] Deadlift analysis (deferred to Phase 5)

#### Phase 4 - API Integration:
- [✅] /upload endpoint accepts video files
- [✅] Frontend can retrieve results via GET
- [⚠️] WebSocket real-time updates (using polling instead)
- [✅] CORS configured for frontend
- [✅] Error responses are user-friendly

#### Phase 5 - Polish (Optional):
- [⏭️] Performance optimization (deferred if time limited)
- [⏭️] Multiple exercise support (deferred)
```

---

### Blocker Tracking

**Document blockers as they arise:**

```markdown
### Active Blockers

| # | Blocker Description | Impact | Discovered | Status | Resolution |
|---|---------------------|--------|------------|--------|------------|
| 1 | MediaPipe slow on large videos | Performance | Day 2 | Resolved | Reduced FPS from 30 to 10 |
| 2 | Database connection pool exhaustion | Stability | Day 3 | Resolved | Increased pool size to 10 |
| 3 | Frontend CORS errors | Integration | Day 4 | Open | Added CORS middleware, testing |

### Resolved Blockers

| # | Blocker Description | Impact | Resolution Date | How Resolved |
|---|---------------------|--------|-----------------|--------------|
| 1 | MediaPipe slow on large videos | Performance | Day 2 | Reduced processing FPS to 10 |
| 2 | Gemini API rate limits | Speed | Day 3 | Switched to gemini-2.0-flash model |
```

---

### Commit Message Log (For Version Control)

**Track Git commits aligned with tasks:**

```markdown
### Commit History

| Commit Hash | Date | Message | Files Changed | Phase |
|-------------|------|---------|---------------|-------|
| a1b2c3d | Day 1 | feat: Initialize ADK agent structure | 5 files | 1 |
| e4f5g6h | Day 1 | feat: Add database schema and connection | 3 files | 1 |
| i7j8k9l | Day 2 | feat: Implement upload_video tool | 2 files | 2 |
| m0n1o2p | Day 2 | feat: Implement pose extraction with MediaPipe | 2 files | 2 |
| q3r4s5t | Day 3 | feat: Add form analysis and coaching logic | 2 files | 3 |
| u6v7w8x | Day 3 | feat: Implement database persistence for results | 2 files | 3 |
| y9z0a1b | Day 4 | feat: Add FastAPI upload endpoint | 1 file | 4 |
| c2d3e4f | Day 4 | fix: Add CORS middleware for frontend | 1 file | 4 |
```

---

### AI Agent Instructions for Progress Tracking

**When working with an AI coding assistant, use these prompts:**

#### Starting a Task:

## 11. File Structure & Organization

### Complete Project Structure
biome_agent/
│
├── biome_coaching_agent/ # ADK Agent (main application)
│ ├── init.py # Must contain: from . import agent
│ ├── agent.py # Must define: root_agent = Agent(...)
│ ├── config.py # Configuration (DB, API keys, S3)
│ └── tools/ # Agent capabilities
│ ├── init.py
│ ├── upload_video.py
│ ├── extract_pose_landmarks.py
│ ├── analyze_workout_form.py
│ ├── save_analysis_results.py
│ └── notify_progress.py
│
├── db/ # Database layer
│ ├── connection.py # PostgreSQL connection pool
│ └── queries.py # All SQL query functions
│
├── uploads/ # Video storage (local/temp)
│ └── .gitkeep
│
├── test_videos/ # Sample videos for testing
│ └── sample_squat.mp4
│
├── app.py # Optional: Custom FastAPI routes
├── schema.sql # Database schema (9 tables)
├── requirements.txt # Python dependencies
├── .env # Environment variables (not in git)
├── .gitignore # Git ignore rules
└── README.md # Setup and usage documentation


---

### Files to Create (New)

| File Path | Purpose | Phase | Lines (Est.) |
|-----------|---------|-------|--------------|
| `biome_coaching_agent/__init__.py` | Agent module init | 1 | 1 |
| `biome_coaching_agent/agent.py` | Root agent definition | 1 | 80 |
| `biome_coaching_agent/config.py` | Configuration management | 1 | 30 |
| `biome_coaching_agent/tools/__init__.py` | Tools module init | 1 | 10 |
| `biome_coaching_agent/tools/upload_video.py` | Video upload tool | 2 | 85 |
| `biome_coaching_agent/tools/extract_pose_landmarks.py` | MediaPipe integration | 2 | 220 |
| `biome_coaching_agent/tools/analyze_workout_form.py` | Form analysis logic | 3 | 180 |
| `biome_coaching_agent/tools/save_analysis_results.py` | Database persistence | 3 | 120 |
| `biome_coaching_agent/tools/notify_progress.py` | Progress updates | 4 | 40 |
| `db/connection.py` | Database connection | 1 | 40 |
| `db/queries.py` | SQL query functions | 2-3 | 250 |
| `schema.sql` | Database schema | 1 | 250 |
| `app.py` | Custom FastAPI app | 4 | 65 |
| `requirements.txt` | Dependencies | 1 | 12 |
| `.env` | Environment variables | 1 | 10 |
| `README.md` | Documentation | 4 | 100 |

**Total New Files:** 16 files  
**Estimated Total LOC:** ~1,500 lines

---

### Files to Modify (Existing)

If frontend already exists:
- Frontend API configuration (point to backend)
- Frontend upload component (connect to /upload endpoint)

Otherwise: No existing files to modify (greenfield project)

---

### Key Directories Explained

**`biome_coaching_agent/`** - Main ADK agent
- Contains agent definition and all tools
- Must follow ADK naming convention for auto-discovery

**`biome_coaching_agent/tools/`** - Agent capabilities  
- Each file = one tool (Python function)
- Tools are called by agent during reasoning

**`db/`** - Database abstraction layer
- `connection.py` - Connection pooling
- `queries.py` - All SQL operations (called by tools)

**`uploads/`** - Temporary video storage
- Videos saved here after upload
- Could be replaced with S3 in production

**`test_videos/`** - Sample data for testing
- Demo videos for development and testing

---

### Files NOT to Create

❌ No separate microservices (vision_service/, agent_service/)  
❌ No manual WebSocket manager (use ADK callbacks)  
❌ No complex API routing files (ADK auto-generates)  
❌ No separate orchestration service (ADK Runner handles this)

---

### Git Ignore Rules

**.gitignore:**
```gitignore
# Environment
.env
.venv/
venv/

# Uploads
uploads/*.mp4
uploads/*.mov
uploads/*.avi
!uploads/.gitkeep

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# Database
*.db
```

---

### Environment Variables

**.env template:**
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/biome_coaching

# Google API
GOOGLE_API_KEY=your_gemini_api_key_here

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_BUCKET_NAME=biome-videos

# Application
DEBUG=true
PORT=8000
```

---

### Dependencies List

**requirements.txt:**
```
google-adk>=1.0.0
mediapipe==0.10.9
opencv-python>=4.8.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
boto3>=1.29.0
numpy>=1.24.0
pydantic>=2.0.0
```

This is everything you need - no more, no less. Simple and complete! 🎯



## 12. AI Agent Instructions

### Implementation Workflow
<!-- This is where you give specific instructions to your AI agent -->

🎯 **MANDATORY PROCESS:**

**When implementing any task:**

1. **Read First** - Review relevant sections (especially Section 7, 9, 11)
2. **Confirm Understanding** - Briefly state what you'll implement
3. **Implement** - Write code following ADK patterns from Section 7
4. **Test** - Verify it works before moving to next task
5. **Update Progress** - Mark task complete in Section 10 format

**Before writing code:**
- ✅ Check Section 11 for correct file paths
- ✅ Check Section 7 for code patterns and structure
- ✅ Use exact ADK conventions (Agent + Tools, not microservices)

**After writing code:**
- ✅ Add docstrings to all functions
- ✅ Include error handling (try/except with meaningful messages)
- ✅ Test with sample data
- ✅ Report what was done in Section 10 format

---

### Communication Preferences
<!-- This is where you set expectations for how the AI should communicate -->

**What I want:**
- ✅ **Be concise** - Short explanations, focus on code
- ✅ **Show file paths** - Always specify which file you're modifying
- ✅ **Highlight decisions** - If you made a choice, explain why briefly
- ✅ **Flag issues early** - Tell me immediately if something seems wrong

**What I don't want:**
- ❌ Long explanations of basic concepts
- ❌ Asking permission for every small decision
- ❌ Suggesting alternative approaches (just follow the spec)
- ❌ Repeating information I already know

**Response format:**
📝 Implementing: [Task name]
📂 File: [path/to/file.py]
[Code here]
✅ Done. Tested with [test case]. Ready for next task.


---

### Code Quality Standards
<!-- This is where you define your coding standards for the AI to follow -->

**Follow ADK Best Practices:**
- Use Google Python Style Guide (2-space indentation, 80-char lines)
- All tools return `dict` with `"status"` key
- All tools accept `ToolContext` parameter (even if unused)
- Use type hints for all function parameters
- Docstrings required (Args, Returns format)

**Python Standards:**
```python
# ✅ DO THIS
def upload_video(
    video_file_path: str,
    exercise_name: str,
    tool_context: ToolContext = None
) -> dict:
    """
    Upload workout video to storage.
    
    Args:
        video_file_path: Path to video file
        exercise_name: Exercise type (Squat, Deadlift, etc.)
        tool_context: ADK context for state management
        
    Returns:
        dict: Status and session_id
    """
    try:
        # Implementation here
        return {"status": "success", "session_id": session_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ❌ DON'T DO THIS
def upload(path, name):  # No types, no docstring, no error handling
    id = uuid.uuid4()
    # save file
    return id
```

**Database Queries:**
- Use parameterized queries: `cursor.execute(sql, (param1, param2))`
- Never use string formatting: ❌ `f"SELECT * FROM users WHERE id = {user_id}"`
- Always use context manager: `with get_db_connection() as conn:`

**Error Handling:**
- Every tool wrapped in try/except
- Return structured errors: `{"status": "error", "message": "..."}`
- Log errors for debugging: `logging.error(f"Upload failed: {str(e)}")`

**Testing:**
- Test each tool individually before moving on
- Use `test_videos/sample_squat.mp4` for testing
- Verify database records after each operation

---

### Quick Reference for AI

**Agent Structure (REQUIRED):**
```python
# biome_coaching_agent/agent.py
from google.adk.agents import Agent
from .tools import tool1, tool2

root_agent = Agent(
    name="biome_coaching_agent",
    model="gemini-2.0-flash",
    description="Brief description",
    instruction="Detailed instruction...",
    tools=[tool1, tool2]
)
```

**Tool Structure (REQUIRED):**
```python
# biome_coaching_agent/tools/my_tool.py
from google.adk.tools.tool_context import ToolContext

def my_tool(
    param1: str,
    param2: int,
    tool_context: ToolContext = None
) -> dict:
    """Tool description."""
    try:
        # Implementation
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

**Database Query (REQUIRED):**
```python
# db/queries.py
def query_name(conn, param1, param2):
    """Query description."""
    cursor = conn.cursor()
    cursor.execute("SQL HERE", (param1, param2))
    return cursor.fetchone()
```

---

### Priority Rules

**For Hackathon Speed:**
1. **Working > Perfect** - Get it working first, optimize later
2. **Core features only** - Skip nice-to-haves until Phase 5
3. **Hardcode when safe** - Exercise type detection can return "Squat" for now
4. **Local storage OK** - S3 integration can wait until after demo

**But never skip:**
- ❌ Error handling (breaks demo)
- ❌ Database transactions (data corruption)
- ❌ ADK structure (won't work otherwise)
- ❌ Type hints & docstrings (breaks ADK tool discovery)

---

### When Stuck

**If you encounter an issue:**

1. **Check ADK docs** - Review ADK folder examples
2. **Check template** - Re-read Section 7 patterns
3. **Ask me** - Include: what you tried, what error you got
4. **Workaround** - Suggest simplest solution to keep moving

**Don't:**
- ❌ Spin trying 10 different approaches
- ❌ Switch to completely different architecture
- ❌ Skip the task without asking

---

## 13. Second-Order Impact Analysis

### Impact Assessment
<!-- This is where you think through broader consequences of your changes -->

**Hackathon Compliance Requirements:**

Based on Cloud Run Hackathon rules, this project must comply with:

---

### ✅ Core Requirements (MUST HAVE)

**1. Cloud Run Deployment (Required)**
   - Must deploy to Cloud Run as foundation
   - Use Cloud Run **Service** type (responds to HTTP requests)
   - Auto-scales based on traffic
   - **Impact:** Need to containerize FastAPI + MediaPipe + ADK

**2. Google ADK (Required for "AI Agents Category")**
   - Building agent-based application using Google ADK ✅
   - Solves real-world problem (injury prevention) ✅
   - **Impact:** Must follow ADK structure conventions (Section 7)

**3. Original Work (Contest Period)**
   - Project created between Oct 6 - Nov 10, 2025
   - No pre-existing code allowed
   - **Impact:** Everything built during hackathon

**4. Submission Requirements**
   - Public code repository (GitHub) ✅
   - Architecture diagram showing technologies ⚠️ Need to create
   - Demo video (max 3 minutes) ⚠️ Need to record
   - Comprehensive text description ⚠️ Need to write
   - Hosted project URL (Cloud Run) ⚠️ Need to deploy
   - English language support ✅

---

### 🎁 Bonus Points Opportunities (Optional but Valuable)

**1. Use Google AI Model (+0.4 points)**
   - ✅ Using Gemini 2.0 Flash for coaching analysis
   - **Action:** Document this prominently in submission

**2. Multiple Cloud Run Services (+0.4 points)**
   - ⚠️ Currently: Single service (backend)
   - **Opportunity:** Deploy frontend separately on Cloud Run
   - **Action:** Consider deploying React frontend as second Cloud Run service

**3. Publish Blog Post (+0.4 points)**
   - ⚠️ Not yet done
   - **Opportunity:** Write Medium/dev.to post about building with ADK + Cloud Run
   - **Action:** Document development process, learnings, challenges

**4. Social Media Post (+0.4 points)**
   - ⚠️ Not yet done
   - **Opportunity:** Post on LinkedIn/X with #CloudRunHackathon
   - **Action:** Share project demo, architecture, learnings

**Maximum Total Score:** 6.6 points (5.0 base + 1.6 bonus)

---

### ⚠️ Critical Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Cloud Run deployment fails | Cannot submit | Medium | Test deployment early in Phase 4, use Cloud Build |
| MediaPipe dependencies too large | Deployment timeout | Medium | Optimize Docker image, use multi-stage build, request 4GB+ memory |
| Video processing exceeds timeout | Demo breaks | High | Set Cloud Run timeout to 300s, optimize FPS to 5-10 |
| Database incompatible with Cloud Run | Backend fails | Medium | Use Cloud SQL (PostgreSQL) instead of local DB |
| Exceeds $100 Google Cloud credit | Can't finish | Low | Monitor usage, use cheapest Gemini model (Flash), limit test videos |
| Video files too large for Cloud Run | Upload fails | Medium | Enforce 100MB limit, use Cloud Storage for videos |
| Demo video over 3 minutes | Submission invalid | Low | Practice demo, time it, edit tightly |
| Missing public repository | Disqualified | Low | Make repo public before submission |

---

### 🎯 Judging Criteria Strategy

**Technical Implementation (40% weight):**
- Clean, well-documented Python code with docstrings ✅
- Proper ADK structure following conventions ✅
- Efficient error handling in all tools ✅
- Production-ready with Cloud Run deployment ⚠️ (Phase 4)
- **Focus:** Show code quality, ADK best practices, scalability

**Demo and Presentation (40% weight):**
- Clear problem definition (injury prevention in fitness) ✅
- Effective solution presentation via demo and docs ⚠️ (Phase 4)
- Architecture diagram showing all components ⚠️ (Need to create)
- Explanation of Cloud Run usage ⚠️ (Document in README)
- **Focus:** Professional presentation, clear value proposition

**Innovation and Creativity (20% weight):**
- Novel use of ADK for real-time coaching ✅
- Unique combination: MediaPipe + Gemini + ADK ✅
- Addresses significant problem effectively ✅
- **Focus:** Emphasize uniqueness, real-world impact

**Expected Score:** 5.0-5.8/6.6 (competitive for category win, potential Grand Prize)

---

### 🏗️ Cloud Run Deployment Considerations

**Changes Required for Cloud Run:**

**1. Database**
   - **Current:** Local PostgreSQL
   - **Cloud Run:** Cloud SQL (PostgreSQL) or Firestore
   - **Action:** Update connection string in `config.py`

**2. File Storage**
   - **Current:** Local `uploads/` folder
   - **Cloud Run:** Google Cloud Storage bucket
   - **Action:** Replace file saving logic with Cloud Storage API

**3. Container Image**
   - **Need:** Dockerfile for FastAPI + MediaPipe + ADK
   - **Size:** MediaPipe is large (~500MB), optimize layers
   - **Action:** Multi-stage build, minimize dependencies

**4. Environment Variables**
   - **Current:** `.env` file
   - **Cloud Run:** Set via `gcloud run deploy --set-env-vars`
   - **Action:** Document all required env vars

**5. Resource Allocation**
   - **Memory:** 4GB minimum (MediaPipe + video processing)
   - **Timeout:** 300 seconds (video analysis takes time)
   - **CPU:** 2 vCPUs recommended

**Deployment Command:**
```bash
gcloud run deploy biome-agent \
  --source . \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300s \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=postgresql://...,GOOGLE_API_KEY=...
```

---

### 📋 Pre-Submission Checklist

**Code & Repository:**
- [ ] Code repository is public on GitHub
- [ ] README.md with clear setup instructions
- [ ] requirements.txt complete and tested
- [ ] .gitignore properly configured
- [ ] Code follows ADK conventions (Section 7)
- [ ] All tools have docstrings and error handling

**Cloud Run Deployment:**
- [ ] Dockerfile created and optimized
- [ ] Deployed to Cloud Run successfully
- [ ] Public URL accessible and functional
- [ ] Database connected (Cloud SQL or Firestore)
- [ ] Video storage working (Cloud Storage)
- [ ] Environment variables configured

**Documentation:**
- [ ] Architecture diagram created (use draw.io/excalidraw)
- [ ] Comprehensive text description written
- [ ] Technologies used clearly documented
- [ ] Learning and challenges documented

**Demo:**
- [ ] Demo video recorded (under 3 minutes)
- [ ] Shows complete flow: upload → analysis → results
- [ ] English audio or subtitles
- [ ] Uploaded to YouTube/Vimeo and public
- [ ] URL added to submission

**Bonus Content (Optional):**
- [ ] Blog post published on Medium/dev.to
- [ ] Social media post with #CloudRunHackathon
- [ ] Screenshots and visuals created

**Submission:**
- [ ] Category selected: "AI Agents Category"
- [ ] All required fields filled on Devpost
- [ ] Submission reviewed for prohibited content
- [ ] Tested: All links work and are public

---

### 🚫 Disqualification Risks (AVOID)

**Do NOT:**
- ❌ Use code created before October 6, 2025
- ❌ Fail to deploy to Cloud Run
- ❌ Submit video longer than 3 minutes
- ❌ Keep code repository private
- ❌ Include offensive or copyrighted content
- ❌ Miss demo video or text description
- ❌ Forget to provide test access/credentials

---

### 💡 Success Strategy Summary

**Phase 4 Priority Actions:**
1. Deploy to Cloud Run early (test thoroughly)
2. Create architecture diagram (tools: draw.io, Lucidchart)
3. Record demo video (practice first, keep under 3 min)
4. Write comprehensive submission text (problem → solution → tech → impact)
5. Make repository public with great README
6. Consider: Deploy frontend separately for +0.4 bonus points
7. Consider: Write blog post for +0.4 bonus points
8. Post on social media with #CloudRunHackathon for +0.4 bonus

**This maximizes chances for category win or Grand Prize! 🏆**

---

**🎯 Ready to Plan Your Next Project?**

This template gives you the framework - now fill it out with your specific project details! 

*Want the complete version with detailed examples, advanced strategies, and full AI agent workflows? [Watch the full tutorial video here]*

---
