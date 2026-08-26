"""testing for models used so far"""

import random
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[1]
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

from poker_engine.config.cfg import PokerSkeleton
from poker_engine.models.Human import Human
from poker_engine.models.RandomAgent import RandomAgent
from poker_engine.objects.Illegal_Move import GameQuit, IllegalMoveError


cfg = PokerSkeleton()


class HumanModelTests(unittest.TestCase):
    def test_human_rejects_non_integer_choice(self):
        player = Human("human", 1000, [])

        with patch("builtins.input", return_value="bad"):
            with patch("builtins.print"):
                with self.assertRaises(IllegalMoveError):
                    player.decision([cfg.check], call=0)

    def test_human_rejects_choice_outside_legal_actions(self):
        player = Human("human", 1000, [])

        with patch("builtins.input", return_value=str(cfg.fold)):
            with patch("builtins.print"):
                with self.assertRaises(IllegalMoveError):
                    player.decision([cfg.check], call=0)

    def test_human_returns_check_without_amount_prompt(self):
        player = Human("human", 1000, [])

        with patch("builtins.input", return_value=str(cfg.check)):
            with patch("builtins.print"):
                self.assertEqual(player.decision([cfg.check], call=0), (cfg.check, 0))

    def test_human_prompt_prints_visible_decision_state(self):
        player = Human("human", 750, [])
        player.current_bet = 100

        with patch("builtins.input", return_value=str(cfg.call)):
            with patch("builtins.print") as mock_print:
                self.assertEqual(player.decision([cfg.fold, cfg.call], call=200), (cfg.call, 0))

        printed = "\n".join(str(call.args[0]) for call in mock_print.call_args_list)
        self.assertIn("human's turn", printed)
        self.assertIn("Chips       : 750", printed)
        self.assertIn("Current bet : 100", printed)
        self.assertIn("To call     : 200", printed)
        self.assertIn("Actions", printed)

    def test_human_prompts_for_bet_and_raise_amounts(self):
        player = Human("human", 1000, [])

        with patch("builtins.input", side_effect=[str(cfg.bet), "250"]):
            with patch("builtins.print"):
                self.assertEqual(player.decision([cfg.bet], call=0), (cfg.bet, 250))

        with patch("builtins.input", side_effect=[str(cfg.raise_), "300"]):
            with patch("builtins.print"):
                self.assertEqual(player.decision([cfg.raise_], call=100), (cfg.raise_, 300))

    def test_human_rejects_non_integer_bet_amount(self):
        player = Human("human", 1000, [])

        with patch("builtins.input", side_effect=[str(cfg.bet), "bad"]):
            with patch("builtins.print"):
                with self.assertRaises(IllegalMoveError):
                    player.decision([cfg.bet], call=0)

    def test_human_can_quit_from_action_prompt(self):
        player = Human("human", 1000, [])

        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print"):
                with self.assertRaises(GameQuit):
                    player.decision([cfg.check], call=0)

    def test_human_can_quit_from_amount_prompt(self):
        player = Human("human", 1000, [])

        with patch("builtins.input", side_effect=[str(cfg.bet), "quit"]):
            with patch("builtins.print"):
                with self.assertRaises(GameQuit):
                    player.decision([cfg.bet], call=0)


class RandomAgentModelTests(unittest.TestCase):
    def test_random_agent_rejects_empty_legal_actions(self):
        player = RandomAgent("bot", 1000, [])

        with self.assertRaises(IllegalMoveError):
            player.decision([], call=0)

    def test_random_agent_check_call_and_fold_return_zero_amount(self):
        player = RandomAgent("bot", 1000, [])

        with patch("random.choice", return_value=cfg.check):
            self.assertEqual(player.decision([cfg.check], call=0), (cfg.check, 0))
        with patch("random.choice", return_value=cfg.call):
            self.assertEqual(player.decision([cfg.call], call=100), (cfg.call, 0))
        with patch("random.choice", return_value=cfg.fold):
            self.assertEqual(player.decision([cfg.fold], call=100), (cfg.fold, 0))

    def test_random_agent_bet_is_between_minimum_and_stack(self):
        player = RandomAgent("bot", 1000, [])
        random.seed(1)

        action, amount = player.decision([cfg.bet], call=0)

        self.assertEqual(action, cfg.bet)
        self.assertGreaterEqual(amount, cfg.big_blind)
        self.assertLessEqual(amount, player.chips)

    def test_random_agent_short_stack_bet_can_be_all_in_below_big_blind(self):
        player = RandomAgent("bot", 40, [])

        action, amount = player.decision([cfg.bet], call=0)

        self.assertEqual(action, cfg.bet)
        self.assertEqual(amount, 40)

    def test_random_agent_raise_uses_remaining_chips_after_call(self):
        player = RandomAgent("bot", 1000, [])

        action, amount = player.decision([cfg.raise_], call=250)

        self.assertEqual(action, cfg.raise_)
        self.assertEqual(amount, 750)


if __name__ == "__main__":
    unittest.main()
