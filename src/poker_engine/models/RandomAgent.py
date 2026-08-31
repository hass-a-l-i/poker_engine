import random
from poker_engine.objects.Card import Card
from poker_engine.objects.Illegal_Move import IllegalMoveError
from poker_engine.objects.Player import Player
from poker_engine.config.cfg import PokerSkeleton
cfg = PokerSkeleton()

"""
inheritance from player class
"""
class RandomAgent(Player):
    def __init__(self, name: str, chips: int, hand: list[Card]) -> None:
        """create a random-action poker player."""
        super().__init__(name, chips, hand)

    def decision(self,
                 legal_actions: list[int],
                 call:int,
                 min_raise: int = cfg.big_blind,
                 ) -> tuple[int, int]:
        """choose a random legal action and amount."""
        if len(legal_actions) == 0:
            raise IllegalMoveError("No choices")
        choice = random.choice(legal_actions)
        str_choice = cfg.actions_dict[choice]
        if str_choice == "Bet":
            minimum = min(cfg.big_blind, self.chips)
            amount = random.randint(minimum, self.chips)
            return choice, amount
        if str_choice == "Raise":
            minimum_raise = min_raise
            maximum_raise = self.chips - call
            if maximum_raise <= minimum_raise:
                amount = maximum_raise
            else:
                amount = random.randint(minimum_raise, maximum_raise)
            return choice, amount
        return choice, 0
