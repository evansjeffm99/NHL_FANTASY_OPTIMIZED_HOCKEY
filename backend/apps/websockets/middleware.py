"""WebSocket middleware for JWT authentication."""
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    """Middleware for JWT authentication in WebSockets."""

    async def __call__(self, scope, receive, send):
        """Authenticate WebSocket connection."""
        headers = dict(scope['headers'])

        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Bearer':
                    token = AccessToken(token_key)
                    user = await self.get_user(token['user_id'])
                    scope['user'] = user
            except Exception as e:
                logger.error(f"WebSocket auth error: {e}")
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        """Get user from database."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
