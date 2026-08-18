from .Card import Card
from poker_engine.config.cfg import PokerSkeleton as cfg
from typing import Any


class HandEval:
    def __init__(self, all_cards:list[Card]) -> None:
        self.all_cards = all_cards
        self.ord_ranks = [c.get_rank_numeric() for c in all_cards]

    @staticmethod
    def _counter(ranks: list[Any]) -> dict[int, int]:
        counts:dict[int, int] = {}
        ctr = 1
        current = -1
        for r in ranks:
            if r == current:
                ctr += 1
            else:
                ctr = 1
            if ctr > 1:
                counts[current] = ctr
            current = r
        return counts

    @staticmethod
    def is_pair(repeat_vals: list[int]) -> bool:
        if repeat_vals.count(2) == 1:
            return True
        return False

    @staticmethod
    def is_two_pair(repeat_vals: list[int]) -> bool:
        if repeat_vals.count(2) == 2:
            return True
        return False

    @staticmethod
    def is_three_kind(repeat_vals: list[int]) -> bool:
        if 3 in repeat_vals:
            return True
        return False

    @staticmethod
    def is_four_kind(repeat_vals: list[int]) -> bool:
        if 4 in repeat_vals:
            return True
        return False

    @staticmethod
    def is_full_house(repeat_vals: list[int]) -> bool:
        if 3 in repeat_vals and 2 in repeat_vals:
            return True
        return False

    @staticmethod
    def is_flush(repeat_vals: list[int]) -> bool:
        if any(n >= 5 for n in repeat_vals):
            return True
        return False

    @staticmethod
    def is_straight(ranks:list[int]) -> bool:
        wheel_straight:set[int] = {1,2,3,4,13}
        rank_set:set = set(ranks)
        if wheel_straight.issubset(rank_set):
            return True
        ranks = sorted(list(rank_set))
        ctr:int = 1
        cand:int = ranks[0]
        for r in ranks[1:]:
            if r - cand == 1:
                ctr += 1
                if ctr >= 5:
                    return True
            else:
                ctr = 1
            cand = r
        return False

    def _return_ranking(self):
        self.ord_ranks.sort()
        cnt_ranks = self._counter(self.ord_ranks)
        ord_suits = [c.get_suit_numeric() for c in self.all_cards]
        ord_suits.sort()
        cnt_suits = self._counter(ord_suits)
        rank_repeats = list(cnt_ranks.values())
        suit_repeats = list(cnt_suits.values())
        if {9, 10, 11, 12, 13}.issubset(set(self.ord_ranks)) and self.is_flush(suit_repeats):
            return cfg.hands_dict["Royal Flush"], "Royal Flush"
        elif self.is_straight(self.ord_ranks) and self.is_flush(suit_repeats):
            return cfg.hands_dict["Straight Flush"], "Straight Flush"
        elif self.is_four_kind(rank_repeats):
            return cfg.hands_dict["Four of a Kind"], "Four of a Kind"
        elif self.is_full_house(rank_repeats):
            return cfg.hands_dict["Full House"], "Full House"
        elif self.is_flush(suit_repeats):
            return cfg.hands_dict["Flush"], "Flush"
        elif self.is_straight(self.ord_ranks):
            return cfg.hands_dict["Straight"], "Straight"
        elif self.is_three_kind(rank_repeats):
            return cfg.hands_dict["Three of a Kind"], "Three of a Kind"
        elif self.is_two_pair(rank_repeats):
            return cfg.hands_dict["Two Pair"], "Two Pair"
        elif self.is_pair(rank_repeats):
            return cfg.hands_dict["Pair"], "Pair"
        else:
            return cfg.hands_dict["High Card"], "High Card"


    def _top_five(self, hand_rank):
        if (hand_rank == cfg.hands_dict["Straight"]
            or hand_rank == cfg.hands_dict["Straight Flush"]):
            replaced = [0 if x == 13 else x for x in self.ord_ranks]
            replaced.sort(reverse=True)
            high = replaced[0:5]
            high = tuple(high)
        else:
            self.ord_ranks.sort(reverse=True)
            high = self.ord_ranks[0:5]
            high = tuple(high)
        return high


    def score_tuple(self):
        num_ranking, str_ranking = self._return_ranking()
        five = self._top_five(num_ranking)
        score = (num_ranking,) + five
        return score, str_ranking



