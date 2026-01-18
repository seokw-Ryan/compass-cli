"""Base LLM provider interface."""

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
    """Base class for LLM providers."""

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
