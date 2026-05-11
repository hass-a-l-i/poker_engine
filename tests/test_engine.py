import poker_engine.config.global_vars as gv
from poker_engine.old.Cards import Card
from poker_engine.old.Deck import Deck
from poker_engine.old.Players import Player
from poker_engine.old.Table import Table
from poker_engine.old.Rounds import Round
actions_dict = gv.actions_dict

if __name__ == "__main__":
    print(gv.game_rules)
    n = 3
    buy_in = 1000
    deck = Deck().initialise()
    player_ls = [Player(name=f"Player {i+1}", chips=buy_in) for i in range(n)]
    table = Table(players=player_ls, deck=deck)
    table.deck.shuffle()
    table.deal()
    #
    # table.flop()
    # table.turn()
    # table.river()
    # print(table.community_cards())
    # print(table.deck)
    bb = 100
    sb = 50
    round = Round(player_ls, bb, sb)
    round.begin()

    # now need to do a round
    # def actions for each player in round class







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









