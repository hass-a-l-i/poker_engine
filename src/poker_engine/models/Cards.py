import poker_engine.config.global_vars as gv
suits = gv.suits
ranks = gv.ranks
rank_order = gv.rank_order


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

