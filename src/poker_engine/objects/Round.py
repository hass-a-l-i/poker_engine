from poker_engine.objects.Player import Player
from poker_engine.objects.Illegal_Move import IllegalMoveError
from poker_engine.config.cfg import PokerSkeleton
import logging

cfg = PokerSkeleton()
logger = logging.getLogger(__name__)

class Round:
    def __init__(self, players:list[Player]) -> None:
        self.players = players
        self.pot:int = 0
        self.highest_bet = cfg.big_blind
        self.player_idx = 0
        self.players_to_act = len(self.players)
        self.burned = []

    """helpers"""
    @property
    def _current_player(self) -> Player:
        return self.players[self.player_idx]
    def _next_player(self) -> None:
        self.player_idx = (self.player_idx + 1) % len(self.players)
        while not self.players[self.player_idx].active:
            self.player_idx = (self.player_idx + 1) % len(self.players)
    def _count_active(self) -> int:
        ctr:int = 0
        for player in self.players:
            if player.active:
                ctr += 1
        return ctr
    def _legal_move(self, player: Player) -> list[int]:
        allowed = [cfg.fold]
        call = self.highest_bet - player.current_bet
        if self.highest_bet == 0:
            allowed.append(cfg.check)
            if player.chips > 0:
                allowed.append(cfg.bet)
        else:
            if player.chips >= call > 0:
                allowed.append(cfg.call)
            if call == 0:
                allowed.append(cfg.check)
            if player.chips > call:
                allowed.append(cfg.raise_)
        return allowed

    """main"""
    def information(self, player:Player) -> None:
        print(f"---------- {player.name}'s turn ----------")
        print(f"Hand : {player.show_hand()}, Pot : {self.pot}")
    def end_round(self) -> bool:
        cond1 = (self._count_active() == 1)
        cond2 = (self.players_to_act == 0)
        return cond1 or cond2
    def resolve_action(self, player, action, bet_amount):
        if action == cfg.fold:
            player.active = False
            logging.debug(f"{player.name} folded")
            self.players_to_act -= 1
        elif action == cfg.check:
            if self.highest_bet != player.current_bet:
                logging.error("Cannot check here.")
                raise IllegalMoveError("Cannot check here.")
            else:
                logging.debug(f"{player.name} checks.")
                self.players_to_act -= 1
        elif action == cfg.call:
            call = self.highest_bet - player.current_bet
            if call <= 0:
                logging.error("Cannot call. Highest bet > player current bet.")
                raise IllegalMoveError(f"Cannot call. Highest bet > player current bet.")
            player.current_bet += call
            self.pot += call
            player.chips -= call
            logging.debug(f"{player.name} calls with {call}. Chips remaining : {player.chips}")
            self.players_to_act -= 1
        elif action == cfg.bet:
            if bet_amount <= 0:
                logging.error(f"Bet must be >= 0.")
                raise IllegalMoveError(f"Bet must be >= 0.")
            if bet_amount > player.chips:
                logging.error(f"Bet amount cannot be more than chips available ({player.chips}).")
                raise IllegalMoveError(f"Bet amount cannot be more than chips available ({player.chips}).")
            self.highest_bet = bet_amount + player.current_bet
            player.current_bet += bet_amount
            player.chips -= bet_amount
            self.pot += bet_amount
            self.players_to_act = self._count_active() - 1
            logging.debug(f"{player.name} bets {bet_amount}. Chips remaining : {player.chips}")
        elif action == cfg.raise_:
            raise_amount = bet_amount
            if raise_amount <= 0:
                logging.error(f"Raise must be >= 0.")
                raise IllegalMoveError(f"Raise must be >= 0.")
            call_amount = self.highest_bet - player.current_bet
            if call_amount < 0:
                logging.error(f"Cannot raise on own bet.")
                raise IllegalMoveError(f"Cannot raise on own bet.")
            stake = raise_amount + call_amount
            self.highest_bet = stake + player.current_bet
            player.current_bet += stake
            player.chips -= stake
            self.pot += stake
            self.players_to_act = self._count_active() - 1
            logging.debug(f"{player.name} calls with {call_amount} and raises by {raise_amount}. Chips remaining : {player.chips}")

        if not player.all_in:
            if player.chips == 0:
                player.all_in = True
                logger.info(f"{player.name} is all-in!")
    def return_burned(self):
        return self.burned
    def side_pot(self):
        pass
    def reset_betting(self):
        self.players_to_act = len([p for p in self.players if p.active])
        self.highest_bet = 0
        self.player_idx = 0
        for player in self.players:
            player.current_bet = 0
    def reset_round(self):
        self.reset_betting()
        self.pot = 0
        for player in self.players:
            for card in player.hand:
                self.burned.append(card)
            player.hand = []
            player.active = True
        self.burned = []

    def run(self):
        logger.debug("Begin betting round")
        while not self.end_round():
            player = self._current_player
            allowed_actions = self._legal_move(player)
            while True:
                try:
                    action, amount = player.decision(allowed_actions, call=self.highest_bet - player.current_bet)
                    self.resolve_action(player, action, bet_amount=amount)
                    break
                except IllegalMoveError as e:
                    print(f"########## ILLEGAL MOVE: {e} Please try again ########## ")
            self._next_player()
        self.reset_betting()
        logger.debug("End betting round")









