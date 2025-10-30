"""
Configuration loader for Biome Coaching Agent.
Loads environment variables and exposes typed accessors.
"""
import os
from dataclasses import dataclass

try:
  # Optional: load from .env if present during local dev
  from dotenv import load_dotenv  # type: ignore

  load_dotenv()
except Exception:
  # dotenv is optional; ignore if not installed yet
  pass


@dataclass(frozen=True)
class Settings:
  database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/biome_coaching")
  google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
  debug: bool = os.getenv("DEBUG", "true").lower() == "true"


settings = Settings()


