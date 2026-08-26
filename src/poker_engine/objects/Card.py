from poker_engine.config.cfg import PokerSkeleton
cfg = PokerSkeleton()


class Card:
    def __init__(self, card:str) -> None:
        """create a card from a suit and rank string."""
        if len(card) > 3 or len(card) < 2:
            raise ValueError("Valid suit and rank needed to construct Card object")
        suit:str = card[0]
        rank:str = card[1:]
        if suit not in cfg.suits:
            raise ValueError(f"The suit {suit} does not exist.")
        if rank not in cfg.ranks:
            raise ValueError(f"The rank {rank} does not exist.")

        self.suit:str = suit
        self.rank:str = rank

    def __str__(self) -> str:
        """return the printable card representation."""
        return f"|{self.suit}{self.rank}|"

    def get_suit(self) -> str:
        """return the card suit."""
        return self.suit
    def get_rank(self) -> str:
        """return the card rank."""
        return self.rank
    def get_rank_numeric(self) -> int:
        """return the rank as a configured numeric value."""
        rank_order: dict = {str(rank): idx + 1 for idx, rank in enumerate(cfg.ranks)}
        return rank_order[self.rank]
    def get_suit_numeric(self) -> int:
        """return the suit as a configured numeric value."""
        suit_order: dict = {str(suit): idx + 1 for idx, suit in enumerate(cfg.suits)}
        return suit_order[self.suit]
