from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PowerRankingViewSet, ScheduleAnalysisViewSet

router = DefaultRouter()
router.register(r'power-rankings', PowerRankingViewSet)
router.register(r'schedule-analysis', ScheduleAnalysisViewSet)

urlpatterns = [path('', include(router.urls))]
