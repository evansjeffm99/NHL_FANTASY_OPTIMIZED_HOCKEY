"""Notification service."""
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending notifications."""

    @staticmethod
    def send_email(user, subject, message):
        """Send email notification."""
        logger.info(f"Sending email to {user.email}: {subject}")
        # Email logic would go here

    @staticmethod
    def send_websocket_update(channel, data):
        """Send WebSocket update."""
        logger.info(f"Sending WebSocket update to {channel}")
        # WebSocket logic would go here
