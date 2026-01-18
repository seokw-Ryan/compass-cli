# Compass CLI

A Python-first CLI tool for personal knowledge management with RAG capabilities.

## Installation

### Via npm (recommended)

```bash
npm install -g compass-cli
compass --help
```

### From source

```bash
cd python
pip install -e .
python -m compass --help
```

## Quick Start

```bash
# Initialize a vault
compass init --vault ~/my-vault

# Configure settings
compass config set llm.provider openai
compass config set llm.model gpt-4

# Ingest documents
compass ingest ~/Documents

# Start chat interface
compass chat

# Execute a one-off prompt
compass exec "summarize my recent notes"
```

## Features

- **Local-First Storage**: All data stored locally - documents, database, embeddings, sessions
- **Privacy-Preserving**: No cloud storage, no telemetry, no data collection
- XDG-compliant configuration management
- Flexible vault structure (portable directories)
- Multiple LLM provider support (OpenAI, Anthropic, Google, Ollama)
- Document ingestion and RAG pipeline
- Session management and resumption
- Custom slash commands
- Decision journaling and weekly review tools

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
