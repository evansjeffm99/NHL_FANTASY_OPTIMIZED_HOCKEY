from django.db import models
from apps.teams.models import Team

class Game(models.Model):
    """NHL Game model."""

    game_id = models.IntegerField(unique=True, db_index=True)
    game_date = models.DateField(db_index=True)
    season = models.CharField(max_length=10)

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')

    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('final', 'Final'),
        ('postponed', 'Postponed')
    ], default='scheduled')

    is_playoff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-game_date']
        indexes = [models.Index(fields=['game_date']), models.Index(fields=['season'])]

    def __str__(self):
        return f"{self.away_team.abbreviation} @ {self.home_team.abbreviation} ({self.game_date})"
