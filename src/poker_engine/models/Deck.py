import numpy as np
from poker_engine.models.Cards import Card
import poker_engine.config.global_vars as gv
start_deck = gv.start_deck


class Deck:
    def __init__(self) -> None:
        self.state = []

    def __str__(self) -> str:
        if all(isinstance(card, Card) for card in self.state):
            return " ".join([str(card) for card in self.state])
        else:
            raise Exception("Deck does not contain all card objects")

    def __len__(self) -> int:
        return len(self.state)

    def initialise(self) -> None:
        for card in start_deck:
            card_in = Card(card)
            self.state.append(card_in)

    def shuffle(self):
        if all(isinstance(card, Card) for card in self.state):
            if len(self.state) == 52:
                deck_ind = np.array(range(0, 52))
                shuffle = np.random.choice(deck_ind, len(deck_ind), replace=False)
                self.state = np.array([self.state[i] for i in shuffle])
            else:
                raise Exception("Deck does not contain 52 cards")
        else:
            raise Exception("Deck does not contain all card objects")

