from poker_engine.objects.Card import Card
from poker_engine.config.cfg import PokerSkeleton

cfg = PokerSkeleton()

class Player:
    def __init__(self, name:str, chips:int, hand:list[Card]=None) -> None:
        """create a player with chips, cards, and betting state."""
        self.name = name
        self.chips = chips
        self.hand = [] if hand is None else hand
        self.current_bet = 0
        self.active:bool = True
        self.score: tuple[int, ...] | None = None
        self.rank:str | None = None
        self.all_in:bool = False
        self.total_stake:int = 0

    def __repr__(self):
        """return the player name for debugging."""
        return self.name

    def info(self) -> str:
        """return player specific info"""
        info = (
            "-----------------------------\n"
            f"Type : Player \n"
            f"Name : {self.name} \n"
            f"Chips : {self.chips} \n"
            f"Hand : {self.show_hand()} \n"
            f"Current bet : {self.current_bet} \n"
            f"Active : {self.active} \n"
            "-----------------------------"
              )
        return info

    """guard checks"""
    def hand_len_check(self) -> bool:
        """validate that the player can receive another card."""
        if len(self.hand) == 2:
            raise ValueError(f"{self.name} has ({len(self.hand)}) in their hand already.")
        elif len(self.hand) > 2:
            raise ValueError(f"{self.name} has too many ({len(self.hand)}) cards in their hand.")
        return True
    def hand_type_check(self) -> bool:
        """validate that every card in hand is a card object."""
        if not all(isinstance(card, Card) for card in self.hand):
            raise TypeError("Hand includes non Card objects.")
        return True

    """hand manipulation"""
    def get_hand(self) -> list[Card]:
        """return the player's current hand."""
        return self.hand
    def add_card(self, card:Card) -> None:
        """add one card to the player's hand."""
        if not isinstance(card, Card):
            raise TypeError("Can only add Card objects to a player's hand.")
        check = self.hand_len_check() and self.hand_type_check()
        if check:
            self.hand.append(card)
    def show_hand(self) -> str:
        """return the printable cards in the player's hand."""
        if self.hand_type_check():
            return "  ".join([str(card) for card in self.hand])
        return ""
    def hand_rank(self) -> int:
        """return the sum of numeric ranks in the hand."""
        if self.hand_type_check():
            return sum(card.get_rank_numeric() for card in self.hand)
        return -1
    def pop(self, idx=None) -> Card:
        """remove and return a card from the player's hand."""
        idx = 0 if idx is None else idx
        return self.hand.pop(idx)

    """inherited methods"""
    def decision(self,
                 legal_actions: list[int],
                 call:int,
                 min_raise: int = cfg.big_blind):
        """require subclasses to choose a legal poker action."""
        raise NotImplementedError("Decision needed in child class")




