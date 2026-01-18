"""Citation generation for RAG responses."""

from typing import List, Dict, Any


def generate_citations(chunks: List[Dict[str, Any]]) -> str:
    """Generate citation text from retrieved chunks."""
    if not chunks:
        return ""

    citations = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("source", "unknown")
        citations.append(f"[{i}] {source}")

    return "\n\nSources:\n" + "\n".join(citations)


def format_context(chunks: List[Dict[str, Any]]) -> str:
    """Format retrieved chunks as context for LLM."""
    if not chunks:
        return ""

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        content = chunk.get("content", "")
        source = chunk.get("metadata", {}).get("source", "unknown")
        context_parts.append(f"[Document {i} - {source}]\n{content}")

    return "\n\n".join(context_parts)
