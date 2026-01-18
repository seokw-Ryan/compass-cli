# Example Vault

This is a sample vault demonstrating the Compass CLI structure.

## Contents

- `.compass/` - Configuration and custom commands
- `notes/` - Example notes and documents
- `metrics/` - Sample personal data

## Using This Vault

You can use this as a template for your own vault:

```bash
# Copy to your location
cp -r examples/vault ~/my-compass-vault

# Initialize (if needed)
cd ~/my-compass-vault
compass init --vault .

# Start using it
compass chat --vault .
```

## Structure Guidelines

### Notes

Keep your notes organized by topic or project. Use consistent naming:
- `project-name.md` for project documentation
- `YYYY-MM-DD-event.md` for dated entries
- `topic-subtopic.md` for hierarchical topics

### Metrics

Store personal data in simple formats (CSV, JSON) for easy ingestion and analysis.

### Commands

Create custom slash commands for repeated queries:
- `/daily` - Daily review
- `/weekly` - Weekly review
- `/decide <topic>` - Decision analysis
- `/plan <goal>` - Planning assistant

Each command is a Markdown file with a prompt template.
