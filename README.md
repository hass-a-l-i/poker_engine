# Poker Simulator

Python-based Texas Hold'em poker simulator.

Incomplete draft. Edge cases to be added as well as bot strategies.

## Current Features

- Card and deck objects
- Deck initialisation and shuffling
- Player, human, and simple agent models
- Basic betting round loop
- Legal action checks for fold, check, call, and bet
- Table object for community cards
- Early CLI-based interaction

## Project Status

This repository is at an early engine prototype stage.

All-in behaviour and side pots, are intentionally left for later.

## Structure

```text
src/poker_engine/
  config/      Global constants
  models/      Human and agent player implementations
  objects/     Core objects such as Card, Deck, Player, Round, Table
  archive/     Earlier implementation kept for reference during refactor
  engine.py    Manual entry point for trying the engine
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
## Goals

To create a poker simulator package with plug-and-play strategies.
Allows users to test specific strategies against one another.
Reinforcement learning bots and quantum optimization will be testable here too.
Post simulation metrics will be standardized with potential add-ons pending.

## Next Steps

See [TODO.md](TODO.md) for the current roadmap and restart checklist.
