from poker_engine.archive.Players import Player
import poker_engine.archive.global_vars as gv
actions_dict = gv.actions_dict

"""
TO DO:
- blinds is only first round pre flop
- do len log >= len players and highest bet == current bet for all playwers thene nd rouind
- type casting
- once round logic complete need to do round winning logic, game object?
"""

class Round:
    def __init__(self, players:list[Player], big_blind:int, small_blind:int) -> None:
        self.players = players
        self.pot:int = 0
        self.log:list[tuple[Player, int]] = [] # list of tuples, player, action
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.highest_bet = big_blind

    def init(self) -> None:
        pass
        # lol
        # do dealer


    def begin(self) -> None:
        self.blinds()
        while True:
            no_players:int = len(self.players)
            if (no_players == 1) or self.end_round():
                break
            player = self.select_player()
            player, action = self.turn(player)
            self.turn_result(player, action)


    def blinds(self) -> None:
        sb_player = self.players[-2]
        print(f"{sb_player.name} puts forward a small blind of {self.small_blind}.")
        sb_player.chips -= self.small_blind
        sb_player.current_bet = self.small_blind
        bb_player = self.players[-1]
        print(f"{bb_player.name} puts forward a small blind of {self.big_blind}.")
        bb_player.chips -= self.big_blind
        bb_player.current_bet = self.big_blind
        self.pot += self.big_blind + self.small_blind


    def select_player(self):
        current_player:Player = self.players[0]
        print(f"{current_player.name}'s turn")
        current_player.info()
        print(f"Highest bet on table : {self.highest_bet}")
        print(f"Pot : {self.pot}")
        return current_player


    def turn(self, current_player) -> tuple[Player, int]:
        act = input("Choose action (1:Check, 2:Call, 3:Bet, 4:Fold) \n")
        action = -1
        allowed_actions: list[int] = [1, 2, 3, 4]
        try:
            action:int = int(act)
            if action not in allowed_actions:
                print("Action is not one of the allowed actions, try again.")
            else:
                self.log.append((current_player, action))
        except ValueError:
            print(f"Action must be of type int, try again")
        return current_player, action


    def end_round(self) -> bool:
        bet_equal = all(p.current_bet == self.highest_bet for p in self.players)
        if (len(self.log) >= len(self.players)) and bet_equal:
            return True
        return False


    def turn_result(self, last_player, last_action):
        if last_action == 1:
            self.check_action(last_player)
        elif last_action == 2:
            self.call_action(last_player)
        elif last_action == 3:
            self.bet_action(last_player)
        elif last_action == 4:
            self.fold_action(last_player)
        self.next_player()


    def fold_action(self, player):
        self.players.pop(0)
        print(f"{player.name} folded")


    def bet_action(self, player):
        bet = input(f"Choose bet: \n")
        try:
            bet = int(bet)
            if bet < 0:
                print("Bets can't be less than 0, try again")
            elif bet < (self.highest_bet - player.current_bet):
                print(f"Bet must be larger than {self.highest_bet - player.current_bet}, try again")
            elif bet >= player.chips:
                print("All in!")
                bet = player.chips

            if bet > (self.highest_bet - player.current_bet):
                self.highest_bet = bet + player.current_bet
                player.current_bet += bet
                player.chips -= bet
                self.pot += bet
                print(f"Chips remaining: {player.chips}")

        except ValueError:
            print(f"Integer expected, try again")


    def call_action(self, player):
        call = self.highest_bet - player.current_bet
        if call <= 0:
            print(f"Cannot call here.")
        else:
            player.current_bet += call
            self.pot += call
            player.chips -= call
            print(f"{player.name} calls with {call}")
            print(f"Chips remaining: {player.chips}")


    def check_action(self, player):
        if self.highest_bet != player.current_bet:
            print("Cannot check here.")
        else:
            print(f"{player.name} checks.")


    # if go one round and highest bet unchanged

    def next_player(self):
        player_done = self.players.pop(0)
        self.players.append(player_done)

