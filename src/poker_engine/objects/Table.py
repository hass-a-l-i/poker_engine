from poker_engine.objects.Card import Card
from poker_engine.objects.Player import Player
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.HandEval import HandEval
from poker_engine.config.cfg import PokerSkeleton
import logging

cfg = PokerSkeleton()
logger = logging.getLogger(__name__)


class Table:
    def __init__(self, players:list[Player], deck:Deck, rnd:Round, cards:list[Card]=None) -> None:
        self.cards = [] if cards is None else cards
        self.players = players
        self.deck = deck
        self.round = rnd
        self.ranked_players = []
        self.winners:list[Player] = []
        self.end_game = False

    """helpers"""
    def _community_cards(self) -> str:
        return " ".join([str(card) for card in self.cards])
    def deal(self) -> None:
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                player.add_card(card)
        logger.info("Cards Dealt.")

    """main"""
    def _update_table(self, no_cards:int) -> None:
        burned = self.deck.pop()
        self.round.burned.append(burned)
        for _ in range(no_cards):
            card: Card = self.deck.pop()
            self.cards.append(card)

    def init_round(self, round_name:str, no_cards:int=None):
        fold_check = len([p for p in self.players if p.active])
        if fold_check == 1:
            logger.info("All players folded.")
        if round_name == "Pre-Flop":
            self.round.run()
        else:
            self._update_table(no_cards)
            logging.info(f"{round_name} : {self._community_cards()}")
            self.round.run()

    def resolve_winner(self):
        for p in self.players:
            all_cards = self.cards + p.hand
            p.score = HandEval(all_cards).score_tuple()
        self.ranked_players = [(p, p.score) for p in self.players]
        self.ranked_players .sort(key=lambda item: item[1], reverse=True)

        logger.debug([(player.name, score) for player, score in self.ranked_players])
        best_ranked = max(self.ranked_players, key=lambda item: item[1])
        best_score = best_ranked[1]
        self.winners = [player for player, score in self.ranked_players if score == best_score]
        logger.info(f"Winner(s) : {", ".join([p.name for p in self.winners])}")

    def distribute_winnings(self):
        pot_share, odd_chips = divmod(self.round.pot, len(self.winners))
        logger.debug(f"Distributed winnings : {pot_share}")
        for idx, p in enumerate(self.winners):
            p.chips += pot_share
            if idx < odd_chips:
                p.chips += 1
        if odd_chips:
            logger.debug(f"Distributed odd chips : {odd_chips}")
        logger.debug(f"Chips : {[(item[0].name, item[0].chips) for item in self.ranked_players]}")
        total_chips = sum([p.chips for p in self.players])
        logger.debug(f"Total chips : {total_chips}")


    # then do side pots (doing now total committed and all in added)
    # legal raises
    # blinds

    def resolve_losers(self):
        losers = [p for p in self.players if p.chips == 0]
        for p in losers:
            logger.info(f"{p.name} has no chips - they are out!")
            for card in p.hand:
                self.round.burned.append(card)
        self.players = [p for p in self.players if p.chips > 0]
        self.round.players = self.players

        if len(self.players) == 1:
            winner = self.players[0]
            logger.info(f"All players out. {winner.name} wins!")
            self.end_game = True


    def reset(self):
        self.winners = []
        self.ranked_players = []
        burned = self.round.return_burned()
        self.round.reset_round()
        self.deck.add(burned)
        self.deck.add(self.cards)
        self.cards = []
        for p in self.players:
            p.all_in = False


    def run(self):
        while not self.end_game:
            self.deck.shuffle()
            self.deal()
            self.init_round(round_name="Pre-Flop")
            self.init_round(round_name="Flop", no_cards=3)
            self.init_round(round_name="Turn", no_cards=1)
            self.init_round(round_name="River", no_cards=1)
            self.resolve_winner()
            self.distribute_winnings()
            self.resolve_losers()
            self.reset()

