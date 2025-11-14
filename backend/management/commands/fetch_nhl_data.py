"""Management command to fetch NHL data."""
from django.core.management.base import BaseCommand
from services.nhl_api import NHLAPIService
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch NHL data from API'

    def handle(self, *args, **options):
        self.stdout.write('Fetching NHL data...')

        standings = NHLAPIService.fetch_standings()
        if standings:
            self.stdout.write(self.style.SUCCESS('Successfully fetched standings'))

        schedule = NHLAPIService.fetch_schedule()
        if schedule:
            self.stdout.write(self.style.SUCCESS('Successfully fetched schedule'))
