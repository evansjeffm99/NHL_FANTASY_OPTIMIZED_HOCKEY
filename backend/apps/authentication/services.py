"""
Authentication services for business logic and helper functions.
"""

from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import UserSession
import logging

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Service class for authentication-related operations."""

    @staticmethod
    def get_client_ip(request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def create_session(user, refresh_token, access_token, ip_address, user_agent):
        """Create a new user session."""
        expires_at = timezone.now() + timedelta(
            days=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].days
        )

        session = UserSession.objects.create(
            user=user,
            refresh_token=refresh_token,
            access_token=access_token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at
        )

        logger.info(f"Created session for user {user.email} from {ip_address}")
        return session

    @staticmethod
    def deactivate_session(refresh_token):
        """Deactivate a user session."""
        try:
            session = UserSession.objects.get(refresh_token=refresh_token)
            session.is_active = False
            session.save()
            logger.info(f"Deactivated session for user {session.user.email}")
            return True
        except UserSession.DoesNotExist:
            logger.warning(f"Attempted to deactivate non-existent session")
            return False

    @staticmethod
    def clean_expired_sessions():
        """Clean up expired sessions."""
        expired_count = UserSession.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()[0]

        logger.info(f"Cleaned up {expired_count} expired sessions")
        return expired_count

    @staticmethod
    def get_active_sessions(user):
        """Get all active sessions for a user."""
        return UserSession.objects.filter(
            user=user,
            is_active=True,
            expires_at__gt=timezone.now()
        )

    @staticmethod
    def revoke_all_sessions(user, except_token=None):
        """Revoke all sessions for a user except the specified one."""
        sessions = UserSession.objects.filter(user=user, is_active=True)

        if except_token:
            sessions = sessions.exclude(refresh_token=except_token)

        count = sessions.update(is_active=False)
        logger.info(f"Revoked {count} sessions for user {user.email}")
        return count
