from poker_engine.objects.Card import Card
from poker_engine.objects.HandEval import HandEval
from poker_engine.config.cfg import PokerSkeleton as cfg

def high_card_tst():
    tst_cards = [Card('♥2'),
                 Card('♣4'),
                 Card('♣6'),
                 Card('♠8'),
                 Card('♥10'),
                 Card('♦Q'),
                 Card('♠A')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["High Card"]

def pair_tst():
    tst_cards = [Card('♥2'),
                 Card('♣4'),
                 Card('♣2'),
                 Card('♠8'),
                 Card('♥10'),
                 Card('♦Q'),
                 Card('♠A')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Pair"]

def two_pair_tst():
    tst_cards = [Card('♥2'),
                 Card('♣4'),
                 Card('♣2'),
                 Card('♠8'),
                 Card('♥10'),
                 Card('♦Q'),
                 Card('♠4')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Two Pair"]

def three_kind_tst():
    tst_cards = [Card('♥2'),
                 Card('♣5'),
                 Card('♣2'),
                 Card('♠8'),
                 Card('♥10'),
                 Card('♦Q'),
                 Card('♠2')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Three of a Kind"]

def straight_tst():
    tst_cards = [Card('♥7'),
                 Card('♣3'),
                 Card('♣8'),
                 Card('♠9'),
                 Card('♥10'),
                 Card('♦Q'),
                 Card('♠J')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Straight"]

def flush_tst():
    tst_cards = [Card('♣4'),
                 Card('♣3'),
                 Card('♣8'),
                 Card('♣9'),
                 Card('♥10'),
                 Card('♦4'),
                 Card('♣J')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Flush"]

def full_house_tst():
    tst_cards = [Card('♠J'),
                 Card('♣3'),
                 Card('♣8'),
                 Card('♠9'),
                 Card('♥J'),
                 Card('♦3'),
                 Card('♣J')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Full House"]

def four_kind_tst():
    tst_cards = [Card('♠J'),
                 Card('♣3'),
                 Card('♣8'),
                 Card('♠9'),
                 Card('♥J'),
                 Card('♦J'),
                 Card('♣J')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Four of a Kind"]


def straight_flush_tst():
    tst_cards = [Card('♦7'),
                 Card('♣3'),
                 Card('♥10'),
                 Card('♥Q'),
                 Card('♥J'),
                 Card('♥8'),
                 Card('♥9')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Straight Flush"]


def royal_flush_tst():
    tst_cards = [Card('♦7'),
                 Card('♣3'),
                 Card('♥K'),
                 Card('♥Q'),
                 Card('♥J'),
                 Card('♥10'),
                 Card('♥A')]
    _class = HandEval(tst_cards)._return_rank()
    assert _class == cfg.hands_dict["Royal Flush"]

def run_tests():
    high_card_tst()
    pair_tst()
    two_pair_tst()
    three_kind_tst()
    straight_tst()
    flush_tst()
    full_house_tst()
    four_kind_tst()
    straight_flush_tst()
    royal_flush_tst()
    print("Hand eval tests passed")

if __name__ == "__main__":
    run_tests()
