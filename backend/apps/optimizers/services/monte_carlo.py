"""Monte Carlo simulation service."""
import numpy as np
import logging

logger = logging.getLogger(__name__)


class MonteCarloService:
    """Service for Monte Carlo simulations."""

    @staticmethod
    def run_simulation(num_simulations=10000):
        """Run Monte Carlo simulation for team performance."""
        logger.info(f"Running {num_simulations} Monte Carlo simulations")

        # Simplified simulation
        results = []
        for _ in range(num_simulations):
            # Simulate game outcomes
            outcome = np.random.choice(['win', 'loss', 'ot_loss'], p=[0.5, 0.3, 0.2])
            results.append(outcome)

        win_probability = results.count('win') / num_simulations

        return {
            'simulations': num_simulations,
            'win_probability': round(win_probability, 4),
            'outcomes': {
                'wins': results.count('win'),
                'losses': results.count('loss'),
                'ot_losses': results.count('ot_loss')
            }
        }
