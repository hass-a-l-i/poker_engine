import numpy as np

suits = np.array(['S', 'D', 'C', 'H'])
ranks = np.array(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
rank_order = {str(rank): idx + 1 for idx, rank in enumerate(ranks)}
# ranks_A_low = np.array(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
# ranks_A_low_order = {str(rank): idx + 1 for idx, rank in enumerate(ranks_A_low)}


class Card:
    def __init__(self, card):
        if len(card) > 3 or len(card) < 2:
            raise ValueError("Valid suit and rank needed to construct Card object")
        if len(card) == 3:
            suit = card[0]
            rank = card[1:]
        else:
            suit = card[0]
            rank = card[1]
        if suit not in suits:
            raise ValueError(f"The suit {suit} does not exist.")
        if rank not in ranks:
            raise ValueError(f"The rank {rank} does not exist.")
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"|{self.suit}{self.rank}|"

    def __repr__(self):
        return f"Suit = {self.suit}, Rank = {self.rank}"

    def get_rank_numeric(self) -> int:
        return rank_order[self.rank]

