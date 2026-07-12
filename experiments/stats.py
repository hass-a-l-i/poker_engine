from poker_engine.models.RandomAgent import Agent
from poker_engine.models.Human import Human
from poker_engine.objects.Card import Card
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table
from poker_engine.objects.HandEval import HandEval
from poker_engine.config.cfg import PokerSkeleton as cfg


def hand_finder(hand_name:str):
    ctr = 0
    while True:
        deck = Deck()
        deck = deck.initialise()
        deck.shuffle()
        table = deck[:5]
        cards = deck[6:8]
        _all = cards + table
        rank = HandEval().return_rank(_all)
        if rank == cfg.hands_dict[hand_name]:
            print([str(c) for c in table])
            print([str(c) for c in cards])
            print(f"Runs : {ctr}")
            break
        ctr += 1


if __name__ == "__main__":
    hand_finder(hand_name="Straight Flush")