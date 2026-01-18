# Local-First Design Principles

Compass CLI is designed with **local-first** principles, ensuring all user data remains on the user's machine and is never sent to cloud services without explicit user action.

## Core Principles

1. **All data is stored locally** - Documents, embeddings, sessions, and configuration are stored on the user's local filesystem
2. **No cloud storage by default** - No automatic syncing or cloud backup unless explicitly configured by the user
3. **Privacy-preserving LLM usage** - When using cloud LLM providers, only the current query is sent; conversation history remains local
4. **User control** - Users have full control over where data is stored and can move/backup vaults as regular directories

## Data Storage Locations

### Vault Data (User's Knowledge Base)
- **Location**: User-specified directory (e.g., `~/my-vault`)
- **Structure**:
  ```
  vault/
  ├── .compass/           # Compass metadata (local only)
  │   ├── profile.toml    # Vault configuration
  │   ├── compass.db      # SQLite database (documents, chunks, embeddings)
  │   └── commands/       # Custom slash commands
  ├── notes/              # User's notes (plain files)
  ├── metrics/            # User's metrics/data files
  └── ...                 # Any other user files
  ```
- **Database**: SQLite file stored in `.compass/compass.db` within the vault
- **Backup**: Users can backup by copying the entire vault directory

### Application Data (XDG-Compliant)
- **Configuration**: `~/.config/compass/config.toml` (or `$XDG_CONFIG_HOME/compass/`)
- **Sessions**: `~/.local/state/compass/sessions/` (or `$XDG_STATE_HOME/compass/sessions/`)
- **Logs**: `~/.local/state/compass/logs/runs.jsonl`
- **Cache**: `~/.cache/compass/` (temporary data only)

All paths respect XDG Base Directory Specification and can be overridden via environment variables:
- `COMPASS_CONFIG_HOME`
- `COMPASS_DATA_HOME`
- `COMPASS_STATE_HOME`
- `COMPASS_CACHE_HOME`
- `COMPASS_VAULT`

## What Stays Local

### ✅ Always Local
- **Documents**: All ingested documents are stored in the vault
- **Embeddings**: Generated embeddings are stored in the local SQLite database
- **Chunks**: Document chunks are stored locally
- **Sessions**: Chat session history is stored locally as JSON files
- **Configuration**: All settings are stored in local TOML files
- **Logs**: Command execution logs are stored locally
- **Vault metadata**: Profile, commands, and vault configuration

### ⚠️ External Services (User Choice)
- **LLM Providers**: When using cloud LLM APIs (OpenAI, Anthropic, Google), only the current query and context are sent. Conversation history is maintained locally.
- **Embedding Services**: If using cloud embedding APIs, document content may be sent. Users can opt for local embedding models (e.g., Ollama) to keep everything local.

## Privacy Considerations

### LLM Provider Usage
When using cloud LLM providers:
- Only the current conversation turn is sent (query + context from RAG)
- Full conversation history remains on the user's machine
- Users can review what's being sent before queries execute
- API keys are stored locally in configuration (never committed to version control)

### Embedding Generation
- **Local models** (e.g., Ollama): Everything stays local ✅
- **Cloud APIs** (e.g., OpenAI embeddings): Document content is sent to the API ⚠️
- Users should be aware of this trade-off and choose accordingly

### No Telemetry or Analytics
- Compass CLI does not send any telemetry, analytics, or usage data
- All logging is local only
- No tracking or user behavior monitoring

## Database Design

The SQLite database (`compass.db`) stores:
- **Documents**: Full document content and metadata
- **Chunks**: Text chunks with positions
- **Embeddings**: Vector embeddings stored as BLOB (local only)
- **Sessions**: Session metadata (full messages stored as JSON files)

All database operations are local file I/O - no network calls.

## Migration and Backup

### Backup Strategy
Users can backup their entire knowledge base by:
1. Copying the vault directory
2. The `.compass/compass.db` file contains all indexed data
3. Sessions are stored separately in the state directory

### Migration
- Vaults are portable - move the directory to another machine
- Database is SQLite (portable across platforms)
- Configuration can be exported/imported as TOML

## Implementation Guarantees

The codebase enforces local-first storage through:
1. **Path management**: All paths use `compass.paths` utilities that default to local XDG directories
2. **Database location**: Database is always stored within the vault directory
3. **No cloud storage code**: No S3, GCS, or other cloud storage integrations
4. **Explicit user consent**: Any external API calls require explicit configuration

## Future Considerations

If cloud sync is ever added (opt-in):
- It must be explicitly enabled by the user
- Users must provide their own cloud storage credentials
- End-to-end encryption would be required
- Clear documentation about what is synced
