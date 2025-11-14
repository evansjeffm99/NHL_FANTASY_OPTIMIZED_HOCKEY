"""
Authentication serializers for API request/response handling.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    storage_quota_gb = serializers.SerializerMethodField()
    storage_used_gb = serializers.SerializerMethodField()
    storage_available_gb = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'display_name',
            'avatar_url', 'favorite_team', 'is_active', 'is_staff',
            'created_at', 'updated_at', 'storage_quota_gb',
            'storage_used_gb', 'storage_available_gb'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_staff']

    def get_storage_quota_gb(self, obj):
        """Get user storage quota in GB."""
        return obj.get_storage_quota_bytes() / (1024 ** 3)

    def get_storage_used_gb(self, obj):
        """Get user storage used in GB."""
        return obj.mega_storage_used_bytes / (1024 ** 3)

    def get_storage_available_gb(self, obj):
        """Get user available storage in GB."""
        return obj.get_storage_available_bytes() / (1024 ** 3)


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'display_name', 'favorite_team'
        ]

    def validate(self, attrs):
        """Validate password confirmation matches."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        return attrs

    def create(self, validated_data):
        """Create new user with validated data."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validate credentials and return user."""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    'Invalid email or password.',
                    code='authorization'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".',
                code='authorization'
            )

        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.Serializer):
    """Serializer for JWT token response."""

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer for token refresh request."""

    refresh = serializers.CharField(required=True)

    def validate(self, attrs):
        """Validate and refresh the token."""
        refresh_token = attrs.get('refresh')

        try:
            token = RefreshToken(refresh_token)
            attrs['access'] = str(token.access_token)
        except Exception as e:
            raise serializers.ValidationError(
                f'Invalid refresh token: {str(e)}',
                code='token_invalid'
            )

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validate password change."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'New passwords do not match.'
            })
        return attrs

    def validate_old_password(self, value):
        """Validate old password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
