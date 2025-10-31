"""
Save analysis results tool for Biome Coaching Agent.

Persists complete analysis results to PostgreSQL database including
form issues, metrics, strengths, and recommendations.
"""
import time
from typing import Any, Dict

from google.adk.tools.tool_context import ToolContext

from db.connection import get_db_connection  # type: ignore
from db import queries  # type: ignore


def save_analysis_results(
  session_id: str,
  analysis_data: dict,
  tool_context: ToolContext = None,
) -> dict:
  """
  Save complete analysis results to database.

  Args:
    session_id: Analysis session ID.
    analysis_data: Dictionary containing analysis results:
      {
        "overall_score": float (0-10),
        "total_frames": int,
        "issues": [{issue_type, severity, frame_start, frame_end, coaching_cue, confidence_score}, ...],
        "metrics": [{metric_name, actual_value, target_value, status}, ...],
        "strengths": [str, ...],
        "recommendations": [{recommendation_text, priority}, ...],
      }
    tool_context: ADK tool context (unused).

  Returns:
    dict: {status: "success" | "error", result_id: str, message: str}
  """
  try:
    if analysis_data.get("status") != "success":
      return {"status": "error", "message": "Analysis data indicates failure"}

    overall_score = analysis_data.get("overall_score", 0.0)
    total_frames = analysis_data.get("total_frames", 0)
    processing_time = analysis_data.get("processing_time", None)

    issues = analysis_data.get("issues", [])
    metrics_list = analysis_data.get("metrics", [])
    strengths = analysis_data.get("strengths", [])
    recommendations = analysis_data.get("recommendations", [])

    # Record processing time if not provided
    if processing_time is None:
      processing_time = 0.0  # Default, could track start/end in future

    with get_db_connection() as conn:
      # Create analysis result record
      result_id = queries.create_analysis_result(
        conn=conn,
        session_id=session_id,
        overall_score=overall_score,
        total_frames=total_frames,
        processing_time=processing_time,
      )

      # Save form issues
      for issue in issues:
        queries.create_form_issue(
          conn=conn,
          result_id=result_id,
          issue_type=issue.get("issue_type", "Unknown Issue"),
          severity=issue.get("severity", "moderate"),
          frame_start=issue.get("frame_start", 0),
          frame_end=issue.get("frame_end", 0),
          coaching_cue=issue.get("coaching_cue", ""),
          confidence_score=issue.get("confidence_score"),
        )

      # Save metrics
      for metric in metrics_list:
        queries.create_metric(
          conn=conn,
          result_id=result_id,
          metric_name=metric.get("metric_name", "Unknown"),
          actual_value=metric.get("actual_value", ""),
          target_value=metric.get("target_value", ""),
          status=metric.get("status", "warning"),
        )

      # Save strengths
      for strength_text in strengths:
        queries.create_strength(
          conn=conn,
          result_id=result_id,
          strength_text=strength_text,
        )

      # Save recommendations
      for rec in recommendations:
        queries.create_recommendation(
          conn=conn,
          result_id=result_id,
          recommendation_text=rec.get("recommendation_text", ""),
          priority=rec.get("priority", 1),
        )

      # Update session status to completed
      queries.update_session_status(conn, session_id, "completed", None)

      # Commit transaction (handled by context manager)

    return {
      "status": "success",
      "result_id": result_id,
      "message": f"Saved analysis results: {len(issues)} issues, {len(metrics_list)} metrics, {len(strengths)} strengths",
    }
  except Exception as e:
    # Update session status to failed on error
    try:
      with get_db_connection() as conn:
        queries.update_session_status(conn, session_id, "failed", str(e))
    except Exception:
      pass  # Ignore errors during error handling

    return {"status": "error", "message": f"Failed to save results: {str(e)}"}

