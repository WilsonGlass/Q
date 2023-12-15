from copy import deepcopy
from Q.Common.Board.tile import Tile
from Q.Common.Turn.turn import Turn
from Q.Common.public_player_data import PublicPlayerData
from Q.Player.Strategy.cheater_strategy import CheaterStrategy
from Q.Player.behaved_player import Player
from typing import List
from Q.Player.base import Player


class Cheater(Player):
    """
    Represents a cheating player
    """
    def __init__(self, name, strategy: CheaterStrategy, hand: List[Tile] = []):
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
        Sets up the game by giving the player their tiles. We do not need to use the given_map but are keeping the
        parameter as this is a public API.
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
