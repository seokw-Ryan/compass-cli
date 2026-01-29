"""Configuration management using TOML.

All configuration is stored locally in TOML files. No configuration data
is sent to external services. API keys and sensitive settings remain
on the user's local filesystem only.
"""

from pathlib import Path
from typing import Any, Dict, Optional
import toml
from compass.paths import get_config_dir, ensure_dir


class Config:
    """Configuration manager for Compass.
    
    Stores all configuration locally in TOML format. Configuration files
    are stored in the XDG config directory (~/.config/compass/) by default.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize config manager."""
        if config_path is None:
            config_path = get_config_dir() / "config.toml"
        self.config_path = config_path
        self._data: Dict[str, Any] = {}
        self._file_data: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        # Start with defaults
        self._data = self._get_defaults()

        # Merge with file contents if exists
        if self.config_path.exists():
            self._file_data = toml.load(self.config_path)
            self._merge_config(self._file_data)
        else:
            self._file_data = {}

    def save(self) -> None:
        """Save configuration to file."""
        ensure_dir(self.config_path.parent)
        with open(self.config_path, "w") as f:
            toml.dump(self._data, f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value using dot notation (e.g., 'llm.provider')."""
        parts = key.split(".")
        value = self._data
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """Set config value using dot notation."""
        parts = key.split(".")
        target = self._data
        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]
        target[parts[-1]] = value

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration as a dict."""
        return self._data.copy()

    def is_set(self, key: str) -> bool:
        """Check if a config key is explicitly set in the file."""
        parts = key.split(".")
        value: Any = self._file_data
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return False
        return True

    def _merge_config(self, source: Dict[str, Any]) -> None:
        """Merge source config into current config."""
        def merge_dict(target: dict, source: dict) -> None:
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    merge_dict(target[key], value)
                else:
                    target[key] = value
        merge_dict(self._data, source)

    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "llm": {
                "mode": None,
                "provider": "ollama",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000,
            },
            "quick": {
                "options": [
                    "Daily review",
                    "Summarize recent notes",
                    "Plan my day",
                ],
            },
            "rag": {
                "chunk_size": 512,
                "chunk_overlap": 50,
                "top_k": 5,
            },
            "user": {
                "name": None,
            },
            "vault": {
                "default_path": None,
            },
        }
