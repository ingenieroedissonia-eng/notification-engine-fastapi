# File: core/repositories/channel_repository.py
"""
This module defines the abstract interface for channel data access.
"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from core.channel import Channel


class ChannelRepository(ABC):
    """
    Abstract base class defining the repository interface for channels.
    """

    @abstractmethod
    async def get_by_id(self, channel_id: UUID) -> Optional[Channel]:
        """
        Retrieves a channel by its unique identifier.

        Args:
            channel_id: The UUID of the channel to retrieve.

        Returns:
            An optional Channel object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def delete(self, channel_id: UUID) -> None:
        """
        Deletes a channel by its unique identifier.

        Args:
            channel_id: The UUID of the channel to delete.
        """
        pass