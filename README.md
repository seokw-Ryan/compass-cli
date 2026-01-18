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

- XDG-compliant configuration management
- Flexible vault structure
- Multiple LLM provider support (OpenAI, Anthropic, Google, Ollama)
- Document ingestion and RAG pipeline
- Session management and resumption
- Custom slash commands
- Decision journaling and weekly review tools

## Development

See `python/README.md` for Python development setup.

See `npm/README.md` for npm wrapper details.

## License

MIT
