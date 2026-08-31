from poker_engine.objects.Player import Player
from poker_engine.objects.Illegal_Move import IllegalMoveError
from poker_engine.config.cfg import PokerSkeleton
from poker_engine.objects.Card import Card
import logging

cfg = PokerSkeleton()
logger = logging.getLogger(__name__)


class Round:
    def __init__(self, players: list[Player]) -> None:
        """create betting state for one poker hand."""
        self.players = players
        self.pot: int = 0
        self.highest_bet = 0
        self.min_raise = cfg.big_blind
        self.player_idx = 0
        self.players_to_act = len(self.players)
        self.burned = []

    """helpers"""
    @property
    def _current_player(self) -> Player:
        """return idx of current player"""
        return self.players[self.player_idx]
    def _count_active(self) -> int:
        """no of active players"""
        return sum(1 for player in self.players if player.active)
    def _count_players_who_can_act(self) -> int:
        """players who are still able to act i.e. not all in but active"""
        return sum(1 for player in self.players if player.active and not player.all_in)
    def _has_pending_call_decision(self) -> bool:
        """true when a player can still call or fold against an unmatched bet"""
        return any(
            player.active
            and not player.all_in
            and player.current_bet < self.highest_bet
            for player in self.players
        )
    def _decrement_players_to_act(self) -> None:
        """decrease active players amount by one"""
        self.players_to_act = max(0, self.players_to_act - 1)
    def _log_all_in(self, player: Player) -> None:
        """log when a player has committed all chips."""
        if player.all_in:
            logger.info(f"{player.name} is all-in!")
    def _next_player(self) -> None:
        """find next player who is active and not all in"""
        if self._count_players_who_can_act() == 0:
            return

        for _ in range(len(self.players)):
            self.player_idx = (self.player_idx + 1) % len(self.players)
            player = self.players[self.player_idx]
            if player.active and not player.all_in:
                return
    def _legal_move(self, player: Player) -> list[int]:
        """return list of legal moves"""
        if not player.active or player.all_in:
            return []

        allowed = []
        call_amount = self.highest_bet - player.current_bet

        if call_amount > 0:
            allowed.append(cfg.fold)
            if player.chips > 0:
                allowed.append(cfg.call)
            if player.chips > call_amount:
                allowed.append(cfg.raise_)
        else:
            allowed.append(cfg.check)
            if player.chips > 0 and self._count_players_who_can_act() > 1:
                if self.highest_bet == 0:
                    allowed.append(cfg.bet)
                else:
                    allowed.append(cfg.raise_)

        return allowed
    def _commit_chips(self, player: Player, amount: int) -> int:
        """total amount committed per round"""
        if amount <= 0:
            raise IllegalMoveError("Committed amount must be positive.")

        committed = min(player.chips, amount)
        player.chips -= committed
        player.current_bet += committed
        player.total_stake += committed
        self.pot += committed

        if player.chips == 0:
            player.all_in = True

        return committed
    def _post_blind(self, player: Player, amount: int) -> int:
        """post given blind for a player"""
        blind = min(player.chips, amount)
        if blind <= 0:
            return 0
        committed = self._commit_chips(player, blind)
        self.highest_bet = max(self.highest_bet, player.current_bet)
        return committed
    def _return_burned(self) -> list[Card]:
        """returns burned cards"""
        return self.burned

    """main"""
    def end_round(self) -> bool:
        """
        conditions to check if round over. true if active players <=1 or no players can act
        """
        active_players = [player for player in self.players if player.active]
        if len(active_players) <= 1:
            if active_players:
                logger.debug(f"Only one player left: {active_players[0].name}")
            return True
        if self._count_players_who_can_act() == 0:
            return True
        if self._count_players_who_can_act() == 1 and not self._has_pending_call_decision():
            remaining_player = next(
                player for player in self.players if player.active and not player.all_in
            )
            logger.info(f"Only one player can act: {remaining_player.name}")
            return True
        return self.players_to_act <= 0
    def post_blinds(self, small_blind_idx: int, big_blind_idx: int) -> None:
        """post blinds for all players (big and small). based on button (dealer)"""
        self.highest_bet = 0
        self.min_raise = cfg.big_blind
        small_blind_player = self.players[small_blind_idx]
        big_blind_player = self.players[big_blind_idx]
        small_blind = self._post_blind(small_blind_player, cfg.small_blind)
        big_blind = self._post_blind(big_blind_player, cfg.big_blind)
        logger.info(f"{small_blind_player.name} posts small blind: {small_blind}")
        self._log_all_in(small_blind_player)
        logger.info(f"{big_blind_player.name} posts big blind: {big_blind}")
        self._log_all_in(big_blind_player)
    def resolve_action(self, player: Player, action: int, bet_amount: int) -> None:
        """Resolves (post) a chosen action"""
        if action == cfg.fold:
            player.active = False
            logger.info(f"{player.name} folded")
            self._decrement_players_to_act()
        elif action == cfg.check:
            if self.highest_bet != player.current_bet:
                logger.error("Cannot check here.")
                raise IllegalMoveError("Cannot check here.")
            logger.info(f"{player.name} checks.")
            self._decrement_players_to_act()
        elif action == cfg.call:
            call_amount = self.highest_bet - player.current_bet
            if call_amount <= 0:
                logger.error("Cannot call when there is nothing to call.")
                raise IllegalMoveError("Cannot call when there is nothing to call.")
            committed = self._commit_chips(player, call_amount)
            logger.info(f"{player.name} calls {committed}. Chips remaining : {player.chips}")
            self._log_all_in(player)
            self._decrement_players_to_act()
        elif action == cfg.bet:
            if self.highest_bet != 0:
                raise IllegalMoveError("Cannot bet after betting has opened. Use raise.")
            if bet_amount <= 0:
                logger.error("Bet must be positive.")
                raise IllegalMoveError("Bet must be positive.")
            if bet_amount > player.chips:
                raise IllegalMoveError(f"Bet amount cannot be more than chips available ({player.chips}).")
            min_bet = min(cfg.big_blind, player.chips)
            if bet_amount < min_bet and bet_amount < player.chips:
                raise IllegalMoveError(f"Minimum bet is {min_bet} unless all-in.")
            committed = self._commit_chips(player, bet_amount)
            self.highest_bet = player.current_bet
            self.min_raise = max(committed, cfg.big_blind)
            self.players_to_act = max(0, self._count_players_who_can_act() - 1)
            logger.info(f"{player.name} bets {committed}. Chips remaining : {player.chips}")
            self._log_all_in(player)
        elif action == cfg.raise_:
            raise_amount = bet_amount
            call_amount = self.highest_bet - player.current_bet
            if call_amount < 0:
                logger.error("Cannot raise on own bet.")
                raise IllegalMoveError("Cannot raise on own bet.")
            if player.chips <= call_amount:
                raise IllegalMoveError("Player cannot raise without chips beyond the call.")
            if raise_amount <= 0:
                logger.error("Raise must be positive.")
                raise IllegalMoveError("Raise must be positive.")
            total_commit = call_amount + raise_amount
            if total_commit > player.chips:
                raise IllegalMoveError(f"Raise total cannot exceed chips available ({player.chips}).")
            full_raise = raise_amount >= self.min_raise
            all_in_short_raise = total_commit == player.chips and not full_raise
            if not full_raise and not all_in_short_raise:
                raise IllegalMoveError(f"Minimum raise is {self.min_raise} unless all-in.")
            old_highest = self.highest_bet
            committed = self._commit_chips(player, total_commit)
            if player.current_bet > old_highest:
                self.highest_bet = player.current_bet
            if full_raise:
                self.min_raise = raise_amount
                self.players_to_act = max(0, self._count_players_who_can_act() - 1)
            else:
                self._decrement_players_to_act()
            logger.info(
                f"{player.name} calls {call_amount} and raises {raise_amount}. "
                f"Total committed : {committed}. Chips remaining : {player.chips}"
            )
            self._log_all_in(player)
        else:
            raise IllegalMoveError("Unknown action.")
    def reset_betting(self):
        """reset all betting params for bet phases (flop, river, turn)"""
        self.players_to_act = self._count_players_who_can_act()
        self.highest_bet = 0
        self.min_raise = cfg.big_blind
        self.player_idx = 0
        for player in self.players:
            player.current_bet = 0
    def reset_round(self):
        """reset all round params for new round"""
        self.reset_betting()
        self.pot = 0
        for player in self.players:
            for card in player.hand:
                self.burned.append(card)
            player.hand = []
            player.active = True
            player.all_in = False
            player.total_stake = 0
    def run(self, start_idx: int | None = None) -> None:
        """orchestrator function for rounds"""
        logger.debug("Begin betting round")
        if start_idx is not None and self.players:
            self.player_idx = start_idx % len(self.players)
        while not self.end_round():
            player = self._current_player
            allowed_actions = self._legal_move(player)
            if not allowed_actions:
                self._next_player()
                continue
            while True:
                try:
                    action, amount = player.decision(
                        allowed_actions,
                        call=self.highest_bet - player.current_bet,
                        min_raise=self.min_raise,
                    )
                    if action not in allowed_actions:
                        raise IllegalMoveError("Impossible action.")
                    self.resolve_action(player, action, bet_amount=amount)
                    break
                except IllegalMoveError as e:
                    logger.error(f"ILLEGAL MOVE: {e} Please try again")
            self._next_player()
        self.reset_betting()
        logger.debug("End betting round")
