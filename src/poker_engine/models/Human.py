from poker_engine.objects.Card import Card
from poker_engine.objects.Player import Player
from poker_engine.objects.Illegal_Move import IllegalMoveError
from poker_engine.config.cfg import PokerSkeleton
cfg = PokerSkeleton()


class Human(Player):
    def __init__(self, name:str, chips:int, hand:list[Card]) -> None:
        super().__init__(name, chips, hand)


    def decision(self,
                 legal_actions: list[int],
                 call:int
                 ) -> tuple[int, int]:
        menu_str = ", ".join([f"{k}: {v}" for k, v in cfg.actions_dict.items() if k in legal_actions])
        choice = input(f"Choose an action: {menu_str} \n" )
        try :
            choice = int(choice)
        except ValueError:
            raise IllegalMoveError("Invalid input type.")
        if choice not in legal_actions:
            raise IllegalMoveError("Impossible action.")
        str_choice = cfg.actions_dict[choice]
        if str_choice == "Bet":
            amount = int(input(f"Choose bet: \n"))
            return choice, amount
        return choice, 0

