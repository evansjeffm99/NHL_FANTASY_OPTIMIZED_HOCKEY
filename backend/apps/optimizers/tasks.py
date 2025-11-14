from celery import shared_task
from services.nhl_api import NHLAPIService
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_nhl_data_task():
    logger.info("Fetching NHL data...")
    return {'status': 'success'}

@shared_task
def calculate_power_rankings_task():
    logger.info("Calculating power rankings...")
    return {'status': 'success'}

@shared_task
def clean_cache_task():
    logger.info("Cleaning cache...")
    return {'status': 'success'}
