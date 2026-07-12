from math import inf

from poker_engine.objects.Card import Card
from poker_engine.objects.Player import Player
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.HandEval import HandEval
import logging

logger = logging.getLogger(__name__)


class Table:
    def __init__(self, players:list[Player], deck:Deck, rnd:Round, cards:list[Card]=None) -> None:
        self.cards = [] if cards is None else cards
        self.players = players
        self.deck = deck
        self.round = rnd
        self.ranked_players = []
        self.winners:list[Player] = []

    """helpers"""
    def _community_cards(self) -> str:
        return " ".join([str(card) for card in self.cards])
    def deal(self) -> None:
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                player.add_card(card)

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
        logger.info(f"{self.winners} are winners")

    def distribute_winnings(self):
        pot_share = int(self.round.pot / len(self.winners))
        logger.debug(f"Distributed winnings : {pot_share}")
        for p in self.winners:
            p.chips += pot_share
        logger.info(f"Chips : {[(item[0].name, item[0].chips) for item in self.ranked_players]}")
        chips = sum([p.chips for p in self.players])
        logger.debug(f"Total chips : {chips}") # SENSE CHECKS HERE LIKE SUM CHIPS?????

    # first do end table conditions (i.e. game) remove dead players
    # then do side pots
    # splitting odd chips evenly
    # all ins (if doesnt have enough chips)
    # legal raises
    # blinds



    def resolve_losers(self):
        pass

    def reset(self):
        self.winners = []
        self.ranked_players = []
        burned = self.round.return_burned()
        self.round.reset()
        self.deck.add(burned)
        self.deck.add(self.cards)
        self.cards = []


    def run(self):
        self.deck.shuffle()
        self.deal()
        self.init_round(round_name="Pre-Flop")
        self.init_round(round_name="Flop", no_cards=3)
        self.init_round(round_name="River", no_cards=1)
        self.init_round(round_name="Turn", no_cards=1)
        self.resolve_winner()
        self.distribute_winnings()
        ### RESOLVE LOSERS
        self.reset()

