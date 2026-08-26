"""
betting and raising tests
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from poker_engine.config.cfg import PokerSkeleton
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Illegal_Move import IllegalMoveError
from poker_engine.objects.Player import Player
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table


cfg = PokerSkeleton()


class BettingTests(unittest.TestCase):
    def make_players(self, chips):
        return [Player(f"p{idx}", stack) for idx, stack in enumerate(chips)]

    def test_blinds_are_posted_to_stakes_and_pot(self):
        players = self.make_players([1000, 1000, 1000])
        rnd = Round(players)

        rnd.post_blinds(small_blind_idx=1, big_blind_idx=2)

        self.assertEqual(players[1].chips, 950)
        self.assertEqual(players[1].current_bet, 50)
        self.assertEqual(players[1].total_stake, 50)
        self.assertEqual(players[2].chips, 900)
        self.assertEqual(players[2].current_bet, 100)
        self.assertEqual(players[2].total_stake, 100)
        self.assertEqual(rnd.pot, 150)
        self.assertEqual(rnd.highest_bet, 100)

    def test_short_blind_posts_all_in_for_available_stack(self):
        players = self.make_players([1000, 25])
        rnd = Round(players)

        rnd.post_blinds(small_blind_idx=1, big_blind_idx=0)

        self.assertEqual(players[1].chips, 0)
        self.assertEqual(players[1].current_bet, 25)
        self.assertEqual(players[1].total_stake, 25)
        self.assertTrue(players[1].all_in)
        self.assertEqual(rnd.pot, 125)

    def test_short_stack_can_call_all_in(self):
        players = self.make_players([40, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100

        rnd.resolve_action(players[0], cfg.call, 0)

        self.assertEqual(players[0].chips, 0)
        self.assertEqual(players[0].current_bet, 40)
        self.assertEqual(players[0].total_stake, 40)
        self.assertTrue(players[0].all_in)
        self.assertEqual(rnd.pot, 40)

    def test_call_is_rejected_when_nothing_to_call(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)

        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.call, 0)

    def test_check_is_rejected_when_player_has_not_matched_bet(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100

        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.check, 0)

    def test_bet_validation_rejects_invalid_amounts(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)

        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.bet, 0)
        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.bet, 1001)
        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.bet, cfg.big_blind - 1)

    def test_bet_below_big_blind_is_allowed_when_all_in(self):
        players = self.make_players([40, 1000])
        rnd = Round(players)

        rnd.resolve_action(players[0], cfg.bet, 40)

        self.assertEqual(players[0].chips, 0)
        self.assertEqual(players[0].current_bet, 40)
        self.assertTrue(players[0].all_in)
        self.assertEqual(rnd.highest_bet, 40)

    def test_bet_is_rejected_after_betting_opened(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100

        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.bet, 200)

    def test_raise_validation_rejects_invalid_amounts(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100
        rnd.min_raise = 100

        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.raise_, 0)
        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.raise_, 50)
        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.raise_, 1000)

    def test_unknown_action_is_rejected(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)

        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], 999, 0)

    def test_min_raise_is_enforced_unless_all_in(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100
        rnd.min_raise = 100

        with self.assertRaises(IllegalMoveError):
            rnd.resolve_action(players[0], cfg.raise_, 50)

        players[0].chips = 120
        rnd.resolve_action(players[0], cfg.raise_, 20)

        self.assertEqual(players[0].chips, 0)
        self.assertEqual(players[0].current_bet, 120)
        self.assertTrue(players[0].all_in)

    def test_side_pots_use_total_stake_and_active_eligibility(self):
        players = self.make_players([0, 0, 0])
        players[0].total_stake = 100
        players[1].total_stake = 300
        players[2].total_stake = 500
        players[0].active = True
        players[1].active = False
        players[2].active = True
        table = Table(players=players, deck=Deck.initialise(), rnd=Round(players))

        pots = table.build_side_pots()

        self.assertEqual([pot["amount"] for pot in pots], [300, 400, 200])
        self.assertEqual([[player.name for player in pot["eligible"]] for pot in pots], [
            ["p0", "p2"],
            ["p2"],
            ["p2"],
        ])

    def test_side_pots_are_distributed_to_each_pot_winner(self):
        players = self.make_players([0, 0, 0])
        players[0].total_stake = 100
        players[1].total_stake = 300
        players[2].total_stake = 300
        players[0].score = (9, 13)
        players[1].score = (2, 10, 9, 8, 7)
        players[2].score = (3, 4, 3, 13)
        table = Table(players=players, deck=Deck.initialise(), rnd=Round(players))
        table.winners = [players[0]]

        table.distribute_winnings()

        self.assertEqual(players[0].chips, 300)
        self.assertEqual(players[1].chips, 0)
        self.assertEqual(players[2].chips, 400)


if __name__ == "__main__":
    unittest.main()
