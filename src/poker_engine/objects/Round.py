from xml.etree.ElementPath import prepare_parent

from poker_engine.objects.Player import Player
from poker_engine.objects.Deck import Deck
from poker_engine.config.cfg import PokerSkeleton
cfg = PokerSkeleton()


class Round:
    def __init__(self, players:list[Player], deck:Deck) -> None:
        self.players = players
        self.deck = deck
        self.pot:int = 0
        self.log:list[tuple[Player, int]] = []
        self.highest_bet = 0
        self.player_idx = 0

    """helpers"""
    @property
    def _current_player(self) -> Player:
        return self.players[self.player_idx]
    def _next_player(self) -> None:
        self.player_idx = (self.player_idx + 1) % len(self.players)
        while not self.players[self.player_idx].active:
            self.player_idx = (self.player_idx + 1) % len(self.players)
    def _deal(self) -> None:
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                player.add_card(card)
    def _count_active(self) -> int:
        ctr = 0
        for player in self.players:
            if player.active:
                ctr += 1
        return ctr

    def initialise(self):
        self.deck.shuffle()
        print(self.deck)
        self._deal()
        player = self._current_player
        print(repr(player))
        player.active = False
        self._next_player()
        player = self._current_player
        print(repr(player))







    def legal_move(self, player:Player) -> list[int]:
        allowed = [cfg.fold]
        if player.current_bet == self.highest_bet:
            allowed.append(cfg.check)
            if player.chips > 0:
                allowed.append(cfg.bet)
        elif player.current_bet < self.highest_bet:
            allowed.append(cfg.call)
            if player.chips > (self.highest_bet - player.current_bet):
                allowed.append(cfg.bet)
        return allowed

    def fold(self):
        pass







