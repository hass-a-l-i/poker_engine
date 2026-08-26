from collections import Counter
from itertools import combinations

from .Card import Card
from poker_engine.config.cfg import PokerSkeleton

cfg = PokerSkeleton()


class HandEval:
    def __init__(self, all_cards: list[Card]) -> None:
        """store and validate the cards used for hand evaluation."""
        if len(all_cards) < 5:
            raise ValueError("At least five cards are needed to evaluate a poker hand.")
        if len(all_cards) > 7:
            raise ValueError("At most seven cards can be evaluated.")
        if not all(isinstance(card, Card) for card in all_cards):
            raise TypeError("Hand evaluator only accepts Card objects.")

        self.all_cards = all_cards
        self.ord_ranks = [self._rank_value(card) for card in all_cards]

    @staticmethod
    def _rank_value(card: Card) -> int:
        """get numeric rank of a card"""
        return card.get_rank_numeric()

    @staticmethod
    def _straight_high(ranks: list[int]) -> int | None:
        """wheel straight identifier"""
        rank_set = set(ranks)
        if {13, 4, 3, 2, 1}.issubset(rank_set):
            return 4

        ordered = sorted(rank_set, reverse=True)
        for idx in range(len(ordered) - 4):
            window = ordered[idx:idx + 5]
            if window[0] - window[4] == 4:
                return window[0]
        return None

    @classmethod
    def _score_five(cls, cards: tuple[Card, ...]) -> tuple[tuple[int, ...], str]:
        """returns a five-tuple score which has rank then highest 4 cards descending"""
        ranks = [cls._rank_value(card) for card in cards]
        counts = Counter(ranks)
        count_values = sorted(counts.values(), reverse=True)
        flush = len({card.suit for card in cards}) == 1
        straight_high = cls._straight_high(ranks)

        if flush and straight_high == 13:
            return (cfg.hands_dict["Royal Flush"], 13), "Royal Flush"
        if flush and straight_high is not None:
            return (cfg.hands_dict["Straight Flush"], straight_high), "Straight Flush"

        if count_values == [4, 1]:
            quad = max(rank for rank, count in counts.items() if count == 4)
            kicker = max(rank for rank, count in counts.items() if count == 1)
            return (cfg.hands_dict["Four of a Kind"], quad, kicker), "Four of a Kind"

        if count_values == [3, 2]:
            trip = max(rank for rank, count in counts.items() if count == 3)
            pair = max(rank for rank, count in counts.items() if count == 2)
            return (cfg.hands_dict["Full House"], trip, pair), "Full House"

        if flush:
            return (cfg.hands_dict["Flush"], *sorted(ranks, reverse=True)), "Flush"

        if straight_high is not None:
            return (cfg.hands_dict["Straight"], straight_high), "Straight"

        if count_values == [3, 1, 1]:
            trip = max(rank for rank, count in counts.items() if count == 3)
            kickers = sorted((rank for rank, count in counts.items() if count == 1), reverse=True)
            return (cfg.hands_dict["Three of a Kind"], trip, *kickers), "Three of a Kind"

        if count_values == [2, 2, 1]:
            pairs = sorted((rank for rank, count in counts.items() if count == 2), reverse=True)
            kicker = max(rank for rank, count in counts.items() if count == 1)
            return (cfg.hands_dict["Two Pair"], *pairs, kicker), "Two Pair"

        if count_values == [2, 1, 1, 1]:
            pair = max(rank for rank, count in counts.items() if count == 2)
            kickers = sorted((rank for rank, count in counts.items() if count == 1), reverse=True)
            return (cfg.hands_dict["Pair"], pair, *kickers), "Pair"

        return (cfg.hands_dict["High Card"], *sorted(ranks, reverse=True)), "High Card"

    def _best(self) -> tuple[tuple[int, ...], str]:
        """returns the highest score tuple (with kickers) and rank"""
        best_score = None
        best_rank = ""
        for candidate in combinations(self.all_cards, 5):
            score, rank = self._score_five(candidate)
            if best_score is None or score > best_score:
                best_score = score
                best_rank = rank
        return best_score, best_rank

    def _return_ranking(self):
        """return the numeric hand ranking and rank name."""
        score, rank = self._best()
        return score[0], rank

    def _return_rank(self):
        """return the numeric hand ranking only."""
        score, _ = self._best()
        return score[0]

    def _top_five(self, hand_rank):
        """return the kicker values from the best score."""
        score, _ = self._best()
        return score[1:]

    def score_tuple(self):
        """return the best score tuple and rank name."""
        return self._best()
