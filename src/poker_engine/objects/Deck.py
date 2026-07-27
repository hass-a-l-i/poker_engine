import random
import copy
from poker_engine.objects.Card import Card
from poker_engine.config.cfg import PokerSkeleton
import logging

cfg = PokerSkeleton()
logger = logging.getLogger(__name__)

class Deck:
    def __init__(self, deck:list[Card]=None) -> None:
        self.state:list[Card] = [] if deck is None else deck
    def __str__(self) -> str:
        return " ".join([str(card) for card in self.state])
    def __len__(self) -> int:
        return len(self.state)
    def __getitem__(self, item):
        return self.state[item]

    @classmethod
    def initialise(cls) -> "Deck":
        cards = [Card(f"{s}{r}") for s in cfg.suits for r in cfg.ranks]
        deck_obj = cls(cards)
        deck_obj.validate()
        logging.debug("Deck Initialised")
        return deck_obj

    def pop(self, idx=None) -> Card:
        idx = 0 if idx is None else idx
        return self.state.pop(idx)
    def validate(self) -> None:
        no_cards:int = len(self.state)
        if not all(isinstance(card, Card) for card in self.state):
            logger.error("Deck does not contain all card objects")
            raise TypeError("Deck does not contain all card objects")
        if no_cards != 52:
            logger.error("Deck does not contain 52 cards")
            raise ValueError("Deck does not contain 52 cards")
    def shuffle(self) -> None:
        random.shuffle(self.state)
        logging.debug("Deck Shuffled")
        self.validate()
    def copy(self) -> "Deck":
        return copy.deepcopy(self)
    def add(self, cards:list[Card]) -> None:
        for card in cards:
            self.state.append(card)




