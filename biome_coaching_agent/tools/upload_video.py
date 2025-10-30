"""
Video upload tool for Biome Coaching Agent.

Validates the file and creates an analysis session record.
For hackathon/local dev, this copies to a local `uploads/` directory.
"""
import os
import shutil
import uuid
from datetime import datetime
from typing import Optional

from google.adk.tools.tool_context import ToolContext

from db.connection import get_db_connection  # type: ignore
from db import queries  # type: ignore


ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".webm"}
MAX_MB = 100


def _ensure_uploads_dir() -> str:
  uploads_dir = os.path.join(os.getcwd(), "uploads")
  os.makedirs(uploads_dir, exist_ok=True)
  return uploads_dir


def upload_video(
  video_file_path: str,
  exercise_name: str,
  user_id: Optional[str] = None,
  tool_context: ToolContext = None,
) -> dict:
  """
  Store the workout video and create an analysis session.

  Args:
    video_file_path: Absolute or relative path to the source video file.
    exercise_name: Name of the exercise (e.g., "Squat").
    user_id: Optional user id (None for demo mode).
    tool_context: ADK tool context (unused).

  Returns:
    dict: {status, session_id, video_url}
  """
  try:
    if not os.path.isfile(video_file_path):
      return {"status": "error", "message": "Video file not found"}

    ext = os.path.splitext(video_file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
      return {"status": "error", "message": f"Unsupported file type: {ext}"}

    file_size_bytes = os.path.getsize(video_file_path)
    if file_size_bytes > MAX_MB * 1024 * 1024:
      return {"status": "error", "message": "File exceeds 100MB limit"}

    uploads_dir = _ensure_uploads_dir()
    session_id = str(uuid.uuid4())
    dest_filename = f"{session_id}{ext}"
    dest_path = os.path.join(uploads_dir, dest_filename)
    shutil.copy2(video_file_path, dest_path)

    # Best effort mime type guess
    mime_type = {
      ".mp4": "video/mp4",
      ".mov": "video/quicktime",
      ".avi": "video/x-msvideo",
      ".webm": "video/webm",
    }.get(ext, "application/octet-stream")

    with get_db_connection() as conn:
      queries.create_analysis_session(
        conn=conn,
        session_id=session_id,
        user_id=user_id,
        exercise_name=exercise_name,
        video_url=dest_path,
        duration=None,
        file_size=file_size_bytes,
      )
      queries.update_session_status(conn, session_id, "processing")

    return {"status": "success", "session_id": session_id, "video_url": dest_path}
  except Exception as e:
    return {"status": "error", "message": str(e)}


