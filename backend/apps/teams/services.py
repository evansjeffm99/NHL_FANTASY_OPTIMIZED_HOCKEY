"""
Team services for business logic and analytics.
"""

from django.db.models import Avg, Sum, Count, Q
from django.core.cache import cache
from .models import Team, TeamSchedule
import logging

logger = logging.getLogger(__name__)


class TeamService:
    """Service class for team-related operations."""

    @staticmethod
    def get_team_stats(team):
        """Get comprehensive team statistics."""
        stats = {
            'basic': {
                'wins': team.wins,
                'losses': team.losses,
                'overtime_losses': team.overtime_losses,
                'points': team.points,
                'games_played': team.games_played,
                'win_percentage': float(team.win_percentage),
            },
            'scoring': {
                'goals_for': team.goals_for,
                'goals_against': team.goals_against,
                'goal_differential': team.goal_differential,
                'goals_per_game': team.goals_for / max(team.games_played, 1),
                'goals_allowed_per_game': team.goals_against / max(team.games_played, 1),
            },
            'special_teams': {
                'power_play_percentage': float(team.power_play_percentage),
                'penalty_kill_percentage': float(team.penalty_kill_percentage),
            },
            'shots': {
                'shots_per_game': float(team.shots_per_game),
                'shots_allowed_per_game': float(team.shots_allowed_per_game),
            },
            'rankings': {
                'power_ranking': team.power_ranking,
                'strength_of_schedule': float(team.strength_of_schedule),
            }
        }

        return stats

    @staticmethod
    def calculate_schedule_strength(team, season=None, week=None):
        """Calculate schedule strength for a team."""
        cache_key = f'schedule_strength_{team.id}_{season}_{week}'
        cached = cache.get(cache_key)

        if cached:
            return cached

        query = TeamSchedule.objects.filter(team=team)

        if season:
            query = query.filter(season=season)

        if week:
            query = query.filter(week_number=week)

        aggregates = query.aggregate(
            avg_games=Avg('games_count'),
            total_back_to_backs=Sum('back_to_back_games'),
            total_off_nights=Sum('off_nights'),
            avg_opponent_strength=Avg('opponent_strength_avg'),
            avg_difficulty=Avg('schedule_difficulty'),
        )

        result = {
            'team': team.abbreviation,
            'season': season,
            'week': week,
            'average_games_per_week': aggregates['avg_games'] or 0,
            'total_back_to_backs': aggregates['total_back_to_backs'] or 0,
            'total_off_nights': aggregates['total_off_nights'] or 0,
            'average_opponent_strength': aggregates['avg_opponent_strength'] or 0,
            'average_difficulty': aggregates['avg_difficulty'] or 0,
        }

        cache.set(cache_key, result, 3600)  # Cache for 1 hour
        return result

    @staticmethod
    def get_best_weekly_matchups(season, week, limit=10):
        """Get teams with the best schedules for a specific week."""
        schedules = TeamSchedule.objects.filter(
            season=season,
            week_number=week
        ).select_related('team').order_by(
            '-games_count',
            'schedule_difficulty',
            '-off_nights'
        )[:limit]

        return schedules

    @staticmethod
    def update_power_rankings():
        """Update power rankings for all teams based on current performance."""
        teams = Team.objects.filter(is_active=True).order_by(
            '-points',
            '-goal_differential',
            '-wins'
        )

        for rank, team in enumerate(teams, start=1):
            team.power_ranking = rank
            team.save(update_fields=['power_ranking', 'updated_at'])

        logger.info(f"Updated power rankings for {teams.count()} teams")
        return teams.count()
