"""OpenAI API provider."""

from typing import List
from compass.llm.base import LLMProvider, Message


class OpenAIProvider(LLMProvider):
    """OpenAI API provider (stub)."""

    def complete(self, messages: List[Message], **kwargs) -> str:
        """Generate completion."""
        raise NotImplementedError("OpenAI provider not yet implemented")

    def stream(self, messages: List[Message], **kwargs):
        """Generate streaming completion."""
        raise NotImplementedError("OpenAI streaming not yet implemented")
