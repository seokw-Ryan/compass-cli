"""Ingestion pipeline orchestration."""

from pathlib import Path
from typing import List, Dict, Any
from compass.ingest.loaders import get_loader
from compass.ingest.chunking import SimpleChunker


class IngestionPipeline:
    """Orchestrates document ingestion."""

    def __init__(self):
        """Initialize pipeline."""
        self.chunker = SimpleChunker()

    def process_file(self, path: Path) -> Dict[str, Any]:
        """Process a single file."""
        loader = get_loader(path)
        if loader is None:
            return {"error": f"No loader for {path.suffix}"}

        doc = loader.load(path)
        chunks = self.chunker.chunk(doc["content"])

        return {
            "document": doc,
            "chunks": chunks,
            "path": str(path),
        }

    def process_directory(self, path: Path) -> List[Dict[str, Any]]:
        """Process all files in directory."""
        results = []
        for file_path in path.rglob("*"):
            if file_path.is_file():
                result = self.process_file(file_path)
                results.append(result)
        return results
