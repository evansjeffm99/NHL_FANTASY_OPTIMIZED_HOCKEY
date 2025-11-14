"""
Admin configuration for team models.
"""

from django.contrib import admin
from .models import Team, TeamSchedule


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin for Team model."""

    list_display = [
        'abbreviation', 'name', 'conference', 'division',
        'wins', 'losses', 'points', 'power_ranking', 'is_active'
    ]
    list_filter = ['conference', 'division', 'is_active']
    search_fields = ['name', 'location', 'abbreviation']
    ordering = ['-points', '-wins']

    fieldsets = (
        ('Basic Information', {
            'fields': ('team_id', 'abbreviation', 'name', 'location', 'conference', 'division')
        }),
        ('Branding', {
            'fields': ('logo_url', 'primary_color', 'secondary_color')
        }),
        ('Season Statistics', {
            'fields': (
                'wins', 'losses', 'overtime_losses', 'points',
                'goals_for', 'goals_against'
            )
        }),
        ('Advanced Statistics', {
            'fields': (
                'power_play_percentage', 'penalty_kill_percentage',
                'shots_per_game', 'shots_allowed_per_game'
            )
        }),
        ('Rankings', {
            'fields': ('power_ranking', 'strength_of_schedule')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    readonly_fields = ['created_at', 'updated_at']


@admin.register(TeamSchedule)
class TeamScheduleAdmin(admin.ModelAdmin):
    """Admin for TeamSchedule model."""

    list_display = [
        'team', 'season', 'week_number', 'games_count',
        'back_to_back_games', 'schedule_difficulty'
    ]
    list_filter = ['season', 'week_number']
    search_fields = ['team__name', 'team__abbreviation']
    ordering = ['season', 'week_number', 'team']

    fieldsets = (
        ('Basic Information', {
            'fields': ('team', 'season', 'week_number', 'week_start_date', 'week_end_date')
        }),
        ('Games', {
            'fields': ('games_count', 'home_games', 'away_games', 'back_to_back_games', 'off_nights')
        }),
        ('Strength Metrics', {
            'fields': ('opponent_strength_avg', 'schedule_difficulty')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    readonly_fields = ['created_at', 'updated_at']
