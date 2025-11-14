from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PowerRanking(models.Model):
    """Team power rankings."""
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    week_number = models.IntegerField()
    rank = models.IntegerField()
    score = models.DecimalField(max_digits=8, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['team', 'season', 'week_number']]
        ordering = ['rank']


class ScheduleAnalysis(models.Model):
    """Schedule strength analysis results."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    week_number = models.IntegerField(null=True, blank=True)
    analysis_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
