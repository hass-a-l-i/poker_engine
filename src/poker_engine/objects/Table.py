from poker_engine.objects.Card import Card
from poker_engine.objects.Player import Player
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.HandEval import HandEval

# ---------------


class Table:
    def __init__(self, players:list[Player], deck:Deck, rnd:Round, cards:list[Card]=None) -> None:
        self.cards = [] if cards is None else cards
        self.players = players
        self.deck = deck
        self.round = rnd
        self.ranked_players = []

    """helpers"""
    def _community_cards(self) -> str:
        return " ".join([str(card) for card in self.cards])
    def _deal(self) -> None:
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                player.add_card(card)

    """main"""
    def _update_table(self, no_cards:int) -> None:
        for _ in range(no_cards):
            card: Card = self.deck.pop()
            self.cards.append(card)

    def init_round(self, round_name:str, no_cards:int=None):
        print("-----------------------------------")
        print(round_name)
        fold_check = len([p for p in self.players if p.active])
        if fold_check == 1:
            print("All players folded.")
        if round_name == "Pre-Flop":
            self.round.run()
        else:
            self._update_table(no_cards)
            print(self._community_cards())
            self.round.run()

    def resolve_winner(self):
        pass

    def run(self):
        self.deck.shuffle()
        self._deal()
        self.init_round(round_name="Pre-Flop")
        self.init_round(round_name="Flop", no_cards=3)
        self.init_round(round_name="River", no_cards=1)
        self.init_round(round_name="Turn", no_cards=1)
        for p in self.players:
            all_cards = self.cards + p.hand
            rank = HandEval().evaluate(all_cards)
            self.ranked_players.append((p, rank))
        self.ranked_players.sort(key=lambda item: item[1])
        print([(p.name, rank) for (p, rank) in self.ranked_players])
