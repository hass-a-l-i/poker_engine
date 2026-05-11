from poker_engine.objects.Card import Card
from poker_engine.objects.Deck import Deck
from poker_engine.models.Human import Human
from poker_engine.models.Agent import Agent
from poker_engine.objects.Round import Round

def deck_tst():
    deck = Deck()
    deck = deck.initialise()
    # deck.shuffle()
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
    human2, bot2 = player_tst()
    human3, bot3 = player_tst()
    human2.name = 'tst_human2'
    bot2.name = 'tst_bot2'
    bot3.name = 'tst_bot3'
    # bot.active = False
    players = [human, bot, bot2, bot3]
    deck = deck_tst()
    r = Round(players, deck)
    r.run()


if __name__ == "__main__":
    # main logic here - wrap in func main
    round_tst()
















