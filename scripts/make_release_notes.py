#!/usr/bin/env python3
"""Generate release notes from git history."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_version() -> str:
    """Get current version."""
    version_file = Path(__file__).parent.parent / "VERSION"
    return version_file.read_text().strip()


def get_commits_since_tag(tag: str = None) -> list[str]:
    """Get commits since last tag."""
    if tag:
        cmd = ["git", "log", f"{tag}..HEAD", "--oneline"]
    else:
        cmd = ["git", "log", "--oneline"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        return []


def get_last_tag() -> str:
    """Get the last git tag."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def categorize_commit(commit: str) -> tuple[str, str]:
    """Categorize commit by type."""
    message = commit.split(" ", 1)[1] if " " in commit else commit

    if message.startswith(("feat:", "feature:")):
        return "Features", message
    elif message.startswith("fix:"):
        return "Bug Fixes", message
    elif message.startswith("docs:"):
        return "Documentation", message
    elif message.startswith(("chore:", "build:", "ci:")):
        return "Maintenance", message
    elif message.startswith("refactor:"):
        return "Refactoring", message
    elif message.startswith("test:"):
        return "Tests", message
    else:
        return "Other Changes", message


def generate_release_notes(version: str) -> str:
    """Generate release notes."""
    last_tag = get_last_tag()
    commits = get_commits_since_tag(last_tag)

    # Group commits by category
    categories = {}
    for commit in commits:
        if not commit:
            continue
        category, message = categorize_commit(commit)
        if category not in categories:
            categories[category] = []
        categories[category].append(message)

    # Build release notes
    notes = [
        f"# Release v{version}",
        "",
        f"Released: {datetime.now().strftime('%Y-%m-%d')}",
        "",
    ]

    if last_tag:
        notes.append(f"Changes since {last_tag}:")
    else:
        notes.append("Initial release")

    notes.append("")

    # Add categories
    for category in ["Features", "Bug Fixes", "Documentation", "Refactoring", "Tests", "Maintenance", "Other Changes"]:
        if category in categories:
            notes.append(f"## {category}")
            notes.append("")
            for message in categories[category]:
                notes.append(f"- {message}")
            notes.append("")

    # Add installation instructions
    notes.extend([
        "## Installation",
        "",
        "### Via npm",
        "```bash",
        "npm install -g compass-cli",
        "```",
        "",
        "### Via direct download",
        "Download the appropriate binary for your platform from the assets below.",
        "",
    ])

    return "\n".join(notes)


def main():
    """Main entry point."""
    version = get_version()
    notes = generate_release_notes(version)
    print(notes)


if __name__ == "__main__":
    main()
