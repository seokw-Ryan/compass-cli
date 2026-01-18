"""Vault initialization and validation."""

from pathlib import Path
from typing import Optional
import toml
from compass.paths import ensure_dir


class Vault:
    """Vault manager for Compass."""

    def __init__(self, path: Path):
        """Initialize vault at given path."""
        self.path = path
        self.compass_dir = path / ".compass"
        self.config_file = self.compass_dir / "profile.toml"
        self.commands_dir = self.compass_dir / "commands"

    def exists(self) -> bool:
        """Check if vault is initialized."""
        return self.compass_dir.exists() and self.config_file.exists()

    def init(self) -> None:
        """Initialize a new vault."""
        if self.exists():
            raise ValueError(f"Vault already initialized at {self.path}")

        # Create vault structure
        ensure_dir(self.path)
        ensure_dir(self.compass_dir)
        ensure_dir(self.commands_dir)

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
