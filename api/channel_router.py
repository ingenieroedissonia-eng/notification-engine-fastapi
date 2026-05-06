# File: api/channel_router.py
"""
API Router for handling channel-related operations.

This router provides endpoints for listing and managing communication channels.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core.channel import Channel
from core.repositories.channel_repository import ChannelRepository
from core.use_cases.list_channels import ListChannels
from infrastructure.repositories.in_memory_channel_repository import (
    InMemoryChannelRepository,
)

router = APIRouter(
    prefix="/channels",
    tags=["Channels"],
)


def get_channel_repository() -> ChannelRepository:
    """
    Dependency injector for the ChannelRepository.

    Returns:
        An instance of a class that implements the ChannelRepository interface.
    """
    return InMemoryChannelRepository.get_instance()


def get_list_channels_use_case(
    repository: ChannelRepository = Depends(get_channel_repository),
) -> ListChannels:
    """
    Dependency injector for the ListChannels use case.

    Args:
        repository: The channel repository implementation.

    Returns:
        An instance of the ListChannels use case.
    """
    return ListChannels(channel_repository=repository)


@router.get(
    "/",
    response_model=List[Channel],
    summary="List all available channels",
    status_code=status.HTTP_200_OK,
)
async def list_available_channels(
    use_case: ListChannels = Depends(get_list_channels_use_case),
) -> List[Channel]:
    """
    Retrieves a list of all configured communication channels.

    This endpoint fetches all channels from the system, which can be used
    to understand the available methods for sending notifications.
    """
    try:
        channels = await use_case.execute()
        return channels
    except Exception as e:
        # As per contract feedback, specific ChannelError is not available.
        # A general server error is raised for any unexpected issues.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while listing channels: {e}",
        )