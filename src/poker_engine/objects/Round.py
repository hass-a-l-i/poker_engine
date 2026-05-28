from poker_engine.objects.Player import Player
from poker_engine.objects.Illegal_Move import IllegalMoveError
from poker_engine.config.cfg import PokerSkeleton

cfg = PokerSkeleton()


class Round:
    def __init__(self, players:list[Player]) -> None:
        self.players = players
        self.pot:int = 0
        self.log:list[tuple[Player, int]] = []
        self.highest_bet = 0
        self.player_idx = 0
        self.players_to_act = len(self.players)

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
            print(f"{player.name} folded")
            self.players_to_act -= 1
        elif action == cfg.check:
            if self.highest_bet != player.current_bet:
                raise IllegalMoveError("Cannot check here.")
            else:
                print(f"{player.name} checks.")
                self.players_to_act -= 1
        elif action == cfg.call:
            call = self.highest_bet - player.current_bet
            if call <= 0:
                raise IllegalMoveError(f"Cannot call. Highest bet > player current bet.")
            player.current_bet += call
            self.pot += call
            player.chips -= call
            print(f"{player.name} calls with {call}.")
            self.players_to_act -= 1
        elif action == cfg.bet:
            if bet_amount <= 0:
                raise IllegalMoveError(f"Bet must be >= 0.")
            if bet_amount > player.chips:
                raise IllegalMoveError(f"Bet amount cannot be more than chips available ({player.chips}).")
            self.highest_bet = bet_amount + player.current_bet
            player.current_bet += bet_amount
            player.chips -= bet_amount
            self.pot += bet_amount
            self.players_to_act = self._count_active() - 1
            print(f"{player.name} bets {bet_amount}.")
        elif action == cfg.raise_:
            raise_amount = bet_amount
            if raise_amount <= 0:
                raise IllegalMoveError(f"Raise must be >= 0.")
            call_amount = self.highest_bet - player.current_bet
            if call_amount < 0:
                raise IllegalMoveError(f"Cannot raise on own bet.")
            stake = raise_amount + call_amount
            self.highest_bet = stake + player.current_bet
            player.current_bet += stake
            player.chips -= stake
            self.pot += stake
            self.players_to_act = self._count_active() - 1
            print(f"{player.name} calls with {call_amount} and raises by {raise_amount}.")


    def run(self):
        while not self.end_round():
            player = self._current_player
            # self.information(player)
            allowed_actions = self._legal_move(player)
            while True:
                try:
                    action, amount = player.decision(allowed_actions, call=self.highest_bet - player.current_bet)
                    self.resolve_action(player, action, bet_amount=amount)
                    break
                except IllegalMoveError as e:
                    print(f"########## ILLEGAL MOVE: {e} Please try again ########## ")
            self._next_player()
        # for p in self.players:
        #     print(f"{p.name} : {p.chips}")

        # reset
        self.players_to_act = len([p for p in self.players if p.active])
        self.highest_bet = 0
        for player in self.players:
            player.current_bet = 0







