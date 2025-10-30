"""
Raw SQL query helpers for Biome Coaching Agent.

Phase 1: skeleton only. Filled in during later phases.
"""
from typing import Any, Optional

import psycopg


def ping(conn: psycopg.Connection) -> bool:
  """Simple connectivity check."""
  cur = conn.cursor()
  cur.execute("SELECT 1;")
  row = cur.fetchone()
  return bool(row and row[0] == 1)


# Placeholders for Phase 2/3 implementations
def create_analysis_session(
  conn: psycopg.Connection,
  session_id: str,
  user_id: Optional[str],
  exercise_name: str,
  video_url: str,
  duration: Optional[float],
  file_size: Optional[int],
) -> str:
  cur = conn.cursor()
  cur.execute(
    (
      "INSERT INTO analysis_sessions "
      "(id, user_id, exercise_name, video_url, video_duration, file_size, status, created_at) "
      "VALUES (%s, %s, %s, %s, %s, %s, 'pending', NOW()) RETURNING id"
    ),
    (session_id, user_id, exercise_name, video_url, duration, file_size),
  )
  row = cur.fetchone()
  return row[0]


def get_analysis_session(
  conn: psycopg.Connection,
  session_id: str,
) -> Any:
  cur = conn.cursor()
  cur.execute("SELECT * FROM analysis_sessions WHERE id = %s", (session_id,))
  return cur.fetchone()


def update_session_status(
  conn: psycopg.Connection,
  session_id: str,
  status: str,
  error_message: Optional[str] = None,
) -> None:
  cur = conn.cursor()
  cur.execute(
    "UPDATE analysis_sessions SET status = %s, error_message = %s WHERE id = %s",
    (status, error_message, session_id),
  )


