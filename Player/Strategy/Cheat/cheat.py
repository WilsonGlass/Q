from abc import abstractmethod
from Q.Common.Board.tile import Tile
from Q.Player.Strategy.strategy import Strategy
from Q.Common.public_player_data import PublicPlayerData
from Q.Common.Turn.turn import Turn
from typing import List, Optional


class Cheat(Strategy):
    def get_turn(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Optional[Turn]:
        """
        Gets the turn object depending on the current public player data
        """
        return self.cheat(pub_data, hand)
    
    @abstractmethod
    def cheat(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        """
        Implements the cheating strategy
        """
        pass


