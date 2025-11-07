"""
Custom API server for Biome Coaching Agent with video upload support.
Wraps the ADK agent and provides REST endpoints for the React frontend.
"""
import os
import uuid
import shutil
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import ADK agent and tools
from biome_coaching_agent.config import settings
from biome_coaching_agent.tools.upload_video import upload_video
from biome_coaching_agent.tools.extract_pose_landmarks import extract_pose_landmarks
from biome_coaching_agent.tools.analyze_workout_form import analyze_workout_form
from biome_coaching_agent.tools.save_analysis_results import save_analysis_results
from biome_coaching_agent.logging_config import get_logger
from biome_coaching_agent.exceptions import (
    ValidationError,
    DatabaseError,
    PoseExtractionError,
    AnalysisError,
)
from db.connection import get_db_connection
from db import queries

# Initialize logger
logger = get_logger(__name__)

# Validate configuration on startup
try:
    settings.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.critical(f"Configuration validation failed: {e}")
    raise

app = FastAPI(
    title="Biome Coaching API",
    description="AI-powered fitness form coaching API",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",  # React dev server (alternate port)
        "http://localhost:8080",  # React on 8080
        "http://localhost:8081",  # React on 8081
        "http://localhost:8000",  # Self
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Only methods we use
    allow_headers=["Content-Type", "Accept", "Authorization"],  # Only necessary headers
)

# Ensure uploads directory exists
UPLOADS_DIR = Path(settings.uploads_dir)
UPLOADS_DIR.mkdir(exist_ok=True)
logger.info(f"Uploads directory: {UPLOADS_DIR.absolute()}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "biome-coaching-api",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/analyze",
            "results": "/api/results/{session_id}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with dependency verification"""
    checks = {}
    overall_healthy = True
    
    # Check database
    try:
        with get_db_connection() as conn:
            queries.ping(conn)
        checks["database"] = "connected"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        overall_healthy = False
        logger.error(f"Health check - database failed: {e}")
    
    # Check MediaPipe availability
    try:
        import mediapipe
        checks["mediapipe"] = "available"
    except ImportError as e:
        checks["mediapipe"] = f"missing: {str(e)}"
        overall_healthy = False
        logger.error(f"Health check - MediaPipe missing: {e}")
    
    # Check uploads directory writable
    try:
        test_file = UPLOADS_DIR / ".health_check"
        test_file.touch()
        test_file.unlink()
        checks["storage"] = "writable"
    except Exception as e:
        checks["storage"] = f"error: {str(e)}"
        overall_healthy = False
        logger.error(f"Health check - storage failed: {e}")
    
    # Check Gemini API key configured
    checks["gemini_key"] = "configured" if settings.google_api_key else "missing"
    if not settings.google_api_key:
        overall_healthy = False
    
    status_code = 200 if overall_healthy else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if overall_healthy else "unhealthy",
            "service": "biome-coaching-api",
            "checks": checks
        }
    )


