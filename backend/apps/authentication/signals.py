"""
Authentication signals for post-save actions.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_mega_folder(sender, instance, created, **kwargs):
    """
    Create a Mega.io folder for new users if Mega is enabled.

    This signal is triggered after a User is created to set up
    their cloud storage folder.
    """
    if created and settings.MEGA_ENABLED:
        try:
            from services.mega_storage import MegaStorageService

            # Create user-specific folder in Mega
            folder_id = MegaStorageService.create_user_folder(instance)

            if folder_id:
                instance.mega_folder_id = folder_id
                instance.save(update_fields=['mega_folder_id'])
                logger.info(f"Created Mega folder for user {instance.email}")

        except Exception as e:
            logger.error(f"Failed to create Mega folder for user {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    """Log user creation for audit purposes."""
    if created:
        logger.info(f"New user created: {instance.email} (ID: {instance.id})")
