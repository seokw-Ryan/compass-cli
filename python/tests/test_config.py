"""Tests for configuration management."""

import pytest
from pathlib import Path
import tempfile
from compass.config import Config


@pytest.fixture
def temp_config():
    """Create temporary config for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        config_path = Path(f.name)
    yield config_path
    config_path.unlink(missing_ok=True)


def test_config_defaults(temp_config):
    """Test default configuration."""
    config = Config(temp_config)
    assert config.get("llm.provider") == "ollama"
    assert config.get("llm.model") == "gpt-4"
    assert config.get("rag.chunk_size") == 512


def test_config_set_get(temp_config):
    """Test setting and getting config values."""
    config = Config(temp_config)
    config.set("llm.temperature", 0.5)
    assert config.get("llm.temperature") == 0.5


def test_config_save_load(temp_config):
    """Test saving and loading config."""
    config1 = Config(temp_config)
    config1.set("test.key", "value")
    config1.save()

    config2 = Config(temp_config)
    config2.load()
    assert config2.get("test.key") == "value"


def test_config_nested_keys(temp_config):
    """Test nested key access."""
    config = Config(temp_config)
    config.set("a.b.c", "deep")
    assert config.get("a.b.c") == "deep"


def test_config_default_value(temp_config):
    """Test default value for missing keys."""
    config = Config(temp_config)
    assert config.get("nonexistent", "default") == "default"
