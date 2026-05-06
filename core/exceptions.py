# File: core/exceptions.py
"""
Custom exceptions for the notification system.

This module defines a set of custom exception classes to handle specific
error conditions within the notification service. Using specific exceptions
improves error handling and makes the code more readable and maintainable.
"""

class NotificationError(Exception):
    """Base exception class for all notification-related errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"NotificationError: {self.message}"


class ChannelError(NotificationError):
    """Raised when there is an issue with a notification channel."""
    def __init__(self, message: str, channel_id: str | None = None):
        self.channel_id = channel_id
        full_message = f"Channel '{channel_id}': {message}" if channel_id else message
        super().__init__(full_message)

    def __str__(self) -> str:
        return f"ChannelError: {self.message}"


class InvalidConfigurationError(NotificationError):
    """Raised when a configuration setting is invalid or missing."""
    def __init__(self, message: str, setting_key: str | None = None):
        self.setting_key = setting_key
        full_message = f"Configuration key '{setting_key}': {message}" if setting_key else message
        super().__init__(full_message)

    def __str__(self) -> str:
        return f"InvalidConfigurationError: {self.message}"


class ExternalServiceError(NotificationError):
    """Raised when an external service (e.g., email provider, SMS gateway) fails."""
    def __init__(self, message: str, service_name: str | None = None):
        self.service_name = service_name
        full_message = f"External service '{service_name}': {message}" if service_name else message
        super().__init__(full_message)

    def __str__(self) -> str:
        return f"ExternalServiceError: {self.message}"