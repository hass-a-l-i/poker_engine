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
from poker_engine.models.QuantumRandomAgent import QuantumRandomAgent
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

    def test_random_agent_raise_uses_random_amount_after_call(self):
        player = RandomAgent("bot", 1000, [])

        with patch("random.randint", return_value=300) as randint:
            action, amount = player.decision([cfg.raise_], call=250)

        self.assertEqual(action, cfg.raise_)
        self.assertEqual(amount, 300)
        randint.assert_called_once_with(cfg.big_blind, 750)

    def test_random_agent_raise_uses_round_min_raise(self):
        player = RandomAgent("bot", 1000, [])

        with patch("random.randint", return_value=500) as randint:
            self.assertEqual(player.decision([cfg.raise_], call=250, min_raise=400), (cfg.raise_, 500))

        randint.assert_called_once_with(400, 750)


class QuantumRandomAgentModelTests(unittest.TestCase):
    def test_quantum_random_agent_rejects_empty_legal_actions(self):
        player = QuantumRandomAgent("quantum_bot", 1000, [])

        with self.assertRaises(IllegalMoveError):
            player.decision([], call=0)

    def test_quantum_random_agent_maps_quantum_index_to_legal_action(self):
        player = QuantumRandomAgent("quantum_bot", 1000, [])

        with patch.object(QuantumRandomAgent, "quantum_randint", return_value=1):
            self.assertEqual(player.decision([cfg.check, cfg.fold], call=0), (cfg.fold, 0))

    def test_quantum_random_agent_bet_uses_quantum_amount(self):
        player = QuantumRandomAgent("quantum_bot", 1000, [])

        with patch.object(QuantumRandomAgent, "quantum_randint", side_effect=[0, 250]) as quantum_randint:
            self.assertEqual(player.decision([cfg.bet], call=0), (cfg.bet, 250))

        self.assertEqual(quantum_randint.call_args_list[0].args, (0, 0))
        self.assertEqual(quantum_randint.call_args_list[1].args, (cfg.big_blind, 1000))

    def test_quantum_random_agent_short_stack_bet_can_be_all_in_below_big_blind(self):
        player = QuantumRandomAgent("quantum_bot", 40, [])

        with patch.object(QuantumRandomAgent, "quantum_randint", side_effect=[0, 40]):
            self.assertEqual(player.decision([cfg.bet], call=0), (cfg.bet, 40))

    def test_quantum_random_agent_raise_uses_quantum_amount_when_full_raise_available(self):
        player = QuantumRandomAgent("quantum_bot", 1000, [])

        with patch.object(QuantumRandomAgent, "quantum_randint", side_effect=[0, 300]) as quantum_randint:
            self.assertEqual(player.decision([cfg.raise_], call=250), (cfg.raise_, 300))

        self.assertEqual(quantum_randint.call_args_list[1].args, (cfg.big_blind, 750))

    def test_quantum_random_agent_raise_uses_round_min_raise(self):
        player = QuantumRandomAgent("quantum_bot", 1000, [])

        with patch.object(QuantumRandomAgent, "quantum_randint", side_effect=[0, 500]) as quantum_randint:
            self.assertEqual(player.decision([cfg.raise_], call=250, min_raise=400), (cfg.raise_, 500))

        self.assertEqual(quantum_randint.call_args_list[1].args, (400, 750))

    def test_quantum_random_agent_short_all_in_raise_uses_remaining_chips(self):
        player = QuantumRandomAgent("quantum_bot", 150, [])

        with patch.object(QuantumRandomAgent, "quantum_randint", return_value=0) as quantum_randint:
            self.assertEqual(player.decision([cfg.raise_], call=100), (cfg.raise_, 50))

        quantum_randint.assert_called_once_with(0, 0)

    def test_quantum_randint_rejects_invalid_range(self):
        with self.assertRaises(ValueError):
            QuantumRandomAgent.quantum_randint(5, 4)

    def test_quantum_randint_returns_fixed_value_without_quantum_backend(self):
        self.assertEqual(QuantumRandomAgent.quantum_randint(7, 7), 7)


if __name__ == "__main__":
    unittest.main()
