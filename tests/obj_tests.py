from poker_engine.objects.Deck import Deck

def deck_tst():
    deck = Deck()
    deck = deck.initialise()
    og_deck = deck.copy()
    deck.shuffle()
    assert deck.state != og_deck.state


deck_tst()