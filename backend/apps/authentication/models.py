"""
Authentication models for custom User management.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with email-based authentication.

    Extends Django's AbstractUser to use email instead of username
    and adds NHL Fantasy-specific fields.
    """

    # Remove username field
    username = None

    # Use email as the unique identifier
    email = models.EmailField(
        _('email address'),
        unique=True,
        db_index=True,
        help_text=_('Required. Must be a valid email address.')
    )

    # User profile fields
    display_name = models.CharField(
        _('display name'),
        max_length=150,
        blank=True,
        help_text=_('Optional display name for the user.')
    )

    avatar_url = models.URLField(
        _('avatar URL'),
        blank=True,
        null=True,
        help_text=_('URL to user avatar image.')
    )

    # Fantasy preferences
    favorite_team = models.CharField(
        _('favorite team'),
        max_length=3,
        blank=True,
        help_text=_('3-letter NHL team code (e.g., TOR, MTL, NYR).')
    )

    # Mega.io storage fields
    mega_folder_id = models.CharField(
        _('Mega.io folder ID'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('User-specific Mega.io folder ID for cloud storage.')
    )

    mega_storage_used_bytes = models.BigIntegerField(
        _('Mega.io storage used'),
        default=0,
        help_text=_('Storage space used in bytes.')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(
        _('last login IP'),
        blank=True,
        null=True
    )

    # Manager
    objects = UserManager()

    # Authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        """String representation of the user."""
        return self.email

    def get_full_name(self):
        """Return the full name of the user."""
        if self.display_name:
            return self.display_name
        return super().get_full_name()

    def get_storage_quota_bytes(self):
        """Return the user's storage quota in bytes."""
        from django.conf import settings
        return settings.MEGA_USER_QUOTA_GB * 1024 * 1024 * 1024

    def get_storage_available_bytes(self):
        """Return available storage space in bytes."""
        return self.get_storage_quota_bytes() - self.mega_storage_used_bytes

    def has_storage_space(self, required_bytes):
        """Check if user has enough storage space."""
        return self.get_storage_available_bytes() >= required_bytes


class UserSession(models.Model):
    """
    Track user sessions for JWT token management and security.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    refresh_token = models.CharField(
        max_length=500,
        unique=True,
        db_index=True
    )

    access_token = models.CharField(
        max_length=500,
        db_index=True
    )

    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('user session')
        verbose_name_plural = _('user sessions')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['refresh_token']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        """String representation of the session."""
        return f"{self.user.email} - {self.created_at}"
