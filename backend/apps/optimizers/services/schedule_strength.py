"""Schedule strength analysis service."""
from apps.teams.models import Team, TeamSchedule
from django.db.models import Avg
import logging

logger = logging.getLogger(__name__)


class ScheduleStrengthService:
    """Service for analyzing schedule strength."""

    @staticmethod
    def analyze_week(season, week_number):
        """Analyze schedule strength for a specific week."""
        schedules = TeamSchedule.objects.filter(
            season=season,
            week_number=week_number
        ).select_related('team')

        analysis = []
        for schedule in schedules:
            analysis.append({
                'team': schedule.team.abbreviation,
                'games': schedule.games_count,
                'difficulty': float(schedule.schedule_difficulty),
                'off_nights': schedule.off_nights,
                'back_to_backs': schedule.back_to_back_games
            })

        return sorted(analysis, key=lambda x: (-x['games'], x['difficulty']))
