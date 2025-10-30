"""
Database connection utilities for PostgreSQL using psycopg2.
Provides a context manager for safe connection acquisition.
"""
import contextlib
import os
from typing import Iterator

import psycopg2


def _get_connection_string() -> str:
  env_url = os.getenv("DATABASE_URL")
  if env_url:
    return env_url
  # Sensible default for local dev
  return "postgresql://postgres:postgres@localhost:5432/biome_coaching"


@contextlib.contextmanager
def get_db_connection() -> Iterator[psycopg2.extensions.connection]:
  """
  Yield a PostgreSQL connection and ensure proper cleanup.
  """
  conn = psycopg2.connect(_get_connection_string())
  try:
    yield conn
    conn.commit()
  except Exception:
    conn.rollback()
    raise
  finally:
    conn.close()


