"""
Team serializers for API request/response handling.
"""

from rest_framework import serializers
from .models import Team, TeamSchedule


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model."""

    games_played = serializers.IntegerField(read_only=True)
    win_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        read_only=True
    )
    goal_differential = serializers.IntegerField(read_only=True)
    points_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Team
        fields = [
            'id', 'team_id', 'abbreviation', 'name', 'location',
            'conference', 'division', 'logo_url', 'primary_color',
            'secondary_color', 'wins', 'losses', 'overtime_losses',
            'points', 'goals_for', 'goals_against', 'games_played',
            'win_percentage', 'goal_differential', 'points_percentage',
            'power_play_percentage', 'penalty_kill_percentage',
            'shots_per_game', 'shots_allowed_per_game',
            'power_ranking', 'strength_of_schedule', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamScheduleSerializer(serializers.ModelSerializer):
    """Serializer for TeamSchedule model."""

    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        write_only=True
    )

    class Meta:
        model = TeamSchedule
        fields = [
            'id', 'team', 'team_id', 'season', 'week_number',
            'week_start_date', 'week_end_date', 'games_count',
            'home_games', 'away_games', 'back_to_back_games',
            'off_nights', 'opponent_strength_avg', 'schedule_difficulty',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamStandingsSerializer(serializers.ModelSerializer):
    """Simplified serializer for team standings."""

    games_played = serializers.IntegerField(read_only=True)
    win_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        read_only=True
    )
    goal_differential = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'abbreviation', 'name', 'conference', 'division',
            'wins', 'losses', 'overtime_losses', 'points',
            'goals_for', 'goals_against', 'games_played',
            'win_percentage', 'goal_differential', 'power_ranking'
        ]
