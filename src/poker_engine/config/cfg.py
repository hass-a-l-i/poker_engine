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
        "Royal Flush": 10,
        "Straight Flush": 9,
        "Four of a Kind": 8,
        "Full House": 7,
        "Flush": 6,
        "Straight": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "Pair": 2,
        "High Card": 1,
    }


