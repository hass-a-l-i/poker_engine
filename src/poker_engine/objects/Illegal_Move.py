class IllegalMoveError(Exception):
    """represent an invalid poker action."""
    pass


class GameQuit(Exception):
    """represent a user request to quit the game."""
    pass
