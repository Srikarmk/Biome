"""
Database connection utilities for PostgreSQL using psycopg (v3).
Provides a context manager for safe connection acquisition.
"""
import contextlib
import os
from typing import Iterator

import psycopg

# Import logger - avoid circular import by importing locally if needed
try:
  from biome_coaching_agent.logging_config import get_logger
  logger = get_logger(__name__)
except ImportError:
  # Fallback to basic logging if biome_coaching_agent not available
  import logging
  logger = logging.getLogger(__name__)


def _get_connection_string() -> str:
  """Get database connection string from environment or use default."""
  env_url = os.getenv("DATABASE_URL")
  if env_url:
    logger.debug("Using DATABASE_URL from environment")
    return env_url
  # Sensible default for local dev
  logger.debug("Using default database connection string")
  return "postgresql://postgres:postgres@localhost:5432/biome_coaching"


@contextlib.contextmanager
def get_db_connection() -> Iterator[psycopg.Connection]:
  """
  Yield a PostgreSQL connection and ensure proper cleanup.
  
  Handles commit/rollback automatically and ensures connection is closed.
  
  Yields:
    psycopg.Connection: Database connection
    
  Raises:
    psycopg.Error: Database connection or operation failed
  """
  conn_string = _get_connection_string()
  logger.debug("Establishing database connection")
  
  try:
    conn = psycopg.connect(conn_string)
    logger.debug("Database connection established")
  except psycopg.Error as conn_err:
    logger.error(f"Failed to connect to database: {conn_err}", exc_info=True)
    raise
  
  try:
    yield conn
    conn.commit()
    logger.debug("Database transaction committed")
  except Exception as e:
    conn.rollback()
    logger.warning(f"Database transaction rolled back due to error: {e}")
    raise
  finally:
    conn.close()
    logger.debug("Database connection closed")


