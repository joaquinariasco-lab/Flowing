# src/flowing/decision/event.py

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import time
import uuid

def generate_id():
    return str(uuid.uuid4())

@dataclass
class ToolCall:
    name: str
    arguments: Dict[str, Any]

@dataclass
class DecisionEvent:
    agent_id: str
    prompt: str
    model: str
    temperature: float
    output: str

    tool_calls: List[ToolCall] = field(default_factory=list)

    parent_id: Optional[str] = None
    decision_id: str = field(default_factory=generate_id)
    timestamp: float = field(default_factory=time.time)
