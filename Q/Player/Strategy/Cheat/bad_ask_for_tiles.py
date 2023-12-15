from Q.Common.Board.tile import Tile
from Q.Player.Strategy.Cheat.cheat import Cheat
from Q.Common.public_player_data import PublicPlayerData
from Q.Player.Strategy.strategy import Strategy
from Q.Common.Turn.turn import Turn
from typing import List, Optional

from Q.Common.Turn.turn_outcome import TurnOutcome


class BadAskForTiles(Cheat):
    """
    Represents a cheater's interface for requesting an invalid replacement
    """
    def cheat(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Optional[Turn]:
        if pub_data.num_ref_tiles < len(hand):
            return Turn(TurnOutcome.REPLACED, {})
