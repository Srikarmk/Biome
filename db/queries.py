"""
Raw SQL query helpers for Biome Coaching Agent.

Phase 1: skeleton only. Filled in during later phases.
"""
from typing import Any, Optional

import psycopg2


def ping(conn: psycopg2.extensions.connection) -> bool:
  """Simple connectivity check."""
  cur = conn.cursor()
  cur.execute("SELECT 1;")
  row = cur.fetchone()
  return bool(row and row[0] == 1)


# Placeholders for Phase 2/3 implementations
def create_analysis_session(
  conn: psycopg2.extensions.connection,
  session_id: str,
  user_id: Optional[str],
  exercise_name: str,
  video_url: str,
  duration: Optional[float],
  file_size: Optional[int],
) -> str:
  raise NotImplementedError


def get_analysis_session(
  conn: psycopg2.extensions.connection,
  session_id: str,
) -> Any:
  raise NotImplementedError


def update_session_status(
  conn: psycopg2.extensions.connection,
  session_id: str,
  status: str,
  error_message: Optional[str] = None,
) -> None:
  raise NotImplementedError


