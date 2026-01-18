"""Smoke tests for CLI."""

import pytest
from typer.testing import CliRunner
from compass.cli import app

runner = CliRunner()


def test_help():
    """Test --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "compass" in result.stdout.lower()


def test_version():
    """Test --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


def test_config_show():
    """Test config show command."""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0


def test_init_help():
    """Test init --help."""
    result = runner.invoke(app, ["init", "--help"])
    assert result.exit_code == 0
    assert "vault" in result.stdout.lower()


def test_ingest_help():
    """Test ingest --help."""
    result = runner.invoke(app, ["ingest", "--help"])
    assert result.exit_code == 0


def test_chat_help():
    """Test chat --help."""
    result = runner.invoke(app, ["chat", "--help"])
    assert result.exit_code == 0


def test_exec_help():
    """Test exec --help."""
    result = runner.invoke(app, ["exec", "--help"])
    assert result.exit_code == 0
