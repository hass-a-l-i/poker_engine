from dataclasses import dataclass, field

@dataclass(frozen=True)
class PokerSkeleton:
    suits: tuple[str] = (
        '♠', 
        '♦', 
        '♣', 
        '♥'
    )
    ranks: tuple[str] = (
        '2', 
        '3', 
        '4', 
        '5', 
        '6', 
        '7', 
        '8', 
        '9', 
        '10', 
        'J', 
        'Q', 
        'K', 
        'A'
    )
    big_blind: int = 100
    small_blind: int = 50
    start_chips: int = 1000
    check: int = 1
    call: int = 2
    bet: int = 3
    raise_: int = 4
    fold: int = 5
    actions_dict = {
        1: "Check", 
        2: "Call", 
        3: "Bet", 
        4: "Raise",
        5: "Fold"
    }
    hands_dict = {
        "Royal Flush": 1,
        "Straight Flush": 2,
        "Four of a Kind": 3,######
        "Full House": 4,######
        "Flush": 5,######
        "Straight": 6,
        "Three of a Kind": 7,######
        "Two Pair": 8,######
        "Pair": 9,######
        "High Card": 10,
    }


