"""
Form analysis tool for Biome Coaching Agent.

Analyzes pose data and generates coaching feedback with specific cues,
severity scores, and actionable recommendations. Focuses on squat analysis
for hackathon MVP.
"""
from typing import Any, Dict, List

from google.adk.tools.tool_context import ToolContext
from biome_coaching_agent.logging_config import get_logger  # type: ignore
from biome_coaching_agent.exceptions import AnalysisError, ValidationError  # type: ignore

# Initialize logger
logger = get_logger(__name__)


def _calculate_squat_score(metrics: Dict[str, Any], frames: List[Dict[str, Any]]) -> float:
  """Calculate overall form score (0-10) for squat exercise."""
  score = 10.0  # Start with perfect score
  penalties: List[float] = []

  # Check depth: min_knee_angle < 90° is good depth
  min_knee_angle = min(
    metrics.get("left_knee_min", 180),
    metrics.get("right_knee_min", 180)
  )
  if min_knee_angle > 110:
    # Insufficient depth
    penalty = min((min_knee_angle - 90) / 20, 3.0)  # Max 3 point penalty
    penalties.append(penalty)
  elif min_knee_angle < 70:
    # Excessive depth (potential knee strain)
    penalty = (70 - min_knee_angle) / 10
    penalties.append(min(penalty, 1.5))

  # Check knee alignment - asymmetry penalty
  avg_left_knee = metrics.get("left_knee_avg", 180)
  avg_right_knee = metrics.get("right_knee_avg", 180)
  asymmetry = abs(avg_left_knee - avg_right_knee)
  if asymmetry > 15:
    penalties.append(min(asymmetry / 15 * 1.5, 2.0))

  # Check hip hinge - should maintain ~180° at top
  avg_hip = (metrics.get("left_hip_avg", 180) + metrics.get("right_hip_avg", 180)) / 2
  if avg_hip < 150:
    # Excessive forward lean
    penalties.append(min((150 - avg_hip) / 20, 2.0))

  # Apply penalties
  total_penalty = sum(penalties)
  final_score = max(0.0, score - total_penalty)

  return round(final_score, 1)


