from poker_engine.objects.Card import Card
from poker_engine.config.cfg import PokerSkeleton

cfg = PokerSkeleton()

class Player:
    def __init__(self, name:str, chips:int, hand:list[Card]=None) -> None:
        self.name = name
        self.chips = chips
        self.hand = [] if hand is None else hand
        self.current_bet = 0
        self.active:bool = True
        self.score: tuple[int, ...] | None = None

    def __repr__(self) -> str:
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
        if len(self.hand) == 2:
            raise ValueError(f"{self.name} has ({len(self.hand)}) in their hand already.")
        elif len(self.hand) > 2:
            raise ValueError(f"{self.name} has too many ({len(self.hand)}) cards in their hand.")
        return True
    def hand_type_check(self) -> bool:
        if not all(isinstance(card, Card) for card in self.hand):
            raise TypeError("Hand includes non Card objects.")
        return True

    """hand manipulation"""
    def get_hand(self) -> list[Card]:
        return self.hand
    def add_card(self, card:Card) -> None:
        check = self.hand_len_check() and self.hand_type_check()
        if check:
            self.hand.append(card)
    def show_hand(self) -> str:
        if self.hand_type_check:
            return "  ".join([str(card) for card in self.hand])
        return ""
    def hand_rank(self) -> int:
        if self.hand_type_check:
            return sum(card.get_rank_numeric() for card in self.hand)
        return -1
    def pop(self, idx=None) -> Card:
        idx = 0 if idx is None else idx
        return self.hand.pop(idx)

    """inherited methods"""
    def decision(self,
                 legal_actions: list[int],
                 call:int):
        raise NotImplementedError("Decision needed in child class")




