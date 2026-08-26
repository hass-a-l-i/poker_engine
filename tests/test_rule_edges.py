"""
Tests for specific edge cases likely to be missed by poker engines
"""
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
import logging

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from poker_engine.config.cfg import PokerSkeleton
from poker_engine.models.Human import Human
from poker_engine.models.RandomAgent import RandomAgent
from poker_engine.objects.Card import Card
from poker_engine.objects.Deck import Deck
from poker_engine.objects.HandEval import HandEval
from poker_engine.objects.Illegal_Move import GameQuit
from poker_engine.objects.Player import Player
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table


cfg = PokerSkeleton()
SPADE, DIAMOND, CLUB, HEART = cfg.suits


def card(suit, rank):
    return Card(f"{suit}{rank}")


def cards(*values):
    return [card(suit, rank) for suit, rank in values]


class ScriptedPlayer(Player):
    def __init__(self, name, chips, actions=None):
        super().__init__(name, chips, [])
        self.actions = list(actions or [])

    def decision(self, legal_actions, call):
        if not self.actions:
            raise AssertionError(f"No scripted action left for {self.name}")
        return self.actions.pop(0)


class QuittingPlayer(Player):
    def decision(self, legal_actions, call):
        raise GameQuit(f"{self.name} quit the game.")


class RoundRuleEdgeTests(unittest.TestCase):
    def make_players(self, stacks):
        return [Player(f"p{idx}", stack) for idx, stack in enumerate(stacks)]

    def test_legal_moves_when_no_bet_has_check_and_bet_only(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)

        self.assertEqual(rnd._legal_move(players[0]), [cfg.check, cfg.bet])

    def test_legal_moves_facing_bet_for_short_stack_call_only_no_raise(self):
        players = self.make_players([40, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100

        self.assertEqual(rnd._legal_move(players[0]), [cfg.fold, cfg.call])

    def test_folded_and_all_in_players_have_no_legal_moves(self):
        players = self.make_players([1000, 0])
        players[0].active = False
        players[1].all_in = True
        rnd = Round(players)

        self.assertEqual(rnd._legal_move(players[0]), [])
        self.assertEqual(rnd._legal_move(players[1]), [])

    def test_single_betting_capable_player_cannot_open_betting(self):
        players = self.make_players([1000, 0, 0])
        players[1].all_in = True
        players[2].all_in = True
        rnd = Round(players)

        with self.assertLogs("poker_engine.objects.Round", level="DEBUG") as captured:
            self.assertTrue(rnd.end_round())

        self.assertIn("Only one player can act: p0", captured.output[0])
        self.assertEqual(rnd._legal_move(players[0]), [cfg.check])

    def test_single_betting_capable_player_can_still_answer_unmatched_bet(self):
        players = self.make_players([1000, 0])
        players[0].current_bet = 50
        players[1].current_bet = 100
        players[1].all_in = True
        rnd = Round(players)
        rnd.highest_bet = 100

        self.assertFalse(rnd.end_round())
        self.assertEqual(rnd._legal_move(players[0]), [cfg.fold, cfg.call, cfg.raise_])

    def test_one_active_player_left_is_logged(self):
        players = self.make_players([1000, 1000])
        players[1].active = False
        rnd = Round(players)

        with self.assertLogs("poker_engine.objects.Round", level="DEBUG") as captured:
            self.assertTrue(rnd.end_round())

        self.assertIn("Only one player left: p0", captured.output[0])

    def test_all_in_raise_logs_action_before_all_in_status(self):
        players = self.make_players([1000, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100

        with self.assertLogs("poker_engine.objects.Round", level="DEBUG") as captured:
            rnd.resolve_action(players[0], cfg.raise_, 900)

        self.assertIn(
            "p0 calls 100 and raises 900. Total committed : 1000. Chips remaining : 0",
            captured.output[0],
        )
        self.assertIn("p0 is all-in!", captured.output[1])

    def test_full_raise_updates_highest_bet_min_raise_and_reopens_action(self):
        players = self.make_players([1000, 1000, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100
        rnd.min_raise = 100
        players[0].current_bet = 50
        players[0].total_stake = 50
        rnd.players_to_act = 1

        rnd.resolve_action(players[0], cfg.raise_, 150)

        self.assertEqual(players[0].chips, 800)
        self.assertEqual(players[0].current_bet, 250)
        self.assertEqual(players[0].total_stake, 250)
        self.assertEqual(rnd.highest_bet, 250)
        self.assertEqual(rnd.min_raise, 150)
        self.assertEqual(rnd.players_to_act, 2)

    def test_short_all_in_raise_does_not_reopen_action(self):
        players = self.make_players([120, 1000, 1000])
        rnd = Round(players)
        rnd.highest_bet = 100
        rnd.min_raise = 100
        rnd.players_to_act = 2

        rnd.resolve_action(players[0], cfg.raise_, 20)

        self.assertTrue(players[0].all_in)
        self.assertEqual(players[0].current_bet, 120)
        self.assertEqual(rnd.highest_bet, 120)
        self.assertEqual(rnd.min_raise, 100)
        self.assertEqual(rnd.players_to_act, 1)

    def test_reset_betting_clears_street_bets_but_keeps_hand_stakes(self):
        players = self.make_players([900, 800])
        players[0].current_bet = 100
        players[0].total_stake = 100
        players[1].current_bet = 200
        players[1].total_stake = 200
        rnd = Round(players)
        rnd.highest_bet = 200

        rnd.reset_betting()

        self.assertEqual([p.current_bet for p in players], [0, 0])
        self.assertEqual([p.total_stake for p in players], [100, 200])
        self.assertEqual(rnd.highest_bet, 0)


class TableRuleEdgeTests(unittest.TestCase):
    def make_table(self, stacks, button_idx=0):
        players = [Player(f"p{idx}", stack) for idx, stack in enumerate(stacks)]
        rnd = Round(players)
        return Table(players=players, deck=Deck.initialise(), rnd=rnd, button_idx=button_idx)

    def test_heads_up_blind_positions_put_button_on_small_blind(self):
        table = self.make_table([1000, 1000], button_idx=0)

        self.assertEqual(table._blind_positions(), (0, 1))
        self.assertEqual(table._preflop_start_idx(big_blind_idx=1), 0)
        self.assertEqual(table._postflop_start_idx(), 1)

    def test_six_max_blind_positions_are_after_button(self):
        table = self.make_table([1000] * 6, button_idx=3)

        self.assertEqual(table._blind_positions(), (4, 5))
        self.assertEqual(table._preflop_start_idx(big_blind_idx=5), 0)
        self.assertEqual(table._postflop_start_idx(), 4)

    def test_postflop_start_skips_folded_and_all_in_players(self):
        table = self.make_table([1000, 1000, 1000, 1000], button_idx=0)
        table.players[1].active = False
        table.players[2].all_in = True

        self.assertEqual(table._postflop_start_idx(), 3)

    def test_player_mix_summary_describes_mixed_humans_and_agents(self):
        players = [
            RandomAgent("bot_0", 1000, []),
            RandomAgent("bot_1", 1000, []),
            Human("human", 1000, []),
        ]
        table = Table(players=players, deck=Deck.initialise(), rnd=Round(players))
        table.end_game = True

        with self.assertLogs("poker_engine.objects.Table", level="INFO") as captured:
            table.run()

        self.assertIn("Initialised game with 2 random agents and 1 human", captured.output[0])

    def test_player_mix_summary_describes_single_type_games(self):
        humans = [Human("human_0", 1000, []), Human("human_1", 1000, [])]
        agents = [RandomAgent("bot_0", 1000, []), RandomAgent("bot_1", 1000, [])]
        human_table = Table(players=humans, deck=Deck.initialise(), rnd=Round(humans))
        agent_table = Table(players=agents, deck=Deck.initialise(), rnd=Round(agents))

        self.assertEqual(human_table._player_mix_summary(), "2 humans")
        self.assertEqual(agent_table._player_mix_summary(), "2 random agents")

    def test_preflop_logs_before_blinds_are_posted(self):
        players = [RandomAgent("bot_0", 1000, []), RandomAgent("bot_1", 1000, [])]
        table = Table(players=players, deck=Deck.initialise(), rnd=Round(players))
        table_logger = logging.getLogger("poker_engine.objects.Table")

        def post_blinds():
            table_logger.info("posting blinds")
            return 0

        def end_by_folds_check():
            table.end_game = True
            return True

        with patch.object(table.deck, "shuffle"), \
                patch.object(table, "_deal"), \
                patch.object(table, "post_blinds", side_effect=post_blinds), \
                patch.object(table, "init_round"), \
                patch.object(table, "end_by_folds_check", side_effect=end_by_folds_check), \
                self.assertLogs("poker_engine.objects.Table", level="INFO") as captured:
            table.run()

        self.assertIn("Pre-Flop", captured.output[1])
        self.assertIn("posting blinds", captured.output[2])

    def test_button_rotates_after_fold_ended_hand(self):
        players = [
            ScriptedPlayer("button", 1000, actions=[(cfg.fold, 0)]),
            ScriptedPlayer("small", 1000, actions=[(cfg.fold, 0)]),
            ScriptedPlayer("big", 1000, actions=[]),
        ]
        table = Table(players=players, deck=Deck.initialise(), rnd=Round(players), button_idx=0)
        table.deck.shuffle()
        table._deal()
        preflop_start_idx = table.post_blinds()

        table.init_round("Pre-Flop", start_idx=preflop_start_idx)
        self.assertTrue(table.end_by_folds_check())

        self.assertEqual(table.button_idx, 1)
        self.assertEqual(len(table.deck), 52)
        self.assertEqual(sum(player.chips for player in table.players), 3000)

    def test_human_quit_ends_table_run(self):
        players = [
            QuittingPlayer("quitter", 1000),
            ScriptedPlayer("other", 1000, actions=[]),
        ]
        table = Table(players=players, deck=Deck.initialise(), rnd=Round(players))

        with self.assertLogs("poker_engine.objects.Table", level="INFO") as captured:
            table.run()

        self.assertTrue(table.end_game)
        self.assertTrue(any("quitter quit the game." in line for line in captured.output))

    def test_folded_contributor_dead_money_goes_to_remaining_eligible_player(self):
        table = self.make_table([0, 0, 0])
        table.players[0].total_stake = 100
        table.players[1].total_stake = 100
        table.players[2].total_stake = 100
        table.players[0].active = False
        table.players[1].active = False
        table.players[2].active = True
        table.round.pot = 300
        table.winners = [table.players[2]]

        table.distribute_winnings()

        self.assertEqual([player.chips for player in table.players], [0, 0, 300])

    def test_split_side_pot_distributes_odd_chip_to_first_winner(self):
        table = self.make_table([0, 0, 0])
        for player in table.players:
            player.total_stake = 101
            player.active = True
            player.score = (2, 13, 11, 8, 7)
        table.round.pot = 303
        table.winners = table.players[:]

        table.distribute_winnings()

        self.assertEqual([player.chips for player in table.players], [101, 101, 101])

    def test_distribute_winnings_logs_readable_payouts(self):
        table = self.make_table([0, 0])
        for player in table.players:
            player.total_stake = 5
            player.active = True
            player.score = (1, 13)
        table.players[0].score = (2, 13)
        table.round.pot = 10
        table.winners = [table.players[0]]

        with self.assertLogs("poker_engine.objects.Table", level="DEBUG") as captured:
            table.distribute_winnings()

        self.assertIn("Distributed pot 10: p0 wins 10", captured.output[0])
        self.assertNotIn("[('p0'", captured.output[0])

    def test_multi_layer_side_pot_distribution(self):
        table = self.make_table([0, 0, 0, 0])
        stakes = [50, 150, 300, 300]
        scores = [
            (9, 13),
            (1, 12, 10, 8, 7, 2),
            (2, 13, 11, 8, 7),
            (3, 6, 5, 13),
        ]
        for player, stake, score in zip(table.players, stakes, scores):
            player.total_stake = stake
            player.score = score
            player.active = True
        table.round.pot = sum(stakes)
        table.winners = [table.players[0]]

        table.distribute_winnings()

        self.assertEqual([player.chips for player in table.players], [200, 0, 0, 600])

class HandEvalRuleEdgeTests(unittest.TestCase):
    def score(self, *values):
        return HandEval(cards(*values)).score_tuple()

    def test_royal_ranks_must_be_same_suit_for_royal_flush(self):
        _, rank = self.score(
            (HEART, "A"),
            (DIAMOND, "K"),
            (CLUB, "Q"),
            (SPADE, "J"),
            (HEART, "10"),
            (HEART, "2"),
            (HEART, "3"),
        )

        self.assertEqual(rank, "Straight")

    def test_best_full_house_uses_highest_trip_and_pair_from_two_trips(self):
        score, rank = self.score(
            (SPADE, "A"),
            (DIAMOND, "A"),
            (CLUB, "A"),
            (SPADE, "K"),
            (DIAMOND, "K"),
            (CLUB, "K"),
            (HEART, "2"),
        )

        self.assertEqual(rank, "Full House")
        self.assertEqual(score, (cfg.hands_dict["Full House"], 13, 12))

    def test_flush_score_uses_best_five_suited_cards_only(self):
        score, rank = self.score(
            (HEART, "2"),
            (HEART, "5"),
            (HEART, "8"),
            (HEART, "J"),
            (HEART, "A"),
            (CLUB, "K"),
            (DIAMOND, "Q"),
        )

        self.assertEqual(rank, "Flush")
        self.assertEqual(score, (cfg.hands_dict["Flush"], 13, 10, 7, 4, 1))

    def test_invalid_hand_size_and_card_type_are_rejected(self):
        with self.assertRaises(ValueError):
            HandEval(cards((SPADE, "A"), (DIAMOND, "K"), (CLUB, "Q"), (HEART, "J")))

        with self.assertRaises(ValueError):
            HandEval(cards(
                (SPADE, "A"),
                (DIAMOND, "K"),
                (CLUB, "Q"),
                (HEART, "J"),
                (SPADE, "10"),
                (DIAMOND, "9"),
                (CLUB, "8"),
                (HEART, "7"),
            ))

        with self.assertRaises(TypeError):
            HandEval(cards((SPADE, "A"), (DIAMOND, "K"), (CLUB, "Q"), (HEART, "J")) + ["not-card"])


if __name__ == "__main__":
    unittest.main()
