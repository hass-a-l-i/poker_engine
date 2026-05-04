import inspect
from poker_engine.models.Cards import Card


class Player:
    def __init__(self, name:str, chips:int, hand:list[Card]=None) -> None:
        self.name = name
        self.chips = chips
        self.hand = [] if hand is None else hand
        self.dealer = False
        self.current_bet = 0

    def get_hand(self) -> list[Card]:
        return self.hand

    def info(self) -> None:
        current_hand = "  ".join([str(card) for card in self.hand]) if self.hand else None
        information:str = f"""
        Hand: {current_hand}
        Chips: {self.chips}
        Current bet: {self.current_bet}
        """ #
        information = inspect.cleandoc(information)
        print(information)

    @property
    def check_cards(self) -> bool:
        no_cards:int = len(self.hand)
        if not all(isinstance(card, Card) for card in self.hand):
            raise Exception("Hand includes non Card objects.")
        if no_cards >= 2:
            raise Exception(f"{self.name} has too many cards ({no_cards}) in their hand.")
        return True

    def add_card(self, card:Card) -> None:
        if self.check_cards:
            self.hand.append(card)

    def show_hand(self) -> None:
        if self.check_cards:
            print("  ".join([str(card) for card in self.hand]))

    def hand_rank(self) -> int:
        if self.check_cards:
            return sum(card.get_rank_numeric() for card in self.hand)
        return -1

    # make immmutable -> tuple?
    def get_action(self):
        pass


class Human(Player):
    pass


class Agent(Player):
    pass




"""
# no_cards:int = len(self.hand)
# if no_cards >= 2:
#     raise Exception(f"Hand must have < 2 cards. Currently have {no_cards} cards.")
# if not isinstance(card, Card):
#     raise Exception(f"Data added to hand is not Card object.")
# self.hand.append(card)
"""