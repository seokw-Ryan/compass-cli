"""Text chunking strategies."""

from typing import List, Dict, Any


class Chunker:
    """Base chunker class."""

    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        """Initialize chunker."""
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        """Split text into chunks."""
        raise NotImplementedError


class SimpleChunker(Chunker):
    """Simple character-based chunker."""

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        """Split text into fixed-size chunks with overlap."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            chunks.append(
                {
                    "content": chunk_text,
                    "position": len(chunks),
                    "start": start,
                    "end": end,
                }
            )

            start += self.chunk_size - self.overlap

        return chunks
