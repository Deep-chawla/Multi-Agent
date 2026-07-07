from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class Message:
    id: str = field(default_factory=lambda: str(uuid4()))
    conversation_id: str = ""
    role: str = ""                  # user | assistant | system
    content: str = ""
    agent: str | None = None        # GeneralAgent, CodingAgent, RAGAgent...
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)