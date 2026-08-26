from poker_engine.objects.Card import Card
from poker_engine.objects.Player import Player
from poker_engine.objects.Illegal_Move import GameQuit, IllegalMoveError
from poker_engine.config.cfg import PokerSkeleton
cfg = PokerSkeleton()

"""
inheritance from player class
"""
class Human(Player):
    def __init__(self, name:str, chips:int, hand:list[Card]) -> None:
        """create a human-controlled poker player."""
        super().__init__(name, chips, hand)

    def _print_decision_prompt(self, legal_actions: list[int], call: int) -> None:
        """print the current decision state for a human player."""
        menu_str = ", ".join(
            [f"{k}: {v}" for k, v in cfg.actions_dict.items() if k in legal_actions]
        )
        print(f"\n---------- {self.name}'s turn ----------", flush=True)
        print(f"Hand        : {self.show_hand()}", flush=True)
        print(f"Chips       : {self.chips}", flush=True)
        print(f"Current bet : {self.current_bet}", flush=True)
        print(f"To call     : {max(call, 0)}", flush=True)
        print(f"Actions     : {menu_str}", flush=True)

    def decision(self,
                 legal_actions: list[int],
                 call:int
                 ) -> tuple[int, int]:
        """read and return a validated human betting decision."""
        self._print_decision_prompt(legal_actions, call)
        choice = input("Choose action > ").strip()
        if choice.lower() == "quit":
            raise GameQuit(f"{self.name} quit the game.")
        try :
            choice = int(choice)
        except ValueError:
            raise IllegalMoveError("Invalid input type.")
        if choice not in legal_actions:
            raise IllegalMoveError("Impossible action.")
        str_choice = cfg.actions_dict[choice]
        if str_choice in ("Bet", "Raise"):
            try:
                amount_choice = input(f"Choose {str_choice.lower()} amount > ").strip()
                if amount_choice.lower() == "quit":
                    raise GameQuit(f"{self.name} quit the game.")
                amount = int(amount_choice)
            except ValueError:
                raise IllegalMoveError("Invalid amount type.")
            return choice, amount
        return choice, 0
