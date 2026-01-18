# Welcome to Compass

This is an example vault showing how to organize your knowledge with Compass CLI.

## Vault Structure

- `.compass/` - Compass configuration and custom commands
  - `profile.toml` - Vault-specific settings
  - `commands/` - Custom slash commands
- `notes/` - Your notes and documents
- `metrics/` - Personal data and metrics

## Getting Started

1. Initialize Compass in your own directory:
   ```bash
   compass init --vault ~/my-vault
   ```

2. Configure your LLM provider:
   ```bash
   compass config set llm.provider openai
   compass config set llm.api_key YOUR_KEY
   ```

3. Ingest your documents:
   ```bash
   compass ingest ~/Documents
   ```

4. Start chatting:
   ```bash
   compass chat
   ```

## Custom Commands

Create custom slash commands in `.compass/commands/`. Each Markdown file becomes a command.

For example, `.compass/commands/daily.md` becomes `/daily` in chat.

## Tips

- Keep notes in Markdown for best results
- Use consistent naming conventions
- Tag or categorize notes for easier retrieval
- Regularly run ingestion to keep the knowledge base fresh

## Learn More

- Check the main README for full documentation
- Explore the example files in this vault
- Experiment with different queries and commands
