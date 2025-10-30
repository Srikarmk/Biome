"""
Pose extraction tool using MediaPipe.

Processes the stored video at a reduced FPS to extract 33 pose landmarks
and computes simple joint angle metrics for hackathon demo.
"""
from typing import Any, Dict, List, Optional

import cv2  # type: ignore
import numpy as np  # type: ignore

from google.adk.tools.tool_context import ToolContext

from db.connection import get_db_connection  # type: ignore
from db import queries  # type: ignore


def _angle_between(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
  """Compute angle at p2 formed by p1-p2-p3 in degrees."""
  v1 = p1 - p2
  v2 = p3 - p2
  denom = (np.linalg.norm(v1) * np.linalg.norm(v2)) + 1e-8
  cosang = float(np.clip(np.dot(v1, v2) / denom, -1.0, 1.0))
  return float(np.degrees(np.arccos(cosang)))


def _calc_joint_angles(landmarks: List[Dict[str, float]]) -> Dict[str, float]:
  """Calculate a few representative angles (knee and hip)."""
  # MediaPipe indices: hip 24/23, knee 26/25, ankle 28/27
  def lp(idx: int) -> np.ndarray:
    lm = landmarks[idx]
    return np.array([lm["x"], lm["y"]], dtype=np.float32)

  left_knee = _angle_between(lp(23), lp(25), lp(27))
  right_knee = _angle_between(lp(24), lp(26), lp(28))
  # Hip angle: shoulder-hip-knee approximation using 12/11, 24/23, 26/25
  left_hip = _angle_between(lp(11), lp(23), lp(25))
  right_hip = _angle_between(lp(12), lp(24), lp(26))
  return {
    "left_knee": left_knee,
    "right_knee": right_knee,
    "left_hip": left_hip,
    "right_hip": right_hip,
  }


def _aggregate_metrics(angle_series: List[Dict[str, float]]) -> Dict[str, Any]:
  keys = angle_series[0].keys() if angle_series else []
  agg: Dict[str, Any] = {"count": len(angle_series)}
  for k in keys:
    vals = np.array([frame[k] for frame in angle_series], dtype=np.float32)
    agg[f"{k}_avg"] = float(np.mean(vals))
    agg[f"{k}_min"] = float(np.min(vals))
    agg[f"{k}_max"] = float(np.max(vals))
  return agg


def extract_pose_landmarks(
  session_id: str,
  fps: int = 10,
  tool_context: ToolContext = None,
) -> dict:
  """
  Extract pose landmarks and joint angles for a given session's video.

  Args:
    session_id: Analysis session id whose video will be processed.
    fps: Target processing fps for speed.
    tool_context: ADK tool context (unused).

  Returns:
    dict: {status, detected_exercise, total_frames, metrics, frames}
  """
  try:
    with get_db_connection() as conn:
      row = queries.get_analysis_session(conn, session_id)
    if not row:
      return {"status": "error", "message": "Session not found"}

    # Row layout depends on cursor factory; safest is to lookup by column order
    # Assuming video_url is 4th or 5th; fallback to last non-null text
    video_url = None
    for col in row:
      if isinstance(col, str) and ("/" in col or "\\" in col) and (col.endswith(".mp4") or col.endswith(".mov") or col.endswith(".avi") or col.endswith(".webm")):
        video_url = col
        break
    if not video_url:
      return {"status": "error", "message": "Video path not found in session"}

    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
      return {"status": "error", "message": "Failed to open video"}

    native_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_interval = max(int(round(native_fps / max(fps, 1))), 1)

    # Lazy import MediaPipe to avoid global import-time protobuf version conflicts
    try:
      import mediapipe as mp  # type: ignore
    except Exception as imp_err:
      return {"status": "error", "message": f"Failed to import MediaPipe: {imp_err}"}

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(model_complexity=1)

    frames: List[Dict[str, Any]] = []
    angle_series: List[Dict[str, float]] = []
    idx = 0
    while True:
      ret, frame = cap.read()
      if not ret:
        break
      if idx % frame_interval != 0:
        idx += 1
        continue

      rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      res = pose.process(rgb)
      if not res.pose_landmarks:
        idx += 1
        continue

      lm_list: List[Dict[str, float]] = []
      for lm in res.pose_landmarks.landmark:
        lm_list.append({"x": float(lm.x), "y": float(lm.y), "z": float(lm.z)})

      angles = _calc_joint_angles(lm_list)
      angle_series.append(angles)
      frames.append({"frame": idx, "landmarks": lm_list, "angles": angles})
      idx += 1

    cap.release()
    pose.close()

    if not frames:
      return {"status": "error", "message": "No person detected in video"}

    metrics = _aggregate_metrics(angle_series)

    return {
      "status": "success",
      "detected_exercise": "Squat",  # hackathon simplification
      "total_frames": len(frames),
      "metrics": metrics,
      "frames": frames,
    }
  except Exception as e:
    return {"status": "error", "message": str(e)}


