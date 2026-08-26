import random
import copy
from poker_engine.objects.Card import Card
from poker_engine.config.cfg import PokerSkeleton
import logging

cfg = PokerSkeleton()
logger = logging.getLogger(__name__)

class Deck:
    def __init__(self, deck:list[Card]=None) -> None:
        """create a deck from an optional list of cards."""
        self.state:list[Card] = [] if deck is None else deck
    def __str__(self) -> str:
        """return the printable deck order."""
        return " ".join([str(card) for card in self.state])
    def __len__(self) -> int:
        """return the number of cards in the deck."""
        return len(self.state)
    def __getitem__(self, item):
        """return a card or slice from the deck."""
        return self.state[item]

    @classmethod
    def initialise(cls) -> "Deck":
        """create and validate a full standard deck."""
        cards = [Card(f"{s}{r}") for s in cfg.suits for r in cfg.ranks]
        deck_obj = cls(cards)
        deck_obj.validate()
        logging.debug("Deck Initialised")
        return deck_obj

    def pop(self, idx=None) -> Card:
        """remove and return a card from the deck."""
        idx = 0 if idx is None else idx
        return self.state.pop(idx)
    def validate(self) -> None:
        """validate that the deck contains one full set of cards."""
        no_cards:int = len(self.state)
        if not all(isinstance(card, Card) for card in self.state):
            logger.error("Deck does not contain all card objects")
            raise TypeError("Deck does not contain all card objects")
        if no_cards != 52:
            logger.error("Deck does not contain 52 cards")
            raise ValueError("Deck does not contain 52 cards")
        card_keys = [(card.suit, card.rank) for card in self.state]
        if len(set(card_keys)) != 52:
            logger.error("Deck contains duplicate cards")
            raise ValueError("Deck contains duplicate cards")
    def shuffle(self) -> None:
        """shuffle the deck and validate the result."""
        random.shuffle(self.state)
        logging.debug("Deck Shuffled")
        self.validate()
    def copy(self) -> "Deck":
        """return a deep copy of the deck."""
        return copy.deepcopy(self)
    def add(self, cards:list[Card]) -> None:
        """append cards back into the deck."""
        for card in cards:
            if not isinstance(card, Card):
                raise TypeError("Deck can only contain Card objects")
            self.state.append(card)




