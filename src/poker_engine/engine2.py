import poker_engine.config.global_vars as gv
from poker_engine.old.Cards import Card
from poker_engine.old.Deck import Deck
from poker_engine.old.Players import Player
from poker_engine.old.Table import Table
from poker_engine.old.Rounds import Round
actions_dict = gv.actions_dict

if __name__ == "__main__":
    # main logic here - wrap in func main
    print(gv.game_rules)
    n = 3
    buy_in = 1000
    deck = Deck().initialise()
    player_ls = [Player(name=f"Player {i+1}", chips=buy_in) for i in range(n)]
    table = Table(players=player_ls, deck=deck)
    table.deck.shuffle()
    table.deal()
    bb = 100
    sb = 50
    round = Round(player_ls, bb, sb)
    round.begin()










