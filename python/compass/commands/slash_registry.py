"""Slash command registry and execution."""

from typing import Dict, Callable, Any
from pathlib import Path


class SlashCommand:
    """Represents a slash command."""

    def __init__(self, name: str, handler: Callable, description: str = ""):
        """Initialize command."""
        self.name = name
        self.handler = handler
        self.description = description

    def execute(self, args: str = "") -> Any:
        """Execute command."""
        return self.handler(args)


class SlashRegistry:
    """Registry for slash commands."""

    def __init__(self):
        """Initialize registry."""
        self._commands: Dict[str, SlashCommand] = {}

    def register(self, name: str, handler: Callable, description: str = "") -> None:
        """Register a command."""
        self._commands[name] = SlashCommand(name, handler, description)

    def execute(self, name: str, args: str = "") -> Any:
        """Execute a command."""
        if name not in self._commands:
            raise ValueError(f"Unknown command: {name}")
        return self._commands[name].execute(args)

    def list_commands(self) -> Dict[str, str]:
        """List all commands with descriptions."""
        return {name: cmd.description for name, cmd in self._commands.items()}


# Global registry instance
registry = SlashRegistry()
