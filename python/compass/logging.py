"""JSONL logging for run history."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from compass.paths import get_state_dir, ensure_dir


class RunLogger:
    """Logger for command execution history."""

    def __init__(self, log_file: Optional[Path] = None):
        """Initialize run logger."""
        if log_file is None:
            log_dir = ensure_dir(get_state_dir() / "logs")
            log_file = log_dir / "runs.jsonl"
        self.log_file = log_file

    def log(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log an event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data,
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_command(self, command: str, args: Dict[str, Any]) -> None:
        """Log a command execution."""
        self.log("command", {"command": command, "args": args})

    def log_error(self, error: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log an error."""
        self.log("error", {"error": error, "context": context or {}})

    def log_completion(self, command: str, duration_ms: float) -> None:
        """Log command completion."""
        self.log("completion", {"command": command, "duration_ms": duration_ms})
