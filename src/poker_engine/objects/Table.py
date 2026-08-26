from poker_engine.objects.Card import Card
from poker_engine.objects.Player import Player
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.HandEval import HandEval
from poker_engine.objects.Illegal_Move import GameQuit
from poker_engine.config.cfg import PokerSkeleton
import logging

cfg = PokerSkeleton()
logger = logging.getLogger(__name__)


class Table:
    def __init__(
        self,
        players: list[Player],
        deck: Deck,
        rnd: Round,
        cards: list[Card] = None,
        button_idx: int = 0,
    ) -> None:
        """create a table with players, deck, round state, and board cards."""
        self.cards = [] if cards is None else cards
        self.players = players
        self.deck = deck
        self.round = rnd
        self.ranked_players = []
        self.winners: list[Player] = []
        self.end_game = False
        self.button_idx = button_idx

    """helpers"""
    def _community_cards(self) -> str:
        """return the printable community cards."""
        return " ".join([str(card) for card in self.cards])
    def _deal(self) -> None:
        """deal two private cards to every player."""
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                player.add_card(card)
        logger.info("Cards Dealt.")

    def _update_table(self, no_cards: int) -> None:
        """burn one card and add community cards to the board."""
        burned = self.deck.pop()
        self.round.burned.append(burned)
        for _ in range(no_cards):
            card: Card = self.deck.pop()
            self.cards.append(card)

    def _next_active_idx(self, start_idx: int) -> int:
        """return the next active non-all-in player index."""
        for offset in range(len(self.players)):
            idx = (start_idx + offset) % len(self.players)
            player = self.players[idx]
            if player.active and not player.all_in:
                return idx
        return start_idx % len(self.players)

    def _blind_positions(self) -> tuple[int, int]:
        """return the small blind and big blind positions."""
        if len(self.players) == 2:
            return self.button_idx, (self.button_idx + 1) % len(self.players)
        return (
            (self.button_idx + 1) % len(self.players),
            (self.button_idx + 2) % len(self.players),
        )

    def _preflop_start_idx(self, big_blind_idx: int) -> int:
        """return the first player to act before the flop."""
        if len(self.players) == 2:
            return self.button_idx
        return self._next_active_idx(big_blind_idx + 1)

    def _postflop_start_idx(self) -> int:
        """return the first player to act after the flop."""
        if len(self.players) == 2:
            return self._next_active_idx((self.button_idx + 1) % len(self.players))
        return self._next_active_idx(self.button_idx + 1)

    def _rotate_button(self) -> None:
        """move the dealer button to the next player."""
        if len(self.players) > 1:
            self.button_idx = (self.button_idx + 1) % len(self.players)
    def _player_mix_summary(self) -> str:
        """return a readable summary of player model types."""
        random_agents = sum(1 for player in self.players if type(player).__name__ == "RandomAgent")
        humans = sum(1 for player in self.players if type(player).__name__ == "Human")
        other_players = len(self.players) - random_agents - humans
        parts = []

        if random_agents:
            label = "random agent" if random_agents == 1 else "random agents"
            parts.append(f"{random_agents} {label}")
        if humans:
            label = "human" if humans == 1 else "humans"
            parts.append(f"{humans} {label}")
        if other_players:
            label = "player" if other_players == 1 else "players"
            parts.append(f"{other_players} {label}")

        return " and ".join(parts)
    def _rankings_summary(self) -> str:
        """return a readable summary of ranked player hands."""
        rankings = []
        for player, score in self.ranked_players:
            rankings.append(
                f"{player.name}: hand={player.show_hand()}, rank={player.rank}, score={score}"
            )
        return " ### ".join(rankings)
    def _payout_summary(self, payouts: list[tuple[Player, int]]) -> str:
        """return a readable summary of pot payouts."""
        return ", ".join(f"{player.name} wins {amount}" for player, amount in payouts)

    """main"""
    def init_round(self, round_name: str, no_cards: int = None, start_idx: int = None):
        """prepare and run one named betting round."""
        if round_name == "Pre-Flop":
            self.round.run(start_idx=start_idx)
        else:
            self._update_table(no_cards)
            logger.info(f"{round_name} : {self._community_cards()}")
            self.round.run(start_idx=start_idx)

    def post_blinds(self) -> int:
        """post blinds and return the preflop starting position."""
        small_blind_idx, big_blind_idx = self._blind_positions()
        self.round.post_blinds(small_blind_idx, big_blind_idx)
        return self._preflop_start_idx(big_blind_idx)

    def resolve_winner(self):
        """evaluate active hands and store the winning players."""
        eligible_players = [p for p in self.players if p.active]
        for player in eligible_players:
            all_cards = self.cards + player.hand
            player.score, player.rank = HandEval(all_cards).score_tuple()

        self.ranked_players = [(p, p.score) for p in eligible_players]
        self.ranked_players.sort(key=lambda item: item[1], reverse=True)

        logger.debug(f"Hand rankings: {self._rankings_summary()}")
        best_score = self.ranked_players[0][1]
        self.winners = [player for player, score in self.ranked_players if score == best_score]
        logger.info(
            f"Winner(s) : {', '.join([p.name for p in self.winners])} "
            f"with {self.winners[0].rank}. Winnings : {self.round.pot}"
        )

    def build_side_pots(self) -> list[dict]:
        """build side pots from player stakes and eligibility."""
        contributors = [p for p in self.players if p.total_stake > 0]
        stake_levels = sorted(set(p.total_stake for p in contributors))
        pots = []
        previous_level = 0

        for level in stake_levels:
            amount_per_player = level - previous_level
            involved = [p for p in contributors if p.total_stake >= level]
            eligible = [p for p in involved if p.active]
            pot_amount = amount_per_player * len(involved)

            if pot_amount > 0 and eligible:
                pots.append({
                    "amount": pot_amount,
                    "eligible": eligible,
                    "contributors": involved,
                })

            previous_level = level

        return pots

    def distribute_winnings(self):
        """distribute the pot or side pots to eligible winners."""
        if len(self.winners) == 1 and len([p for p in self.players if p.active]) == 1:
            self.winners[0].chips += self.round.pot
            logger.debug(f"{self.winners[0].name} wins uncontested pot : {self.round.pot}")
            return

        pots = self.build_side_pots()
        if not pots:
            pots = [{"amount": self.round.pot, "eligible": self.winners}]

        for pot in pots:
            best_score = max(player.score for player in pot["eligible"])
            winners = [player for player in pot["eligible"] if player.score == best_score]
            pot_share, odd_chips = divmod(pot["amount"], len(winners))

            payouts = []
            for idx, player in enumerate(winners):
                payout = pot_share
                if idx < odd_chips:
                    payout += 1
                player.chips += payout
                payouts.append((player, payout))

            logger.debug(
                f"Distributed pot {pot['amount']}: {self._payout_summary(payouts)}"
            )

        total_chips = sum([p.chips for p in self.players])
        logger.debug(f"Total chips : {total_chips}")

    def end_by_folds_check(self):
        """finish the hand early when only one player remains active."""
        active_players = [p for p in self.players if p.active]
        if len(active_players) == 1:
            self.winners = active_players
            self.distribute_winnings()
            self.resolve_losers()
            logger.info(
                f"Winner(s) : {', '.join([p.name for p in self.winners])} "
                f"due to all players folding. Winnings : {self.round.pot}"
            )
            self.last_player_check()
            self.reset()
            if not self.end_game:
                self._rotate_button()
            return True
        return False

    def resolve_losers(self):
        """remove players who have no remaining chips."""
        losers = [p for p in self.players if p.chips == 0]
        for player in losers:
            logger.info(f"{player.name} has no chips - they are out!")
            for card in player.hand:
                self.round.burned.append(card)

        self.players = [p for p in self.players if p.chips > 0]
        self.round.players = self.players
        if self.players:
            self.button_idx %= len(self.players)

    def reset(self):
        """reset table and round state after a completed hand."""
        self.winners = []
        self.ranked_players = []
        self.round.reset_round()
        burned = self.round._return_burned()
        self.deck.add(burned)
        self.deck.add(self.cards)
        self.cards = []
        self.round.burned = []
        for player in self.players:
            player.all_in = False
            player.score = None
            player.rank = None
            player.total_stake = 0

    def last_player_check(self):
        """end the game when one player remains."""
        if len(self.players) == 1:
            winner = self.players[0]
            logger.info(f"All players out. {winner.name} wins!")
            self.end_game = True

    def run(self):
        """run hands until the game has one winner."""
        logger.info(f"Initialised game with {self._player_mix_summary()}")
        try:
            while not self.end_game:
                self.deck.shuffle()
                self._deal()

                logger.info("Pre-Flop")
                preflop_start_idx = self.post_blinds()
                self.init_round(round_name="Pre-Flop", start_idx=preflop_start_idx)
                if self.end_by_folds_check():
                    continue

                postflop_start_idx = self._postflop_start_idx()
                self.init_round(round_name="Flop", no_cards=3, start_idx=postflop_start_idx)
                if self.end_by_folds_check():
                    continue

                self.init_round(round_name="Turn", no_cards=1, start_idx=postflop_start_idx)
                if self.end_by_folds_check():
                    continue

                self.init_round(round_name="River", no_cards=1, start_idx=postflop_start_idx)
                if self.end_by_folds_check():
                    continue

                self.resolve_winner()
                self.distribute_winnings()
                self.resolve_losers()
                self.last_player_check()
                self.reset()
                self._rotate_button()
        except GameQuit as exc:
            logger.info(str(exc))
            self.end_game = True
