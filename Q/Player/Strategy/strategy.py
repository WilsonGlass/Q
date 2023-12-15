from abc import ABC, abstractmethod
from typing import List
from Q.Common.Board.tile import Tile
from Q.Common.public_player_data import PublicPlayerData
from Q.Common.Turn.turn import Turn


class Strategy(ABC):
    """
    The interface for automated player strategies.
    """
    @abstractmethod
    def get_turn(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        """
        Gets the turn object depending on the current public player data
        """
        pass
