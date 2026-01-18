"""Sandbox policy management."""

from enum import Enum
from typing import Optional


class SandboxPolicy(Enum):
    """Sandbox execution policies."""

    NONE = "none"  # No sandboxing
    READ_ONLY = "read_only"  # Read-only file system access
    ISOLATED = "isolated"  # Full isolation with temp directory
    STRICT = "strict"  # Strict mode with minimal permissions


class Sandbox:
    """Sandbox manager (placeholder for future implementation)."""

    def __init__(self, policy: SandboxPolicy = SandboxPolicy.READ_ONLY):
        """Initialize sandbox with given policy."""
        self.policy = policy

    def execute(self, command: str) -> str:
        """Execute command in sandbox (stub)."""
        raise NotImplementedError("Sandbox execution not yet implemented")

    def validate_path(self, path: str) -> bool:
        """Validate if path access is allowed (stub)."""
        if self.policy == SandboxPolicy.NONE:
            return True
        # Placeholder: implement actual validation
        return True
