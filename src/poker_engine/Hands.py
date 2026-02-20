import numpy as np
from Cards import Card


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        if len(self.cards) >= 2:
            raise Exception(f"Hand limited to two cards exactly. Currently hand has {len(self.cards)} cards.")
        self.cards.append(card)

    def show_hand(self):
        print("  ".join([card.__repr__() for card in self.cards]))

    def __repr__(self):
        return ", ".join([card.__repr__() for card in self.cards])

