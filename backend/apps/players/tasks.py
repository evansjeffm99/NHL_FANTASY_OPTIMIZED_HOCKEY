from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_player_stats_task():
    logger.info("Updating player stats...")
    return {'status': 'success'}
