from poker_engine.models.Agent import Agent
from poker_engine.models.Human import Human
from poker_engine.objects.Card import Card
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table
from poker_engine.objects.HandEval import HandEval
from poker_engine.config.cfg import PokerSkeleton as cfg
import logging

def deck_tst():
    deck = Deck()
    deck = deck.initialise()
    deck.shuffle()
    return deck

def card_tst(show):
    a = Card('♠2')
    b = Card('♦9')
    if show:
        print(a)
        print(b)
        print(a.suit)
        print(b.suit)
        print(a.rank)
        print(b.rank)
    return a, b



def player_tst():
    a, b = card_tst(show=False)
    man = Human('tst_human', 1000, [])
    robot = Agent('tst_bot', 1000, [])
    return man, robot


def round_tst():
    human, bot = player_tst()
    _ , bot2 = player_tst()
    _ , bot3 = player_tst()
    bot2.name = 'tst_bot2'
    bot3.name = 'tst_bot3'
    players = [human, bot, bot2, bot3]
    r = Round(players)
    r.run()


def table_tst():
    human, bot = player_tst()
    _, bot2 = player_tst()
    _, bot3 = player_tst()
    _, bot4 = player_tst()
    bot2.name = 'tst_bot2'
    bot3.name = 'tst_bot3'
    bot4.name = 'tst_bot4'
    players = [bot4, bot, bot2, bot3]
    rnd = Round(players)
    deck = Deck()
    deck = deck.initialise()
    t = Table(players=players, rnd=rnd, deck=deck)
    t.run()


def hand_eval():
    deck = deck_tst()
    deck.shuffle()
    table = deck[:5]
    cards = deck[6:8]
    all = cards + table
    rank = HandEval().return_rank(all)
    return table, cards, rank


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                        handlers=[
                            logging.FileHandler(filename="logs/poker_engine.log", mode='w'),
                            logging.StreamHandler()
                        ]
                        )
    table_tst()

















