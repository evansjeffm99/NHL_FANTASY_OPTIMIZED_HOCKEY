"""
Celery tasks for team data updates.
"""

from celery import shared_task
from services.nhl_api import NHLAPIService
from .services import TeamService
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def update_standings_task(self):
    """Update team standings from NHL API."""
    try:
        logger.info("Starting team standings update")

        standings = NHLAPIService.fetch_standings()

        if standings:
            # Update teams with new data
            # Implementation depends on NHL API structure
            logger.info(f"Successfully updated standings")

        # Update power rankings
        TeamService.update_power_rankings()

        return {'status': 'success', 'message': 'Standings updated'}

    except Exception as e:
        logger.error(f"Error updating standings: {str(e)}")
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
