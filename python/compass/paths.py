"""XDG-compliant path utilities."""

import os
from pathlib import Path
from typing import Optional


def get_xdg_config_home() -> Path:
    """Get XDG config home directory."""
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def get_xdg_data_home() -> Path:
    """Get XDG data home directory."""
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))


def get_xdg_state_home() -> Path:
    """Get XDG state home directory."""
    return Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))


def get_xdg_cache_home() -> Path:
    """Get XDG cache home directory."""
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))


def get_config_dir() -> Path:
    """Get Compass config directory."""
    if override := os.environ.get("COMPASS_CONFIG_HOME"):
        return Path(override)
    return get_xdg_config_home() / "compass"


def get_data_dir() -> Path:
    """Get Compass data directory."""
    if override := os.environ.get("COMPASS_DATA_HOME"):
        return Path(override)
    return get_xdg_data_home() / "compass"


def get_state_dir() -> Path:
    """Get Compass state directory."""
    if override := os.environ.get("COMPASS_STATE_HOME"):
        return Path(override)
    return get_xdg_state_home() / "compass"


def get_cache_dir() -> Path:
    """Get Compass cache directory."""
    if override := os.environ.get("COMPASS_CACHE_HOME"):
        return Path(override)
    return get_xdg_cache_home() / "compass"


def get_vault_path() -> Optional[Path]:
    """Get vault path from environment or config."""
    if vault_env := os.environ.get("COMPASS_VAULT"):
        return Path(vault_env)
    return None


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path
