# Compass CLI

```
  _____    ____    __  __   _____     __        _____    _____
 / ____|  / __ \  |  \/  | |  __ \   /  \      / ____|  / ____|
| |      | |  | | | \  / | | |__) | / /\ \    | (____   | (___
| |      | |  | | | |\/| | |  ___/ / /  \ \    \____ \  \___   \
| |____  | |__| | | |  | | | |    / /    \_\   ____)  |  ____) |
 \_____|  \____/  |_|  |_| |_|   /_/      \_\ |______/  |_____/
```

A Python-first CLI tool for personal knowledge management with RAG capabilities.

## Installation

```bash
pip install -r requirements.txt
compass
```

On first launch Compass shows a welcome screen where you pick your LLM provider (Local/Ollama, OpenAI, Anthropic, or Google) and optionally enter an API key. No other terminal commands are needed.

### Requirements

- Python 3.10+
- [jido](https://github.com/your-org/jido) cloned alongside this repo (for hardware detection)

## Quick Start

```bash
# Launch Compass — first run walks you through setup
compass

# Once inside chat, use slash commands:
#   /settings  - Change provider, API key, or re-run hardware detection
#   /help      - List all commands
#   /exit      - Quit

# You can also use subcommands directly:
compass init --vault ~/my-vault
compass ingest ~/Documents
compass exec "summarize my recent notes"
```

## Features

- **Zero-Config Startup**: Run `compass` and configure everything in-app
- **Hardware Detection**: Integrated [jido](https://github.com/your-org/jido) scans CPU, RAM, and GPU on first run
- **Local-First Storage**: All data stored locally - documents, database, embeddings, sessions
- **Privacy-Preserving**: No cloud storage, no telemetry, no data collection
- XDG-compliant configuration management
- Flexible vault structure (portable directories)
- Multiple LLM provider support (Ollama, OpenAI, Anthropic, Google)
- In-app `/settings` command to change provider and API keys at any time
- Document ingestion and RAG pipeline
- Session management and resumption
- Custom slash commands

## Privacy & Data Storage

Compass CLI is designed with **local-first** principles:

- ✅ **All data stored locally** - Vaults, databases, sessions, and configs are on your filesystem
- ✅ **No cloud storage by default** - Your knowledge base stays on your machine
- ✅ **No telemetry** - Zero tracking or analytics
- ⚠️ **LLM providers** - When using cloud LLM APIs, only current queries are sent (conversation history stays local)
- ⚠️ **Embeddings** - Use local models (Ollama) for complete privacy, or cloud APIs if preferred

See [`docs/LOCAL_FIRST.md`](docs/LOCAL_FIRST.md) for detailed information about data storage and privacy.

## Development

See `python/README.md` for Python development setup.

See `npm/README.md` for npm wrapper details.

## License

MIT
