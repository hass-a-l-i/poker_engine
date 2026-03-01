from pickletools import decimalnl_long

from poker_engine.models.Cards import Card
from poker_engine.models.Deck import Deck
from poker_engine.models.Players import Player
from poker_engine.models.Table import Table

if __name__ == "__main__":
    deck = Deck().initialise()
    n = 3
    player_ls = [Player(name=f"Player {i+1}") for i in range(n)]
    table = Table(players=player_ls, deck=deck)
    # table.deck.shuffle()
    table.deal()
    for player in player_ls:
        player.info()
    table.flop()
    table.turn()
    table.river()
    print(table.community_cards())
    print(table.deck)

    # now need to do a round




"""
card = Card("H10")
print(card)
print(repr(card))
suit = card.get_suit()
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
"""









