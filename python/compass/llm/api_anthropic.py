"""Anthropic API provider."""

from typing import List
from compass.llm.base import LLMProvider, Message


class AnthropicProvider(LLMProvider):
    """Anthropic API provider (stub)."""

    def complete(self, messages: List[Message], **kwargs) -> str:
        """Generate completion."""
        raise NotImplementedError("Anthropic provider not yet implemented")

    def stream(self, messages: List[Message], **kwargs):
        """Generate streaming completion."""
        raise NotImplementedError("Anthropic streaming not yet implemented")
