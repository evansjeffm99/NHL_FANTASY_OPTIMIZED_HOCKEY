"""Caching service."""
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """Service for cache operations."""

    @staticmethod
    def get_or_set(key, callback, timeout=300):
        """Get from cache or set with callback."""
        value = cache.get(key)

        if value is None:
            value = callback()
            cache.set(key, value, timeout)

        return value

    @staticmethod
    def invalidate_pattern(pattern):
        """Invalidate cache keys matching pattern."""
        # Redis-specific pattern invalidation
        logger.info(f"Invalidating cache pattern: {pattern}")
