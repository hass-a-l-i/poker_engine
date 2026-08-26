from poker_engine.archive.Cards import Card
from poker_engine.archive.Players import Player
from poker_engine.archive.Deck import Deck


class Table:
    def __init__(self, cards:list[Card]=None, players:list[Player]=None, deck:Deck=None) -> None:
        self.cards = [] if cards is None else cards
        self.players = [] if players is None else players
        self.deck = None if deck is None else deck

    def community_cards(self) -> str:
        return " ".join([str(card) for card in self.cards])

    def check_table(self) -> bool:
        if not all(isinstance(card, Card) for card in self.cards):
            raise Exception("Community cards include non Card objects.")
        if not all(isinstance(player, Player) for player in self.players):
            raise Exception("Non Player types detected at table.")
        for player in self.players:
            hand:list[Card] = player.get_hand()
            no_cards: int = len(hand)
            if no_cards < 2:
                raise Exception(f"Player {player.name} has {no_cards} cards in hand. Round cannot continue.")
        return True

    def flop(self) -> None:
        no_cards = len(self.cards)
        if no_cards == 0:
            for i in range(3):
                card:Card = self.deck.pop()
                self.cards.append(card)
        else:
            raise Exception(f"Flop not possible. Currently have {no_cards} cards on table.")

    def turn(self) -> None:
        no_cards = len(self.cards)
        if no_cards == 3:
            for i in range(1):
                card:Card = self.deck.pop()
                self.cards.append(card)
        else:
            raise Exception(f"Turn not possible. Currently have {no_cards} cards on table.")

    def river(self) -> None:
        no_cards = len(self.cards)
        if no_cards == 4:
            for i in range(1):
                card:Card = self.deck.pop()
                self.cards.append(card)
        else:
            raise Exception(f"Turn not possible. Currently have {no_cards} cards on table.")

    def deal(self) -> None:
        for i in range(2):
            for player in self.players:
                card:Card = self.deck.pop()
                player.add_card(card)


