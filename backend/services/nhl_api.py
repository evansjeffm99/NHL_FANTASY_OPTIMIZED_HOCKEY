"""NHL API service for fetching data."""
import requests
from django.conf import settings
from django.core.cache import cache
import logging
import time

logger = logging.getLogger(__name__)


class NHLAPIService:
    """Service for interacting with NHL API."""

    BASE_URL = settings.NHL_API_BASE_URL
    TIMEOUT = settings.NHL_API_TIMEOUT

    @classmethod
    def _request(cls, endpoint, params=None, retries=3):
        """Make API request with retry logic."""
        url = f"{cls.BASE_URL}/{endpoint}"

        for attempt in range(retries):
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=cls.TIMEOUT
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:
                logger.warning(f"API request failed (attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"API request failed after {retries} attempts")
                    raise

    @classmethod
    def fetch_standings(cls):
        """Fetch current NHL standings."""
        cache_key = 'nhl_standings'
        cached = cache.get(cache_key)

        if cached:
            return cached

        try:
            data = cls._request('standings')
            cache.set(cache_key, data, 3600)  # Cache for 1 hour
            return data
        except Exception as e:
            logger.error(f"Error fetching standings: {e}")
            return None

    @classmethod
    def fetch_schedule(cls, date=None):
        """Fetch NHL schedule."""
        endpoint = 'schedule'
        params = {'date': date} if date else {}

        try:
            return cls._request(endpoint, params)
        except Exception as e:
            logger.error(f"Error fetching schedule: {e}")
            return None

    @classmethod
    def fetch_player_stats(cls, player_id):
        """Fetch player statistics."""
        cache_key = f'player_stats_{player_id}'
        cached = cache.get(cache_key)

        if cached:
            return cached

        try:
            data = cls._request(f'player/{player_id}/landing')
            cache.set(cache_key, data, 1800)  # Cache for 30 minutes
            return data
        except Exception as e:
            logger.error(f"Error fetching player stats: {e}")
            return None
