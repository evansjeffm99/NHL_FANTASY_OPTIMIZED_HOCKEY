from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['game_date', 'away_team', 'home_team', 'away_score', 'home_score', 'status']
