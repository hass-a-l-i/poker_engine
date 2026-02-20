import numpy as np

suits = np.array(['S', 'D', 'C', 'H'])
ranks = np.array(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
rank_order = {str(rank): idx + 1 for idx, rank in enumerate(ranks)}


class Card:
    def __init__(self, card):
        if len(card) != 2:
            raise ValueError("Suit and rank needed to construct Card object")
        suit = card[0]
        rank = card[1]
        if suit not in suits:
            raise ValueError(f"The suit {suit} does not exist.")
        if rank not in ranks:
            raise ValueError(f"The rank {rank} does not exist.")
        self.suit = suit
        self.rank = rank

    def show_card(self):
        print(f"|{self.suit}{self.rank}|")

    def __repr__(self):
        return f"|{self.suit}{self.rank}|"

    # def __len__(self):
    #     return len(card)

    def hierarchy(self):
        return rank_order[self.rank]

