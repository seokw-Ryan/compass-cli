"""Document loaders for various file formats."""

from pathlib import Path
from typing import Dict, Any, Optional


class DocumentLoader:
    """Base document loader."""

    def load(self, path: Path) -> Dict[str, Any]:
        """Load document from path."""
        raise NotImplementedError


class TextLoader(DocumentLoader):
    """Load plain text files."""

    def load(self, path: Path) -> Dict[str, Any]:
        """Load text file."""
        content = path.read_text(encoding="utf-8", errors="ignore")
        return {
            "content": content,
            "metadata": {
                "source": str(path),
                "type": "text",
            },
        }


class MarkdownLoader(DocumentLoader):
    """Load Markdown files."""

    def load(self, path: Path) -> Dict[str, Any]:
        """Load Markdown file."""
        content = path.read_text(encoding="utf-8", errors="ignore")
        return {
            "content": content,
            "metadata": {
                "source": str(path),
                "type": "markdown",
            },
        }


def get_loader(path: Path) -> Optional[DocumentLoader]:
    """Get appropriate loader for file."""
    suffix = path.suffix.lower()
    if suffix == ".md":
        return MarkdownLoader()
    elif suffix in [".txt", ".log"]:
        return TextLoader()
    return None
