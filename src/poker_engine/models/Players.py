from poker_engine.models.Cards import Card


class Player:
    def __init__(self, hand=None) -> None:
        self.hand:list[Card] = [] if hand is None else hand

    def __repr__(self) -> str:
        info:str = f"""
        Player Info:
        No. cards in hand : {len(self.hand)}
        """
        return info

    @property
    def check_cards(self) -> bool:
        no_cards:int = len(self.hand)
        if not all(isinstance(card, Card) for card in self.hand):
            raise Exception("Hand includes non Card objects.")
        if no_cards != 2:
            raise Exception(f"Hand must have 2 cards. Currently have {no_cards} cards.")
        return True

    def add_card(self, card:Card) -> None:
        no_cards:int = len(self.hand)
        if no_cards >= 2:
            raise Exception(f"Hand must have < 2 cards. Currently have {no_cards} cards.")
        if not isinstance(card, Card):
            raise Exception(f"Data added to hand is not Card object.")
        self.hand.append(card)

    def show_hand(self) -> None:
        if self.check_cards:
            print("  ".join([str(card) for card in self.hand]))

    def hand_rank(self) -> int:
        if self.check_cards:
            return sum(card.get_rank_numeric() for card in self.hand)
        return -1



