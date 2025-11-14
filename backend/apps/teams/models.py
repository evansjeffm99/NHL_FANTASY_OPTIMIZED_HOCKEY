"""
Team models for NHL franchise data and statistics.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    """
    NHL Team model representing franchise information and current season stats.
    """

    # Basic Information
    team_id = models.IntegerField(
        unique=True,
        db_index=True,
        help_text=_('Official NHL API team ID')
    )

    abbreviation = models.CharField(
        max_length=3,
        unique=True,
        db_index=True,
        help_text=_('3-letter team abbreviation (e.g., TOR, MTL, NYR)')
    )

    name = models.CharField(
        max_length=100,
        help_text=_('Full team name (e.g., Toronto Maple Leafs)')
    )

    location = models.CharField(
        max_length=100,
        help_text=_('Team city/location')
    )

    conference = models.CharField(
        max_length=20,
        choices=[
            ('Eastern', 'Eastern Conference'),
            ('Western', 'Western Conference'),
        ],
        help_text=_('NHL Conference')
    )

    division = models.CharField(
        max_length=20,
        choices=[
            ('Atlantic', 'Atlantic Division'),
            ('Metropolitan', 'Metropolitan Division'),
            ('Central', 'Central Division'),
            ('Pacific', 'Pacific Division'),
        ],
        help_text=_('NHL Division')
    )

    # Branding
    logo_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('URL to team logo image')
    )

    primary_color = models.CharField(
        max_length=7,
        blank=True,
        help_text=_('Primary team color (hex code)')
    )

    secondary_color = models.CharField(
        max_length=7,
        blank=True,
        help_text=_('Secondary team color (hex code)')
    )

    # Season Statistics
    wins = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    losses = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    overtime_losses = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    goals_for = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_('Total goals scored')
    )

    goals_against = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_('Total goals allowed')
    )

    # Advanced Statistics
    power_play_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    penalty_kill_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    shots_per_game = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    shots_allowed_per_game = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    # Rankings and Strength
    power_ranking = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(32)],
        help_text=_('Current power ranking (1-32)')
    )

    strength_of_schedule = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=0.000,
        help_text=_('Strength of schedule rating')
    )

    # Metadata
    is_active = models.BooleanField(
        default=True,
        help_text=_('Is team active in current season')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')
        ordering = ['-points', '-wins']
        indexes = [
            models.Index(fields=['team_id']),
            models.Index(fields=['abbreviation']),
            models.Index(fields=['conference', 'division']),
            models.Index(fields=['-points']),
        ]

    def __str__(self):
        """String representation of team."""
        return f"{self.location} {self.name} ({self.abbreviation})"

    @property
    def games_played(self):
        """Calculate total games played."""
        return self.wins + self.losses + self.overtime_losses

    @property
    def win_percentage(self):
        """Calculate win percentage."""
        if self.games_played == 0:
            return 0.0
        return (self.wins / self.games_played) * 100

    @property
    def goal_differential(self):
        """Calculate goal differential."""
        return self.goals_for - self.goals_against

    @property
    def points_percentage(self):
        """Calculate points percentage."""
        if self.games_played == 0:
            return 0.0
        max_points = self.games_played * 2
        return (self.points / max_points) * 100


class TeamSchedule(models.Model):
    """
    Team schedule for fantasy week analysis and strength of schedule calculations.
    """

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='schedule_entries'
    )

    season = models.CharField(
        max_length=10,
        help_text=_('Season identifier (e.g., 2024-2025)')
    )

    week_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(26)],
        help_text=_('Fantasy week number')
    )

    week_start_date = models.DateField()
    week_end_date = models.DateField()

    # Games in this fantasy week
    games_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(7)]
    )

    home_games = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    away_games = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    back_to_back_games = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_('Number of back-to-back game situations')
    )

    off_nights = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_('Games on nights with fewer than 5 total NHL games')
    )

    # Strength metrics
    opponent_strength_avg = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=0.000,
        help_text=_('Average opponent power ranking')
    )

    schedule_difficulty = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=0.000,
        help_text=_('Composite schedule difficulty score')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('team schedule')
        verbose_name_plural = _('team schedules')
        ordering = ['season', 'week_number', 'team']
        unique_together = [['team', 'season', 'week_number']]
        indexes = [
            models.Index(fields=['team', 'season', 'week_number']),
            models.Index(fields=['week_start_date', 'week_end_date']),
        ]

    def __str__(self):
        """String representation."""
        return f"{self.team.abbreviation} - Week {self.week_number} ({self.season})"
