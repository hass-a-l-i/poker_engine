from poker_engine.models.Cards import Card
from poker_engine.models.Players import Player
import poker_engine.config.global_vars as gv
actions_dict = gv.actions_dict

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
        # do dealer


    def begin(self) -> None:
        # current_player: Player = self.players[0]
        # current_player.info()
        while True:
            no_players:int = len(self.players)
            if no_players == 1:
                break
            player = self.select_player()
            player, action = self.turn(player)
            self.turn_result(player, action)


    def select_player(self):
        current_player:Player = self.players[0]
        current_player.info()
        print(f"Highest bet on table : {self.highest_bet}")
        return current_player

    def turn(self, current_player) -> tuple[Player, int]:
        # current_player:Player = self.players[0]
        # current_player.info()
        # print(f"Highest bet on table : {self.highest_bet}")
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


    def turn_result(self, last_player, last_action):
        # last_player = None
        # last_action = None
        # if len(self.log) > 0:
        #     prev_log = self.log[-1]
        #     last_player = prev_log[0]
        #     last_action = prev_log[1]

        self.fold_check(last_player, last_action)
        self.bet_check(last_player, last_action)

        if last_action == 1:
            pass

        if last_action in [2]:
            last_player = self.players.pop(0)
            self.players.append(last_player)


    def rotate_players(self):
        pass


    def fold_check(self, player, action):
        if action == 4:
            self.players.pop(0)
            print(f"{player.name} folded")


    def bet_check(self, player, action):
        if action == 3:
            bet = input(f"Choose bet (type 0 for all-in): \n")
            # need to include betting scenarios too - or move onto call - do basic actions first
            try:
                bet = int(bet)
                if bet == 0:
                    bet = player.chips
                if bet < 0:
                    print("Bets can't be less than 0, try again")
                elif bet < self.highest_bet:
                    print("Bets must be larger than highest bet, try again")
                elif bet > player.chips:
                    print("Bet amount is above available chips, try again")
                else:
                    player.chips -= bet
                    last_player = self.players.pop(0)
                    self.players.append(last_player)

                if bet > self.highest_bet:
                    self.highest_bet = bet

                player.current_bet = bet
                print(f"Chips remaining: {player.chips}")
            except ValueError:
                print(f"Integer expected, try again")


    def call_check(self):
        pass # do this now

