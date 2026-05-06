# File: infrastructure/repositories/in_memory_channel_repository.py
"""
In-memory implementation of the ChannelRepository interface.

This module provides a concrete implementation of the ChannelRepository that stores
channel data in memory. It is suitable for testing, development, or scenarios
where persistence is not required. It follows the Singleton pattern to ensure
a single instance of the repository throughout the application lifecycle.
"""
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4

from core.channel import Channel
from core.exceptions import ChannelError, InvalidConfigurationError
from core.repositories.channel_repository import ChannelRepository


class InMemoryChannelRepository(ChannelRepository):
    """
    An in-memory repository for managing notification channels.

    This class implements the ChannelRepository interface and stores channels
    in a simple dictionary. It is not thread-safe for concurrent writes
    without additional locking mechanisms.
    """
    _instance: Optional["InMemoryChannelRepository"] = None
    _channels: Dict[UUID, Channel]

    def __init__(self) -> None:
        """
        Initializes the in-memory repository.

        Raises:
            RuntimeError: If an instance already exists, to enforce Singleton pattern.
        """
        if InMemoryChannelRepository._instance is not None:
            raise RuntimeError(
                "An instance of InMemoryChannelRepository already exists. "
                "Use get_instance() to retrieve it."
            )
        from core.channel import ChannelType
        from uuid import uuid4
        ch_email = Channel(name="Email", type=ChannelType.EMAIL, configuration={})
        ch_sms = Channel(name="SMS", type=ChannelType.SMS, configuration={})
        ch_push = Channel(name="Push", type=ChannelType.PUSH, configuration={})
        self._channels = {
            ch_email.id: ch_email,
            ch_sms.id: ch_sms,
            ch_push.id: ch_push,
        }

    @classmethod
    def get_instance(cls) -> "InMemoryChannelRepository":
        """
        Gets the singleton instance of the repository.

        Returns:
            The singleton InMemoryChannelRepository instance.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def save(self, channel: Channel) -> Channel:
        """
        Saves or updates a channel in the in-memory store.

        If the channel does not have an ID, a new one is generated.
        Basic validation is performed on the channel's properties.

        Args:
            channel: The Channel object to save.

        Returns:
            The saved Channel object, potentially with a new ID.

        Raises:
            ChannelError: If the channel name or type is empty.
            InvalidConfigurationError: If the configuration is not a dictionary.
        """
        if not channel.name:
            raise ChannelError("Channel name cannot be empty.")
        if not channel.type:
            raise ChannelError("Channel type cannot be empty.")
        if not isinstance(channel.configuration, dict):
            raise InvalidConfigurationError("Channel configuration must be a dictionary.")

        self._channels[channel.id] = channel
        return channel

    async def get_by_id(self, channel_id: UUID) -> Optional[Channel]:
        """
        Retrieves a channel by its unique identifier.

        Args:
            channel_id: The UUID of the channel to retrieve.

        Returns:
            The Channel object if found, otherwise None.
        """
        return self._channels.get(channel_id)

    async def get_all(self) -> List[Channel]:
        """
        Retrieves all channels from the repository.

        Returns:
            A list of all Channel objects.
        """
        return list(self._channels.values())

    async def delete(self, channel_id: UUID) -> None:
        """
        Deletes a channel from the repository by its ID.

        Args:
            channel_id: The UUID of the channel to delete.

        Raises:
            ChannelError: If no channel with the given ID is found.
        """
        if channel_id in self._channels:
            del self._channels[channel_id]
        else:
            raise ChannelError(f"Channel with id {channel_id} not found.")

    async def get_by_type(self, channel_type: str):
        for channel in self._channels.values():
            if hasattr(channel, 'type') and str(channel.type).upper() == channel_type.upper():
                return channel
        return None
