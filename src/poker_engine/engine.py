"""
main engine
"""

import argparse
import logging
import sys
from pathlib import Path

from poker_engine.config.cfg import PokerSkeleton
from poker_engine.models.Human import Human
from poker_engine.models.RandomAgent import RandomAgent
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table

cfg = PokerSkeleton()


def show_logs(show):
    """configure console and file logging for the engine."""
    if show:
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")

        log_dir = Path(__file__).resolve().parent / "logs"
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                            handlers=[
                                logging.FileHandler(filename=log_dir / "poker_engine.log", mode='w', encoding="utf-8"),
                                logging.StreamHandler(sys.stdout)
                            ]
                            )


def build_players(random_agents: int, humans: int, starting_chips: int):
    """create the configured mix of random agents and humans."""
    players = []
    for idx in range(random_agents):
        players.append(RandomAgent(f"bot_{idx + 1}", starting_chips, []))
    for idx in range(humans):
        players.append(Human(f"human_{idx + 1}", starting_chips, []))
    return players


def build_parser() -> argparse.ArgumentParser:
    """create the command line argument parser."""
    parser = argparse.ArgumentParser(description="run a texas hold'em poker simulation.")
    parser.add_argument(
        "--random-agents",
        type=int,
        default=3,
        help="number of random agents to seat.",
    )
    parser.add_argument(
        "--humans",
        type=int,
        default=0,
        help="number of human players to seat.",
    )
    parser.add_argument(
        "--starting-chips",
        type=int,
        default=cfg.start_chips,
        help="starting chip stack for each player.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="hide detailed engine logs and only show the final winner.",
    )
    return parser


def final_result_summary(table: Table) -> str:
    """return the final winner summary for a completed game."""
    if len(table.players) == 1:
        winner = table.players[0]
        return f"Game winner: {winner.name} with {winner.chips} chips."
    if table.winners:
        winners = ", ".join(player.name for player in table.winners)
        return f"Hand winner: {winners}."
    return ""


def run_game(
    random_agents: int = 3,
    humans: int = 0,
    starting_chips: int = cfg.start_chips,
    show_logging: bool = True,
    quiet: bool = False,
) -> Table:
    """run a poker game and return the final table state."""
    if random_agents < 0 or humans < 0:
        raise ValueError("player counts cannot be negative.")
    if random_agents + humans < 2:
        raise ValueError("at least two players are required.")
    if starting_chips <= 0:
        raise ValueError("starting chips must be positive.")

    show_logs(show_logging and not quiet)
    players = build_players(random_agents, humans, starting_chips)
    rnd = Round(players)
    deck = Deck.initialise()
    table = Table(players=players, rnd=rnd, deck=deck)
    table.run()
    summary = final_result_summary(table)
    if summary:
        print(summary)
    return table


def main(argv: list[str] | None = None) -> int:
    """run the poker engine from the command line."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.random_agents < 0 or args.humans < 0:
        parser.error("player counts cannot be negative.")
    if args.random_agents + args.humans < 2:
        parser.error("at least two players are required.")
    if args.starting_chips <= 0:
        parser.error("starting chips must be positive.")

    run_game(
        random_agents=args.random_agents,
        humans=args.humans,
        starting_chips=args.starting_chips,
        quiet=args.quiet,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
