import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[1]
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

from poker_engine import engine
from poker_engine.objects.Card import Card
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Player import Player
from poker_engine.models.Human import Human
from poker_engine.models.RandomAgent import RandomAgent


class EngineEntrypointTests(unittest.TestCase):
    def test_engine_uses_current_human_model_not_archive_model(self):
        self.assertTrue(issubclass(engine.Human, Player))
        self.assertEqual(engine.Human.__module__, "poker_engine.models.Human")

    def test_engine_human_accepts_cards_from_current_deck(self):
        human = engine.Human("human", 1000, [])
        dealt_card = Deck.initialise().pop()

        human.add_card(dealt_card)

        self.assertIsInstance(human.hand[0], Card)

    def test_build_players_uses_requested_mix_and_stack(self):
        players = engine.build_players(random_agents=2, humans=1, starting_chips=500)

        self.assertEqual([type(player) for player in players], [RandomAgent, RandomAgent, Human])
        self.assertEqual([player.chips for player in players], [500, 500, 500])
        self.assertEqual([player.name for player in players], ["bot_1", "bot_2", "human_1"])

    def test_main_runs_configured_table(self):
        with patch("poker_engine.engine.run_game") as run_game:
            result = engine.main(["--random-agents", "2", "--humans", "0", "--quiet"])

        self.assertEqual(result, 0)
        run_game.assert_called_once_with(
            random_agents=2,
            humans=0,
            starting_chips=1000,
            quiet=True,
        )

    def test_run_game_returns_final_table(self):
        with patch("poker_engine.engine.show_logs") as show_logs, \
                patch("poker_engine.engine.Table.run") as table_run, \
                patch("builtins.print") as mock_print:
            table = engine.run_game(random_agents=2, humans=0, starting_chips=500, show_logging=False)

        self.assertEqual(len(table.players), 2)
        self.assertEqual([player.chips for player in table.players], [500, 500])
        show_logs.assert_called_once_with(False)
        table_run.assert_called_once()
        mock_print.assert_not_called()

    def test_run_game_prints_winner_even_when_logging_is_disabled(self):
        def finish_game(table):
            table.players = [table.players[0]]
            table.players[0].chips = 2000

        with patch("poker_engine.engine.show_logs") as show_logs, \
                patch("poker_engine.engine.Table.run", autospec=True, side_effect=finish_game), \
                patch("builtins.print") as mock_print:
            engine.run_game(random_agents=2, humans=0, quiet=True)

        show_logs.assert_called_once_with(False)
        mock_print.assert_called_once_with("Game winner: bot_1 with 2000 chips.")

    def test_run_game_rejects_invalid_player_counts(self):
        with self.assertRaises(ValueError):
            engine.run_game(random_agents=1, humans=0, show_logging=False)

    def test_main_rejects_too_few_players(self):
        with patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            engine.main(["--random-agents", "1", "--humans", "0"])


if __name__ == "__main__":
    unittest.main()
