# File: core/channel.py
"""
Defines the core domain entity for a communication channel.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict
from uuid import UUID, uuid4


class ChannelType(str, Enum):
    """Enumeration for the types of communication channels."""
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"


@dataclass
class Channel:
    """
    Represents a communication channel through which notifications are sent.

    Attributes:
        id: The unique identifier for the channel.
        name: A human-readable name for the channel (e.g., "Transactional Email").
        type: The type of the channel (e.g., EMAIL, SMS, PUSH).
        configuration: A dictionary containing the specific settings required
                       to operate this channel (e.g., API keys, server addresses).
    """
    id: UUID = field(default_factory=uuid4)
    name: str
    type: ChannelType
    configuration: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Perform post-initialization validation."""
        if not self.name or not self.name.strip():
            raise ValueError("Channel name cannot be empty.")
        if not isinstance(self.type, ChannelType):
            raise TypeError(f"Invalid channel type. Must be one of {list(ChannelType)}.")
        if not isinstance(self.configuration, dict):
            raise TypeError("Configuration must be a dictionary.")