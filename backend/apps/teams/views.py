"""
Team views for API endpoints.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q

from .models import Team, TeamSchedule
from .serializers import TeamSerializer, TeamScheduleSerializer, TeamStandingsSerializer
from .services import TeamService


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for NHL teams.

    Provides CRUD operations and additional endpoints for team data.
    """

    queryset = Team.objects.filter(is_active=True)
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conference', 'division', 'is_active']
    search_fields = ['name', 'location', 'abbreviation']
    ordering_fields = ['points', 'wins', 'power_ranking', 'name']
    ordering = ['-points']

    @extend_schema(
        summary='Get team standings',
        description='Retrieve current NHL standings organized by conference and division',
        responses={200: TeamStandingsSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def standings(self, request):
        """Get current NHL standings."""
        teams = self.get_queryset().order_by('-points', '-wins', 'games_played')
        serializer = TeamStandingsSerializer(teams, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Get team statistics',
        description='Retrieve detailed statistics for a specific team',
        responses={200: TeamSerializer}
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get detailed team statistics."""
        team = self.get_object()
        stats = TeamService.get_team_stats(team)
        return Response(stats)

    @extend_schema(
        summary='Get team schedule strength',
        description='Calculate and retrieve schedule strength metrics',
        parameters=[
            OpenApiParameter('season', str, description='Season (e.g., 2024-2025)'),
            OpenApiParameter('week', int, description='Week number'),
        ],
        responses={200: dict}
    )
    @action(detail=True, methods=['get'])
    def schedule_strength(self, request, pk=None):
        """Get team schedule strength analysis."""
        team = self.get_object()
        season = request.query_params.get('season')
        week = request.query_params.get('week')

        strength = TeamService.calculate_schedule_strength(
            team,
            season=season,
            week=week
        )
        return Response(strength)


class TeamScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for team schedules.

    Manages fantasy week schedules and strength of schedule data.
    """

    queryset = TeamSchedule.objects.all()
    serializer_class = TeamScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['team', 'season', 'week_number']
    ordering_fields = ['week_number', 'schedule_difficulty', 'games_count']
    ordering = ['week_number']

    @extend_schema(
        summary='Get weekly matchups',
        description='Retrieve all matchups for a specific fantasy week',
        parameters=[
            OpenApiParameter('season', str, required=True),
            OpenApiParameter('week', int, required=True),
        ],
        responses={200: TeamScheduleSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def weekly_matchups(self, request):
        """Get all team schedules for a specific week."""
        season = request.query_params.get('season')
        week = request.query_params.get('week')

        if not season or not week:
            return Response(
                {'error': 'Both season and week parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        schedules = self.get_queryset().filter(
            season=season,
            week_number=week
        ).order_by('-games_count', 'team__abbreviation')

        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Get best weekly matchups',
        description='Find teams with the best schedules for a given week',
        parameters=[
            OpenApiParameter('season', str, required=True),
            OpenApiParameter('week', int, required=True),
            OpenApiParameter('limit', int, description='Number of results (default: 10)'),
        ],
        responses={200: TeamScheduleSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def best_matchups(self, request):
        """Get teams with best schedules for the week."""
        season = request.query_params.get('season')
        week = request.query_params.get('week')
        limit = int(request.query_params.get('limit', 10))

        if not season or not week:
            return Response(
                {'error': 'Both season and week parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        best = TeamService.get_best_weekly_matchups(season, week, limit)
        serializer = self.get_serializer(best, many=True)
        return Response(serializer.data)
