"""Document retrieval."""

from typing import List, Dict, Any


class Retriever:
    """Base retriever class."""

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents."""
        raise NotImplementedError


class DummyRetriever(Retriever):
    """Dummy retriever for testing."""

    def __init__(self, documents: List[Dict[str, Any]]):
        """Initialize with document corpus."""
        self.documents = documents

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Return first top_k documents (no actual retrieval)."""
        return self.documents[:top_k]