def _identify_squat_issues(
  metrics: Dict[str, Any],
  frames: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
  """Identify specific form issues with severity and frame ranges."""
  issues: List[Dict[str, Any]] = []

  min_knee_angle = min(
    metrics.get("left_knee_min", 180),
    metrics.get("right_knee_min", 180)
  )

  # Issue 1: Insufficient depth
  if min_knee_angle > 100:
    severity = "severe" if min_knee_angle > 120 else "moderate"
    frame_start = 0
    frame_end = len(frames) - 1
    # Find frames where knee angle is problematic
    for i, frame_data in enumerate(frames):
      angles = frame_data.get("angles", {})
      knee_avg = (angles.get("left_knee", 180) + angles.get("right_knee", 180)) / 2
      if knee_avg > 100:
        frame_start = min(frame_start, frame_data.get("frame", i))
        frame_end = max(frame_end, frame_data.get("frame", i))

    issues.append({
      "issue_type": "Insufficient Squat Depth",
      "severity": severity,
      "frame_start": frame_start,
      "frame_end": frame_end,
      "coaching_cue": (
        f"Lower your hips until your thighs are parallel to the floor "
        f"(target knee angle < 90°). Currently reaching {min_knee_angle:.0f}°. "
        "Focus on pushing your hips back and down, not just your knees forward."
      ),
      "confidence_score": 0.85,
    })

  # Issue 2: Knee valgus (knees caving inward)
  avg_left_knee = metrics.get("left_knee_avg", 180)
  avg_right_knee = metrics.get("right_knee_avg", 180)
  asymmetry = abs(avg_left_knee - avg_right_knee)
  if asymmetry > 15:
    severity = "severe" if asymmetry > 25 else "moderate"
    # Find asymmetric frames
    problematic_frames = [
      f.get("frame", 0)
      for f in frames
      if abs(f.get("angles", {}).get("left_knee", 180) - f.get("angles", {}).get("right_knee", 180)) > 15
    ]
    frame_start = min(problematic_frames) if problematic_frames else 0
    frame_end = max(problematic_frames) if problematic_frames else len(frames) - 1

    issues.append({
      "issue_type": "Knee Asymmetry/Valgus",
      "severity": severity,
      "frame_start": frame_start,
      "frame_end": frame_end,
      "coaching_cue": (
        f"Keep both knees aligned. You have {asymmetry:.0f}° difference between legs. "
        "Push your knees outward to track over your toes. Focus on engaging your glutes."
      ),
      "confidence_score": 0.75,
    })

  # Issue 3: Excessive forward lean (hip angle too closed)
  avg_hip = (metrics.get("left_hip_avg", 180) + metrics.get("right_hip_avg", 180)) / 2
  if avg_hip < 145:
    severity = "severe" if avg_hip < 135 else "moderate"
    frame_start = 0
    frame_end = len(frames) - 1

    issues.append({
      "issue_type": "Excessive Forward Lean",
      "severity": severity,
      "frame_start": frame_start,
      "frame_end": frame_end,
      "coaching_cue": (
        f"Maintain a more upright torso. Your hip angle is {avg_hip:.0f}° (target > 150°). "
        "Keep your chest up, core braced, and focus on sitting back into the squat."
      ),
      "confidence_score": 0.70,
    })

  return issues


def _generate_metrics(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
  """Generate metric comparisons (actual vs target)."""
  metric_list: List[Dict[str, Any]] = []

  # Knee depth metric
  min_knee = min(metrics.get("left_knee_min", 180), metrics.get("right_knee_min", 180))
  metric_list.append({
    "metric_name": "Knee Flexion (Depth)",
    "actual_value": f"{min_knee:.0f}°",
    "target_value": "< 90°",
    "status": "good" if min_knee < 95 else ("warning" if min_knee < 110 else "error"),
  })

  # Knee symmetry metric
  asymmetry = abs(metrics.get("left_knee_avg", 180) - metrics.get("right_knee_avg", 180))
  metric_list.append({
    "metric_name": "Knee Symmetry",
    "actual_value": f"{asymmetry:.0f}° difference",
    "target_value": "< 10°",
    "status": "good" if asymmetry < 10 else ("warning" if asymmetry < 20 else "error"),
  })

  # Hip angle metric
  avg_hip = (metrics.get("left_hip_avg", 180) + metrics.get("right_hip_avg", 180)) / 2
  metric_list.append({
    "metric_name": "Hip Angle (Torso Position)",
    "actual_value": f"{avg_hip:.0f}°",
    "target_value": "> 150°",
    "status": "good" if avg_hip > 155 else ("warning" if avg_hip > 145 else "error"),
  })

  return metric_list


def _generate_strengths(metrics: Dict[str, Any], issues: List[Dict[str, Any]]) -> List[str]:
  """Generate positive feedback for correct form elements."""
  strengths: List[str] = []

  min_knee = min(metrics.get("left_knee_min", 180), metrics.get("right_knee_min", 180))
  if min_knee < 95:
    strengths.append("Excellent squat depth! You're achieving proper range of motion.")

  asymmetry = abs(metrics.get("left_knee_avg", 180) - metrics.get("right_knee_avg", 180))
  if asymmetry < 10:
    strengths.append("Great knee alignment and symmetry throughout the movement.")

  if not issues:
    strengths.append("Outstanding form! Keep up the excellent technique.")

  if not strengths:
    strengths.append("Good effort! Focus on the cues below to improve your form.")

  return strengths


def _generate_recommendations(
  issues: List[Dict[str, Any]],
  overall_score: float,
) -> List[Dict[str, Any]]:
  """Generate improvement recommendations."""
  recommendations: List[Dict[str, Any]] = []

  if overall_score < 6.0:
    recommendations.append({
      "recommendation_text": (
        "Practice bodyweight squats with a focus on proper form before adding weight. "
        "Use a mirror or video feedback to monitor your technique."
      ),
      "priority": 1,
    })

  has_depth_issue = any("Depth" in issue.get("issue_type", "") for issue in issues)
  if has_depth_issue:
    recommendations.append({
      "recommendation_text": (
        "Work on hip mobility and ankle flexibility to improve squat depth. "
        "Consider exercises like goblet squats to practice the movement pattern."
      ),
      "priority": 2,
    })

  has_valgus = any("Valgus" in issue.get("issue_type", "") or "Asymmetry" in issue.get("issue_type", "") for issue in issues)
  if has_valgus:
    recommendations.append({
      "recommendation_text": (
        "Strengthen your glutes and hip abductors with exercises like clamshells, "
        "lateral band walks, and hip thrusts to prevent knee caving."
      ),
      "priority": 2,
    })

  if overall_score >= 8.0:
    recommendations.append({
      "recommendation_text": "Your form is solid! Consider gradually increasing load or adding variations like pause squats.",
      "priority": 3,
    })

  return recommendations


def analyze_workout_form(
  pose_data: dict,
  exercise_name: str,
  tool_context: ToolContext = None,
) -> dict:
  """
  Analyze workout form from pose data and generate coaching feedback.

  Args:
    pose_data: Dictionary containing pose extraction results:
      {
        "status": "success",
        "total_frames": int,
        "metrics": {left_knee_avg, left_knee_min, ...},
        "frames": [{frame, landmarks, angles}, ...]
      }
    exercise_name: Name of exercise (e.g., "Squat")
    tool_context: ADK tool context (unused).

  Returns:
    dict: {
      status: "success" | "error",
      overall_score: float (0-10),
      total_frames: int,
      issues: [{issue_type, severity, frame_start, frame_end, coaching_cue, confidence_score}, ...],
      metrics: [{metric_name, actual_value, target_value, status}, ...],
      strengths: [str, ...],
      recommendations: [{recommendation_text, priority}, ...],
    } or {status, error_type, message} on error
  """
  logger.info(f"Starting form analysis - exercise: {exercise_name}")
  
  try:
    # Validate pose data status
    if pose_data.get("status") != "success":
      error_msg = pose_data.get("message", "Pose data extraction failed")
      logger.error(f"Pose data invalid: {error_msg}")
      raise ValidationError(f"Invalid pose data: {error_msg}")

    # Validate exercise is supported
    if exercise_name.lower() not in ["squat", "squats"]:
      logger.warning(f"Unsupported exercise requested: {exercise_name}")
      raise ValidationError(
        f"Exercise '{exercise_name}' not yet supported. Currently only 'Squat' is available."
      )

    metrics = pose_data.get("metrics", {})
    frames = pose_data.get("frames", [])

    if not frames:
      logger.error("No frame data available for analysis")
      raise ValidationError("No frame data available for analysis")
    
    logger.debug(f"Analyzing {len(frames)} frames with metrics: {list(metrics.keys())}")

    # Calculate overall score
    overall_score = _calculate_squat_score(metrics, frames)
    logger.debug(f"Overall score calculated: {overall_score}/10")

    # Identify issues
    issues = _identify_squat_issues(metrics, frames)
    logger.debug(f"Identified {len(issues)} form issues")

    # Generate metrics
    metrics_list = _generate_metrics(metrics)

    # Generate strengths
    strengths = _generate_strengths(metrics, issues)
    logger.debug(f"Generated {len(strengths)} strengths")

    # Generate recommendations
    recommendations = _generate_recommendations(issues, overall_score)
    logger.debug(f"Generated {len(recommendations)} recommendations")

    logger.info(
      f"Form analysis complete - exercise: {exercise_name}, "
      f"score: {overall_score}/10, issues: {len(issues)}, "
      f"strengths: {len(strengths)}"
    )

    return {
      "status": "success",
      "overall_score": overall_score,
      "total_frames": pose_data.get("total_frames", len(frames)),
      "issues": issues,
      "metrics": metrics_list,
      "strengths": strengths,
      "recommendations": recommendations,
    }
  
  except ValidationError as ve:
    logger.warning(f"Validation error during analysis: {ve}")
    return {
      "status": "error",
      "error_type": "validation",
      "message": str(ve)
    }
  
  except Exception as e:
    logger.critical(f"Unexpected error during form analysis: {e}", exc_info=True)
    return {
      "status": "error",
      "error_type": "unknown",
      "message": f"Analysis failed: {str(e)}"
    }

