"""
Celery configuration for NHL Fantasy Optimizer.

This module configures Celery for background task processing and scheduled jobs.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('nhl_fantasy_optimizer')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    'fetch-nhl-data-nightly': {
        'task': 'apps.optimizers.tasks.fetch_nhl_data_task',
        'schedule': crontab(hour=3, minute=0),  # 3 AM daily
    },
    'update-team-standings': {
        'task': 'apps.teams.tasks.update_standings_task',
        'schedule': crontab(hour=4, minute=0),  # 4 AM daily
    },
    'update-player-stats': {
        'task': 'apps.players.tasks.update_player_stats_task',
        'schedule': crontab(hour=5, minute=0),  # 5 AM daily
    },
    'calculate-power-rankings': {
        'task': 'apps.optimizers.tasks.calculate_power_rankings_task',
        'schedule': crontab(hour=6, minute=0),  # 6 AM daily
    },
    'clean-old-cache': {
        'task': 'apps.optimizers.tasks.clean_cache_task',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Weekly on Sunday at 2 AM
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f'Request: {self.request!r}')
