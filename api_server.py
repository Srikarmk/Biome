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
        "http://localhost:8000",  # Self
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
UPLOADS_DIR = Path("uploads")
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
    """Health check endpoint"""
    try:
        # Test database connection
        with get_db_connection() as conn:
            queries.ping(conn)
        
        return {
            "status": "healthy",
            "service": "biome-coaching-api",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "biome-coaching-api",
                "error": str(e)
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
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Save uploaded file temporarily
        temp_path = UPLOADS_DIR / f"temp_{session_id}_{video.filename}"
        logger.debug(f"Saving uploaded file to temporary location: {temp_path}")
        
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        file_size = temp_path.stat().st_size
        logger.info(f"File saved: {file_size} bytes")
        
        # Step 1: Upload video (copies to permanent location with session_id)
        logger.info(f"Step 1/4: Uploading video for session {session_id}")
        upload_result = upload_video(
            video_file_path=str(temp_path),
            exercise_name=exercise_name,
            user_id=user_id,
        )
        
        # Clean up temp file
        if temp_path and temp_path.exists():
            temp_path.unlink()
            logger.debug("Temporary file cleaned up")
        
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
        # Clean up temp file on error
        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
        
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
        session_id: The analysis session ID
    
    Returns:
        Complete analysis results if available
    """
    try:
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
        session_id: The analysis session ID
    
    Returns:
        Session details including status
    """
    try:
        logger.debug(f"Fetching session info for {session_id}")
        
        with get_db_connection() as conn:
            session_row = queries.get_analysis_session(conn, session_id)
        
        if not session_row:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Parse the row (structure: id, user_id, exercise_id, exercise_name, video_url, ...)
        return JSONResponse({
            "session_id": str(session_row[0]),
            "user_id": str(session_row[1]) if session_row[1] else None,
            "exercise_name": session_row[3],
            "video_url": session_row[4],
            "status": session_row[6],
            "created_at": session_row[7].isoformat() if session_row[7] else None,
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching session {session_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Configure server
    # Cloud Run uses PORT env var (defaults to 8080)
    # For local dev, can override with PORT=8000
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    logger.info(f"Starting Biome Coaching API server on {host}:{port}")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

