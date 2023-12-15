from dataclasses import dataclass
from typing import List, Union

from Q.Common.Board.tile import Tile
from Q.Common.Turn.turn_outcome import TurnOutcome


@dataclass
class PlayerGameState:
    """
    Information the game state knows about the referee
    """
    name: str
    hand: List[Tile]
    points: int
