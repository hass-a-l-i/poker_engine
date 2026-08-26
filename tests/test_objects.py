"""
Robust testing suite for Objects used in engine
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[1]
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

from poker_engine.config.cfg import PokerSkeleton
from poker_engine.objects.Card import Card
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Player import Player
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table


cfg = PokerSkeleton()
spade, diamond, club, heart = cfg.suits


def card(suit=spade, rank="A"):
    return Card(f"{suit}{rank}")


def card_key(card_obj):
    return card_obj.suit, card_obj.rank


class CardObjectTests(unittest.TestCase):
    def test_card_parses_suit_and_rank(self):
        spade_two = Card(f"{spade}2")
        diamond_nine = Card(f"{diamond}9")

        self.assertEqual(spade_two.suit, spade)
        self.assertEqual(diamond_nine.suit, diamond)
        self.assertEqual(spade_two.rank, "2")
        self.assertEqual(diamond_nine.rank, "9")
        self.assertEqual(str(spade_two), f"|{spade}2|")
        self.assertEqual(str(diamond_nine), f"|{diamond}9|")

    def test_card_accepts_ten_rank(self):
        ten = Card(f"{heart}10")

        self.assertEqual(ten.suit, heart)
        self.assertEqual(ten.rank, "10")
        self.assertEqual(str(ten), f"|{heart}10|")

    def test_card_rejects_invalid_lengths(self):
        for value in ("", spade, f"{spade}100"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Card(value)

    def test_card_rejects_unknown_suit_or_rank(self):
        with self.assertRaises(ValueError):
            Card("XA")
        with self.assertRaises(ValueError):
            Card(f"{spade}1")

    def test_card_numeric_values_follow_config_order(self):
        self.assertEqual(Card(f"{spade}2").get_rank_numeric(), 1)
        self.assertEqual(Card(f"{spade}A").get_rank_numeric(), 13)
        self.assertEqual(Card(f"{spade}A").get_suit_numeric(), 1)
        self.assertEqual(Card(f"{heart}A").get_suit_numeric(), 4)

    def test_card_getters_return_parsed_values(self):
        ace = Card(f"{club}A")

        self.assertEqual(ace.get_suit(), club)
        self.assertEqual(ace.get_rank(), "A")


class DeckObjectTests(unittest.TestCase):
    def test_initialised_deck_has_52_unique_cards(self):
        deck = Deck.initialise()
        keys = [card_key(item) for item in deck.state]

        self.assertEqual(len(deck), 52)
        self.assertEqual(len(set(keys)), 52)
        self.assertEqual(set(key[0] for key in keys), set(cfg.suits))
        self.assertEqual(set(key[1] for key in keys), set(cfg.ranks))

    def test_deck_string_and_getitem_expose_card_order(self):
        cards = [card(spade, "A"), card(heart, "K")]
        deck = Deck(cards)

        self.assertIs(deck[0], cards[0])
        self.assertEqual(str(deck), f"|{spade}A| |{heart}K|")

    def test_deck_shuffle_preserves_card_set_and_size(self):
        deck = Deck.initialise()
        before = {card_key(item) for item in deck.state}

        deck.shuffle()

        self.assertEqual(len(deck), 52)
        self.assertEqual({card_key(item) for item in deck.state}, before)

    def test_deck_pop_defaults_to_top_and_supports_index(self):
        cards = [card(spade, "A"), card(heart, "K"), card(diamond, "Q")]
        deck = Deck(cards[:])

        self.assertEqual(card_key(deck.pop()), card_key(cards[0]))
        self.assertEqual(card_key(deck.pop(1)), card_key(cards[2]))
        self.assertEqual(len(deck), 1)

    def test_deck_copy_is_deep_copy(self):
        deck = Deck.initialise()
        copied = deck.copy()

        self.assertIsNot(copied, deck)
        self.assertIsNot(copied.state[0], deck.state[0])
        self.assertEqual([card_key(item) for item in copied.state], [card_key(item) for item in deck.state])

    def test_deck_add_accepts_only_cards(self):
        deck = Deck([])
        added = [card(spade, "A"), card(heart, "K")]

        deck.add(added)

        self.assertEqual(deck.state, added)
        with self.assertRaises(TypeError):
            deck.add(["not-card"])

    def test_deck_validate_rejects_non_cards_wrong_size_and_duplicates(self):
        with patch("poker_engine.objects.Deck.logger.error"):
            with self.assertRaises(TypeError):
                Deck(["not-card"] * 52).validate()

            with self.assertRaises(ValueError):
                Deck([card(spade, "A")]).validate()

            duplicate_deck = Deck.initialise()
            duplicate_deck.state[-1] = duplicate_deck.state[0]
            with self.assertRaises(ValueError):
                duplicate_deck.validate()


class PlayerObjectTests(unittest.TestCase):
    def test_player_defaults_are_set(self):
        player = Player("alice", 1000)

        self.assertEqual(player.name, "alice")
        self.assertEqual(player.chips, 1000)
        self.assertEqual(player.hand, [])
        self.assertEqual(player.current_bet, 0)
        self.assertTrue(player.active)
        self.assertIsNone(player.score)
        self.assertIsNone(player.rank)
        self.assertFalse(player.all_in)
        self.assertEqual(player.total_stake, 0)
        self.assertEqual(repr(player), "alice")

    def test_player_uses_provided_hand_object(self):
        hand = [card(spade, "A")]
        player = Player("alice", 1000, hand)

        self.assertIs(player.get_hand(), hand)

    def test_player_add_card_allows_exactly_two_cards(self):
        player = Player("alice", 1000)

        player.add_card(card(spade, "A"))
        player.add_card(card(heart, "K"))

        self.assertEqual(len(player.hand), 2)
        with self.assertRaises(ValueError):
            player.add_card(card(diamond, "Q"))

    def test_player_add_card_rejects_non_card(self):
        player = Player("alice", 1000)

        with self.assertRaises(TypeError):
            player.add_card("not-card")

    def test_player_hand_type_check_rejects_invalid_existing_hand(self):
        player = Player("alice", 1000, ["not-card"])

        with self.assertRaises(TypeError):
            player.hand_type_check()
        with self.assertRaises(TypeError):
            player.show_hand()
        with self.assertRaises(TypeError):
            player.hand_rank()

    def test_player_hand_len_check_rejects_overfull_hands(self):
        player = Player("alice", 1000, [card(spade, "A"), card(heart, "K")])
        with self.assertRaises(ValueError):
            player.hand_len_check()

        player.hand.append(card(diamond, "Q"))
        with self.assertRaises(ValueError):
            player.hand_len_check()

    def test_player_show_hand_rank_and_pop(self):
        player = Player("alice", 1000, [card(spade, "2"), card(heart, "A")])

        self.assertEqual(player.show_hand(), f"|{spade}2|  |{heart}A|")
        self.assertEqual(player.hand_rank(), 14)
        popped = player.pop()
        self.assertEqual(card_key(popped), (spade, "2"))
        self.assertEqual(len(player.hand), 1)

    def test_base_player_decision_must_be_implemented_by_subclass(self):
        player = Player("alice", 1000)

        with self.assertRaises(NotImplementedError):
            player.decision([], 0)

    def test_player_info_contains_current_state(self):
        player = Player("alice", 1000, [card(spade, "A")])
        player.current_bet = 50
        player.active = False

        info = player.info()

        self.assertIn("Name : alice", info)
        self.assertIn("Chips : 1000", info)
        self.assertIn(f"Hand : |{spade}A|", info)
        self.assertIn("Current bet : 50", info)
        self.assertIn("Active : False", info)


class TableObjectTests(unittest.TestCase):
    def make_table(self, players_count=3):
        players = [Player(f"p{idx}", 1000) for idx in range(players_count)]
        rnd = Round(players)
        return Table(players=players, deck=Deck.initialise(), rnd=rnd)

    def test_table_initialises_with_expected_defaults(self):
        table = self.make_table()

        self.assertEqual(table.cards, [])
        self.assertEqual(table.ranked_players, [])
        self.assertEqual(table.winners, [])
        self.assertFalse(table.end_game)
        self.assertEqual(table.button_idx, 0)

    def test_deal_gives_each_player_two_cards_and_reduces_deck(self):
        table = self.make_table(players_count=4)

        table._deal()

        self.assertEqual([len(player.hand) for player in table.players], [2, 2, 2, 2])
        self.assertEqual(len(table.deck), 44)

    def test_update_table_burns_one_card_and_deals_community_cards(self):
        table = self.make_table()

        table._update_table(3)

        self.assertEqual(len(table.cards), 3)
        self.assertEqual(len(table.round.burned), 1)
        self.assertEqual(len(table.deck), 48)

    def test_community_cards_string_uses_current_board(self):
        table = self.make_table()
        table.cards = [card(spade, "A"), card(heart, "K")]

        self.assertEqual(table._community_cards(), f"|{spade}A| |{heart}K|")

    def test_next_active_idx_wraps_and_skips_ineligible_players(self):
        table = self.make_table(players_count=4)
        table.players[0].active = False
        table.players[1].all_in = True

        self.assertEqual(table._next_active_idx(0), 2)
        self.assertEqual(table._next_active_idx(3), 3)

    def test_rotate_button_wraps_around_players(self):
        table = self.make_table(players_count=3)
        table.button_idx = 2

        table._rotate_button()

        self.assertEqual(table.button_idx, 0)

    def test_last_player_check_sets_end_game_for_single_player(self):
        table = self.make_table(players_count=1)

        table.last_player_check()

        self.assertTrue(table.end_game)

    def test_resolve_losers_removes_zero_stack_players_and_syncs_round(self):
        table = self.make_table(players_count=3)
        table.players[1].chips = 0
        table.players[1].hand = [card(spade, "A")]

        table.resolve_losers()

        self.assertEqual([player.name for player in table.players], ["p0", "p2"])
        self.assertIs(table.round.players, table.players)
        self.assertEqual(len(table.round.burned), 1)

    def test_reset_returns_all_cards_and_clears_hand_state(self):
        table = self.make_table(players_count=3)
        table._deal()
        table._update_table(3)
        for player in table.players:
            player.active = False
            player.all_in = True
            player.score = (1, 13)
            player.rank = "High Card"
            player.total_stake = 100
        table.winners = [table.players[0]]
        table.ranked_players = [(table.players[0], (1, 13))]

        table.reset()

        self.assertEqual(len(table.deck), 52)
        self.assertEqual(len({card_key(item) for item in table.deck.state}), 52)
        self.assertEqual(table.cards, [])
        self.assertEqual(table.round.burned, [])
        self.assertEqual(table.winners, [])
        self.assertEqual(table.ranked_players, [])
        self.assertTrue(all(player.active for player in table.players))
        self.assertTrue(all(not player.all_in for player in table.players))
        self.assertTrue(all(player.score is None for player in table.players))
        self.assertTrue(all(player.rank is None for player in table.players))
        self.assertTrue(all(player.total_stake == 0 for player in table.players))

    def test_resolve_winner_logs_readable_rankings(self):
        players = [Player("alice", 1000), Player("bob", 1000)]
        players[0].hand = [card(spade, "A"), card(heart, "A")]
        players[1].hand = [card(spade, "K"), card(heart, "Q")]
        table = Table(players=players, deck=Deck.initialise(), rnd=Round(players))
        table.cards = [
            card(club, "A"),
            card(diamond, "2"),
            card(club, "5"),
            card(heart, "8"),
            card(spade, "10"),
        ]

        with self.assertLogs("poker_engine.objects.Table", level="DEBUG") as captured:
            table.resolve_winner()

        rankings_log = captured.output[0]
        self.assertIn("Hand rankings:", rankings_log)
        self.assertIn(f"alice: hand=|{spade}A|  |{heart}A|, rank=Three of a Kind, score=(4, 13, 9, 7)", rankings_log)
        self.assertIn(f"bob: hand=|{spade}K|  |{heart}Q|", rankings_log)
        self.assertNotIn("[('alice'", rankings_log)


if __name__ == "__main__":
    unittest.main()
