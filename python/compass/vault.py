"""Vault initialization and validation.

All vault data is stored locally on the user's filesystem. The vault
contains user documents, notes, and a local SQLite database for indexing.
No data is sent to cloud services unless explicitly configured by the user
(e.g., when using cloud LLM providers for queries).
"""

from pathlib import Path
from typing import Optional
import toml
from compass.paths import ensure_dir
from compass.db.manager import DatabaseManager


class Vault:
    """Vault manager for Compass.
    
    A vault is a local directory containing the user's knowledge base.
    All data is stored locally - documents, database, embeddings, and metadata.
    """

    def __init__(self, path: Path):
        """Initialize vault at given path.
        
        Args:
            path: Path to the vault directory. All Compass data will be
                  stored in path/.compass/ subdirectory.
        """
        self.path = path.resolve()
        self.compass_dir = self.path / ".compass"
        self.config_file = self.compass_dir / "profile.toml"
        self.commands_dir = self.compass_dir / "commands"
        self.db_manager = DatabaseManager(self.path)

    def exists(self) -> bool:
        """Check if vault is initialized."""
        return self.compass_dir.exists() and self.config_file.exists()

    def init(self) -> None:
        """Initialize a new vault.
        
        Creates the vault directory structure and initializes the local
        SQLite database. All data will be stored locally on the filesystem.
        """
        if self.exists():
            raise ValueError(f"Vault already initialized at {self.path}")

        # Create vault structure
        ensure_dir(self.path)
        ensure_dir(self.compass_dir)
        ensure_dir(self.commands_dir)

        # Initialize local database (stored in .compass/compass.db)
        self.db_manager.ensure_database()

        # Create default profile
        profile = {
            "vault": {
                "name": self.path.name,
                "created": "2026-01-17",
            },
            "preferences": {
                "default_llm": "openai",
            },
        }
        with open(self.config_file, "w") as f:
            toml.dump(profile, f)

        # Create sample command
        sample_command = self.commands_dir / "daily.md"
        sample_command.write_text(
            "# Daily Review\n\n"
            "Review my tasks and notes from today. "
            "Highlight any decisions I made and suggest follow-ups.\n"
        )

    def validate(self) -> bool:
        """Validate vault structure."""
        if not self.exists():
            return False
        return (
            self.compass_dir.is_dir()
            and self.config_file.is_file()
            and self.commands_dir.is_dir()
        )

    def get_profile(self) -> dict:
        """Get vault profile configuration."""
        if not self.config_file.exists():
            return {}
        return toml.load(self.config_file)
    
    def get_database_path(self) -> Path:
        """Get the path to the vault's local database.
        
        Returns:
            Path to the SQLite database file (compass.db)
        """
        return self.db_manager.get_path()
    
    def get_database_connection(self):
        """Get a connection to the vault's local database.
        
        Returns:
            SQLite connection object
        """
        return self.db_manager.get_connection()


def find_vault(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find vault by searching up directory tree."""
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()
    while current != current.parent:
        vault = Vault(current)
        if vault.exists():
            return current
        current = current.parent
    return None
