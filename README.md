# Poker Engine

A Python package for running Texas Hold'em poker simulations from the command line or from another Python program.

The project models cards, decks, players, betting rounds, community-card streets, hand evaluation, all-in state, side pots, showdown ranking, and winner distribution. 

It includes both a human command-line player and a simple random agent, making it useful for automated simulations and experimenting with poker strategies.

## Features

- Standard 52-card deck with validation, shuffling, dealing, and card return.
- Player state tracking for chips, hole cards, active/folded status, all-in status, street bet, total hand stake, score, and rank.
- Human player model with command-line prompts for legal actions.
- Human players can type `quit` at any prompt to stop the game immediately.
- Random agent model for automated simulations.
- Texas Hold'em table flow:
  - dealer button rotation
  - small blind and big blind posting
  - pre-flop, flop, turn, and river streets
  - community-card dealing with burn cards
  - early hand ending when all but one player fold
  - automatic betting-street skipping when no meaningful action remains
- Betting engine support for check, call, bet, raise, fold, all-in calls, all-in bets, full raises, and short all-in raises.
- Side-pot construction and distribution across eligible players.
- Five-card hand evaluation from five to seven available cards.
- Console and file logging with readable betting, street, all-in, and showdown output.
- Installable package with both a console command and `python -m` entrypoint.
- Importable API for running games from your own scripts.
- Unit tests covering objects, betting rules, edge cases, entrypoints, models, hand evaluation, and stress invariants.

## Installation

From the project root, install the package into your virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

After installation, the package exposes:

- `poker-engine` as a console command
- `python -m poker_engine` as a module command
- `poker_engine.engine.run_game` as a Python API

## Command Line Usage

Run the default game with three random agents:

```powershell
.\.venv\Scripts\poker-engine.exe
```

Run a mixed game with three random agents and one human:

```powershell
.\.venv\Scripts\poker-engine.exe --random-agents 3 --humans 1
```

Run as a Python module:

```powershell
.\.venv\Scripts\python.exe -m poker_engine --random-agents 3 --humans 1
```

If your virtual environment is activated, the command is shorter:

```powershell
poker-engine --random-agents 3 --humans 1
```

View all CLI options:

```powershell
poker-engine --help
```

Available options:

```text
--random-agents     number of random agents to seat
--humans            number of human players to seat
--starting-chips    starting chip stack for each player
--quiet             hide detailed engine logs and only show the final winner
```

Example:

```powershell
poker-engine --random-agents 5 --humans 1 --starting-chips 2000
```

## Python API

Use the package from another Python file:

```python
from poker_engine.engine import run_game

table = run_game(random_agents=3, humans=1, starting_chips=1000)

print(table.players)
print(table.winners)
```

Use quiet mode from Python when you only want the final winner printed:

```python
from poker_engine.engine import run_game

table = run_game(random_agents=3, humans=1, starting_chips=1000, quiet=True)
```

Run a non-interactive simulation:

```python
from poker_engine.engine import run_game

table = run_game(random_agents=4, humans=0, starting_chips=1000)

for player in table.players:
    print(player.name, player.chips)
```

Build players manually when you need direct control:

```python
from poker_engine.models.RandomAgent import RandomAgent
from poker_engine.objects.Deck import Deck
from poker_engine.objects.Round import Round
from poker_engine.objects.Table import Table

players = [
    RandomAgent("bot_1", 1000, []),
    RandomAgent("bot_2", 1000, []),
    RandomAgent("bot_3", 1000, []),
]

round_state = Round(players)
deck = Deck.initialise()
table = Table(players=players, deck=deck, rnd=round_state)
table.run()
```

## Human Input

Human players are prompted only with legal actions for their current state.

Example:

```text
---------- human_1's turn ----------
Hand        : |♣2|  |♦10|
Chips       : 1000
Current bet : 0
To call     : 100
Actions     : 2: Call, 4: Raise, 5: Fold
Choose action >
```

Action IDs are defined in `PokerSkeleton`:

```text
1: Check
2: Call
3: Bet
4: Raise
5: Fold
```

When choosing `Bet` or `Raise`, the human player is prompted for an amount.

