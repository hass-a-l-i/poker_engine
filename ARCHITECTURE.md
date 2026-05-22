# Architecture Notes

These notes describe the intended shape of the poker engine while it is still
being refactored.

## Main Responsibilities

`Card`

- Represents one playing card.
- Validates suit and rank.

`Deck`

- Owns the list of remaining cards.
- Creates a standard 52-card deck.
- Shuffles and deals cards.

`Player`

- Owns player state: name, chips, hand, current bet, active/folded status.
- Provides shared behaviour for human and bot players.

`Human` / `Agent`

- Choose actions.
- Should return an `(action, amount)` tuple.
- Should not directly mutate the round state.

`Round`

- Runs one betting round.
- Tracks whose turn it is.
- Tracks the current highest bet.
- Tracks how many players still need to act.
- Applies fold, check, call, and bet actions.
- Should not evaluate poker hands.

`Table` / future `Game`

- Owns full-hand flow.
- Deals community cards.
- Runs betting rounds for preflop, flop, turn, and river.
- Detects whether the hand ends by folds or by showdown.
- Awards the pot.

`HandEvaluator`

- Future class or module.
- Takes a player's hole cards plus community cards.
- Returns a comparable hand strength.
- Decides showdown winners.

## Important State Distinctions

`active`

- Means the player is still in the hand.
- Becomes `False` when a player folds.

`players_to_act`

- Means the number of active players who still need to respond in the current
  betting round.
- Decreases after fold, check, or call.
- Resets after a bet or raise because other players must respond.

These two pieces of state are related but not interchangeable.

## Current Simplification

The current prototype should ignore advanced poker edge cases until the base
loop works reliably.

Postponed:

- all-in behaviour
- side pots
- split pots
- multiple hands with rotating blinds
- strong bot strategy

This keeps the next milestone small: one complete hand from deal to winner.
