from .Card import Card
import random
from poker_engine.config.cfg import PokerSkeleton as cfg
from typing import Any

# cfg = PokerSkeleton()


class HandEval:
    def __init__(self):
        self.eval_tuple = ()

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

    # @staticmethod
    # def _suit_counter(ranks: list[Any]) -> dict[int, int]:
    #     suits_dict = {i: hand for i, hand in enumerate(hands_list, start=1)}
    #     counts:dict[int, int] = {}

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

    def return_rank(self, table_cards: list[Card]):
        """
        RANK HAND FIRST
        """
        # print([(str(c)) for c in table_cards])
        ord_ranks = [c.get_rank_numeric() for c in table_cards]
        ord_ranks.sort()
        cnt_ranks = self._counter(ord_ranks)
        ord_suits = [c.get_suit_numeric() for c in table_cards]
        ord_suits.sort()
        cnt_suits = self._counter(ord_suits)
        rank_repeats = list(cnt_ranks.values())
        suit_repeats = list(cnt_suits.values())
        if {9, 10, 11, 12, 13}.issubset(set(ord_ranks)) and self.is_flush(suit_repeats):
            return cfg.hands_dict["Royal Flush"]
        elif self.is_straight(ord_ranks) and self.is_flush(suit_repeats):
            return cfg.hands_dict["Straight Flush"]
        elif self.is_four_kind(rank_repeats):
            return cfg.hands_dict["Four of a Kind"]
        elif self.is_full_house(rank_repeats):
            return cfg.hands_dict["Full House"]
        elif self.is_flush(suit_repeats):
            return cfg.hands_dict["Flush"]
        elif self.is_straight(ord_ranks):
            return cfg.hands_dict["Straight"]
        elif self.is_three_kind(rank_repeats):
            return cfg.hands_dict["Three of a Kind"]
        elif self.is_two_pair(rank_repeats):
            return cfg.hands_dict["Two Pair"]
        elif self.is_pair(rank_repeats):
            return cfg.hands_dict["Pair"]
        else:
            return cfg.hands_dict["High Card"]

    # score tuple returned to all players then find max?
    def score_tuple(self):
        pass


    # if draw then do tuple of rest of cards compare
