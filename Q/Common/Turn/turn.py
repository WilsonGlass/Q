from dataclasses import dataclass, field
from typing import Dict

from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.Turn.turn_outcome import TurnOutcome


@dataclass
class Turn:
    """
    Represents a Turn a player can create in the Q Game
    """
    turn_outcome: TurnOutcome
    placements: Dict[Pos, Tile] = field(default_factory=dict)
