from poker_engine.models.Agent import Agent
from poker_engine.models.Human import Human
from poker_engine.objects.Card import Card
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table
from poker_engine.objects.HandEval import HandEval
from poker_engine.config.cfg import PokerSkeleton as cfg

def deck_tst():
    deck = Deck()
    deck = deck.initialise()
    og_deck = deck.copy()
    deck.shuffle()
    assert deck.state != og_deck.state


def card_tst():
    a = Card('♠2')
    b = Card('♦9')
    assert a.suit == "♠"
    assert b.suit == "♦"
    assert a.rank == "2"
    assert b.rank == "9"
    assert a.__str__() == "|♠2|"
    assert b.__str__() == "|♦9|"





def run_tests():
    deck_tst()
    card_tst()
    print("Object tests passed")

if __name__ == "__main__":
    run_tests()
