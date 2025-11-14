"""
Authentication middleware for request processing.
"""

from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
import logging

logger = logging.getLogger(__name__)


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate users using JWT tokens.

    This middleware attempts to authenticate requests using JWT tokens
    before they reach the view layer.
    """

    def process_request(self, request):
        """Process incoming request and authenticate if JWT token is present."""
        if request.path.startswith('/api/'):
            try:
                jwt_authentication = JWTAuthentication()
                response = jwt_authentication.authenticate(request)

                if response is not None:
                    user, token = response
                    request.user = user
                    request.auth = token

            except (InvalidToken, AuthenticationFailed) as e:
                logger.debug(f"JWT authentication failed: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error in JWT middleware: {str(e)}")

        return None
