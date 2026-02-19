import numpy as np


class Game:
    # need attributes for game
    def __init__(self):
        pass



class GameState:
    def __init__(self, deck, table, hands, players):
        self.deck = deck
        self.table = table
        self.hands = hands
        self.players = players
        self.min_bet = 0
        self.pot = 0
        self.side_pot = 0
        self.folded = []
        self.bet_round = 0

    def shuffle_deck(self):
        deck_ind = np.array(range(0, 52))
        shuffle = np.random.choice(deck_ind, len(deck_ind), replace=False)
        self.deck = np.array([self.deck[i] for i in shuffle])

    def deal_hands(self, no_players):
        for _ in range(2):
            for i in range(no_players):
                self.hands[i].append(self.deck[0])
                self.deck = np.delete(self.deck, 0)

    def deal_table(self, flop):
        if flop:
            self.table = self.deck[0:3]
            self.deck = self.deck[3:]
        else:
            self.table = np.append(self.table, self.deck[0])
            self.deck = self.deck[1:]

    def set_blinds(self, dealer):
        if dealer > len(self.players) - 1:
            dealer = dealer - len(self.players)
        sb = dealer + 1
        bb = dealer + 2
        fp = dealer + 3
        if sb > len(self.players) - 1:
            sb = sb - len(self.players)
        if bb > len(self.players) - 1:
            bb = bb - len(self.players)
        if fp > len(self.players) - 1:
            fp = fp - len(self.players)
        self.players[sb].small_blind = True
        self.players[bb].big_blind = True
        return fp