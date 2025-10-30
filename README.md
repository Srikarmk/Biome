## Biome Coaching Agent

AI-powered fitness form coaching that analyzes workout videos and delivers precise, encouraging cues to improve technique and prevent injuries. Built with ADK for speed, reliability, and extensibility — optimized for a great hackathon demo.

### TL;DR (Elevator Pitch)
Biome is your AI form coach. Upload a short workout video; in seconds, Biome flags issues (with frame numbers), scores your form, and suggests focused corrections. It’s like having a coach in your pocket.

### Problem
Most people train without a coach. Poor form causes plateaus and injuries, and current tools don’t give actionable, frame-specific guidance.

### Solution
Biome extracts pose landmarks, computes key joint angles, and produces specific cues and recommendations mapped to severity — fast enough for live demos.

### What’s Novel
- Frame-specific coaching cues tied to quantified joint-angle metrics
- Lightweight, local-first demo flow that works reliably at hackathons
- Schema-first design for results, issues, metrics, and user progress

---

## Features
- **Video upload workflow**: Validates and stores videos locally in `uploads/`
- **Session tracking**: Persists analysis sessions, statuses, and results in PostgreSQL
- **Form insights**: Stores issues, metrics, strengths, and recommendations per session
- **Hackathon-friendly**: Runs locally with sensible defaults; simple demo flow

---

## Judging Criteria Mapping
- **Innovation**: Pose-driven analytics with actionable, timestamped cues; schema designed for longitudinal progress.
- **Technical Execution**: ADK agent pattern, modular tools (`upload_video`, `extract_pose_landmarks`), clean DB layer, reproducible setup.
- **Impact**: Injury prevention, skill progression, and accessibility of coaching.
- **User Experience**: Simple upload → immediate feedback; clear next steps.
- **Feasibility/Scalability**: Extensible to mobile capture, cloud inference, and team dashboards.

---

## Tech Stack
- **Framework**: ADK (Agent Development Kit)
- **Model**: `gemini-2.0-flash`
- **Language**: Python 3.11+
- **Database**: PostgreSQL

---

## Cloud Run Compliance (Hackathon)

This project targets the Cloud Run Hackathon’s AI Agents category and aligns with the listed requirements.

- **Category**: AI Agents — built with Google ADK and deployable to Cloud Run
- **Cloud Run requirement**: Runs as a Cloud Run Service (HTTP). You may also add a Cloud Run Job for batch analysis.
- **Google AI model**: Uses Gemini (`gemini-2.0-flash`).
- **Submission assets**: Hosted URL, 3‑minute demo video, public repository, architecture diagram, English documentation.

### Important Dates (from rules)
- Contest period: Opens Oct 6, 2025; closes Nov 10, 2025 at 5:00 PM PT
- Judging: Nov 10 – Dec 5, 2025
- Winners announced: ~Dec 12, 2025

### Deploy to Cloud Run
Prereqs: gcloud CLI, a Google Cloud project, and Artifact Registry enabled.

```bash
# Build container image
gcloud builds submit --tag "gcr.io/$GOOGLE_CLOUD_PROJECT/biome-agent"

# Deploy to Cloud Run (Service)
gcloud run deploy biome-agent \
  --image "gcr.io/$GOOGLE_CLOUD_PROJECT/biome-agent" \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080

# Set required env vars
gcloud run services update biome-agent \
  --region us-central1 \
  --update-env-vars DATABASE_URL="postgresql://..."
```

Notes:
- For HTTP serving, expose a small FastAPI/ASGI entrypoint or use `adk api_server biome_coaching_agent` wrapped by a server in the container. Ensure the container listens on `$PORT`.
- For batch processing, optionally add a Cloud Run Job that triggers `extract_pose_landmarks` on queued sessions.

### Cloud Run Submission Checklist
- Hosted URL to the running service (include in Devpost)
- Architecture diagram (add to repo: `docs/architecture.png` and reference link below)
- 3‑minute demo video (YouTube/Vimeo, public, English or with English subtitles)
- Public GitHub repository
- Text description: features, tech used, data sources, findings/learnings
- Testing access: if private routes exist, include credentials in submission
- Declare third‑party integrations (MediaPipe/OpenCV)

Architecture diagram placeholder: `docs/architecture.png` (add before submission)

---

## Architecture Overview
- `root_agent` orchestrates a two-step tool flow: upload → pose extraction.
- `upload_video` validates and stores a file, creates an `analysis_sessions` row.
- `extract_pose_landmarks` uses MediaPipe + OpenCV to compute joint angles, aggregates metrics, and returns per-frame data.
- PostgreSQL stores sessions, results, and insights defined in `schema.sql`.

---

## Repository Structure
- `biome_coaching_agent/agent.py`: Root ADK agent (`root_agent`) and tool wiring
- `biome_coaching_agent/tools/upload_video.py`: Video upload + session creation
- `db/connection.py`: PostgreSQL connection utilities
- `schema.sql`: Full database schema + seed data

---

