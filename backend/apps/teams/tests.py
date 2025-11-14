"""
Tests for teams app.
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Team, TeamSchedule
from datetime import date

User = get_user_model()


class TeamModelTest(TestCase):
    """Test cases for Team model."""

    def setUp(self):
        """Set up test data."""
        self.team = Team.objects.create(
            team_id=1,
            abbreviation='TOR',
            name='Maple Leafs',
            location='Toronto',
            conference='Eastern',
            division='Atlantic',
            wins=40,
            losses=20,
            overtime_losses=5,
            points=85,
            goals_for=200,
            goals_against=150
        )

    def test_team_creation(self):
        """Test team creation."""
        self.assertEqual(self.team.abbreviation, 'TOR')
        self.assertEqual(self.team.name, 'Maple Leafs')

    def test_games_played(self):
        """Test games played calculation."""
        self.assertEqual(self.team.games_played, 65)

    def test_goal_differential(self):
        """Test goal differential calculation."""
        self.assertEqual(self.team.goal_differential, 50)

    def test_win_percentage(self):
        """Test win percentage calculation."""
        expected = (40 / 65) * 100
        self.assertAlmostEqual(self.team.win_percentage, expected, places=2)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints."""

    def setUp(self):
        """Set up test client and data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        self.team = Team.objects.create(
            team_id=1,
            abbreviation='TOR',
            name='Maple Leafs',
            location='Toronto',
            conference='Eastern',
            division='Atlantic',
            wins=40,
            losses=20,
            points=85
        )

    def test_list_teams(self):
        """Test listing teams."""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_team_detail(self):
        """Test getting team detail."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/teams/{self.team.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['abbreviation'], 'TOR')

    def test_standings_endpoint(self):
        """Test standings endpoint."""
        response = self.client.get('/api/teams/standings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