Type `quit` at any human action or amount prompt to stop the game immediately.

## Logging

Logging is enabled by default for command-line runs and writes to:

```text
src/poker_engine/logs/poker_engine.log
```

Logs are also streamed to the console in the same output stream as human prompts, so prompt and game output stay in order.

Example log lines:

```text
Initialised game with 3 random agents and 1 human
Pre-Flop
bot_1 posts small blind: 50
bot_2 posts big blind: 100
bot_3 calls 100. Chips remaining : 900
bot_2 is all-in!
Flop : |♥10| |♣Q| |♦5|
Hand rankings: bot_1: hand=|♣2|  |♦10|, rank=Pair, score=(2, 7, 9, 8, 5)
```

Use quiet mode when you only want to see who won:

```powershell
poker-engine --quiet
```

Disable detailed logging from Python:

```python
from poker_engine.engine import run_game

table = run_game(random_agents=4, humans=0, quiet=True)
```

Even with logging disabled, `run_game` still prints the final winner when the game completes.

## Package Structure

```text
src/poker_engine/
  __main__.py          module entrypoint for python -m poker_engine
  engine.py            cli parser, game setup, and run_game api
  config/
    cfg.py             fixed poker constants and action ids
  models/
    Human.py           command-line human player
    RandomAgent.py     random automated player
  objects/
    Card.py            card parsing and numeric ordering
    Deck.py            deck lifecycle and validation
    HandEval.py        five-card hand scoring from holdem cards
    Illegal_Move.py    betting validation and quit exceptions
    Player.py          base player state and hand helpers
    Round.py           betting-round state machine
    Table.py           table, streets, showdown, side pots, and game loop
```

## Core Concepts

`Card`
: Parses and stores a suit/rank card such as `♠A` or `♦10`.

`Deck`
: Builds, validates, shuffles, deals, and receives returned cards.

`Player`
: Stores shared player state. Human and agent models inherit from this class.

`Round`
: Handles betting state, legal actions, chip commitment, all-in state, blinds, raises, and betting-round completion.

`Table`
: Coordinates full Hold'em hands: dealing, streets, blinds, active players, showdown, side pots, winners, resets, and button movement.

`HandEval`
: Scores the best five-card poker hand from five to seven cards.

## Betting Rules

The betting engine validates:

- players cannot act after folding or going all-in
- checks are allowed only when the player has matched the current bet
- calls are allowed only when there is an outstanding bet
- bets must be positive and cannot exceed the player's stack
- bets below the big blind are allowed only when the player is all-in
- raises must include enough chips beyond the call amount
- full raises reopen action
- short all-in raises do not reopen action
- betting streets end when no player can act or only one player can act with no pending call decision

## Showdown And Pots

At showdown, each active player is evaluated using their two hole cards and the community cards. Players are sorted by score tuple, winners are selected by the best score, and pots are distributed.

Side pots are built from each player's `total_stake`, with folded players contributing dead money but not remaining eligible to win.

Odd chips are distributed to the first winner in the tied winner order for that pot.

## Running Tests

Run the full test suite with unittest:

```powershell
.\.venv\Scripts\python.exe -m unittest
```

Run focused suites:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_betting
.\.venv\Scripts\python.exe -m unittest tests.test_rule_edges
.\.venv\Scripts\python.exe -m unittest tests.test_hand_eval
```

The suite covers:

- card and deck invariants
- player state helpers
- betting validation
- all-in and raise edge cases
- side-pot distribution
- hand evaluation rankings
- table lifecycle and reset behavior
- command-line entrypoint behavior
- random-agent behavior
- seeded stress simulations

## Development Notes

This package uses a `src` layout and setuptools metadata in `pyproject.toml`.

Editable install is recommended while developing:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

After editing code, run:

```powershell
.\.venv\Scripts\python.exe -m unittest
```

## Requirements

- Python 3.10 or newer
- numpy

Dependencies are declared in `pyproject.toml`.

## Scope

This project is a complete command-line and importable Texas Hold'em simulation engine for deterministic engine testing, human-vs-agent play, and random-agent simulations. It is intentionally focused on engine behavior rather than a graphical interface, online multiplayer, persistence, or advanced bot strategy training.
