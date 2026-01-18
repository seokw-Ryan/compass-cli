"""Base LLM provider interface.

When using cloud LLM providers (OpenAI, Anthropic, Google), only the
current query and context are sent to the API. Full conversation history
is maintained locally and never sent to external services.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class Message:
    """Chat message."""

    def __init__(self, role: str, content: str):
        """Initialize message."""
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        """Convert to dict."""
        return {"role": self.role, "content": self.content}


class LLMProvider(ABC):
    """Base class for LLM providers.
    
    Providers may use cloud APIs, but conversation history is maintained
    locally. Only the current query and retrieved context are sent to
    the LLM API.
    """

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        """Initialize provider."""
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def complete(
        self,
        messages: List[Message],
        **kwargs,
    ) -> str:
        """Generate completion."""
        pass

    @abstractmethod
    def stream(
        self,
        messages: List[Message],
        **kwargs,
    ):
        """Generate streaming completion."""
        pass
