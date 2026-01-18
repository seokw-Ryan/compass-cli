"""Database migration utilities."""

import sqlite3
from pathlib import Path
from typing import Optional


def init_database(db_path: Path) -> None:
    """Initialize database with schema."""
    schema_path = Path(__file__).parent / "schema.sql"
    schema = schema_path.read_text()

    conn = sqlite3.connect(db_path)
    conn.executescript(schema)
    conn.commit()
    conn.close()


def migrate(db_path: Path, version: Optional[int] = None) -> None:
    """Run database migrations (stub)."""
    # Placeholder for future migration system
    pass
