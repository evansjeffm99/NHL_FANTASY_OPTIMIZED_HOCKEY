from django.db import models
from apps.teams.models import Team

class Player(models.Model):
    """NHL Player model."""

    player_id = models.IntegerField(unique=True, db_index=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='players')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    jersey_number = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=2, choices=[
        ('C', 'Center'), ('LW', 'Left Wing'), ('RW', 'Right Wing'),
        ('D', 'Defense'), ('G', 'Goalie')
    ])

    # Stats
    games_played = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    plus_minus = models.IntegerField(default=0)

    # Fantasy metrics
    fantasy_points = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    average_ice_time = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fantasy_points']
        indexes = [models.Index(fields=['player_id']), models.Index(fields=['team'])]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
