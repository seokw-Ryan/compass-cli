"""Database connection manager for local-first storage."""

import sqlite3
from pathlib import Path
from typing import Optional
from compass.db.migrate import init_database


class DatabaseManager:
    """Manages local SQLite database connections.
    
    All database operations are local-only. The database file is stored
    within the vault directory to ensure data portability and privacy.
    """

    def __init__(self, vault_path: Path):
        """Initialize database manager for a vault.
        
        Args:
            vault_path: Path to the vault directory. Database will be stored
                       at vault_path/.compass/compass.db
        """
        self.vault_path = vault_path.resolve()
        self.compass_dir = self.vault_path / ".compass"
        self.db_path = self.compass_dir / "compass.db"
        
    def ensure_database(self) -> Path:
        """Ensure database exists and is initialized.
        
        Creates the database file and schema if it doesn't exist.
        
        Returns:
            Path to the database file
        """
        # Create .compass directory if it doesn't exist
        self.compass_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize database if it doesn't exist
        if not self.db_path.exists():
            init_database(self.db_path)
        
        return self.db_path
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection.
        
        Ensures database exists before returning connection.
        
        Returns:
            SQLite connection object
        """
        self.ensure_database()
        return sqlite3.connect(self.db_path)
    
    def exists(self) -> bool:
        """Check if database file exists."""
        return self.db_path.exists()
    
    def get_path(self) -> Path:
        """Get the database file path."""
        return self.db_path
