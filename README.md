# Poker Engine

Python-based Texas Hold'em poker engine.

This project is currently focused on the core engine logic: cards, deck handling, 
players, betting actions, and round flow. It is not a complete poker game yet,
but the structure is being built so hand evaluation, table flow, and stronger
bot logic can be added later.

## Current Features

- Card and deck objects
- Deck initialisation and shuffling
- Player, human, and simple agent models
- Basic betting round loop
- Legal action checks for fold, check, call, and bet
- Table object for community cards
- Early CLI-based interaction

## Project Status

This repository is paused at an early engine prototype stage.

The next main milestone is to stabilise one complete hand flow:

1. Create players and deck
2. Deal hole cards
3. Run a betting round
4. Deal flop, turn, and river
5. Compare hands at showdown
6. Award the pot

Some edge cases, especially all-in behaviour and side pots, are intentionally
left for later.

## Structure

```text
src/poker_engine/
  config/      Shared poker constants
  models/      Human and agent player implementations
  objects/     Core domain objects such as Card, Deck, Player, Round, Table
  old/         Earlier implementation kept for reference during refactor
  engine.py    Current manual entry point for trying the engine
```

## Running Locally

From the project root:

Powershell:
```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe src\poker_engine\engine.py
```

Command Line:
```bat
set PYTHONPATH=src && .venv\Scripts\python.exe src\poker_engine\engine.py
```

## Learning Goals

This project is mainly being used to practise:

- object-oriented Python
- modelling stateful systems
- error handling
- testing game rules
- separating responsibilities between classes
- building a project that can grow over time

## Next Steps

See [TODO.md](TODO.md) for the current roadmap and restart checklist.
