from django.test import TestCase
from .models import Player

class PlayerModelTest(TestCase):
    def test_player_creation(self):
        player = Player.objects.create(
            player_id=8478402,
            first_name='Auston',
            last_name='Matthews',
            position='C'
        )
        self.assertEqual(str(player), 'Auston Matthews')
