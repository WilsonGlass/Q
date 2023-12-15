from copy import deepcopy
from typing import List

from Q.Common.Board.tile import Tile
from Q.Player.Strategy.dag import Dag
from Q.Common.Turn.turn import Turn

from Q.Player.Strategy.strategy import Strategy
from Q.Common.public_player_data import PublicPlayerData
from Q.Player.base import Player


class Player(Player):
    """
    Implementation of a Player which follows a well-defined Strategy
    """
    def __init__(self, name: str, strategy: Strategy = Dag(), hand: List[Tile] = []):
        """
        Initializes a player with a given name, strategy and hand for the Q Game
        """
        self._name = name
        self.strategy = strategy
        self.hand = hand

    def name(self) -> str:
        """
        Returns the player's name
        """
        return self._name

    def setup(self, pub_data: PublicPlayerData, tiles: List[Tile]):
        """
        Sets up the game by giving the player their tiles.
        """
        self.hand = pub_data.current_player_data.hand

    def take_turn(self, s: PublicPlayerData) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        return self.strategy.get_turn(s, deepcopy(self.hand))

    def win(self, w: bool) -> None:
        """
        From specs: the player is informed whether it won or not
        :param w: boolean value to be used to inform the player whether they won
        """
        if w:
            print("You won!")
        else:
            print("You lost!")

    def new_tiles(self, st: List[Tile]):
        """
        From specs: The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        self.hand = st
      