@app.post("/api/analyze")
async def analyze_video_endpoint(
    video: UploadFile = File(...),
    exercise_name: str = Form(...),
    user_id: Optional[str] = Form(None),
):
    """
    Upload and analyze a workout video.
    
    This endpoint orchestrates the full analysis workflow:
    1. Saves the uploaded video
    2. Runs pose extraction using MediaPipe
    3. Analyzes form using Gemini AI
    4. Saves results to database
    5. Returns complete analysis
    
    Args:
        video: Uploaded video file
        exercise_name: Name of exercise being performed
        user_id: Optional user identifier
    
    Returns:
        Complete analysis results with issues, metrics, strengths, and recommendations
    """
    start_time = time.time()
    temp_path = None
    
    try:
        logger.info(
            f"Analysis request received - exercise: {exercise_name}, "
            f"user_id: {user_id}, filename: {video.filename}"
        )
        
        # Validation: File type
        if not video.content_type or not video.content_type.startswith('video/'):
            raise HTTPException(
                status_code=400,
                detail={"error": "File must be a video (mp4, mov, avi, webm)", "step": "validation"}
            )
        
        # Validation: Read file size
        video.file.seek(0, 2)  # Seek to end
        file_size_bytes = video.file.tell()
        video.file.seek(0)  # Reset to beginning
        
        # Validation: Empty file
        if file_size_bytes == 0:
            raise HTTPException(
                status_code=400,
                detail={"error": "File is empty", "step": "validation"}
            )
        
        # Validation: File too small (likely corrupted)
        if file_size_bytes < 1024:  # 1KB minimum
            raise HTTPException(
                status_code=400,
                detail={"error": "File too small (minimum 1KB)", "step": "validation"}
            )
        
        # Validation: File too large
        max_size = 100 * 1024 * 1024  # 100MB
        if file_size_bytes > max_size:
            size_mb = file_size_bytes / (1024 * 1024)
            raise HTTPException(
                status_code=413,
                detail={"error": f"File too large: {size_mb:.1f}MB (max 100MB)", "step": "validation"}
            )
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Save uploaded file temporarily
        # SECURITY: Use only session_id, ignore user-provided filename to prevent path traversal
        safe_ext = Path(video.filename).suffix.lower() if video.filename else ".tmp"
        temp_path = UPLOADS_DIR / f"temp_{session_id}{safe_ext}"
        logger.debug(f"Saving uploaded file to temporary location: {temp_path}")
        
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        file_size = temp_path.stat().st_size
        logger.info(f"File saved: {file_size} bytes")
        
        try:
            # Step 1: Upload video (copies to permanent location with session_id)
            logger.info(f"Step 1/4: Uploading video for session {session_id}")
            upload_result = upload_video(
                video_file_path=str(temp_path),
                exercise_name=exercise_name,
                user_id=user_id,
            )
            
            if upload_result.get("status") != "success":
                error_msg = upload_result.get("message", "Upload failed")
                error_type = upload_result.get("error_type", "unknown")
                logger.error(f"Upload failed: {error_msg} (type: {error_type})")
                raise HTTPException(
                    status_code=400 if error_type == "validation" else 500,
                    detail={
                        "error": error_msg,
                        "error_type": error_type,
                        "step": "upload"
                    }
                )
        finally:
            # Always cleanup temp file
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                    logger.debug("Temporary file cleaned up")
                except Exception as cleanup_err:
                    logger.warning(f"Failed to cleanup temp file: {cleanup_err}")
        
        session_id = upload_result["session_id"]
        logger.info(f"Video uploaded successfully, session_id: {session_id}")
        
        # Step 2: Extract pose landmarks
        logger.info(f"Step 2/4: Extracting pose landmarks for session {session_id}")
        pose_result = extract_pose_landmarks(session_id=session_id, fps=10)
        
        if pose_result.get("status") != "success":
            error_msg = pose_result.get("message", "Pose extraction failed")
            logger.error(f"Pose extraction failed: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Pose extraction failed: {error_msg}",
                    "step": "pose_extraction",
                    "session_id": session_id
                }
            )
        
        logger.info(
            f"Pose extraction complete: {pose_result.get('total_frames', 0)} frames processed"
        )
        
        # Step 3: Analyze form
        logger.info(f"Step 3/4: Analyzing form for session {session_id}")
        analysis_result = analyze_workout_form(
            pose_data=pose_result,
            exercise_name=exercise_name,
        )
        
        if analysis_result.get("status") != "success":
            error_msg = analysis_result.get("message", "Analysis failed")
            logger.error(f"Form analysis failed: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Analysis failed: {error_msg}",
                    "step": "analysis",
                    "session_id": session_id
                }
            )
        
        logger.info(
            f"Form analysis complete: score {analysis_result.get('overall_score')}/10, "
            f"{len(analysis_result.get('issues', []))} issues found"
        )
        
        # Step 4: Save results to database
        logger.info(f"Step 4/4: Saving results for session {session_id}")
        save_result = save_analysis_results(
            session_id=session_id,
            analysis_data=analysis_result,
        )
        
        if save_result.get("status") != "success":
            error_msg = save_result.get("message", "Failed to save results")
            logger.error(f"Save results failed: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Failed to save results: {error_msg}",
                    "step": "save_results",
                    "session_id": session_id
                }
            )
        
        processing_time = time.time() - start_time
        logger.info(
            f"Analysis complete for session {session_id} in {processing_time:.2f}s"
        )
        
        # Return complete analysis
        return JSONResponse({
            "status": "success",
            "session_id": session_id,
            "result_id": save_result.get("result_id"),
            "overall_score": analysis_result.get("overall_score"),
            "total_frames": analysis_result.get("total_frames"),
            "processing_time": round(processing_time, 2),
            "issues": analysis_result.get("issues", []),
            "metrics": analysis_result.get("metrics", []),
            "strengths": analysis_result.get("strengths", []),
            "recommendations": analysis_result.get("recommendations", []),
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected error in analyze endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Internal server error: {str(e)}",
                "step": "unknown"
            }
        )


@app.get("/api/results/{session_id}")
async def get_results(session_id: str):
    """
    Get analysis results for a session.
    
    Args:
        session_id: The analysis session ID (UUID format)
    
    Returns:
        Complete analysis results if available
    """
    try:
        # Validate UUID format
        try:
            uuid.UUID(session_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid session_id format (must be UUID)"
            )
        
        logger.info(f"Fetching results for session {session_id}")
        
        with get_db_connection() as conn:
            result = queries.get_analysis_result_by_session(conn, session_id)
        
        if not result:
            logger.warning(f"No results found for session {session_id}")
            raise HTTPException(
                status_code=404,
                detail="Results not found for this session"
            )
        
        logger.info(f"Results retrieved successfully for session {session_id}")
        return JSONResponse(result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching results for session {session_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve results: {str(e)}"
        )


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get session information including status.
    
    Args:
        session_id: The analysis session ID (UUID format)
    
    Returns:
        Session details including status
    """
    try:
        # Validate UUID format
        try:
            uuid.UUID(session_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid session_id format (must be UUID)"
            )
        
        logger.debug(f"Fetching session info for {session_id}")
        
        with get_db_connection() as conn:
            session_row = queries.get_analysis_session(conn, session_id)
        
        if not session_row:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Parse the row with explicit indices (matches SELECT order in queries.py)
        # Order: id, user_id, exercise_id, exercise_name, video_url, video_duration, status, created_at, started_at, completed_at, error_message
        return JSONResponse({
            "session_id": str(session_row[0]),  # id
            "user_id": str(session_row[1]) if session_row[1] else None,  # user_id
            "exercise_name": session_row[3],  # exercise_name
            "video_url": session_row[4],  # video_url
            "status": session_row[6],  # status
            "created_at": session_row[7].isoformat() if session_row[7] else None,  # created_at
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching session {session_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Configure server using centralized settings
    logger.info(f"Starting Biome Coaching API server on {settings.host}:{settings.port}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Database: {settings.database_url.split('@')[-1] if '@' in settings.database_url else 'configured'}")
    
    uvicorn.run(
        "api_server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level
    )

