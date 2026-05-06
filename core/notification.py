# File: core/notification.py
"""Core domain entity for a notification."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class NotificationStatus(str, Enum):
    """
    Enum for the status of a notification.

    Attributes:
        PENDING: The notification has been created but not yet sent.
        SENT: The notification has been successfully sent.
        FAILED: The notification failed to be sent.
    """
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


@dataclass(frozen=True)
class Notification:
    """
    Represents a notification to be sent to a recipient.

    This is a core domain entity, representing the data and state of a notification
    independent of any persistence or transport layer. It is immutable.

    Attributes:
        id: The unique identifier for the notification.
        recipient: The address or identifier of the recipient (e.g., email, phone number, user_id).
        message: The content of the notification.
        status: The current delivery status of the notification.
        created_at: The timestamp when the notification was created.
        updated_at: The timestamp when the notification was last updated.
    """
    id: UUID
    recipient: str
    message: str
    status: NotificationStatus
    created_at: datetime
    updated_at: datetime