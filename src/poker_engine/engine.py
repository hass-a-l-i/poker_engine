import poker_engine.config.global_vars as gv
from poker_engine.models.Cards import Card
from poker_engine.models.Deck import Deck
from poker_engine.models.Players import Player
from poker_engine.models.Table import Table
from poker_engine.models.Rounds import Round
actions_dict = gv.actions_dict

if __name__ == "__main__":
    print(gv.game_rules)
    n = 3
    buy_in = 1000
    deck = Deck().initialise()
    player_ls = [Player(name=f"Player {i+1}", chips=buy_in) for i in range(n)]
    table = Table(players=player_ls, deck=deck)
    # table.deck.shuffle()
    table.deal()
    table.flop()
    table.turn()
    table.river()
    print(table.community_cards())
    print(table.deck)
    bb = 100
    sb = 50
    round = Round(player_ls, bb, sb)
    round.begin()
    # round_players = player_ls
    # idx = 0
    # while True:
    #     player = round_players[idx]
    #     player.info()
    #     action = None
    #     act:str = input("Action please \n")
    #     try:
    #         act:int = int(act)
    #         action = actions_dict[act]
    #         if action == "Fold":
    #             round_players.remove(player)
    #             print(f"{player.name} folded")
    #             idx = 0
    #         elif idx == len(round_players) - 1:
    #             idx = 0
    #         else:
    #             idx += 1
    #     except (ValueError, KeyError):
    #         print("Invalid action try again.")
    #
    #     if len(round_players) == 1:
    #         break

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









