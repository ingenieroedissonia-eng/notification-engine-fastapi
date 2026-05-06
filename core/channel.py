# File: core/channel.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict
from uuid import UUID, uuid4


class ChannelType(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"


@dataclass
class Channel:
    name: str
    type: ChannelType
    id: UUID = field(default_factory=uuid4)
    configuration: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Channel name cannot be empty.")
        if not isinstance(self.type, ChannelType):
            raise TypeError(f"Invalid channel type. Must be one of {list(ChannelType)}.")
        if not isinstance(self.configuration, dict):
            raise TypeError("Configuration must be a dictionary.")