from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Application configuration sourced from environment variables."""

    data_dir: Path
    database_filename: str

    @property
    def database_path(self) -> Path:
        return self.data_dir / self.database_filename


@lru_cache()
def get_settings() -> Settings:
    base_dir = Path(__file__).resolve().parents[1]
    default_data_dir = base_dir / "data"

    data_dir = Path(
        os.getenv("APP_DATA_DIR", str(default_data_dir))
    ).expanduser().resolve()
    database_filename = os.getenv("APP_DATABASE_FILENAME", "app.db")

    settings = Settings(data_dir=data_dir, database_filename=database_filename)
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    return settings
