from typing import List
from abc import ABCMeta, abstractmethod
from Q.Common.Board.tile import Tile
from Q.Common.Turn.turn import Turn
from Q.Common.public_player_data import PublicPlayerData


class Player(metaclass=ABCMeta):
    """
    Player interface
    """
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def setup(self, pub_data: PublicPlayerData, tiles: List[Tile]):
        """
        The player is handed the initial map and a set of initial tiles.
        """
        raise NotImplementedError

    @abstractmethod
    def take_turn(self, s: PublicPlayerData) -> Turn:
        """
        The player may pass, ask for a tile replacement, or request a map extension
        """
        raise NotImplementedError

    @abstractmethod
    def win(self, w: bool):
        """
        The player is informed whether it won or not
        """
        raise NotImplementedError

    @abstractmethod
    def new_tiles(self, st: List[Tile]):
        """
        The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        raise NotImplementedError
      