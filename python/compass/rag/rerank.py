"""Result reranking."""

from typing import List, Dict, Any


class Reranker:
    """Base reranker class."""

    def rerank(
        self, query: str, documents: List[Dict[str, Any]], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Rerank documents by relevance."""
        raise NotImplementedError


class NoOpReranker(Reranker):
    """Pass-through reranker (no reranking)."""

    def rerank(
        self, query: str, documents: List[Dict[str, Any]], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Return documents as-is."""
        return documents[:top_k]
