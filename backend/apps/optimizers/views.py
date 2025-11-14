from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PowerRanking, ScheduleAnalysis
from .serializers import PowerRankingSerializer, ScheduleAnalysisSerializer
from .services.monte_carlo import MonteCarloService

class PowerRankingViewSet(viewsets.ModelViewSet):
    queryset = PowerRanking.objects.all()
    serializer_class = PowerRankingSerializer

class ScheduleAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ScheduleAnalysis.objects.all()
    serializer_class = ScheduleAnalysisSerializer

    @action(detail=False, methods=['post'])
    def analyze(self, request):
        """Run schedule analysis."""
        season = request.data.get('season')
        week = request.data.get('week')

        # Perform analysis
        results = {'status': 'analysis_complete', 'season': season, 'week': week}

        # Save analysis
        analysis = ScheduleAnalysis.objects.create(
            user=request.user,
            season=season,
            week_number=week,
            analysis_data=results
        )

        return Response(ScheduleAnalysisSerializer(analysis).data)

    @action(detail=False, methods=['post'])
    def monte_carlo(self, request):
        """Run Monte Carlo simulation."""
        simulations = request.data.get('simulations', 10000)
        results = MonteCarloService.run_simulation(simulations)
        return Response(results)
