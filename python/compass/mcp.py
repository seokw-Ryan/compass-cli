"""Local MCP-style access to on-device data.

This module provides a minimal, local-only interface for accessing files stored
in the user's vault. No network calls are made.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List

from compass.paths import get_default_vault_path, ensure_dir


@dataclass
class LocalDataAccess:
    """Local data access helper for MCP-style tool calls."""

    vault_path: Path

    @classmethod
    def from_config(cls, vault_path: Path | None) -> "LocalDataAccess":
        """Create a LocalDataAccess instance from a configured vault path."""
        resolved = vault_path or get_default_vault_path()
        ensure_dir(resolved)
        return cls(resolved.resolve())

    def status(self) -> str:
        """Return a short status string for the local data store."""
        return f"Local vault: {self.vault_path}"

    def list_files(self, relative_dir: str = "") -> List[str]:
        """List files under the vault path."""
        root = (self.vault_path / relative_dir).resolve()
        if not root.exists() or not root.is_dir():
            return []
        results = []
        for path in root.rglob("*"):
            if path.is_file():
                results.append(str(path.relative_to(self.vault_path)))
        return sorted(results)

    def read_text(self, relative_path: str, max_chars: int = 2000) -> str:
        """Read a text file from the vault, truncated for safety."""
        target = (self.vault_path / relative_path).resolve()
        if not target.exists() or not target.is_file():
            raise FileNotFoundError(relative_path)
        data = target.read_text(errors="replace")
        if len(data) > max_chars:
            return data[:max_chars] + "\n...[truncated]..."
        return data
