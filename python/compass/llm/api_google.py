"""Google API provider."""

from typing import List
from compass.llm.base import LLMProvider, Message


class GoogleProvider(LLMProvider):
    """Google API provider (stub)."""

    def complete(self, messages: List[Message], **kwargs) -> str:
        """Generate completion."""
        raise NotImplementedError("Google provider not yet implemented")

    def stream(self, messages: List[Message], **kwargs):
        """Generate streaming completion."""
        raise NotImplementedError("Google streaming not yet implemented")
