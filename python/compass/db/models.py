"""Database models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Document:
    """Document model."""

    id: Optional[int]
    path: str
    content: str
    metadata: Dict[str, Any]
    hash: str
    ingested_at: datetime
    updated_at: datetime


@dataclass
class Chunk:
    """Chunk model."""

    id: Optional[int]
    document_id: int
    content: str
    embedding: Optional[bytes]
    position: int
    metadata: Dict[str, Any]
