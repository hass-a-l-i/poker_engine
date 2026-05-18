import random
from poker_engine.objects.Card import Card
from poker_engine.objects.Player import Player
from poker_engine.config.cfg import PokerSkeleton
cfg = PokerSkeleton()


class Agent(Player):
    def __init__(self, name: str, chips: int, hand: list[Card]) -> None:
        super().__init__(name, chips, hand)

    def decision(self,
                 legal_actions: list[int],
                 call:int,
                 ) -> tuple[int, int]:
        menu_str = ", ".join([f"{k}: {v}" for k, v in cfg.actions_dict.items() if k in legal_actions])
        # print(f"Choose an action: {menu_str}")
        # choice = random.choice(legal_actions)
        if len([i for i in legal_actions if i != 5]) == 0:
            print("no choices")
        choice = random.choice([i for i in legal_actions if i != 5])
        str_choice = cfg.actions_dict[choice]
        if str_choice == "Bet":
            # amount = random.randint(min_bet, min_bet+10)
            amount = random.randint(1, self.chips)
            return choice, amount
        if str_choice == "Raise":
            amount = random.randint(1, self.chips - call)
            return choice, amount
        return choice, 0
