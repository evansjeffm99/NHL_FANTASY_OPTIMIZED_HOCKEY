"""
Admin configuration for authentication models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""

    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'display_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'display_name', 'avatar_url')}),
        (_('Fantasy preferences'), {'fields': ('favorite_team',)}),
        (_('Mega.io storage'), {'fields': ('mega_folder_id', 'mega_storage_used_bytes')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at', 'last_login_ip')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login']


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin for UserSession model."""

    list_display = ['user', 'ip_address', 'created_at', 'expires_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'expires_at']
    search_fields = ['user__email', 'ip_address', 'user_agent']
    ordering = ['-created_at']
    readonly_fields = ['user', 'refresh_token', 'access_token', 'created_at']

    fieldsets = (
        (None, {'fields': ('user', 'is_active')}),
        (_('Tokens'), {'fields': ('refresh_token', 'access_token')}),
        (_('Session info'), {'fields': ('ip_address', 'user_agent', 'created_at', 'expires_at')}),
    )
