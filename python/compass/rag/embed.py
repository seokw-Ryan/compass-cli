"""Embedding generation.

Embeddings can be generated locally (e.g., using Ollama) or via cloud APIs.
When using cloud embedding services, document content is sent to the API.
Users should be aware of this trade-off and can choose local models for
complete privacy.
"""

from typing import List
import hashlib


class Embedder:
    """Base embedder class.
    
    Embedders generate vector representations of text. For local-first
    privacy, use local embedding models (e.g., Ollama). Cloud embedding
    APIs will send document content to external services.
    """

    def embed(self, text: str) -> List[float]:
        """Generate embedding for text."""
        raise NotImplementedError

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        return [self.embed(text) for text in texts]


class DummyEmbedder(Embedder):
    """Dummy embedder for testing (returns hash-based pseudo-embedding)."""

    def embed(self, text: str) -> List[float]:
        """Generate pseudo-embedding from text hash."""
        hash_bytes = hashlib.md5(text.encode()).digest()
        # Convert to list of floats normalized to [-1, 1]
        return [(b / 255.0) * 2 - 1 for b in hash_bytes]
