import numpy as np
from typing import Self
from poker_engine.models.Cards import Card
import poker_engine.config.global_vars as gv
from poker_engine.models.Players import Player

start_deck = gv.start_deck


class Deck:
    def __init__(self, deck:list[Card]=None) -> None:
        self.state:list[Card] = [] if deck is None else deck

    def __str__(self) -> str:
        return " ".join([str(card) for card in self.state])

    def __len__(self) -> int:
        return len(self.state)

    def __getitem__(self, item):
        return self.state[item]

    def pop(self, idx=None) -> Card:
        idx = 0 if idx is None else idx
        return self.state.pop(idx)

    def initialise(self) -> Self:
        for card in start_deck:
            card_in = Card(card)
            self.state.append(card_in)
        return self

    @property
    def check_cards(self) -> bool:
        no_cards:int = len(self.state)
        if not all(isinstance(card, Card) for card in self.state):
            raise Exception("Deck does not contain all card objects")
        if no_cards != 52:
            raise Exception("Deck does not contain 52 cards")
        return True

    def shuffle(self) -> None:
        if self.check_cards:
            deck_ind = np.array(range(0, 52))
            shuffle = np.random.choice(deck_ind, len(deck_ind), replace=False)
            self.state = [self.state[i] for i in shuffle]


