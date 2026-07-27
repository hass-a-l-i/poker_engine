import random
from poker_engine.objects.Card import Card
from poker_engine.objects.Illegal_Move import IllegalMoveError
from poker_engine.objects.Player import Player
from poker_engine.config.cfg import PokerSkeleton
cfg = PokerSkeleton()


class RandomAgent(Player):
    def __init__(self, name: str, chips: int, hand: list[Card]) -> None:
        super().__init__(name, chips, hand)

    def decision(self,
                 legal_actions: list[int],
                 call:int,
                 ) -> tuple[int, int]:
        filt = [i for i in legal_actions if i != 5]
        choice = random.choice(filt) ### ENSURE NO FOLD
        if len(filt) == 0:
            raise IllegalMoveError("No choices")
        str_choice = cfg.actions_dict[choice]
        if str_choice == "Bet":
            # amount = random.randint(1, self.chips)
            amount = random.randint(1, 20) ### CAPPING BETMAX FOR TESTS
            return choice, amount
        if str_choice == "Raise":
            # amount = random.randint(1, self.chips - call)
            amount = random.randint(1, self.chips - call)
            return choice, amount
        return choice, 0
