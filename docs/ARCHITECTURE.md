# Architecture Notes

## Local Data Storage (Vault)

Default location for user data:

- `~/.local/share/compass/vault` (XDG data directory)
- Override with `COMPASS_VAULT` or `vault.default_path` in config

The vault is a normal directory and can be moved or backed up. All data stays
local by default.

## MCP-Style Local Data Access

The `compass.mcp.LocalDataAccess` class provides a minimal local-only interface
that tools (and future LLM integrations) can use to access vault data:

- List files in the vault
- Read file contents (truncated)

No network calls are made; this is a local backend layer that is safe to use
with local-only workflows.

## Vector DB vs SQLite

Use SQLite first for simplicity:

- Works well for small to medium collections
- Easy to ship and keep local
- Great for keyword search + embeddings stored as BLOBs

Consider a vector database when:

- The embedding count is large (hundreds of thousands or more)
- You need fast approximate nearest neighbor search
- You plan to support multiple embedding models or multi-tenant use

Recommended local-first options:

- SQLite + FTS5 + embeddings stored locally
- FAISS (embedded) for fast vector search without a server

## LangChain (or similar)

Avoid heavy frameworks early:

- Adds complexity and vendor lock-in
- Slower iteration for a CLI-first app

Use LangChain when:

- You need advanced tool orchestration
- You want plug-and-play integrations
- You want tracing/observability for complex pipelines

For now, a light internal interface keeps control and privacy.
