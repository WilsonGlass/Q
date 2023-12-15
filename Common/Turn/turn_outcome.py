from enum import Enum


class TurnOutcome(Enum):
    """
    Represents different types of outcomes of turns in the Q game
    """
    PLACED = "placed"
    REPLACED = "replaced"
    PASSED = "passed"



