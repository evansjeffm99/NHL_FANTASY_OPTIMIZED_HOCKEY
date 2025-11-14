"""
URL configuration for teams endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, TeamScheduleViewSet

app_name = 'teams'

router = DefaultRouter()
router.register(r'', TeamViewSet, basename='team')
router.register(r'schedules', TeamScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]
