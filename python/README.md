# Compass Python CLI

This directory contains the Python implementation of Compass.

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run the CLI
python -m compass --help
compass --help
```

## Running Tests

```bash
pytest
```

## Code Quality

```bash
# Format code
black compass tests

# Lint
ruff compass tests

# Type check
mypy compass
```

## Project Structure

- `compass/` - Main package
  - `cli.py` - Typer CLI entry point
  - `config.py` - Configuration management
  - `paths.py` - XDG path utilities
  - `vault.py` - Vault initialization and validation
  - `sessions.py` - Session management
  - `logging.py` - JSONL logging
  - `sandbox.py` - Sandbox policies
  - `db/` - Database layer
  - `ingest/` - Document ingestion pipeline
  - `rag/` - RAG implementation
  - `llm/` - LLM provider interfaces
  - `tools/` - Built-in tools (planner, journal, etc.)
  - `prompts/` - System prompts
  - `commands/` - Slash command registry

## Building with PyInstaller

See `../packaging/` for build scripts.
