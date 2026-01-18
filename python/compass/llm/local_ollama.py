"""Ollama local provider."""

from typing import List
from compass.llm.base import LLMProvider, Message


class OllamaProvider(LLMProvider):
    """Ollama local provider (stub)."""

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        base_url: str = "http://localhost:11434",
    ):
        """Initialize Ollama provider."""
        super().__init__(model, temperature, max_tokens)
        self.base_url = base_url

    def complete(self, messages: List[Message], **kwargs) -> str:
        """Generate completion."""
        raise NotImplementedError("Ollama provider not yet implemented")

    def stream(self, messages: List[Message], **kwargs):
        """Generate streaming completion."""
        raise NotImplementedError("Ollama streaming not yet implemented")
