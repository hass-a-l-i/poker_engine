"""
tests for hand evaluator
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from poker_engine.objects.Card import Card
from poker_engine.objects.HandEval import HandEval
from poker_engine.config.cfg import PokerSkeleton


CFG = PokerSkeleton()
SPADE, DIAMOND, CLUB, HEART = CFG.suits


def cards(*values):
    return [Card(f"{suit}{rank}") for suit, rank in values]


class HandEvalTests(unittest.TestCase):
    def assert_rank(self, expected, *values):
        _, rank = HandEval(cards(*values)).score_tuple()
        self.assertEqual(rank, expected)

    def test_high_card(self):
        self.assert_rank(
            "High Card",
            (HEART, "2"),
            (CLUB, "4"),
            (CLUB, "6"),
            (SPADE, "8"),
            (HEART, "10"),
            (DIAMOND, "Q"),
            (SPADE, "A"),
        )

    def test_pair(self):
        self.assert_rank(
            "Pair",
            (HEART, "2"),
            (CLUB, "4"),
            (CLUB, "2"),
            (SPADE, "8"),
            (HEART, "10"),
            (DIAMOND, "Q"),
            (SPADE, "A"),
        )

    def test_two_pair(self):
        self.assert_rank(
            "Two Pair",
            (HEART, "2"),
            (CLUB, "4"),
            (CLUB, "2"),
            (SPADE, "8"),
            (HEART, "10"),
            (DIAMOND, "Q"),
            (SPADE, "4"),
        )

    def test_three_of_a_kind(self):
        self.assert_rank(
            "Three of a Kind",
            (HEART, "2"),
            (CLUB, "5"),
            (CLUB, "2"),
            (SPADE, "8"),
            (HEART, "10"),
            (DIAMOND, "Q"),
            (SPADE, "2"),
        )

    def test_straight(self):
        self.assert_rank(
            "Straight",
            (HEART, "7"),
            (CLUB, "3"),
            (CLUB, "8"),
            (SPADE, "9"),
            (HEART, "10"),
            (DIAMOND, "Q"),
            (SPADE, "J"),
        )

    def test_flush(self):
        self.assert_rank(
            "Flush",
            (CLUB, "4"),
            (CLUB, "3"),
            (CLUB, "8"),
            (CLUB, "9"),
            (HEART, "10"),
            (DIAMOND, "4"),
            (CLUB, "J"),
        )

    def test_full_house(self):
        self.assert_rank(
            "Full House",
            (SPADE, "J"),
            (CLUB, "3"),
            (CLUB, "8"),
            (SPADE, "9"),
            (HEART, "J"),
            (DIAMOND, "3"),
            (CLUB, "J"),
        )

    def test_four_of_a_kind(self):
        self.assert_rank(
            "Four of a Kind",
            (SPADE, "J"),
            (CLUB, "3"),
            (CLUB, "8"),
            (SPADE, "9"),
            (HEART, "J"),
            (DIAMOND, "J"),
            (CLUB, "J"),
        )

    def test_straight_flush(self):
        self.assert_rank(
            "Straight Flush",
            (DIAMOND, "7"),
            (CLUB, "3"),
            (HEART, "10"),
            (HEART, "Q"),
            (HEART, "J"),
            (HEART, "8"),
            (HEART, "9"),
        )

    def test_royal_flush(self):
        self.assert_rank(
            "Royal Flush",
            (DIAMOND, "7"),
            (CLUB, "3"),
            (HEART, "K"),
            (HEART, "Q"),
            (HEART, "J"),
            (HEART, "10"),
            (HEART, "A"),
        )

    def test_straight_and_flush_must_be_same_suit_for_straight_flush(self):
        self.assert_rank(
            "Flush",
            (HEART, "2"),
            (HEART, "4"),
            (HEART, "6"),
            (HEART, "8"),
            (HEART, "Q"),
            (DIAMOND, "9"),
            (CLUB, "10"),
        )

    def test_wheel_straight_scores_lower_than_six_high_straight(self):
        wheel_score, _ = HandEval(cards(
            (SPADE, "A"),
            (DIAMOND, "2"),
            (CLUB, "3"),
            (HEART, "4"),
            (SPADE, "5"),
        )).score_tuple()
        six_high_score, _ = HandEval(cards(
            (SPADE, "2"),
            (DIAMOND, "3"),
            (CLUB, "4"),
            (HEART, "5"),
            (SPADE, "6"),
        )).score_tuple()

        self.assertLess(wheel_score, six_high_score)

    def test_pair_tie_breaker_uses_pair_rank_before_kickers(self):
        aces_score, _ = HandEval(cards(
            (SPADE, "A"),
            (DIAMOND, "A"),
            (CLUB, "2"),
            (HEART, "3"),
            (SPADE, "4"),
        )).score_tuple()
        kings_score, _ = HandEval(cards(
            (SPADE, "K"),
            (DIAMOND, "K"),
            (CLUB, "Q"),
            (HEART, "J"),
            (SPADE, "10"),
        )).score_tuple()

        self.assertGreater(aces_score, kings_score)


if __name__ == "__main__":
    unittest.main()
