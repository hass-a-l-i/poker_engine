"""
stress testing over multiple games to prove soundness of engine
"""

import random
import sys
import unittest
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

from poker_engine.config.cfg import PokerSkeleton
from poker_engine.models.RandomAgent import RandomAgent
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table


cfg = PokerSkeleton()


class InvariantCheckingTable(Table):
    def __init__(self, *args, expected_total_chips: int, max_hands: int = 200, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_total_chips = expected_total_chips
        self.max_hands = max_hands
        self.hands_completed = 0

    def _assert_no_negative_stacks(self) -> None:
        for player in self.players:
            if player.chips < 0:
                raise AssertionError(f"{player.name} has negative chips: {player.chips}")

    def _assert_total_chips_conserved(self) -> None:
        pot_is_already_awarded = bool(self.winners)
        live_pot = 0 if pot_is_already_awarded else self.round.pot
        total_chips = sum(player.chips for player in self.players) + live_pot
        if total_chips != self.expected_total_chips:
            raise AssertionError(
                f"Chip total changed from {self.expected_total_chips} to {total_chips}"
            )

    def _assert_card_conservation(self) -> None:
        cards = []
        cards.extend(self.deck.state)
        cards.extend(self.round.burned)
        cards.extend(self.cards)
        for player in self.players:
            cards.extend(player.hand)

        card_keys = [(card.suit, card.rank) for card in cards]
        if len(card_keys) != 52:
            raise AssertionError(f"Expected 52 tracked cards, found {len(card_keys)}")
        if len(set(card_keys)) != 52:
            raise AssertionError("Duplicate cards detected in live table state")

    def reset(self):
        self._assert_no_negative_stacks()
        self._assert_total_chips_conserved()
        self._assert_card_conservation()
        super().reset()
        self._assert_no_negative_stacks()
        self._assert_total_chips_conserved()
        self._assert_card_conservation()
        self.hands_completed += 1
        if self.hands_completed >= self.max_hands:
            self.end_game = True


class EngineStressTests(unittest.TestCase):
    def run_seeded_game(self, seed: int, players_count: int, max_hands: int = 150):
        random.seed(seed)
        players = [
            RandomAgent(f"bot_{idx}", cfg.start_chips, [])
            for idx in range(players_count)
        ]
        expected_total_chips = sum(player.chips for player in players)
        rnd = Round(players)
        table = InvariantCheckingTable(
            players=players,
            deck=Deck.initialise(),
            rnd=rnd,
            expected_total_chips=expected_total_chips,
            max_hands=max_hands,
        )

        table.run()

        self.assertGreater(table.hands_completed, 0)
        self.assertLessEqual(table.hands_completed, max_hands)
        self.assertEqual(sum(player.chips for player in table.players), expected_total_chips)
        self.assertTrue(all(player.chips >= 0 for player in table.players))
        self.assertEqual(len({(card.suit, card.rank) for card in table.deck.state}), 52)
        self.assertEqual(len(table.deck), 52)

    def test_random_heads_up_games_keep_core_invariants(self):
        for seed in range(10):
            with self.subTest(seed=seed):
                self.run_seeded_game(seed=seed, players_count=2)

    def test_random_six_max_games_keep_core_invariants(self):
        for seed in range(10, 20):
            with self.subTest(seed=seed):
                self.run_seeded_game(seed=seed, players_count=6)


if __name__ == "__main__":
    unittest.main()
