"""
Authentication views for user registration, login, and profile management.
"""

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    TokenSerializer,
    RefreshTokenSerializer,
    ChangePasswordSerializer
)
from .services import AuthenticationService

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    Creates a new user account and returns JWT tokens.
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: TokenSerializer,
            400: OpenApiResponse(description='Bad Request'),
        },
        description='Register a new user account'
    )
    def post(self, request, *args, **kwargs):
        """Register a new user and return JWT tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Store session
        ip_address = AuthenticationService.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        AuthenticationService.create_session(
            user=user,
            refresh_token=str(refresh),
            access_token=str(refresh.access_token),
            ip_address=ip_address,
            user_agent=user_agent
        )

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API endpoint for user login.

    Authenticates user credentials and returns JWT tokens.
    """

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: TokenSerializer,
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized'),
        },
        description='Login with email and password'
    )
    def post(self, request):
        """Authenticate user and return JWT tokens."""
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Update last login IP
        ip_address = AuthenticationService.get_client_ip(request)
        user.last_login_ip = ip_address
        user.save(update_fields=['last_login_ip', 'last_login'])

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Store session
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        AuthenticationService.create_session(
            user=user,
            refresh_token=str(refresh),
            access_token=str(refresh.access_token),
            ip_address=ip_address,
            user_agent=user_agent
        )

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    API endpoint for refreshing JWT access tokens.
    """

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RefreshTokenSerializer,
        responses={
            200: OpenApiResponse(description='New access token'),
            400: OpenApiResponse(description='Bad Request'),
        },
        description='Refresh JWT access token'
    )
    def post(self, request):
        """Refresh JWT access token."""
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            'access': serializer.validated_data['access']
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API endpoint for user logout.

    Invalidates the refresh token and marks session as inactive.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(description='Successfully logged out'),
            400: OpenApiResponse(description='Bad Request'),
        },
        description='Logout and invalidate tokens'
    )
    def post(self, request):
        """Logout user and invalidate tokens."""
        try:
            refresh_token = request.data.get('refresh')

            if refresh_token:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()

                # Mark session as inactive
                AuthenticationService.deactivate_session(refresh_token)

            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the current user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the current authenticated user."""
        return self.request.user

    @extend_schema(
        responses={
            200: UserSerializer,
        },
        description='Get current user profile'
    )
    def get(self, request, *args, **kwargs):
        """Get current user profile."""
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description='Bad Request'),
        },
        description='Update current user profile'
    )
    def patch(self, request, *args, **kwargs):
        """Update current user profile."""
        return super().patch(request, *args, **kwargs)


class ChangePasswordView(APIView):
    """
    API endpoint for changing user password.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description='Password changed successfully'),
            400: OpenApiResponse(description='Bad Request'),
        },
        description='Change user password'
    )
    def post(self, request):
        """Change user password."""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
