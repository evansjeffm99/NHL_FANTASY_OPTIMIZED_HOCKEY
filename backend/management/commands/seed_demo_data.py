"""Management command to seed demo data."""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding demo data...')

        # Load fixtures
        try:
            call_command('loaddata', 'backend/fixtures/teams.json')
            self.stdout.write(self.style.SUCCESS('Loaded teams fixture'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading teams: {e}'))
