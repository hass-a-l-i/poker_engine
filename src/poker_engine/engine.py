from poker_engine.models.Cards import Card
from poker_engine.models.Deck import Deck
from poker_engine.models.Players import Player

if __name__ == "__main__":
    card = Card("H3")
    print(card)
    print(repr(card))
    suit = card.__getattribute__("suit")
    print(suit)
    number = card.get_rank_numeric()
    print(number)
    card2 = Card("HJ")

    deck = Deck()
    deck.initialise()
    print(deck)
    deck.shuffle()
    print(deck)
    print(len(deck))

    p1 = Player()
    p1.add_card(card)
    p1.add_card(card2)
    p1.show_hand()
    print(repr(p1))
    hand_num = p1.hand_rank()
    print(hand_num)
    print(len(p1.hand))












