"""Session management for chat and execution contexts."""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json
from compass.paths import get_state_dir, ensure_dir


class Session:
    """Represents a Compass session."""

    def __init__(self, session_id: Optional[str] = None):
        """Initialize or resume a session."""
        self.id = session_id or self._generate_id()
        self.created_at = datetime.now()
        self.messages: list[Dict[str, Any]] = []

    def _generate_id(self) -> str:
        """Generate a unique session ID."""
        return f"sess_{uuid.uuid4().hex[:12]}"

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session."""
        self.messages.append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dict."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "messages": self.messages,
        }


class SessionManager:
    """Manages session persistence."""

    def __init__(self):
        """Initialize session manager."""
        self.sessions_dir = ensure_dir(get_state_dir() / "sessions")

    def save(self, session: Session) -> Path:
        """Save session to disk."""
        session_file = self.sessions_dir / f"{session.id}.json"
        with open(session_file, "w") as f:
            json.dump(session.to_dict(), f, indent=2)
        return session_file

    def load(self, session_id: str) -> Optional[Session]:
        """Load session from disk."""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return None

        with open(session_file) as f:
            data = json.load(f)

        session = Session(session_id=data["id"])
        session.created_at = datetime.fromisoformat(data["created_at"])
        session.messages = data["messages"]
        return session

    def list_sessions(self) -> list[str]:
        """List all session IDs."""
        return [f.stem for f in self.sessions_dir.glob("*.json")]