## Prerequisites
- Python 3.11+
- PostgreSQL 14+ running locally
- Windows PowerShell (this repo tested on Windows 10+)

Optional but recommended (per ADK docs):
- `uv` package manager for fast env + dependency management

---

## Quickstart (2 minutes)
```powershell
git clone https://github.com/<your-org>/biome_agent.git
cd biome_agent

# Python env (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt

# Database (psql)
psql -U postgres -c "CREATE DATABASE biome_coaching;"
psql -U postgres -d biome_coaching -f schema.sql

# Optional: point to a non-default DB
$env:DATABASE_URL = "postgresql://<user>:<pass>@<host>:<port>/biome_coaching"

# Run (choose one)
adk web biome_coaching_agent
# or
adk run biome_coaching_agent
```

---

## Setup

### 1) Clone
```bash
git clone https://github.com/<your-org>/biome_agent.git
cd biome_agent
```

### 2) Python environment
Using uv (recommended):
```bash
uv venv --python "python3.11" .venv
.venv\Scripts\activate  # Windows PowerShell
uv pip install -U pip
uv pip install -r requirements.txt  # if you add one
```

Or with plain venv/pip:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
```

### 3) Database
Create a database and apply schema:
```bash
# In psql:
CREATE DATABASE biome_coaching;
\c biome_coaching;
\i schema.sql;
```

Configure connection (optional). By default, the app uses:
```
postgresql://postgres:postgres@localhost:5432/biome_coaching
```

Override via environment variable:
```powershell
$env:DATABASE_URL = "postgresql://<user>:<pass>@<host>:<port>/biome_coaching"
```

---

## Run

This project follows ADK’s agent discovery convention. The root agent lives at `biome_coaching_agent/agent.py` and exports `root_agent`.

Common options:
- ADK Web UI
```bash
adk web biome_coaching_agent
```

- CLI interactive
```bash
adk run biome_coaching_agent
```

- API server
```bash
adk api_server biome_coaching_agent
```

If ADK is not on your PATH, install per ADK docs or run via your environment that includes ADK.

---

## Demo Flow (Hackathon-Friendly)
1) Start the agent (Web UI or CLI)
2) Upload a small test video (≤100MB; supported: .mp4, .mov, .avi, .webm)
3) The agent will:
   - Store the file in `uploads/` with a generated session ID
   - Create an `analysis_sessions` record with status `processing`
   - Proceed with pose extraction and analysis (tooling hooks set up)
4) Review results: issues, metrics, strengths, recommendations are persisted for visualization

Note: The local demo uses simple file copy for uploads and assumes a reachable PostgreSQL.

### 2-Minute Judge Demo Script
1. Open ADK Web: `adk web biome_coaching_agent`
2. Show a test squat video file (10–20s)
3. Upload via the agent UI; show immediate session ID response
4. Trigger `extract_pose_landmarks` on that session
5. Present outputs: total frames, key angle stats, and example cues
6. Explain next-step UI to visualize frame-level issues and progress over time

---

## Configuration
- `DATABASE_URL`: PostgreSQL connection string (optional; has a sensible default)
- Upload directory: created automatically as `uploads/` in project root
- Max upload size: 100MB

---

## Database Schema Highlights
Key tables (see `schema.sql` for details):
- `analysis_sessions`: One per uploaded video/session
- `analysis_results`: Overall score, timing, frame count
- `form_issues`: Issue type, severity, frame range, coaching cue
- `metrics`: Named metric values and targets
- `strengths`, `recommendations`: Positive feedback and next steps

Quick apply from repo root:
```bash
psql -U postgres -d biome_coaching -f schema.sql
```

---

## Development Notes
- Agent defined in `biome_coaching_agent/agent.py` with tools: `upload_video`, `extract_pose_landmarks`
- Database connection helper: `db/connection.py`
- Replace or extend the `extract_pose_landmarks` tool to integrate your CV/ML pipeline

---

## Troubleshooting
- Cannot connect to DB: verify Postgres is running and `DATABASE_URL` is correct.
- `psycopg2` build issues on Windows: `requirements.txt` uses `psycopg2-binary` for convenience.
- Video fails to open: confirm the file path is correct and codec is supported.
- No person detected: try a brighter video, centered subject, and slower movement.

---

## Hackathon Checklist
- Problem, solution, and demo flow documented
- Local run instructions and environment variables
- Database schema and seed data included
- Clear boundaries for future improvements (pose extraction hook)
- License included

---

## Impact and Next Steps
- Reduce injuries and accelerate learning for everyday athletes
- Expand to mobile capture and on-device inference for privacy
- Add visualization UI and coach-mode dashboards
- Integrate with wearables for multi-sensor feedback

---

## Roadmap (Post-hackathon)
- Real pose extraction pipeline integration
- Frontend for video capture and results visualization
- Model evaluation on curated movement datasets
- Mobile capture and privacy-preserving on-device inference

---

## Team
- Biome Team — engineering, ML, product (add names/links here)

---

## License
This project is licensed under the terms of the LICENSE file in this repository.

